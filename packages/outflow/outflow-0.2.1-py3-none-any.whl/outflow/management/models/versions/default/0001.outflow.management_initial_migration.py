# -*- coding: utf-8 -*-
"""Initial migration

Revision ID: 0001.outflow.management
Revises:
Create Date: 2020-11-19 13:43:50.767650

"""
import sqlalchemy as sa
from alembic import op
from outflow.core.db.alembic.helpers import create_schema

# revision identifiers, used by Alembic.
revision = "0001.outflow.management"
down_revision = None
branch_labels = ("outflow.management",)
depends_on = None


def upgrade_outflow_schema():
    create_schema("outflow")
    op.create_table(
        "task",
        sa.Column("id_task", sa.INTEGER(), nullable=False),
        sa.Column("task_plugin", sa.String(length=256), nullable=False),
        sa.Column("task_name", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id_task"),
        schema="outflow",
    )
    op.grant_permissions("task", schema="outflow")
    op.create_table(
        "runtime_exception",
        sa.Column("id_runtime_exception", sa.INTEGER(), nullable=False),
        sa.Column("task_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["outflow.task.id_task"],
        ),
        sa.PrimaryKeyConstraint("id_runtime_exception"),
        schema="outflow",
    )
    op.grant_permissions("runtime_exception", schema="outflow")


def downgrade_outflow_schema():
    op.drop_table("runtime_exception", schema="outflow")
    op.drop_table("task", schema="outflow")


def upgrade_no_schema():
    op.create_table(
        "task",
        sa.Column("id_task", sa.INTEGER(), nullable=False),
        sa.Column("task_plugin", sa.String(length=256), nullable=False),
        sa.Column("task_name", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id_task"),
    )
    op.grant_permissions("task")
    op.create_table(
        "runtime_exception",
        sa.Column("id_runtime_exception", sa.INTEGER(), nullable=False),
        sa.Column("task_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id_task"],
        ),
        sa.PrimaryKeyConstraint("id_runtime_exception"),
    )
    op.grant_permissions("runtime_exception")


def downgrade_no_schema():
    op.drop_table("runtime_exception")
    op.drop_table("task")


def upgrade():
    from outflow.core.db import get_outflow_schema

    if get_outflow_schema():
        upgrade_outflow_schema()
    else:
        upgrade_no_schema()


def downgrade():
    from outflow.core.db import get_outflow_schema

    if get_outflow_schema():
        downgrade_outflow_schema()
    else:
        downgrade_no_schema()
