"""
Train/test splitting functionality for GPU classification datasets.

This module provides stratified splitting to maintain class balance
across training and test sets.
"""

import logging
from typing import Any, Dict, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

# Default random seed for reproducibility
DEFAULT_RANDOM_SEED = 42


def stratified_split(
    df: pd.DataFrame, test_size: float = 0.2, random_seed: int = DEFAULT_RANDOM_SEED
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Perform stratified train/test split on the dataset.

    Args:
        df: DataFrame with columns ['title', 'bulk_notes', 'is_gpu']
        test_size: Fraction of data to use for test set (default 0.2 for 80/20 split)
        random_seed: Random seed for reproducibility

    Returns:
        Tuple of (train_df, test_df, split_metadata)

    The split maintains class balance within 2% tolerance.
    """
    logger.info(f"Performing stratified {int((1-test_size)*100)}/{int(test_size*100)} split")

    # Validate input
    if "is_gpu" not in df.columns:
        raise ValueError("DataFrame must contain 'is_gpu' column for stratification")

    total_samples = len(df)
    if total_samples == 0:
        raise ValueError("Cannot split empty dataset")

    # Calculate original class distribution
    original_gpu_ratio = df["is_gpu"].mean()
    logger.info(f"Original GPU ratio: {original_gpu_ratio:.4f}")

    # Perform stratified split
    X = df[["title", "bulk_notes"]]
    y = df["is_gpu"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_seed)

    # Reconstruct DataFrames
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    # Calculate split statistics
    train_size = len(train_df)
    test_size_actual = len(test_df)
    train_gpu_ratio = train_df["is_gpu"].mean()
    test_gpu_ratio = test_df["is_gpu"].mean()

    # Check class balance preservation
    balance_diff_train = abs(train_gpu_ratio - original_gpu_ratio)
    balance_diff_test = abs(test_gpu_ratio - original_gpu_ratio)
    max_balance_diff = max(balance_diff_train, balance_diff_test)

    logger.info(f"Train set: {train_size} samples, GPU ratio: {train_gpu_ratio:.4f}")
    logger.info(f"Test set: {test_size_actual} samples, GPU ratio: {test_gpu_ratio:.4f}")
    logger.info(f"Maximum balance difference: {max_balance_diff:.4f}")

    # Warn if balance difference exceeds 2%
    if max_balance_diff > 0.02:
        logger.warning(f"Class balance difference ({max_balance_diff:.4f}) exceeds 2% threshold")

    # Prepare metadata
    split_metadata = {
        "total_samples": total_samples,
        "train_size": train_size,
        "test_size": test_size_actual,
        "train_test_ratio": f"{int((1-test_size)*100)}/{int(test_size*100)}",
        "original_gpu_ratio": float(original_gpu_ratio),
        "train_gpu_ratio": float(train_gpu_ratio),
        "test_gpu_ratio": float(test_gpu_ratio),
        "max_balance_difference": float(max_balance_diff),
        "random_seed": random_seed,
        "balance_preserved": max_balance_diff <= 0.02,
    }

    return train_df, test_df, split_metadata


def validate_split_balance(train_df: pd.DataFrame, test_df: pd.DataFrame, tolerance: float = 0.02) -> bool:
    """
    Validate that the train/test split maintains class balance.

    Args:
        train_df: Training dataset
        test_df: Test dataset
        tolerance: Maximum allowed difference in class ratios (default 2%)

    Returns:
        True if balance is preserved within tolerance, False otherwise
    """
    train_gpu_ratio = train_df["is_gpu"].mean()
    test_gpu_ratio = test_df["is_gpu"].mean()

    balance_diff = abs(train_gpu_ratio - test_gpu_ratio)

    logger.info(f"Train GPU ratio: {train_gpu_ratio:.4f}")
    logger.info(f"Test GPU ratio: {test_gpu_ratio:.4f}")
    logger.info(f"Balance difference: {balance_diff:.4f}")

    is_balanced = balance_diff <= tolerance

    if not is_balanced:
        logger.warning(f"Split balance check failed: difference {balance_diff:.4f} > tolerance {tolerance}")
    else:
        logger.info("Split balance check passed")

    return is_balanced


def get_split_summary(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a summary of the train/test split.

    Args:
        train_df: Training dataset
        test_df: Test dataset

    Returns:
        Dictionary with split summary statistics
    """
    total_samples = len(train_df) + len(test_df)

    train_gpu_count = train_df["is_gpu"].sum()
    train_non_gpu_count = len(train_df) - train_gpu_count
    test_gpu_count = test_df["is_gpu"].sum()
    test_non_gpu_count = len(test_df) - test_gpu_count

    summary = {
        "total_samples": total_samples,
        "train_samples": len(train_df),
        "test_samples": len(test_df),
        "train_gpu_count": int(train_gpu_count),
        "train_non_gpu_count": int(train_non_gpu_count),
        "test_gpu_count": int(test_gpu_count),
        "test_non_gpu_count": int(test_non_gpu_count),
        "train_gpu_ratio": float(train_df["is_gpu"].mean()),
        "test_gpu_ratio": float(test_df["is_gpu"].mean()),
    }

    return summary
