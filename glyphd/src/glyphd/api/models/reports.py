"""
DTO models for GPU market reports.
"""

from typing import Dict, List

from pydantic import BaseModel, Field


class ReportDTO(BaseModel):
    """
    Data Transfer Object for GPU market insight reports.

    Represents a market insight report with markdown content and structured data.
    """

    markdown: str = Field(..., description="The full markdown content of the report")
    summary_stats: Dict[str, str] = Field(..., description="Summary statistics from the report")
    top_ranked: List[str] = Field(..., description="List of top-ranked GPU models")
    scoring_weights: Dict[str, float] = Field(..., description="Weights used for scoring")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "markdown": "# GPU Market Insight Report\n*Generated on 2025-07-24*\n\n## Summary Statistics\n...",
                "summary_stats": {
                    "number_of_listings": "5",
                    "unique_models": "5",
                    "price_range": "$1000.00 - $10000.00",
                    "average_price": "$4600.00",
                    "median_price": "$2500.00",
                    "score_range": "0.3314 - 0.7000",
                    "average_score": "0.4789",
                    "most_common_model": "H100_PCIE_80GB",
                },
                "top_ranked": ["H100_PCIE_80GB", "A100_40GB_PCIE", "RTX_A5000", "RTX_3090", "RTX_4090"],
                "scoring_weights": {
                    "vram_weight": 0.3,
                    "mig_weight": 0.2,
                    "nvlink_weight": 0.1,
                    "tdp_weight": 0.2,
                    "price_weight": 0.2,
                },
            }
        }
