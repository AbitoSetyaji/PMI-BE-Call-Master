from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from models.report import Report
from models.vehicle_type import VehicleType
from models.user import User
from schemas.report import ReportCreate, ReportUpdate, ReportStatusUpdate, ReportResponse
from utils.response import success_response, paginated_response
import uuid


async def get_all_reports(db: AsyncSession, current_user: User, page: int = 1, size: int = 10) -> dict:
    """
    Get all reports with pagination (admin can see all, others see their own)
    
    Args:
        db: Database session
        current_user: Current authenticated user
        page: Page number (default: 1)
        size: Items per page (default: 10)
        
    Returns:
        Paginated list of reports
    """
    # Build query
    if current_user.role == "admin":
        # Admin can see all reports
        query = select(Report).options(selectinload(Report.transport_type_rel))
        count_query = select(func.count()).select_from(Report)
    else:
        # Others see all reports (can be filtered on frontend)
        query = select(Report).options(selectinload(Report.transport_type_rel))
        count_query = select(func.count()).select_from(Report)
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(
        query
        .offset((page - 1) * size)
        .limit(size)
    )
    reports = result.scalars().all()
    
    reports_list = []
    for r in reports:
        report_dict = ReportResponse.model_validate(r).model_dump()
        report_dict["transport_type_name"] = r.transport_type_rel.name if r.transport_type_rel else None
        reports_list.append(report_dict)
    
    return paginated_response(
        message="Data laporan berhasil diambil",
        items=reports_list,
        total=total,
        page=page,
        size=size
    )


async def get_report_by_id(db: AsyncSession, report_id: str, current_user: User) -> dict:
    """
    Get report by ID
    
    Args:
        db: Database session
        report_id: Report ID
        current_user: Current authenticated user
        
    Returns:
        Report data
        
    Raises:
        HTTPException: If report not found
    """
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.transport_type_rel))
        .where(Report.id == report_id)
    )
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laporan tidak ditemukan"
        )
    
    report_dict = ReportResponse.model_validate(report).model_dump()
    report_dict["transport_type_name"] = report.transport_type_rel.name if report.transport_type_rel else None
    
    return success_response(
        message="Data laporan berhasil diambil",
        data=report_dict
    )


async def create_report(db: AsyncSession, report_data: ReportCreate, current_user: User) -> dict:
    """
    Create new report
    
    Args:
        db: Database session
        report_data: Report creation data
        current_user: Current authenticated user
        
    Returns:
        Created report data
        
    Raises:
        HTTPException: If transport_type doesn't exist
    """
    # Verify transport type exists
    result = await db.execute(select(VehicleType).where(VehicleType.id == report_data.transport_type))
    transport_type = result.scalar_one_or_none()
    
    if not transport_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis transportasi tidak ditemukan"
        )
    
    # Create new report
    new_report = Report(
        id=str(uuid.uuid4()),
        requester_name=report_data.requester_name,
        requester_phone=report_data.requester_phone,
        transport_type=report_data.transport_type,
        use_stretcher=report_data.use_stretcher,
        patient_name=report_data.patient_name,
        patient_gender=report_data.patient_gender,
        patient_age=report_data.patient_age,
        patient_history=report_data.patient_history,
        pickup_address=report_data.pickup_address,
        destination_address=report_data.destination_address,
        schedule_date=report_data.schedule_date,
        schedule_time=report_data.schedule_time,
        contact_person_name=report_data.contact_person_name,
        contact_person_phone=report_data.contact_person_phone,
        note=report_data.note,
        attachment_ktp=report_data.attachment_ktp,
        attachment_house_photo=report_data.attachment_house_photo,
        attachment_sharelok=report_data.attachment_sharelok,
        status="pending"
    )
    
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    
    return success_response(
        message="Laporan berhasil ditambahkan",
        data=ReportResponse.model_validate(new_report).model_dump()
    )


