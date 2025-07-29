"""
Quantization capacity models for glyphsieve.

This module defines Pydantic models for quantization capacity, including the number of models
of different sizes that can fit on a GPU based on its VRAM.
"""

from pydantic import BaseModel, Field


class QuantizationCapacitySpec(BaseModel):
    """
    Pydantic model for quantization capacity.

    This model defines the number of models of different sizes (7B, 13B, 70B) that can fit
    on a GPU based on its VRAM.
    """

    model_7b: int = Field(..., alias="7b", description="Number of 7B parameter models that can fit")
    model_13b: int = Field(..., alias="13b", description="Number of 13B parameter models that can fit")
    model_70b: int = Field(..., alias="70b", description="Number of 70B parameter models that can fit")

    class Config:
        """Pydantic model configuration."""

        allow_population_by_field_name = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "7b": 3,
                "13b": 1,
                "70b": 0,
            }
        }
