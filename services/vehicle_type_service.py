from typing import Any, Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from models.vehicle_type import VehicleType
from models.user import User
from schemas.vehicle_type import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse
from utils.response import success_response, paginated_response
import uuid


async def get_all_vehicle_types(db: AsyncSession, page: int = 1, size: int = 10) -> Dict[str, Any]:
    """
    Get all vehicle types with pagination
    
    Args:
        db: Database session
        page: Page number (default: 1)
        size: Items per page (default: 10)
        
    Returns:
        Paginated list of vehicle types
    """
    # Get total count
    total_result = await db.execute(select(func.count()).select_from(VehicleType))
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        select(VehicleType)
        .offset((page - 1) * size)
        .limit(size)
    )
    vehicle_types = result.scalars().all()
    
    vehicle_types_list = [VehicleTypeResponse.model_validate(vt).model_dump() for vt in vehicle_types]
    
    return paginated_response(
        message="Data jenis kendaraan berhasil diambil",
        items=vehicle_types_list,
        total=total,
        page=page,
        size=size
    )


async def get_vehicle_type_by_id(db: AsyncSession, vehicle_type_id: str) -> Dict[str, Any]:
    """
    Get vehicle type by ID
    
    Args:
        db: Database session
        vehicle_type_id: Vehicle type ID
        
    Returns:
        Vehicle type data
        
    Raises:
        HTTPException: If vehicle type not found
    """
    result = await db.execute(select(VehicleType).where(VehicleType.id == vehicle_type_id))
    vehicle_type = result.scalar_one_or_none()
    
    if not vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis kendaraan tidak ditemukan"
        )
    
    return success_response(
        message="Data jenis kendaraan berhasil diambil",
        data=VehicleTypeResponse.model_validate(vehicle_type).model_dump()
    )


async def create_vehicle_type(
    db: AsyncSession,
    vehicle_type_data: VehicleTypeCreate,
    current_user: User
) -> Dict[str, Any]:
    """
    Create new vehicle type (admin only)
    
    Args:
        db: Database session
        vehicle_type_data: Vehicle type creation data
        current_user: Current authenticated user
        
    Returns:
        Created vehicle type data
        
    Raises:
        HTTPException: If not admin or name already exists
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menambah jenis kendaraan"
        )
    
    # Check if name already exists
    result = await db.execute(
        select(VehicleType).where(VehicleType.name == vehicle_type_data.name)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Jenis kendaraan dengan nama ini sudah ada"
        )
    
    # Create new vehicle type
    new_vehicle_type = VehicleType(
        id=str(uuid.uuid4()),
        name=vehicle_type_data.name,
    )
    
    db.add(new_vehicle_type)
    await db.commit()
    await db.refresh(new_vehicle_type)
    
    return success_response(
        message="Jenis kendaraan berhasil ditambahkan",
        data=VehicleTypeResponse.model_validate(new_vehicle_type).model_dump()
    )


async def update_vehicle_type(
    db: AsyncSession,
    vehicle_type_id: str,
    vehicle_type_data: VehicleTypeUpdate,
    current_user: User
) -> Dict[str, Any]:
    """
    Update vehicle type (admin only)
    
    Args:
        db: Database session
        vehicle_type_id: Vehicle type ID
        vehicle_type_data: Update data
        current_user: Current authenticated user
        
    Returns:
        Updated vehicle type data
        
    Raises:
        HTTPException: If not admin or vehicle type not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat mengubah jenis kendaraan"
        )
    
    result = await db.execute(select(VehicleType).where(VehicleType.id == vehicle_type_id))
    vehicle_type = result.scalar_one_or_none()
    
    if not vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis kendaraan tidak ditemukan"
        )
    
    # Update fields
    if vehicle_type_data.name:
        # Check if new name already exists
        result = await db.execute(
            select(VehicleType).where(
                VehicleType.name == vehicle_type_data.name,
                VehicleType.id != vehicle_type_id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nama jenis kendaraan sudah digunakan"
            )
        vehicle_type.name = vehicle_type_data.name
   
    await db.commit()
    await db.refresh(vehicle_type)
    
    return success_response(
        message="Jenis kendaraan berhasil diupdate",
        data=VehicleTypeResponse.model_validate(vehicle_type).model_dump()
    )


async def delete_vehicle_type(
    db: AsyncSession,
    vehicle_type_id: str,
    current_user: User
) -> Dict[str, Any]:
    """
    Delete vehicle type (admin only)
    
    Args:
        db: Database session
        vehicle_type_id: Vehicle type ID
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not admin or vehicle type not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menghapus jenis kendaraan"
        )
    
    result = await db.execute(select(VehicleType).where(VehicleType.id == vehicle_type_id))
    vehicle_type = result.scalar_one_or_none()
    
    if not vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis kendaraan tidak ditemukan"
        )
    
    await db.delete(vehicle_type)
    await db.commit()
    
    return success_response(
        message="Jenis kendaraan berhasil dihapus",
        data={"id": vehicle_type_id}
    )
