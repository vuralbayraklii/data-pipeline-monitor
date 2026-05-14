"""Dataset data models."""
from typing import Literal
from pydantic import BaseModel, Field

class DatasetCreate(BaseModel):
    """Schema for creating a dataset."""
    name: str = Field(..., description="Dataset name", min_length=1, max_length=255)
    source: str = Field(..., description="Data source location (e.g., s3://bucket/path)", min_length=1)
    description: str = Field(default="", description="Dataset description", max_length=1000)

class Dataset(DatasetCreate):
    """Schema for a dataset with metadata."""
    id: str = Field(..., description="Unique dataset identifier")
    status: Literal["active", "archived", "processing"] = Field(
        default="active",
        description="Dataset status"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "ds_001",
                "name": "sales_data",
                "source": "s3://data-bucket/sales",
                "description": "Monthly sales data",
                "status": "active"
            }
        }
