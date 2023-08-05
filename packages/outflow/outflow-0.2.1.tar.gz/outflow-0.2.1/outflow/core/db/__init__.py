# -*- coding: utf-8 -*-
from .database import Databases, DeclarativeBases, DefaultBase  # noqa: F401


def get_outflow_schema():
    from outflow.core.pipeline import config

    schema = "outflow" if config["use_outflow_schema"] else None
    return schema
