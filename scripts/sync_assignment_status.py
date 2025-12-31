"""
Script to sync Assignment status with Report status
Run this once after migration to update existing data
"""
import asyncio
from sqlalchemy import select
from db.session import get_db, engine
from sqlalchemy.ext.asyncio import AsyncSession
from models.assignment import Assignment
from models.report import Report


async def sync_assignment_status():
    """Sync all assignment statuses based on their report status"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Get all assignments
        result = await db.execute(select(Assignment))
        assignments = result.scalars().all()
        
        print(f"Found {len(assignments)} assignments to sync")
        
        for assignment in assignments:
            # Get the related report
            result = await db.execute(
                select(Report).where(Report.id == assignment.report_id)
            )
            report = result.scalar_one_or_none()
            
            if report:
                old_status = assignment.status
                
                # Map report status to assignment status
                status_mapping = {
                    "pending": "active",
                    "assigned": "assigned",
                    "on_way": "on_progress",
                    "arrived_pickup": "on_progress",
                    "arrived_destination": "on_progress",
                    "done": "completed",
                    "canceled": "cancelled"
                }
                
                new_status = status_mapping.get(report.status, "active")
                assignment.status = new_status
                
                print(f"Assignment {assignment.id[:8]}... : Report status '{report.status}' -> Assignment status '{new_status}' (was '{old_status}')")
        
        await db.commit()
        print("\n✅ All assignments synced successfully!")


if __name__ == "__main__":
    asyncio.run(sync_assignment_status())
