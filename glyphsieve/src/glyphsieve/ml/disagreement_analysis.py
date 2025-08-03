"""
Disagreement analysis between rule-based and ML classification systems.

This module provides functionality to identify and score cases where the rule-based
normalization system and ML classifier disagree on GPU classification.
"""

import logging
from typing import Dict

import pandas as pd

from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.disagreement_scoring import DisagreementScoringConfig

logger = logging.getLogger(__name__)


def load_disagreement_config(config_file: str = "disagreement_scoring.yaml") -> DisagreementScoringConfig:
    """
    Load disagreement scoring configuration from YAML file.

    Args:
        config_file: Path to the configuration file

    Returns:
        DisagreementScoringConfig: Loaded and validated configuration
    """
    loader = GlyphSieveYamlLoader()
    return loader.load(DisagreementScoringConfig, config_file)


class DisagreementAnalyzer:
    """
    Analyzer for identifying and scoring disagreements between rule-based and ML systems.
    """

    def __init__(self, config: DisagreementScoringConfig):
        """
        Initialize the disagreement analyzer.

        Args:
            config: Disagreement scoring configuration
        """
        self.config = config

    def identify_disagreements(self, df: pd.DataFrame, min_confidence: float = 0.7) -> pd.DataFrame:
        """
        Identify disagreements between rule-based and ML classification.

        Args:
            df: DataFrame with columns: canonical_model, ml_is_gpu, ml_score
            min_confidence: Minimum ML confidence threshold for consideration

        Returns:
            DataFrame with disagreement cases
        """
        logger.info(f"Analyzing {len(df)} rows for disagreements with min_confidence={min_confidence}")

        # Validate required columns
        required_columns = ["canonical_model", "ml_is_gpu", "ml_score", "title", "bulk_notes"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Filter by minimum confidence
        high_conf_df = df[df["ml_score"] >= min_confidence].copy()
        logger.info(f"Found {len(high_conf_df)} rows above confidence threshold")

        # Identify Type A disagreements: Rules=UNKNOWN, ML=GPU
        type_a_mask = (high_conf_df["canonical_model"] == "UNKNOWN") & (high_conf_df["ml_is_gpu"] == 1)
        type_a_disagreements = high_conf_df[type_a_mask].copy()
        type_a_disagreements["disagreement_type"] = "rules_unknown_ml_gpu"

        # Identify Type B disagreements: Rules=known GPU, ML=not GPU
        type_b_mask = (high_conf_df["canonical_model"] != "UNKNOWN") & (high_conf_df["ml_is_gpu"] == 0)
        type_b_disagreements = high_conf_df[type_b_mask].copy()
        type_b_disagreements["disagreement_type"] = "rules_gpu_ml_unknown"

        # Combine disagreements
        disagreements = pd.concat([type_a_disagreements, type_b_disagreements], ignore_index=True)

        logger.info(f"Found {len(type_a_disagreements)} Type A disagreements (rules=UNKNOWN, ML=GPU)")
        logger.info(f"Found {len(type_b_disagreements)} Type B disagreements (rules=GPU, ML=not GPU)")
        logger.info(f"Total disagreements: {len(disagreements)}")

        if len(disagreements) == 0:
            logger.warning("No disagreements found - this may indicate perfect agreement or data issues")
            return pd.DataFrame()

        # Add confidence levels
        disagreements["confidence_level"] = disagreements["ml_score"].apply(self._categorize_confidence)

        # Calculate priority scores
        disagreements["priority_score"] = disagreements.apply(self._calculate_priority_score, axis=1)

        return disagreements

    def _categorize_confidence(self, ml_score: float) -> str:
        """
        Categorize ML confidence level.

        Args:
            ml_score: ML confidence score

        Returns:
            Confidence level category
        """
        if ml_score >= self.config.high_confidence_threshold:
            return "high"
        elif ml_score >= self.config.medium_confidence_threshold:
            return "medium"
        else:
            return "low"

    def _calculate_priority_score(self, row: pd.Series) -> float:
        """
        Calculate priority score for a disagreement case.

        Args:
            row: DataFrame row with disagreement data

        Returns:
            Priority score (1-10 scale)
        """
        # Base score from ML confidence
        confidence_component = row["ml_score"] * self.config.confidence_weight

        # Disagreement type component
        if row["disagreement_type"] == "rules_unknown_ml_gpu":
            type_multiplier = self.config.rules_unknown_ml_gpu_multiplier
        else:
            type_multiplier = self.config.rules_gpu_ml_unknown_multiplier

        type_component = type_multiplier * self.config.disagreement_type_weight

        # Text complexity component
        title_complexity = (
            min(len(str(row.get("title", ""))), self.config.max_title_length) / self.config.max_title_length
        )
        notes_complexity = (
            min(len(str(row.get("bulk_notes", ""))), self.config.max_bulk_notes_length)
            / self.config.max_bulk_notes_length
        )
        complexity_component = (title_complexity + notes_complexity) / 2 * self.config.text_complexity_weight

        # Frequency component (simplified - could be enhanced with actual frequency analysis)
        frequency_component = 0.5 * self.config.frequency_weight  # Placeholder

        # Combine components
        raw_score = confidence_component + type_component + complexity_component + frequency_component

        # Scale to 1-10 range
        scaled_score = (
            raw_score * (self.config.max_priority_score - self.config.min_priority_score)
            + self.config.min_priority_score
        )

        # Ensure within bounds
        return max(self.config.min_priority_score, min(scaled_score, self.config.max_priority_score))

    def generate_summary_stats(self, disagreements: pd.DataFrame, total_rows: int) -> Dict:
        """
        Generate summary statistics for disagreements.

        Args:
            disagreements: DataFrame with disagreement cases
            total_rows: Total number of rows analyzed

        Returns:
            Dictionary with summary statistics
        """
        if len(disagreements) == 0:
            return {
                "total_disagreements": 0,
                "disagreement_rate": 0.0,
                "type_breakdown": {},
                "confidence_breakdown": {},
                "high_priority_count": 0,
            }

        disagreement_rate = len(disagreements) / total_rows * 100

        # Type breakdown
        type_counts = disagreements["disagreement_type"].value_counts().to_dict()

        # Confidence breakdown
        confidence_counts = disagreements["confidence_level"].value_counts().to_dict()

        # High priority cases (score > 7)
        high_priority_count = len(disagreements[disagreements["priority_score"] > 7])

        return {
            "total_disagreements": len(disagreements),
            "disagreement_rate": disagreement_rate,
            "type_breakdown": type_counts,
            "confidence_breakdown": confidence_counts,
            "high_priority_count": high_priority_count,
            "avg_priority_score": disagreements["priority_score"].mean(),
            "max_priority_score": disagreements["priority_score"].max(),
            "min_priority_score": disagreements["priority_score"].min(),
        }

    def get_top_disagreements_by_type(self, disagreements: pd.DataFrame, n: int = 10) -> Dict[str, pd.DataFrame]:
        """
        Get top N disagreements for each type.

        Args:
            disagreements: DataFrame with disagreement cases
            n: Number of top cases to return per type

        Returns:
            Dictionary mapping disagreement type to top cases
        """
        result = {}

        for disagreement_type in disagreements["disagreement_type"].unique():
            type_cases = disagreements[disagreements["disagreement_type"] == disagreement_type]
            top_cases = type_cases.nlargest(n, ["priority_score", "ml_score"])
            result[disagreement_type] = top_cases

        return result
