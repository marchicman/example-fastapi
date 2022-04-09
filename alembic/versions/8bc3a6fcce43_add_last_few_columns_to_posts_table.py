"""add last few columns to posts table

Revision ID: 8bc3a6fcce43
Revises: a0306b637c2b
Create Date: 2022-04-04 05:22:31.087922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bc3a6fcce43'
down_revision = 'a0306b637c2b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
