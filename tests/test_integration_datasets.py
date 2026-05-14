"""Integration tests for Dataset Registry module."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_datasets():
    """Reset datasets before each test."""
    from app.api.routes import datasets
    datasets._datasets.clear()
    datasets._counter = 0
    yield

class TestDatasetCRUDOperations:
    """Complete CRUD test suite for datasets."""

    def test_create_dataset_with_all_fields(self):
        """Test creating dataset with all fields."""
        payload = {
            "name": "sales_data",
            "source": "s3://bucket/sales",
            "description": "Monthly sales data"
        }
        
        response = client.post("/api/datasets", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "sales_data"
        assert data["source"] == "s3://bucket/sales"
        assert data["description"] == "Monthly sales data"
        assert data["id"].startswith("ds_")
        assert data["status"] == "active"

    def test_create_dataset_with_minimal_fields(self):
        """Test creating dataset with only required fields."""
        payload = {
            "name": "minimal_dataset",
            "source": "s3://bucket/minimal"
        }
        
        response = client.post("/api/datasets", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "minimal_dataset"
        assert data["description"] == ""

    def test_get_dataset_after_creation(self):
        """Test retrieving a created dataset."""
        # Create
        create_payload = {
            "name": "test_dataset",
            "source": "s3://bucket/test"
        }
        create_resp = client.post("/api/datasets", json=create_payload)
        dataset_id = create_resp.json()["id"]
        
        # Get
        get_resp = client.get(f"/api/datasets/{dataset_id}")
        
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == dataset_id

    def test_list_multiple_datasets(self):
        """Test listing multiple datasets."""
        # Create 3 datasets
        for i in range(3):
            payload = {
                "name": f"dataset_{i}",
                "source": f"s3://bucket/data_{i}"
            }
            client.post("/api/datasets", json=payload)
        
        # List
        response = client.get("/api/datasets")
        
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) == 3

    def test_update_dataset(self):
        """Test updating an existing dataset."""
        # Create
        create_payload = {
            "name": "original",
            "source": "s3://bucket/original"
        }
        create_resp = client.post("/api/datasets", json=create_payload)
        dataset_id = create_resp.json()["id"]
        
        # Update
        update_payload = {
            "name": "updated",
            "source": "s3://bucket/updated",
            "description": "Updated description"
        }
        update_resp = client.put(f"/api/datasets/{dataset_id}", json=update_payload)
        
        assert update_resp.status_code == 200
        updated_data = update_resp.json()
        assert updated_data["name"] == "updated"
        assert updated_data["source"] == "s3://bucket/updated"
        assert updated_data["description"] == "Updated description"
        assert updated_data["id"] == dataset_id

    def test_delete_dataset(self):
        """Test deleting a dataset."""
        # Create
        create_payload = {
            "name": "to_delete",
            "source": "s3://bucket/delete"
        }
        create_resp = client.post("/api/datasets", json=create_payload)
        dataset_id = create_resp.json()["id"]
        
        # Delete
        delete_resp = client.delete(f"/api/datasets/{dataset_id}")
        assert delete_resp.status_code == 204
        
        # Verify gone
        get_resp = client.get(f"/api/datasets/{dataset_id}")
        assert get_resp.status_code == 404

    def test_full_crud_workflow(self):
        """Test complete CREATE → READ → UPDATE → DELETE workflow."""
        # CREATE
        create_payload = {
            "name": "lifecycle_test",
            "source": "s3://bucket/lifecycle",
            "description": "Test complete lifecycle"
        }
        create_resp = client.post("/api/datasets", json=create_payload)
        assert create_resp.status_code == 201
        dataset_id = create_resp.json()["id"]
        
        # READ
        get_resp = client.get(f"/api/datasets/{dataset_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "lifecycle_test"
        
        # UPDATE
        update_payload = {
            "name": "lifecycle_updated",
            "source": "s3://bucket/lifecycle2"
        }
        put_resp = client.put(f"/api/datasets/{dataset_id}", json=update_payload)
        assert put_resp.status_code == 200
        assert put_resp.json()["name"] == "lifecycle_updated"
        
        # DELETE
        delete_resp = client.delete(f"/api/datasets/{dataset_id}")
        assert delete_resp.status_code == 204
        
        # VERIFY
        final_resp = client.get(f"/api/datasets/{dataset_id}")
        assert final_resp.status_code == 404

class TestErrorHandling:
    """Test error cases."""

    def test_create_dataset_missing_name(self):
        """Test validation: missing name."""
        payload = {"source": "s3://bucket"}
        response = client.post("/api/datasets", json=payload)
        assert response.status_code == 422

    def test_create_dataset_missing_source(self):
        """Test validation: missing source."""
        payload = {"name": "dataset"}
        response = client.post("/api/datasets", json=payload)
        assert response.status_code == 422

    def test_get_nonexistent_dataset(self):
        """Test getting non-existent dataset."""
        response = client.get("/api/datasets/ds_0000")
        assert response.status_code == 404

    def test_update_nonexistent_dataset(self):
        """Test updating non-existent dataset."""
        payload = {"name": "name", "source": "s3://bucket"}
        response = client.put("/api/datasets/ds_0000", json=payload)
        assert response.status_code == 404

    def test_delete_nonexistent_dataset(self):
        """Test deleting non-existent dataset."""
        response = client.delete("/api/datasets/ds_0000")
        assert response.status_code == 404

class TestHealthChecks:
    """Test service health endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == "0.1.0"
        assert "status" in data

class TestDatasetIDSequencing:
    """Test dataset ID generation."""

    def test_dataset_ids_are_sequential(self):
        """Test that dataset IDs are auto-incremented."""
        ids = []
        for i in range(3):
            payload = {
                "name": f"dataset_{i}",
                "source": f"s3://bucket/{i}"
            }
            response = client.post("/api/datasets", json=payload)
            ids.append(response.json()["id"])
        
        # Check sequential pattern
        assert ids[0] == "ds_0001"
        assert ids[1] == "ds_0002"
        assert ids[2] == "ds_0003"

    def test_list_datasets_preserves_creation_order(self):
        """Test that listing datasets maintains order."""
        names = []
        for i in range(3):
            payload = {
                "name": f"dataset_{i}",
                "source": f"s3://bucket/{i}"
            }
            client.post("/api/datasets", json=payload)
            names.append(f"dataset_{i}")
        
        response = client.get("/api/datasets")
        datasets = response.json()
        retrieved_names = [d["name"] for d in datasets]
        
        assert retrieved_names == names
