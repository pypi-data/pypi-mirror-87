# -*- coding: utf-8 -*-
import argparse
import importlib
import os
import tempfile
from pathlib import Path

import outflow.core.db.alembic as outflow_alembic
from alembic import command
from alembic.config import Config, main
from outflow.core.command import Command, argument
from outflow.core.db import DeclarativeBases
from outflow.core.logging import logger
from outflow.core.plugin import Plugin
from outflow.core.tasks.task import Task
from sqlalchemy import UniqueConstraint

from .management import Management


def generate_alembic_ini_file(alembic_ini_path, alembic_config):
    with open(alembic_ini_path, "w") as ini_file:
        ini_file.write("[alembic]\n")
        for key, value in alembic_config["main_options"].items():
            ini_file.write(f"{key} = {value}\n")

        for key, value in alembic_config["admin"].items():
            ini_file.write(f"{key} = {value}\n")


def get_alembic_config(db_label, pipeline_context, plugin=None):

    version_locations = []
    for plugin_name in pipeline_context.settings.PLUGINS:
        location = Plugin.get_path(plugin_name) / "models" / "versions" / db_label
        if Path(location).is_dir():
            version_locations.append(location.absolute().as_posix())

    alembic_path = Path(outflow_alembic.__file__).parent.absolute().as_posix()

    config = {
        "main_options": {
            "script_location": alembic_path,
            "version_locations": " ".join(version_locations),
            "output_encoding": "utf-8",
        },
        "attributes": {
            "connection": pipeline_context.databases[db_label].admin_connection,
            "login_info": pipeline_context.config["databases"][db_label],
            "Base": DeclarativeBases[db_label],
            "db_label": db_label,
        },
        "admin": {
            "sqlalchemy.url": pipeline_context.databases[db_label]._generate_url(
                admin=True
            )
        },
        "post_write_hooks": {
            "hooks": "black",
            "black.type": "console_scripts",
            "black.entrypoint": "black",
        },
    }

    if plugin:
        config["attributes"]["plugin"] = plugin

    return config


@Management.subcommand(invokable=False)
class Db(Command):
    """
    Root command of the subcommands managing the database
    """


@Db.subcommand()
class ExecuteSQL(Command):
    """
    Execute a SQL command on the pipeline database.
    """

    def add_arguments(self):
        # create an exclusive group for the two options
        group = self.parser_add_mutually_exclusive_group(required=True)

        # add argument to set the path of the script
        group.add_argument(
            "-i",
            "--input",
            help="""
            The absolute path to the script to run on the pipeline database.
            """,
            type=argparse.FileType("r"),
            default=None,
        )

        # argument to read a command from the command line
        group.add_argument(
            "-e",
            "--execute",
            help="The command to run on the pipeline database.",
            type=str,
            default=None,
        )

    def setup_tasks(self):
        """
        Executed to clear the database.
        """

        @Task.as_task(with_self=True)
        def ExecuteCli(self: Task):
            """
            to execute a script on the outflow database from the command line.
            """
            # get the database objects for the outflow
            session = self.context.db.session

            # try closing the session to kill all current transactions
            try:
                session.close_all()
            except Exception as e:
                logger.error("can't close sessions on sqlalchemy")
                logger.error(e)
                return

            # execute the script if present or the command in argument
            if self.context.args.execute is None:
                script = self.context.args.input.read()
            else:
                script = self.context.args.execute
            logger.debug("running command(s):\n{0}".format(script))
            try:
                session.execute(script)
            except Exception as e:
                logger.error(e)
                return

            return {}

        return ExecuteCli()


@Db.subcommand(with_task_context=True, allow_extra_args=True)
@argument("-d", "--db_label", type=str, default="default")
@argument(
    "command",
    type=str,
    help=""" The command to give to alembic. """,
)
def alembic(self: Task):
    db_label = self.context.args.db_label

    alembic_config = get_alembic_config(db_label, self.context)

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        alembic_ini_path = (Path(tmp_dir_path) / "alembic.ini").resolve()
        generate_alembic_ini_file(alembic_ini_path, alembic_config)

        alembic_args = [
            "-c",
            alembic_ini_path.as_posix(),
            *self.context.extra_args,
        ]

        main(argv=alembic_args)


