from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DriverLocationBase(BaseModel):
    """Base DriverLocation schema with shared attributes"""
    driver_id: str
    latitude: Decimal = Field(..., ge=-90, le=90, decimal_places=8)
    longitude: Decimal = Field(..., ge=-180, le=180, decimal_places=8)
    assignment_id: Optional[str] = None


class DriverLocationCreate(DriverLocationBase):
    """Schema for creating a new driver location"""
    pass


class DriverLocationUpdate(BaseModel):
    """Schema for updating driver location"""
    latitude: Decimal = Field(..., ge=-90, le=90, decimal_places=8)
    longitude: Decimal = Field(..., ge=-180, le=180, decimal_places=8)


class DriverLocationResponse(DriverLocationBase):
    """Schema for driver location response"""
    id: str
    timestamp: datetime
    assignment_id: Optional[str] = None
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class DriverLocationWithDriverResponse(DriverLocationResponse):
    """Schema for driver location with driver name"""
    driver_name: Optional[str] = None


class DriverLocationQuery(BaseModel):
    """Schema for querying driver locations"""
    driver_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
