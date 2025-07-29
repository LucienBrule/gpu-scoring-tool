"""
Storage interfaces for the glyphd core.

This module defines the interfaces for storage backends used by glyphd.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from glyphd.api.models import GPUListingDTO, ImportMetadata


class ListingStore(ABC):
    """
    Interface for a storage backend that stores GPU listings.

    This interface defines the methods that must be implemented by any storage backend
    that stores GPU listings.
    """

    @abstractmethod
    def insert_listings(self, listings: List[GPUListingDTO], import_id: str) -> int:
        """
        Insert a batch of listings into the store with the given import ID.

        Args:
            listings: The listings to insert
            import_id: The ID of the import batch

        Returns:
            The number of listings inserted
        """
        pass

    @abstractmethod
    def query_listings(
        self,
        model: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        region: Optional[str] = None,
        after: Optional[datetime] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[GPUListingDTO]:
        """
        Query listings from the store with optional filters.

        Args:
            model: Filter by canonical model name (supports fuzzy matching)
            min_price: Filter by minimum price
            max_price: Filter by maximum price
            min_score: Filter by minimum score
            max_score: Filter by maximum score
            region: Filter by region
            after: Filter by listings seen after this timestamp
            limit: Maximum number of results to return
            offset: Number of results to skip for pagination

        Returns:
            A list of listings matching the filters
        """
        pass

    @abstractmethod
    def list_imports(self) -> List[ImportMetadata]:
        """
        List all import batches in the store.

        Returns:
            A list of import batch metadata
        """
        pass
