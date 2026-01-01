"""Add coffin_checklist_confirmed column to assignments

Revision ID: add_coffin_checklist
Revises: add_loc_assign_id
Create Date: 2026-01-01 14:45:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_coffin_checklist'
down_revision = 'add_loc_assign_id'
branch_labels = None
depends_on = None


def upgrade():
    # Add coffin_checklist_confirmed column to assignments table
    op.add_column('assignments', sa.Column('coffin_checklist_confirmed', sa.Boolean(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('assignments', 'coffin_checklist_confirmed')
