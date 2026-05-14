"""Test dataset endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestDatasetEndpoints:
    """Test suite for dataset endpoints."""

    def test_create_dataset_success(self):
        """Test creating a dataset with valid data."""
        payload = {
            "name": "sales_data",
            "source": "s3://bucket/sales",
            "description": "Monthly sales data"
        }
        
        response = client.post("/api/datasets", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "sales_data"
        assert data["id"].startswith("ds_")
        assert data["status"] == "active"

    def test_create_dataset_missing_name(self):
        """Test creating dataset without required name."""
        payload = {
            "source": "s3://bucket/sales"
        }
        
        response = client.post("/api/datasets", json=payload)
        
        assert response.status_code == 422

    def test_list_datasets_empty(self):
        """Test listing datasets when empty."""
        response = client.get("/api/datasets")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_list_datasets_after_creation(self):
        """Test listing datasets after creating some."""
        # Create two datasets
        for i in range(2):
            payload = {
                "name": f"dataset_{i}",
                "source": f"s3://bucket/data_{i}"
            }
            client.post("/api/datasets", json=payload)
        
        response = client.get("/api/datasets")
        
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) >= 2

    def test_get_dataset_not_found(self):
        """Test getting a non-existent dataset."""
        response = client.get("/api/datasets/ds_9999")
        
        assert response.status_code == 404

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
