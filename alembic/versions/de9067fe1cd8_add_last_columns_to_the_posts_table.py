"""add last columns to the posts table

Revision ID: de9067fe1cd8
Revises: c2d6c009e5bf
Create Date: 2022-01-04 12:51:12.353140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de9067fe1cd8'
down_revision = 'c2d6c009e5bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('getdate()'), nullable=False))

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created at')

    pass
