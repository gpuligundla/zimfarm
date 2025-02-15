"""User: username is mandatory + unique

Revision ID: f1a7eae2c347
Revises: dc811d96975c
Create Date: 2023-03-31 18:05:44.896451

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f1a7eae2c347"
down_revision = "dc811d96975c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("user", "username", existing_type=sa.VARCHAR(), nullable=False)
    op.create_unique_constraint("username_unq", "user", ["username"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("username_unq", "user", type_="unique")
    op.alter_column("user", "username", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###
