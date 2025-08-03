from pydantic import BaseModel, ConfigDict, Field


class DisagreementScoringConfig(BaseModel):
    """
    Pydantic model for disagreement scoring configuration.

    This model defines the weights and thresholds used for scoring
    disagreements between rule-based and ML classification systems.
    """

    # Confidence level thresholds
    high_confidence_threshold: float = Field(0.8, description="Threshold for high confidence ML predictions")
    medium_confidence_threshold: float = Field(0.6, description="Threshold for medium confidence ML predictions")

    # Priority scoring weights (should sum to 1.0)
    confidence_weight: float = Field(0.4, description="Weight for ML confidence score in priority calculation")
    disagreement_type_weight: float = Field(0.3, description="Weight for disagreement type in priority calculation")
    text_complexity_weight: float = Field(0.2, description="Weight for text complexity in priority calculation")
    frequency_weight: float = Field(0.1, description="Weight for pattern frequency in priority calculation")

    # Type-specific priority multipliers
    rules_unknown_ml_gpu_multiplier: float = Field(
        1.2, description="Priority multiplier for rules=UNKNOWN, ML=GPU cases"
    )
    rules_gpu_ml_unknown_multiplier: float = Field(
        1.0, description="Priority multiplier for rules=GPU, ML=UNKNOWN cases"
    )

    # Text complexity scoring parameters
    max_title_length: int = Field(200, description="Maximum title length for normalization")
    max_bulk_notes_length: int = Field(1000, description="Maximum bulk notes length for normalization")

    # Priority score scaling
    min_priority_score: float = Field(1.0, description="Minimum priority score")
    max_priority_score: float = Field(10.0, description="Maximum priority score")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "high_confidence_threshold": 0.8,
                "medium_confidence_threshold": 0.6,
                "confidence_weight": 0.4,
                "disagreement_type_weight": 0.3,
                "text_complexity_weight": 0.2,
                "frequency_weight": 0.1,
                "rules_unknown_ml_gpu_multiplier": 1.2,
                "rules_gpu_ml_unknown_multiplier": 1.0,
                "max_title_length": 200,
                "max_bulk_notes_length": 1000,
                "min_priority_score": 1.0,
                "max_priority_score": 10.0,
            }
        }
    )
