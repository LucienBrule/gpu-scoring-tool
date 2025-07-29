"""
GPU metadata models for glyphsieve.

This module defines Pydantic models for GPU metadata, including VRAM, TDP, generation, and feature flags.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from glyphsieve.models.quantization import QuantizationCapacitySpec


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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "canonical_model": "RTX_A5000",
                "vram_gb": 24,
                "tdp_watts": 230,
                "mig_support": 0,
                "nvlink": True,
                "generation": "Ampere",
                "cuda_cores": 8192,
                "slot_width": 2,
                "pcie_generation": 4,
            }
        }
    )


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


class GPUListingDTO(BaseModel):
    """
    Data Transfer Object for a normalized GPU listing.

    This model represents a GPU listing that has been normalized with a canonical model name.
    """

    title: str = Field(..., description="Original title of the GPU listing")
    price: float = Field(..., description="Price of the GPU")
    canonical_model: str = Field(..., description="Canonical model name (e.g., RTX_A5000)")
    match_type: str = Field(..., description="Type of match (exact, regex, fuzzy)")
    match_score: float = Field(..., description="Confidence score of the match")


class EnrichedGPUListingDTO(BaseModel):
    """
    Data Transfer Object for an enriched GPU listing.

    This model represents a GPU listing that has been enriched with metadata from the GPU registry.
    """

    # Original fields from GPUListingDTO
    title: str = Field(..., description="Original title of the GPU listing")
    price: float = Field(..., description="Price of the GPU")
    canonical_model: str = Field(..., description="Canonical model name (e.g., RTX_A5000)")
    match_type: str = Field(..., description="Type of match (exact, regex, fuzzy)")
    match_score: float = Field(..., description="Confidence score of the match")

    # Enriched fields from GPUMetadata
    vram_gb: int = Field(..., description="VRAM capacity in GB")
    tdp_w: int = Field(..., description="Thermal Design Power in watts")
    mig_capable: int = Field(0, description="MIG support level (0, 4, or 7)")
    slots: int = Field(1, description="Physical slot width")
    form_factor: str = Field("Standard", description="Form factor (e.g., Standard, SFF)")

    # Optional fields
    nvlink: Optional[bool] = Field(None, description="NVLink support")
    generation: Optional[str] = Field(None, description="GPU architecture generation")
    cuda_cores: Optional[int] = Field(None, description="Number of CUDA cores")
    pcie_generation: Optional[int] = Field(None, description="PCIe generation")

    # Notes and warnings
    notes: Optional[str] = Field(None, description="Additional notes about the GPU")
    warnings: Optional[str] = Field(None, description="Warnings about metadata mismatches")

    # Quantization capacity
    quantization_capacity: Optional[QuantizationCapacitySpec] = Field(
        None, description="Quantization capacity for different model sizes"
    )
