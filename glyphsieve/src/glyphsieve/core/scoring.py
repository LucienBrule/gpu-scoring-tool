"""
Scoring module for glyphsieve.

This module provides functionality for scoring GPU listings based on various metrics.
It implements the Strategy Pattern for scoring, allowing different scoring strategies
to be used interchangeably.
"""
import abc
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import pandas as pd
import yaml
from pydantic import BaseModel, Field

from glyphsieve.models.gpu import GPUMetadata


class ScoringWeights(BaseModel):
    """
    Pydantic model for scoring weights.

    This model defines the weights used for scoring GPU listings.
    """
    vram_weight: float = Field(0.3, description="Weight for VRAM capacity")
    mig_weight: float = Field(0.2, description="Weight for MIG support")
    nvlink_weight: float = Field(0.1, description="Weight for NVLink support")
    tdp_weight: float = Field(0.2, description="Weight for TDP (inverse)")
    price_weight: float = Field(0.2, description="Weight for price (inverse)")

    # Normalization parameters
    max_vram_gb: int = Field(80, description="Maximum VRAM capacity in GB for normalization")
    max_mig_partitions: int = Field(7, description="Maximum MIG partitions for normalization")
    max_tdp_watts: int = Field(700, description="Maximum TDP in watts for normalization")
    max_price: float = Field(10000.0, description="Maximum price for normalization")

    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "vram_weight": 0.3,
                "mig_weight": 0.2,
                "nvlink_weight": 0.1,
                "tdp_weight": 0.2,
                "price_weight": 0.2,
                "max_vram_gb": 80,
                "max_mig_partitions": 7,
                "max_tdp_watts": 700,
                "max_price": 10000.0
            }
        }


def load_scoring_weights(weights_file: Optional[str] = None) -> ScoringWeights:
    """
    Load scoring weights from a YAML file.

    Args:
        weights_file: Path to the YAML file with scoring weights.
                     If None, uses the default weights.

    Returns:
        ScoringWeights: Loaded scoring weights
    """
    if weights_file is None:
        # Use default weights
        return ScoringWeights()

    # Load weights from file
    weights_path = Path(weights_file)
    if not weights_path.exists():
        raise FileNotFoundError(f"Weights file not found: {weights_file}")

    with open(weights_path, "r") as f:
        weights_data = yaml.safe_load(f)

    return ScoringWeights(**weights_data)


class ScoringStrategy(abc.ABC):
    """
    Abstract base class for scoring strategies.

    This class defines the interface for scoring strategies.
    """

    @abc.abstractmethod
    def score_listing(self, row: Dict[str, Any], weights: ScoringWeights) -> float:
        """
        Score a single GPU listing.

        Args:
            row: Dictionary representing a row from the input DataFrame
            weights: Scoring weights

        Returns:
            float: Score for the listing (0.0-1.0)
        """
        pass

    @abc.abstractmethod
    def score_dataframe(self, df: pd.DataFrame, weights: ScoringWeights) -> pd.DataFrame:
        """
        Score all listings in a DataFrame.

        Args:
            df: Input DataFrame with GPU listings
            weights: Scoring weights

        Returns:
            pd.DataFrame: DataFrame with added 'score' column
        """
        pass


class WeightedAdditiveScorer(ScoringStrategy):
    """
    Weighted additive scoring strategy.

    This strategy scores GPU listings using a weighted sum of normalized metrics.
    """

    def score_listing(self, row: Dict[str, Any], weights: ScoringWeights) -> float:
        """
        Score a single GPU listing using the weighted additive model.

        Args:
            row: Dictionary representing a row from the input DataFrame
            weights: Scoring weights

        Returns:
            float: Score for the listing (0.0-1.0)
        """
        score_components = []

        # VRAM score (higher is better)
        vram_gb = max(0, row.get('vram_gb', 0))  # Ensure non-negative
        vram_score = min(vram_gb / weights.max_vram_gb, 1.0) * weights.vram_weight
        score_components.append(vram_score)

        # MIG support score (higher is better)
        mig_support = max(0, row.get('mig_support', 0))  # Ensure non-negative
        mig_score = min(mig_support / weights.max_mig_partitions, 1.0) * weights.mig_weight
        score_components.append(mig_score)

        # NVLink score (binary)
        nvlink = row.get('nvlink', False)
        nvlink_score = weights.nvlink_weight if nvlink else 0.0
        score_components.append(nvlink_score)

        # TDP score (lower is better, so we invert)
        tdp_watts = max(0, row.get('tdp_watts', 0))  # Ensure non-negative
        if tdp_watts > 0:
            # Invert so that lower TDP gets a higher score
            tdp_score = (1.0 - min(tdp_watts / weights.max_tdp_watts, 1.0)) * weights.tdp_weight
        else:
            tdp_score = 0.0  # Missing TDP data
        score_components.append(tdp_score)

        # Price score (lower is better, so we invert)
        price = max(0, row.get('price', 0.0))  # Ensure non-negative
        if price > 0:
            # Invert so that lower price gets a higher score
            price_score = (1.0 - min(price / weights.max_price, 1.0)) * weights.price_weight
        else:
            price_score = 0.0  # Missing price data
        score_components.append(price_score)

        # Sum all components for final score and ensure it's between 0 and 1
        return max(0.0, min(sum(score_components), 1.0))

    def score_dataframe(self, df: pd.DataFrame, weights: ScoringWeights) -> pd.DataFrame:
        """
        Score all listings in a DataFrame using the weighted additive model.

        Args:
            df: Input DataFrame with GPU listings
            weights: Scoring weights

        Returns:
            pd.DataFrame: DataFrame with added 'score' column
        """
        # Create a copy to avoid modifying the original
        result_df = df.copy()

        # Apply scoring to each row
        result_df['score'] = result_df.apply(
            lambda row: self.score_listing(row, weights), axis=1
        )

        return result_df


def score_csv(
    input_file: str,
    output_file: str,
    weights_file: Optional[str] = None,
    strategy: Optional[ScoringStrategy] = None
) -> pd.DataFrame:
    """
    Score GPU listings in a CSV file.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        weights_file: Path to weights YAML file (optional)
        strategy: Scoring strategy to use (defaults to WeightedAdditiveScorer)

    Returns:
        pd.DataFrame: DataFrame with added 'score' column
    """
    # Load the input CSV
    df = pd.read_csv(input_file)

    # Load scoring weights
    weights = load_scoring_weights(weights_file)

    # Use the specified strategy or default to WeightedAdditiveScorer
    if strategy is None:
        strategy = WeightedAdditiveScorer()

    # Score the DataFrame
    scored_df = strategy.score_dataframe(df, weights)

    # Write the output CSV
    scored_df.to_csv(output_file, index=False)

    return scored_df
