"""create posts table

Revision ID: 9e79e78daab2
Revises: 
Create Date: 2022-03-19 17:27:51.785299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e79e78daab2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
