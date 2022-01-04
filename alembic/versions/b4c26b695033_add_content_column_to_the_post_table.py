"""add content column to the post table

Revision ID: b4c26b695033
Revises: 94bab396d1c8
Create Date: 2022-01-04 11:02:27.279231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c26b695033'
down_revision = '94bab396d1c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('content')
    pass
