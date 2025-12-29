from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
import uuid


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    plate_number = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(CHAR(36), ForeignKey("vehicle_types.id"), nullable=False)
    status = Column(String(50), nullable=False, default="available")  # available, in_use, maintenance
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    vehicle_type = relationship("VehicleType", back_populates="vehicles")
    assignments = relationship("Assignment", back_populates="vehicle")
