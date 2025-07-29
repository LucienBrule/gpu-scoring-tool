from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from glyphd.api.models import GPUListingDTO
from glyphd.core.dependencies.gpu_listings import get_gpu_listings

router = APIRouter(tags=["Listings"])


@router.get(
    "/listings",
    response_model=List[GPUListingDTO],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Get GPU Listings",
    description="Retrieve all GPU listings with optional filtering by model and quantization capability",
)
async def get_listings(
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
