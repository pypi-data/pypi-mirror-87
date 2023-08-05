# -*- coding: utf-8 -*-
from unittest.mock import patch

from outflow.core.logging import default_config as default_logger_config
from outflow.core.pipeline.context import PipelineContext
from outflow.core.pipeline.settings_management.lazy_settings import Settings


class TaskTestCase:
    """
    The TaskTestCase class is designed to be overridden in derived classes to create unit tests for tasks.

    Example:
        class TestMyPluginTasks(TaskTestCase):
            def test_task1(self):
                # --- initialize the task ---
                from my_plugin import task1

                self.task = task1()

                self.config = {
                    "tasks": {
                        "my_task_name": {
                            "param_a": "aaaaaa",
                            "param_b": "bbbb",
                        }
                    }
                }

                # --- run the task ---

                result = self.run_task(target_a='my_data', target_b='my_data')

                # --- make assertions ---

                # test the result
                result == 'my_result'

                # (...)

            def test_task2(self):
                # --- initialize the task ---
                from my_plugin import task2

                self.task = task2()

                # (...)
    """

    def setup_method(self):
        """
        Setup the pipeline before each test
        :return:
        """

        # reset the task
        self.task = None
        self.config = {"logging": default_logger_config, "use_outflow_schema": False}
        self.settings = Settings(
            "outflow.core.pipeline.settings_management.default_settings"
        )

    def teardown_method(self):
        pass

    def run_task(self, *args, **kwargs):

        if self.task is None:
            raise ValueError("The task has not been initialized")

        with patch("outflow.core.pipeline.settings", new=self.settings):
            with patch("outflow.core.pipeline.config", new=self.config):
                self.task.context = PipelineContext()
                return self.task(*args, **kwargs)
