"""
FastAPI router for the glyphd API.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status

from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO
from glyphd.core.dependencies import (
    get_gpu_listings,
    get_gpu_models,
    get_insight_report,
)

# Create the API router
router = APIRouter(prefix="/api")


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Health Check",
    description="Simple health check endpoint to verify API is running",
)
async def health_check():
    """
    Health check endpoint.
    Returns a simple status message to indicate the API is running.

    Returns:
        dict: A simple status message.
    """
    return {"status": "ok"}


@router.get(
    "/listings",
    response_model=List[GPUListingDTO],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    tags=["Listings"],
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


@router.get(
    "/models",
    response_model=List[GPUModelDTO],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    tags=["Models"],
    summary="Get GPU Models",
    description="Retrieve all GPU model metadata including specifications and market data",
)
async def get_models(models: List[GPUModelDTO] = Depends(get_gpu_models)):
    """
    Get all GPU model metadata.

    Args:
        models: List of GPU models from dependency injection

    Returns:
        List[GPUModelDTO]: A list of GPU models with their metadata.
    """
    return models


@router.get(
    "/report",
    response_model=ReportDTO,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    tags=["Report"],
    summary="Get Market Insight Report",
    description="Retrieve the latest GPU market insight report with summary statistics and scoring weights",
)
async def get_report(report: Optional[ReportDTO] = Depends(get_insight_report)):
    """
    Get the latest GPU market insight report.

    Args:
        report: The insight report from dependency injection

    Returns:
        ReportDTO: The market insight report with markdown content and structured data.
    """
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    return report


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(
        title="Glyphd: GPU Market API",
        description="API service exposing enriched GPU listings, model metadata, scoring reports, and insight overlays from the glyphsieve pipeline.",
        version="0.1.0",
        contact={
            "name": "Glyphsieve Research",
            "url": "https://github.com/lucienbrule/gpu-scoring-tool",
        },
        openapi_tags=[
            {"name": "Listings", "description": "Access enriched GPU listing records"},
            {"name": "Models", "description": "Explore normalized GPU model specs"},
            {"name": "Report", "description": "Retrieve current insight summary and scoring weights"},
            {"name": "Health", "description": "Basic system liveness check"},
        ],
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Mount the API router
    app.include_router(router)

    return app
