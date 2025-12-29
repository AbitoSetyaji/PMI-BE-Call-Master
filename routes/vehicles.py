from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from services import vehicle_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_vehicles(
    page: int = 1,
    size: int = 10,
    status: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all vehicles
    
    Args:
        page: Page number (default: 1)
        size: Items per page (default: 10)
        status: Filter by status (optional)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of vehicles
    """
    return await vehicle_service.get_all_vehicles(db, page, size, status)


@router.get("/{vehicle_id}", status_code=status.HTTP_200_OK)
async def get_vehicle(
    vehicle_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get vehicle by ID
    
    Args:
        vehicle_id: Vehicle ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Vehicle details
    """
    return await vehicle_service.get_vehicle_by_id(db, vehicle_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new vehicle (admin only)
    
    Args:
        vehicle_data: Vehicle creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created vehicle
    """
    return await vehicle_service.create_vehicle(db, vehicle_data, current_user)


@router.put("/{vehicle_id}", status_code=status.HTTP_200_OK)
async def update_vehicle(
    vehicle_id: str,
    vehicle_data: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update vehicle information (admin only)
    
    Args:
        vehicle_id: Vehicle ID
        vehicle_data: Update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated vehicle
    """
    return await vehicle_service.update_vehicle(db, vehicle_id, vehicle_data, current_user)


@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
async def delete_vehicle(
    vehicle_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete vehicle (admin only)
    
    Args:
        vehicle_id: Vehicle ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return await vehicle_service.delete_vehicle(db, vehicle_id, current_user)
