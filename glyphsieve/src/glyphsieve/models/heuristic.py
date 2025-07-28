"""
Heuristic models for glyphsieve.

This module defines Pydantic models for heuristic configurations, including
quantization capability heuristics.
"""

from pydantic import BaseModel, Field


class HeuristicConfig(BaseModel):
    """
    Base class for heuristic configuration.

    This class should be extended by specific heuristic configurations.
    """

    pass


class QuantizationHeuristicConfig(HeuristicConfig):
    """
    Configuration for the quantization capability heuristic.

    This model defines the thresholds for classifying a GPU as quantization-capable.
    """

    min_vram_gb: int = Field(24, description="Minimum VRAM capacity in GB")
    max_tdp_watts: int = Field(300, description="Maximum Thermal Design Power in watts")
    min_mig_support: int = Field(1, description="Minimum MIG support level (0=none, 1-7=supported)")

    class Config:
        """Pydantic model configuration."""

        schema_extra = {"example": {"min_vram_gb": 24, "max_tdp_watts": 300, "min_mig_support": 1}}
