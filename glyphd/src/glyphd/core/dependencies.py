"""
Dependency injection module for glyphd.

This module provides dependencies for the FastAPI application,
including data loaders and configuration.
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from fastapi import Depends

from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO
from glyphd.core.loader import (
    load_gpu_model_metadata,
    load_insight_report,
    load_scored_listings,
)

# Set up logging
logger = logging.getLogger(__name__)

# Default paths for data files
DEFAULT_SCORED_LISTINGS_PATH = Path("scored_sample.csv")
DEFAULT_GPU_MODEL_METADATA_PATH = Path("sieveviz/Final_Market_Value_GPU_Summary.csv")
DEFAULT_INSIGHT_REPORT_DIR = Path("reports")


@lru_cache
def get_scored_listings_path() -> Path:
    """
    Get the path to the scored listings file.

    Returns:
        Path: The path to the scored listings file
    """
    return DEFAULT_SCORED_LISTINGS_PATH


@lru_cache
def get_gpu_model_metadata_path() -> Path:
    """
    Get the path to the GPU model metadata file.

    Returns:
        Path: The path to the GPU model metadata file
    """
    return DEFAULT_GPU_MODEL_METADATA_PATH


@lru_cache
def get_insight_report_path() -> Path:
    """
    Get the path to the latest insight report file.

    Returns:
        Path: The path to the latest insight report file
    """
    # Find the latest report directory
    try:
        reports_dir = DEFAULT_INSIGHT_REPORT_DIR
        latest_dir = sorted(list(reports_dir.glob("*")))[-1]
        insight_path = latest_dir / "insight.md"
        return insight_path
    except (IndexError, FileNotFoundError):
        logger.warning(f"No insight report found in {DEFAULT_INSIGHT_REPORT_DIR}")
        # Return a default path that will be handled by the loader
        return DEFAULT_INSIGHT_REPORT_DIR / "latest" / "insight.md"


@lru_cache
def get_gpu_listings(path: Path = Depends(get_scored_listings_path)) -> List[GPUListingDTO]:
    """
    Load GPU listings from the scored listings file.

    Args:
        path: Path to the scored listings file

    Returns:
        List of GPUListingDTO objects
    """
    try:
        return load_scored_listings(path)
    except FileNotFoundError:
        logger.warning(f"Scored listings file not found: {path}")
        return []
    except Exception as e:
        logger.error(f"Error loading scored listings: {e}")
        return []


@lru_cache
def get_gpu_models(path: Path = Depends(get_gpu_model_metadata_path)) -> List[GPUModelDTO]:
    """
    Load GPU models from the GPU model metadata file.

    Args:
        path: Path to the GPU model metadata file

    Returns:
        List of GPUModelDTO objects
    """
    try:
        return load_gpu_model_metadata(path)
    except FileNotFoundError:
        logger.warning(f"GPU model metadata file not found: {path}")
        return []
    except Exception as e:
        logger.error(f"Error loading GPU model metadata: {e}")
        return []


@lru_cache
def get_insight_report(path: Path = Depends(get_insight_report_path)) -> Optional[ReportDTO]:
    """
    Load the insight report from the latest insight report file.

    Args:
        path: Path to the insight report file

    Returns:
        ReportDTO object or None if the file is not found
    """
    try:
        return load_insight_report(path)
    except FileNotFoundError:
        logger.warning(f"Insight report file not found: {path}")
        return None
    except Exception as e:
        logger.error(f"Error loading insight report: {e}")
        return None
