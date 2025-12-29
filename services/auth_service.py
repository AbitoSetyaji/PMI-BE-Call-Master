from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserLogin, UserCreate
from core.security import verify_password, create_access_token, get_password_hash
from utils.response import success_response, error_response


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate user by email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain password
        
    Returns:
        User object if authenticated, None otherwise
    """
    print(f"🔍 DEBUG: Attempting login for email: {email}")
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        print(f"❌ DEBUG: User with email '{email}' NOT FOUND in database")
        return None
    
    print(f"✅ DEBUG: User found - ID: {user.id}, Name: {user.name}, Role: {user.role}")
    print(f"🔐 DEBUG: Stored password hash (first 20 chars): {user.password[:20] if user.password else 'EMPTY'}...")
    print(f"🔐 DEBUG: Password hash length: {len(user.password) if user.password else 0}")
    
    is_valid = verify_password(password, user.password)
    print(f"🔐 DEBUG: Password verification result: {is_valid}")
    
    if not is_valid:
        print(f"❌ DEBUG: Password verification FAILED for user {email}")
        return None
    
    print(f"✅ DEBUG: Authentication SUCCESSFUL for user {email}")
    return user


async def login(db: AsyncSession, credentials: UserLogin) -> dict:
    """
    Login user and generate JWT token
    
    Args:
        db: Database session
        credentials: Login credentials
        
    Returns:
        Dict with access_token, token_type, and user info
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = await authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user data
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }
    )
    
    return success_response(
        message="Login berhasil",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }
    )


async def register(db: AsyncSession, user_data: UserCreate) -> dict:
    """
    Register a new user
    
    Args:
        db: Database session
        user_data: User registration data
        
    Returns:
        Dict with access_token, token_type, and user info
        
    Raises:
        HTTPException: If email already exists
    """
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
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": new_user.email,
            "user_id": new_user.id,
            "role": new_user.role
        }
    )
    
    return success_response(
        message="Registrasi berhasil",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }
        }
    )


async def refresh_token(current_user: User) -> dict:
    """
    Refresh access token for authenticated user
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        Dict with new access_token and user info
    """
    # Create new access token with same user data
    access_token = create_access_token(
        data={
            "sub": current_user.email,
            "user_id": current_user.id,
            "role": current_user.role
        }
    )
    
    return success_response(
        message="Token berhasil diperbarui",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email,
                "role": current_user.role
            }
        }
    )
