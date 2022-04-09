"""add user table

Revision ID: 22500e3508d5
Revises: 6becae7f7069
Create Date: 2022-03-20 21:34:34.450214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22500e3508d5'
down_revision = '6becae7f7069'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('email', sa.String(), nullable=False),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
