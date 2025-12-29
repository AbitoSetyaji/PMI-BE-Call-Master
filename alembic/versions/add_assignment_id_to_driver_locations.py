"""
Revision ID: add_loc_assign_id
Revises: add_assignment_status
Create Date: 2025-12-23 11:42:00.000000

Add assignment_id column to driver_locations table so that:
1. Tracking page can identify which drivers are on duty (have active assignment)
2. Support On Duty vs Idle counter on tracking dashboard
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'add_loc_assign_id'
down_revision = 'add_assignment_status'
branch_labels = None
depends_on = None

def upgrade():
    # Check if column already exists
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('driver_locations')]
    
    if 'assignment_id' not in columns:
        # Add assignment_id column to driver_locations table (nullable)
        op.add_column('driver_locations', 
                      sa.Column('assignment_id', CHAR(36), nullable=True))
        
        # Add foreign key constraint
        op.create_foreign_key(
            'fk_driver_locations_assignment_id',
            'driver_locations',
            'assignments',
            ['assignment_id'],
            ['id']
        )

def downgrade():
    # Check if foreign key exists before dropping
    try:
        op.drop_constraint('fk_driver_locations_assignment_id', 'driver_locations', type_='foreignkey')
    except:
        pass
    
    # Check if column exists before dropping
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('driver_locations')]
    
    if 'assignment_id' in columns:
        op.drop_column('driver_locations', 'assignment_id')

