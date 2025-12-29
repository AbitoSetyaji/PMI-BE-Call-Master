from db.session import Base

# Import all models here for Alembic to detect them
from models.user import User
from models.vehicle_type import VehicleType
from models.vehicle import Vehicle
from models.report import Report
from models.assignment import Assignment
from models.driver_location import DriverLocation

__all__ = ["Base", "User", "VehicleType", "Vehicle", "Report", "Assignment", "DriverLocation"]
