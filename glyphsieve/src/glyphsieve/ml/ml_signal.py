"""
ML Signal Module

This module provides ML-based GPU classification signals for the normalization pipeline.
It uses configurable parameters loaded from YAML configuration files.
"""

from typing import Optional, Tuple

from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.ml_config import MLConfig


def predict_is_gpu(title: str, bulk_notes: str, threshold: Optional[float] = None) -> Tuple[bool, float]:
    """
    Predict if a listing is an NVIDIA GPU using the configured ML model.

    This function loads the ML configuration and delegates to the predictor module
    while respecting the configuration settings.

    Args:
        title (str): Listing title
        bulk_notes (str): Supplemental notes
        threshold (float, optional): Confidence threshold. If None, uses config value

    Returns:
        tuple:
            - is_gpu (bool): True if confidence >= threshold
            - score (float): Model probability that listing is an NVIDIA GPU (0.0 - 1.0)

    Notes:
        - If ML is disabled in config, returns (False, 0.0)
        - Text will be lowercased and concatenated as input to the model
        - Will fallback to (False, 0.0) if model is unavailable
    """
    # Load ML configuration
    config = _load_ml_config()

    # Check if ML is enabled
    if not config.enabled:
        return False, 0.0

    # Use config threshold if not provided
    if threshold is None:
        threshold = config.threshold

    # Import predictor here to avoid circular imports and performance impact when ML is disabled
    from glyphsieve.ml.predictor import predict_is_gpu as _predict_is_gpu

    return _predict_is_gpu(title, bulk_notes, threshold)


def _load_ml_config() -> MLConfig:
    """
    Load ML configuration from YAML file.

    Returns:
        MLConfig: The loaded configuration
    """
    loader = GlyphSieveYamlLoader()
    return loader.load(MLConfig, "configs/ml_config.yaml")
