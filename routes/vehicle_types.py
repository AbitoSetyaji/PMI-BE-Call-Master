from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse
from services import vehicle_type_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_vehicle_types(
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all vehicle types
    
    Args:
        page: Page number (default: 1)
        size: Items per page (default: 10)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of vehicle types
    """
    return await vehicle_type_service.get_all_vehicle_types(db, page, size)


@router.get("/{vehicle_type_id}", status_code=status.HTTP_200_OK)
async def get_vehicle_type(
    vehicle_type_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get vehicle type by ID
    
    Args:
        vehicle_type_id: Vehicle type ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Vehicle type details
    """
    return await vehicle_type_service.get_vehicle_type_by_id(db, vehicle_type_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vehicle_type(
    vehicle_type_data: VehicleTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new vehicle type (admin only)
    
    Args:
        vehicle_type_data: Vehicle type creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created vehicle type
    """
    return await vehicle_type_service.create_vehicle_type(db, vehicle_type_data, current_user)


@router.put("/{vehicle_type_id}", status_code=status.HTTP_200_OK)
async def update_vehicle_type(
    vehicle_type_id: str,
    vehicle_type_data: VehicleTypeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update vehicle type (admin only)
    
    Args:
        vehicle_type_id: Vehicle type ID
        vehicle_type_data: Update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated vehicle type
    """
    return await vehicle_type_service.update_vehicle_type(db, vehicle_type_id, vehicle_type_data, current_user)


@router.delete("/{vehicle_type_id}", status_code=status.HTTP_200_OK)
async def delete_vehicle_type(
    vehicle_type_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete vehicle type (admin only)
    
    Args:
        vehicle_type_id: Vehicle type ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return await vehicle_type_service.delete_vehicle_type(db, vehicle_type_id, current_user)
