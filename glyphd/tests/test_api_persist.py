"""
Tests for the persist API endpoints.
"""

import tempfile
import uuid
from datetime import datetime
from typing import List

import pytest
from fastapi.testclient import TestClient

from glyphd.api.models import GPUListingDTO
from glyphd.api.router import create_app
from glyphd.core.dependencies.storage import get_storage_engine
from glyphd.core.storage.sqlite_store import SqliteListingStore


@pytest.fixture
def temp_db_path() -> str:
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as tmp_file:
        return tmp_file.name


@pytest.fixture
def test_storage(temp_db_path: str) -> SqliteListingStore:
    """Create a test storage engine with temporary database."""
    return SqliteListingStore(db_path=temp_db_path)


@pytest.fixture
def test_app(test_storage: SqliteListingStore):
    """Create a test FastAPI app with overridden storage dependency."""
    app = create_app()

    # Override the storage dependency for testing
    app.dependency_overrides[get_storage_engine] = lambda: test_storage

    return app


@pytest.fixture
def client(test_app):
    """Create a test client for the FastAPI app."""
    return TestClient(test_app)


@pytest.fixture
def sample_listings() -> List[GPUListingDTO]:
    """Create sample GPU listings for testing."""
    return [
        GPUListingDTO(
            canonical_model="H100_PCIE_80GB",
            vram_gb=80,
            mig_support=7,
            nvlink=True,
            tdp_watts=350,
            price=34995.0,
            score=0.92,
        ),
        GPUListingDTO(
            canonical_model="A100_SXM4_80GB",
            vram_gb=80,
            mig_support=7,
            nvlink=True,
            tdp_watts=400,
            price=25000.0,
            score=0.85,
        ),
        GPUListingDTO(
            canonical_model="RTX_4090",
            vram_gb=24,
            mig_support=0,
            nvlink=False,
            tdp_watts=450,
            price=1599.0,
            score=0.75,
        ),
    ]


def test_import_endpoint(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """Test the import listings endpoint."""
    # Convert sample listings to dict format for JSON serialization
    listings_data = [listing.model_dump() for listing in sample_listings]

    # Make POST request to import endpoint
    response = client.post("/api/persist/listings", json=listings_data)

    # Verify response status
    assert response.status_code == 200

    # Parse response data
    result_data = response.json()

    # Verify response structure matches ImportResultDTO
    assert "import_id" in result_data
    assert "record_count" in result_data
    assert "first_model" in result_data
    assert "last_model" in result_data
    assert "timestamp" in result_data

    # Verify response values
    assert result_data["record_count"] == 3
    assert result_data["first_model"] == "H100_PCIE_80GB"
    assert result_data["last_model"] == "RTX_4090"

    # Verify import_id is a valid UUID
    import_id = result_data["import_id"]
    uuid.UUID(import_id)  # This will raise ValueError if not a valid UUID

    # Verify timestamp is a valid datetime string
    timestamp_str = result_data["timestamp"]
    datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))


def test_import_endpoint_empty_payload(client: TestClient) -> None:
    """Test the import endpoint with empty payload."""
    response = client.post("/api/persist/listings", json=[])

    # Should return 422 for empty payload
    assert response.status_code == 422
    assert "Empty listings array provided" in response.json()["detail"]


def test_import_endpoint_invalid_payload(client: TestClient) -> None:
    """Test the import endpoint with invalid payload."""
    invalid_data = [
        {
            "canonical_model": "H100_PCIE_80GB",
            # Missing required fields
        }
    ]

    response = client.post("/api/persist/listings", json=invalid_data)

    # Should return 422 for validation errors
    assert response.status_code == 422


def test_import_endpoint_single_listing(client: TestClient) -> None:
    """Test the import endpoint with a single listing."""
    single_listing = [
        {
            "canonical_model": "H100_PCIE_80GB",
            "vram_gb": 80,
            "mig_support": 7,
            "nvlink": True,
            "tdp_watts": 350,
            "price": 34995.0,
            "score": 0.92,
        }
    ]

    response = client.post("/api/persist/listings", json=single_listing)

    assert response.status_code == 200
    result_data = response.json()

    assert result_data["record_count"] == 1
    assert result_data["first_model"] == "H100_PCIE_80GB"
    assert result_data["last_model"] == "H100_PCIE_80GB"
