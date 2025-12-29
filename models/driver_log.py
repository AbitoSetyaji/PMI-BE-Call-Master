from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base
import uuid


class DriverVehicleLog(Base):
    __tablename__ = "driver_vehicle_logs"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(CHAR(36), ForeignKey("vehicles.id"), nullable=False)
    report_id = Column(CHAR(36), ForeignKey("reports.id"), nullable=False)
    start_time = Column(DateTime, server_default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    start_location = Column(Text, nullable=True)
    end_location = Column(Text, nullable=True)
    
    # Relationships
    driver = relationship("User", back_populates="driver_logs")
    vehicle = relationship("Vehicle", back_populates="driver_logs")
    report = relationship("Report", back_populates="driver_logs")
