import logging
from typing import cast

from glyphd.api.models import ReportDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext

logger = logging.getLogger(__name__)


def load_insight_report() -> ReportDTO:
    """
    Load structured GPU market insight report from YAML.

    Returns:
        ReportDTO object

    Raises:
        Exception: if the file cannot be found or loaded
    """
    try:
        context = GlyphdResourceContext()
        return cast(ReportDTO, context.load(ReportDTO, "insight.yaml"))
    except Exception as e:
        logger.error(f"Error loading insight report: {e}")
        raise
