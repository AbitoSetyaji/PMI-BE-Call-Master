from schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin
)
from schemas.vehicle_type import (
    VehicleTypeBase,
    VehicleTypeCreate,
    VehicleTypeUpdate,
    VehicleTypeResponse
)
from schemas.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse
)
from schemas.report import (
    ReportBase,
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    ReportStatusUpdate
)
from schemas.assignment import (
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse
)
from schemas.driver_location import (
    DriverLocationBase,
    DriverLocationCreate,
    DriverLocationUpdate,
    DriverLocationResponse,
    DriverLocationQuery
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    # Vehicle Type schemas
    "VehicleTypeBase",
    "VehicleTypeCreate",
    "VehicleTypeUpdate",
    "VehicleTypeResponse",
    # Vehicle schemas
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
    # Report schemas
    "ReportBase",
    "ReportCreate",
    "ReportUpdate",
    "ReportResponse",
    "ReportStatusUpdate",
    # Assignment schemas
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    # Driver location schemas
    "DriverLocationBase",
    "DriverLocationCreate",
    "DriverLocationUpdate",
    "DriverLocationResponse",
    "DriverLocationQuery"
]
