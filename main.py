from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from db.session import init_db, close_db

# Import routers
from routes import auth, reports, users, vehicle_types, vehicles, assignments, driver_locations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting PMI Emergency Call System...")
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down PMI Emergency Call System...")
    await close_db()
    print("✅ Database connections closed")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistem Tanggap Darurat Palang Merah Indonesia",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Production domains
        "https://pmikotasmg.site",
        "https://www.pmikotasmg.site",
        "https://api.pmikotasmg.site",
        # Direct IP access (production server)
        "http://148.230.100.61",
        "http://148.230.100.61:3000",
        "http://148.230.100.61:3001",
        # Development
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers with /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(vehicle_types.router, prefix="/api/vehicle-types", tags=["Vehicle Types"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(driver_locations.router, prefix="/api/driver-locations", tags=["Driver Locations"])

# Also include routers without /api prefix for frontend compatibility
app.include_router(auth.router, prefix="/auth", tags=["Authentication (No API Prefix)"])
app.include_router(users.router, prefix="/users", tags=["Users (No API Prefix)"])
app.include_router(vehicle_types.router, prefix="/vehicle-types", tags=["Vehicle Types (No API Prefix)"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles (No API Prefix)"])
app.include_router(reports.router, prefix="/reports", tags=["Reports (No API Prefix)"])
app.include_router(assignments.router, prefix="/assignments", tags=["Assignments (No API Prefix)"])
app.include_router(driver_locations.router, prefix="/driver-locations", tags=["Driver Locations (No API Prefix)"])


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to PMI Emergency Call System API",
        "version": settings.APP_VERSION,
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
