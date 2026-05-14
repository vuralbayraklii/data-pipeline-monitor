"""Test dataset endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestDatasetEndpoints:
    """Test suite for dataset endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Clear datasets before each test."""
        from app.api.routes import datasets
        datasets._datasets.clear()
        datasets._counter = 0

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
        data = response.json()
        assert "items" in data
        assert data["items"] == []
        assert data["total"] == 0

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
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 2

    def test_get_dataset_not_found(self):
        """Test getting a non-existent dataset."""
        response = client.get("/api/datasets/ds_9999")
        
        assert response.status_code == 404

    def test_get_dataset_success(self):
        """Test getting an existing dataset."""
        # Create a dataset first
        payload = {
            "name": "test_data",
            "source": "s3://bucket/test"
        }
        create_response = client.post("/api/datasets", json=payload)
        dataset_id = create_response.json()["id"]
        
        # Get the dataset
        response = client.get(f"/api/datasets/{dataset_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == dataset_id
        assert data["name"] == "test_data"

    def test_update_dataset_success(self):
        """Test updating an existing dataset."""
        # Create a dataset
        payload = {
            "name": "original_name",
            "source": "s3://bucket/original"
        }
        create_response = client.post("/api/datasets", json=payload)
        dataset_id = create_response.json()["id"]
        
        # Update the dataset
        update_payload = {
            "name": "updated_name",
            "source": "s3://bucket/updated",
            "description": "Updated description"
        }
        response = client.put(f"/api/datasets/{dataset_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == dataset_id
        assert data["name"] == "updated_name"
        assert data["source"] == "s3://bucket/updated"
        assert data["description"] == "Updated description"

    def test_update_dataset_not_found(self):
        """Test updating a non-existent dataset."""
        payload = {
            "name": "new_name",
            "source": "s3://bucket/new"
        }
        
        response = client.put("/api/datasets/ds_9999", json=payload)
        
        assert response.status_code == 404

    def test_delete_dataset_success(self):
        """Test deleting an existing dataset."""
        # Create a dataset
        payload = {
            "name": "to_delete",
            "source": "s3://bucket/delete"
        }
        create_response = client.post("/api/datasets", json=payload)
        dataset_id = create_response.json()["id"]
        
        # Delete the dataset
        response = client.delete(f"/api/datasets/{dataset_id}")
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/datasets/{dataset_id}")
        assert get_response.status_code == 404

    def test_delete_dataset_not_found(self):
        """Test deleting a non-existent dataset."""
        response = client.delete("/api/datasets/ds_9999")
        
        assert response.status_code == 404

    def test_full_crud_flow(self):
        """Test complete CRUD workflow."""
        # CREATE
        create_payload = {
            "name": "workflow_test",
            "source": "s3://bucket/workflow",
            "description": "Testing full workflow"
        }
        create_response = client.post("/api/datasets", json=create_payload)
        assert create_response.status_code == 201
        dataset_id = create_response.json()["id"]
        
        # READ
        read_response = client.get(f"/api/datasets/{dataset_id}")
        assert read_response.status_code == 200
        
        # UPDATE
        update_payload = {
            "name": "workflow_test_updated",
            "source": "s3://bucket/workflow_v2",
            "description": "Updated in workflow test"
        }
        update_response = client.put(f"/api/datasets/{dataset_id}", json=update_payload)
        assert update_response.status_code == 200
        
        # DELETE
        delete_response = client.delete(f"/api/datasets/{dataset_id}")
        assert delete_response.status_code == 204

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
