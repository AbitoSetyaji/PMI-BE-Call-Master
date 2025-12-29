from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
import uuid


class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = Column(CHAR(36), ForeignKey("reports.id"), nullable=False)
    vehicle_id = Column(CHAR(36), ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(CHAR(36), nullable=False)  # ID driver (tidak perlu foreign key user)
    
    # Status: active → assigned → on_progress → completed / cancelled
    status = Column(String(20), default="active", nullable=False)
    
    assigned_at = Column(DateTime, server_default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)  # When assignment is completed
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    report = relationship("Report", back_populates="assignments")
    vehicle = relationship("Vehicle", back_populates="assignments")
