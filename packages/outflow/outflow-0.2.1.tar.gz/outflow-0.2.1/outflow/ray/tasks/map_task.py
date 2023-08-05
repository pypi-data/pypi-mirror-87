# -*- coding: utf-8 -*-
import sys
from typing import List

import ray

from outflow.core.target import Target
from outflow.core.tasks.task import Task
from outflow.core.types import IterateOn
from outflow.ray.actors import MapActor


class MapTask(Task):
    def __init__(
        self,
        start: Task,
        *,
        end: Task = None,
        name=None,
        reduce_func=None,
        outputs=None,
        output_name="map_output",
        num_cpus=1,
        raise_exceptions=False
    ):

        super().__init__()

        if outputs is None:
            self.outputs = {output_name: Target(output_name, type=List)}
        else:
            self.outputs = outputs

        if name is not None:
            self.name = name

        self.start = start

        if end is None:
            self.start.terminating = True
        else:
            end.terminating = True

        if reduce_func is None:
            self.reduce = lambda x: {output_name: x}
        self.raise_exceptions = raise_exceptions
        self.num_cpus = num_cpus

    def run(self, **map_inputs):

        loop_workflow = self.start.workflow
        loop_workflow.start = self.start

        actor_results = list()

        for index, generated_inputs in enumerate(self.generator(**map_inputs)):
            # ensure the workflow start is the given task
            actor = MapActor.options(num_cpus=self.num_cpus).remote(
                loop_workflow,
                generated_inputs,
                index,
                self.raise_exceptions,
                context=self.context,
                python_path=sys.path,
            )

            actor_results.append(actor.run.remote())

        result = [
            objid for sublist in ray.get(actor_results) for objid in sublist
        ]  # TODO remove this
        return self.reduce(result)

    def generator(self, **map_inputs):
        """
        default generator function
        :param map_inputs:
        :return:
        """

        not_iterable_inputs = map_inputs.copy()

        iterable_targets = [
            target
            for target, target in self.start.inputs.items()
            if target.type.__name__.startswith(IterateOn.prefix)
        ]

        # todo: support multiple iterable inputs
        iterable_target = iterable_targets[0]

        # get the input name of the sequence to map
        sequence_input_name = iterable_target.type.__name__[len(IterateOn.prefix) :]
        input_name = iterable_target.name

        del not_iterable_inputs[sequence_input_name]

        for input_value in map_inputs[
            sequence_input_name
        ]:  # TODO add zip to support multiple mapped sequence
            yield {input_name: input_value, **not_iterable_inputs}
