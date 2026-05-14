"""Dataset registry routes."""
from typing import List
from fastapi import APIRouter

from ..models.dataset import Dataset, DatasetCreate

router = APIRouter(
    prefix="/api/datasets",
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for this learning phase
_datasets: dict[str, Dataset] = {}
_counter = 0

@router.post("", response_model=Dataset, status_code=201)
async def create_dataset(dataset_create: DatasetCreate) -> Dataset:
    """Create a new dataset.
    
    Args:
        dataset_create: The dataset data to create
        
    Returns:
        The created dataset with ID and metadata
        
    Raises:
        HTTPException: If validation fails
    """
    global _counter
    _counter += 1
    dataset_id = f"ds_{_counter:04d}"
    
    dataset = Dataset(
        id=dataset_id,
        **dataset_create.model_dump()
    )
    
    _datasets[dataset_id] = dataset
    return dataset

@router.get("", response_model=List[Dataset])
async def list_datasets() -> List[Dataset]:
    """List all datasets.
    
    Returns:
        List of all datasets in the registry
    """
    return list(_datasets.values())

@router.get("/{dataset_id}", response_model=Dataset)
async def get_dataset(dataset_id: str) -> Dataset:
    """Get a specific dataset.
    
    Args:
        dataset_id: The dataset identifier
        
    Returns:
        The requested dataset
        
    Raises:
        HTTPException: If dataset not found
    """
    if dataset_id not in _datasets:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return _datasets[dataset_id]
