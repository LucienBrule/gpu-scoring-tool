"""
GPU metadata models for glyphsieve.

This module defines Pydantic models for GPU metadata, including VRAM, TDP, generation, and feature flags.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GPUMetadata(BaseModel):
    """
    Pydantic model for GPU metadata.
    
    This model defines the structure of GPU metadata, including VRAM, TDP, generation, and feature flags.
    """
    canonical_model: str = Field(..., description="Canonical model name (e.g., RTX_A5000)")
    vram_gb: int = Field(..., description="VRAM capacity in GB")
    tdp_watts: int = Field(..., description="Thermal Design Power in watts")
    mig_support: int = Field(0, description="MIG support level (0, 4, or 7)")
    nvlink: bool = Field(False, description="NVLink support")
    generation: str = Field(..., description="GPU architecture generation (e.g., Ada, Ampere, Hopper, Blackwell)")
    cuda_cores: Optional[int] = Field(None, description="Number of CUDA cores")
    slot_width: Optional[int] = Field(None, description="Physical slot width")
    pcie_generation: Optional[int] = Field(None, description="PCIe generation")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "canonical_model": "RTX_A5000",
                "vram_gb": 24,
                "tdp_watts": 230,
                "mig_support": 0,
                "nvlink": True,
                "generation": "Ampere",
                "cuda_cores": 8192,
                "slot_width": 2,
                "pcie_generation": 4
            }
        }


class GPURegistry(BaseModel):
    """
    Registry of GPU metadata.
    
    This model defines a collection of GPU metadata, indexed by canonical model name.
    """
    gpus: List[GPUMetadata] = Field(..., description="List of GPU metadata")
    
    def to_dict(self) -> Dict[str, GPUMetadata]:
        """
        Convert the registry to a dictionary indexed by canonical model name.
        
        Returns:
            Dict[str, GPUMetadata]: Dictionary of GPU metadata indexed by canonical model name
        """
        return {gpu.canonical_model: gpu for gpu in self.gpus}