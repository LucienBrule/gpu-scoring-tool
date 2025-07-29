from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from glyphd.api.models import GPUModelDTO
from glyphd.core.dependencies.gpu_models import get_gpu_models

router = APIRouter(tags=["Models"])


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
