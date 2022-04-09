"""add foreign-key to posts table

Revision ID: a0306b637c2b
Revises: 22500e3508d5
Create Date: 2022-03-20 22:00:51.057735

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0306b637c2b'
down_revision = '22500e3508d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
