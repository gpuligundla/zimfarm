"""Store refresh tokens

Revision ID: fe65a1b0f953
Revises: cbedcefd6059
Create Date: 2023-04-03 21:12:33.745734

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fe65a1b0f953"
down_revision = "cbedcefd6059"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refresh_token",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("mongo_val", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("mongo_id", sa.String(), nullable=True),
        sa.Column(
            "token",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("expire_time", sa.DateTime(timezone=False), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mongo_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("refresh_token")
    # ### end Alembic commands ###
