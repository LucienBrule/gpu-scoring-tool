"""
Integration tests for SQLite-backed REST API endpoints.

This module tests the full workflow of importing GPU listings via the persist API
and then querying them via the listings API to verify end-to-end persistence integration.
"""

import tempfile
import uuid
from datetime import datetime
from typing import List

import pytest
from fastapi.testclient import TestClient

from glyphd.api.models import GPUListingDTO
from glyphd.api.router import create_app
from glyphd.core.dependencies.listing_repository import get_listing_repository
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
    """Create a test FastAPI app with overridden storage dependencies."""
    app = create_app()

    # Override both storage dependencies to use the same test storage instance
    app.dependency_overrides[get_storage_engine] = lambda: test_storage
    app.dependency_overrides[get_listing_repository] = lambda: test_storage

    return app


@pytest.fixture
def client(test_app):
    """Create a test client for the FastAPI app."""
    return TestClient(test_app)


@pytest.fixture
def sample_listings() -> List[GPUListingDTO]:
    """Create sample GPU listings with distinct canonical models and prices for testing."""
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
    ]


def test_import_and_query_integration(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test the full integration workflow: import listings and then query them.

    This test validates that:
    1. Listings can be imported via POST /api/persist/listings
    2. Imported listings can be retrieved via GET /api/listings
    3. The data persists correctly in SQLite
    4. Response structures are valid
    """
    # Step 1: Import listings via persist endpoint
    listings_data = [listing.model_dump() for listing in sample_listings]

    import_response = client.post("/api/persist/listings", json=listings_data)

    # Verify import response
    assert import_response.status_code == 200
    import_result = import_response.json()

    # Validate import response structure
    assert "import_id" in import_result
    assert "record_count" in import_result
    assert "first_model" in import_result
    assert "last_model" in import_result
    assert "timestamp" in import_result

    # Verify import response values
    assert import_result["record_count"] == 2
    assert import_result["first_model"] == "H100_PCIE_80GB"
    assert import_result["last_model"] == "A100_SXM4_80GB"

    # Verify import_id is a valid UUID
    import_id = import_result["import_id"]
    uuid.UUID(import_id)  # This will raise ValueError if not a valid UUID

    # Verify timestamp is a valid datetime string
    timestamp_str = import_result["timestamp"]
    datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

    # Step 2: Query all listings via listings endpoint
    query_response = client.get("/api/listings")

    # Verify query response
    assert query_response.status_code == 200
    query_result = query_response.json()

    # Verify we got back the imported listings
    assert len(query_result) == 2

    # Verify the listings data matches what we imported
    returned_models = {listing["canonical_model"] for listing in query_result}
    expected_models = {"H100_PCIE_80GB", "A100_SXM4_80GB"}
    assert returned_models == expected_models

    # Verify specific listing data
    h100_listing = next(listing for listing in query_result if listing["canonical_model"] == "H100_PCIE_80GB")
    assert h100_listing["price"] == 34995.0
    assert h100_listing["score"] == 0.92
    assert h100_listing["vram_gb"] == 80

    a100_listing = next(listing for listing in query_result if listing["canonical_model"] == "A100_SXM4_80GB")
    assert a100_listing["price"] == 25000.0
    assert a100_listing["score"] == 0.85
    assert a100_listing["vram_gb"] == 80


def test_query_with_model_filter(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test querying listings with model filter after import.
    """
    # Import listings first
    listings_data = [listing.model_dump() for listing in sample_listings]
    import_response = client.post("/api/persist/listings", json=listings_data)
    assert import_response.status_code == 200

    # Query with model filter
    query_response = client.get("/api/listings?model=H100")
    assert query_response.status_code == 200

    query_result = query_response.json()

    # Should return only H100 listings (fuzzy matching)
    assert len(query_result) >= 1
    for listing in query_result:
        assert "H100" in listing["canonical_model"]


def test_query_with_price_filter(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test querying listings with price filters after import.
    """
    # Import listings first
    listings_data = [listing.model_dump() for listing in sample_listings]
    import_response = client.post("/api/persist/listings", json=listings_data)
    assert import_response.status_code == 200

    # Query with price filter (should return only A100 at $25,000)
    query_response = client.get("/api/listings?min_price=20000&max_price=30000")
    assert query_response.status_code == 200

    query_result = query_response.json()

    # Should return only A100 listing
    assert len(query_result) == 1
    assert query_result[0]["canonical_model"] == "A100_SXM4_80GB"
    assert query_result[0]["price"] == 25000.0


def test_query_with_pagination(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test querying listings with pagination after import.
    """
    # Import listings first
    listings_data = [listing.model_dump() for listing in sample_listings]
    import_response = client.post("/api/persist/listings", json=listings_data)
    assert import_response.status_code == 200

    # Query with limit=1
    query_response = client.get("/api/listings?limit=1")
    assert query_response.status_code == 200

    query_result = query_response.json()

    # Should return only 1 listing
    assert len(query_result) == 1

    # Query with offset=1, limit=1
    query_response = client.get("/api/listings?limit=1&offset=1")
    assert query_response.status_code == 200

    query_result = query_response.json()

    # Should return the second listing
    assert len(query_result) == 1


def test_empty_query_after_no_import(client: TestClient) -> None:
    """
    Test querying listings when no data has been imported.
    """
    query_response = client.get("/api/listings")
    assert query_response.status_code == 200

    query_result = query_response.json()

    # Should return empty list
    assert query_result == []


def test_import_validation_errors(client: TestClient) -> None:
    """
    Test that import endpoint properly validates input data.
    """
    # Test empty payload
    response = client.post("/api/persist/listings", json=[])
    assert response.status_code == 422
    assert "Empty listings array provided" in response.json()["detail"]

    # Test invalid payload
    invalid_data = [
        {
            "canonical_model": "H100_PCIE_80GB",
            # Missing required fields
        }
    ]
    response = client.post("/api/persist/listings", json=invalid_data)
    assert response.status_code == 422


def test_query_validation_errors(client: TestClient) -> None:
    """
    Test that query endpoint properly validates query parameters.
    """
    # Test invalid price range
    response = client.get("/api/listings?min_price=30000&max_price=20000")

    # The endpoint returns 500 due to storage layer exception handling
    # but the validation message is still present in the error detail
    assert response.status_code == 500
    assert "min_price cannot be greater than max_price" in response.json()["detail"]

    # Test invalid limit
    response = client.get("/api/listings?limit=0")
    assert response.status_code == 422

    # Test invalid offset
    response = client.get("/api/listings?offset=-1")
    assert response.status_code == 422


def test_import_id_in_api_response(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that import responses include import_id and that listings include import metadata.
    """
    # Import listings
    listings_data = [listing.model_dump() for listing in sample_listings]
    import_response = client.post("/api/persist/listings", json=listings_data)
    assert import_response.status_code == 200

    # Check that import response includes import_id
    import_result = import_response.json()
    assert "import_id" in import_result
    assert import_result["import_id"] is not None
    import_id = import_result["import_id"]

    # Validate that import_id is a valid UUID
    try:
        uuid.UUID(import_id)
    except ValueError:
        pytest.fail(f"import_id {import_id} is not a valid UUID")

    # Query listings and verify they include import metadata
    query_response = client.get("/api/listings")
    assert query_response.status_code == 200

    query_result = query_response.json()
    assert len(query_result) == len(sample_listings)

    for listing in query_result:
        # Check that import_id is present and matches
        assert "import_id" in listing
        assert listing["import_id"] == import_id

        # Check that import_index is present and valid
        assert "import_index" in listing
        assert listing["import_index"] is not None
        assert isinstance(listing["import_index"], int)
        assert listing["import_index"] >= 1
        assert listing["import_index"] <= len(sample_listings)


def test_query_with_import_id_filter(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test querying listings with import_id filter after multiple imports.
    """
    # Import first batch of listings (first listing only)
    first_batch = sample_listings[:1]
    first_batch_data = [listing.model_dump() for listing in first_batch]
    first_import_response = client.post("/api/persist/listings", json=first_batch_data)
    assert first_import_response.status_code == 200
    first_import_id = first_import_response.json()["import_id"]

    # Import second batch of listings (second listing only)
    second_batch = sample_listings[1:]
    second_batch_data = [listing.model_dump() for listing in second_batch]
    second_import_response = client.post("/api/persist/listings", json=second_batch_data)
    assert second_import_response.status_code == 200
    second_import_id = second_import_response.json()["import_id"]

    # Verify import_ids are different
    assert first_import_id != second_import_id

    # Query by first import_id
    query_response = client.get(f"/api/listings?import_id={first_import_id}")
    assert query_response.status_code == 200

    query_result = query_response.json()
    assert len(query_result) == len(first_batch)

    for listing in query_result:
        assert listing["import_id"] == first_import_id

    # Query by second import_id
    query_response = client.get(f"/api/listings?import_id={second_import_id}")
    assert query_response.status_code == 200

    query_result = query_response.json()
    assert len(query_result) == len(second_batch)

    for listing in query_result:
        assert listing["import_id"] == second_import_id

    # Query by non-existent import_id
    query_response = client.get("/api/listings?import_id=non-existent-id")
    assert query_response.status_code == 200

    query_result = query_response.json()
    assert len(query_result) == 0


def test_import_index_sequential_in_api(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that import_index is assigned sequentially within each import batch via API.
    """
    # Import listings
    listings_data = [listing.model_dump() for listing in sample_listings]
    import_response = client.post("/api/persist/listings", json=listings_data)
    assert import_response.status_code == 200

    import_id = import_response.json()["import_id"]

    # Query listings and verify import_index assignment
    query_response = client.get(f"/api/listings?import_id={import_id}")
    assert query_response.status_code == 200

    query_result = query_response.json()
    assert len(query_result) == len(sample_listings)

    # Check that import_index values are unique and sequential
    import_indices = [listing["import_index"] for listing in query_result]
    import_indices.sort()
    expected_indices = list(range(1, len(sample_listings) + 1))
    assert import_indices == expected_indices, f"Expected sequential indices {expected_indices}, got {import_indices}"


def test_multiple_imports_distinct_import_ids_api(client: TestClient, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that multiple imports generate distinct import_ids and maintain separate import_index sequences via API.
    """
    # Import same data twice to test that import_ids are distinct
    listings_data = [listing.model_dump() for listing in sample_listings]

    # First import
    first_import_response = client.post("/api/persist/listings", json=listings_data)
    assert first_import_response.status_code == 200
    first_import_id = first_import_response.json()["import_id"]

    # Second import
    second_import_response = client.post("/api/persist/listings", json=listings_data)
    assert second_import_response.status_code == 200
    second_import_id = second_import_response.json()["import_id"]

    # Verify import_ids are different
    assert first_import_id != second_import_id

    # Query first import and verify import_index sequence
    query_response = client.get(f"/api/listings?import_id={first_import_id}")
    assert query_response.status_code == 200
    first_result = query_response.json()
    assert len(first_result) == len(sample_listings)

    first_indices = sorted([listing["import_index"] for listing in first_result])
    expected_indices = list(range(1, len(sample_listings) + 1))
    assert first_indices == expected_indices

    # Query second import and verify import_index sequence
    query_response = client.get(f"/api/listings?import_id={second_import_id}")
    assert query_response.status_code == 200
    second_result = query_response.json()
    assert len(second_result) == len(sample_listings)

    second_indices = sorted([listing["import_index"] for listing in second_result])
    assert second_indices == expected_indices
