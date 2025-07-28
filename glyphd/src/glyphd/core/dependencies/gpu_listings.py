import logging
from functools import lru_cache
from typing import List, cast

from glyphd.api.models import GPUListingDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext

logger = logging.getLogger(__name__)
resource_context = GlyphdResourceContext()


@lru_cache
def get_gpu_listings() -> List[GPUListingDTO]:
    """
    Load GPU listings from the scored listings resource.

    Returns:
        List of GPUListingDTO objects
    """
    try:
        return cast(List[GPUListingDTO], resource_context.load(GPUListingDTO, "scored_sample.csv"))
    except FileNotFoundError:
        logger.warning("Scored listings file not found: scored_sample.csv")
        return []
    except Exception as e:
        logger.error(f"Error loading scored listings: {e}")
        return []
