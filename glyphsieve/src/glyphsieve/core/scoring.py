"""
Scoring module for glyphsieve.

This module provides functionality for scoring GPU listings based on various metrics.
It implements the Strategy Pattern for scoring, allowing different scoring strategies
to be used interchangeably.
"""

import abc
import csv
import os
from typing import Any, Dict, Optional

import pandas as pd

from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.scoring import ScoredGPU
from glyphsieve.models.scoring_weights import ScoringWeights


def load_scoring_weights(weights_file: Optional[str] = None) -> ScoringWeights:
    """
    Load scoring weights from a YAML file using the resource loader strategy.

    Args:
        weights_file: Optional override path for the scoring weights file.

    Returns:
        ScoringWeights: Parsed and validated scoring weights model.
    """
    loader = GlyphSieveYamlLoader()
    return loader.load(ScoringWeights, weights_file or "scoring_weights.yaml")


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
        vram_gb = max(0, row.get("vram_gb", 0))  # Ensure non-negative
        vram_score = min(vram_gb / weights.max_vram_gb, 1.0) * weights.vram_weight
        score_components.append(vram_score)

        # MIG support score (higher is better)
        mig_support = max(0, row.get("mig_support", 0))  # Ensure non-negative
        mig_score = min(mig_support / weights.max_mig_partitions, 1.0) * weights.mig_weight
        score_components.append(mig_score)

        # NVLink score (binary)
        nvlink = row.get("nvlink", False)
        nvlink_score = weights.nvlink_weight if nvlink else 0.0
        score_components.append(nvlink_score)

        # TDP score (lower is better, so we invert)
        tdp_watts = max(0, row.get("tdp_watts", 0))  # Ensure non-negative
        if tdp_watts > 0:
            # Invert so that lower TDP gets a higher score
            tdp_score = (1.0 - min(tdp_watts / weights.max_tdp_watts, 1.0)) * weights.tdp_weight
        else:
            tdp_score = 0.0  # Missing TDP data
        score_components.append(tdp_score)

        # Price score (lower is better, so we invert)
        price = max(0, row.get("price", 0.0))  # Ensure non-negative
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
        result_df["score"] = result_df.apply(lambda row: self.score_listing(row, weights), axis=1)

        return result_df


