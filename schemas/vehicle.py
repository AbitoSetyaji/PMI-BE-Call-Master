from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VehicleBase(BaseModel):
    """Base Vehicle schema with shared attributes"""
    name: str = Field(..., min_length=1, max_length=255)
    plate_number: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., description="Vehicle type ID (UUID)")


class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle"""
    status: Optional[str] = Field(default="available", pattern="^(available|in_use|maintenance)$")


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    plate_number: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = Field(None, description="Vehicle type ID (UUID)")
    status: Optional[str] = Field(None, pattern="^(available|in_use|maintenance)$")


class VehicleResponse(VehicleBase):
    """Schema for vehicle response"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class VehicleWithTypeResponse(VehicleResponse):
    """Schema for vehicle response with vehicle type details"""
    vehicle_type_name: Optional[str] = None
    vehicle_type_description: Optional[str] = None
