"""Dataset data models."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class DatasetCreate(BaseModel):
    """Schema for creating a dataset."""
    name: str = Field(..., description="Dataset name", min_length=1, max_length=255)
    source: str = Field(..., description="Data source location (e.g., s3://bucket/path)", min_length=1)
    description: str = Field(default="", description="Dataset description", max_length=1000)

class Dataset(DatasetCreate):
    """Schema for a dataset with full metadata."""
    id: str = Field(..., description="Unique dataset identifier")
    status: Literal["active", "archived", "processing"] = Field(
        default="active",
        description="Dataset status"
    )
    
    # Object Storage Integration
    object_storage_path: str = Field(..., description="S3 path (e.g., s3://bucket/key)")
    bucket: str = Field(..., description="Storage bucket name")
    object_key: str = Field(..., description="Object key in bucket")
    
    # Data Catalog Integration
    catalog_branch: str = Field(default="main", description="Nessie branch reference")
    table_format: Literal["iceberg", "delta", "parquet", "csv"] = Field(
        default="iceberg",
        description="Table format"
    )
    
    # Data Characteristics
    row_count: int | None = Field(default=None, description="Estimated row count")
    size_bytes: int = Field(default=0, description="Total size in bytes")
    
    # Pipeline Integration
    last_run_id: str | None = Field(default=None, description="Last pipeline run ID")
    last_run_status: Literal["pending", "running", "success", "failed"] | None = Field(
        default=None,
        description="Status of last pipeline run"
    )
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed_at: datetime | None = Field(default=None)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ds_001",
                "name": "sales_data",
                "source": "s3://data-lake/sales",
                "description": "Monthly sales data",
                "status": "active",
                "object_storage_path": "s3://data-lake/sales/2024/05",
                "bucket": "data-lake",
                "object_key": "sales/2024/05",
                "catalog_branch": "main",
                "table_format": "iceberg",
                "row_count": 1500000,
                "size_bytes": 5368709120,
                "last_run_id": "run_042",
                "last_run_status": "success",
                "created_at": "2024-05-01T10:30:00Z",
                "updated_at": "2024-05-14T15:45:00Z",
                "last_accessed_at": "2024-05-14T12:00:00Z"
            }
        }
    )

