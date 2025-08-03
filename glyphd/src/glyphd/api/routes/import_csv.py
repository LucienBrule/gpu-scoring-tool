"""
FastAPI route for importing raw CSV files.
"""

import csv
import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from glyphd.api.models import ImportResultDTO
from glyphd.core.dependencies.storage import get_storage_engine
from glyphd.core.services import PipelineService
from glyphd.core.storage.sqlite_store import SqliteListingStore

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/import",
    tags=["Import"],
)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
IMPORT_BATCHES_DIR = Path("data/import_batches")




@router.post(
    "/csv",
    response_model=ImportResultDTO,
    summary="Import and process raw CSV file",
    description="Upload a raw CSV file that will be processed through the glyphsieve normalization and scoring pipeline",
)
async def import_csv(
    file: UploadFile = File(..., description="CSV file to upload"),
    storage: SqliteListingStore = Depends(get_storage_engine),
) -> ImportResultDTO:
    """
    Import and process a raw CSV file through the glyphsieve pipeline.
    
    Args:
        file: Uploaded CSV file
        storage: SQLite storage engine (injected dependency)
        
    Returns:
        ImportResultDTO: Metadata about the import operation including processed listings
        
    Raises:
        HTTPException: If file validation fails or processing errors occur
    """
    # Validate file extension
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=422,
            detail="Only CSV files are supported. Please upload a file with .csv extension."
        )
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB."
        )
    
    # Generate import ID
    import_id = str(uuid.uuid4())
    timestamp = datetime.now(UTC)
    
    try:
        # Read and validate CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Basic CSV validation
        if not csv_content.strip():
            raise HTTPException(status_code=422, detail="CSV file is empty")
        
        logger.info(f"Processing CSV '{file.filename}' with import_id: {import_id}")
        
        # Initialize pipeline service and process CSV
        pipeline_service = PipelineService()
        processed_listings = await pipeline_service.process_raw_csv(
            csv_data=csv_content,
            import_id=import_id,
            background=False  # Process synchronously for now
        )
        
        if not processed_listings:
            raise HTTPException(
                status_code=422, 
                detail="No valid GPU listings found after processing"
            )
        
        # Extract model names for tracking
        models = [listing.canonical_model for listing in processed_listings]
        first_model = models[0]
        last_model = models[-1]
        
        # Persist processed listings to database
        record_count = storage.insert_listings(processed_listings, import_id)
        
        logger.info(
            f"Successfully processed and imported {record_count} listings from '{file.filename}' "
            f"with import_id: {import_id}"
        )
        
        # Create response with actual processed data
        return ImportResultDTO(
            import_id=uuid.UUID(import_id),
            record_count=record_count,
            first_model=first_model,
            last_model=last_model,
            timestamp=timestamp,
            filename=file.filename,
            total_rows=len(processed_listings),
            valid_rows=len(processed_listings),
            invalid_rows=0,  # Pipeline handles invalid rows internally
            score_range=(
                min(listing.score for listing in processed_listings),
                max(listing.score for listing in processed_listings)
            ) if processed_listings else None,
            top_models=list(set(models[:5])),  # Top 5 unique models
        )
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Invalid file encoding. Please ensure the CSV file is UTF-8 encoded."
        )
    except Exception as e:
        logger.error(f"Failed to process CSV upload '{file.filename}': {e}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process CSV upload: {e!s}"
        )


def _validate_and_count_csv(csv_content: str) -> tuple[int, int]:
    """
    Validate CSV content and count rows.
    
    Args:
        csv_content: Raw CSV content as string
        
    Returns:
        Tuple of (valid_row_count, rejected_row_count)
        
    Raises:
        ValueError: If CSV is malformed or empty
    """
    if not csv_content.strip():
        raise ValueError("CSV file is empty")
    
    try:
        # Parse CSV and count rows
        reader = csv.DictReader(csv_content.splitlines())
        
        # Check if we have a header
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")
        
        valid_rows = 0
        rejected_rows = 0
        
        for row_num, row in enumerate(reader, start=1):
            # Basic validation - check if row has any non-empty values
            if any(value.strip() for value in row.values() if value):
                valid_rows += 1
            else:
                rejected_rows += 1
                logger.warning(f"Rejected empty row {row_num} in CSV")
        
        if valid_rows == 0:
            raise ValueError("CSV file contains no valid data rows")
        
        return valid_rows, rejected_rows
        
    except csv.Error as e:
        raise ValueError(f"Malformed CSV file: {e}")