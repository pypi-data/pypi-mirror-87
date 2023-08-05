# -*- coding: utf-8 -*-
import sys

from outflow.core.tasks.base_task import BaseTask
from outflow.ray.actors import TaskActor


class ParallelTask(BaseTask):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        super().__call__()
        self.actor = TaskActor.options(
            resources={"head_node": 1}, num_cpus=self.num_cpus
        ).remote(context=self.context, python_path=sys.path)
        self.actor.set_run.remote(self.run)
        actor_result = self.actor.run.remote(
            **kwargs, **self.bind_kwargs, **self.parameterized_kwargs
        )

        return actor_result
