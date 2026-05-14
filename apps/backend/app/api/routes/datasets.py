"""Dataset registry routes - Phase 3 with filtering, pagination, and service simulation."""
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

from app.models.dataset import Dataset, DatasetCreate

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

# In-memory storage
_datasets: dict[str, Dataset] = {}
_counter = 0

def _generate_dataset_id() -> str:
    """Generate sequential dataset ID."""
    global _counter
    _counter += 1
    return f"ds_{_counter:04d}"

def reset_datasets() -> None:
    """Reset datasets (for testing)."""
    global _datasets, _counter
    _datasets = {}
    _counter = 0

# Pre-populate with sample data for Phase 3
def _init_sample_data():
    """Initialize with sample datasets."""
    sample_datasets = [
        {
            "name": "sales_data",
            "source": "s3://data-lake/sales",
            "description": "Monthly sales data from 2024",
            "object_storage_path": "s3://data-lake/sales/2024/05",
            "bucket": "data-lake",
            "object_key": "sales/2024/05",
            "catalog_branch": "main",
            "table_format": "iceberg",
            "row_count": 1500000,
            "size_bytes": 5368709120,
            "status": "active"
        },
        {
            "name": "customer_data",
            "source": "s3://data-lake/customers",
            "description": "Customer master data",
            "object_storage_path": "s3://data-lake/customers/2024/05",
            "bucket": "data-lake",
            "object_key": "customers/2024/05",
            "catalog_branch": "main",
            "table_format": "parquet",
            "row_count": 250000,
            "size_bytes": 1073741824,
            "status": "active"
        },
        {
            "name": "transactions_data",
            "source": "s3://data-lake/transactions",
            "description": "All transactions processed",
            "object_storage_path": "s3://data-lake/transactions/2024/05",
            "bucket": "data-lake",
            "object_key": "transactions/2024/05",
            "catalog_branch": "feature-branch",
            "table_format": "csv",
            "row_count": 5000000,
            "size_bytes": 2147483648,
            "status": "processing",
            "last_run_id": "run_0001",
            "last_run_status": "running"
        }
    ]
    
    for i, data in enumerate(sample_datasets):
        ds_id = _generate_dataset_id()
        now = datetime.utcnow()
        dataset = Dataset(
            id=ds_id,
            name=data["name"],
            source=data["source"],
            description=data.get("description", ""),
            status=data.get("status", "active"),
            object_storage_path=data["object_storage_path"],
            bucket=data["bucket"],
            object_key=data["object_key"],
            catalog_branch=data.get("catalog_branch", "main"),
            table_format=data.get("table_format", "iceberg"),
            row_count=data.get("row_count"),
            size_bytes=data.get("size_bytes", 0),
            last_run_id=data.get("last_run_id"),
            last_run_status=data.get("last_run_status"),
            created_at=now - timedelta(days=30),
            updated_at=now - timedelta(days=i),
        )
        _datasets[ds_id] = dataset

_init_sample_data()

@router.post("", status_code=201)
async def create_dataset(dataset: DatasetCreate) -> Dataset:
    """
    Create a new dataset.
    
    Args:
        dataset: Dataset creation data
        
    Returns:
        Created dataset
        
    Raises:
        422: Validation error
    """
    dataset_id = _generate_dataset_id()
    now = datetime.utcnow()
    
    # Extract bucket and key from source path
    source_parts = dataset.source.split("/")
    bucket = source_parts[2] if len(source_parts) > 2 else "data-lake"
    object_key = "/".join(source_parts[3:]) if len(source_parts) > 3 else ""
    
    new_dataset = Dataset(
        id=dataset_id,
        name=dataset.name,
        source=dataset.source,
        description=dataset.description,
        object_storage_path=dataset.source,
        bucket=bucket,
        object_key=object_key,
        created_at=now,
        updated_at=now
    )
    
    _datasets[dataset_id] = new_dataset
    return new_dataset

