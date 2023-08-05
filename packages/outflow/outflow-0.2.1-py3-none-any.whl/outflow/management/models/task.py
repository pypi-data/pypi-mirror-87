#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from outflow.core.db import DefaultBase as Base
from outflow.core.db import get_outflow_schema
from outflow.core.db.non_null_column import NonNullColumn
from sqlalchemy import INTEGER, ForeignKey, String

# from sqlalchemy.orm import relationship


class Task(Base):
    """
    Stores the tasks
    """

    id_task = NonNullColumn(INTEGER(), primary_key=True)
    task_plugin = NonNullColumn(String(256), descr="Name of the plugin")
    task_name = NonNullColumn(String(256), descr="Name of the task")

    __tablename__ = "task"
    __table_args__ = {"schema": get_outflow_schema()}

    def __repr__(self):
        return "JobLog(" f"name={self.task_name}" ")"


class RuntimeException(Base):
    """
    This table provides the history of the runtime exceptions that
    occurred in the pipeline.
    """

    id_runtime_exception = NonNullColumn(INTEGER(), primary_key=True)
    task_id = NonNullColumn(INTEGER(), ForeignKey(Task.id_task))
    # exception_type = NonNullColumn(
    #     exception_type_enum,
    #     descr="Type of the exception. Possible " f"values are: {exception_type_list}",
    # )
    # exception_level = NonNullColumn(
    #     exception_level_enum,
    #     descr="Level of the exception. Possible"
    #     " values are: "
    #     f"{exception_level_list}",
    # )
    # exception_msg = NonNullColumn(String(), descr="Message related to the exception")

    __tablename__ = "runtime_exception"
    __table_args__ = {"schema": get_outflow_schema()}

    # task = relationship("task")
