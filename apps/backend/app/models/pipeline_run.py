"""Pipeline run data models."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class PipelineRunCreate(BaseModel):
    """Schema for creating a pipeline run."""
    dataset_id: str = Field(..., description="Associated dataset ID")
    status: Literal["pending", "running", "success", "failed"] = Field(
        default="pending",
        description="Run status"
    )
    rows_processed: int = Field(default=0, description="Number of rows processed")

class PipelineRun(PipelineRunCreate):
    """Schema for a pipeline run with metadata."""
    id: str = Field(..., description="Unique run identifier (e.g., run_001)")
    start_time: datetime = Field(..., description="Run start time")
    end_time: datetime | None = Field(default=None, description="Run end time")
    duration_seconds: int | None = Field(default=None, description="Execution duration")
    error_message: str | None = Field(default=None, description="Error details if failed")
    logs: list[str] = Field(default_factory=list, description="Execution logs")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "run_001",
                "dataset_id": "ds_001",
                "status": "success",
                "start_time": "2024-05-14T10:00:00Z",
                "end_time": "2024-05-14T10:15:30Z",
                "duration_seconds": 930,
                "rows_processed": 1500000,
                "error_message": None,
                "logs": [
                    "Started ingestion pipeline",
                    "Connected to MinIO: bucket=data-lake",
                    "Fetched 1500000 rows",
                    "Applied transformations",
                    "Completed successfully"
                ],
                "created_at": "2024-05-14T10:00:00Z",
                "updated_at": "2024-05-14T10:15:30Z"
            }
        }
    )
