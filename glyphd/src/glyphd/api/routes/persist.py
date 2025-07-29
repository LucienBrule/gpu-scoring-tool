import logging
import uuid
from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from glyphd.api.models import GPUListingDTO, ImportResultDTO
from glyphd.core.dependencies.storage import get_storage_engine
from glyphd.core.storage.sqlite_store import SqliteListingStore

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/persist",
    tags=["Persist"],
)


@router.post(
    "/listings",
    response_model=ImportResultDTO,
    summary="Import GPU listings into SQLite store",
    description="Import a batch of scored GPU listings into the SQLite database",
)
def import_listings(
    listings: List[GPUListingDTO],
    storage: SqliteListingStore = Depends(get_storage_engine),
) -> ImportResultDTO:
    """
    Import a batch of GPU listings into the SQLite store.

    Args:
        listings: List of GPU listings to import
        storage: SQLite storage engine (injected dependency)

    Returns:
        ImportResultDTO: Metadata about the import operation

    Raises:
        HTTPException: If the import fails or if the payload is invalid
    """
    if not listings:
        raise HTTPException(status_code=422, detail="Empty listings array provided")

    # Generate unique import ID
    import_id = str(uuid.uuid4())
    timestamp = datetime.now(UTC)

    try:
        # Extract model names for first/last tracking
        models = [listing.canonical_model for listing in listings]
        first_model = models[0]
        last_model = models[-1]

        # Insert listings into storage
        record_count = storage.insert_listings(listings, import_id)

        logger.info(f"Successfully imported {record_count} listings with import_id: {import_id}")

        return ImportResultDTO(
            import_id=uuid.UUID(import_id),
            record_count=record_count,
            first_model=first_model,
            last_model=last_model,
            timestamp=timestamp,
        )

    except Exception as e:
        logger.error(f"Failed to import listings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to import listings: {e!s}")
