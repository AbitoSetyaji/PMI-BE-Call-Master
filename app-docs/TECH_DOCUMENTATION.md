# Technical Documentation - PMI Emergency Call System

## Overview

Dokumentasi teknis untuk PMI Emergency Call System yang dibangun menggunakan FastAPI, SQLAlchemy, dan MySQL.

---

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Project Structure](#project-structure)
3. [Database Schema](#database-schema)
4. [Core Components](#core-components)
5. [Security Implementation](#security-implementation)
6. [Development Setup](#development-setup)
7. [Deployment Guide](#deployment-guide)
8. [Best Practices](#best-practices)

---

## Technology Stack

### Backend Framework

- **FastAPI 0.120.1**: Modern, fast web framework for building APIs
- **Python 3.x**: Programming language
- **Uvicorn**: ASGI server for running FastAPI

### Database

- **MySQL**: Relational database
- **SQLAlchemy 2.0.25**: SQL toolkit and ORM
- **Alembic 1.13.1**: Database migration tool
- **aiomysql 0.2.0**: Async MySQL driver

### Authentication & Security

- **python-jose 3.3.0**: JWT token handling
- **passlib 1.7.4**: Password hashing
- **bcrypt 5.0.0**: Secure password hashing algorithm

### Validation & Serialization

- **Pydantic 2.5.3**: Data validation using Python type annotations
- **pydantic-settings 2.1.0**: Settings management

### Utilities

- **python-dotenv 1.0.0**: Environment variable management
- **email-validator 2.3.0**: Email validation

---

## Project Structure

```
PMI-Call/
│
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Alembic environment config
│   └── script.py.mako         # Migration template
│
├── app-docs/                   # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── FLOW_DOCUMENTATION.md
│   └── TECH_DOCUMENTATION.md
│
├── core/                       # Core application modules
│   ├── __init__.py
│   ├── config.py              # Application settings
│   ├── dependencies.py        # FastAPI dependencies
│   └── security.py            # Security utilities (JWT, hashing)
│
├── db/                        # Database configuration
│   ├── __init__.py
│   ├── base.py                # Base model imports
│   └── session.py             # Database session management
│
├── models/                    # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── vehicle.py             # Vehicle model
│   ├── vehicle_type.py        # Vehicle type model
│   ├── report.py              # Emergency report model
│   ├── assignment.py          # Assignment model
│   ├── driver_location.py     # Driver location tracking
│   └── driver_log.py          # Driver activity logs
│
├── routes/                    # API route handlers
│   ├── __init__.py
│   ├── auth.py                # Authentication endpoints
│   ├── users.py               # User CRUD endpoints
│   ├── vehicles.py            # Vehicle CRUD endpoints
│   ├── vehicle_types.py       # Vehicle type endpoints
│   ├── new_reports.py         # Report endpoints
│   ├── assignments.py         # Assignment endpoints
│   └── driver_locations.py    # Location tracking endpoints
│
├── schemas/                   # Pydantic schemas
│   ├── __init__.py
│   ├── user.py                # User schemas
│   ├── vehicle.py             # Vehicle schemas
│   ├── vehicle_type.py        # Vehicle type schemas
│   ├── report.py              # Report schemas
│   ├── assignment.py          # Assignment schemas
│   └── driver_location.py     # Location schemas
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py        # Authentication logic
│   ├── user_service.py        # User business logic
│   ├── vehicle_service.py     # Vehicle management
│   ├── vehicle_type_service.py
│   ├── new_report_service.py  # Report handling
│   ├── assignment_service.py  # Assignment logic
│   └── driver_location_service.py
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── response.py            # Standardized response helpers
│
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore
├── alembic.ini                # Alembic configuration
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── init_transport_system.py   # Database initialization script
└── reset_database.py          # Database reset utility
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email (unique)  │
│ password (hash) │
│ role            │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────┐         ┌─────────────────┐
│ driver_locations    │         │  driver_logs    │
├─────────────────────┤         ├─────────────────┤
│ id (PK)             │         │ id (PK)         │
│ driver_id (FK)      │         │ driver_id (FK)  │
│ latitude            │         │ action          │
│ longitude           │         │ details         │
│ timestamp           │         │ timestamp       │
└─────────────────────┘         └─────────────────┘

┌─────────────────┐
│ vehicle_types   │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│   vehicles      │
├─────────────────┤
│ id (PK)         │
│ license_plate   │
│ type_id (FK)    │
│ status          │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│  assignments    │
├─────────────────┤
│ id (PK)         │
│ report_id (FK)  │◄───────┐
│ vehicle_id (FK) │        │
│ driver_id (FK)  │        │
│ status          │        │
│ assigned_at     │        │
│ completed_at    │        │
└─────────────────┘        │
                           │ 1:N
                           │
                  ┌────────┴────────┐
                  │    reports      │
                  ├─────────────────┤
                  │ id (PK)         │
                  │ caller_name     │
                  │ caller_phone    │
                  │ location        │
                  │ latitude        │
                  │ longitude       │
                  │ description     │
                  │ status          │
                  │ priority        │
                  │ created_at      │
                  └─────────────────┘
```

### Table Definitions

#### users

```sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- 'admin', 'driver', 'reporter'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

#### vehicle_types

```sql
CREATE TABLE vehicle_types (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### vehicles

```sql
CREATE TABLE vehicles (
    id CHAR(36) PRIMARY KEY,
    license_plate VARCHAR(20) NOT NULL UNIQUE,
    type_id CHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'available', 'on_duty', 'maintenance'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES vehicle_types(id),
    INDEX idx_license_plate (license_plate),
    INDEX idx_status (status)
);
```

#### reports

```sql
CREATE TABLE reports (
    id CHAR(36) PRIMARY KEY,
    caller_name VARCHAR(255) NOT NULL,
    caller_phone VARCHAR(20) NOT NULL,
    location TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'pending', 'assigned', 'on_progress', 'completed', 'cancelled'
    priority VARCHAR(20) NOT NULL,  -- 'low', 'medium', 'high', 'critical'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
);
```

#### assignments

```sql
CREATE TABLE assignments (
    id CHAR(36) PRIMARY KEY,
    report_id CHAR(36) NOT NULL,
    vehicle_id CHAR(36) NOT NULL,
    driver_id CHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'assigned', 'on_progress', 'completed', 'cancelled'
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (driver_id) REFERENCES users(id),
    INDEX idx_report (report_id),
    INDEX idx_status (status)
);
```

#### driver_locations

```sql
CREATE TABLE driver_locations (
    id CHAR(36) PRIMARY KEY,
    driver_id CHAR(36) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES users(id),
    INDEX idx_driver (driver_id),
    INDEX idx_timestamp (timestamp)
);
```

#### driver_logs

```sql
CREATE TABLE driver_logs (
    id CHAR(36) PRIMARY KEY,
    driver_id CHAR(36) NOT NULL,
    action VARCHAR(255) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES users(id),
    INDEX idx_driver (driver_id),
    INDEX idx_timestamp (timestamp)
);
```

---

## Core Components

### 1. Configuration Management (core/config.py)

```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    APP_NAME: str = "PMI Emergency Call System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
```

Environment variables loaded from `.env` file using pydantic-settings.

### 2. Database Session (db/session.py)

```python
# Async SQLAlchemy setup
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for route handlers
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 3. Security Layer (core/security.py)

**Password Hashing:**

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**JWT Token Management:**

```python
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
```

### 4. Authentication Dependency (core/dependencies.py)

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Verify and decode JWT
    # Fetch user from database
    # Return user object
```

### 5. Standardized Responses (utils/response.py)

```python
def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200
) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(
    message: str,
    error: str = None,
    status_code: int = 400
) -> dict:
    return {
        "success": False,
        "message": message,
        "error": error
    }
```

---

## Security Implementation

### Authentication Flow

1. **User Registration**

   - Password hashed using bcrypt
   - Email validation using email-validator
   - Role-based user creation

2. **Login Process**

   - Email lookup
   - Password verification
   - JWT token generation
   - Token expiration: 30 minutes (configurable)

3. **Protected Endpoints**
   - Token extraction from Authorization header
   - Token validation and decoding
   - User existence verification
   - Request processing

### Authorization

**Role-Based Access Control (RBAC):**

- **Admin**: Full system access
- **Driver**: Own assignments, location updates
- **Reporter**: Create reports, view own reports

### Password Security

- Minimum length enforced via Pydantic validators
- Bcrypt hashing with automatic salt
- Password never stored in plain text
- Password never returned in API responses

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Setup

### Prerequisites

- Python 3.9 or higher
- MySQL 8.0 or higher
- pip package manager

### Installation Steps

1. **Clone Repository**

```bash
git clone <repository-url>
cd PMI-Call
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with your configuration
```

Example `.env`:

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/pmi_call
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=PMI Emergency Call System
APP_VERSION=1.0.0
DEBUG=True
```

5. **Create Database**

```bash
mysql -u root -p
CREATE DATABASE pmi_call CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Run Migrations**

```bash
alembic upgrade head
```

7. **Initialize Data (Optional)**

```bash
python init_transport_system.py
```

8. **Run Development Server**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

**Create New Migration:**

```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply Migrations:**

```bash
alembic upgrade head
```

**Rollback Migration:**

```bash
alembic downgrade -1
```

**View Migration History:**

```bash
alembic history
```

---

## Deployment Guide

### Production Checklist

1. **Environment Configuration**

   - Set `DEBUG=False`
   - Generate strong `JWT_SECRET_KEY`
   - Configure proper CORS origins
   - Set up SSL/TLS certificates

2. **Database**

   - Use connection pooling
   - Configure proper indexes
   - Set up regular backups
   - Enable query logging (temporarily for monitoring)

3. **Application Server**

   - Use Gunicorn with Uvicorn workers

   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Reverse Proxy (Nginx)**

   ```nginx
   server {
       listen 80;
       server_name api.pmi-emergency.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Process Manager (systemd)**

   ```ini
   [Unit]
   Description=PMI Emergency Call System
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/PMI-Call
   ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Security**

   - Enable HTTPS only
   - Implement rate limiting
   - Set up firewall rules
   - Regular security audits

7. **Monitoring**
   - Set up logging (file/cloud)
   - Monitor server resources
   - Track API performance
   - Alert on errors

---

## Best Practices

### Code Organization

1. **Separation of Concerns**

   - Routes: Handle HTTP requests
   - Services: Business logic
   - Models: Database entities
   - Schemas: Data validation

2. **Dependency Injection**

   - Use FastAPI's Depends()
   - Keep dependencies reusable
   - Avoid global state

3. **Error Handling**
   ```python
   try:
       # Operation
   except SpecificException as e:
       raise HTTPException(status_code=400, detail=str(e))
   ```

### Database Operations

1. **Use Async Operations**

   ```python
   async def get_user(db: AsyncSession, user_id: str):
       result = await db.execute(select(User).filter(User.id == user_id))
       return result.scalar_one_or_none()
   ```

2. **Efficient Queries**

   - Use selective loading
   - Avoid N+1 queries
   - Index frequently queried columns

3. **Transaction Management**
   - Let the session context manager handle commits
   - Rollback on exceptions
   - Close sessions properly

### API Design

1. **RESTful Conventions**

   - Use proper HTTP methods
   - Meaningful resource names
   - Consistent URL structure

2. **Response Consistency**

   - Always use standardized response format
   - Include appropriate status codes
   - Provide clear error messages

3. **Validation**
   - Validate all inputs using Pydantic
   - Return clear validation errors
   - Sanitize user inputs

### Testing

1. **Unit Tests**

   - Test service layer functions
   - Mock database calls
   - Test edge cases

2. **Integration Tests**

   - Test API endpoints
   - Use test database
   - Clean up after tests

3. **Test Coverage**
   ```bash
   pytest --cov=. --cov-report=html
   ```

---

## Performance Optimization

### Database

- Use connection pooling
- Optimize complex queries
- Add appropriate indexes
- Use query result caching

### Application

- Implement response caching
- Use async operations
- Minimize external API calls
- Optimize data serialization

### Infrastructure

- Use CDN for static assets
- Enable gzip compression
- Load balancing for scaling
- Database read replicas

---

## Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Check DATABASE_URL format
   - Verify MySQL is running
   - Check network connectivity
   - Verify credentials

2. **JWT Token Issues**

   - Check token expiration
   - Verify JWT_SECRET_KEY
   - Ensure proper header format

3. **Migration Errors**

   - Review migration script
   - Check database state
   - Manual schema verification

4. **Performance Issues**
   - Enable query logging
   - Check for N+1 queries
   - Monitor server resources
   - Review slow query log

---

## API Testing

### Using cURL

**Register User:**

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

**Login:**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Authenticated Request:**

```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer <your-token>"
```

### Using Postman

1. Import collection from documentation
2. Set environment variables
3. Use pre-request scripts for token management

---

## Maintenance

### Regular Tasks

- Database backups (daily)
- Log rotation (weekly)
- Security updates (as needed)
- Dependency updates (monthly)
- Performance monitoring (continuous)

### Database Maintenance

```sql
-- Analyze tables
ANALYZE TABLE users, vehicles, reports, assignments;

-- Optimize tables
OPTIMIZE TABLE driver_locations, driver_logs;

-- Check for unused indexes
SHOW INDEX FROM reports;
```

---

## Resources

### Official Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Alembic](https://alembic.sqlalchemy.org/)

### Tools

- [Postman](https://www.postman.com/) - API Testing
- [DBeaver](https://dbeaver.io/) - Database Management
- [VS Code](https://code.visualstudio.com/) - Code Editor

---

**Last Updated**: November 3, 2025  
**Version**: 1.0.0  
**Maintained by**: Development Team
