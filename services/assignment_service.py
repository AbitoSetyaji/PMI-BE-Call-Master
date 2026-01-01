from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from models.assignment import Assignment
from models.report import Report
from models.vehicle import Vehicle
from models.user import User
from schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from utils.response import success_response, paginated_response
import uuid


async def get_all_assignments(db: AsyncSession, current_user: User, page: int = 1, size: int = 10) -> dict:
    """
    Get all assignments with pagination (admin and reporter)
    
    Args:
        db: Database session
        current_user: Current authenticated user
        page: Page number (default: 1)
        size: Items per page (default: 10)
        
    Returns:
        Paginated list of assignments
        
    Raises:
        HTTPException: If not admin or reporter
    """
    if current_user.role not in ["admin", "reporter"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin dan reporter yang dapat melihat semua penugasan"
        )
    
    # Get total count
    total_result = await db.execute(select(func.count()).select_from(Assignment))
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.report).selectinload(Report.transport_type_rel),
            selectinload(Assignment.vehicle)
        )
        .offset((page - 1) * size)
        .limit(size)
    )
    assignments = result.scalars().all()
    
    assignments_list = []
    for a in assignments:
        assignment_dict = AssignmentResponse.model_validate(a).model_dump()
        
        # Get driver name manually
        driver_result = await db.execute(select(User).where(User.id == a.driver_id))
        driver = driver_result.scalar_one_or_none()
        assignment_dict["driver_name"] = driver.name if driver else None
        assignment_dict["vehicle_plate"] = a.vehicle.plate_number if a.vehicle else None
        
        # Add report data for formatted Report ID
        if a.report:
            transport_type_name = None
            if a.report.transport_type_rel:
                transport_type_name = a.report.transport_type_rel.name
            assignment_dict["report"] = {
                "transport_type_name": transport_type_name,
                "schedule_date": str(a.report.schedule_date) if a.report.schedule_date else None,
                "schedule_time": str(a.report.schedule_time) if a.report.schedule_time else None,
                "requester_name": a.report.requester_name,
                "requester_phone": a.report.requester_phone,
            }
        else:
            assignment_dict["report"] = None
            
        assignments_list.append(assignment_dict)
    
    return paginated_response(
        message="Data penugasan berhasil diambil",
        items=assignments_list,
        total=total,
        page=page,
        size=size
    )


async def get_assignment_by_id(db: AsyncSession, assignment_id: str, current_user: User) -> dict:
    """
    Get assignment by ID
    
    Args:
        db: Database session
        assignment_id: Assignment ID
        current_user: Current authenticated user
        
    Returns:
        Assignment data
        
    Raises:
        HTTPException: If assignment not found
    """
    result = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.report),
            selectinload(Assignment.vehicle)
        )
        .where(Assignment.id == assignment_id)
    )
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penugasan tidak ditemukan"
        )
    
    # Check permissions (driver can only see their own assignments)
    if current_user.role == "driver" and assignment.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke penugasan ini"
        )
    
    assignment_dict = AssignmentResponse.model_validate(assignment).model_dump()
    
    # Get driver name manually
    driver_result = await db.execute(select(User).where(User.id == assignment.driver_id))
    driver = driver_result.scalar_one_or_none()
    assignment_dict["driver_name"] = driver.name if driver else None
    assignment_dict["vehicle_plate"] = assignment.vehicle.plate_number if assignment.vehicle else None
    
    return success_response(
        message="Data penugasan berhasil diambil",
        data=assignment_dict
    )


async def get_assignments_by_driver(
    db: AsyncSession,
    driver_id: str,
    current_user: User,
    page: int = 1,
    size: int = 10
) -> dict:
    """
    Get assignments by driver ID with pagination
    
    Args:
        db: Database session
        driver_id: Driver ID
        current_user: Current authenticated user
        page: Page number (default: 1)
        size: Items per page (default: 10)
        
    Returns:
        Paginated list of assignments
        
    Raises:
        HTTPException: If no permission
    """
    # Driver can only see their own assignments
    if current_user.role == "driver" and current_user.id != driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda hanya dapat melihat penugasan sendiri"
        )
    
    # Get total count
    total_result = await db.execute(
        select(func.count()).select_from(Assignment).where(Assignment.driver_id == driver_id)
    )
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.report),
            selectinload(Assignment.vehicle)
        )
        .where(Assignment.driver_id == driver_id)
        .offset((page - 1) * size)
        .limit(size)
    )
    assignments = result.scalars().all()
    
    assignments_list = []
    for a in assignments:
        assignment_dict = AssignmentResponse.model_validate(a).model_dump()
        
        # Get driver name manually
        driver_result = await db.execute(select(User).where(User.id == a.driver_id))
        driver = driver_result.scalar_one_or_none()
        assignment_dict["driver_name"] = driver.name if driver else None
        assignment_dict["vehicle_plate"] = a.vehicle.plate_number if a.vehicle else None
        assignments_list.append(assignment_dict)
    
    return paginated_response(
        message="Data penugasan driver berhasil diambil",
        items=assignments_list,
        total=total,
        page=page,
        size=size
    )


