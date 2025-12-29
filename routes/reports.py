from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.report import ReportCreate, ReportUpdate, ReportResponse, ReportStatusUpdate
from services import new_report_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_reports(
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all reports
    
    Args:
        page: Page number (default: 1)
        size: Items per page (default: 10)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of reports
    """
    return await new_report_service.get_all_reports(db, current_user, page, size)


@router.get("/{report_id}", status_code=status.HTTP_200_OK)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get report by ID
    
    Args:
        report_id: Report ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Report details
    """
    return await new_report_service.get_report_by_id(db, report_id, current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new report
    
    Args:
        report_data: Report creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created report
    """
    return await new_report_service.create_report(db, report_data, current_user)


@router.put("/{report_id}", status_code=status.HTTP_200_OK)
async def update_report(
    report_id: str,
    report_data: ReportUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update report (admin only)
    
    Args:
        report_id: Report ID
        report_data: Update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated report
    """
    return await new_report_service.update_report(db, report_id, report_data, current_user)


@router.put("/{report_id}/status", status_code=status.HTTP_200_OK)
async def update_report_status(
    report_id: str,
    status_data: ReportStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update report status
    
    Args:
        report_id: Report ID
        status_data: Status update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated report
    """
    return await new_report_service.update_report_status(db, report_id, status_data, current_user)


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
async def delete_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete report (admin only)
    
    Args:
        report_id: Report ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return await new_report_service.delete_report(db, report_id, current_user)
