"""
Revision ID: make_vehicle_id_nullable
Revises: bec85b7efbe1
Create Date: 2025-12-10 00:00:00.000000

Make vehicle_id nullable in assignments table so that:
1. Admin/Reporter creates assignment and assigns Driver (vehicle_id = null)
2. Driver accepts and selects a vehicle (vehicle_id gets filled)
3. Driver executes the assignment
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import CHAR

# revision identifiers, used by Alembic.
revision = 'make_vehicle_id_nullable'
down_revision = 'bec85b7efbe1'
branch_labels = None
depends_on = None

def upgrade():
    # Make vehicle_id nullable in assignments table
    op.alter_column('assignments', 'vehicle_id', 
                    existing_type=CHAR(36), 
                    nullable=True)

def downgrade():
    # Revert: make vehicle_id not nullable
    op.alter_column('assignments', 'vehicle_id', 
                    existing_type=CHAR(36), 
                    nullable=False)
