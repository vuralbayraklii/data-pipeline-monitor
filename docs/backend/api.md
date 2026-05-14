# Backend API Documentation

## Overview

The backend is built with **FastAPI** and provides RESTful endpoints for dataset management.

### Base URL
```
http://localhost:8000
```

### Health Check
```
GET /health
```

Returns service health status.

---

## Dataset Endpoints

All dataset endpoints are prefixed with `/api/datasets`

### 1. Create Dataset

**Request:**
```http
POST /api/datasets
Content-Type: application/json

{
  "name": "sales_data",
  "source": "s3://bucket/sales",
  "description": "Monthly sales data"
}
```

**Response (201 Created):**
```json
{
  "id": "ds_0001",
  "name": "sales_data",
  "source": "s3://bucket/sales",
  "description": "Monthly sales data",
  "status": "active"
}
```

**Errors:**
- `422 Unprocessable Entity` - Validation error

---

### 2. List Datasets

**Request:**
```http
GET /api/datasets
```

**Response (200 OK):**
```json
[
  {
    "id": "ds_0001",
    "name": "sales_data",
    "source": "s3://bucket/sales",
    "description": "Monthly sales data",
    "status": "active"
  }
]
```

---

### 3. Get Single Dataset

**Request:**
```http
GET /api/datasets/{dataset_id}
```

**Response (200 OK):**
```json
{
  "id": "ds_0001",
  "name": "sales_data",
  "source": "s3://bucket/sales",
  "description": "Monthly sales data",
  "status": "active"
}
```

**Errors:**
- `404 Not Found` - Dataset doesn't exist

---

## Data Models

### Dataset

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (auto-generated) |
| `name` | string | Dataset name (required, max 255 chars) |
| `source` | string | Data source location (required) |
| `description` | string | Optional description |
| `status` | enum | One of: `active`, `archived`, `processing` |

---

## Development Notes

- Current implementation uses in-memory storage
- Database integration planned for Phase 2
- All endpoints return JSON
- CORS enabled for frontend (localhost:3000, localhost:5173)

---

**Last Updated:** May 2026
