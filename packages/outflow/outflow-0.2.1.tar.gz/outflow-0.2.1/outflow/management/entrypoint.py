#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from outflow.core.pipeline import Pipeline


def entrypoint():
    pipeline = Pipeline(
        root_directory=None,
        settings_module="outflow.core.pipeline.settings_management.default_settings",
        force_dry_run=True,
    )
    return pipeline.run()
