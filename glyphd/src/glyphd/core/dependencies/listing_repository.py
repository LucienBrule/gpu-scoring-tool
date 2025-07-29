"""
Dependency injection for listing repository.
"""

import os
from functools import lru_cache

from glyphd.core.storage.interface import ListingStore
from glyphd.core.storage.sqlite_store import SqliteListingStore


@lru_cache
def get_listing_repository() -> ListingStore:
    """
    Get the listing repository instance.

    Returns:
        ListingStore: The listing repository instance
    """
    # Get database path from environment or use default
    db_path = os.getenv("GLYPHD_DB_PATH", "data/gpu.sqlite")

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    return SqliteListingStore(db_path)
