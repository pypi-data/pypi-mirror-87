#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ## Mandatory code in every plugin.models __init__.py needed for alembic
# ## DO NOT EDIT

import importlib
import os
import pkgutil
import sys

from outflow.core.db import DefaultBase
from sqlalchemy.ext.declarative import DeferredReflection

pkg_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module("." + name, __package__)

# Creates a list of all the tables represented by classes in the current plugin
# It is needed for alembic to generate migrations correctly
tables = {
    cls.__tablename__: cls
    for cls in DefaultBase.__subclasses__()
    if sys.modules[__name__].__name__ in cls.__module__
    and cls not in DeferredReflection.__subclasses__()
}

# ## End of mandatory code
