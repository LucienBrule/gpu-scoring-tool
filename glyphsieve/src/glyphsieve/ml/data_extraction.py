"""
Data extraction and labeling for GPU binary classification.

This module handles reading normalized CSV data, applying binary labeling logic
for NVIDIA GPUs, and preparing clean training datasets.
"""

import logging
from typing import Any, Dict, Tuple

import pandas as pd

from glyphsieve.core.normalization import CANONICAL_MODELS

logger = logging.getLogger(__name__)


def is_nvidia_gpu(canonical_model: str) -> bool:
    """
    Determine if a canonical_model represents an NVIDIA GPU using shared logic.

    Args:
        canonical_model: The canonical model string from normalization

    Returns:
        True if the model is an NVIDIA GPU, False otherwise

    Logic:
        Uses the shared CANONICAL_MODELS from core.normalization to determine
        if the canonical_model is a recognized NVIDIA GPU. Returns True if
        the model exists in CANONICAL_MODELS, False if "UNKNOWN" or not found.
    """
    if not canonical_model or canonical_model == "UNKNOWN":
        return False

    # Use shared logic: if the canonical_model exists in CANONICAL_MODELS,
    # it's a recognized NVIDIA GPU
    return canonical_model in CANONICAL_MODELS


def extract_training_data(input_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Extract and prepare training data from normalized CSV.

    Args:
        input_path: Path to the stage_normalized.csv file

    Returns:
        Tuple of (training_dataframe, metadata_dict)

    The training dataframe contains columns: title, bulk_notes, is_gpu
    The metadata dict contains processing statistics.
    """
    logger.info(f"Reading normalized data from {input_path}")

    # Read the CSV file
    df = pd.read_csv(input_path)
    total_rows = len(df)
    logger.info(f"Loaded {total_rows} rows from normalized data")

    # Check required columns exist
    required_columns = ["title", "bulk_notes", "canonical_model"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Apply binary labeling logic
    df["is_gpu"] = df["canonical_model"].apply(is_nvidia_gpu).astype(int)

    # Data quality checks - remove rows with missing title or bulk_notes
    initial_count = len(df)
    df_clean = df.dropna(subset=["title", "bulk_notes"])

    # Also remove rows with empty strings
    df_clean = df_clean[(df_clean["title"].str.strip() != "") & (df_clean["bulk_notes"].str.strip() != "")]

    final_count = len(df_clean)
    skipped_rows = initial_count - final_count

    logger.info(f"Removed {skipped_rows} rows with missing/empty title or bulk_notes")
    logger.info(f"Final dataset size: {final_count} rows")

    # Calculate class distribution
    gpu_count = df_clean["is_gpu"].sum()
    non_gpu_count = final_count - gpu_count
    gpu_ratio = gpu_count / final_count if final_count > 0 else 0

    logger.info(f"Class distribution - GPU: {gpu_count} ({gpu_ratio:.2%}), Non-GPU: {non_gpu_count}")

    # Prepare training dataset with only required columns
    training_df = df_clean[["title", "bulk_notes", "is_gpu"]].copy()

    # Prepare metadata
    metadata = {
        "total_rows_processed": total_rows,
        "rows_after_cleaning": final_count,
        "skipped_rows": skipped_rows,
        "gpu_count": int(gpu_count),
        "non_gpu_count": int(non_gpu_count),
        "gpu_ratio": float(gpu_ratio),
        "label_spec_version": "v1.0",
    }

    return training_df, metadata


def validate_training_data(df: pd.DataFrame) -> None:
    """
    Validate the training dataset format and content.

    Args:
        df: Training dataframe to validate

    Raises:
        ValueError: If validation fails
    """
    # Check required columns
    expected_columns = ["title", "bulk_notes", "is_gpu"]
    if list(df.columns) != expected_columns:
        raise ValueError(f"Expected columns {expected_columns}, got {list(df.columns)}")

    # Check data types
    if df["is_gpu"].dtype not in ["int64", "int32"]:
        raise ValueError(f"is_gpu column should be integer, got {df['is_gpu'].dtype}")

    # Check binary values
    unique_labels = set(df["is_gpu"].unique())
    if not unique_labels.issubset({0, 1}):
        raise ValueError(f"is_gpu should only contain 0 and 1, got {unique_labels}")

    # Check for missing values
    if df.isnull().any().any():
        raise ValueError("Training data should not contain missing values")

    # Check for empty strings
    if (df["title"].str.strip() == "").any() or (df["bulk_notes"].str.strip() == "").any():
        raise ValueError("Training data should not contain empty strings")

    logger.info("Training data validation passed")
