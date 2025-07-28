from fastapi import APIRouter
from starlette import status

from glyphd.api.models.health_status import HealthStatus

router = APIRouter( tags=["Health"])


@router.get(
    "/health",
    response_model=HealthStatus,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Simple health check endpoint to verify API is running",
)
async def health_check() -> HealthStatus:
    """
    Health check endpoint.
    Returns a simple status message to indicate the API is running.

    Returns:
        HealthStatus: A simple status message.
    """
    return HealthStatus(status="ok")
