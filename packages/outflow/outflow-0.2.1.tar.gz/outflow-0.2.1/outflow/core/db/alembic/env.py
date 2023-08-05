# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging

from outflow.core.db.alembic.operations import GrantPermissionsOp
from outflow.core.plugin import Plugin
from sqlalchemy import engine_from_config, pool

from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops

logger = logging.getLogger("alembic")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = config.attributes["Base"].metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


writer = rewriter.Rewriter()


@writer.rewrites(ops.CreateTableOp)
def create_table(context, revision, op):
    logger.debug(f"Adding grant_permissions operation on table {op.table_name}")
    return [
        op,
        GrantPermissionsOp(op.table_name, schema=op.schema),
    ]


def get_table_name_list():
    plugin_name = config.attributes["plugin"]
    db_label = config.attributes["db_label"]

    # ensure models submodules are loaded
    Plugin.import_models_submodules(plugin_name)

    # get the tables associated with the given database label
    tables = Plugin.get_models_tables(plugin_name=plugin_name, db_label=db_label)
    table_names = [table_name for table_name, model_class in tables.items()]
    return table_names


def include_obj(obj, name, type_, reflected, compare_to):
    """Decide to include the object or not in the migration

    When a migration is generated, only the plugins models are included
    """
    if type_ == "table":
        if name in get_table_name_list():
            return True
        else:
            return False
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        compare_type=True,
        process_revision_directives=writer,
        include_object=include_obj,
    )

    with context.begin_transaction():
        if connection.engine.name == "postgresql":
            context.execute("SET search_path TO public")
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    try:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            run_migrations(connection)
    except KeyError:
        connection = config.attributes["connection"]
        run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