async def update_report(
    db: AsyncSession,
    report_id: str,
    report_data: ReportUpdate,
    current_user: User
) -> dict:
    """
    Update report information (admin only)
    
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
    if current_user.role != "admin":
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
    if report_data.requester_name is not None:
        report.requester_name = report_data.requester_name
    if report_data.requester_phone is not None:
        report.requester_phone = report_data.requester_phone
    if report_data.transport_type is not None:
        # Verify transport type exists
        result = await db.execute(select(VehicleType).where(VehicleType.id == report_data.transport_type))
        transport_type = result.scalar_one_or_none()
        if not transport_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jenis transportasi tidak ditemukan"
            )
        report.transport_type = report_data.transport_type
    if report_data.use_stretcher is not None:
        report.use_stretcher = report_data.use_stretcher
    if report_data.patient_name is not None:
        report.patient_name = report_data.patient_name
    if report_data.patient_gender is not None:
        report.patient_gender = report_data.patient_gender
    if report_data.patient_age is not None:
        report.patient_age = report_data.patient_age
    if report_data.patient_history is not None:
        report.patient_history = report_data.patient_history
    if report_data.pickup_address is not None:
        report.pickup_address = report_data.pickup_address
    if report_data.destination_address is not None:
        report.destination_address = report_data.destination_address
    if report_data.schedule_date is not None:
        report.schedule_date = report_data.schedule_date
    if report_data.schedule_time is not None:
        report.schedule_time = report_data.schedule_time
    if report_data.contact_person_name is not None:
        report.contact_person_name = report_data.contact_person_name
    if report_data.contact_person_phone is not None:
        report.contact_person_phone = report_data.contact_person_phone
    if report_data.note is not None:
        report.note = report_data.note
    if report_data.attachment_ktp is not None:
        report.attachment_ktp = report_data.attachment_ktp
    if report_data.attachment_house_photo is not None:
        report.attachment_house_photo = report_data.attachment_house_photo
    if report_data.attachment_sharelok is not None:
        report.attachment_sharelok = report_data.attachment_sharelok
    if report_data.status is not None:
        report.status = report_data.status
    
    await db.commit()
    await db.refresh(report)
    
    return success_response(
        message="Laporan berhasil diupdate",
        data=ReportResponse.model_validate(report).model_dump()
    )


async def update_report_status(
    db: AsyncSession,
    report_id: str,
    status_data: ReportStatusUpdate,
    current_user: User
) -> dict:
    """
    Update report status
    
    Args:
        db: Database session
        report_id: Report ID
        status_data: Status update data
        current_user: Current authenticated user
        
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
    
    # Validate status transition
    valid_statuses = ["pending", "assigned", "on_way", "arrived_pickup", "arrived_destination", "done", "canceled"]
    
    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status tidak valid"
        )
    
    # Update report status
    report.status = status_data.status
    
    # If status is "done", update vehicle status to available and assignment to completed
    if status_data.status == "done":
        from models.assignment import Assignment
        from models.vehicle import Vehicle
        from datetime import datetime
        
        # Find active assignment
        result = await db.execute(
            select(Assignment).where(Assignment.report_id == report_id)
        )
        assignment = result.scalar_one_or_none()
        
        if assignment:
            # Update assignment status to completed
            assignment.status = "completed"
            assignment.completed_at = datetime.utcnow()
            
            # Update vehicle status
            if assignment.vehicle_id:
                result = await db.execute(
                    select(Vehicle).where(Vehicle.id == assignment.vehicle_id)
                )
                vehicle = result.scalar_one_or_none()
                if vehicle:
                    vehicle.status = "available"
    
    # If status is "on_way", update assignment status to on_progress
    elif status_data.status == "on_way":
        from models.assignment import Assignment
        
        result = await db.execute(
            select(Assignment).where(Assignment.report_id == report_id)
        )
        assignment = result.scalar_one_or_none()
        
        if assignment:
            assignment.status = "on_progress"
    
    # If status is "assigned", keep assignment status as assigned
    elif status_data.status == "assigned":
        from models.assignment import Assignment
        
        result = await db.execute(
            select(Assignment).where(Assignment.report_id == report_id)
        )
        assignment = result.scalar_one_or_none()
        
        if assignment:
            assignment.status = "assigned"
    
    await db.commit()
    await db.refresh(report)
    
    return success_response(
        message="Status laporan berhasil diupdate",
        data=ReportResponse.model_validate(report).model_dump()
    )


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
    
    return success_response(
        message="Laporan berhasil dihapus",
        data={"id": report_id}
    )
