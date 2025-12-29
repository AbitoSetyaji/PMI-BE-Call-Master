"""
Seed script to create test driver locations
Run this script to create sample driver location data for testing
"""
import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from db.session import AsyncSessionLocal, init_db
from models.user import User
from models.driver_location import DriverLocation


async def seed_driver_locations():
    """Seed sample driver locations into database"""
    
    async with AsyncSessionLocal() as db:
        # Find all drivers
        result = await db.execute(
            select(User).where(User.role == "driver")
        )
        drivers = result.scalars().all()
        
        if not drivers:
            print("❌ No drivers found in database!")
            print("   Please run 'python seed_users.py' first to create driver users.")
            return
        
        print(f"📍 Found {len(drivers)} driver(s)")
        
        # Sample locations around Jakarta
        sample_locations = [
            {"latitude": -6.2088, "longitude": 106.8456, "desc": "Jakarta Pusat"},
            {"latitude": -6.1751, "longitude": 106.8650, "desc": "Jakarta Utara"},
            {"latitude": -6.2297, "longitude": 106.6895, "desc": "Tangerang"},
            {"latitude": -6.2615, "longitude": 106.7809, "desc": "Jakarta Selatan"},
            {"latitude": -6.2384, "longitude": 106.9756, "desc": "Bekasi"},
        ]
        
        for i, driver in enumerate(drivers):
            # Check if driver already has location
            result = await db.execute(
                select(DriverLocation).where(DriverLocation.driver_id == driver.id).limit(1)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"⚠️  Driver {driver.name} already has location data, skipping...")
                continue
            
            # Use different location for each driver
            loc = sample_locations[i % len(sample_locations)]
            
            new_location = DriverLocation(
                id=str(uuid.uuid4()),
                driver_id=driver.id,
                latitude=loc["latitude"],
                longitude=loc["longitude"],
                assignment_id=None  # No active assignment
            )
            
            db.add(new_location)
            await db.commit()
            print(f"✅ Created location for driver: {driver.name}")
            print(f"   📍 {loc['desc']} ({loc['latitude']}, {loc['longitude']})")
    
    print("\n🎉 Driver locations seeding completed!")
    print("\n👉 Refresh the tracking page to see driver locations on the map.")


if __name__ == "__main__":
    print("🌱 Starting driver locations seeding...\n")
    asyncio.run(seed_driver_locations())
