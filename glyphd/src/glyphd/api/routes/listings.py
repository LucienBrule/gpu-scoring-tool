from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from glyphd.api.models import GPUListingDTO
from glyphd.core.dependencies.gpu_listings import get_gpu_listings
from glyphd.core.dependencies.listing_repository import get_listing_repository
from glyphd.core.storage.interface import ListingStore

router = APIRouter(tags=["Listings"])


@router.get(
    "/listings/legacy",
    response_model=List[GPUListingDTO],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Get GPU Listings (Legacy)",
    description=(
        "Retrieve all GPU listings with optional filtering by model and quantization capability (legacy endpoint)"
    ),
)
async def get_listings_legacy(
    model: Optional[str] = Query(None, description="Filter by exact model name"),
    quantized: Optional[bool] = Query(None, description="Filter by quantization capability"),
    listings: List[GPUListingDTO] = Depends(get_gpu_listings),
):
    """
    Get all GPU listings with optional filtering.

    Args:
        model: Optional filter by exact model name
        quantized: Optional filter by quantization capability
        listings: List of GPU listings from dependency injection

    Returns:
        List[GPUListingDTO]: A list of GPU listings.
    """
    # Apply filters
    filtered_listings = []
    for listing in listings:
        # Filter by model
        if model and listing.canonical_model != model:
            continue

        # For quantized filter, we'll consider MIG support > 0 as quantized
        if quantized is not None:
            is_quantized = listing.mig_support > 0
            if is_quantized != quantized:
                continue

        filtered_listings.append(listing)

    return filtered_listings


@router.get(
    "/listings",
    response_model=List[GPUListingDTO],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Query GPU Listings from Database",
    description="Retrieve GPU listings from SQLite database with filtering, fuzzy matching, and pagination",
)
async def get_listings(
    model: Optional[str] = Query(None, description="Filter by model name (supports fuzzy matching)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    import_id: Optional[str] = Query(None, description="Filter by import batch ID"),
    limit: Optional[int] = Query(100, ge=1, le=1000, description="Maximum number of results (default: 100, max: 1000)"),
    offset: Optional[int] = Query(0, ge=0, description="Number of results to skip for pagination"),
    store: ListingStore = Depends(get_listing_repository),
):
    """
    Query GPU listings from the SQLite database with optional filtering and pagination.

    Args:
        model: Optional filter by model name (supports fuzzy matching)
        min_price: Optional minimum price filter
        max_price: Optional maximum price filter
        import_id: Optional filter by import batch ID
        limit: Maximum number of results to return (default: 100, max: 1000)
        offset: Number of results to skip for pagination
        store: Listing repository from dependency injection

    Returns:
        List[GPUListingDTO]: A list of GPU listings matching the filters.

    Raises:
        HTTPException: 400 for invalid query parameters
    """
    try:
        # Validate price range
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="min_price cannot be greater than max_price"
            )

        # Query the store
        listings = store.query_listings(
            model=model,
            min_price=min_price,
            max_price=max_price,
            import_id=import_id,
            limit=limit,
            offset=offset,
        )

        return listings

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid query parameters: {e!s}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e!s}")
