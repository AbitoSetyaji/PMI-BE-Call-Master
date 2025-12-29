from typing import Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from models.vehicle import Vehicle
from models.vehicle_type import VehicleType
from models.user import User
from schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleWithTypeResponse
from utils.response import success_response, paginated_response
import uuid


async def get_all_vehicles(db: AsyncSession, page: int = 1, size: int = 10, status_filter: str = None) -> dict:
    """
    Get all vehicles with pagination
    
    Args:
        db: Database session
        page: Page number (default: 1)
        size: Items per page (default: 10)
        status_filter: Filter by status (optional)
        
    Returns:
        Paginated list of vehicles
    """
    # Build base query with optional status filter
    base_query = select(Vehicle).options(selectinload(Vehicle.vehicle_type))
    if status_filter and status_filter in ["available", "in_use", "maintenance", "on_duty"]:
        base_query = base_query.where(Vehicle.status == status_filter)
    
    # Get total count
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        base_query.offset((page - 1) * size).limit(size)
    )
    vehicles = result.scalars().all()
    
    vehicles_list = []
    for v in vehicles:
        vehicle_dict = VehicleResponse.model_validate(v).model_dump()
        vehicle_dict["vehicle_type_name"] = v.vehicle_type.name if v.vehicle_type else None
        vehicles_list.append(vehicle_dict)
    
    return paginated_response(
        message="Data kendaraan berhasil diambil",
        items=vehicles_list,
        total=total,
        page=page,
        size=size
    )


async def get_vehicle_by_id(db: AsyncSession, vehicle_id: str) -> dict:
    """
    Get vehicle by ID
    
    Args:
        db: Database session
        vehicle_id: Vehicle ID
        
    Returns:
        Vehicle data
        
    Raises:
        HTTPException: If vehicle not found
    """
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .where(Vehicle.id == vehicle_id)
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    vehicle_dict = VehicleResponse.model_validate(vehicle).model_dump()
    vehicle_dict["vehicle_type_name"] = vehicle.vehicle_type.name if vehicle.vehicle_type else None
    
    return success_response(
        message="Data kendaraan berhasil diambil",
        data=vehicle_dict
    )


async def create_vehicle(
    db: AsyncSession, 
    vehicle_data: VehicleCreate,
    current_user: User
) -> dict:
    """
    Create new vehicle (admin only)
    
    Args:
        db: Database session
        vehicle_data: Vehicle creation data
        current_user: Current authenticated user
        
    Returns:
        Created vehicle data
        
    Raises:
        HTTPException: If not admin or plate number already exists
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menambah kendaraan"
        )
    
    # Verify vehicle type exists
    result = await db.execute(select(VehicleType).where(VehicleType.id == vehicle_data.type))
    vehicle_type = result.scalar_one_or_none()
    
    if not vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis kendaraan tidak ditemukan"
        )
    
    # Check if plate number already exists
    result = await db.execute(
        select(Vehicle).where(Vehicle.plate_number == vehicle_data.plate_number)
    )
    existing_vehicle = result.scalar_one_or_none()
    
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nomor plat sudah terdaftar"
        )
    
    # Create new vehicle
    new_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        name=vehicle_data.name,
        plate_number=vehicle_data.plate_number,
        type=vehicle_data.type,
        status=vehicle_data.status or "available"
    )
    
    db.add(new_vehicle)
    await db.commit()
    
    # Refresh and load vehicle_type
    await db.refresh(new_vehicle)
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .where(Vehicle.id == new_vehicle.id)
    )
    new_vehicle = result.scalar_one()
    
    vehicle_dict = VehicleResponse.model_validate(new_vehicle).model_dump()
    vehicle_dict["vehicle_type_name"] = new_vehicle.vehicle_type.name if new_vehicle.vehicle_type else None
    
    return success_response(
        message="Kendaraan berhasil ditambahkan",
        data=vehicle_dict
    )


async def update_vehicle(
    db: AsyncSession,
    vehicle_id: str,
    vehicle_data: VehicleUpdate,
    current_user: User
) -> dict:
    """
    Update vehicle information (admin only)
    
    Args:
        db: Database session
        vehicle_id: Vehicle ID
        vehicle_data: Update data
        current_user: Current authenticated user
        
    Returns:
        Updated vehicle
        
    Raises:
        HTTPException: If not admin or vehicle not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat mengubah kendaraan"
        )
    
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    # Update fields
    if vehicle_data.name:
        vehicle.name = vehicle_data.name
    if vehicle_data.type:
        # Verify vehicle type exists
        result = await db.execute(select(VehicleType).where(VehicleType.id == vehicle_data.type))
        vehicle_type = result.scalar_one_or_none()
        if not vehicle_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jenis kendaraan tidak ditemukan"
            )
        vehicle.type = vehicle_data.type
    if vehicle_data.plate_number:
        # Check if new plate number already exists
        result = await db.execute(
            select(Vehicle).where(
                Vehicle.plate_number == vehicle_data.plate_number,
                Vehicle.id != vehicle_id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nomor plat sudah digunakan oleh kendaraan lain"
            )
        vehicle.plate_number = vehicle_data.plate_number
    if vehicle_data.status:
        vehicle.status = vehicle_data.status
    
    await db.commit()
    
    # Refresh and load vehicle_type
    result = await db.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.vehicle_type))
        .where(Vehicle.id == vehicle_id)
    )
    vehicle = result.scalar_one()
    
    vehicle_dict = VehicleResponse.model_validate(vehicle).model_dump()
    vehicle_dict["vehicle_type_name"] = vehicle.vehicle_type.name if vehicle.vehicle_type else None
    
    return success_response(
        message="Kendaraan berhasil diupdate",
        data=vehicle_dict
    )


async def delete_vehicle(db: AsyncSession, vehicle_id: str, current_user: User) -> dict:
    """
    Delete vehicle (admin only)
    
    Args:
        db: Database session
        vehicle_id: Vehicle ID
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not admin or vehicle not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menghapus kendaraan"
        )
    
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    await db.delete(vehicle)
    await db.commit()
    
    return success_response(
        message="Kendaraan berhasil dihapus",
        data={"id": vehicle_id}
    )
