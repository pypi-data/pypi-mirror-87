# -*- coding: utf-8 -*-
from ray._raylet import ObjectRef

from outflow.core.logging import logger
from outflow.core.target import TargetException
from outflow.ray.results import Results as RayResults


class TaskManager:
    """
    Manage task calls and store the result references
    """

    def __init__(self):
        # to avoid reprocessing, store a reference of each task result for each already visited graph node
        self.results = RayResults()

    def compute(self, workflow):

        workflow.scheduler = self

        # run through each task of the workflow to gather task result references
        try:
            for task in workflow:
                self.add(task)
        except RecursionError:
            raise Exception("There is a cycle in the dependency graph")

    def add(self, task):
        """Store the reference of the task result dict

        Args:
            task ([type]): [description]
        """
        if task.id in self.results:
            # avoid reprocessing already visited graph nodes
            return

        # create a dictionary to store the reference to the task inputs
        task_inputs = {}

        # loop over the task parents to get the task inputs
        for parent in task.parents:
            # ensure the parents result reference is already stored in the promises reference dict
            self.add(parent)

            # and loop over parents
            for output_key in parent.outputs:
                task_inputs[output_key] = self.results.get_item_reference(
                    parent.id, output_key
                )

        # check if the current task have been processed during previous steps
        if task.id in self.results:
            return

        # if not, store the reference of the task result dict
        logger.debug(f"Running task {task.name}")

        task_return_value = task(**task_inputs)

        if task_return_value is not None and not isinstance(
            task_return_value, ObjectRef
        ):
            if not isinstance(task_return_value, dict):
                if len(task.outputs) > 1:
                    raise TargetException(
                        f"Task {task.name} must return a dictionary since it has defined more than one output target"
                    )
                else:
                    task_return_value = {
                        next(iter(task.outputs)): task_return_value
                    }  # get first and only item in dictionary task.outputs

        self.results._set(task.id, task_return_value)

        # repeat the process with task child
        for child in task.children:
            self.add(child)