@router.get("")
async def list_datasets(
    status: str | None = None,
    format: str | None = None,
    branch: str | None = None,
    search: str | None = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    order: str = "desc"
) -> dict:
    """
    List datasets with filtering and pagination.
    
    Args:
        status: Filter by status (active, archived, processing)
        format: Filter by table format (iceberg, delta, parquet, csv)
        branch: Filter by catalog branch
        search: Search by name or description
        limit: Number of results to return
        offset: Number of results to skip
        sort_by: Field to sort by (name, size_bytes, created_at, updated_at)
        order: Sort order (asc, desc)
        
    Returns:
        Filtered and paginated datasets with metadata
    """
    datasets = list(_datasets.values())
    
    # Apply filters
    if status:
        datasets = [d for d in datasets if d.status == status]
    
    if format:
        datasets = [d for d in datasets if d.table_format == format]
    
    if branch:
        datasets = [d for d in datasets if d.catalog_branch == branch]
    
    if search:
        search_lower = search.lower()
        datasets = [d for d in datasets if search_lower in d.name.lower() or search_lower in d.description.lower()]
    
    # Count before pagination
    total = len(datasets)
    
    # Sort
    reverse = (order == "desc")
    if sort_by == "name":
        datasets.sort(key=lambda d: d.name, reverse=reverse)
    elif sort_by == "size_bytes":
        datasets.sort(key=lambda d: d.size_bytes, reverse=reverse)
    elif sort_by == "updated_at":
        datasets.sort(key=lambda d: d.updated_at, reverse=reverse)
    else:  # created_at default
        datasets.sort(key=lambda d: d.created_at, reverse=reverse)
    
    # Paginate
    paginated = datasets[offset:offset + limit]
    
    return {
        "items": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
        "page": offset // limit + 1 if limit > 0 else 1,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/aggregations", )
async def get_dataset_aggregations() -> dict:
    """
    Get dataset aggregations and statistics.
    
    Returns:
        Aggregated statistics
    """
    datasets = list(_datasets.values())
    
    if not datasets:
        return {
            "total_datasets": 0,
            "total_size_bytes": 0,
            "by_status": {},
            "by_format": {},
            "by_branch": {}
        }
    
    # Group by status
    by_status = {}
    for ds in datasets:
        status = ds.status
        if status not in by_status:
            by_status[status] = {"count": 0, "size_bytes": 0}
        by_status[status]["count"] += 1
        by_status[status]["size_bytes"] += ds.size_bytes
    
    # Group by format
    by_format = {}
    for ds in datasets:
        fmt = ds.table_format
        if fmt not in by_format:
            by_format[fmt] = {"count": 0}
        by_format[fmt]["count"] += 1
    
    # Group by branch
    by_branch = {}
    for ds in datasets:
        branch = ds.catalog_branch
        if branch not in by_branch:
            by_branch[branch] = {"count": 0}
        by_branch[branch]["count"] += 1
    
    return {
        "total_datasets": len(datasets),
        "total_size_bytes": sum(d.size_bytes for d in datasets),
        "by_status": by_status,
        "by_format": by_format,
        "by_branch": by_branch
    }

@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str) -> Dataset:
    """
    Get a specific dataset by ID.
    
    Args:
        dataset_id: Dataset ID
        
    Returns:
        Dataset details
        
    Raises:
        404: Dataset not found
    """
    if dataset_id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return _datasets[dataset_id]

@router.put("/{dataset_id}")
async def update_dataset(dataset_id: str, dataset: DatasetCreate) -> Dataset:
    """
    Update a dataset.
    
    Args:
        dataset_id: Dataset ID
        dataset: Updated dataset data
        
    Returns:
        Updated dataset
        
    Raises:
        404: Dataset not found
        422: Validation error
    """
    if dataset_id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    existing = _datasets[dataset_id]
    existing.name = dataset.name
    existing.source = dataset.source
    existing.description = dataset.description
    existing.updated_at = datetime.utcnow()
    
    _datasets[dataset_id] = existing
    return existing

@router.delete("/{dataset_id}", status_code=204)
async def delete_dataset(dataset_id: str) -> None:
    """
    Delete a dataset.
    
    Args:
        dataset_id: Dataset ID
        
    Raises:
        404: Dataset not found
    """
    if dataset_id not in _datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    del _datasets[dataset_id]
