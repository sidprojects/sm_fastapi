"""add foreign key to posts table

Revision ID: 843cba65777c
Revises: b35f5bfcb0bc
Create Date: 2022-01-09 14:37:38.860614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843cba65777c'
down_revision = 'b35f5bfcb0bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
