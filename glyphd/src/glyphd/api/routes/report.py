from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from glyphd.api.models import ReportDTO
from glyphd.core.dependencies.insight_report import get_insight_report

router = APIRouter(tags=["Report"])


@router.get(
    "/report",
    response_model=ReportDTO,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
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
