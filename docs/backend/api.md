# Backend API Documentation

## Overview

The backend is built with **FastAPI** and provides RESTful endpoints for dataset management.

### Base URL
```
http://localhost:8000
```

### API Version
- Version: 0.1.0
- Status: Learning Project

---

## Health Checks

### Root Endpoint
```http
GET /
```

Returns service status and version information.

**Response (200 OK):**
```json
{
  "message": "Data Pipeline Monitor API",
  "version": "0.1.0",
  "status": "running"
}
```

### Health Check
```http
GET /health
```

Returns service health status (for monitoring/load balancers).

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "data-pipeline-monitor-api"
}
```

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
- `422 Unprocessable Entity` - Validation error (missing/invalid fields)

---

### 2. List All Datasets

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
  },
  {
    "id": "ds_0002",
    "name": "customer_data",
    "source": "s3://bucket/customers",
    "description": "",
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

### 4. Update Dataset

**Request:**
```http
PUT /api/datasets/{dataset_id}
Content-Type: application/json

{
  "name": "updated_sales_data",
  "source": "s3://bucket/sales/updated",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": "ds_0001",
  "name": "updated_sales_data",
  "source": "s3://bucket/sales/updated",
  "description": "Updated description",
  "status": "active"
}
```

**Errors:**
- `404 Not Found` - Dataset doesn't exist
- `422 Unprocessable Entity` - Validation error

---

### 5. Delete Dataset

**Request:**
```http
DELETE /api/datasets/{dataset_id}
```

**Response:**
- `204 No Content` (success, no response body)

**Errors:**
- `404 Not Found` - Dataset doesn't exist

---

## Data Models

### DatasetCreate

Schema for creating or updating datasets.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | Yes | 1-255 characters |
| `source` | string | Yes | Min 1 character, typically S3 path |
| `description` | string | No | Max 1000 characters, default="" |

### Dataset

Complete dataset schema with metadata.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | string | - | Auto-generated identifier (ds_XXXX) |
| `name` | string | - | Dataset name |
| `source` | string | - | Data source location |
| `description` | string | "" | Optional description |
| `status` | enum | "active" | One of: `active`, `archived`, `processing` |

---

## CORS Configuration

CORS is enabled for local development:
- Allowed Origins: `http://localhost:3000`, `http://localhost:5173`
- Allowed Methods: All
- Allowed Headers: All
- Credentials: Allowed

---

## Error Responses

All errors return JSON with appropriate HTTP status codes:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Malformed request
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Server error

---

## Testing

Run tests with:
```bash
cd apps/backend
pytest tests/ -v
```

Current test coverage: **28+ test cases**
- CRUD operations
- Error handling
- Validation
- Edge cases

---

## Local Development

### Start Backend Server

```bash
cd apps/backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Start development server (auto-reloads)
uvicorn app.main:app --reload

# Server will be at http://localhost:8000
```

### Interactive API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Related Documentation

- [Backend Setup](setup.md) - Installation and configuration
- [Data Models](models.md) - Detailed model documentation
- [Development Workflow](../DEVELOPMENT_WORKFLOW.md) - How to contribute
- [AI Agent Guide](../AI_AGENT_GUIDE.md) - Instructions for agents

---

**Last Updated:** May 14, 2026  
**Status:** Phase 2 - Dataset Registry Module (Complete)
