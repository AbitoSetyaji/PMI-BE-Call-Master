from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.driver_log import (
    DriverVehicleLogCreate, 
    DriverVehicleLogResponse,
    DriverVehicleLogComplete
)
from services import driver_log_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_driver_logs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all driver logs (admin only)
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of driver logs
    """
    return await driver_log_service.get_all_driver_logs(db, current_user)


@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_driver_log(
    log_data: DriverVehicleLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start a driver log (driver begins journey)
    - Creates new log entry
    - Sets start_time automatically
    - Updates vehicle status to in_use
    
    Args:
        log_data: Log creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created driver log
    """
    return await driver_log_service.start_driver_log(db, log_data, current_user)


@router.post("/end", status_code=status.HTTP_200_OK)
async def end_driver_log(
    driver_id: str,
    report_id: str,
    complete_data: DriverVehicleLogComplete,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    End a driver log (driver completes journey)
    - Sets end_time automatically
    - Updates vehicle status to available
    
    Args:
        driver_id: Driver ID
        report_id: Report ID
        complete_data: Completion data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Completed driver log
    """
    return await driver_log_service.end_driver_log(db, driver_id, report_id, complete_data, current_user)


@router.get("/{log_id}", status_code=status.HTTP_200_OK)
async def get_driver_log(
    log_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get driver log by ID
    
    Args:
        log_id: Log ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Driver log details
    """
    return await driver_log_service.get_driver_log_by_id(db, log_id, current_user)
