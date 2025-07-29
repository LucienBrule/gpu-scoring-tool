"""
Scoring models for glyphsieve.

This module defines Pydantic models for scoring GPU listings, including raw scores,
quantization scores, and final scores.
"""

from pydantic import BaseModel, Field


class ScoredGPU(BaseModel):
    """
    Pydantic model for a scored GPU.

    This model represents the output of the scoring engine, including raw score,
    quantization score, and final score.
    """

    model: str = Field(..., description="Canonical model name (e.g., RTX_A5000)")
    raw_score: float = Field(..., description="Raw score before quantization adjustment")
    quantization_score: float = Field(0.0, description="Score adjustment based on quantization capacity")
    final_score: float = Field(..., description="Final score after all adjustments (0-100)")

    class Config:
        """Pydantic model configuration."""

        schema_extra = {
            "example": {
                "model": "RTX_A5000",
                "raw_score": 0.85,
                "quantization_score": 0.15,
                "final_score": 97.75,
            }
        }
