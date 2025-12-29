from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base User schema with shared attributes"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: str = Field(..., pattern="^(admin|driver|reporter)$")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(admin|driver|reporter)$")


class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
