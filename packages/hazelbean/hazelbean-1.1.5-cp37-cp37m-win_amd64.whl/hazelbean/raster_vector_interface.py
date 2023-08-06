import os, sys, shutil, random, math, atexit, time
from collections import OrderedDict
import functools
from functools import reduce
from osgeo import gdal, osr, ogr
import numpy as np
import random
import multiprocessing
import multiprocessing.pool
import hazelbean as hb
import scipy
import geopandas as gpd
import warnings
import netCDF4
import logging
import pandas as pd
import pygeoprocessing.geoprocessing as pgp
from pygeoprocessing.geoprocessing import *

# Conditional imports
try:
    import geoecon as ge
except:
    ge = None

numpy = np
L = hb.get_logger('hb_rasterstats')
pgp_logger = logging.getLogger('geoprocessing')

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

def convert_polygons_to_id_raster(input_vector_path, output_raster_path, match_raster_path,
                                  id_column_label=None, data_type=None, ndv=None, all_touched=None, compress=True):
    if not id_column_label:
        # Get the column label of the first column
        gdf = gpd.read_file(input_vector_path)
        id_column_label = gdf.columns[0]

    if not data_type:
        data_type = 1

    if not ndv:
        ndv = 255
    band_nodata_list = [ndv]

    option_list = list(hb.DEFAULT_GTIFF_CREATION_OPTIONS)
    if all_touched:
        option_list.append("ALL_TOUCHED=TRUE")

    option_list.append("ATTRIBUTE=" + str(id_column_label))

    if compress:
        option_list.append("COMPRESS=DEFLATE")
    hb.new_raster_from_base_pgp(match_raster_path, output_raster_path, data_type, band_nodata_list, gtiff_creation_options=option_list)
    burn_values = [1]  # will be ignored because attribute set but still needed.

    # option_list = []


    # The callback here is useful, but rather than rewrite the funciton, we just locallay reset the PGP logger level.
    prior_level = pgp_logger.getEffectiveLevel()
    pgp_logger.setLevel(logging.INFO)
    pgp.rasterize(input_vector_path, output_raster_path, burn_values, option_list, layer_id=0)
    pgp_logger.setLevel(prior_level)


