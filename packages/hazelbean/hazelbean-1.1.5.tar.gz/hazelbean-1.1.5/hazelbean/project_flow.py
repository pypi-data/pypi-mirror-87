import os, sys, types, inspect, logging, collections, time, copy
# import nose
from collections import OrderedDict
from osgeo import gdal, osr, ogr
import numpy as np
import hazelbean as hb
import multiprocessing

try:
    import anytree
except:
    'anytree is probably not needed except for project flow.'

L = hb.get_logger('project_flow')
L.setLevel(logging.INFO)

def op():
    pass

def run_iterator(p, task, iteration_counter):
    things_returned = []
    for child in task.children:
        L.info('non-parallel iter ' + str(iteration_counter) + ': Running task ' + str(child.name) + ' with iterator parent ' + child.parent.name + ' in dir ' + str(p.cur_dir))
        r = p.run_task(child)
        things_returned.append(r)

    return things_returned
def run_iterator_in_parallel(p, task, iteration_counter):
    things_returned = []
    for child in task.children:
        L.info('iter ' + str(iteration_counter) + ': Running task ' + str(child.name) + ' with iterator parent ' + child.parent.name + ' in dir ' + str(p.cur_dir))
        r = p.run_task(child)
        things_returned.append(r)

    return things_returned


class InputPath(object):
    """Defines a path where an object can be calculated, but also alternate file locations that if they exist, mean that the calculation should not be done and the
    existing object should be used instead. Checks first base_data (defined by HB installation), then model_base_data, then project_base_data, then recalculates into calculation_path
    if none exist.

    base_data_extension_dirs allows the file to have a different root directory structure if it is in a base data dir such that it is BASE_DATA_DIR + base_data_extension_dirs + file_name

    """
    def __init__(self, calculation_dir, file_name, projectflow_object, base_data_extension_dirs=None):
        self.calculation_dir = calculation_dir
        self.file_name = file_name
        self.p = projectflow_object

        self.path = None
        self.dir = None

        if base_data_extension_dirs is None:
            base_data_extension_dirs = hb.file_root(self.calculation_dir)

        self.calculation_path = os.path.join(self.calculation_dir, self.file_name)

        self.project_base_data_dir = os.path.join(self.p.project_base_data_dir, base_data_extension_dirs)
        self.model_base_data_dir = os.path.join(self.p.model_base_data_dir, base_data_extension_dirs)
        self.base_data_dir = os.path.join(self.p.project_base_data_dir, base_data_extension_dirs)

    def __repr__(self):
        return self.get_path(self.file_name)

    def __str__(self):
        return self.get_path(self.file_name)

    def get_path(self, file_name=None):
        if file_name is None:
            file_name = self.file_name

        if file_name is not None:
            if hb.path_exists(os.path.join(self.project_base_data_dir, file_name)) > 0:
                return os.path.join(self.project_base_data_dir, file_name)
            elif hb.path_exists(os.path.join(self.model_base_data_dir, file_name)) > 0:
                return os.path.join(self.model_base_data_dir, file_name)
            elif hb.path_exists(os.path.join(self.base_data_dir, file_name)) > 0:
                return os.path.join(self.base_data_dir, file_name)
            else:
                return os.path.join(self.calculation_dir, file_name)
        else:
            print(1234, self.calculation_dir, file_name)
            return os.path.join(self.calculation_dir, file_name)

    def get_dir(self, file_name=None):
        if file_name is not None:
            if hb.path_exists(os.path.join(self.project_base_data_dir, file_name)) > 0:
                return self.project_base_data_dir
            elif hb.path_exists(os.path.join(self.model_base_data_dir, file_name)) > 0:
                return self.model_base_data_dir
            elif hb.path_exists(os.path.join(self.base_data_dir, file_name)) > 0:
                return self.base_data_dir
            else:
                return self.calculation_dir
        else:
            return self.calculation_dir

