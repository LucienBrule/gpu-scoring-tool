"""
Loader module for glyphd.

This module provides functions to load pipeline outputs from the filesystem into in-memory DTOs,
ready to be served via API endpoints.
"""

import csv
import json
import logging
from pathlib import Path
from typing import List

from pydantic import ValidationError

from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO
from glyphsieve.core.resources.yaml_loader import YamlLoader
from glyphsieve.models.gpu import GPURegistry
from glyphsieve.models.scoring_weights import ScoringWeights

# Set up logging
logger = logging.getLogger(__name__)


def load_scored_listings(path: Path) -> List[GPUListingDTO]:
    """
    Load scored GPU listings from a CSV file.

    Args:
        path: Path to the scored.csv file

    Returns:
        List of GPUListingDTO objects

    Raises:
        FileNotFoundError: If the file does not exist
        ValidationError: If the data does not match the expected schema
    """
    if not path.exists():
        logger.error(f"Scored listings file not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    listings = []
    try:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert types and handle potential missing or malformed fields
                try:
                    listing = GPUListingDTO(
                        canonical_model=row.get("canonical_model", ""),
                        vram_gb=int(row.get("vram_gb", 0)),
                        mig_support=int(row.get("mig_support", 0)),
                        nvlink=str(row.get("nvlink", "False")).lower() == "true",
                        tdp_watts=int(row.get("tdp_watts", 0)),
                        price=float(row.get("price", 0.0)),
                        score=float(row.get("score", 0.0)),
                    )
                    listings.append(listing)
                except (ValueError, ValidationError) as e:
                    logger.warning(f"Skipping invalid listing row: {row}. Error: {e}")
                    continue
    except Exception as e:
        logger.error(f"Error loading scored listings: {e}")
        raise

    logger.info(f"Loaded {len(listings)} GPU listings from {path}")
    return listings


def load_gpu_model_metadata(path: Path) -> List[GPUModelDTO]:
    """
    Load GPU model metadata from a CSV file.

    Args:
        path: Path to the Final_Market_Value_GPU_Summary.csv file

    Returns:
        List of GPUModelDTO objects

    Raises:
        FileNotFoundError: If the file does not exist
        ValidationError: If the data does not match the expected schema
    """
    if not path.exists():
        logger.error(f"GPU model metadata file not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    # Also load GPU specs from YAML if available
    gpu_specs = {}
    try:
        # Use YamlLoader to load GPU specs
        loader = YamlLoader()
        gpu_registry = loader.load(GPURegistry, "gpu_specs.yaml")

        # Convert the registry to a dictionary for easier lookup
        for gpu in gpu_registry.gpus:
            canonical_model = gpu.canonical_model
            if canonical_model:
                gpu_specs[canonical_model] = {
                    "vram_gb": gpu.vram_gb,
                    "tdp_watts": gpu.tdp_watts,
                    "mig_support": gpu.mig_support,
                    "nvlink": gpu.nvlink,
                    "generation": gpu.generation,
                    "cuda_cores": gpu.cuda_cores,
                    "slot_width": gpu.slot_width,
                    "pcie_generation": gpu.pcie_generation,
                }
        logger.info(f"Loaded specs for {len(gpu_specs)} GPU models using YamlLoader")
    except Exception as e:
        logger.warning(f"Error loading GPU specs: {e}. Will continue with market data only.")

    models = []
    try:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Extract market data
                    model_name = row.get("Model", "")

                    # Try to find matching specs
                    canonical_model = model_name.replace(" ", "_").upper()
                    specs = gpu_specs.get(canonical_model, {})

                    # Create model DTO
                    model = GPUModelDTO(
                        model=model_name,
                        listing_count=int(row.get("Listing_Count", 0)),
                        min_price=float(row.get("Min_Price", 0.0)),
                        median_price=float(row.get("Median_Price", 0.0)),
                        max_price=float(row.get("Max_Price", 0.0)),
                        avg_price=float(row.get("Avg_Price", 0.0)),
                        **specs,  # Add any matching specs
                    )
                    models.append(model)
                except (ValueError, ValidationError) as e:
                    logger.warning(f"Skipping invalid model row: {row}. Error: {e}")
                    continue
    except Exception as e:
        logger.error(f"Error loading GPU model metadata: {e}")
        raise

    logger.info(f"Loaded metadata for {len(models)} GPU models from {path}")
    return models


def load_insight_report(path: Path) -> ReportDTO:
    """
    Load GPU market insight report from a markdown or JSON file.

    Args:
        path: Path to the insight.md or insight.json file

    Returns:
        ReportDTO object

    Raises:
        FileNotFoundError: If the file does not exist
        ValidationError: If the data does not match the expected schema
    """
    if not path.exists():
        logger.error(f"Insight report file not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    # Check if this is a JSON file
    if path.suffix.lower() == ".json":
        try:
            with open(path, "r") as f:
                data = json.load(f)
                report = ReportDTO(**data)
                logger.info(f"Loaded insight report from JSON: {path}")
                return report
        except Exception as e:
            logger.error(f"Error loading insight report from JSON: {e}")
            raise

    # Otherwise, assume it's a markdown file
    try:
        with open(path, "r") as f:
            markdown_content = f.read()

        # Extract summary stats from the markdown
        summary_stats = {}
        for line in markdown_content.split("\n"):
            if line.startswith("- **") and ":**" in line:
                key = line.split("**")[1].strip().lower().replace(" ", "_")
                value = line.split(":**")[1].strip()
                summary_stats[key] = value

        # Extract top ranked models
        top_ranked = []
        in_top_section = False
        for line in markdown_content.split("\n"):
            if "## 🏆 Top 10 Cards by Score" in line:
                in_top_section = True
                continue
            if in_top_section and line.startswith("| "):
                if "---" in line:
                    continue
                if "Rank" in line and "Model" in line:
                    continue
                parts = line.split("|")
                if len(parts) >= 3:
                    model = parts[2].strip()
                    top_ranked.append(model)
            if in_top_section and line.startswith("##"):
                break

        # Load scoring weights
        scoring_weights = {
            "vram_weight": 0.0,
            "mig_weight": 0.0,
            "nvlink_weight": 0.0,
            "tdp_weight": 0.0,
            "price_weight": 0.0,
        }

        try:
            # Use YamlLoader to load scoring weights
            loader = YamlLoader()
            weights = loader.load(ScoringWeights, "scoring_weights.yaml")
            scoring_weights = {
                "vram_weight": weights.vram_weight,
                "mig_weight": weights.mig_weight,
                "nvlink_weight": weights.nvlink_weight,
                "tdp_weight": weights.tdp_weight,
                "price_weight": weights.price_weight,
            }
            logger.info("Loaded scoring weights using YamlLoader")
        except Exception as e:
            logger.warning(f"Error loading scoring weights: {e}. Using defaults.")

        # Create report DTO
        report = ReportDTO(
            markdown=markdown_content,
            summary_stats=summary_stats,
            top_ranked=top_ranked,
            scoring_weights=scoring_weights,
        )

        logger.info(f"Loaded insight report from markdown: {path}")
        return report
    except Exception as e:
        logger.error(f"Error loading insight report: {e}")
        raise
