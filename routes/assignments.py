from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from services import assignment_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_assignments(
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all assignments (admin only)
    
    Args:
        page: Page number (default: 1)
        size: Items per page (default: 10)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of assignments
    """
    return await assignment_service.get_all_assignments(db, current_user, page, size)


@router.get("/driver/{driver_id}", status_code=status.HTTP_200_OK)
async def get_assignments_by_driver(
    driver_id: str,
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get assignments by driver ID
    
    Args:
        driver_id: Driver ID
        page: Page number (default: 1)
        size: Items per page (default: 10)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of assignments
    """
    return await assignment_service.get_assignments_by_driver(db, driver_id, current_user, page, size)


@router.get("/{assignment_id}", status_code=status.HTTP_200_OK)
async def get_assignment(
    assignment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get assignment by ID
    
    Args:
        assignment_id: Assignment ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Assignment details
    """
    return await assignment_service.get_assignment_by_id(db, assignment_id, current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new assignment (admin only)
    - Assigns driver and vehicle to report
    - Updates report status to 'assigned'
    - Updates vehicle status to 'in_use'
    
    Args:
        assignment_data: Assignment creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created assignment
    """
    return await assignment_service.create_assignment(db, assignment_data, current_user)


@router.put("/{assignment_id}", status_code=status.HTTP_200_OK)
async def update_assignment(
    assignment_id: str,
    assignment_data: AssignmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update assignment (admin only)
    
    Args:
        assignment_id: Assignment ID
        assignment_data: Update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated assignment
    """
    return await assignment_service.update_assignment(db, assignment_id, assignment_data, current_user)


@router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
async def delete_assignment(
    assignment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete assignment (admin only)
    - Sets vehicle back to 'available'
    - Sets report back to 'pending'
    
    Args:
        assignment_id: Assignment ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return await assignment_service.delete_assignment(db, assignment_id, current_user)
