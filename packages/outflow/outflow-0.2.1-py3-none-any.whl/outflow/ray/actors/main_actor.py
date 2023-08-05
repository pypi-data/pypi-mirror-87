# -*- coding: utf-8 -*-

import ray
from outflow.core.logging import logger
from outflow.core.tasks.task_manager import TaskManager

from .base_actor import BaseActor


@ray.remote
class MainActor(BaseActor):
    def run(self, *, task_list):
        logger.debug(
            f"Run pipeline with actor '{self}' and with pipeline context '{self.pipeline_context}'"
        )
        task_manager = TaskManager()

        for task in task_list:
            task.workflow.set_context(self.pipeline_context)
            task_manager.compute(task.workflow)

        return [task_manager.results.resolve(task.id) for task in task_list]
