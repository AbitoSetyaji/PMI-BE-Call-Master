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
    allow_origins=["*"],  # Configure this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(vehicle_types.router, prefix="/api/vehicle-types", tags=["Vehicle Types"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(driver_locations.router, prefix="/api/driver-locations", tags=["Driver Locations"])


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
