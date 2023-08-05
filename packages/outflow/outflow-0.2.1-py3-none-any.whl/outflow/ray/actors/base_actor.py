# -*- coding: utf-8 -*-
from outflow.core.logging import logger


class BaseActor:
    def __init__(self, context=None, actor_init_kwargs=None, python_path=None):
        logger.debug(f"Initialize actor '{self}'")
        self.pipeline_context = context
        if actor_init_kwargs is None:
            actor_init_kwargs = dict()
        self.__dict__.update(**actor_init_kwargs)

        import logging

        logging.config.dictConfig(self.pipeline_context.config["logging"])
        from outflow.core.logging import set_plugins_loggers_config

        set_plugins_loggers_config()

    def update_pipeline_context_args(self, pipeline_args, extra_args):
        logger.debug(
            f"Update pipeline context '{self.pipeline_context}' with args '{pipeline_args}' and extra_args '{extra_args}'"
        )
        self.pipeline_context.args = pipeline_args
        self.pipeline_context.extra_args = extra_args