def zonal_statistics_flex(input_raster,
                          zone_vector_path,
                          zone_ids_raster_path=None,
                          id_column_label=None,
                          zones_raster_data_type=None,
                          values_raster_data_type=None,
                          zones_ndv=None,
                          values_ndv=None,
                          all_touched=None,
                          assert_projections_same=True,
                          unique_zone_ids=None,
                          csv_output_path=None,
                          vector_output_path=None,
                          stats_to_retrieve='sums',
                          enumeration_classes=None,
                          multiply_raster_path=None,
                          verbose=False,
                          rewrite_zone_ids_raster=True,
                          max_enumerate_value=1000,):
    """ if zone_ids_raster_path is set, use it and/or create it for later processing speed-ups.

     Big caveat on unique_zone_ids: must start at 1 and be sequential by zone. Otherwise, if left None, will just test first 10000 ints. This speeds up a lot not having to have a lookup.
     """
    input_path = hb.get_flex_as_path(input_raster)
    base_raster_path_band = (input_path, 1)




    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    if assert_projections_same:
        hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path])
    else:
        pass
        # a = hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path], return_result=True)
        # if not a:
        #     L.critical('Ran zonal_statistics_flex but the inputs werent in identical projections.')

  # if zone_ids_raster_path is not defined, use the PGP version, which doesn't use a rasterized approach.
    if not zone_ids_raster_path and rewrite_zone_ids_raster is False:
        to_return = pgp.zonal_statistics(
            base_raster_path_band, zone_vector_path,
            aggregate_layer_name=None, ignore_nodata=True,
            polygons_might_overlap=True, working_dir=None)
        if csv_output_path is not None:
            hb.python_object_to_csv(to_return, csv_output_path)
        return to_return

    # if zone_ids_raster_path is defined, then we are using a rasterized approach.
    # NOTE that by construction, this type of zonal statistics cannot handle overlapping polygons (each polygon is just represented by its id int value in the raster).
    else:
        if zones_ndv is None:
            zones_ndv = -9999

    if values_ndv is None:
        values_ndv = hb.get_raster_info_hb(input_raster)['nodata'][0]

    # Double check in case get_Raster fails
    if values_ndv is None:
        values_ndv = -9999.0

    # if zone_ids_raster_path is given, use it to speed up processing (creating it first if it doesnt exist)
    if not os.path.exists(zone_ids_raster_path) and rewrite_zone_ids_raster is not False:
        # Calculate the id raster and save it
        if verbose:
            L.info('Creating id_raster with convert_polygons_to_id_raster')
        hb.convert_polygons_to_id_raster(zone_vector_path, zone_ids_raster_path, input_raster, id_column_label=id_column_label, data_type=zones_raster_data_type,
                                         ndv=zones_ndv, all_touched=all_touched)
    else:
        if verbose:
            L.info('Zone_ids_raster_path existed, so not creating it.')
        # hb.assert_gdal_paths_have_same_geotransform([zone_ids_raster_path, input_raster])
    print('unique_zone_ids', unique_zone_ids)
    if unique_zone_ids is None:
        gdf = gpd.read_file(zone_vector_path)
        print('gdf', gdf)
        unique_zone_ids_pre = np.unique(gdf[id_column_label][gdf[id_column_label].notnull()]).astype(np.int64)
        # unique_zone_ids_pre = unique_zone_ids_pre[0]

        to_append = []
        if 0 not in unique_zone_ids_pre:
            to_append.append(0)
        # if zones_ndv not in unique_zone_ids_pre:
        #     to_append.append(zones_ndv)
        unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre))
        # unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre) + [max(unique_zone_ids_pre) + 1])

    if verbose:
        L.info('Starting zonal_statistics_rasterized using zone_ids_raster_path at ' + str(zone_ids_raster_path))

    # Call zonal_statistics_rasterized to parse vars into cython-format and go from there.


    if stats_to_retrieve == 'sums':
        L.debug('Exporting sums.')
        L.debug('unique_zone_ids', unique_zone_ids)
        unique_ids, sums = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        df = pd.DataFrame(index=unique_ids, data={'sums': sums})
        df[df == 0] = np.nan
        df.dropna(inplace=True)
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'sums_counts':
        L.debug('Exporting sums_counts.')
        unique_ids, sums, counts = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        df = pd.DataFrame(index=unique_ids, data={'sums': sums, 'counts': counts})
        df[df == 0] = np.nan
        df.dropna(inplace=True)
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'enumeration':
        L.debug('Exporting enumeration.')

        if enumeration_classes is None:
            enumeration_classes = hb.unique_raster_values_path(input_raster)
        unique_ids, enumeration = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, enumeration_classes=enumeration_classes, multiply_raster_path = multiply_raster_path, verbose=verbose, )

        enumeration = np.asarray(enumeration)
        df = pd.DataFrame(index=unique_ids, columns=[str(i) for i in list(range(0, len(enumeration_classes)))], data=enumeration)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')
            gdf_no_geom = gdf.drop(columns='geometry')

        if csv_output_path is not None:
            gdf_no_geom.to_csv(csv_output_path)


        return df


