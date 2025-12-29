"""
PMI Transport System - Complete Database Initialization Script

This script will:
1. Create default vehicle types (patient_transport, mortuary_transport)
2. Create sample vehicles for each type
3. Create admin, driver, and reporter users
4. Display all credentials

Run this ONCE after database migration:
  python init_transport_system.py
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import AsyncSessionLocal
from db.base import Base
import uuid


async def create_vehicle_types():
    """Create default vehicle types"""
    # Import here to avoid circular dependencies
    from models.vehicle_type import VehicleType
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as db:
        try:
            print("[*] Creating vehicle types...")
            
            # Check if vehicle types already exist
            result = await db.execute(select(VehicleType))
            existing = result.scalars().all()
            
            if len(existing) > 0:
                print("[!] Vehicle types already exist, skipping...")
                # Return existing IDs
                patient = next((vt for vt in existing if vt.name == "patient_transport"), None)
                mortuary = next((vt for vt in existing if vt.name == "mortuary_transport"), None)
                if patient and mortuary:
                    return patient.id, mortuary.id
            
            # Patient Transport
            patient_transport = VehicleType(
                id=str(uuid.uuid4()),
                name="patient_transport"
            )
            
            # Mortuary Transport
            mortuary_transport = VehicleType(
                id=str(uuid.uuid4()),
                name="mortuary_transport"
            )
            
            db.add(patient_transport)
            db.add(mortuary_transport)
            
            await db.commit()
            await db.refresh(patient_transport)
            await db.refresh(mortuary_transport)
            
            print("[OK] Vehicle types created successfully!")
            print(f"  - {patient_transport.name} (ID: {patient_transport.id})")
            print(f"  - {mortuary_transport.name} (ID: {mortuary_transport.id})")
            
            return patient_transport.id, mortuary_transport.id
            
        except Exception as e:
            print(f"[ERROR] Creating vehicle types: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()
            sys.exit(1)


async def create_sample_vehicles(patient_type_id: str, mortuary_type_id: str):
    """Create sample vehicles for both transport types"""
    from models.vehicle import Vehicle
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as db:
        try:
            print("\n[*] Creating sample vehicles...")
            
            # Check if vehicles exist
            result = await db.execute(select(Vehicle))
            existing = result.scalars().all()
            
            if len(existing) > 0:
                print("[!] Vehicles already exist, skipping...")
                return
            
            vehicles = [
                # Patient transport vehicles
                Vehicle(
                    id=str(uuid.uuid4()),
                    name="Ambulans Pasien PMI 01",
                    plate_number="B 1111 PMI",
                    type=patient_type_id,
                    status="available"
                ),
                Vehicle(
                    id=str(uuid.uuid4()),
                    name="Ambulans Pasien PMI 02",
                    plate_number="B 1112 PMI",
                    type=patient_type_id,
                    status="available"
                ),
                # Mortuary transport vehicles
                Vehicle(
                    id=str(uuid.uuid4()),
                    name="Ambulans Jenazah PMI 01",
                    plate_number="B 2221 PMI",
                    type=mortuary_type_id,
                    status="available"
                ),
                Vehicle(
                    id=str(uuid.uuid4()),
                    name="Ambulans Jenazah PMI 02",
                    plate_number="B 2222 PMI",
                    type=mortuary_type_id,
                    status="available"
                )
            ]
            
            for vehicle in vehicles:
                db.add(vehicle)
            
            await db.commit()
            
            print("[OK] Sample vehicles created successfully!")
            for vehicle in vehicles:
                print(f"  - {vehicle.name} ({vehicle.plate_number})")
            
        except Exception as e:
            print(f"[ERROR] Creating sample vehicles: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()


async def create_users():
    """Create admin, drivers, and reporter users"""
    from models.user import User
    from core.security import get_password_hash
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as db:
        try:
            print("\n[*] Creating users...")
            
            users_to_create = [
                {
                    "name": "Admin PMI",
                    "email": "admin@pmi.id",
                    "password": "admin123",
                    "role": "admin"
                },
                {
                    "name": "Driver PMI 01",
                    "email": "driver1@pmi.id",
                    "password": "driver123",
                    "role": "driver"
                },
                {
                    "name": "Driver PMI 02",
                    "email": "driver2@pmi.id",
                    "password": "driver123",
                    "role": "driver"
                },
                {
                    "name": "Reporter Test",
                    "email": "reporter@pmi.id",
                    "password": "reporter123",
                    "role": "reporter"
                }
            ]
            
            created_users = []
            
            for user_data in users_to_create:
                # Check if user already exists
                result = await db.execute(
                    select(User).where(User.email == user_data["email"])
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    user = User(
                        id=str(uuid.uuid4()),
                        name=user_data["name"],
                        email=user_data["email"],
                        password=get_password_hash(user_data["password"]),
                        role=user_data["role"]
                    )
                    db.add(user)
                    created_users.append(user_data)
                    print(f"  [OK] {user_data['role'].capitalize()}: {user_data['name']}")
                else:
                    print(f"  [!] {user_data['role'].capitalize()}: {user_data['email']} already exists")
            
            await db.commit()
            
            if created_users:
                print("\n[INFO] Login Credentials:")
                for user in created_users:
                    print(f"  {user['role'].capitalize():8} - {user['email']:20} / {user['password']}")
            
        except Exception as e:
            print(f"[ERROR] Creating users: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()


async def main():
    """Main initialization function"""
    print("=" * 75)
    print(" " * 15 + "PMI Transport System - Database Initialization")
    print("=" * 75)
    
    # Step 1: Create vehicle types
    print("\n[STEP 1/3] Setting up vehicle types...")
    result = await create_vehicle_types()
    
    # Step 2: Create sample vehicles
    if result:
        patient_id, mortuary_id = result
        print("\n[STEP 2/3] Setting up sample vehicles...")
        await create_sample_vehicles(patient_id, mortuary_id)
    else:
        print("\n[!] Skipping vehicle creation - vehicle types not created")
    
    # Step 3: Create users
    print("\n[STEP 3/3] Setting up user accounts...")
    await create_users()
    
    # Summary
    print("\n" + "=" * 75)
    print(" " * 25 + "[SUCCESS] Setup Complete!")
    print("=" * 75)
    print("\n[NEXT STEPS]")
    print("  1. Start server    : fastapi dev main.py")
    print("  2. API Docs        : http://localhost:8000/docs")
    print("  3. Login as Admin  : admin@pmi.id / admin123")
    print("  4. Login as Driver : driver1@pmi.id / driver123")
    print("\n[IMPORTANT]")
    print("  - Change default passwords after first login!")
    print("  - Vehicle Types: patient_transport, mortuary_transport")
    print("  - Sample vehicles created for testing")
    print("=" * 75)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Setup cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
