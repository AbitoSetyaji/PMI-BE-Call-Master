from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DriverVehicleLogBase(BaseModel):
    """Base DriverVehicleLog schema with shared attributes"""
    driver_id: str
    vehicle_id: str
    report_id: str


class DriverVehicleLogCreate(DriverVehicleLogBase):
    """Schema for creating a new driver vehicle log"""
    start_location: Optional[str] = None


class DriverVehicleLogUpdate(BaseModel):
    """Schema for updating a driver vehicle log"""
    end_time: Optional[datetime] = None
    end_location: Optional[str] = None


class DriverVehicleLogResponse(DriverVehicleLogBase):
    """Schema for driver vehicle log response"""
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class DriverVehicleLogComplete(BaseModel):
    """Schema for completing a driver vehicle log"""
    end_location: str = Field(..., min_length=1)