def zonal_statistics_rasterized(zone_ids_raster_path, values_raster_path, zones_ndv=None, values_ndv=None, zone_ids_data_type=None,
                                values_data_type=None, unique_zone_ids=None, stats_to_retrieve='sums', enumeration_classes=None, multiply_raster_path=None, verbose=True, max_enumerate_value=1000):
    """
    Calculate zonal statistics using a pre-generated raster ID array.

    NOTE that by construction, this type of zonal statistics cannot handle overlapping polygons (each polygon is just represented by its id int value in the raster).
    """

    if verbose:
        L.info('Starting to run zonal_statistics_rasterized using iterblocks.')

    if unique_zone_ids is None:
        if verbose:
            L.info('Load zone_ids_raster and compute unique values in it. Could be slow (and could be pregenerated for speed if desired).')

        zone_ids = hb.as_array(zone_ids_raster_path)
        unique_zone_ids = np.unique(zone_ids).astype(np.int64)
        L.warning('Generated unique_zone_ids via brute force. This could be optimized.', str(unique_zone_ids))
        zone_ids = None
    else:
        unique_zone_ids = unique_zone_ids.astype(np.int64)

    # Get dimensions of rasters for callback reporting'
    zone_ds = gdal.OpenEx(zone_ids_raster_path)
    n_cols = zone_ds.RasterYSize
    n_rows = zone_ds.RasterXSize
    n_pixels = n_cols * n_rows

    # Create new arrays to hold results.
    # NOTE THAT this creates an array as long as the MAX VALUE in unique_zone_ids, which means there could be many zero values. This
    # is intended as it increases computation speed to not have to do an additional lookup.
    aggregated_sums = np.zeros(len(unique_zone_ids), dtype=np.float64)
    aggregated_counts = np.zeros(len(unique_zone_ids), dtype=np.int64)

    last_time = time.time()
    pixels_processed = 0

    # Iterate through block_offsets
    zone_ids_raster_path_band = (zone_ids_raster_path, 1)
    aggregated_enumeration = None
    for c, block_offset in enumerate(list(hb.iterblocks(zone_ids_raster_path_band, offset_only=True))):
        sample_fraction = None # TODOO add this in to function call.
        # sample_fraction = .05
        if sample_fraction is not None:
            if random.random() < sample_fraction:
                select_block = True
            else:
                select_block = False
        else:
            select_block = True

        if select_block:
            block_offset_new_gdal_api = {
                'xoff': block_offset['xoff'],
                'yoff': block_offset['yoff'],
                'buf_ysize': block_offset['win_ysize'],
                'buf_xsize': block_offset['win_xsize'],
            }

            zones_ds = gdal.OpenEx(zone_ids_raster_path)
            values_ds = gdal.OpenEx(values_raster_path)
            # No idea why, but using **block_offset_new_gdal_api failed, so I unpack it manually here.
            try:
                zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.int64)
                values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)

            except:
                L.critical('unable to load' + zone_ids_raster_path + ' ' + values_raster_path)
                pass
                # zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.int64)
                # values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.float64)

            if zones_array.shape != values_array.shape:
                L.critical('zones_array.shape != values_array.shape', zones_array.shape, values_array.shape)

            unique_zone_ids_np = np.asarray(unique_zone_ids, dtype=np.int64)

            if len(unique_zone_ids_np) > 1000:
                L.critical('Running zonal_statistics_flex with many unique_zone_ids: ' + str(unique_zone_ids_np))

            if stats_to_retrieve=='sums':
                sums = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
                aggregated_sums += sums
            elif stats_to_retrieve == 'sums_counts':
                sums, counts = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
                aggregated_sums += sums
                aggregated_counts += counts
            elif stats_to_retrieve == 'enumeration':
                if multiply_raster_path is not None:
                    multiply_ds = gdal.OpenEx(multiply_raster_path)
                    multiply_raster = multiply_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
                else:
                    multiply_raster = np.asarray([[1]], dtype=np.float64)
                enumeration = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                        stats_to_retrieve=stats_to_retrieve, enumeration_classes=np.asarray(enumeration_classes, dtype=np.int64), multiply_raster=multiply_raster)

                if aggregated_enumeration is None:
                    aggregated_enumeration = np.copy(enumeration)
                else:
                    aggregated_enumeration += enumeration
            pixels_processed += block_offset_new_gdal_api['buf_xsize'] * block_offset_new_gdal_api['buf_ysize']

            last_time = hb.invoke_timed_callback(
                last_time, lambda: L.info('Zonal statistics rasterized percent complete:', float(pixels_processed) / n_pixels * 100.0), 3)
    if stats_to_retrieve == 'sums':
        return unique_zone_ids, aggregated_sums
    elif stats_to_retrieve == 'sums_counts':
        return unique_zone_ids, aggregated_sums, aggregated_counts
    elif stats_to_retrieve == 'enumeration':

        return unique_zone_ids, aggregated_enumeration

def extract_correspondence_and_categories_dicts_from_df_cols(input_df, broad_col, narrow_col):
    set_differences = hb.compare_sets(input_df[broad_col], input_df[narrow_col])

    correspondence = {}
    categories = {}
    for i in set_differences['right_set']:
        categories[i] = []
    for i in set_differences['left_set']:
        correspondence[i] = input_df[input_df[broad_col] == i][narrow_col].values[0]
        categories[input_df[input_df[broad_col] == i][narrow_col].values[0]].append(i)
    return correspondence, categories



