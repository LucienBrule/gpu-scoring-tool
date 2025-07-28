import logging
from functools import lru_cache
from typing import List, cast

from glyphd.api.models import GPUModelDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext

logger = logging.getLogger(__name__)
resource_context = GlyphdResourceContext()


@lru_cache
def get_gpu_models() -> List[GPUModelDTO]:
    """
    Load GPU models from the GPU model metadata file.

    Returns:
        List of GPUModelDTO objects
    """
    try:
        return cast(List[GPUModelDTO], resource_context.load(GPUModelDTO, "market_value_gpu_summary.csv"))
    except FileNotFoundError:
        logger.warning("GPU model metadata file not found: market_value_gpu_summary.csv")
        return []
    except Exception as e:
        logger.error(f"Error loading GPU model metadata: {e}")
        return []
