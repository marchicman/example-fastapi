"""add content column to posts table

Revision ID: 6becae7f7069
Revises: 9e79e78daab2
Create Date: 2022-03-19 17:40:34.915956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6becae7f7069'
down_revision = '9e79e78daab2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