class InputDir(object):

    def __init__(self, calculation_dir, projectflow_object):
        self.calculation_dir = calculation_dir
        self.p = projectflow_object

        self.project_base_data_dir = self.p.project_base_data_dir
        self.model_base_data_dir = self.p.model_base_data_dir
        self.base_data_dir = self.p.project_base_data_dir

    def __repr__(self):
        return self.get_dir()

    def __str__(self):
        return self.get_dir()

    def get_dir(self, file_name=None):
        if file_name is not None:
            if hb.path_exists(os.path.join(self.project_base_data_dir, file_name)) > 0:
                return self.project_base_data_dir
            elif hb.path_exists(os.path.join(self.model_base_data_dir, file_name)) > 0:
                return self.model_base_data_dir
            elif hb.path_exists(os.path.join(self.base_data_dir, file_name)) > 0:
                return self.base_data_dir
            else:
                return self.calculation_dir
        else:
            return self.calculation_dir

class Task(anytree.NodeMixin):
    def __init__(self, function, project=None, parent=None, type='task', **kwargs):
        """
        There are TWO basic types of parallelizataion. Tasks that aren't dependent sequentially,
        or tasks that are defined in a different, unrelated extent, but possibly with sequential tasks.
        This Iterator object is fo the latter type, iterating over some zonal definition.
        """

        self.function = function
        self.p = project
        self.type = type
        self.let_children_skip = False

        # Note that parent here is defined by anytree and it is not possible to set it to None, as parent has to be a Node
        if parent:
            self.parent = parent

        self.task_dir = kwargs.get('task_dir', None)

        self.name = self.function.__name__
        self.creates_dir = kwargs.get('creates_dir', True)
        self.logging_level = None  # Will be inherited from project flow or set explicitly

        if self.function.__name__ == 'execute':
            self.run = 1
            self.skip_existing = 1

        else:
            self.run = 0
            self.skip_existing = 0


class InputTask(anytree.NodeMixin):
    def __init__(self, function, project=None, parent=None, type='input_task', **kwargs):
        """
        Input Tasks are like Tasks but assume that you will not rerun anything whose file exists (and this, skip_existing is differently implemented).
        Input Tasks also check to see if a file of the same name already exists in p.project_base_data, p.model_base_data, or p.base_data
        """

        self.function = function
        self.p = project
        self.type = type

        # Note that parent here is defined by anytree and it is not possible to set it to None, as parent has to be a Node
        if parent:
            self.parent = parent

        self.task_dir = kwargs.get('task_dir', None)

        self.name = self.function.__name__
        self.creates_dir = kwargs.get('creates_dir', True)
        self.logging_level = None  # Will be inherited from project flow or set explicitly

        self.run = 1
        self.skip_existing = 1  # Will thus overwrite by default.

class OutputTask(anytree.NodeMixin):
    def __init__(self, function, project=None, parent=None, type='output_task', **kwargs):
        """
        Input Tasks are like Tasks but assume that you will not rerun anything whose file exists (and this, skip_existing is differently implemented).
        """

        self.function = function
        self.p = project
        self.type = type

        # Note that parent here is defined by anytree and it is not possible to set it to None, as parent has to be a Node
        if parent:
            self.parent = parent

        self.task_dir = kwargs.get('task_dir', None)

        self.name = self.function.__name__
        self.creates_dir = kwargs.get('creates_dir', True)
        self.logging_level = None  # Will be inherited from project flow or set explicitly

        self.run = 1
        self.skip_existing = 0  # Will thus overwrite by default.


