# -*- coding: utf-8 -*-
import traceback

import ray
from outflow.core.logging import logger
from outflow.core.tasks.task_manager import TaskManager

from .base_actor import BaseActor


@ray.remote
class MapActor(BaseActor):
    def __init__(self, workflow, inputs, index, raise_exceptions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import logging

        logging.basicConfig(level=logging.DEBUG)
        # init_logger()

        self.workflow = workflow
        self.inputs = inputs
        self.index = index
        self.raise_exceptions = raise_exceptions

    def run(self):
        profile = False

        if profile:
            import cProfile

            pr = cProfile.Profile()
            pr.enable()

        ret = self._run()

        if profile:
            pr.dump_stats("one_outflow_raster_workflow.prof")
            pr.disable()

        return ret

    def _run(self):
        results = list()
        workflow_copy = self.workflow.copy()
        workflow_copy.entrypoint.bind(**self.inputs)

        terminating_tasks = list()

        for task in workflow_copy:
            task.context = self.pipeline_context
            task.parallel_workflow_id = self.index

        task_manager = TaskManager()

        try:
            task_manager.compute(workflow_copy)

            for task in workflow_copy:
                if task.terminating:
                    terminating_tasks.append(task_manager.results[task.id])

            results.append(terminating_tasks)
        except Exception as e:
            if self.raise_exceptions:
                raise e
            logger.warning(f"A map actor raised an exception in Map '{self}'")
            logger.warning(traceback.format_exc())
            results = [e]

        return results
