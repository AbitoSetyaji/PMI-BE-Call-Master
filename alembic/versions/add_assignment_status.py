"""add assignment status and completed_at columns

Revision ID: add_assignment_status
Revises: make_vehicle_id_nullable
Create Date: 2024-12-22 16:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_assignment_status'
down_revision = 'make_vehicle_id_nullable'
branch_labels = None
depends_on = None


def upgrade():
    # Add status column with default value 'active'
    op.add_column('assignments', sa.Column('status', sa.String(20), nullable=False, server_default='active'))
    
    # Add completed_at column (nullable)
    op.add_column('assignments', sa.Column('completed_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('assignments', 'status')
    op.drop_column('assignments', 'completed_at')
