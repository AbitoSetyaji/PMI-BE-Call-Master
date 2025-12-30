from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AssignmentBase(BaseModel):
    """Base Assignment schema with shared attributes"""
    report_id: str = Field(..., description="Report ID (UUID)")
    vehicle_id: Optional[str] = Field(None, description="Vehicle ID (UUID)")
    driver_id: str = Field(..., description="Driver ID (UUID)")


class AssignmentCreate(BaseModel):
    report_id: str = Field(None, description="Report ID (UUID)")
    driver_id: Optional[str] = Field(None, description="Driver ID (UUID)")


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment"""
    vehicle_id: Optional[str] = Field(None, description="Vehicle ID (UUID)")
    driver_id: Optional[str] = Field(None, description="Driver ID (UUID)")
    coffin_checklist_confirmed: Optional[bool] = Field(None, description="Coffin/Keranda checklist confirmed")


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response"""
    id: str
    status: str = "active"  # active, assigned, on_progress, completed, cancelled
    assigned_at: datetime
    completed_at: Optional[datetime] = None  # When assignment is completed
    coffin_checklist_confirmed: bool = False  # Coffin/Keranda checklist confirmed
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class AssignmentWithRelationsResponse(AssignmentResponse):
    """Schema for assignment response with related data"""
    driver_name: Optional[str] = None
    vehicle_plate: Optional[str] = None
