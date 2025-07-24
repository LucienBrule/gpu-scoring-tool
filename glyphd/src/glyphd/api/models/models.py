"""
DTO models for GPU model metadata.
"""
from typing import Optional
from pydantic import BaseModel, Field


class GPUModelDTO(BaseModel):
    """
    Data Transfer Object for GPU model metadata.
    
    Represents a GPU model with its specifications and market data.
    """
    model: str = Field(..., description="The model name of the GPU")
    listing_count: int = Field(..., description="The number of listings for this model")
    min_price: float = Field(..., description="The minimum price for this model")
    median_price: float = Field(..., description="The median price for this model")
    max_price: float = Field(..., description="The maximum price for this model")
    avg_price: float = Field(..., description="The average price for this model")
    
    # Additional fields from gpu_specs.yaml
    vram_gb: Optional[int] = Field(None, description="The amount of VRAM in GB")
    tdp_watts: Optional[int] = Field(None, description="The TDP in watts")
    mig_support: Optional[int] = Field(None, description="The MIG support level (0-7)")
    nvlink: Optional[bool] = Field(None, description="Whether the GPU supports NVLink")
    generation: Optional[str] = Field(None, description="The GPU generation (e.g., Ada, Ampere)")
    cuda_cores: Optional[int] = Field(None, description="The number of CUDA cores")
    slot_width: Optional[int] = Field(None, description="The slot width")
    pcie_generation: Optional[int] = Field(None, description="The PCIe generation")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "model": "NVIDIA H100 PCIe 80GB",
                "listing_count": 7,
                "min_price": 23800.0,
                "median_price": 34995.0,
                "max_price": 49999.0,
                "avg_price": 34024.71,
                "vram_gb": 80,
                "tdp_watts": 350,
                "mig_support": 7,
                "nvlink": True,
                "generation": "Hopper",
                "cuda_cores": 18176,
                "slot_width": 2,
                "pcie_generation": 5
            }
        }