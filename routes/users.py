from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from services import user_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(
    page: int = 1,
    size: int = 10,
    role: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users (admin only)
    
    Args:
        page: Page number (default: 1)
        size: Items per page (default: 10)
        role: Filter by role (optional)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of all users
    """
    return await user_service.get_all_users(db, current_user, page, size, role)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return await user_service.get_user_by_id(db, user_id, current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new user (admin only)
    
    Args:
        user_data: User creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created user
    """
    return await user_service.create_user(db, user_data, current_user)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user information
    
    Args:
        user_id: User ID to update
        user_data: Update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated user
    """
    return await user_service.update_user(db, user_id, user_data, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete user (admin only)
    
    Args:
        user_id: User ID to delete
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return await user_service.delete_user(db, user_id, current_user)
