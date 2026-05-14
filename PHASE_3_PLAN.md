## Phase 3: Service Simulation & Advanced Features

**Status:** 🚀 Starting

**Date Started:** May 14, 2026

**Phase Objective:** Add service simulation features (pipeline runs, object storage metadata, branch references) and implement advanced filtering, pagination, and data enrichment.

---

## Overview

Phase 3 extends the Dataset Registry with simulated backend services:
- **Object Storage Simulation** - Fake MinIO bucket metadata
- **Data Catalog Simulation** - Fake Nessie/Iceberg branch references
- **Pipeline Simulation** - Fake Airflow pipeline run tracking
- **Advanced Queries** - Filtering, sorting, pagination
- **Data Enrichment** - Enhanced dataset information with source tracking

---

## Key Features to Implement

### 1. Extended Dataset Model
**Files:** `apps/backend/app/models/dataset.py`

Add fields to represent integrated services:
- `object_storage_path` - MinIO s3:// path with bucket/key structure
- `catalog_branch` - Nessie branch reference (e.g., "main", "feature-xyz")
- `table_format` - Iceberg/Delta/Parquet format specification
- `last_run_id` - Reference to last pipeline execution
- `row_count` - Estimated rows (from preview)
- `size_bytes` - Dataset size in bytes
- `updated_at` - Last update timestamp

### 2. Pipeline Runs Module
**Files:**
- `apps/backend/app/models/pipeline_run.py` - PipelineRun model
- `apps/backend/app/api/routes/pipeline_runs.py` - Pipeline endpoints

Features:
- Create pipeline run records
- Track run status (pending, running, success, failed)
- Link runs to datasets
- List runs by dataset
- Get run details with logs

### 3. Object Storage Simulation
**Files:**
- `apps/backend/app/models/object_storage.py` - ObjectStorageFile model
- `apps/backend/app/api/routes/object_storage.py` - Storage endpoints

Features:
- List objects in simulated bucket
- Get object metadata
- Simulate S3 paths with versioning
- Track object sizes and timestamps

### 4. Advanced Dataset Queries
**Files:** `apps/backend/app/api/routes/datasets.py` (extend)

Features:
- Filter by status, catalog branch, format
- Pagination (limit/offset)
- Sort by name, size, updated_at
- Search by name/description
- Aggregations (total size, count by status)

### 5. Frontend Enhancements
**Files:**
- `apps/frontend/src/pages/DatasetsPage.vue` (extend)
- `apps/frontend/src/components/DatasetFilters.vue` (new)
- `apps/frontend/src/components/DatasetDetails.vue` (new)
- `apps/frontend/src/services/pipelineRuns.ts` (new)

Features:
- Filter panel with status/format/branch selections
- Pagination controls
- Dataset detail modal showing all fields
- Pipeline run history view
- Object storage explorer

### 6. Testing
**Files:**
- `tests/test_pipeline_runs.py` (new)
- `tests/test_object_storage.py` (new)
- `tests/test_dataset_queries.py` (new)
- `tests/test_advanced_features.py` (new)

Target: 40+ new test cases

### 7. Documentation
**Files:**
- `docs/backend/pipeline-runs.md` (new)
- `docs/backend/object-storage.md` (new)
- `docs/architecture/data-flow.md` (new)
- `docs/features/filtering-pagination.md` (new)

---

## Implementation Plan

### Week 1: Core Models & APIs
- [ ] Task 1: Extended Dataset model with new fields
- [ ] Task 2: PipelineRun model and endpoints
- [ ] Task 3: ObjectStorageFile model and endpoints
- [ ] Task 4: Database schema planning (for Phase 4)

### Week 2: Advanced Queries
- [ ] Task 5: Filter/sort/search implementation
- [ ] Task 6: Pagination support
- [ ] Task 7: Aggregation endpoints
- [ ] Task 8: Query optimization

### Week 3: Frontend Integration
- [ ] Task 9: Filter component
- [ ] Task 10: Dataset detail modal
- [ ] Task 11: Pagination UI
- [ ] Task 12: Pipeline runs viewer

### Week 4: Testing & Documentation
- [ ] Task 13: Comprehensive test suite
- [ ] Task 14: API documentation updates
- [ ] Task 15: Architecture documentation
- [ ] Task 16: Integration testing

---

## Data Models

### Extended Dataset
```python
class Dataset(DatasetCreate):
    """Complete dataset with service metadata."""
    id: str
    status: Literal["active", "archived", "processing"]
    
    # Object Storage Integration
    object_storage_path: str  # e.g., "s3://data-lake/sales/2024/05"
    bucket: str  # e.g., "data-lake"
    object_key: str  # e.g., "sales/2024/05"
    
    # Data Catalog Integration
    catalog_branch: str  # e.g., "main", "feature-xyz"
    table_format: Literal["iceberg", "delta", "parquet", "csv"]
    
    # Data Characteristics
    row_count: int | None  # From preview
    size_bytes: int  # Total size
    
    # Pipeline Integration
    last_run_id: str | None  # Reference to last PipelineRun
    last_run_status: Literal["pending", "running", "success", "failed"] | None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_accessed_at: datetime | None
```

### PipelineRun
```python
class PipelineRun(BaseModel):
    """Simulated Airflow pipeline execution."""
    id: str  # e.g., "run_001"
    dataset_id: str  # Associated dataset
    status: Literal["pending", "running", "success", "failed"]
    start_time: datetime
    end_time: datetime | None
    duration_seconds: int | None
    rows_processed: int
    error_message: str | None
    logs: list[str]  # Simulated execution logs
```

### ObjectStorageFile
```python
class ObjectStorageFile(BaseModel):
    """MinIO-like object storage metadata."""
    id: str
    bucket: str
    key: str
    size_bytes: int
    content_type: str
    created_at: datetime
    updated_at: datetime
    version_id: str | None
    etag: str
```

---

## API Endpoints (Phase 3)

### Extended Dataset Endpoints
```
GET /api/datasets?status=active&format=iceberg&limit=20&offset=0
GET /api/datasets?search=sales&sort_by=updated_at&order=desc
GET /api/datasets/aggregations  # Returns stats
POST /api/datasets/{id}/preview  # Get sample rows
```

### Pipeline Run Endpoints
```
GET /api/datasets/{id}/pipeline-runs
POST /api/datasets/{id}/pipeline-runs  # Simulate new run
GET /api/pipeline-runs/{run_id}
GET /api/pipeline-runs/{run_id}/logs
```

### Object Storage Endpoints
```
GET /api/storage/buckets/{bucket}
GET /api/storage/objects/{bucket}/{key}
GET /api/storage/objects?bucket=data-lake&prefix=sales/
```

---

## Success Criteria

- ✅ All 40+ new test cases passing
- ✅ Extended dataset model with all fields
- ✅ Pipeline runs CRUD endpoints working
- ✅ Object storage simulation endpoints
- ✅ Advanced query filters implemented
- ✅ Pagination working correctly
- ✅ Frontend filters and detail views
- ✅ Complete documentation
- ✅ 0 warnings in test output
- ✅ Code coverage > 85%

---

## Next Phase Considerations (Phase 4)

Once Phase 3 is complete, Phase 4 will:
- Integrate real PostgreSQL database
- Add user authentication
- Implement real MinIO integration
- Add data lineage tracking
- Implement caching layer

---

## Related Documentation

- [Phase 2 Completion](PHASE_2_COMPLETION.md)
- [PLAN.md](PLAN.md)
- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)
- [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)

---

**Last Updated:** May 14, 2026  
**Status:** Planning Complete → Ready for Implementation
