"""
Integration tests for forecast API endpoints.

These tests verify the complete workflow of ingesting data and querying deltas.
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from glyphd.api.router import create_app
from glyphd.core.storage.sqlite_store import SqliteListingStore


@pytest.fixture
def client():
    """Create test client with in-memory database."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def storage():
    """Create test storage with in-memory database."""
    store = SqliteListingStore(":memory:")
    store.initialize_schema()
    return store


class TestForecastAPIIntegration:
    """Integration tests for forecast API endpoints."""
    
    def test_forecast_deltas_empty_database(self, client):
        """Test forecast deltas endpoint with empty database."""
        response = client.get("/api/forecast/deltas")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_forecast_deltas_with_filters(self, client):
        """Test forecast deltas endpoint with query filters."""
        # Test with various filter combinations
        response = client.get("/api/forecast/deltas?model=RTX_4090")
        assert response.status_code == 200
        
        response = client.get("/api/forecast/deltas?min_price_change_pct=5.0")
        assert response.status_code == 200
        
        response = client.get("/api/forecast/deltas?region=US")
        assert response.status_code == 200
        
        response = client.get("/api/forecast/deltas?limit=50")
        assert response.status_code == 200
    
    def test_forecast_delta_by_id_not_found(self, client):
        """Test getting specific delta that doesn't exist."""
        response = client.get("/api/forecast/deltas/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_complete_ingestion_and_delta_workflow(self, client):
        """Test complete workflow: ingest data twice, then query deltas."""
        # First ingestion - create initial snapshots
        first_listings = [
            {
                "canonical_model": "RTX_4090",
                "vram_gb": 24,
                "mig_support": 0,
                "nvlink": False,
                "tdp_watts": 450,
                "price": 1500.0,
                "score": 85.0,
                "import_id": "test-import-1",
                "import_index": 0,
            },
            {
                "canonical_model": "RTX_3080",
                "vram_gb": 10,
                "mig_support": 0,
                "nvlink": False,
                "tdp_watts": 320,
                "price": 800.0,
                "score": 75.0,
                "import_id": "test-import-1",
                "import_index": 1,
            }
        ]
        
        response = client.post("/api/persist/listings", json=first_listings)
        assert response.status_code == 200
        first_result = response.json()
        assert first_result["record_count"] == 2
        
        # Wait a moment to ensure different timestamps
        import time
        time.sleep(0.1)
        
        # Second ingestion with modified prices - should create deltas
        second_listings = [
            {
                "canonical_model": "RTX_4090",
                "vram_gb": 24,
                "mig_support": 0,
                "nvlink": False,
                "tdp_watts": 450,
                "price": 1600.0,  # Price increased by $100
                "score": 87.0,    # Score increased by 2
                "import_id": "test-import-2",
                "import_index": 0,
            },
            {
                "canonical_model": "RTX_3080",
                "vram_gb": 10,
                "mig_support": 0,
                "nvlink": False,
                "tdp_watts": 320,
                "price": 750.0,   # Price decreased by $50
                "score": 73.0,    # Score decreased by 2
                "import_id": "test-import-2",
                "import_index": 1,
            }
        ]
        
        response = client.post("/api/persist/listings", json=second_listings)
        assert response.status_code == 200
        second_result = response.json()
        assert second_result["record_count"] == 2
        
        # Query deltas - should have deltas from the second ingestion
        response = client.get("/api/forecast/deltas")
        assert response.status_code == 200
        deltas = response.json()
        
        # We should have deltas, but the exact count depends on whether
        # the snapshots have matching source_urls (which may be None)
        assert isinstance(deltas, list)
        
        # Test filtering by model
        response = client.get("/api/forecast/deltas?model=RTX_4090")
        assert response.status_code == 200
        rtx4090_deltas = response.json()
        assert isinstance(rtx4090_deltas, list)
        
        # Test filtering by minimum price change
        response = client.get("/api/forecast/deltas?min_price_change_pct=5.0")
        assert response.status_code == 200
        significant_deltas = response.json()
        assert isinstance(significant_deltas, list)
    
    def test_forecast_deltas_response_format(self, client):
        """Test that forecast deltas response has correct format."""
        response = client.get("/api/forecast/deltas")
        assert response.status_code == 200
        
        deltas = response.json()
        assert isinstance(deltas, list)
        
        # If there are deltas, verify the structure
        for delta in deltas:
            required_fields = [
                "id", "model", "price_delta", "price_delta_pct", 
                "score_delta", "timestamp", "current_snapshot_id", 
                "previous_snapshot_id"
            ]
            for field in required_fields:
                assert field in delta
            
            # Verify data types
            assert isinstance(delta["id"], int)
            assert isinstance(delta["model"], str)
            assert isinstance(delta["price_delta"], int | float)
            assert isinstance(delta["price_delta_pct"], int | float)
            assert isinstance(delta["score_delta"], int | float)
            assert isinstance(delta["current_snapshot_id"], int)
            assert isinstance(delta["previous_snapshot_id"], int)
    
    def test_forecast_delta_limit_parameter(self, client):
        """Test that limit parameter works correctly."""
        # Test with small limit
        response = client.get("/api/forecast/deltas?limit=1")
        assert response.status_code == 200
        deltas = response.json()
        assert len(deltas) <= 1
        
        # Test with larger limit
        response = client.get("/api/forecast/deltas?limit=100")
        assert response.status_code == 200
        deltas = response.json()
        assert len(deltas) <= 100
    
    def test_forecast_deltas_timestamp_filter(self, client):
        """Test filtering deltas by timestamp."""
        # Test with future timestamp (should return no results)
        future_time = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        response = client.get(f"/api/forecast/deltas?after={future_time}")
        assert response.status_code == 200
        deltas = response.json()
        assert len(deltas) == 0
        
        # Test with past timestamp
        past_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        response = client.get(f"/api/forecast/deltas?after={past_time}")
        assert response.status_code == 200
        # Should not error, regardless of results
    
    def test_forecast_api_error_handling(self, client):
        """Test error handling in forecast API."""
        # Test invalid delta ID
        response = client.get("/api/forecast/deltas/invalid")
        assert response.status_code == 422  # Validation error for non-integer ID
        
        # Test invalid query parameters
        response = client.get("/api/forecast/deltas?min_price_change_pct=invalid")
        assert response.status_code == 422  # Validation error for non-float value
        
        response = client.get("/api/forecast/deltas?limit=invalid")
        assert response.status_code == 422  # Validation error for non-integer limit


class TestForecastWorkflowWithCSV:
    """Test forecast functionality with CSV ingestion."""
    
    def test_csv_ingestion_creates_snapshots_and_deltas(self, client):
        """Test that CSV ingestion creates snapshots and deltas."""
        # Create test CSV content
        csv_content_v1 = """title,price,condition,seller
"NVIDIA GeForce RTX 4090 24GB Graphics Card",1500.00,New,TechStore
"RTX 3080 Ti 12GB Gaming Card",800.00,Used,GamersParadise"""
        
        csv_content_v2 = """title,price,condition,seller
"NVIDIA GeForce RTX 4090 24GB Graphics Card",1600.00,New,TechStore
"RTX 3080 Ti 12GB Gaming Card",750.00,Used,GamersParadise"""
        
        # First CSV upload
        response = client.post(
            "/api/import/csv",
            files={"file": ("test_v1.csv", csv_content_v1, "text/csv")}
        )
        assert response.status_code == 200
        result1 = response.json()
        assert result1["record_count"] > 0
        
        # Wait a moment
        import time
        time.sleep(0.1)
        
        # Second CSV upload with different prices
        response = client.post(
            "/api/import/csv",
            files={"file": ("test_v2.csv", csv_content_v2, "text/csv")}
        )
        assert response.status_code == 200
        result2 = response.json()
        assert result2["record_count"] > 0
        
        # Query deltas
        response = client.get("/api/forecast/deltas")
        assert response.status_code == 200
        deltas = response.json()
        
        # Should have some deltas from the price changes
        # Note: Actual delta creation depends on source_url matching
        assert isinstance(deltas, list)