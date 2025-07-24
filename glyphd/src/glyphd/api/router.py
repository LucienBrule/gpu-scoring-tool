"""
FastAPI router for the glyphd API.
"""
from typing import List, Optional
from fastapi import APIRouter, FastAPI, Query, HTTPException, status, Depends

from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO
from glyphd.core.dependencies import get_gpu_listings, get_gpu_models, get_insight_report

# Create the API router
router = APIRouter(prefix="/api")

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    Returns a simple status message to indicate the API is running.

    Returns:
        dict: A simple status message.
    """
    return {"status": "ok"}

@router.get("/listings", response_model=List[GPUListingDTO], status_code=status.HTTP_200_OK, tags=["GPU Data"])
async def get_listings(
    model: Optional[str] = Query(None, description="Filter by exact model name"),
    quantized: Optional[bool] = Query(None, description="Filter by quantization capability"),
    listings: List[GPUListingDTO] = Depends(get_gpu_listings)
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

@router.get("/models", response_model=List[GPUModelDTO], status_code=status.HTTP_200_OK, tags=["GPU Data"])
async def get_models(
    models: List[GPUModelDTO] = Depends(get_gpu_models)
):
    """
    Get all GPU model metadata.

    Args:
        models: List of GPU models from dependency injection

    Returns:
        List[GPUModelDTO]: A list of GPU models with their metadata.
    """
    return models

@router.get("/report", response_model=ReportDTO, status_code=status.HTTP_200_OK, tags=["Reports"])
async def get_report(
    report: Optional[ReportDTO] = Depends(get_insight_report)
):
    """
    Get the latest GPU market insight report.

    Args:
        report: The insight report from dependency injection

    Returns:
        ReportDTO: The market insight report with markdown content and structured data.
    """
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return report

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(
        title="GlyphD API",
        description="API for GPU scoring and market analysis",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Mount the API router
    app.include_router(router)

    return app
