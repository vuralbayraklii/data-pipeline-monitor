"""Pipeline run management routes."""
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, HTTPException

from app.models.pipeline_run import PipelineRun, PipelineRunCreate

router = APIRouter(prefix="/pipeline-runs", tags=["pipeline-runs"])

# In-memory storage (Phase 3; database in Phase 4)
_pipeline_runs: dict[str, PipelineRun] = {}
_run_counter = 0

def _generate_run_id() -> str:
    """Generate sequential run ID."""
    global _run_counter
    _run_counter += 1
    return f"run_{_run_counter:04d}"

def reset_pipeline_runs() -> None:
    """Reset pipeline runs storage (for testing)."""
    global _pipeline_runs, _run_counter
    _pipeline_runs = {}
    _run_counter = 0

@router.post("", status_code=201)
async def create_pipeline_run(run_data: PipelineRunCreate) -> PipelineRun:
    """
    Create a new pipeline run.
    
    Simulates starting a pipeline execution for a dataset.
    
    Args:
        run_data: Pipeline run creation data
        
    Returns:
        Created pipeline run
        
    Raises:
        422: Validation error
    """
    run_id = _generate_run_id()
    start_time = datetime.utcnow()
    
    # Simulate run with some duration if successful
    end_time = None
    duration_seconds = None
    error_message = None
    logs = ["Pipeline started", "Connecting to data source..."]
    
    if run_data.status == "success":
        end_time = start_time + timedelta(seconds=930)
        duration_seconds = 930
        logs.extend([
            f"Processing {run_data.rows_processed} rows",
            "Applied transformations",
            "Completed successfully"
        ])
    elif run_data.status == "failed":
        end_time = start_time + timedelta(seconds=300)
        duration_seconds = 300
        error_message = "Connection timeout to data source"
        logs.extend([
            "Processing rows...",
            f"Processed 50000 rows before error",
            f"Error: {error_message}"
        ])
    elif run_data.status == "running":
        logs.append("Still processing...")
    
    run = PipelineRun(
        id=run_id,
        dataset_id=run_data.dataset_id,
        status=run_data.status,
        rows_processed=run_data.rows_processed,
        start_time=start_time,
        end_time=end_time,
        duration_seconds=duration_seconds,
        error_message=error_message,
        logs=logs
    )
    
    _pipeline_runs[run_id] = run
    return run

@router.get("")
async def list_pipeline_runs(dataset_id: str | None = None) -> List[PipelineRun]:
    """
    List all pipeline runs, optionally filtered by dataset.
    
    Args:
        dataset_id: Optional filter by dataset ID
        
    Returns:
        List of pipeline runs
    """
    runs = list(_pipeline_runs.values())
    
    if dataset_id:
        runs = [r for r in runs if r.dataset_id == dataset_id]
    
    # Return sorted by start_time descending
    return sorted(runs, key=lambda r: r.start_time, reverse=True)

@router.get("/{run_id}")
async def get_pipeline_run(run_id: str) -> PipelineRun:
    """
    Get a specific pipeline run by ID.
    
    Args:
        run_id: Pipeline run ID
        
    Returns:
        Pipeline run details
        
    Raises:
        404: Pipeline run not found
    """
    if run_id not in _pipeline_runs:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    
    return _pipeline_runs[run_id]

@router.get("/{run_id}/logs")
async def get_pipeline_run_logs(run_id: str) -> dict:
    """
    Get logs from a pipeline run.
    
    Args:
        run_id: Pipeline run ID
        
    Returns:
        Run logs and metadata
        
    Raises:
        404: Pipeline run not found
    """
    if run_id not in _pipeline_runs:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    
    run = _pipeline_runs[run_id]
    return {
        "run_id": run.id,
        "dataset_id": run.dataset_id,
        "status": run.status,
        "start_time": run.start_time,
        "end_time": run.end_time,
        "duration_seconds": run.duration_seconds,
        "logs": run.logs,
        "error_message": run.error_message
    }

@router.put("/{run_id}")
async def update_pipeline_run(run_id: str, run_data: PipelineRunCreate) -> PipelineRun:
    """
    Update a pipeline run (useful for status changes).
    
    Args:
        run_id: Pipeline run ID
        run_data: Updated run data
        
    Returns:
        Updated pipeline run
        
    Raises:
        404: Pipeline run not found
        422: Validation error
    """
    if run_id not in _pipeline_runs:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    
    run = _pipeline_runs[run_id]
    
    # Update fields
    run.dataset_id = run_data.dataset_id
    run.status = run_data.status
    run.rows_processed = run_data.rows_processed
    run.updated_at = datetime.utcnow()
    
    # If transitioning to ended state, set end_time
    if run.status in ["success", "failed"] and run.end_time is None:
        run.end_time = datetime.utcnow()
        run.duration_seconds = int((run.end_time - run.start_time).total_seconds())
    
    _pipeline_runs[run_id] = run
    return run

@router.delete("/{run_id}", status_code=204)
async def delete_pipeline_run(run_id: str) -> None:
    """
    Delete a pipeline run.
    
    Args:
        run_id: Pipeline run ID
        
    Raises:
        404: Pipeline run not found
    """
    if run_id not in _pipeline_runs:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    
    del _pipeline_runs[run_id]