class EnhancedWeightedScorer(ScoringStrategy):
    """
    Enhanced weighted scoring strategy that includes quantization capacity.

    This strategy scores GPU listings using a weighted sum of normalized metrics,
    and incorporates quantization capacity to adjust the final score.
    """

    def score_listing(self, row: Dict[str, Any], weights: ScoringWeights) -> Dict[str, float]:
        """
        Score a single GPU listing using the enhanced weighted model.

        Args:
            row: Dictionary representing a row from the input DataFrame
            weights: Scoring weights

        Returns:
            Dict[str, float]: Dictionary with raw_score, quantization_score, and final_score
        """
        # Calculate raw score components
        score_components = []

        # VRAM score (higher is better)
        vram_gb = max(0, row.get("vram_gb", 0))  # Ensure non-negative
        vram_score = min(vram_gb / weights.max_vram_gb, 1.0) * weights.vram_weight
        score_components.append(vram_score)

        # MIG support score (higher is better)
        mig_support = max(0, row.get("mig_capable", 0))  # Ensure non-negative
        mig_score = min(mig_support / weights.max_mig_partitions, 1.0) * weights.mig_weight
        score_components.append(mig_score)

        # NVLink score (binary)
        nvlink = row.get("nvlink", False)
        nvlink_score = weights.nvlink_weight if nvlink else 0.0
        score_components.append(nvlink_score)

        # TDP score (lower is better, so we invert)
        tdp_watts = max(0, row.get("tdp_w", 0))  # Ensure non-negative
        if tdp_watts > 0:
            # Invert so that lower TDP gets a higher score
            tdp_score = (1.0 - min(tdp_watts / weights.max_tdp_watts, 1.0)) * weights.tdp_weight
        else:
            tdp_score = 0.0  # Missing TDP data
        score_components.append(tdp_score)

        # Price score (lower is better, so we invert)
        price = max(0, row.get("price", 0.0))  # Ensure non-negative
        if price > 0:
            # Invert so that lower price gets a higher score
            price_score = (1.0 - min(price / weights.max_price, 1.0)) * weights.price_weight
        else:
            price_score = 0.0  # Missing price data
        score_components.append(price_score)

        # Calculate raw score (sum of all components)
        raw_score = max(0.0, min(sum(score_components), 1.0))

        # Calculate quantization score based on quantization capacity
        quantization_score = 0.0
        if (
            "quantization_capacity.7b" in row
            and "quantization_capacity.13b" in row
            and "quantization_capacity.70b" in row
        ):
            # Calculate a weighted average of the quantization capacities
            # We give more weight to larger models
            q_7b = row.get("quantization_capacity.7b", 0)
            q_13b = row.get("quantization_capacity.13b", 0)
            q_70b = row.get("quantization_capacity.70b", 0)

            # Normalize the capacities
            q_7b_norm = min(q_7b / 10, 1.0)  # Assume 10 7B models is the max
            q_13b_norm = min(q_13b / 5, 1.0)  # Assume 5 13B models is the max
            q_70b_norm = min(q_70b / 1, 1.0)  # Assume 1 70B model is the max

            # Calculate weighted average
            quantization_score = (0.2 * q_7b_norm + 0.3 * q_13b_norm + 0.5 * q_70b_norm) * weights.quantization_weight

            # Ensure it's between 0 and max_quantization_score
            quantization_score = max(0.0, min(quantization_score, weights.max_quantization_score))

        # Calculate final score
        adjusted_score = raw_score * (1 + quantization_score)

        return {"raw_score": raw_score, "quantization_score": quantization_score, "final_score": adjusted_score}

    def score_dataframe(self, df: pd.DataFrame, weights: ScoringWeights) -> pd.DataFrame:
        """
        Score all listings in a DataFrame using the enhanced weighted model.

        Args:
            df: Input DataFrame with GPU listings
            weights: Scoring weights

        Returns:
            pd.DataFrame: DataFrame with added score columns
        """
        # Create a copy to avoid modifying the original
        result_df = df.copy()

        # Apply scoring to each row
        scores = []
        for _, row in result_df.iterrows():
            score_dict = self.score_listing(row, weights)
            scores.append(score_dict)

        # Add score columns to the DataFrame
        result_df["raw_score"] = [score["raw_score"] for score in scores]
        result_df["quantization_score"] = [score["quantization_score"] for score in scores]
        result_df["score"] = [score["final_score"] for score in scores]

        # Normalize final scores to 0-100 scale
        if not result_df.empty:
            min_score = result_df["score"].min()
            max_score = result_df["score"].max()

            if max_score > min_score:
                result_df["final_score"] = (result_df["score"] - min_score) / (max_score - min_score) * 100
            else:
                result_df["final_score"] = 50.0  # Default to middle value if all scores are the same

        return result_df


def score_csv(
    input_file: str,
    output_file: str,
    weights_file: Optional[str] = None,
    strategy: Optional[ScoringStrategy] = None,
    weight_overrides: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """
    Score GPU listings in a CSV file.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        weights_file: Path to weights YAML file (optional)
        strategy: Scoring strategy to use (defaults to EnhancedWeightedScorer)
        weight_overrides: Dictionary of weight overrides (optional)

    Returns:
        pd.DataFrame: DataFrame with added score columns
    """
    # Load the input CSV
    df = pd.read_csv(input_file)

    # Load scoring weights
    weights = load_scoring_weights(weights_file)

    # Apply weight overrides if provided
    if weight_overrides:
        for key, value in weight_overrides.items():
            if hasattr(weights, key):
                setattr(weights, key, value)

    # Use the specified strategy or default to EnhancedWeightedScorer
    if strategy is None:
        strategy = EnhancedWeightedScorer()

    # Score the DataFrame
    scored_df = strategy.score_dataframe(df, weights)

    # Extract ScoredGPU records
    scored_gpus = []
    for _, row in scored_df.iterrows():
        model = row.get("canonical_model", "Unknown")
        raw_score = row.get("raw_score", 0.0)
        quantization_score = row.get("quantization_score", 0.0)
        final_score = row.get("final_score", 0.0)

        scored_gpu = ScoredGPU(
            model=model, raw_score=raw_score, quantization_score=quantization_score, final_score=final_score
        )
        scored_gpus.append(scored_gpu)

    # Write the output CSV
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    # Write using DictWriter to ensure consistent column order
    with open(output_file, "w", newline="") as f:
        fieldnames = ["model", "raw_score", "quantization_score", "final_score"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for gpu in scored_gpus:
            writer.writerow(gpu.model_dump())

    # Return the full scored DataFrame for backward compatibility
    return scored_df
