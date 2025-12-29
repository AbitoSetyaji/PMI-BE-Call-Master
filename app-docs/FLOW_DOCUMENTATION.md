# Flow Documentation - PMI Emergency Call System

## Overview

Dokumen ini menjelaskan alur kerja (flow) dari berbagai fitur dalam PMI Emergency Call System.

---

## Table of Contents

1. [User Registration & Authentication Flow](#user-registration--authentication-flow)
2. [Emergency Report Flow](#emergency-report-flow)
3. [Vehicle Assignment Flow](#vehicle-assignment-flow)
4. [Driver Location Tracking Flow](#driver-location-tracking-flow)
5. [Report Lifecycle Flow](#report-lifecycle-flow)
6. [System Architecture Flow](#system-architecture-flow)

---

## User Registration & Authentication Flow

### Registration Process

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ POST /api/auth/register
       │ {name, email, password, role}
       │
       ▼
┌─────────────────┐
│  Auth Service   │
│                 │
│  1. Validate    │
│  2. Hash pwd    │
│  3. Save to DB  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Database     │
│  users table    │
└────────┬────────┘
         │
         │ Return user data
         ▼
┌─────────────┐
│   Client    │
│ (Success)   │
└─────────────┘
```

### Login Process

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ POST /api/auth/login
       │ {email, password}
       │
       ▼
┌─────────────────────┐
│   Auth Service      │
│                     │
│  1. Find user       │
│  2. Verify password │
│  3. Generate JWT    │
└──────────┬──────────┘
           │
           │ JWT Token + User Info
           ▼
┌─────────────────┐
│     Client      │
│ Store token in  │
│ local storage   │
└─────────────────┘
```

### Authenticated Request Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ GET /api/users/
       │ Authorization: Bearer <token>
       │
       ▼
┌─────────────────────┐
│  Security Module    │
│                     │
│  1. Extract token   │
│  2. Verify JWT      │
│  3. Decode user ID  │
└──────────┬──────────┘
           │
           │ User authenticated
           ▼
┌─────────────────┐
│  Route Handler  │
│  Process req    │
└────────┬────────┘
         │
         ▼
┌─────────────┐
│   Client    │
│  (Response) │
└─────────────┘
```

---

## Emergency Report Flow

### Creating Emergency Report

```
┌──────────────┐
│  Reporter/   │
│  Caller      │
└──────┬───────┘
       │
       │ 1. Call PMI Emergency Line
       │    or use Mobile App
       │
       ▼
┌─────────────────────────┐
│  Operator/System        │
│                         │
│  Collects:              │
│  - Caller info          │
│  - Location (GPS/desc)  │
│  - Emergency details    │
│  - Priority level       │
└──────────┬──────────────┘
           │
           │ POST /api/reports/
           │
           ▼
┌─────────────────────────┐
│   Report Service        │
│                         │
│  1. Validate data       │
│  2. Set status=pending  │
│  3. Save to DB          │
│  4. Notify admins       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│      Database           │
│   reports table         │
│   (status: pending)     │
└─────────────────────────┘
```

### Report Viewing & Management

```
┌──────────────┐
│  Admin/      │
│  Dispatcher  │
└──────┬───────┘
       │
       │ GET /api/reports/
       │ ?status=pending
       │
       ▼
┌─────────────────────────┐
│   Report Service        │
│                         │
│  1. Query reports       │
│  2. Filter by status    │
│  3. Sort by priority    │
└──────────┬──────────────┘
           │
           │ List of pending reports
           ▼
┌─────────────────────────┐
│  Admin Dashboard        │
│                         │
│  Shows:                 │
│  - Priority indicators  │
│  - Location map         │
│  - Time elapsed         │
│  - Available resources  │
└─────────────────────────┘
```

---

## Vehicle Assignment Flow

### Complete Assignment Process

```
┌──────────────┐
│  Dispatcher  │
└──────┬───────┘
       │
       │ 1. Review pending report
       │
       ▼
┌─────────────────────────────┐
│  Check Available Resources  │
│                             │
│  GET /api/vehicles/         │
│  ?status=available          │
│                             │
│  GET /api/users/            │
│  ?role=driver               │
└──────────┬──────────────────┘
           │
           │ 2. Select appropriate resources
           │    - Vehicle type matches need
           │    - Driver available
           │    - Nearest to location
           │
           ▼
┌─────────────────────────────┐
│  Create Assignment          │
│                             │
│  POST /api/assignments/     │
│  {                          │
│    report_id,               │
│    vehicle_id,              │
│    driver_id                │
│  }                          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Assignment Service         │
│                             │
│  1. Create assignment       │
│  2. Update report status    │
│     → "assigned"            │
│  3. Update vehicle status   │
│     → "on_duty"             │
│  4. Notify driver           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Driver Notification        │
│                             │
│  - Assignment details       │
│  - Report location          │
│  - Caller information       │
│  - Priority level           │
└──────────┬──────────────────┘
           │
           │ Driver accepts
           │
           ▼
┌─────────────────────────────┐
│  Driver Mobile App          │
│                             │
│  PUT /api/assignments/{id}  │
│  /status                    │
│  { status: "on_progress" }  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Start Journey              │
│  - Navigation enabled       │
│  - Location tracking active │
│  - ETA calculated           │
└─────────────────────────────┘
```

---

## Driver Location Tracking Flow

### Real-Time Location Updates

```
┌──────────────┐
│  Driver App  │
└──────┬───────┘
       │
       │ Every 30 seconds or on significant movement
       │
       ▼
┌─────────────────────────────┐
│  GPS Service (Mobile)       │
│                             │
│  1. Get current coordinates │
│  2. Check accuracy          │
│  3. Prepare data            │
└──────────┬──────────────────┘
           │
           │ POST /api/driver-locations/
           │ {
           │   driver_id,
           │   latitude,
           │   longitude,
           │   timestamp
           │ }
           │
           ▼
┌─────────────────────────────┐
│  Location Service           │
│                             │
│  1. Validate coordinates    │
│  2. Update/insert record    │
│  3. Calculate ETA           │
│  4. Broadcast to monitors   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Database                   │
│  driver_locations table     │
│  (Latest position)          │
└──────────┬──────────────────┘
           │
           │ Real-time updates via WebSocket
           ▼
┌─────────────────────────────┐
│  Dispatcher Dashboard       │
│                             │
│  Shows:                     │
│  - Driver positions on map  │
│  - Movement history         │
│  - ETA to destination       │
└─────────────────────────────┘
```

---

## Report Lifecycle Flow

### Complete Report Status Flow

```
┌─────────────┐
│   PENDING   │ ← Initial state when report created
└──────┬──────┘
       │
       │ Dispatcher assigns vehicle + driver
       │
       ▼
┌─────────────┐
│  ASSIGNED   │ ← Assignment created
└──────┬──────┘
       │
       │ Driver accepts and starts journey
       │
       ▼
┌─────────────┐
│ ON_PROGRESS │ ← Driver en route / on scene
└──────┬──────┘
       │
       │ Emergency handled, patient transported/treated
       │
       ▼
┌─────────────┐
│  COMPLETED  │ ← Final successful state
└─────────────┘

       OR

┌─────────────┐
│   PENDING   │
└──────┬──────┘
       │
       │ False alarm / duplicate / not needed
       │
       ▼
┌─────────────┐
│  CANCELLED  │ ← Cancelled before completion
└─────────────┘
```

### Status Update Process

```
┌──────────────┐
│  User/System │
└──────┬───────┘
       │
       │ PUT /api/reports/{id}/status
       │ { status: "on_progress" }
       │
       ▼
┌─────────────────────────────┐
│  Report Service             │
│                             │
│  1. Validate status change  │
│  2. Check permissions       │
│  3. Update database         │
│  4. Log status change       │
│  5. Trigger notifications   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Side Effects               │
│                             │
│  - Update assignment status │
│  - Notify stakeholders      │
│  - Update vehicle status    │
│  - Record timestamp         │
└─────────────────────────────┘
```

---

## System Architecture Flow

### Request Processing Flow

```
┌─────────────┐
│   Client    │
│ (Web/Mobile)│
└──────┬──────┘
       │
       │ HTTP/HTTPS Request
       │
       ▼
┌─────────────────────────────┐
│  FastAPI Application        │
│                             │
│  ┌─────────────────────┐   │
│  │ CORS Middleware     │   │
│  └──────────┬──────────┘   │
│             │               │
│             ▼               │
│  ┌─────────────────────┐   │
│  │ Authentication      │   │
│  │ (JWT Verification)  │   │
│  └──────────┬──────────┘   │
│             │               │
│             ▼               │
│  ┌─────────────────────┐   │
│  │ Route Handler       │   │
│  │ (/api/*)           │   │
│  └──────────┬──────────┘   │
│             │               │
│             ▼               │
│  ┌─────────────────────┐   │
│  │ Service Layer       │   │
│  │ (Business Logic)    │   │
│  └──────────┬──────────┘   │
│             │               │
│             ▼               │
│  ┌─────────────────────┐   │
│  │ Database Session    │   │
│  │ (SQLAlchemy)        │   │
│  └──────────┬──────────┘   │
└─────────────┼───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  MySQL Database             │
│                             │
│  - users                    │
│  - vehicles                 │
│  - vehicle_types            │
│  - reports                  │
│  - assignments              │
│  - driver_locations         │
│  - driver_logs              │
└──────────┬──────────────────┘
           │
           │ Results
           ▼
┌─────────────────────────────┐
│  Response Formatter         │
│  (utils/response.py)        │
│                             │
│  Standardized JSON:         │
│  {                          │
│    success: true/false,     │
│    message: "...",          │
│    data: {...}              │
│  }                          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────┐
│   Client    │
│  (Response) │
└─────────────┘
```

### Database Connection Lifecycle

```
┌──────────────┐
│ App Startup  │
└──────┬───────┘
       │
       │ Lifespan event
       │
       ▼
┌─────────────────────────────┐
│  init_db()                  │
│                             │
│  1. Create engine           │
│  2. Create session maker    │
│  3. Test connection         │
└──────────┬──────────────────┘
           │
           │ App running
           │
           ▼
┌─────────────────────────────┐
│  Per-Request Flow           │
│                             │
│  1. Get DB dependency       │
│  2. Create session          │
│  3. Execute queries         │
│  4. Commit/Rollback         │
│  5. Close session           │
└──────────┬──────────────────┘
           │
           │ App shutdown
           │
           ▼
┌─────────────────────────────┐
│  close_db()                 │
│                             │
│  1. Close all sessions      │
│  2. Dispose engine          │
└─────────────────────────────┘
```

---

## Error Handling Flow

### Error Processing

```
┌─────────────┐
│  Exception  │
│  Occurred   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Exception Type?            │
└──────┬─────────┬────────────┘
       │         │
       │         └─────┐
       │               │
       ▼               ▼
┌─────────────┐  ┌─────────────┐
│ HTTPException│  │ Other Error │
└──────┬──────┘  └──────┬──────┘
       │                │
       │                │ Log error
       │                │ 500 status
       │                │
       ▼                ▼
┌─────────────────────────────┐
│  Format Error Response      │
│                             │
│  {                          │
│    success: false,          │
│    message: "Error",        │
│    error: "Details"         │
│  }                          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

---

**Last Updated**: November 3, 2025
