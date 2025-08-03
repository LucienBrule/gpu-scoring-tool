"""
ML Configuration Model

This module defines the Pydantic model for ML inference configuration.
"""

from pydantic import BaseModel, Field


class MLConfig(BaseModel):
    """
    Configuration model for ML-based GPU classification inference.

    This model defines the parameters used for ML inference during
    the normalization process.
    """

    model_path: str = Field(description="Path to the trained ML model file (relative to glyphsieve resources)")

    threshold: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for ML predictions (0.0 - 1.0). "
        "Predictions with confidence >= threshold will be classified as GPU",
    )

    enabled: bool = Field(
        default=True, description="Whether ML inference is enabled. If false, ML stage will be skipped entirely"
    )
