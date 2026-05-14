"""Object storage metadata models."""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ObjectStorageFile(BaseModel):
    """Schema for MinIO-like object storage file metadata."""
    id: str = Field(..., description="Unique object identifier")
    bucket: str = Field(..., description="Bucket name (e.g., 'data-lake')")
    key: str = Field(..., description="Object key/path (e.g., 'sales/2024/05/data.parquet')")
    size_bytes: int = Field(..., description="File size in bytes")
    content_type: str = Field(default="application/octet-stream", description="MIME type")
    created_at: datetime = Field(..., description="Object creation time")
    updated_at: datetime = Field(..., description="Object last update time")
    version_id: str | None = Field(default=None, description="Version ID for versioned buckets")
    etag: str = Field(..., description="Entity tag (checksum)")
    metadata: dict = Field(default_factory=dict, description="Custom metadata")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "obj_001",
                "bucket": "data-lake",
                "key": "sales/2024/05/data.parquet",
                "size_bytes": 5368709120,
                "content_type": "application/octet-stream",
                "created_at": "2024-05-01T10:30:00Z",
                "updated_at": "2024-05-14T15:45:00Z",
                "version_id": "1234567890abcdef",
                "etag": "a1b2c3d4e5f67890",
                "metadata": {
                    "dataset_id": "ds_001",
                    "format": "iceberg",
                    "compression": "snappy"
                }
            }
        }
    )
