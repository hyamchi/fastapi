"""create users table

Revision ID: ce19164dcf53
Revises: b4c26b695033
Create Date: 2022-01-04 12:19:57.561037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce19164dcf53'
down_revision = 'b4c26b695033'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('email', sa.String(50), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.DateTime(), server_default=sa.text('getdate()'), nullable=False), sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
