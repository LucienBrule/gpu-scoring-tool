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


class ModelSizeConfig(BaseModel):
    """
    Configuration for model size VRAM requirements.
    """

    b7: float = Field(..., alias="7b", description="VRAM required for 7B parameter model (in GB)")
    b13: float = Field(..., alias="13b", description="VRAM required for 13B parameter model (in GB)")
    b70: float = Field(..., alias="70b", description="VRAM required for 70B parameter model (in GB)")

    class Config:
        """Pydantic model configuration."""

        allow_population_by_field_name = True


class QuantizationCapacityConfig(HeuristicConfig):
    """
    Configuration for the quantization capacity heuristic.

    This model defines the parameters for calculating how many models of different sizes
    can fit on a GPU based on its VRAM.
    """

    overhead_gb: float = Field(2.0, description="VRAM overhead in GB (reserved for system)")
    models: ModelSizeConfig = Field(..., description="VRAM requirements for different model sizes (in GB)")

    class Config:
        """Pydantic model configuration."""

        schema_extra = {"example": {"overhead_gb": 2.0, "models": {"7b": 3.5, "13b": 6.5, "70b": 35.0}}}
