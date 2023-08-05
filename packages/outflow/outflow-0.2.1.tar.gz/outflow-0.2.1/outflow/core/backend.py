# -*- coding: utf-8 -*-
from outflow.core.logging import logger
from outflow.core.tasks.task_manager import TaskManager


class Backend:
    def __init__(self, context=None):
        logger.debug(f"Initialize backend '{self}'")
        self.pipeline_context = context

    def update_pipeline_context_args(self, pipeline_args, extra_args):
        logger.debug(
            f"Update pipeline context '{self.pipeline_context}' with args '{pipeline_args}' and extra_args '{extra_args}'"
        )
        self.pipeline_context.args = pipeline_args
        self.pipeline_context.extra_args = extra_args

    def run(self, *, task_list):
        logger.debug(
            f"Run pipeline with backend '{self}' and with pipeline context '{self.pipeline_context}'"
        )
        task_manager = TaskManager()

        for task in task_list:
            task.workflow.set_context(self.pipeline_context)
            task_manager.compute(task.workflow)

        return [task_manager.results.resolve(task.id) for task in task_list]