def migrate(task, migration_func):
    revision = task.context.args.revision

    if revision is None:
        raise Exception("Missing required argument : revision")

    db_label = task.context.args.db_label
    version_locations = list()

    for plugin_name in task.context.settings.PLUGINS:
        location = Plugin.get_path(plugin_name) / "models" / "versions" / db_label
        if location.is_dir():
            for model_file in (Plugin.get_path(plugin_name) / "models").glob(
                "[!_]*.py"
            ):
                db = getattr(
                    importlib.import_module(plugin_name).models,
                    model_file.name.split(".")[0],
                ).Base
                if db == DeclarativeBases[db_label]:
                    version_locations.append(location.resolve().as_posix())

    alembic_config_dict = get_alembic_config(db_label, task.context)
    cfg = Config()

    for key, value in alembic_config_dict["main_options"].items():
        cfg.set_main_option(key, value)

    for key, value in alembic_config_dict["attributes"].items():
        cfg.attributes[key] = value

    logger.info("Calling alembic")

    migration_func(cfg, revision)


@Db.subcommand(with_task_context=True)
@argument("--db_label", "-d", type=str, default="default")
@argument(
    "revision",
    type=str,
    default=None,
    nargs="?",
    help="""
          The revision of the database to switch on. Can be either 'head' for
          the last revision, or an unique identifier of the revision (for
          example 'ae1' for the revision 'ae1027a6acf'), or a decimal value
          '+N' N being the number of revisions to execute from the current one.
          """,
)
def downgrade(self: Task):
    migrate(self, command.downgrade)


@Db.subcommand(with_task_context=True)
@argument("--db_label", "-d", type=str, default="default")
@argument(
    "revision",
    type=str,
    default=None,
    nargs="?",
    help="""
          The revision of the database to switch on. Can be either 'head' for
          the last revision, or an unique identifier of the revision (for
          example 'ae1' for the revision 'ae1027a6acf'), or a decimal value
          '+N' N being the number of revisions to execute from the current one.
          """,
)
def upgrade(self: Task):
    """
    Upgrade the a database to given migration.
    """

    migrate(self, command.upgrade)


@Db.subcommand(with_task_context=True, allow_extra_args=True)
@argument(
    "--plugin",
    "-p",
    type=str,
    required=True,
    help="Name of the plugin for which you want to generate the migrations",
)
@argument("--db_label", "-d", type=str, default="default")
def MakeMigrations(self: Task):
    """A task to automatically generate migrations
    'alembic revision --autogenerate' is used to generate migrations.
    You have to manually edit the migration after being generated, because
    alembic cannot detect changes of table/column name etc, or does not
    generate the schema creation. More info :
    http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect
    """

    plugin = self.context.args.plugin
    db_label = self.context.args.db_label

    plugin_version_path = Plugin.get_path(plugin) / "models" / "versions" / db_label

    # ensure the version directory exist
    os.makedirs(plugin_version_path, exist_ok=True)

    # get the plugin to use
    if plugin == "outflow.management":
        db_label = "default"

        mng_plugin_version_path = (
            Plugin.get_path("outflow.management") / "models" / "versions" / db_label
        )
        version_locations = [mng_plugin_version_path.resolve().as_posix()]
    else:
        version_locations = list()
        # get all the previous versions associated with the given base
        for plugin_name in self.context.settings.PLUGINS:
            version_path = (
                Plugin.get_path(plugin_name) / "models" / "versions" / db_label
            )
            if version_path.is_dir():
                version_locations.append(version_path.resolve().as_posix())

    # check that the plugin is valid
    Plugin.load(plugin)

    alembic_config_dict = get_alembic_config(db_label, self.context, plugin=plugin)
    cfg = Config()

    for key, value in alembic_config_dict["main_options"].items():
        cfg.set_main_option(key, value)

    for key, value in alembic_config_dict["attributes"].items():
        cfg.attributes[key] = value

    for key, value in alembic_config_dict["post_write_hooks"].items():
        cfg.set_section_option("post_write_hooks", key, value)

    logger.info("Calling alembic revision")

    # used to pass arguments to alembic revision command
    # http://alembic.zzzcomputing.com/en/latest/api/commands.html#alembic.command.revision
    args = dict()
    for arg in self.context.extra_args:
        try:
            # Only parse keyword of the form (-)-key=val
            if "=" in arg:
                s = arg.split("=")
            else:
                logger.warning(
                    f"Input keyword {arg} can not be parsed and will be ignored, "
                    "please call extra alembic keywords using '='!"
                )
                continue

            # Replace any hyphen "-" by underscore "_" in keyword argument name
            # (including "-" or "--" prefix)
            s[0] = s[0].replace("-", "_")

            # Remove "_" or "__" prefix
            if s[0].startswith("__"):
                args.update({s[0][2:]: s[1]})
            elif s[0].startswith("_"):
                args.update({s[0][1:]: s[1]})
        except IndexError:
            logger.error(f"Unknown argument: {arg}, skipping!")

    command.revision(
        cfg,
        autogenerate=True,
        version_path=plugin_version_path.as_posix(),
        **args,
    )


