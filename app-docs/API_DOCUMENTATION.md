# API Documentation - PMI Emergency Call System

## Overview

Sistem Tanggap Darurat Palang Merah Indonesia (PMI Emergency Call System) adalah sistem backend untuk mengelola laporan darurat, kendaraan, pengemudi, dan penugasan.

**Base URL**: `http://localhost:8000`  
**Version**: 1.0.0

---

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Vehicle Types](#vehicle-types)
4. [Vehicles](#vehicles)
5. [Reports](#reports)
6. [Assignments](#assignments)
7. [Driver Locations](#driver-locations)
8. [Response Format](#response-format)

---

## Authentication

### Register User

**POST** `/api/auth/register`

Register a new user to the system.

**Request Body:**

```json
{
  "name": "string",
  "email": "user@example.com",
  "password": "string",
  "role": "admin | driver | reporter"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "email": "user@example.com",
    "role": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Login

**POST** `/api/auth/login`

Login to get access token.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "uuid",
      "name": "string",
      "email": "user@example.com",
      "role": "string"
    }
  }
}
```

---

### Get Current User

**GET** `/api/auth/me`

Get currently authenticated user information.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "email": "user@example.com",
    "role": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

## Users

### Get All Users

**GET** `/api/users/`

Retrieve all users with optional pagination.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 100)

**Response (200):**

```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "name": "string",
      "email": "user@example.com",
      "role": "string",
      "created_at": "2025-11-03T10:00:00"
    }
  ],
  "meta": {
    "skip": 0,
    "limit": 100,
    "total": 1
  }
}
```

---

### Get User by ID

**GET** `/api/users/{user_id}`

Retrieve a specific user by ID.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "email": "user@example.com",
    "role": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Create User

**POST** `/api/users/`

Create a new user (Admin only).

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "name": "string",
  "email": "user@example.com",
  "password": "string",
  "role": "admin | driver | reporter"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "email": "user@example.com",
    "role": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Update User

**PUT** `/api/users/{user_id}`

Update an existing user.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "name": "string (optional)",
  "email": "user@example.com (optional)",
  "password": "string (optional)",
  "role": "string (optional)"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "email": "user@example.com",
    "role": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Delete User

**DELETE** `/api/users/{user_id}`

Delete a user (Admin only).

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## Vehicle Types

### Get All Vehicle Types

**GET** `/api/vehicle-types/`

Retrieve all vehicle types.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Query Parameters:**

- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 100)

**Response (200):**

```json
{
  "success": true,
  "message": "Vehicle types retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "name": "Ambulance",
      "description": "Emergency medical vehicle",
      "created_at": "2025-11-03T10:00:00"
    }
  ],
  "meta": {
    "skip": 0,
    "limit": 100,
    "total": 1
  }
}
```

---

### Get Vehicle Type by ID

**GET** `/api/vehicle-types/{vehicle_type_id}`

**Response (200):**

```json
{
  "success": true,
  "message": "Vehicle type retrieved successfully",
  "data": {
    "id": "uuid",
    "name": "Ambulance",
    "description": "Emergency medical vehicle",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Create Vehicle Type

**POST** `/api/vehicle-types/`

**Request Body:**

```json
{
  "name": "string",
  "description": "string (optional)"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "Vehicle type created successfully",
  "data": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Update Vehicle Type

**PUT** `/api/vehicle-types/{vehicle_type_id}`

**Request Body:**

```json
{
  "name": "string (optional)",
  "description": "string (optional)"
}
```

---

### Delete Vehicle Type

**DELETE** `/api/vehicle-types/{vehicle_type_id}`

**Response (200):**

```json
{
  "success": true,
  "message": "Vehicle type deleted successfully"
}
```

---

## Vehicles

### Get All Vehicles

**GET** `/api/vehicles/`

Retrieve all vehicles with optional filtering.

**Query Parameters:**

- `skip` (optional): Number of records to skip
- `limit` (optional): Number of records to return
- `status` (optional): Filter by status (available, on_duty, maintenance)

**Response (200):**

```json
{
  "success": true,
  "message": "Vehicles retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "license_plate": "B 1234 XYZ",
      "type_id": "uuid",
      "type_name": "Ambulance",
      "status": "available",
      "created_at": "2025-11-03T10:00:00"
    }
  ]
}
```

---

### Get Vehicle by ID

**GET** `/api/vehicles/{vehicle_id}`

---

### Create Vehicle

**POST** `/api/vehicles/`

**Request Body:**

```json
{
  "license_plate": "B 1234 XYZ",
  "type_id": "uuid",
  "status": "available | on_duty | maintenance"
}
```

---

### Update Vehicle

**PUT** `/api/vehicles/{vehicle_id}`

**Request Body:**

```json
{
  "license_plate": "string (optional)",
  "type_id": "uuid (optional)",
  "status": "string (optional)"
}
```

---

### Delete Vehicle

**DELETE** `/api/vehicles/{vehicle_id}`

---

## Reports

### Get All Reports

**GET** `/api/reports/`

Retrieve all emergency reports.

**Query Parameters:**

- `skip` (optional): Pagination offset
- `limit` (optional): Number of records
- `status` (optional): Filter by status (pending, assigned, on_progress, completed, cancelled)

**Response (200):**

```json
{
  "success": true,
  "message": "Reports retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "caller_name": "John Doe",
      "caller_phone": "+628123456789",
      "location": "Jl. Sudirman No. 123",
      "latitude": -6.2,
      "longitude": 106.816666,
      "description": "Emergency description",
      "status": "pending",
      "priority": "high",
      "created_at": "2025-11-03T10:00:00"
    }
  ]
}
```

---

### Get Report by ID

**GET** `/api/reports/{report_id}`

---

### Create Report

**POST** `/api/reports/`

**Request Body:**

```json
{
  "caller_name": "string",
  "caller_phone": "string",
  "location": "string",
  "latitude": 0.0,
  "longitude": 0.0,
  "description": "string",
  "priority": "low | medium | high | critical"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "Report created successfully",
  "data": {
    "id": "uuid",
    "caller_name": "John Doe",
    "status": "pending",
    "created_at": "2025-11-03T10:00:00"
  }
}
```

---

### Update Report Status

**PUT** `/api/reports/{report_id}/status`

**Request Body:**

```json
{
  "status": "pending | assigned | on_progress | completed | cancelled"
}
```

---

### Update Report

**PUT** `/api/reports/{report_id}`

**Request Body:**

```json
{
  "caller_name": "string (optional)",
  "caller_phone": "string (optional)",
  "location": "string (optional)",
  "latitude": 0.0 (optional),
  "longitude": 0.0 (optional),
  "description": "string (optional)",
  "priority": "string (optional)",
  "status": "string (optional)"
}
```

---

## Assignments

### Get All Assignments

**GET** `/api/assignments/`

Retrieve all vehicle-driver assignments.

**Query Parameters:**

- `skip`, `limit`: Pagination
- `status`: Filter by status

**Response (200):**

```json
{
  "success": true,
  "message": "Assignments retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "report_id": "uuid",
      "vehicle_id": "uuid",
      "driver_id": "uuid",
      "status": "assigned",
      "assigned_at": "2025-11-03T10:00:00",
      "completed_at": null
    }
  ]
}
```

---

### Create Assignment

**POST** `/api/assignments/`

**Request Body:**

```json
{
  "report_id": "uuid",
  "vehicle_id": "uuid",
  "driver_id": "uuid"
}
```

---

### Update Assignment Status

**PUT** `/api/assignments/{assignment_id}/status`

**Request Body:**

```json
{
  "status": "assigned | on_progress | completed | cancelled"
}
```

---

## Driver Locations

### Get All Driver Locations

**GET** `/api/driver-locations/`

Track current driver locations in real-time.

**Response (200):**

```json
{
  "success": true,
  "message": "Driver locations retrieved successfully",
  "data": [
    {
      "id": "uuid",
      "driver_id": "uuid",
      "latitude": -6.2,
      "longitude": 106.816666,
      "timestamp": "2025-11-03T10:00:00"
    }
  ]
}
```

---

### Update Driver Location

**POST** `/api/driver-locations/`

**Request Body:**

```json
{
  "driver_id": "uuid",
  "latitude": -6.2,
  "longitude": 106.816666
}
```

---

## Response Format

### Success Response

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "meta": { ... }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

### Common Status Codes

- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production.

## CORS

CORS is currently set to allow all origins (`*`). Configure appropriately for production.

## Security

- All endpoints except `/`, `/health`, and `/api/auth/*` require authentication
- Use JWT Bearer token in Authorization header
- Tokens expire after 30 minutes (configurable)

---

**Last Updated**: November 3, 2025
