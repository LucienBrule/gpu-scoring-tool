import logging
import os
from functools import lru_cache

from glyphd.core.storage.sqlite_store import SqliteListingStore

logger = logging.getLogger(__name__)


@lru_cache
def get_storage_engine() -> SqliteListingStore:
    """
    Get the SQLite storage engine instance.

    Returns:
        SqliteListingStore: The configured storage engine instance
    """
    # Get database path from environment or use default
    db_path = os.getenv("GLYPHD_DB_PATH", "data/gpu.sqlite")

    try:
        return SqliteListingStore(db_path=db_path)
    except Exception as e:
        logger.error(f"Error creating storage engine: {e}")
        raise