class ProjectFlow(object):
    def __init__(self, project_dir=None):
        try:
            self.calling_script = inspect.stack()[1][1]
            self.script_dir = os.path.split(self.calling_script)[0]
        except:
            L.debug('Could not identify a calling script.')

        # self.calling_globals = inspect.stack()[1][0].f_globals


        ## PROJECT LEVEL ATTRIBUTES
        # Set the project-level logging level. Individual tasks can overwrite this.
        self.logging_level = logging.INFO

        # # WARNING, although this seems logical, it can mess up multiprocessing if L has a handler. Move back outside.
        # self.L = hb.get_logger('project_flow')

        # TODOO Renable run_dir separation.
        # If true, generates a random dirname and creates it in the folder determined by the following options.
        self.make_run_dir = False

        # If project_dir is not defined, use CWD.
        if project_dir:
            self.project_dir = project_dir
        else:
            self.project_dir = os.getcwd() # This may be temporary though because it may be overwritten by UI

        if not os.path.isdir(self.project_dir):
            try:
                hb.create_directories(self.project_dir)
            except:
                raise NotADirectoryError('A Project Flow object is based on defining a project_dir as its base, but we were unable to create the dir at the given path: ' + self.project_dir)

        self.ui_agnostic_project_dir = self.project_dir # The project_dir can be overwritten by a UI but it can be useful to know where it would have been for eg decing project_base_data_dir

        self.model_base_data_dir = os.path.abspath(os.path.join(self.ui_agnostic_project_dir, '../../base_data'))  # Data that must be redistributed with this project for it to work. Do not put actual base data here that might be used across many projects.
        self.base_data_dir = hb.BASE_DATA_DIR
        self.project_name = hb.file_root(self.project_dir)

        # args is used by UI elements.
        self.args = OrderedDict()

        self.task_paths = OrderedDict()

        self.prepend = '' # for logging

        # Functions are called via their position within a tree data structure.
        # The logic of the project is defined via the flow_tree to which tasks, batches, secenarios etc. are added and run top-to-bottom
        # The tree itself here is initialized by setting the function to be execute
        self.task_tree = Task(self.execute, 'Task tree') # NOTICE that this Task() has no parent. It is the root node.

        self.jobs = [] # Allow only 1 jobs pipeline

        # State variables that are passed into the task's funciton via p. attribtues
        self.cur_task = None
        self.cur_dir = None
        self.run_this = None
        self.skip_existing = None

        self.task_names_defined = [] # Store a list of tasks defined somewhere in the target script. For convenience, e.g., when setting runtime conditionals based on function names existence.

        self.input_dir = getattr(self, 'input_dir', os.path.join(self.project_dir, 'input'))
        self.output_dir = getattr(self, 'output_dir', os.path.join(self.project_dir, 'output'))


    def __str__(self):
        return 'Hazelbean ProjectFlow object. ' + hb.pp(self.__dict__, return_as_string=True)

    def __repr__(self):
        return 'Hazelbean ProjectFlow object. ' + hb.pp(self.__dict__, return_as_string=True)

    def set_project_dir(self, input_dir):
        self.project_dir = input_dir
        self.project_name = hb.file_root(self.project_dir)

        try:
            hb.create_directories(self.project_dir)
        except:
            raise NotADirectoryError('A Project Flow object is based on defining a project_dir as its base, but we were unable to create the dir at the given path: ' + self.project_dir)

        self.input_dir = os.path.join(self.project_dir, 'inputs')
        self.intermediate_dir = os.path.join(self.project_dir, 'intermediate')
        self.output_dir = os.path.join(self.project_dir, 'outputs')

    def write_args_to_project(self, args):
        L.debug('write_args_to_project.')
        for k, v in args.items():
            if k in self.__dict__:
                L.debug('Arg given to P via UI was already in P. Overwritting: ' + str(k) + ', ' + str(v) +', Original value: ' + str(self.__dict__[k]))
            self.__setattr__(k, v)

    def show_tasks(self):
        for pre, fill, task in anytree.RenderTree(self.task_tree):
            if task.name == 'ProjectFlow':
                L.info(pre + task.name)
            else:
                L.info(pre + task.name + ', running: ' + str(task.run) + ', overwriting: ' + str(task.skip_existing))

    def add_task(self, function, project=None, parent=None, type='task', **kwargs):
        """KWARGS: task_dir sets where this task will have as its cur_dir, overwritting the default logic"""
        if not project:
            project = self
        if not parent:
            parent = self.task_tree
        if not isinstance(function, collections.Callable):
            raise TypeError(
                'Fuction passed to add_task() must be callable. ' + str(function.__name__) + ' was not.')
        task = Task(function, self, parent=parent, type=type, **kwargs)

        self.task_names_defined.append(function.__name__)

        # Add attribute to the parent object (the ProjectFlow object) referencing the iterator_object
        setattr(self, task.name, task)

        # Tasks inherit by default the projects' logging level.
        task.logging_level = kwargs.get('logging_level', self.logging_level)


        return task

    def add_input_task(self, function, project=None, parent=None, type='input_task', **kwargs):
        """Input tasks by default save to the projects' input dir and are assumed to always check for file existence to skip anything slow."""
        if not project:
            project = self
        if not parent:
            parent = self.task_tree
        if not isinstance(function, collections.Callable):
            raise TypeError(
                'Function passed to add_task() must be callable. ' + str(function.__name__) + ' was not.')

        task_dir = kwargs.get('task_dir', os.path.join(self.input_dir, function.__name__))

        task = InputTask(function, self, parent=parent, type=type, task_dir=task_dir, **kwargs)

        self.task_names_defined.append(function.__name__)

        # Add attribute to the parent object (the ProjectFlow object) referencing the iterator_object
        setattr(self, task.name, task)

        # Tasks inherit by default the projects' logging level.
        task.logging_level = kwargs.get('logging_level', self.logging_level)


        return task

    def add_output_task(self, function, project=None, parent=None, type='output_task', **kwargs):
        """Input tasks by default save to the projects' input dir and are assumed to always check for file existence to skip anything slow."""
        if not project:
            project = self
        if not parent:
            parent = self.task_tree
        if not isinstance(function, collections.Callable):
            raise TypeError(
                'Fuction passed to add_task() must be callable. ' + str(function.__name__) + ' was not.')

        task_dir = kwargs.get('task_dir', os.path.join(self.output_dir, function.__name__))

        task = OutputTask(function, self, parent=parent, type=type, task_dir=task_dir, **kwargs)

        self.task_names_defined.append(function.__name__)

        # Add attribute to the parent object (the ProjectFlow object) referencing the iterator_object
        setattr(self, task.name, task)

        # Tasks inherit by default the projects' logging level.
        task.logging_level = kwargs.get('logging_level', self.logging_level)


        return task

    def add_iterator(self, function, project=None, parent=None, run_in_parallel=False, type='iterator', **kwargs):
        if not project:
            project = self
        if not parent:
            parent = self.task_tree

        if not isinstance(function, collections.Callable):
            raise TypeError('Fuction passed to add_iterator() must be callable. ' + str(function.__name__) + ' was not.')

        # Create the iterator object
        iterator = Task(function, self, parent=parent, type=type, **kwargs)
        iterator.run_in_parallel = run_in_parallel
        # Add attribute to the parent object (the ProjectFlow object) referencing the iterator_object
        setattr(self, iterator.name, iterator)

        # Tasks inherit by default the projects' logging level.
        iterator.logging_level = self.logging_level

        return iterator


    def run_task(self, current_task):
        for task in anytree.LevelOrderIter(current_task, maxlevel=1): # We ALWAYS have maxlevel = 1 even if there are nested things because it handles all nested children recursively and we don't want the tree iterator to find them. This is sorta stupid instead of just giving the tree itself at the top  node.
            # If the function is not the root execute function, go ahead and run it. Can't run execute this way because it doesn't have a parent.
            if not task.function.__name__ == 'execute':
                # Set task_dirs and cur_dirs based on tree position
                if task.parent.type == 'task':
                    if task.parent is not None and getattr(task.parent, 'task_dir', None):
                        if getattr(task, 'task_dir', None):
                            L.critical('Logic of task_dirs does not make sense here. In particular, a parent was given an explicit task_dir AND its child task was too instead of being derived')
                        else:
                            task.task_dir = os.path.join(task.parent.task_dir, task.function.__name__)
                    elif isinstance(task, (InputTask, OutputTask)):
                        # task.task_dir = hb.InputDir(task.task_dir, self)
                        pass
                    else:
                        if getattr(task, 'task_dir_override', None):
                            pass # Expected outcome if given an override. This case is for when you want to specify a task look somewhere else. Though note it is hard then to make the override programatically determined.
                        else:
                            task.task_dir = os.path.join(self.intermediate_dir, task.function.__name__)
                    self.cur_dir = task.task_dir
                elif task.parent.type == 'iterator':
                    task.task_dir = os.path.join(self.cur_dir_parent_dir, task.name)
                    self.cur_dir = task.task_dir
                else:
                    raise NameError('Unknown Node type')

                # Set the project level task_dirs object to have an attribute equal to the current name. This makes it possible for functions later in the analysis  script to have access to
                # previous task_dir locations.
                setattr(self, task.name + '_dir', task.task_dir)



                # In addition to self.cur_dir, there are also these two project-level convenience funcitons.
                self.cur_task = task
                self.run_this = task.run # NYI, task skipping enabled here.
                if isinstance(task, InputTask):#, GeneratedInputTask)):
                    self.skip_existing = 0  # Don't want to skip InputTasks because these have internal logig for what to skip.
                else:
                    self.skip_existing = task.skip_existing

                if self.skip_existing:
                    if os.path.exists(self.cur_dir):
                        self.run_this = 0

                if not os.path.exists(self.cur_dir.__str__()) and task.creates_dir and task.run and task.type != 'input_task':
                    pass
                    hb.create_directories(str(self.cur_dir))

                # # NYI, but I want to implement task-level logging conditionals.
                # L.setLevel(task.logging_level)
                if task.type in ['task', 'input_task', 'output_task']:
                    if self.run_this:
                        if task.creates_dir:
                            pass # NYI
                            # hb.create_directories(self.cur_dir)
                            # assert os.path.exists(self.cur_dir)

                        # If the task's parent is an iterator, we want to report different info, otherwise these are the same.
                        if task.parent.type == 'iterator':
                            if task.parent.let_children_skip:
                                try:
                                    r = task.function(self)
                                except:
                                    L.critical('FAILED TO RUN task with iterator parent: ' + str(task.name) + ' and loading from ' + str(self.cur_dir))
                            else:
                                r = task.function(self)
                        elif isinstance(task, InputTask):
                            self.prepend = ''
                            L.info(self.prepend + 'Running InputTask ' + str(task.name) + ' in dir ' + str(self.cur_dir))
                            task.function(self)  # Running the Task including anyting in p.run_this
                        elif isinstance(task, OutputTask):
                            self.prepend = ''
                            L.info(self.prepend + 'Running OutputTask ' + str(task.name) + ' in dir ' + str(self.cur_dir))
                            task.function(self)  # Running the Task including anyting in p.run_this
                        else:
                            self.prepend = ''
                            L.info(self.prepend + 'Running Task ' + str(task.name) + ' in dir ' + str(self.cur_dir))
                            task.function(self)  # Running the Task including anyting in p.run_this



                    # NYI, task skipping enabled here.
                    else:

                        if os.path.isdir(self.cur_dir):
                            if task.run:
                                if task.parent.type == 'iterator':
                                    L.info('Skipping task (with iterator parent) ' + str(task.name) + ' because the task_dir already existsed. Dir: ' + str(self.cur_dir))
                                    # task.run = 0
                                    r = task.function(self)
                                elif isinstance(task, InputTask):
                                    self.prepend = ''
                                    L.info(self.prepend + 'Running InputTask ' + str(task.name) + ' in dir ' + str(self.cur_dir))
                                    task.function(self)  # Running the Task including anyting in p.run_this
                                else:
                                    self.prepend = ''
                                    L.info('Skipping task ' + str(task.name) + ' because the task_dir already existsed. Dir: ' + str(self.cur_dir))
                                    task.function(self)  # Running the Task including anyting in p.run_this

                            else:
                                # L.info('Instructed to skip task ' + str(task.name) + ' and loading from ' + str(self.cur_dir))
                                if task.parent.type == 'iterator':
                                    r = task.function(self)
                                    #try:
                                    #    r = task.function(self)
                                    #except:
                                    #    L.critical('FAILED TO RUN task with iterator parent: ' + str(task.name) + ' and loading from ' + str(self.cur_dir))
                                else:
                                    self.prepend = ''
                                    task.function(self)  # Running the Task including anyting in p.run_this

                            # # CALL THE TASK FUNCTION
                            # task.function(p)  # Running the Task EXCLUDING anyting in p.run_this

                        # CONFUSED HERE, I think that I should have had this type of task not run. # Perhaps need to add multiple levels of _run_this, including silent, verbose, all, quick, indexing, etc.
                        else:
                            L.info('Skipping task ' + str(task.name) + ' because task.run was False')
                            if task.parent.type == 'iterator':
                                r = task.function(self)
                            elif isinstance(task, InputTask):
                                self.prepend = ''
                                # L.info(self.prepend + 'Running InputTask ' + str(task.name) + ' in dir ' + str(self.cur_dir))
                                task.function(self)  # Running the Task including anyting in p.run_this

                            else:
                                self.prepend = ''
                                task.function(self)  # Running the Task including anyting in p.run_this


                elif task.type == 'iterator':

                    # Run the function for defining the iterator
                    if task.run:
                        self.prepend += '    '
                        L.info('Creating iterator ' + str(task.name))
                        # HACK, I failed to understand why sometiems the dirs weren't created in time. Thus I force it here.
                        hb.create_directories(self.cur_dir)
                        assert os.path.exists(self.cur_dir)

                        task.function(self)
                        task.function(self)

                    else:
                        # NYI, task skipping enabled here.
                        # L.info('Skipping running Iterator.')
                        task.function(self)

            # Whether run or not, search for children
            if len(task.children) > 0:

                # If the current task is an iterator, then check for replacements before calling the child task.
                # Definition of the projects' self.iterator_replacements is the one part of ProjectFlow that the analysis script needs to be aware of,
                # creating a dict of key-value pairs that are replaced with each step in the iterator.
                if task.type == 'iterator' and task.run:

                    # First check dimensions of iterator_replacements:
                    replacement_lengths = []
                    for replacement_attribute_name, replacement_attribute_value in self.iterator_replacements.items():
                        replacement_lengths.append(len(replacement_attribute_value))
                        assert(len(set(replacement_lengths))==1) # Check that all of the same size.
                    num_iterations = replacement_lengths[0]

                    # self.run_in_parallel = True # TODOO Connect to UI
                    if not getattr(self, 'num_workers', None):
                        self.num_workers = multiprocessing.cpu_count() - 1
                    results = []

                    if task.run_in_parallel:
                        print('num_workers', self.num_workers)
                        # OPTIMIZATION NOTE: It's slow to spawn 460 processes when they are just going to be skipped, thus run_this for iterators needs to be improved.
                        worker_pool = multiprocessing.Pool(self.num_workers) # NOTE, worker pool and results are LOCAL variabes so that they aren't pickled when we pass the project object.

                    # Once all the iterations are done, iterate through the stored results and call their get functions, which blocks running past this point until all are done.
                    # SUPER CONFUSING POINT. the project object will be modified independently by all tasks. Cant think of a good way ro rejoin them
                    returns_from_parallel_tasks = []

                    parsed_iterable = []
                    print('num_iterations', num_iterations)
                    for iteration_counter in range(num_iterations):
                        to_append = []

                        # NOTICE strange dimensionality here: even within a single iteration, we have to iterate through self.iterator_replacements because we might have more than 1 var that needs replacing
                        replacements = OrderedDict()
                        for replacement_attribute_name, replacement_attribute_values in self.iterator_replacements.items():
                            # print(1111, replacement_attribute_name, replacement_attribute_values)
                            current_replacement_value = self.iterator_replacements[replacement_attribute_name][iteration_counter]
                            replacements[replacement_attribute_name] = replacement_attribute_values
                            setattr(self, replacement_attribute_name, current_replacement_value)
                            if replacement_attribute_name == 'cur_dir_parent_dir':
                                setattr(self, 'cur_dir', current_replacement_value)
                            project_copy = copy.copy(self)# Freeze it in place (necessary for parallelizing)

                        # For multiprocessing, you cannot pickle a Gdal DS or Band, so I manually unset them here. For some reason, using the k.close_data corrupted the geotiff headers
                        for i, k in project_copy.__dict__.items():
                            if type(k) in [hb.GlobalPyramidFrame, hb.ArrayFrame]:
                                k.band = None
                                k.ds = None
                                # k.close_data()

                        to_append.append(project_copy)
                        to_append.append(task)
                        to_append.append(iteration_counter)
                        parsed_iterable.append(tuple(to_append))



                    if task.run_in_parallel:
                        try:
                            L.info('Initializing PARALLEL tasks with iterable length: ' + str(len(parsed_iterable)))
                        except Exception as e:
                            L.info('Initializing PARALLEL task but failed or something\nException raised: ' + str(e))

                        # We use apply_async, which immediately lets the next line calculate. It is blocked below with results.get()
                        # result = worker_pool.apply_async(func=run_iterator_in_parallel, args=(project_copy, task, iteration_counter))

                        result = worker_pool.starmap(run_iterator_in_parallel, parsed_iterable)
                        # result = worker_pool.starmap_async(make_path_global_pyramid, parsed_iterable)
                        things_returned = []
                        if task.run:
                            for child in task.children:
                            #     for project_copy, task, iteration_counter in parsed_iterable:
                            #         L.info('parallel iter ' + str(iteration_counter) + ': Running task ' + str(
                            #             child.name) + ' with iterator parent ' + child.parent.name + ' in dir ' + str(
                            #             project_copy.cur_dir))
                            #         r = project_copy.run_task(child)
                            #         things_returned.append(r)
                            #
                                # print('child', child.name)
                                self.run_task(child)  # Run the child found by iterating the task-node's children
                        # for i in result.get():
                        #     results.append(i)
                        # worker_pool.close()
                        # worker_pool.join()
                    else:
                        things_returned = []
                        for child in task.children:
                            for project_copy, task, iteration_counter in parsed_iterable:
                                L.info('non-parallel iter ' + str(iteration_counter) + ': Running task ' + str(
                                    child.name) + ' with iterator parent ' + child.parent.name + ' in dir ' + str(
                                    project_copy.cur_dir))
                                r = project_copy.run_task(child)
                                things_returned.append(r)

                        # run_iterator(self, task, iteration_counter)




                # Task is an iterator's child
                else:
                    if task.run:
                        for child in task.children:
                            self.run_task(child)  # Run the child found by iterating the task-node's children

            # Task is not an iterator, thus we just call it's child directly
            elif task.parent is not None:
                if task.parent.type is 'iterator':
                    for child in task.children:
                        self.run_task(child)# Run the child found by iterating the task-node's children
            else:
                for child in task.children:
                    self.run_task(child)  # Run the child found by iterating the task-node's children

                    # raise NameError('wtf')
        try:
            if(len(r)) > 0:
                return r
        except:
            'nothing needed returning'

    def InputPath(self, dir, file_name, base_data_extension_dirs=None):
        """Thin wrapper so that InputPath calls itself with a reference to the ProjectFlow object, even if not given."""
        return hb.InputPath(dir, file_name, projectflow_object=self, base_data_extension_dirs=base_data_extension_dirs)

    # OPTIONAL START: Cool advance towards project-level logger management. Extent.
    def log(self, log_input):
        if self.cur_task.logging_level == 'debug':
            L.debug(log_input)
        if self.cur_task.logging_level == 'info':
            L.info(log_input)
        if self.cur_task.logging_level == 'warn':
            L.warn(log_input)
        if self.cur_task.logging_level == 'critical':
            L.critical(log_input)

    def execute(self, args=None):
        self.show_tasks()

        if not isinstance(self.task_tree, hb.Task):
            raise NameError('Execute was called in ProjectFlow but no tasks were in task_tree.')

        # Execute can be passed an args dict that can be, for instance, generated by a UI. If args exists, write each
        # key value pair as project object level attributes.
        if args:
            self.write_args_to_project(args)


        # Check to see if any args have been set that change runtime conditionals.
        if args:
            for k, v in args.items():
                if k.startswith('run_') and k.split('_', 1)[1] in self.task_names_defined:
                    a = getattr(self, k.split('_', 1)[1], None)
                    if a:
                        a.run = v


        # TRICKY NOTE: Workspace_dir and project_dir are often but not always the same. Project dir is defined by the model code while workspace dir is defined by the script or UI that is calling the model code.
        # If workspace_dir is defined, it will overwrite project_dir? Is this right?
        self.workspace_dir = getattr(self, 'workspace_dir', None)
        if self.workspace_dir: # Then there IS a UI, so use itz
            self.project_dir = self.workspace_dir
        # If no additional dirs are specified, assume inputs, intermediates and outputs all go in CWD
        # These are the DEFAULT LOCATIONS, but they could be changed by the UI or script calling it for example to make batch runs happen.

        self.intermediate_dir =  getattr(self, 'intermediate_dir', os.path.join(self.project_dir, 'intermediate'))

        # Because the UI will give '', need to overwrite this manually.
        # ALSO, this messed me up when I went to API calls as it wasnt properly being rewritten to based on the new worskpace dir. I'm thinking
        # I need to ditch the basis, intermediate etc setup for now to hone the existing. THEN add them back in
        # if self.intermediate_dir == '':
        #     self.intermediate_dir = os.path.join(self.project_dir, 'intermediate')

        self.output_dir = getattr(self, 'output_dir', os.path.join(self.project_dir, 'outputs'))


        L.debug('self.model_base_data_dir set to ' + str(self.model_base_data_dir))
        self.model_dir = os.path.join(self.ui_agnostic_project_dir, '../') # Model is the name of the application being developed. THis is referred to confusingly as a Project (in the reseracher's storage), and the model has its own projects, which are defined in this code

        L.debug('self.model_dir set to ' + str(self.model_dir))
        self.model_base_data_dir = os.path.abspath(os.path.join(self.ui_agnostic_project_dir, '../../base_data'))  # Data that must be redistributed with this project for it to work. Do not put actual base data here that might be used across many projects.

        self.project_base_data_dir = os.path.join(self.project_dir, 'project_base_data')  # Data that must be redistributed with this project for it to work. Do not put actual base data here that might be used across many projects.

        L.debug('self.project_base_data_dir set to ' + str(self.project_base_data_dir))
        self.temporary_dir = getattr(self, 'temporary_dir', os.path.join(hb.PRIMARY_DRIVE, 'temp'))  # Generates new run_dirs here. Useful also to set the numdal temporary_dir to here for the run.

        self.run_string = hb.pretty_time()  # unique string with time-stamp. To be used on run_specific identifications.
        self.basis_name = ''  # Specify a manually-created dir that contains a subset of results that you want to use. For any input that is not created fresh this run, it will instead take the equivilent file from here. Default is '' because you may not want any subsetting.
        self.basis_dir = os.path.join(self.intermediate_dir, self.basis_name)  # Specify a manually-created dir that contains a subset of results that you want to use. For any input that is not created fresh this run, it will instead take the equivilent file from here. Default is '' because you may not want any subsetting.

        # if self.make_run_dir:
        #     self.run_dir = getattr(self, 'run_dir', hb.make_run_dir(self.intermediate_dir))
        # else:
        #     self.run_dir = self.intermediate_dir

        # hb.create_directories([self.input_dir, self.intermediate_dir, self.output_dir])


        #### WARNING This was a decent idea (mayyybe), but it put a module in the global scope which meant that it couldn't be pickled in multiprocessing.
        # # Get all globally defined variables of type Path and add as project attributes
        # for k, v in self.calling_globals.items():
        #     if isinstance(v, hb.project_flow.Path):
        #         self.__setattr__(k, v)


        L.info('\nRunning Project Flow')
        self.run_task(self.task_tree) # LAUNCH the task tree. Everything else will be called via recursive task calls.

        L.info('Script complete.')


class Path(str):
    def __init__(self, input_path):
        self.path = input_path
        self.explode = hb.explode_path(self.path)

    def __call__(self, *args, **kwargs):
        return p.path

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

if __name__=='__main__':
    print ('cannot run by itself.')