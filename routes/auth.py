from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from core.dependencies import get_current_user
from schemas.user import UserLogin, UserCreate
from services import auth_service
from models.user import User

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login user and generate JWT token
    
    Args:
        credentials: Login credentials (email and password)
        db: Database session
        
    Returns:
        Access token and user information
    """
    return await auth_service.login(db, credentials)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    
    Args:
        user_data: User registration data (name, email, password, role)
        db: Database session
        
    Returns:
        Access token and user information
    """
    return await auth_service.register(db, user_data)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout endpoint (stateless JWT - client should discard token)
    
    Returns:
        Success message
    """
    return {"message": "Logout berhasil. Silakan hapus token dari client."}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh access token - generates a new token with extended expiry
    Use this endpoint before the current token expires to maintain session
    
    Args:
        current_user: Current authenticated user (from valid token)
        
    Returns:
        New access token with extended expiry
    """
    return await auth_service.refresh_token(current_user)

