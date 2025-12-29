from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from fastapi import HTTPException, status
from models.driver_location import DriverLocation
from models.user import User
from schemas.driver_location import DriverLocationCreate, DriverLocationResponse
from utils.response import success_response, paginated_response
import uuid


async def create_driver_location(
    db: AsyncSession,
    location_data: DriverLocationCreate,
    current_user: User
) -> dict:
    """
    Create new driver location entry
    
    Args:
        db: Database session
        location_data: Location data
        current_user: Current authenticated user
        
    Returns:
        Created driver location data
        
    Raises:
        HTTPException: If validation fails
    """
    # Verify driver exists
    result = await db.execute(
        select(User).where(and_(User.id == location_data.driver_id, User.role == "driver"))
    )
    driver = result.scalar_one_or_none()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver tidak ditemukan"
        )
    
    # Driver can only create location for themselves
    if current_user.role == "driver" and current_user.id != location_data.driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver hanya dapat mengirim lokasi sendiri"
        )
    
    # Create new location entry
    new_location = DriverLocation(
        id=str(uuid.uuid4()),
        driver_id=location_data.driver_id,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        assignment_id=location_data.assignment_id
    )
    
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    
    return success_response(
        message="Lokasi driver berhasil ditambahkan",
        data=DriverLocationResponse.model_validate(new_location).model_dump()
    )


async def get_driver_latest_location(
    db: AsyncSession,
    driver_id: str,
    current_user: User
) -> dict:
    """
    Get the latest location of a driver
    
    Args:
        db: Database session
        driver_id: Driver ID
        current_user: Current authenticated user
        
    Returns:
        Latest driver location data
        
    Raises:
        HTTPException: If driver not found
    """
    # Verify driver exists
    result = await db.execute(
        select(User).where(and_(User.id == driver_id, User.role == "driver"))
    )
    driver = result.scalar_one_or_none()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver tidak ditemukan"
        )
    
    # Get latest location
    result = await db.execute(
        select(DriverLocation)
        .where(DriverLocation.driver_id == driver_id)
        .order_by(desc(DriverLocation.timestamp))
        .limit(1)
    )
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lokasi driver tidak ditemukan"
        )
    
    location_dict = DriverLocationResponse.model_validate(location).model_dump()
    location_dict["driver_name"] = driver.name
    
    return success_response(
        message="Lokasi driver berhasil diambil",
        data=location_dict
    )


async def get_driver_location_history(
    db: AsyncSession,
    driver_id: str,
    current_user: User,
    page: int = 1,
    size: int = 50
) -> dict:
    """
    Get driver location history with pagination
    
    Args:
        db: Database session
        driver_id: Driver ID
        current_user: Current authenticated user
        page: Page number (default: 1)
        size: Items per page (default: 50)
        
    Returns:
        Paginated list of driver locations
        
    Raises:
        HTTPException: If not admin or driver not found
    """
    if current_user.role not in ["admin", "driver"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses untuk melihat riwayat lokasi"
        )
    
    # Verify driver exists
    result = await db.execute(
        select(User).where(and_(User.id == driver_id, User.role == "driver"))
    )
    driver = result.scalar_one_or_none()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver tidak ditemukan"
        )
    
    # Driver can only see their own history
    if current_user.role == "driver" and current_user.id != driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver hanya dapat melihat riwayat lokasi sendiri"
        )
    
    # Get total count
    total_result = await db.execute(
        select(func.count()).select_from(DriverLocation).where(DriverLocation.driver_id == driver_id)
    )
    total = total_result.scalar()
    
    # Get location history
    result = await db.execute(
        select(DriverLocation)
        .where(DriverLocation.driver_id == driver_id)
        .order_by(desc(DriverLocation.timestamp))
        .offset((page - 1) * size)
        .limit(size)
    )
    locations = result.scalars().all()
    
    locations_list = [
        DriverLocationResponse.model_validate(loc).model_dump()
        for loc in locations
    ]
    
    return paginated_response(
        message="Riwayat lokasi driver berhasil diambil",
        items=locations_list,
        total=total,
        page=page,
        size=size
    )


async def get_all_active_driver_locations(
    db: AsyncSession,
    current_user: User
) -> dict:
    """
    Get latest location for all drivers (admin/reporter only)
    Shows all drivers including those who haven't shared location yet
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of driver locations with driver info, assignment and report details
        
    Raises:
        HTTPException: If not admin/reporter
    """
    if current_user.role not in ["admin", "reporter"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin dan reporter yang dapat melihat semua lokasi driver"
        )
    
    # Import models here to avoid circular imports
    from models.assignment import Assignment
    from models.report import Report
    from models.vehicle import Vehicle
    
    # Get all drivers
    result = await db.execute(select(User).where(User.role == "driver"))
    drivers = result.scalars().all()
    
    driver_locations = []
    
    # Default location (Jakarta - PMI HQ) for drivers without location
    DEFAULT_LATITUDE = -6.2088
    DEFAULT_LONGITUDE = 106.8456
    
    for driver in drivers:
        # Get latest location for each driver
        result = await db.execute(
            select(DriverLocation)
            .where(DriverLocation.driver_id == driver.id)
            .order_by(desc(DriverLocation.timestamp))
            .limit(1)
        )
        location = result.scalar_one_or_none()
        
        if location:
            # Driver has location data
            location_dict = DriverLocationResponse.model_validate(location).model_dump()
            location_dict["driver_name"] = driver.name
            location_dict["has_location"] = True
            
            # If there's an assignment, get full assignment and report details
            if location.assignment_id:
                assignment_result = await db.execute(
                    select(Assignment).where(Assignment.id == location.assignment_id)
                )
                assignment = assignment_result.scalar_one_or_none()
                
                if assignment:
                    # Get vehicle info
                    vehicle_result = await db.execute(
                        select(Vehicle).where(Vehicle.id == assignment.vehicle_id)
                    )
                    vehicle = vehicle_result.scalar_one_or_none()
                    
                    if vehicle:
                        location_dict["vehicle_license_plate"] = vehicle.plate_number
                        location_dict["vehicle_name"] = vehicle.name
                    
                    # Get report info
                    report_result = await db.execute(
                        select(Report).where(Report.id == assignment.report_id)
                    )
                    report = report_result.scalar_one_or_none()
                    
                    if report:
                        # If report is done or canceled, mark driver as idle (not on duty)
                        if report.status in ["done", "canceled"]:
                            # Clear assignment_id to show as Idle instead of On Duty
                            location_dict["assignment_id"] = None
                            # Don't include completed assignment details
                        else:
                            # Only add report details for active assignments
                            location_dict["report"] = {
                                "id": report.id,
                                "requester_name": report.requester_name,
                                "requester_phone": report.requester_phone,
                                "transport_type": report.transport_type,
                                "use_stretcher": report.use_stretcher,
                                "pickup_address": report.pickup_address,
                                "destination_address": report.destination_address,
                                "notes": report.note,
                                "status": report.status
                            }
            
            driver_locations.append(location_dict)
        else:
            # Driver has NO location data yet - create placeholder entry
            from datetime import datetime
            location_dict = {
                "id": f"no-location-{driver.id}",
                "driver_id": driver.id,
                "driver_name": driver.name,
                "latitude": DEFAULT_LATITUDE,
                "longitude": DEFAULT_LONGITUDE,
                "timestamp": datetime.now().isoformat(),
                "assignment_id": None,
                "has_location": False,  # Flag to indicate no real location
                "status": "no_location"
            }
            driver_locations.append(location_dict)
    
    return success_response(
        message="Data lokasi semua driver berhasil diambil",
        data=driver_locations
    )

