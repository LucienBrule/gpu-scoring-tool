from pydantic import BaseModel, Field


class MLPredictionRequest(BaseModel):
    """Request model for ML GPU prediction."""

    title: str = Field(..., description="GPU listing title to classify")


class MLPredictionResponse(BaseModel):
    """Response model for ML GPU prediction."""

    ml_is_gpu: bool = Field(..., description="Whether the listing is predicted to be a GPU")
    ml_score: float = Field(..., description="Confidence score (0.0-1.0) for GPU classification")
