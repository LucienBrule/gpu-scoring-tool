"""
DTO models for GPU listings.
"""

from pydantic import BaseModel, Field


class GPUListingDTO(BaseModel):
    """
    Data Transfer Object for GPU listing information.

    Represents a GPU listing with its properties and score.
    """

    canonical_model: str = Field(..., description="The canonical model name of the GPU")
    vram_gb: int = Field(..., description="The amount of VRAM in GB")
    mig_support: int = Field(..., description="The MIG support level (0-7)")
    nvlink: bool = Field(..., description="Whether the GPU supports NVLink")
    tdp_watts: int = Field(..., description="The TDP in watts")
    price: float = Field(..., description="The price in USD")
    score: float = Field(..., description="The calculated utility score")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "canonical_model": "H100_PCIE_80GB",
                "vram_gb": 80,
                "mig_support": 7,
                "nvlink": True,
                "tdp_watts": 350,
                "price": 10000.0,
                "score": 0.7,
            }
        }
