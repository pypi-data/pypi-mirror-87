# -*- coding: utf-8 -*-
"""
Lazy Config for Outflow.

Read values from the file specified by the OUTFLOW_CONFIG_PATH environment variable
"""

import json
import os
import pprint
from pathlib import Path

import toml
import yaml
from outflow.core.generic.functional import LazyObject, empty
from outflow.core.logging import default_config as default_logger_config
from outflow.core.logging import logger

ENVIRONMENT_VARIABLE = "OUTFLOW_CONFIG_PATH"


class DictLikeMixin:
    """Define methods to use the config objects like dictionaries"""

    def __getitem__(self, key):
        """Override the [] to be able to use both 'config.key' and 'config["key"]'

        Args:
            key (string): The key used to retrieve the config value
        """
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        """Setter for keys USE WITH CAUTION AS IT MIGHT BREAK OUTFLOW"""
        self.__setattr__(key, value)

    def get(self, key, default=None):
        """Return the value for the specified key if key is in dict like object, if not, return the default value."""
        try:
            return self.__getitem__(key)
        except AttributeError:
            return default

    def __contains__(self, key):
        return hasattr(self, key)


class LazyConfig(LazyObject, DictLikeMixin):
    """
    A lazy proxy for the pipeline config.
    """

    def _setup(self):
        """
        Load the config file pointed to by the environment variable. This
        is used the first time config is needed.
        """
        from .settings_management.lazy_settings import settings

        logger.debug("Resolving the LazyConfig object")

        config_filepath = os.environ.get(ENVIRONMENT_VARIABLE)
        if not config_filepath:
            if settings.ROOT_DIRECTORY is None:  # TODO try if settings file exists
                config_filepath = None
            else:
                # check for the default config file
                for ext in ["json", "yml", "yaml", "toml"]:
                    filepath = Path(settings.ROOT_DIRECTORY) / f"config.{ext}"
                    if filepath.exists():
                        config_filepath = filepath
                        break

        self._wrapped = Config(config_filepath)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Config'.
        return "<LazyConfig>"

    def __getattr__(self, name):
        """Return the value in the config and cache it in self.__dict__."""
        if self._wrapped is empty:
            self._setup()
        val = getattr(self._wrapped, name)

        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        """
        Set the content of config. Clear all cached values if _wrapped changes
         or clear single values when set.
        """
        if name == "_wrapped":
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete a config value and clear it from cache if needed."""
        super().__delattr__(name)
        self.__dict__.pop(name, None)

    @property
    def configured(self):
        """Return True if the settings have already been configured."""
        return self._wrapped is not empty


class Config(DictLikeMixin):
    def __init__(self, config_filepath):

        # store the config filepath in case someone later cares
        self._CONFIG_FILEPATH = config_filepath

        if config_filepath and config_filepath.exists():
            with open(config_filepath, "r") as f:
                # read the file into memory as a string to avoid re-reading.
                config_file_content = f.read()
        else:
            config_file_content = "{}"

        config_format = None

        load_functions = {
            "json": json.loads,
            "yaml": yaml.safe_load,
            "toml": toml.loads,
        }

        # use the outflow schema if true, else use the public schema
        # note: this variable must be set to false if the 'default' database does not support schema
        default_config = {
            "logging": default_logger_config,
            "local_mode": False,
            "use_outflow_schema": False,
        }

        for fmt in load_functions:
            try:
                config_dict = {
                    **default_config,
                    **load_functions[fmt](config_file_content),
                }
                config_format = fmt
            except Exception:
                pass

        if config_format is None:
            raise Exception(f"Unsupported config file {config_filepath}")

        for key in config_dict:
            config_value = config_dict[key]
            self.__setattr__(key, config_value)

    def __repr__(self):
        # skip private keys
        dct = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        return (
            f'<{self.__class__.__name__} "{self._CONFIG_FILEPATH.as_posix() if self._CONFIG_FILEPATH else "Default"}"\n'
            f"{pprint.pformat(dct)}>"
        )


config = LazyConfig()
