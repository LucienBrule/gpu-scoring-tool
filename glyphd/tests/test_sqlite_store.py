"""
Tests for the SqliteListingStore class.

This module contains tests for the SqliteListingStore class, which implements
the ListingStore interface using SQLite as the storage backend.
"""

import os
import tempfile
from typing import List

import pytest
from sqlalchemy import create_engine, text

from glyphd.api.models import GPUListingDTO
from glyphd.core.storage import SqliteListingStore


@pytest.fixture
def sample_listings() -> List[GPUListingDTO]:
    """
    Fixture that returns a list of sample GPU listings.

    Returns:
        A list of sample GPU listings
    """
    return [
        GPUListingDTO(
            canonical_model="H100_PCIE_80GB",
            vram_gb=80,
            mig_support=7,
            nvlink=True,
            tdp_watts=350,
            price=10000.0,
            score=0.7,
        ),
        GPUListingDTO(
            canonical_model="A100_PCIE_80GB",
            vram_gb=80,
            mig_support=7,
            nvlink=True,
            tdp_watts=300,
            price=8000.0,
            score=0.8,
        ),
        GPUListingDTO(
            canonical_model="RTX_4090",
            vram_gb=24,
            mig_support=0,
            nvlink=False,
            tdp_watts=450,
            price=1500.0,
            score=0.6,
        ),
    ]


