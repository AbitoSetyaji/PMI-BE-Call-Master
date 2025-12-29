from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, time


class ReportBase(BaseModel):
    """Base Report schema with shared attributes"""
    # Requester Information
    requester_name: str = Field(..., min_length=1, max_length=255)
    requester_phone: str = Field(..., min_length=1, max_length=20)
    
    # Transport Type
    transport_type: str = Field(..., description="Vehicle type ID (UUID)")
    use_stretcher: bool = Field(default=False)
    
    # Patient Information
    patient_name: str = Field(..., min_length=1, max_length=255)
    patient_gender: str = Field(..., pattern="^(male|female)$")
    patient_age: int = Field(..., ge=0, le=150)
    patient_history: Optional[str] = None
    
    # Pickup & Destination
    pickup_address: str = Field(..., min_length=1)
    destination_address: str = Field(..., min_length=1)
    schedule_date: date
    schedule_time: time
    
    # Contact Person
    contact_person_name: str = Field(..., min_length=1, max_length=255)
    contact_person_phone: str = Field(..., min_length=1, max_length=20)
    
    # Additional Info
    note: Optional[str] = None
    attachment_ktp: Optional[str] = None
    attachment_house_photo: Optional[str] = None
    attachment_sharelok: Optional[str] = None


class ReportCreate(ReportBase):
    """Schema for creating a new report"""
    pass


class ReportUpdate(BaseModel):
    """Schema for updating a report"""
    requester_name: Optional[str] = Field(None, min_length=1, max_length=255)
    requester_phone: Optional[str] = Field(None, min_length=1, max_length=20)
    transport_type: Optional[str] = None
    use_stretcher: Optional[bool] = None
    patient_name: Optional[str] = Field(None, min_length=1, max_length=255)
    patient_gender: Optional[str] = Field(None, pattern="^(male|female)$")
    patient_age: Optional[int] = Field(None, ge=0, le=150)
    patient_history: Optional[str] = None
    pickup_address: Optional[str] = None
    destination_address: Optional[str] = None
    schedule_date: Optional[date] = None
    schedule_time: Optional[time] = None
    contact_person_name: Optional[str] = None
    contact_person_phone: Optional[str] = None
    note: Optional[str] = None
    attachment_ktp: Optional[str] = None
    attachment_house_photo: Optional[str] = None
    attachment_sharelok: Optional[str] = None
    status: Optional[str] = Field(
        None, 
        pattern="^(pending|assigned|on_way|arrived_pickup|arrived_destination|done|canceled)$"
    )


class ReportResponse(ReportBase):
    """Schema for report response"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class ReportStatusUpdate(BaseModel):
    """Schema for updating report status"""
    status: str = Field(
        ..., 
        pattern="^(pending|assigned|on_way|arrived_pickup|arrived_destination|done|canceled)$"
    )
class ReportStatusUpdate(BaseModel):
    """Schema for updating report status"""
    status: str = Field(
        ..., 
        pattern="^(pending|assigned|on_way|arrived_pickup|arrived_destination|done|canceled)$"
    )
