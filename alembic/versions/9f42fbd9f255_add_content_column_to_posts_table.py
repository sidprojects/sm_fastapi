"""add content column to posts table

Revision ID: 9f42fbd9f255
Revises: 4b6e169498b7
Create Date: 2022-01-09 14:13:37.177662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '9f42fbd9f255'
down_revision = '4b6e169498b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
