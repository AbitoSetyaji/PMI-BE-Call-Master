from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VehicleTypeBase(BaseModel):
    """Base VehicleType schema with shared attributes"""
    name: str = Field(..., min_length=1, max_length=100, description="Nama jenis kendaraan")

class VehicleTypeCreate(VehicleTypeBase):
    """Schema for creating a new vehicle type"""
    pass


class VehicleTypeUpdate(BaseModel):
    """Schema for updating vehicle type"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class VehicleTypeResponse(VehicleTypeBase):
    """Schema for vehicle type response"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2
