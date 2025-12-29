from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
import uuid


class DriverLocation(Base):
    __tablename__ = "driver_locations"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    assignment_id = Column(CHAR(36), ForeignKey("assignments.id"), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    driver = relationship("User", back_populates="driver_locations")
    assignment = relationship("Assignment", backref="driver_locations")