def get_vector_info_PGP_REFERENCE(vector_path, layer_index=0):
    """Get information about an OGR vector (datasource).

    Parameters:
        vector_path (str): a path to a OGR vector.
        layer_index (int): index of underlying layer to analyze.  Defaults to
            0.

    Raises:
        ValueError if `vector_path` does not exist on disk or cannot be opened
        as a gdal.OF_VECTOR.

    Returns:
        raster_properties (dictionary): a dictionary with the following
            properties stored under relevant keys.

            'projection' (string): projection of the vector in Well Known
                Text.
            'bounding_box' (list): list of floats representing the bounding
                box in projected coordinates as [minx, miny, maxx, maxy].

    """
    vector = gdal.OpenEx(vector_path, gdal.OF_VECTOR)
    if not vector:
        raise ValueError(
            "Could not open %s as a gdal.OF_VECTOR" % vector_path)
    vector_properties = {}
    layer = vector.GetLayer(iLayer=layer_index)
    # projection is same for all layers, so just use the first one
    spatial_ref = layer.GetSpatialRef()
    if spatial_ref:
        vector_sr_wkt = spatial_ref.ExportToWkt()
    else:
        vector_sr_wkt = None
    vector_properties['projection'] = vector_sr_wkt
    layer_bb = layer.GetExtent()
    layer = None
    vector = None
    # convert form [minx,maxx,miny,maxy] to [minx,miny,maxx,maxy]
    vector_properties['bounding_box'] = [layer_bb[i] for i in [0, 2, 1, 3]]
    return vector_properties


def get_raster_info_PGP_REFERENCE(raster_path):
    """Get information about a GDAL raster (dataset).

    Parameters:
       raster_path (String): a path to a GDAL raster.

    Raises:
        ValueError if `raster_path` is not a file or cannot be opened as a
        gdal.OF_RASTER.

    Returns:
        raster_properties (dictionary): a dictionary with the properties
            stored under relevant keys.

            'pixel_size' (tuple): (pixel x-size, pixel y-size) from
                geotransform.
            'mean_pixel_size' (float): the average size of the absolute value
                of each pixel size element.
            'raster_size' (tuple):  number of raster pixels in (x, y)
                direction.
            'nodata' (list): a list of the nodata values in the bands of the
                raster in the same order as increasing band index.
            'n_bands' (int): number of bands in the raster.
            'geotransform' (tuple): a 6-tuple representing the geotransform of
                (x orign, x-increase, xy-increase,
                 y origin, yx-increase, y-increase).
            'datatype' (int): An instance of an enumerated gdal.GDT_* int
                that represents the datatype of the raster.
            'projection' (string): projection of the raster in Well Known
                Text.
            'bounding_box' (list): list of floats representing the bounding
                box in projected coordinates as [minx, miny, maxx, maxy]
            'block_size' (tuple): underlying x/y raster block size for
                efficient reading.

    """
    raster = gdal.OpenEx(raster_path, gdal.OF_RASTER)
    if not raster:
        raise ValueError(
            "Could not open %s as a gdal.OF_RASTER" % raster_path)
    raster_properties = {}
    projection_wkt = raster.GetProjection()
    if not projection_wkt:
        projection_wkt = None
    raster_properties['projection'] = projection_wkt
    geo_transform = raster.GetGeoTransform()
    raster_properties['geotransform'] = geo_transform
    raster_properties['pixel_size'] = (geo_transform[1], geo_transform[5])
    raster_properties['mean_pixel_size'] = (
            (abs(geo_transform[1]) + abs(geo_transform[5])) / 2.0)
    raster_properties['raster_size'] = (
        raster.GetRasterBand(1).XSize,
        raster.GetRasterBand(1).YSize)
    raster_properties['n_bands'] = raster.RasterCount
    raster_properties['nodata'] = [
        raster.GetRasterBand(index).GetNoDataValue() for index in range(
            1, raster_properties['n_bands'] + 1)]
    # blocksize is the same for all bands, so we can just get the first
    raster_properties['block_size'] = raster.GetRasterBand(1).GetBlockSize()

    # we dont' really know how the geotransform is laid out, all we can do is
    # calculate the x and y bounds, then take the appropriate min/max
    x_bounds = [
        geo_transform[0], geo_transform[0] +
                          raster_properties['raster_size'][0] * geo_transform[1] +
                          raster_properties['raster_size'][1] * geo_transform[2]]
    y_bounds = [
        geo_transform[3], geo_transform[3] +
                          raster_properties['raster_size'][0] * geo_transform[4] +
                          raster_properties['raster_size'][1] * geo_transform[5]]

    raster_properties['bounding_box'] = [
        numpy.min(x_bounds), numpy.min(y_bounds),
        numpy.max(x_bounds), numpy.max(y_bounds)]

    # datatype is the same for the whole raster, but is associated with band
    raster_properties['datatype'] = raster.GetRasterBand(1).DataType
    raster = None
    return raster_properties
























