#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import pathlib
import pkgutil
import sys

from outflow.core.db import DeclarativeBases
from outflow.core.logging import logger
from sqlalchemy.ext.declarative import DeferredReflection


class PluginError(Exception):
    """
    Errors related to plugin loading and definitions.
    """


class Plugin:
    """
    Class to manage plugins module of the pipeline.
    """

    @staticmethod
    def _check_and_load_commands(plugin_name, module="commands"):
        """
        Check if the commands module exist and force the import to register the command tree.
        """
        Plugin._check_module(plugin_name, module)

    @staticmethod
    def _check_module(plugin_name, module):
        """
        Check if a module inside the plugin is importable.
        """
        # name for loading
        name = ".".join([plugin_name, module])

        try:
            importlib.import_module(name)
            logger.debug(f"Module {name} successfully imported")
            return True
        except ImportError:
            if plugin_name != "outflow.management":
                logger.warning(
                    "Cannot import module {0} for plugin {1}:".format(
                        module,
                        plugin_name,
                    )
                )
            return False

    @staticmethod
    def load(plugin_name):
        """
        Check the plugin integrity and import the commands.
        """
        try:
            importlib.import_module(plugin_name)
            logger.debug(f"Plugin '{plugin_name}' successfully imported...")
        except ImportError as e:
            raise PluginError(
                f"The '{plugin_name}' plugin could not be imported. "
                "Check the plugin list in the settings file. "
                "Maybe you forgot the namespace? "
                "Is the plugin properly installed?"
            ) from e
        logger.debug("checking commands, tasks and models...")
        Plugin._check_and_load_commands(plugin_name=plugin_name)
        plugin_content = ["models", "commands", "tasks"]
        content = list()
        for module in plugin_content:
            content.append(Plugin._check_module(plugin_name, module))
        if True not in content:
            raise PluginError(
                "An outflow plugin must contain at least one of "
                f"the following modules to be useful : {plugin_content}"
            )

    @staticmethod
    def get_path(plugin_name):
        try:
            return pathlib.Path(
                importlib.import_module(plugin_name).__file__
            ).parent.resolve()
        except ImportError as e:
            logger.print_exception(
                "Cannot find plugin {0}:".format(
                    plugin_name,
                )
            )
            raise PluginError(e)

    @staticmethod
    def import_models_submodules(plugin_name: str):
        """Import each models of the plugin

        Args:
            plugin_name (str): the plugin name
        """

        models_dir_path = Plugin.get_path(plugin_name) / "models"

        models_module_name = plugin_name + ".models"

        for (module_loader, name, is_pkg) in pkgutil.iter_modules([models_dir_path]):
            importlib.import_module(models_module_name + "." + name)

    @staticmethod
    def get_models_tables(plugin_name: str, db_label: str = "default"):
        """Generate a dict containing all the tables represented by model classes in the selected plugin

        These tables are needed for alembic to generate migrations correctly

        Args:
            plugin_name (str): the plugin name
            db_label (str): The database label used to filter the tables

        Returns:
            Dict: the tables represented by model classes in the selected plugin
        """

        Base = DeclarativeBases[db_label]

        models_module_name = plugin_name + ".models"

        return {
            cls.__tablename__: cls
            for cls in Base.__subclasses__()
            if sys.modules[models_module_name].__name__ in cls.__module__
            and cls not in DeferredReflection.__subclasses__()
        }
