from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from core.security import get_password_hash
from utils.response import success_response, paginated_response
import uuid


async def get_all_users(
    db: AsyncSession,
    current_user: User,
    page: int = 1,
    size: int = 10,
    role: str = None
) -> dict:
    """
    Get all users with pagination (admin only)
    
    Args:
        db: Database session
        current_user: Current authenticated user
        page: Page number (default: 1)
        size: Items per page (default: 10)
        role: Filter by role (optional)
        
    Returns:
        Paginated list of users
        
    Raises:
        HTTPException: If user is not admin or reporter
    """
    if current_user.role not in ["admin", "reporter"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin dan reporter yang dapat melihat semua user"
        )
    
    # Build base query with optional role filter
    base_query = select(User)
    if role and role in ["admin", "driver", "reporter"]:
        base_query = base_query.where(User.role == role)
    
    # Get total count
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated data
    offset = (page - 1) * size
    query = base_query.offset(offset).limit(size)
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Convert to schema
    users_data = [UserResponse.model_validate(user).model_dump() for user in users]
    
    return paginated_response(
        message="Data users berhasil diambil",
        items=users_data,
        total=total,
        page=page,
        size=size
    )

async def get_user_by_id(db: AsyncSession, user_id: str, current_user: User) -> dict:
    """
    Get user by ID
    
    Args:
        db: Database session
        user_id: User ID
        current_user: Current authenticated user
        
    Returns:
        User data
        
    Raises:
        HTTPException: If user not found or no permission
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    
    # Users can only see their own data unless they're admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses ke data user ini"
        )
    
    return success_response(
        message="Data user berhasil diambil",
        data=UserResponse.model_validate(user).model_dump()
    )

async def create_user(db: AsyncSession, user_data: UserCreate, current_user: User) -> dict:
    """
    Create new user (admin only)
    
    Args:
        db: Database session
        user_data: User creation data
        current_user: Current authenticated user
        
    Returns:
        Created user data
        
    Raises:
        HTTPException: If not admin or email already exists
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menambah user"
        )
    
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        id=str(uuid.uuid4()),
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return success_response(
        message="User berhasil ditambahkan",
        data=UserResponse.model_validate(new_user).model_dump()
    )


async def update_user(
    db: AsyncSession, 
    user_id: str, 
    user_data: UserUpdate, 
    current_user: User
) -> dict:
    """
    Update user information
    
    Args:
        db: Database session
        user_id: User ID to update
        user_data: Update data
        current_user: Current authenticated user
        
    Returns:
        Updated user data
        
    Raises:
        HTTPException: If user not found or no permission
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    
    # Only admin or the user themselves can update
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses untuk mengubah user ini"
        )
    
    # Only admin can change role
    if user_data.role and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat mengubah role"
        )
    
    # Update fields
    if user_data.name:
        user.name = user_data.name
    if user_data.email:
        # Check if new email already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email, User.id != user_id)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah digunakan oleh user lain"
            )
        user.email = user_data.email
    if user_data.role:
        user.role = user_data.role
    
    await db.commit()
    await db.refresh(user)
    
    return success_response(
        message="User berhasil diupdate",
        data=UserResponse.model_validate(user).model_dump()
    )



async def delete_user(db: AsyncSession, user_id: str, current_user: User) -> dict:
    """
    Delete user (admin only)
    
    Args:
        db: Database session
        user_id: User ID to delete
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not admin or user not found
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya admin yang dapat menghapus user"
        )
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    
    await db.delete(user)
    await db.commit()
    
    return success_response(
        message="User berhasil dihapus",
        data={"id": user_id}
    )
