import logging
from functools import lru_cache
from typing import Optional, cast

from glyphd.api.models import ReportDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext

logger = logging.getLogger(__name__)
resource_context = GlyphdResourceContext()


@lru_cache
def get_insight_report() -> Optional[ReportDTO]:
    """
    Load the insight report from the latest insight report file.

    Returns:
        ReportDTO object or None if the file is not found
    """
    try:
        return cast(ReportDTO, resource_context.load(ReportDTO, "insight.yaml"))
    except FileNotFoundError:
        logger.warning("Insight report not found: insight.yaml")
        return None
    except Exception as e:
        logger.error(f"Error loading insight report: {e}")
        return None
