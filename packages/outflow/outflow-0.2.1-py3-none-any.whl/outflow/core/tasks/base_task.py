# -*- coding: utf-8 -*-
from copy import deepcopy
from uuid import uuid4

from outflow.core.generic.string import to_camel_case
from outflow.core.pipeline.context import PipelineContext
from outflow.core.workflow import Workflow

from .exceptions import TaskException
from .metaclass import TaskMeta


class BaseTask(metaclass=TaskMeta):
    inputs = None
    outputs = None
    parameters = None

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # reset the targets definition attribute to avoid sharing targets definition with subclasses
        cls.inputs = {}
        cls.outputs = {}
        cls.parameters = {}

    def __init__(self, *args, **kwargs):
        self.uuid = uuid4()
        self.bind_kwargs = kwargs
        self.workflow = Workflow(self)
        self.terminating = False
        self.parallel_workflow_id = None
        self.parallel_workflow_nb = None
        self.num_cpus = 1
        self.context: PipelineContext = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def add_input(cls, target):
        # create the targets def dict if not defined
        cls.inputs.update({target.name: target})

    @classmethod
    def add_output(cls, target):
        cls.outputs.update({target.name: target})

    @classmethod
    def add_parameter(cls, target):
        cls.parameters.update({target.name: target})

    @property
    def id(
        self,
    ):
        return self.name + "-" + str(self.uuid)

    @classmethod
    def as_task(
        cls,
        run_func=None,
        *,
        name=None,
        with_self=False,
        checkpoint=False,
        parallel=False,
    ):
        """
        Transform the decorated function into a outflow task.

        Args:
            run_func: The decorated function.
            name (str): Name of the task. By default, this is the name of the
                function in snake case.
            with_self (bool): If true, the run function will be called as a
                regular method, so the "self" of the task is available in the
                task code.
            checkpoint (bool): *NOT IMPLEMENTED* If true, save output targets
                in configured location, and skip tasks if files exists.
            parallel (bool): If true, the task will be running in its own
                actor, so it can run concurrently as other parallel tasks.

        Returns:
            A task class that run the decorated function
        """

        if checkpoint:
            raise NotImplementedError

        if run_func is None:

            def inner_function(_run_func):
                return cls.as_task(
                    _run_func,
                    name=name,
                    with_self=with_self,
                    checkpoint=checkpoint,
                    parallel=parallel,
                )

            return inner_function
        else:
            if name is None:
                name = run_func.__name__

            task_class = type(
                to_camel_case(name),
                (cls,),
                {"run": run_func, "parallel": parallel, "with_self": with_self},
            )

            return task_class

    def __lshift__(self, task_or_list):
        """
        Link task or list of tasks

        Example: task_or_list = self << task_or_list
        """

        if isinstance(task_or_list, list):
            for task in task_or_list:
                self << task
        else:
            self.add_parent(task_or_list)

        return task_or_list

    def __rshift__(self, task_or_list):
        """
        Link task or list of tasks

        Example: task_or_list = self >> task_or_list
        """
        if isinstance(task_or_list, list):
            for task in task_or_list:
                self >> task
        else:
            task_or_list.add_parent(self)

        return task_or_list

    @staticmethod
    def add_edge(parent_task, child_task):
        if parent_task.workflow is None and child_task.workflow is None:
            workflow = Workflow(parent_task)
            workflow.add_node(child_task)
        elif parent_task.workflow is None:
            workflow = child_task.workflow
            workflow.add_node(parent_task)
        elif child_task.workflow is None:
            workflow = parent_task.workflow
            workflow.add_node(child_task)
        elif parent_task.workflow is not child_task.workflow:
            parent_task.workflow.merge(child_task.workflow)
            workflow = parent_task.workflow
        else:
            workflow = parent_task.workflow

        workflow.add_edge(parent_task, child_task)

    def add_child(self, child_task):
        self.add_edge(self, child_task)

    def add_parent(self, parent_task):
        self.add_edge(parent_task, self)

    @property
    def parents(self):
        return self.workflow.get_parents(self)

    @property
    def children(self):
        return self.workflow.get_children(self)

    def run(self, *args, **kwargs):
        pass

    @property
    def parameterized_kwargs(self):
        """Generate the parameters kwargs dict from the config file content

        'parameterized_kwargs' refers to parameters used as task arguments and declared in the configuration file.

        Raises:
            TaskException: Raise an exception if task parameters are set but no parameters configuration is found

        Returns:
            dict: kwargs dict generated from the config file content
        """
        if self.parameters:
            try:
                kwargs = self.context.config["tasks"][self.name]["parameters"]
            except KeyError as err:
                raise TaskException(
                    f"Could not find parameters of task {self.name} in configuration file"
                ) from err
        else:
            kwargs = {}
        return kwargs

    def __call__(self, *args, **kwargs):
        if args:
            raise Exception(
                "Task use keyword-only arguments but positional arguments were passed to the run function"
            )

    def bind(self, **kwargs):
        self.bind_kwargs.update(kwargs)

    def copy(self):
        task_copy = deepcopy(self)
        task_copy.uuid = uuid4()
        return task_copy
