"""add remaining cols to posts table

Revision ID: f935fd768f28
Revises: 843cba65777c
Create Date: 2022-01-09 15:06:37.765796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f935fd768f28'
down_revision = '843cba65777c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
    server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_column("posts", 'created_at')
    op.drop_column("posts", "published")
