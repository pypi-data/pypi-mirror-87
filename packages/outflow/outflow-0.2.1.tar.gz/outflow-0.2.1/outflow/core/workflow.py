# -*- coding: utf-8 -*-
import networkx


class Workflow:
    def __init__(self, task):
        """
        A class to store a task workflow

        Note: the workflow entrypoint can be any of the workflow tasks


        :param task: the entrypoint of the workflow
        """

        self.entrypoint = task
        # self.task_key_mapping = {}
        self.directed_graph = networkx.DiGraph()
        self.add_node(task)

    # def get_or_create_key(self, task):
    #     if task in self.task_key_mapping:
    #         return self.task_key_mapping[task]
    #     else:
    #         task_key = task.name + "-" + str(uuid4())
    #         self.task_key_mapping[task] = task_key
    #         self.directed_graph.add_node(task_key)
    #         return task_key

    def add_node(self, task):
        # task_key = self.get_or_create_key(task)
        self.directed_graph.add_node(task)
        task.workflow = self

    def add_edge(self, parent_task, child_task):
        # parent_task_key = self.get_or_create_key(parent_task)
        # child_task_key = self.get_or_create_key(child_task)
        self.directed_graph.add_edge(parent_task, child_task)

    def merge(self, workflow):
        # self.task_key_mapping.update(workflow.task_key_mapping)
        self.directed_graph.update(workflow.directed_graph)
        for task in self.directed_graph:
            task.workflow = self

    def copy(self):
        mapping = {task: task.copy() for task in self.directed_graph}
        new_workflow = Workflow(mapping[self.entrypoint])
        new_workflow.directed_graph = networkx.relabel_nodes(
            self.directed_graph, mapping
        )
        for task in new_workflow:
            task.workflow = new_workflow
        return new_workflow

    def get_parents(self, task):
        return self.directed_graph.predecessors(task)

    def get_children(self, task):
        return self.directed_graph.successors(task)

    def __iter__(self):
        for task in self.directed_graph:
            yield task

    def set_context(self, pipeline_context):
        """Set the pipeline context in each task of the workflow"""
        for task in self:
            task.context = pipeline_context