async def create_assignment(
    db: AsyncSession,
    assignment_data: AssignmentCreate,
    current_user: User
) -> dict:
    """
    Create new assignment (admin and reporter)
    
    Args:
        db: Database session
        assignment_data: Assignment creation data
        current_user: Current authenticated user
        
    Returns:
        Created assignment data
        
    Raises:
        HTTPException: If not admin/reporter or validation fails
    """
    if current_user.role not in ["admin", "reporter"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin dan reporter yang dapat membuat penugasan"
        )
    
    # Verify report exists
    result = await db.execute(select(Report).where(Report.id == assignment_data.report_id))
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    # Verify driver exists
    result = await db.execute(select(User).where(User.id == assignment_data.driver_id))
    driver = result.scalar_one_or_none()
    
    if not driver or driver.role != "driver":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver tidak ditemukan"
        )
    
    # Create assignment with status 'assigned'
    new_assignment = Assignment(
        id=str(uuid.uuid4()),
        report_id=assignment_data.report_id,
        driver_id=assignment_data.driver_id,
        status="assigned"  # Set initial status to assigned
    )
    
    # Update report status to assigned
    report.status = "assigned"
    
    db.add(new_assignment)
    await db.commit()
    await db.refresh(new_assignment)
    
    # Load relationships
    result = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.report),
            selectinload(Assignment.vehicle)
        )
        .where(Assignment.id == new_assignment.id)
    )
    new_assignment = result.scalar_one()
    
    assignment_dict = AssignmentResponse.model_validate(new_assignment).model_dump()
    
    # Get driver name manually
    driver_result = await db.execute(select(User).where(User.id == new_assignment.driver_id))
    driver = driver_result.scalar_one_or_none()
    assignment_dict["driver_name"] = driver.name if driver else None
    assignment_dict["vehicle_plate"] = new_assignment.vehicle.plate_number if new_assignment.vehicle else None
    
    return success_response(
        message="Penugasan berhasil dibuat",
        data=assignment_dict
    )


async def update_assignment(
    db: AsyncSession,
    assignment_id: str,
    assignment_data: AssignmentUpdate,
    current_user: User
) -> dict:
    """
    Update assignment
    - Admin can update any assignment
    - Driver can only update vehicle selection for their own assignment
    
    Args:
        db: Database session
        assignment_id: Assignment ID
        assignment_data: Update data
        current_user: Current authenticated user
        
    Returns:
        Updated assignment data
        
    Raises:
        HTTPException: If not authorized or assignment not found
    """
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penugasan tidak ditemukan"
        )
    
    # Check permissions
    is_admin = current_user.role == "admin"
    is_own_assignment = current_user.role == "driver" and assignment.driver_id == current_user.id
    
    if not is_admin and not is_own_assignment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin atau driver yang ditugaskan dapat mengubah penugasan ini"
        )
    
    # Update vehicle if changed
    if assignment_data.vehicle_id and assignment_data.vehicle_id != assignment.vehicle_id:
        # Set old vehicle to available
        result = await db.execute(select(Vehicle).where(Vehicle.id == assignment.vehicle_id))
        old_vehicle = result.scalar_one_or_none()
        if old_vehicle:
            old_vehicle.status = "available"
        
        # Verify new vehicle exists and available
        result = await db.execute(select(Vehicle).where(Vehicle.id == assignment_data.vehicle_id))
        new_vehicle = result.scalar_one_or_none()
        
        if not new_vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kendaraan baru tidak ditemukan"
            )
        
        if new_vehicle.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Kendaraan sedang {new_vehicle.status}"
            )
        
        new_vehicle.status = "in_use"
        assignment.vehicle_id = assignment_data.vehicle_id
    
    # Update driver if changed (admin only)
    if assignment_data.driver_id and is_admin:
        # Verify driver exists
        result = await db.execute(select(User).where(User.id == assignment_data.driver_id))
        driver = result.scalar_one_or_none()
        
        if not driver or driver.role != "driver":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver tidak ditemukan"
            )
        
        assignment.driver_id = assignment_data.driver_id
    
    await db.commit()
    
    # Load relationships
    result = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.report),
            selectinload(Assignment.vehicle)
        )
        .where(Assignment.id == assignment_id)
    )
    assignment = result.scalar_one()
    
    assignment_dict = AssignmentResponse.model_validate(assignment).model_dump()
    
    # Get driver name manually
    driver_result = await db.execute(select(User).where(User.id == assignment.driver_id))
    driver = driver_result.scalar_one_or_none()
    assignment_dict["driver_name"] = driver.name if driver else None
    assignment_dict["vehicle_plate"] = assignment.vehicle.plate_number if assignment.vehicle else None
    
    return success_response(
        message="Penugasan berhasil diupdate",
        data=assignment_dict
    )


async def delete_assignment(
    db: AsyncSession,
    assignment_id: str,
    current_user: User
) -> dict:
    """
    Delete assignment (admin only)
    
    Args:
        db: Database session
        assignment_id: Assignment ID
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not admin or assignment not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menghapus penugasan"
        )
    
    result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penugasan tidak ditemukan"
        )
    
    # Set vehicle back to available
    result = await db.execute(select(Vehicle).where(Vehicle.id == assignment.vehicle_id))
    vehicle = result.scalar_one_or_none()
    if vehicle:
        vehicle.status = "available"
    
    # Set report back to pending
    result = await db.execute(select(Report).where(Report.id == assignment.report_id))
    report = result.scalar_one_or_none()
    if report:
        report.status = "pending"
    
    await db.delete(assignment)
    await db.commit()
    
    return success_response(
        message="Penugasan berhasil dihapus",
        data={"id": assignment_id}
    )
