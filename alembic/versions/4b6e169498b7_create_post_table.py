"""create post table

Revision ID: 4b6e169498b7
Revises: 
Create Date: 2022-01-09 14:02:42.106205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b6e169498b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
