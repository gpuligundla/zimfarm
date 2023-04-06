"""Add Worker Table

Revision ID: 96203f95bc36
Revises: 4de2adfc3d11
Create Date: 2023-04-06 15:56:02.435956

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "96203f95bc36"
down_revision = "4de2adfc3d11"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "worker",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("mongo_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("selfish", sa.Boolean(), nullable=False),
        sa.Column("cpu", sa.Integer(), nullable=False),
        sa.Column("memory", sa.BigInteger(), nullable=False),
        sa.Column("disk", sa.BigInteger(), nullable=False),
        sa.Column("offliners", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("platforms", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=True),
        sa.Column("last_ip", postgresql.INET(), nullable=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_worker_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_worker")),
        sa.UniqueConstraint("mongo_id", name=op.f("uq_worker_mongo_id")),
        sa.UniqueConstraint("name", name=op.f("uq_worker_name")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("worker")
    # ### end Alembic commands ###
