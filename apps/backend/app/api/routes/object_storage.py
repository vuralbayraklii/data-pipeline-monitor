"""Object storage simulation routes."""
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, HTTPException
import hashlib

from app.models.object_storage import ObjectStorageFile

router = APIRouter(prefix="/storage", tags=["object-storage"])

# In-memory storage (Phase 3; MinIO integration in Phase 4)
_objects: dict[str, ObjectStorageFile] = {}
_object_counter = 0

def _generate_object_id() -> str:
    """Generate sequential object ID."""
    global _object_counter
    _object_counter += 1
    return f"obj_{_object_counter:04d}"

def _generate_etag(content: str) -> str:
    """Generate ETag (simple MD5-like hash)."""
    return hashlib.md5(content.encode()).hexdigest()[:16]

def reset_storage() -> None:
    """Reset storage (for testing)."""
    global _objects, _object_counter
    _objects = {}
    _object_counter = 0

# Pre-populate with sample data
def _init_sample_data():
    """Initialize with sample storage objects."""
    sample_objects = [
        {
            "bucket": "data-lake",
            "key": "sales/2024/05/data.parquet",
            "size_bytes": 5368709120,
            "content_type": "application/octet-stream",
            "metadata": {"dataset_id": "ds_0001", "format": "iceberg", "rows": 1500000}
        },
        {
            "bucket": "data-lake",
            "key": "customers/2024/05/data.parquet",
            "size_bytes": 1073741824,
            "content_type": "application/octet-stream",
            "metadata": {"dataset_id": "ds_0002", "format": "parquet", "rows": 250000}
        },
        {
            "bucket": "data-lake",
            "key": "transactions/2024/05/data.csv",
            "size_bytes": 2147483648,
            "content_type": "text/csv",
            "metadata": {"dataset_id": "ds_0003", "format": "csv", "rows": 5000000}
        }
    ]
    
    for i, obj_data in enumerate(sample_objects):
        obj_id = f"obj_{i+1:04d}"
        now = datetime.utcnow()
        _objects[obj_id] = ObjectStorageFile(
            id=obj_id,
            bucket=obj_data["bucket"],
            key=obj_data["key"],
            size_bytes=obj_data["size_bytes"],
            content_type=obj_data["content_type"],
            created_at=now - timedelta(days=14),
            updated_at=now - timedelta(days=1),
            version_id="v1",
            etag=_generate_etag(obj_data["key"]),
            metadata=obj_data["metadata"]
        )

_init_sample_data()

@router.get("/objects")
async def list_storage_objects(bucket: str | None = None, prefix: str | None = None) -> List[ObjectStorageFile]:
    """
    List objects in storage, optionally filtered by bucket and prefix.
    
    Args:
        bucket: Filter by bucket name
        prefix: Filter by key prefix (e.g., "sales/")
        
    Returns:
        List of objects
    """
    objects = list(_objects.values())
    
    if bucket:
        objects = [obj for obj in objects if obj.bucket == bucket]
    
    if prefix:
        objects = [obj for obj in objects if obj.key.startswith(prefix)]
    
    return sorted(objects, key=lambda o: o.created_at, reverse=True)

@router.get("/buckets/{bucket}")
async def list_bucket_objects(bucket: str) -> dict:
    """
    List all objects in a specific bucket.
    
    Args:
        bucket: Bucket name
        
    Returns:
        Bucket information with objects
    """
    objects = [obj for obj in _objects.values() if obj.bucket == bucket]
    
    if not objects:
        return {
            "bucket": bucket,
            "object_count": 0,
            "total_size_bytes": 0,
            "objects": []
        }
    
    total_size = sum(obj.size_bytes for obj in objects)
    
    return {
        "bucket": bucket,
        "object_count": len(objects),
        "total_size_bytes": total_size,
        "objects": sorted(objects, key=lambda o: o.created_at, reverse=True)
    }

@router.get("/objects/{object_id}")
async def get_storage_object(object_id: str) -> ObjectStorageFile:
    """
    Get metadata for a specific object.
    
    Args:
        object_id: Object identifier
        
    Returns:
        Object metadata
        
    Raises:
        404: Object not found
    """
    if object_id not in _objects:
        raise HTTPException(status_code=404, detail="Object not found")
    
    return _objects[object_id]

@router.post("/objects", status_code=201)
async def create_storage_object(bucket: str, key: str, size_bytes: int) -> ObjectStorageFile:
    """
    Create a new storage object (simulated upload).
    
    Args:
        bucket: Target bucket
        key: Object key
        size_bytes: File size in bytes
        
    Returns:
        Created object metadata
        
    Raises:
        422: Validation error
    """
    obj_id = _generate_object_id()
    now = datetime.utcnow()
    
    obj = ObjectStorageFile(
        id=obj_id,
        bucket=bucket,
        key=key,
        size_bytes=size_bytes,
        content_type="application/octet-stream",
        created_at=now,
        updated_at=now,
        version_id="v1",
        etag=_generate_etag(key),
        metadata={"created_via": "api"}
    )
    
    _objects[obj_id] = obj
    return obj

@router.get("/stats")
async def get_storage_stats() -> dict:
    """
    Get storage statistics across all buckets.
    
    Returns:
        Storage statistics
    """
    objects = list(_objects.values())
    
    if not objects:
        return {
            "total_objects": 0,
            "total_size_bytes": 0,
            "buckets": {},
            "formats": {}
        }
    
    # Group by bucket
    buckets = {}
    for obj in objects:
        if obj.bucket not in buckets:
            buckets[obj.bucket] = {"count": 0, "size_bytes": 0}
        buckets[obj.bucket]["count"] += 1
        buckets[obj.bucket]["size_bytes"] += obj.size_bytes
    
    # Group by format (from metadata)
    formats = {}
    for obj in objects:
        fmt = obj.metadata.get("format", "unknown")
        if fmt not in formats:
            formats[fmt] = {"count": 0, "size_bytes": 0}
        formats[fmt]["count"] += 1
        formats[fmt]["size_bytes"] += obj.size_bytes
    
    return {
        "total_objects": len(objects),
        "total_size_bytes": sum(obj.size_bytes for obj in objects),
        "buckets": buckets,
        "formats": formats
    }
