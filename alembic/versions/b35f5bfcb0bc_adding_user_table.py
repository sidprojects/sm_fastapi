"""adding user table

Revision ID: b35f5bfcb0bc
Revises: 9f42fbd9f255
Create Date: 2022-01-09 14:23:31.053040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = 'b35f5bfcb0bc'
down_revision = '9f42fbd9f255'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table("users")
