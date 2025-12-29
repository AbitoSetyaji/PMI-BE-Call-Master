from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from models.report import Report
from models.user import User
from models.driver_log import DriverVehicleLog
from models.vehicle import Vehicle
from schemas.report import ReportCreate, ReportUpdate, ReportAssign
import uuid
from datetime import datetime


async def get_all_reports(
    db: AsyncSession, 
    current_user: User,
    assigned_to_me: bool = False
) -> List[Report]:
    """
    Get reports based on user role
    
    Args:
        db: Database session
        current_user: Current authenticated user
        assigned_to_me: Filter for assigned reports
        
    Returns:
        List of reports
    """
    if current_user.role == "admin":
        # Admin can see all reports
        result = await db.execute(select(Report))
    elif current_user.role == "reporter":
        # Reporter can only see their own reports
        result = await db.execute(
            select(Report).where(Report.reporter_id == current_user.id)
        )
    elif current_user.role == "driver":
        if assigned_to_me:
            # Driver can see reports assigned to them
            result = await db.execute(
                select(Report).where(Report.driver_id == current_user.id)
            )
        else:
            # Or all available reports
            result = await db.execute(select(Report))
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role tidak valid"
        )
    
    reports = result.scalars().all()
    return list(reports)


async def get_report_by_id(db: AsyncSession, report_id: str, current_user: User) -> Report:
    """
    Get report by ID
    
    Args:
        db: Database session
        report_id: Report ID
        current_user: Current authenticated user
        
    Returns:
        Report object
        
    Raises:
        HTTPException: If report not found or no permission
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Check permissions
    if current_user.role == "reporter" and report.reporter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke laporan ini"
        )
    
    if current_user.role == "driver" and report.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke laporan ini"
        )
    
    return report


async def create_report(db: AsyncSession, report_data: ReportCreate, current_user: User) -> Report:
    """
    Create new report
    
    Args:
        db: Database session
        report_data: Report creation data
        current_user: Current authenticated user
        
    Returns:
        Created report
        
    Raises:
        HTTPException: If reporter_id doesn't exist
    """
    # Verify reporter exists
    result = await db.execute(select(User).where(User.id == report_data.reporter_id))
    reporter = result.scalar_one_or_none()
    
    if not reporter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporter tidak ditemukan"
        )
    
    # Create new report
    new_report = Report(
        id=str(uuid.uuid4()),
        reporter_id=report_data.reporter_id,
        location=report_data.location,
        incident_type=report_data.incident_type,
        requested_items=report_data.requested_items,
        status="pending"
    )
    
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    
    return new_report


async def assign_report(
    db: AsyncSession, 
    report_id: str, 
    assign_data: ReportAssign,
    current_user: User
) -> Report:
    """
    Assign driver to report (admin only)
    
    Args:
        db: Database session
        report_id: Report ID
        assign_data: Assignment data
        current_user: Current authenticated user
        
    Returns:
        Updated report
        
    Raises:
        HTTPException: If not admin or report not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menetapkan driver"
        )
    
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Verify driver exists if provided
    if assign_data.driver_id:
        result = await db.execute(
            select(User).where(
                and_(User.id == assign_data.driver_id, User.role == "driver")
            )
        )
        driver = result.scalar_one_or_none()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver tidak ditemukan"
            )
        report.driver_id = assign_data.driver_id
    
    if assign_data.admin_id:
        report.admin_id = assign_data.admin_id
    
    report.status = assign_data.status
    
    await db.commit()
    await db.refresh(report)
    
    return report


async def update_report_status(
    db: AsyncSession,
    report_id: str,
    new_status: str,
    current_user: User,
    vehicle_id: Optional[str] = None,
    start_location: Optional[str] = None,
    end_location: Optional[str] = None
) -> Report:
    """
    Update report status with business logic
    
    Args:
        db: Database session
        report_id: Report ID
        new_status: New status
        current_user: Current authenticated user
        vehicle_id: Vehicle ID for on_the_way status
        start_location: Start location for on_the_way status
        end_location: End location for handled status
        
    Returns:
        Updated report
        
    Raises:
        HTTPException: If validation fails
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Validate permissions
    if current_user.role == "driver" and report.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak ditugaskan untuk laporan ini"
        )
    
    # Handle status transition to "on_the_way"
    if new_status == "on_the_way":
        if not vehicle_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle ID diperlukan untuk status on_the_way"
            )
        
        # Verify vehicle exists and available
        result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
        vehicle = result.scalar_one_or_none()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kendaraan tidak ditemukan"
            )
        
        if vehicle.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kendaraan tidak tersedia"
            )
        
        # Create driver log
        new_log = DriverVehicleLog(
            id=str(uuid.uuid4()),
            driver_id=current_user.id,
            vehicle_id=vehicle_id,
            report_id=report_id,
            start_location=start_location or report.location
        )
        
        # Update vehicle status
        vehicle.status = "in_use"
        
        db.add(new_log)
    
    # Handle status transition to "handled"
    elif new_status == "handled":
        # Find active driver log
        result = await db.execute(
            select(DriverVehicleLog).where(
                and_(
                    DriverVehicleLog.report_id == report_id,
                    DriverVehicleLog.end_time == None
                )
            )
        )
        active_log = result.scalar_one_or_none()
        
        if active_log:
            # Update log end time
            active_log.end_time = datetime.utcnow()
            active_log.end_location = end_location or report.location
            
            # Update vehicle status back to available
            result = await db.execute(
                select(Vehicle).where(Vehicle.id == active_log.vehicle_id)
            )
            vehicle = result.scalar_one_or_none()
            if vehicle:
                vehicle.status = "available"
    
    # Update report status
    report.status = new_status
    
    await db.commit()
    await db.refresh(report)
    
    return report


async def update_report(
    db: AsyncSession,
    report_id: str,
    report_data: ReportUpdate,
    current_user: User
) -> Report:
    """
    Update report information
    
    Args:
        db: Database session
        report_id: Report ID
        report_data: Update data
        current_user: Current authenticated user
        
    Returns:
        Updated report
        
    Raises:
        HTTPException: If report not found or no permission
    """
    if current_user.role not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat mengubah laporan"
        )
    
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Update fields
    if report_data.location:
        report.location = report_data.location
    if report_data.incident_type:
        report.incident_type = report_data.incident_type
    if report_data.status:
        report.status = report_data.status
    if report_data.requested_items:
        report.requested_items = report_data.requested_items
    if report_data.admin_id:
        report.admin_id = report_data.admin_id
    if report_data.driver_id:
        report.driver_id = report_data.driver_id
    
    await db.commit()
    await db.refresh(report)
    
    return report


async def delete_report(db: AsyncSession, report_id: str, current_user: User) -> dict:
    """
    Delete report (admin only)
    
    Args:
        db: Database session
        report_id: Report ID
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not admin or report not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menghapus laporan"
        )
    
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    await db.delete(report)
    await db.commit()
    
    return {"message": "Laporan berhasil dihapus"}
