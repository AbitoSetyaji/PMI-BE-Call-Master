"""
Reset database - Drop and recreate pmi_db
Use this when you need a clean database
"""

import pymysql
from sqlalchemy.engine.url import make_url
from core.config import settings

def reset_database():
    """Drop and recreate database"""
    try:
        # Parse DATABASE_URL
        db_url = make_url(settings.DATABASE_URL.replace("aiomysql", "pymysql"))
        
        # Connect without database selection
        connection = pymysql.connect(
            host=db_url.host,
            user=db_url.username,
            password=db_url.password,
            port=db_url.port or 3306
        )
        
        cursor = connection.cursor()
        
        # Drop database
        print("🗑️  Dropping database pmi_db...")
        cursor.execute("DROP DATABASE IF EXISTS pmi_db")
        
        # Create database
        print("🔨 Creating database pmi_db...")
        cursor.execute("CREATE DATABASE pmi_db")
        
        print("✅ Database reset successfully!")
        print("📝 Next steps:")
        print("   1. Run: alembic upgrade head")
        print("   2. Run: python init_transport_system.py")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")

if __name__ == "__main__":
    confirm = input("⚠️  This will DELETE ALL DATA in pmi_db. Continue? (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
    else:
        print("Cancelled.")
