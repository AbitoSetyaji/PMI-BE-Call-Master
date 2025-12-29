from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Boolean, Date, Time
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
import uuid


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Requester Information
    requester_name = Column(String(255), nullable=False)
    requester_phone = Column(String(20), nullable=False)
    
    # Transport Type
    transport_type = Column(CHAR(36), ForeignKey("vehicle_types.id"), nullable=False)
    use_stretcher = Column(Boolean, nullable=False, default=False)
    
    # Patient Information
    patient_name = Column(String(255), nullable=False)
    patient_gender = Column(String(20), nullable=False)  # male, female
    patient_age = Column(Integer, nullable=False)
    patient_history = Column(Text, nullable=True)
    
    # Pickup & Destination
    pickup_address = Column(Text, nullable=False)
    destination_address = Column(Text, nullable=False)
    schedule_date = Column(Date, nullable=False)
    schedule_time = Column(Time, nullable=False)
    
    # Contact Person
    contact_person_name = Column(String(255), nullable=False)
    contact_person_phone = Column(String(20), nullable=False)
    
    # Additional Info
    note = Column(Text, nullable=True)
    attachment_ktp = Column(String(500), nullable=True)
    attachment_house_photo = Column(String(500), nullable=True)
    attachment_sharelok = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="pending")  
    # pending, assigned, on_way, arrived_pickup, arrived_destination, done, canceled
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    transport_type_rel = relationship("VehicleType", back_populates="reports")
    assignments = relationship("Assignment", back_populates="report")
