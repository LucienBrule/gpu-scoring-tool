"""
FastAPI route for importing enriched CSV from glyphsieve pipeline output.
"""

import csv
import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from glyphd.api.models import GPUListingDTO, ImportResultDTO, PipelineImportRequestDTO
from glyphd.core.dependencies.storage import get_storage_engine
from glyphd.core.storage.sqlite_store import SqliteListingStore

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/imports",
    tags=["Persist"],
)


@router.post(
    "/from-pipeline",
    response_model=ImportResultDTO,
    summary="Import enriched CSV from glyphsieve pipeline output",
    description="Import a fully normalized and enriched CSV from the glyphsieve pipeline into the SQLite database",
)
def import_from_pipeline(
    request: PipelineImportRequestDTO,
    storage: SqliteListingStore = Depends(get_storage_engine),
) -> ImportResultDTO:
    """
    Import enriched CSV from glyphsieve pipeline output.

    Args:
        request: Pipeline import request with CSV path and metadata
        storage: SQLite storage engine (injected dependency)

    Returns:
        ImportResultDTO: Metadata about the import operation

    Raises:
        HTTPException: If the import fails or if the CSV is malformed
    """
    csv_path = Path(request.input_csv_path)
    
    # Validate CSV file exists
    if not csv_path.exists():
        raise HTTPException(
            status_code=422, 
            detail=f"CSV file not found: {request.input_csv_path}"
        )
    
    # Generate unique import ID
    import_id = str(uuid.uuid4())
    timestamp = datetime.now(UTC)
    
    try:
        # Parse CSV and convert to GPUListingDTO objects
        listings = _parse_pipeline_csv(csv_path, import_id)
        
        if not listings:
            raise HTTPException(
                status_code=422, 
                detail="No valid listings found in CSV file"
            )
        
        # Extract model names for first/last tracking
        models = [listing.canonical_model for listing in listings]
        first_model = models[0]
        last_model = models[-1]
        
        # Insert listings into storage
        record_count = storage.insert_listings(listings, import_id)
        
        logger.info(
            f"Successfully imported {record_count} listings from pipeline CSV "
            f"'{request.input_csv_path}' with import_id: {import_id}"
        )
        
        return ImportResultDTO(
            import_id=uuid.UUID(import_id),
            record_count=record_count,
            first_model=first_model,
            last_model=last_model,
            timestamp=timestamp,
        )
        
    except Exception as e:
        logger.error(f"Failed to import pipeline CSV '{request.input_csv_path}': {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to import pipeline CSV: {e!s}"
        )


def _parse_pipeline_csv(csv_path: Path, import_id: str) -> List[GPUListingDTO]:
    """
    Parse pipeline output CSV and convert to GPUListingDTO objects.
    
    Args:
        csv_path: Path to the CSV file
        import_id: Import batch ID
        
    Returns:
        List of GPUListingDTO objects
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    listings = []
    required_fields = {
        'canonical_model', 'vram_gb', 'mig_support', 'nvlink', 
        'tdp_watts', 'price', 'score'
    }
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate required fields exist in CSV
            if not required_fields.issubset(set(reader.fieldnames or [])):
                missing_fields = required_fields - set(reader.fieldnames or [])
                raise ValueError(f"Missing required fields in CSV: {missing_fields}")
            
            for index, row in enumerate(reader):
                try:
                    # Convert string values to appropriate types
                    listing = GPUListingDTO(
                        canonical_model=row['canonical_model'],
                        vram_gb=int(row['vram_gb']),
                        mig_support=int(row['mig_support']),
                        nvlink=row['nvlink'].lower() in ('true', '1', 'yes'),
                        tdp_watts=int(row['tdp_watts']),
                        price=float(row['price']),
                        score=float(row['score']),
                        import_id=import_id,
                        import_index=index,
                    )
                    listings.append(listing)
                    
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid row {index} in CSV: {e}")
                    continue
                    
    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {csv_path}")
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {e}")
    
    return listings