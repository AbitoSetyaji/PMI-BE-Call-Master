from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.driver_location import DriverLocationCreate, DriverLocationResponse
from services import driver_location_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_driver_location(
    location_data: DriverLocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new driver location entry
    - Timestamp is set automatically
    - Driver sends location updates during journey
    
    Args:
        location_data: Location data (driver_id, latitude, longitude)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created driver location
    """
    return await driver_location_service.create_driver_location(db, location_data, current_user)


# IMPORTANT: This route MUST be defined BEFORE /{driver_id} routes
# Otherwise, FastAPI will match "/all/active" as driver_id="all"
@router.get("/all/active", status_code=status.HTTP_200_OK)
async def get_all_active_driver_locations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get latest location for all active drivers (admin only)
    Used for dashboard map view
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of driver locations with driver info
    """
    return await driver_location_service.get_all_active_driver_locations(db, current_user)


@router.get("/{driver_id}", status_code=status.HTTP_200_OK)
async def get_driver_latest_location(
    driver_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the latest location of a specific driver
    
    Args:
        driver_id: Driver ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Latest driver location
    """
    location = await driver_location_service.get_driver_latest_location(db, driver_id, current_user)
    
    if not location:
        return {
            "message": "Belum ada data lokasi untuk driver ini"
        }
    
    return location


@router.get("/{driver_id}/history", status_code=status.HTTP_200_OK)
async def get_driver_location_history(
    driver_id: str,
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get driver location history
    
    Args:
        driver_id: Driver ID
        page: Page number (default: 1)
        size: Items per page (default: 50)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of driver locations
    """
    return await driver_location_service.get_driver_location_history(db, driver_id, current_user, page, size)