@Db.subcommand(description="Generate the database documentation of a plugin")
@argument(
    "plugin_name",
    help="The name of the plugin for which we want to generate the documentation",
)
def GenDoc(plugin_name):
    """
    This function generate an reST file in the current directory. This file
    contains the model documentation about a given plugin.
    """

    plugin_models = importlib.import_module(f"{plugin_name}.models")
    try:
        tables = plugin_models.tables
    except AttributeError:
        raise AttributeError(
            "Are you sure you have included the mandatory code "
            "to your plugin.models.__init__.py ? See the "
            "poppy documentation about models."
        )

    file_name = f"{plugin_name}_model_documentation.rst"
    file_path = os.path.join(os.path.curdir, file_name)

    csv_table_header = (
        ".. csv-table:: {0}\n"
        '   :header: "Column name", "Data type", "Description", '
        '"Priority", "Comment"\n\n'
    )

    with open(file_path, "w") as f:

        # A dictionary containing schema name as key, and all the generated text
        # of the tables in each schema as value
        table_doc_dict = dict()

        for table_name, model_class in tables.items():

            text = ""
            schema_name = "public"

            # Title of the section
            title = f"The table {table_name}\n"
            text += title
            text += f"{'=' * (len(title) - 1)}\n"

            # The docstring of the class representation of the table
            text += " ".join(
                model_class.__doc__.replace("\n", "").split()
            )  # Replaces sequences of space with one and remove linebreaks
            text += "\n\n"

            text += csv_table_header.format(table_name)

            for c in model_class.__table__.columns:
                col_infos = c.infos()
                text += f'   "{col_infos["name"]}", "{col_infos["sql_type"]}", "{col_infos["description"]}", "{col_infos["priority"]}", "{col_infos["comment"]}"\n'

            text += "\n"

            table_args = model_class.__table_args__

            # Extract unique constraints and schema name (if any)
            if type(table_args) == tuple:
                for arg in table_args:
                    if type(arg) == UniqueConstraint:
                        constraint = arg
                        columns = "(" + ",".join([x.key for x in constraint]) + ")"
                        text += f"The tuple of columns {columns} must be unique.\n"
                    elif type(arg) == dict:
                        try:
                            schema_name = arg["schema"]
                        except KeyError:
                            pass

            elif type(table_args) == dict:
                try:
                    schema_name = table_args["schema"]
                except KeyError:
                    pass

            text += "\n"

            try:
                table_doc_dict.update({schema_name: table_doc_dict[schema_name] + text})
            except KeyError:
                table_doc_dict.update({schema_name: text})

        for schema_name, text in table_doc_dict.items():
            schema_header = f"The '{schema_name}' schema\n"

            f.write(f"{'*' * (len(schema_header) - 1)}\n")
            f.write(schema_header)
            f.write(f"{'*' * (len(schema_header) - 1)}\n\n")

            f.write(table_doc_dict[schema_name])

    logger.info(f"{file_name} successfully generated in the current directory")
