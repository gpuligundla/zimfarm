"""remove_ssh_key_last_used

Revision ID: ceae21f592b7
Revises: 43f385b318d4
Create Date: 2023-09-29 10:59:39.739351

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ceae21f592b7"
down_revision = "43f385b318d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sshkey", "last_used")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sshkey",
        sa.Column(
            "last_used", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