@pytest.fixture
def temp_db_path() -> str:
    """
    Fixture that returns a path to a temporary SQLite database.

    Returns:
        Path to a temporary SQLite database
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.sqlite3")
    yield db_path
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)
    os.rmdir(temp_dir)


def test_init_creates_schema(temp_db_path: str) -> None:
    """
    Test that initializing the SqliteListingStore creates the schema.

    Args:
        temp_db_path: Path to a temporary SQLite database
    """
    # Initialize the store
    _store = SqliteListingStore(temp_db_path)

    # Check that the schema was created
    engine = create_engine(f"sqlite:///{temp_db_path}")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"))
        assert result.fetchone() is not None, "schema_version table not created"

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='import_batches'"))
        assert result.fetchone() is not None, "import_batches table not created"

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='models'"))
        assert result.fetchone() is not None, "models table not created"

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='listings'"))
        assert result.fetchone() is not None, "listings table not created"

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='scored_listings'"))
        assert result.fetchone() is not None, "scored_listings table not created"

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='quantized_listings'"))
        assert result.fetchone() is not None, "quantized_listings table not created"


def test_insert_listings(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that inserting listings works correctly.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings
    import_id = "test-import-1"
    count = store.insert_listings(sample_listings, import_id)

    # Check that the correct number of listings was inserted
    assert count == len(sample_listings), f"Expected {len(sample_listings)} listings to be inserted, got {count}"

    # Check that the import batch was created
    engine = create_engine(f"sqlite:///{temp_db_path}")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT import_id, record_count FROM import_batches WHERE import_id = :import_id"),
            {"import_id": import_id},
        )
        row = result.fetchone()
        assert row is not None, f"Import batch {import_id} not created"
        assert row[0] == import_id, f"Expected import_id {import_id}, got {row[0]}"
        assert row[1] == len(sample_listings), f"Expected record_count {len(sample_listings)}, got {row[1]}"

        # Check that the models were created
        for listing in sample_listings:
            result = conn.execute(
                text("SELECT model FROM models WHERE model = :model"),
                {"model": listing.canonical_model},
            )
            assert result.fetchone() is not None, f"Model {listing.canonical_model} not created"

        # Check that the scored listings were created
        result = conn.execute(text("SELECT COUNT(*) FROM scored_listings"))
        count = result.fetchone()[0]
        assert count == len(sample_listings), f"Expected {len(sample_listings)} scored listings, got {count}"


def test_query_listings(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that querying listings works correctly.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings
    import_id = "test-import-1"
    store.insert_listings(sample_listings, import_id)

    # Query all listings
    listings = store.query_listings()
    assert len(listings) == len(sample_listings), f"Expected {len(sample_listings)} listings, got {len(listings)}"

    # Query by model
    model = "H100_PCIE_80GB"
    listings = store.query_listings(model=model)
    assert len(listings) == 1, f"Expected 1 listing for model {model}, got {len(listings)}"
    assert listings[0].canonical_model == model, f"Expected model {model}, got {listings[0].canonical_model}"

    # Query by min_score
    min_score = 0.7
    listings = store.query_listings(min_score=min_score)
    assert len(listings) == 2, f"Expected 2 listings with score >= {min_score}, got {len(listings)}"
    for listing in listings:
        assert listing.score >= min_score, f"Expected score >= {min_score}, got {listing.score}"

    # Query by max_score
    max_score = 0.7
    listings = store.query_listings(max_score=max_score)
    assert len(listings) == 2, f"Expected 2 listings with score <= {max_score}, got {len(listings)}"
    for listing in listings:
        assert listing.score <= max_score, f"Expected score <= {max_score}, got {listing.score}"


def test_list_imports(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that listing imports works correctly.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings with two different import IDs
    import_id_1 = "test-import-1"
    import_id_2 = "test-import-2"
    store.insert_listings(sample_listings[:2], import_id_1)
    store.insert_listings(sample_listings[2:], import_id_2)

    # List the imports
    imports = store.list_imports()
    assert len(imports) == 2, f"Expected 2 imports, got {len(imports)}"

    # Check that the imports have the correct IDs and record counts
    import_ids = [imp.import_id for imp in imports]
    assert import_id_1 in import_ids, f"Expected import ID {import_id_1} in {import_ids}"
    assert import_id_2 in import_ids, f"Expected import ID {import_id_2} in {import_ids}"

    for imp in imports:
        if imp.import_id == import_id_1:
            assert imp.record_count == 2, f"Expected record_count 2 for import {import_id_1}, got {imp.record_count}"
        elif imp.import_id == import_id_2:
            assert imp.record_count == 1, f"Expected record_count 1 for import {import_id_2}, got {imp.record_count}"


def test_idempotent_insert(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that inserting the same listings with the same import ID is idempotent.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings twice with the same import ID
    import_id = "test-import-1"
    store.insert_listings(sample_listings, import_id)
    store.insert_listings(sample_listings, import_id)

    # Check that there is only one import batch
    imports = store.list_imports()
    assert len(imports) == 1, f"Expected 1 import, got {len(imports)}"
    assert imports[0].import_id == import_id, f"Expected import ID {import_id}, got {imports[0].import_id}"
    assert imports[0].record_count == len(
        sample_listings
    ), f"Expected record_count {len(sample_listings)}, got {imports[0].record_count}"

    # Check that there are the correct number of listings
    listings = store.query_listings()
    assert len(listings) == len(sample_listings), f"Expected {len(sample_listings)} listings, got {len(listings)}"


def test_import_index_sequential_assignment(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that import_index is assigned sequentially within each import batch.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings
    import_id = "test-import-1"
    store.insert_listings(sample_listings, import_id)

    # Query all listings and check import_index assignment
    listings = store.query_listings()
    assert len(listings) == len(sample_listings), f"Expected {len(sample_listings)} listings, got {len(listings)}"

    # Check that all listings have the correct import_id
    for listing in listings:
        assert listing.import_id == import_id, f"Expected import_id {import_id}, got {listing.import_id}"
        assert listing.import_index is not None, "import_index should not be None"
        assert listing.import_index >= 1, f"import_index should be >= 1, got {listing.import_index}"
        assert listing.import_index <= len(
            sample_listings
        ), f"import_index should be <= {len(sample_listings)}, got {listing.import_index}"

    # Check that import_index values are unique and sequential
    import_indices = [listing.import_index for listing in listings]
    import_indices.sort()
    expected_indices = list(range(1, len(sample_listings) + 1))
    assert import_indices == expected_indices, f"Expected sequential indices {expected_indices}, got {import_indices}"


def test_query_by_import_id(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that querying by import_id works correctly.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert listings with two different import IDs
    import_id_1 = "test-import-1"
    import_id_2 = "test-import-2"
    store.insert_listings(sample_listings[:2], import_id_1)
    store.insert_listings(sample_listings[2:], import_id_2)

    # Query by first import_id
    listings_1 = store.query_listings(import_id=import_id_1)
    assert len(listings_1) == 2, f"Expected 2 listings for import_id {import_id_1}, got {len(listings_1)}"
    for listing in listings_1:
        assert listing.import_id == import_id_1, f"Expected import_id {import_id_1}, got {listing.import_id}"

    # Query by second import_id
    listings_2 = store.query_listings(import_id=import_id_2)
    assert len(listings_2) == 1, f"Expected 1 listing for import_id {import_id_2}, got {len(listings_2)}"
    for listing in listings_2:
        assert listing.import_id == import_id_2, f"Expected import_id {import_id_2}, got {listing.import_id}"

    # Query by non-existent import_id
    listings_none = store.query_listings(import_id="non-existent")
    assert len(listings_none) == 0, f"Expected 0 listings for non-existent import_id, got {len(listings_none)}"


def test_multiple_imports_distinct_ids(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that multiple imports with different import_ids maintain separate import_index sequences.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert listings with different import IDs
    import_id_1 = "test-import-1"
    import_id_2 = "test-import-2"
    store.insert_listings(sample_listings[:2], import_id_1)
    store.insert_listings(sample_listings[1:], import_id_2)  # Overlapping data to test independence

    # Query by first import_id and check import_index sequence
    listings_1 = store.query_listings(import_id=import_id_1)
    assert len(listings_1) == 2, f"Expected 2 listings for import_id {import_id_1}, got {len(listings_1)}"
    indices_1 = sorted([listing.import_index for listing in listings_1])
    assert indices_1 == [1, 2], f"Expected indices [1, 2] for import_id {import_id_1}, got {indices_1}"

    # Query by second import_id and check import_index sequence
    listings_2 = store.query_listings(import_id=import_id_2)
    assert len(listings_2) == 2, f"Expected 2 listings for import_id {import_id_2}, got {len(listings_2)}"
    indices_2 = sorted([listing.import_index for listing in listings_2])
    assert indices_2 == [1, 2], f"Expected indices [1, 2] for import_id {import_id_2}, got {indices_2}"


def test_import_metadata_in_dtos(temp_db_path: str, sample_listings: List[GPUListingDTO]) -> None:
    """
    Test that import_id and import_index are properly included in returned DTOs.

    Args:
        temp_db_path: Path to a temporary SQLite database
        sample_listings: List of sample GPU listings
    """
    # Initialize the store
    store = SqliteListingStore(temp_db_path)

    # Insert the listings
    import_id = "test-import-metadata"
    store.insert_listings(sample_listings, import_id)

    # Query all listings and verify metadata fields
    listings = store.query_listings()
    assert len(listings) == len(sample_listings), f"Expected {len(sample_listings)} listings, got {len(listings)}"

    for listing in listings:
        # Check that import_id is present and correct
        assert hasattr(listing, "import_id"), "GPUListingDTO should have import_id attribute"
        assert listing.import_id == import_id, f"Expected import_id {import_id}, got {listing.import_id}"

        # Check that import_index is present and valid
        assert hasattr(listing, "import_index"), "GPUListingDTO should have import_index attribute"
        assert listing.import_index is not None, "import_index should not be None"
        assert isinstance(listing.import_index, int), f"import_index should be int, got {type(listing.import_index)}"
        assert listing.import_index >= 1, f"import_index should be >= 1, got {listing.import_index}"
