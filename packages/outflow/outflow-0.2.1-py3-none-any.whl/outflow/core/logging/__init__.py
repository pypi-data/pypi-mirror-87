# -*- coding: utf-8 -*-
import sys

from .logger import OutflowLogger
from .rotating_file_handler import RotatingFileHandlerPerUser
from .terminal_color_formatter import TerminalColorFormatter

set_plugins_loggers_config = None

# create a outflowLogger
outflow_logger = OutflowLogger()

# store the path of the __init__.py file in the OutflowLogger instance
outflow_logger.__file__ = __file__

# Map the submodules to the OutflowLogger instance properties to allow imports
outflow_logger.RotatingFileHandlerPerUser = RotatingFileHandlerPerUser
outflow_logger.TerminalColorFormatter = TerminalColorFormatter

# replace the outflow.core.logging module by outflow logger instance
# this allows to import the 'logger' property of 'OutflowLogger' as a module
sys.modules[__name__] = outflow_logger
