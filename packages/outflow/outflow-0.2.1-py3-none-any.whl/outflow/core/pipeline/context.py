# -*- coding: utf-8 -*-
from outflow.core.db.database import Database, Databases


class PipelineContext:
    def __init__(self, force_dry_run=False):
        from outflow.core.pipeline import config, settings

        self._force_dry_run = force_dry_run
        self.config = config
        self.settings = settings
        self.args = None
        self._databases = None

    def __getstate__(self):
        """
        This excludes database sessions from the serialization because it is
        not serializable.
        """
        state = self.__dict__.copy()
        state["_databases"] = None
        return state

    @property
    def dry_run(self):
        return self._force_dry_run or self.args.dry_run

    @property
    def default_db(self) -> Database:
        return self.databases["default"]

    @property
    def databases(self):
        if self._databases is None:
            self._databases = Databases()

        return self._databases
