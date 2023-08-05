# -*- coding: utf-8 -*-
from outflow.core.logging import logger

from .base_task import BaseTask


class Task(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        super().__call__()

        self.resolve_remote_inputs(kwargs)
        return self.run(**kwargs, **self.bind_kwargs, **self.parameterized_kwargs)

    def resolve_remote_inputs(self, task_kwargs):
        """Transform 'ray' ObjectIDs into Python object

        From main actor: get the object in the object store
        If remote: get in the remote object store and transfer by TCP
        """
        try:
            import ray

            for key, val in task_kwargs.items():
                if isinstance(val, ray._raylet.ObjectID):
                    task_kwargs[key] = ray.get(val)
        except ImportError:
            logger.debug(
                "The 'ray' package is not available, usage of remote objects is therefore impossible"
            )


task = Task.as_task
