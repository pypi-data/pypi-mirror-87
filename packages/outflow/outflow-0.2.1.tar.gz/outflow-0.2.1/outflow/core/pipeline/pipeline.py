# -*- coding: utf-8 -*-
import argparse
import importlib
import logging.config
import os
import pathlib
import sys

from outflow import __version__ as outflow_version
from outflow.core.logging import logger, set_plugins_loggers_config
from outflow.core.pipeline.context import PipelineContext
from outflow.core.plugin import Plugin


class Pipeline:

    system_arguments = {
        "config": (
            ["--config"],
            {"help": "The path to the config file."},
        ),
        "settings": (
            ["--settings"],
            {
                "help": 'The Python path to a settings module, e.g. "my_project.my_settings". If this isn\'t provided, the OUTFLOW_SETTINGS_MODULE environment variable will be used.'
            },
        ),
        "version": (
            ["--version"],
            {"help": "Show program's version number and exit.", "action": "store_true"},
        ),
        "python_path": (
            ["--python_path"],
            {
                "help": 'A directory to add to the Python path, e.g. "/home/pipeline_projects/my_project".',
                "action": "append",
                "default": [],
            },
        ),
        "traceback": (
            ["--traceback"],
            {"help": "Display exception tracebacks."},
        ),
        "no_color": (
            ["--no_color"],
            {"help": "Don't colorize the command output."},
        ),
        "log_level": (
            ["-ll", "--log-level"],
            {
                "help": "Specifies the amount information that the pipeline should print to the console ",
                "choices": ("DEBUG", "INFO", "WARNING", "ERROR"),
            },
        ),
        "local_mode": (
            ["-L", "--local-mode"],
            {"help": "Force local mode", "action": "store_true"},
        ),
    }

    base_arguments = {
        "dry_run": (
            ["--dry_run"],
            {"help": "Run the pipeline without the database", "action": "store_true"},
        ),
    }

    def __init__(
        self,
        *,
        root_directory: str = None,
        settings_module: str = "settings",
        argv=None,
        force_dry_run: bool = False,
    ):
        """Init the pipeline instance with the settings, config, descriptor, etc.

        Args:
            root_directory (str, optional): The pipeline directory where the 'manage.py' file is usually located. Defaults to None.
            settings_module (str, optional): The pipeline directory where the 'manage.py' file is usually located. Defaults to 'settings'.
        """
        from outflow.core.pipeline import config as pipeline_config

        self._context = None
        self._root_command = None
        self.force_dry_run = force_dry_run

        if root_directory is not None:
            # ensure both manage.py and settings.py are in the python path
            root_directory_abs_path = pathlib.Path(root_directory).resolve().as_posix()
            os.environ.setdefault("PIPELINE_ROOT_DIRECTORY", root_directory_abs_path)
            sys.path.append(root_directory_abs_path)

        if settings_module is not None:
            os.environ.setdefault("OUTFLOW_SETTINGS_MODULE", settings_module)

        # check pipeline level command line args
        system_args, self.command_argv = self.parse_system_args(argv=argv)

        if system_args.settings is not None:
            os.environ["OUTFLOW_SETTINGS_MODULE"] = system_args.settings

        if system_args.config is not None:
            os.environ["OUTFLOW_CONFIG_PATH"] = (
                pathlib.Path(system_args.config).resolve().as_posix()
            )

        for dir_path in system_args.python_path:
            sys.path.append(pathlib.Path(dir_path).resolve().as_posix())

        # If true, show program's version number and exit.
        self.display_version = system_args.version

        # setup the logger and force the verbose level if needed
        if system_args.log_level is not None:
            pipeline_config["logging"]["loggers"]["outflow"][
                "level"
            ] = system_args.log_level

        set_plugins_loggers_config()

        logging.config.dictConfig(pipeline_config["logging"])

        logger.debug(f"Config loaded: {pipeline_config}")

        pipeline_config["local_mode"] = system_args.local_mode

        self.load_plugins()
        self.load_backends()

    def load_plugins(self):
        from outflow.core.pipeline import settings

        for plugin_name in settings.PLUGINS:
            Plugin.load(plugin_name)

    def load_backends(self):
        from outflow.core.backend import Backend as DefaultBackend
        from outflow.core.pipeline import settings

        self.backends = {"default": DefaultBackend}

        for key, value in settings.BACKENDS.items():
            try:
                module = importlib.import_module(value)
                self.backends[key] = module.Backend
                logger.debug(f"Backend {key} successfully imported")
            except ImportError:
                logger.warning(f"Cannot import module {value} for backend {key}")

    @property
    def context(self):
        if self._context is None:
            self._context = PipelineContext(force_dry_run=self.force_dry_run)

        return self._context

    @property
    def root_command(self):
        if self._root_command is None:
            try:
                from outflow.core.pipeline import settings
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import the pipeline root command from the settings. Are you sure outflow is installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
            # get the instance of the root command singleton
            self._root_command = settings.ROOT_COMMAND_CLASS()

            # loop over the system and base args and add them to the parser to be able to display the full help message
            # if the system arguments have already been added, pass
            base_root_command_args = {**self.system_arguments, **self.base_arguments}
            self.add_args(base_root_command_args, self._root_command.parser)

        return self._root_command

    def add_args(self, args_dict, parser):
        if not getattr(parser, "_args_already_setup", False):

            for argument in args_dict.values():
                parser.add_argument(*argument[0], **argument[1])
            parser._args_already_setup = True

    def parse_system_args(self, argv=None):
        """
        Parse the system args
        """
        parser = argparse.ArgumentParser(
            description="Preprocess system arguments.",
            add_help=False,
            allow_abbrev=False,
        )

        self.add_args(self.system_arguments, parser)

        return parser.parse_known_args(argv)

    def run(self):
        """Run the pipeline"""
        from outflow.core.db import DeclarativeBases
        from outflow.core.pipeline import config

        if self.display_version:
            print(f"Outflow version '{outflow_version}'")
            return 0

        backend_name = config.get("backend", "default")
        Backend = self.backends.get(backend_name, self.backends["default"])
        backend = Backend(context=self.context)

        try:
            self.result = self.root_command(self.command_argv, backend=backend)
        except Exception:
            raise
        finally:
            # close database connections and bubble up the exception if any
            self.context.databases.close()
            DeclarativeBases.clear_metadata()

        return 0

    @staticmethod
    def get_parent_directory_posix_path(module_path):
        """Return the posix path of the parent directory of the given module

        Args:
            module_path (str): The module path. Usually the one of 'manage.py'

        Returns:
            str: The posix path of the parent directory of the given module
        """
        return pathlib.Path(module_path).parent.resolve().as_posix()
