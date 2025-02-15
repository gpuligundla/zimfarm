"""Create schedules, tasks and requested_tasks

Revision ID: 8279abb2d6dc
Revises: 96203f95bc36
Create Date: 2023-04-13 10:10:52.820099

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8279abb2d6dc"
down_revision = "96203f95bc36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schedule",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("mongo_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("language_code", sa.String(), nullable=False),
        sa.Column("language_name_native", sa.String(), nullable=False),
        sa.Column("language_name_en", sa.String(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("periodicity", sa.String(), nullable=False),
        sa.Column("most_recent_task_id", sa.Uuid(), nullable=True),
        sa.Column(
            "notification", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedule")),
        sa.UniqueConstraint("mongo_id", name=op.f("uq_schedule_mongo_id")),
    )
    op.create_index(op.f("ix_schedule_name"), "schedule", ["name"], unique=True)
    op.create_table(
        "requested_task",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("mongo_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("timestamp", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "events",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("requested_by", sa.String(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("upload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "notification", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("schedule_id", sa.Uuid(), nullable=False),
        sa.Column("worker_id", sa.Uuid(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedule.id"],
            name=op.f("fk_requested_task_schedule_id_schedule"),
        ),
        sa.ForeignKeyConstraint(
            ["worker_id"],
            ["worker.id"],
            name=op.f("fk_requested_task_worker_id_worker"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_requested_task")),
        sa.UniqueConstraint("mongo_id", name=op.f("uq_requested_task_mongo_id")),
    )
    op.create_table(
        "task",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("mongo_id", sa.String(), nullable=True),
        sa.Column(
            "events",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("debug", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("timestamp", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("requested_by", sa.String(), nullable=True),
        sa.Column("canceled_by", sa.String(), nullable=True),
        sa.Column("container", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "notification", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("files", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("upload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("schedule_id", sa.Uuid(), nullable=False),
        sa.Column("worker_id", sa.Uuid(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["schedule_id"], ["schedule.id"], name=op.f("fk_task_schedule_id_schedule")
        ),
        sa.ForeignKeyConstraint(
            ["worker_id"], ["worker.id"], name=op.f("fk_task_worker_id_worker")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task")),
        sa.UniqueConstraint("mongo_id", name=op.f("uq_task_mongo_id")),
    )
    op.create_table(
        "schedule_duration",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("default", sa.Boolean(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("on", sa.DateTime(), nullable=False),
        sa.Column("schedule_id", sa.Uuid(), nullable=False),
        sa.Column("worker_id", sa.Uuid(), nullable=True),
        sa.Column("task_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedule.id"],
            name=op.f("fk_schedule_duration_schedule_id_schedule"),
        ),
        sa.ForeignKeyConstraint(
            ["task_id"], ["task.id"], name=op.f("fk_schedule_duration_task_id_task")
        ),
        sa.ForeignKeyConstraint(
            ["worker_id"],
            ["worker.id"],
            name=op.f("fk_schedule_duration_worker_id_worker"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedule_duration")),
    )
    op.create_foreign_key(
        op.f("fk_schedule_most_recent_task_id_task"),
        "schedule",
        "task",
        ["most_recent_task_id"],
        ["id"],
    )
    op.drop_constraint("uq_worker_name", "worker", type_="unique")
    op.create_index(op.f("ix_worker_name"), "worker", ["name"], unique=True)
    op.create_index(op.f("ix_task_updated_at"), "task", ["updated_at"], unique=False)
    op.create_index(
        op.f("ix_requested_task_updated_at"),
        "requested_task",
        ["updated_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_schedule_most_recent_task_id_task"), "schedule", type_="foreignkey"
    )
    op.drop_index(op.f("ix_worker_name"), table_name="worker")
    op.create_unique_constraint("uq_worker_name", "worker", ["name"])
    op.drop_table("schedule_duration")
    op.drop_table("task")
    op.drop_table("requested_task")
    op.drop_index(op.f("ix_schedule_name"), table_name="schedule")
    op.drop_table("schedule")
    # ### end Alembic commands ###
