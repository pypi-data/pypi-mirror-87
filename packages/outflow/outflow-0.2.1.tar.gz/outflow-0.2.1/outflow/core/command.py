# -*- coding: utf-8 -*-
import inspect
import logging
from typing import List

from declic import Command as DeclicCommand
from declic import Group
from outflow.core.generic.metaclasses import Singleton
from outflow.core.generic.string import to_camel_case, to_snake_case
from outflow.core.library.tasks import PipelineArgs
from outflow.core.tasks.task import Task

logger = logging.getLogger(__name__)


class Command(Group, metaclass=Singleton):
    """
    Outflow base command
    """

    def __init__(self, *args, invokable=True, on_before=None, **kwargs):
        """Bypass the Group command init to avoid subparser instantiation if not needed

        Args:
            invokable (bool, optional): If False, show the help message when called and exit. Defaults to True.
            on_before ([type], optional): Callback called just before the task flow run. Defaults to None.
        """
        logger.debug(f"Initialize command '{self.__class__.__name__}'")

        self.allow_extra_args = False

        if kwargs.pop("allow_extra_args", False):
            self.allow_extra_args = True

        self.commands = {}
        self._subparsers = None

        # this function will be called before each invoke of the group
        # even if the group is not invokable
        self._on_before = on_before

        DeclicCommand.__init__(
            self,
            *args,
            name=to_snake_case(self.__class__.__name__),
            **kwargs,
        )
        self.add_arguments()

        self.invokable = invokable
        self.parser.description = self.__doc__

    @property
    def subparsers(self):
        """Initialize and get the argparse subparser

        Note: CLI positional arguments are not available for commands with associated subcommands

        TODO: implement this property in declic
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_subparsers()
        return self._subparsers

    def invoke(self, args, backend, extra_args):
        """
        Overrides invoke from declic.Group to call directly the main actor run method
        """

        # TODO: add chain support using the parent task list

        if not self.invokable:
            self.print_help()
            return 0

        if not self.allow_extra_args and extra_args:
            error_msg = (
                f'Unrecognized arguments: {" ".join(extra_args)} in command'
                f" {self.name}. If passing these arguments to your task is "
                f'intended behaviour, use "allow_extra_args=True" in the '
                f"subcommands decorator arguments"
            )
            raise Exception(error_msg)

        task_list = self.setup_tasks()

        # for single task, ensure the compute method receive a task list
        if not isinstance(task_list, list):
            if task_list is None:
                task_list = []
            else:
                task_list = [task_list]

        if len(task_list) < 1:
            return 0

        for task in task_list:
            task.terminating = True

        return backend.run(task_list=task_list)

    def main(self, argv=None, backend=None):
        args, extra_args = self.parser.parse_known_args(argv)

        # update the pipeline context with the CLI args
        backend.update_pipeline_context_args(args, extra_args)
        return args.__declic_invoke_function__(
            args, backend=backend, extra_args=extra_args
        )

    def __call__(self, argv=None, backend=None):
        return self.main(argv, backend=backend)

    def parser_add_mutually_exclusive_group(self, *args, **kwargs):
        return self.parser.add_mutually_exclusive_group(*args, **kwargs)

    def add_arguments(self):
        pass

    def setup_tasks(self) -> List[Task]:
        pass

    @classmethod
    def subcommand(cls, *args, name=None, **kwargs):
        """
        A decorator to declare a subcommand
        """

        with_task_context = kwargs.pop("with_task_context", False)

        def decorator(callback_or_command_class):
            is_class = inspect.isclass(callback_or_command_class)
            self = cls()

            if is_class:
                if not issubclass(callback_or_command_class, Command):
                    raise Exception(f"The command shall be a subclass of {Command}")
                SubClass = callback_or_command_class
            else:
                subclass_name = (
                    callback_or_command_class.__name__ if name is None else name
                )

                def add_arguments(self):
                    # get command parameters

                    callback = callback_or_command_class

                    try:
                        params = callback.__cli_params__
                    except AttributeError:
                        params = []

                    # add parameters to the parser
                    for param_args, param_kwargs in params:
                        self.add_argument(*param_args, **param_kwargs)

                def setup_tasks(self):
                    pipeline_args = PipelineArgs()

                    @Task.as_task(name=subclass_name, with_self=with_task_context)
                    def InnerTask(*args, **kwargs):
                        # filter task kwargs using subcommand keywords
                        if args:
                            kwargs.update({"self": args[0]})
                        return self.generic_callback(kwargs, callback_or_command_class)

                    task = InnerTask()
                    pipeline_args >> task
                    return [task]

                SubClass = type(
                    to_camel_case(subclass_name),
                    (Command,),
                    {"setup_tasks": setup_tasks, "add_arguments": add_arguments},
                )
            cmd = SubClass(*args, parent=self, **kwargs)
            self.add_command(cmd)
            return SubClass

        return decorator


def argument(*args, **kwargs):
    def decorator(func_or_command_subclass):
        if inspect.isclass(func_or_command_subclass):
            instance = func_or_command_subclass()
            instance.add_argument(*args, **kwargs)
        else:
            if not hasattr(func_or_command_subclass, "__cli_params__"):
                func_or_command_subclass.__cli_params__ = []
            func_or_command_subclass.__cli_params__.append((args, kwargs))
        return func_or_command_subclass

    return decorator


class RootCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, invokable=False, **kwargs)
