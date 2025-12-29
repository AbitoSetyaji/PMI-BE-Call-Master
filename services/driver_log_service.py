from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from models.driver_log import DriverVehicleLog
from models.user import User
from models.vehicle import Vehicle
from models.report import Report
from schemas.driver_log import DriverVehicleLogCreate, DriverVehicleLogComplete
import uuid
from datetime import datetime


async def get_all_driver_logs(db: AsyncSession, current_user: User) -> List[DriverVehicleLog]:
    """
    Get all driver logs (admin only)
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of driver logs
        
    Raises:
        HTTPException: If not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat melihat semua log"
        )
    
    result = await db.execute(select(DriverVehicleLog))
    logs = result.scalars().all()
    return list(logs)


async def start_driver_log(
    db: AsyncSession,
    log_data: DriverVehicleLogCreate,
    current_user: User
) -> DriverVehicleLog:
    """
    Start a driver log (create new log entry)
    
    Args:
        db: Database session
        log_data: Log creation data
        current_user: Current authenticated user
        
    Returns:
        Created driver log
        
    Raises:
        HTTPException: If validation fails
    """
    # Verify driver exists
    result = await db.execute(
        select(User).where(and_(User.id == log_data.driver_id, User.role == "driver"))
    )
    driver = result.scalar_one_or_none()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver tidak ditemukan"
        )
    
    # Driver can only create log for themselves
    if current_user.role == "driver" and current_user.id != log_data.driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver hanya dapat membuat log untuk diri sendiri"
        )
    
    # Verify vehicle exists and available
    result = await db.execute(select(Vehicle).where(Vehicle.id == log_data.vehicle_id))
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    if vehicle.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Kendaraan sedang {vehicle.status}"
        )
    
    # Verify report exists
    result = await db.execute(select(Report).where(Report.id == log_data.report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Create driver log
    new_log = DriverVehicleLog(
        id=str(uuid.uuid4()),
        driver_id=log_data.driver_id,
        vehicle_id=log_data.vehicle_id,
        report_id=log_data.report_id,
        start_location=log_data.start_location
    )
    
    # Update vehicle status to in_use
    vehicle.status = "in_use"
    
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    
    return new_log


async def end_driver_log(
    db: AsyncSession,
    driver_id: str,
    report_id: str,
    complete_data: DriverVehicleLogComplete,
    current_user: User
) -> DriverVehicleLog:
    """
    End a driver log (complete the log entry)
    
    Args:
        db: Database session
        driver_id: Driver ID
        report_id: Report ID
        complete_data: Completion data
        current_user: Current authenticated user
        
    Returns:
        Updated driver log
        
    Raises:
        HTTPException: If validation fails or log not found
    """
    # Driver can only end their own log
    if current_user.role == "driver" and current_user.id != driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver hanya dapat menyelesaikan log sendiri"
        )
    
    # Find active log
    result = await db.execute(
        select(DriverVehicleLog).where(
            and_(
                DriverVehicleLog.driver_id == driver_id,
                DriverVehicleLog.report_id == report_id,
                DriverVehicleLog.end_time == None
            )
        )
    )
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log aktif tidak ditemukan"
        )
    
    # Update log
    log.end_time = datetime.utcnow()
    log.end_location = complete_data.end_location
    
    # Update vehicle status back to available
    result = await db.execute(select(Vehicle).where(Vehicle.id == log.vehicle_id))
    vehicle = result.scalar_one_or_none()
    
    if vehicle:
        vehicle.status = "available"
    
    await db.commit()
    await db.refresh(log)
    
    return log


async def get_driver_log_by_id(db: AsyncSession, log_id: str, current_user: User) -> DriverVehicleLog:
    """
    Get driver log by ID
    
    Args:
        db: Database session
        log_id: Log ID
        current_user: Current authenticated user
        
    Returns:
        Driver log
        
    Raises:
        HTTPException: If log not found or no permission
    """
    result = await db.execute(select(DriverVehicleLog).where(DriverVehicleLog.id == log_id))
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log tidak ditemukan"
        )
    
    # Check permissions
    if current_user.role == "driver" and log.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke log ini"
        )
    
    return log
