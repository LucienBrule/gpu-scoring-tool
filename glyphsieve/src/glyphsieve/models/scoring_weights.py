from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    """
    Pydantic model for scoring weights.

    This model defines the weights used for scoring GPU listings.
    """

    vram_weight: float = Field(0.25, description="Weight for VRAM capacity")
    mig_weight: float = Field(0.15, description="Weight for MIG support")
    nvlink_weight: float = Field(0.1, description="Weight for NVLink support")
    tdp_weight: float = Field(0.15, description="Weight for TDP (inverse)")
    price_weight: float = Field(0.15, description="Weight for price (inverse)")
    quantization_weight: float = Field(0.2, description="Weight for quantization capacity")

    # Normalization parameters
    max_vram_gb: int = Field(80, description="Maximum VRAM capacity in GB for normalization")
    max_mig_partitions: int = Field(7, description="Maximum MIG partitions for normalization")
    max_tdp_watts: int = Field(700, description="Maximum TDP in watts for normalization")
    max_price: float = Field(10000.0, description="Maximum price for normalization")
    max_quantization_score: float = Field(1.0, description="Maximum quantization score for normalization")

    class Config:
        """Pydantic model configuration."""

        schema_extra = {
            "example": {
                "vram_weight": 0.25,
                "mig_weight": 0.15,
                "nvlink_weight": 0.1,
                "tdp_weight": 0.15,
                "price_weight": 0.15,
                "quantization_weight": 0.2,
                "max_vram_gb": 80,
                "max_mig_partitions": 7,
                "max_tdp_watts": 700,
                "max_price": 10000.0,
                "max_quantization_score": 1.0,
            }
        }
