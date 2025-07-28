import logging
from pathlib import Path
from typing import List, cast

from glyphd.api.models import GPUListingDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext

logger = logging.getLogger(__name__)


def load_scored_listings(path: Path) -> List[GPUListingDTO]:
    """
    Load scored GPU listings from a CSV file using GlyphdResourceContext.

    Args:
        path: Path to the scored.csv file

    Returns:
        List of GPUListingDTO objects
    """
    logger.info(f"Loading GPU listings from {path}")
    context = GlyphdResourceContext()
    return cast(List[GPUListingDTO], context.load(GPUListingDTO, path.name))
