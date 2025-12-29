"""
Seed script to create default users with properly hashed passwords
Run this script to create initial users in the database
"""
import asyncio
from sqlalchemy import select
from db.session import AsyncSessionLocal, init_db
from models.user import User
from core.security import get_password_hash


async def seed_users():
    """Seed default users into database"""
    
    # Default users to create
    default_users = [
        {
            "name": "Admin PMI",
            "email": "admin@pmi.id",
            "password": "admin123",
            "role": "admin"
        },
        {
            "name": "Driver Test",
            "email": "driver@pmi.id", 
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
    
    async with AsyncSessionLocal() as db:
        for user_data in default_users:
            # Check if user already exists
            result = await db.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"⚠️  User {user_data['email']} already exists, skipping...")
                continue
            
            # Create new user with hashed password
            hashed_password = get_password_hash(user_data["password"])
            new_user = User(
                name=user_data["name"],
                email=user_data["email"],
                password=hashed_password,
                role=user_data["role"]
            )
            
            db.add(new_user)
            await db.commit()
            print(f"✅ Created user: {user_data['email']} (password: {user_data['password']})")
    
    print("\n🎉 Seeding completed!")
    print("\nYou can now login with:")
    print("  Email: admin@pmi.id")
    print("  Password: admin123")


if __name__ == "__main__":
    print("🌱 Starting user seeding...\n")
    asyncio.run(seed_users())
