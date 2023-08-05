# -*- coding: utf-8 -*-
from outflow.core.generic.cached_dict import CachedDict
from outflow.core.generic.metaclasses import Singleton
from outflow.core.logging import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.ext.declarative import DeferredReflection, declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class SingletonDictMeta(Singleton):
    def __getitem__(self, key):
        return self()[key]


class SingletonDict(metaclass=SingletonDictMeta):
    def __init__(self):
        self._items = dict()

    @staticmethod
    def _get_dict_value(name):
        raise NotImplementedError()

    def __getitem__(self, key):
        if key not in self._items:
            self._items[key] = self._get_dict_value(key)

        return self._items[key]


class DeclarativeBases(SingletonDict):
    @staticmethod
    def _get_dict_value(key):
        return declarative_base()

    @classmethod
    def clear_metadata(cls):
        self = cls()
        for key in self._items:
            self._items[key].metadata.clear()


class Databases(CachedDict):
    def _get_dict_value(self, key):
        from outflow.core.pipeline import config

        db_login_info = config["databases"][key]
        return Database(db_login_info, db_label=key)

    def close(self):
        for db in self._items.values():
            db.close()


DefaultBase = DeclarativeBases["default"]


class DatabaseException(Exception):
    pass


class Database:
    """
    A class to manage the connection to the database
    """

    def __init__(self, login_info, db_label):
        self.login_info = login_info
        self.db_label = db_label

        self._engine = None
        self._admin_engine = None
        self._session = None
        self._connection = None
        self._admin_connection = None

    @property
    def admin_connection(self):
        if self._admin_connection is None:
            self.connect_admin()

        return self._admin_connection

    def connect_admin(self):
        """
        Make a connection to the database using SQLAlchemy
        """

        # connected = self.is_available()
        logger.debug("Connecting to database as admin")
        self._reflect()
        self._admin_connection = self.admin_engine.connect()

    def connect(self):
        """
        Make a connection to the database using SQLAlchemy
        """

        # connected = self.is_available()
        logger.debug("Connecting to database as user")
        self._reflect()
        self._connection = self.engine.connect()

    @property
    def session(self) -> Session:
        if self._session is None:
            if not self.is_connected:
                self.connect()
            self._session = scoped_session(sessionmaker(bind=self.engine))

        return self._session

    @property
    def admin_engine(self):
        if self._admin_engine is None:
            admin_url = self._generate_url(admin=True)
            self._admin_engine = create_engine(admin_url)
        return self._admin_engine

    @property
    def engine(self):
        if self._engine is None:
            url = self._generate_url()
            self._engine = create_engine(url)
        return self._engine

    def _generate_url(self, admin=False):

        dialect = self.login_info["dialect"]

        if dialect == "sqlite":
            return f"sqlite:///{self.login_info['path']}"

        elif dialect == "postgresql":
            if admin and "admin" not in self.login_info:
                raise DatabaseException(
                    "Admin credentials missing from configuration file"
                )

            return "postgresql://{user}@{address}/{database}".format(
                address=self.login_info["address"],
                user=self.login_info["admin"] if admin else self.login_info["user"],
                database=self.login_info["database"],
            )

    @property
    def is_connected(self):
        return bool(self._connection)

    @property
    def is_connected_as_admin(self):
        return bool(self._admin_connection)

    def _reflect(self):
        try:
            DeferredReflection.prepare(self.engine)
        except NoSuchTableError as e:
            logger.warning(f"The table {e} does not exist")

    def get_configured_sessionmaker(self):
        return

    def close(self):
        """Close any user and/or admin connection for this database"""

        # if connected as user
        if self.is_connected:
            logger.debug(f"Closing connection for database '{self}'")

            # first close any active session
            if self._session:
                self._session.close()
                self._session = None

            # then close the connection
            self._connection.close()
            self._connection = None

        # if connected as admin
        if self.is_connected_as_admin:
            logger.debug(f"Closing admin connection for database '{self}'")
            self._admin_connection.close()
            self._admin_connection = None
