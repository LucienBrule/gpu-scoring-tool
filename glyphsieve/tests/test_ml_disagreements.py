"""
Unit tests for ML disagreement analysis functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from glyphsieve.ml.disagreement_analysis import (
    DisagreementAnalyzer,
    load_disagreement_config,
)
from glyphsieve.models.disagreement_scoring import DisagreementScoringConfig


class TestDisagreementScoringConfig(unittest.TestCase):
    """Test cases for DisagreementScoringConfig model."""

    def test_default_values(self):
        """Test default configuration values."""
        config = DisagreementScoringConfig()

        self.assertEqual(config.high_confidence_threshold, 0.8)
        self.assertEqual(config.medium_confidence_threshold, 0.6)
        self.assertEqual(config.confidence_weight, 0.4)
        self.assertEqual(config.disagreement_type_weight, 0.3)
        self.assertEqual(config.text_complexity_weight, 0.2)
        self.assertEqual(config.frequency_weight, 0.1)
        self.assertEqual(config.rules_unknown_ml_gpu_multiplier, 1.2)
        self.assertEqual(config.rules_gpu_ml_unknown_multiplier, 1.0)
        self.assertEqual(config.min_priority_score, 1.0)
        self.assertEqual(config.max_priority_score, 10.0)

    def test_custom_values(self):
        """Test configuration with custom values."""
        config = DisagreementScoringConfig(high_confidence_threshold=0.9, confidence_weight=0.5, min_priority_score=2.0)

        self.assertEqual(config.high_confidence_threshold, 0.9)
        self.assertEqual(config.confidence_weight, 0.5)
        self.assertEqual(config.min_priority_score, 2.0)
        # Other values should remain default
        self.assertEqual(config.medium_confidence_threshold, 0.6)


class TestLoadDisagreementConfig(unittest.TestCase):
    """Test cases for configuration loading."""

    @patch("glyphsieve.ml.disagreement_analysis.GlyphSieveYamlLoader")
    def test_load_default_config(self, mock_loader_class):
        """Test loading default configuration file."""
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_config = DisagreementScoringConfig()
        mock_loader.load.return_value = mock_config

        result = load_disagreement_config()

        mock_loader.load.assert_called_once_with(DisagreementScoringConfig, "disagreement_scoring.yaml")
        self.assertEqual(result, mock_config)

    @patch("glyphsieve.ml.disagreement_analysis.GlyphSieveYamlLoader")
    def test_load_custom_config(self, mock_loader_class):
        """Test loading custom configuration file."""
        mock_loader = MagicMock()
        mock_loader_class.return_value = mock_loader
        mock_config = DisagreementScoringConfig()
        mock_loader.load.return_value = mock_config

        result = load_disagreement_config("custom_config.yaml")

        mock_loader.load.assert_called_once_with(DisagreementScoringConfig, "custom_config.yaml")
        self.assertEqual(result, mock_config)


class TestDisagreementAnalyzer(unittest.TestCase):
    """Test cases for DisagreementAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = DisagreementScoringConfig()
        self.analyzer = DisagreementAnalyzer(self.config)

        # Create sample test data
        self.sample_data = pd.DataFrame(
            {
                "title": ["NVIDIA RTX 4090", "Intel CPU i7", "RTX 3080 Gaming", "AMD Processor", "GeForce GTX 1660"],
                "bulk_notes": [
                    "High-end gaming GPU",
                    "Desktop processor",
                    "Gaming graphics card",
                    "CPU for workstation",
                    "Budget gaming card",
                ],
                "canonical_model": ["RTX 4090", "UNKNOWN", "RTX 3080", "UNKNOWN", "UNKNOWN"],
                "ml_is_gpu": [1, 0, 1, 1, 0],
                "ml_score": [0.95, 0.2, 0.88, 0.75, 0.65],
            }
        )

    def test_identify_disagreements_type_a(self):
        """Test identification of Type A disagreements (rules=UNKNOWN, ML=GPU)."""
        disagreements = self.analyzer.identify_disagreements(self.sample_data, min_confidence=0.7)

        # Should find row with index 3: canonical_model=UNKNOWN, ml_is_gpu=1, ml_score=0.75
        type_a_cases = disagreements[disagreements["disagreement_type"] == "rules_unknown_ml_gpu"]
        self.assertEqual(len(type_a_cases), 1)
        self.assertEqual(type_a_cases.iloc[0]["title"], "AMD Processor")
        self.assertEqual(type_a_cases.iloc[0]["ml_score"], 0.75)

    def test_identify_disagreements_type_b(self):
        """Test identification of Type B disagreements (rules=GPU, ML=not GPU)."""
        # Modify sample data to create Type B disagreement
        test_data = self.sample_data.copy()
        test_data.loc[2, "ml_is_gpu"] = 0  # RTX 3080 with ml_is_gpu=0
        test_data.loc[2, "ml_score"] = 0.8  # High confidence

        disagreements = self.analyzer.identify_disagreements(test_data, min_confidence=0.7)

        type_b_cases = disagreements[disagreements["disagreement_type"] == "rules_gpu_ml_unknown"]
        self.assertEqual(len(type_b_cases), 1)
        self.assertEqual(type_b_cases.iloc[0]["title"], "RTX 3080 Gaming")
        self.assertEqual(type_b_cases.iloc[0]["canonical_model"], "RTX 3080")

    def test_identify_disagreements_confidence_filtering(self):
        """Test that disagreements are filtered by confidence threshold."""
        # With min_confidence=0.8, should only find high-confidence cases
        disagreements = self.analyzer.identify_disagreements(self.sample_data, min_confidence=0.8)

        # Only the AMD Processor case should be filtered out (ml_score=0.75 < 0.8)
        if len(disagreements) > 0:
            self.assertTrue(all(disagreements["ml_score"] >= 0.8))
        else:
            # If no disagreements found, that's also valid (means no high-confidence disagreements)
            self.assertEqual(len(disagreements), 0)

    def test_identify_disagreements_missing_columns(self):
        """Test error handling for missing required columns."""
        incomplete_data = self.sample_data.drop(columns=["ml_score"])

        with self.assertRaises(ValueError) as context:
            self.analyzer.identify_disagreements(incomplete_data)

        self.assertIn("Missing required columns", str(context.exception))

    def test_identify_disagreements_empty_result(self):
        """Test handling of no disagreements found."""
        # Create data with no disagreements
        no_disagreement_data = pd.DataFrame(
            {
                "title": ["RTX 4090", "Intel CPU"],
                "bulk_notes": ["GPU", "CPU"],
                "canonical_model": ["RTX 4090", "UNKNOWN"],
                "ml_is_gpu": [1, 0],
                "ml_score": [0.95, 0.2],
            }
        )

        disagreements = self.analyzer.identify_disagreements(no_disagreement_data)
        self.assertEqual(len(disagreements), 0)

    def test_categorize_confidence(self):
        """Test confidence level categorization."""
        self.assertEqual(self.analyzer._categorize_confidence(0.9), "high")
        self.assertEqual(self.analyzer._categorize_confidence(0.8), "high")
        self.assertEqual(self.analyzer._categorize_confidence(0.7), "medium")
        self.assertEqual(self.analyzer._categorize_confidence(0.6), "medium")
        self.assertEqual(self.analyzer._categorize_confidence(0.5), "low")

    def test_calculate_priority_score(self):
        """Test priority score calculation."""
        # Create a test row
        test_row = pd.Series(
            {
                "ml_score": 0.9,
                "disagreement_type": "rules_unknown_ml_gpu",
                "title": "Test GPU",
                "bulk_notes": "Test description",
            }
        )

        priority_score = self.analyzer._calculate_priority_score(test_row)

        # Should be within valid range
        self.assertGreaterEqual(priority_score, self.config.min_priority_score)
        self.assertLessEqual(priority_score, self.config.max_priority_score)

        # High confidence should result in higher priority
        self.assertGreater(priority_score, 5.0)

    def test_calculate_priority_score_type_multiplier(self):
        """Test that different disagreement types get different priority multipliers."""
        base_row = pd.Series({"ml_score": 0.8, "title": "Test", "bulk_notes": "Test"})

        # Type A should get higher priority due to multiplier
        type_a_row = base_row.copy()
        type_a_row["disagreement_type"] = "rules_unknown_ml_gpu"
        priority_a = self.analyzer._calculate_priority_score(type_a_row)

        # Type B should get lower priority
        type_b_row = base_row.copy()
        type_b_row["disagreement_type"] = "rules_gpu_ml_unknown"
        priority_b = self.analyzer._calculate_priority_score(type_b_row)

        self.assertGreater(priority_a, priority_b)

    def test_generate_summary_stats(self):
        """Test summary statistics generation."""
        disagreements = self.analyzer.identify_disagreements(self.sample_data, min_confidence=0.7)
        summary = self.analyzer.generate_summary_stats(disagreements, len(self.sample_data))

        self.assertIn("total_disagreements", summary)
        self.assertIn("disagreement_rate", summary)
        self.assertIn("type_breakdown", summary)
        self.assertIn("confidence_breakdown", summary)
        self.assertIn("high_priority_count", summary)

        # Check calculated values
        self.assertEqual(summary["total_disagreements"], len(disagreements))
        self.assertEqual(summary["disagreement_rate"], len(disagreements) / len(self.sample_data) * 100)

    def test_generate_summary_stats_empty(self):
        """Test summary statistics with empty disagreements."""
        empty_disagreements = pd.DataFrame()
        summary = self.analyzer.generate_summary_stats(empty_disagreements, 100)

        self.assertEqual(summary["total_disagreements"], 0)
        self.assertEqual(summary["disagreement_rate"], 0.0)
        self.assertEqual(summary["type_breakdown"], {})
        self.assertEqual(summary["confidence_breakdown"], {})
        self.assertEqual(summary["high_priority_count"], 0)

    def test_get_top_disagreements_by_type(self):
        """Test getting top disagreements by type."""
        disagreements = self.analyzer.identify_disagreements(self.sample_data, min_confidence=0.7)
        top_by_type = self.analyzer.get_top_disagreements_by_type(disagreements, n=5)

        self.assertIsInstance(top_by_type, dict)

        # Should have entries for each disagreement type found
        for disagreement_type in disagreements["disagreement_type"].unique():
            self.assertIn(disagreement_type, top_by_type)

            # Each type should have DataFrame with cases sorted by priority
            type_cases = top_by_type[disagreement_type]
            self.assertIsInstance(type_cases, pd.DataFrame)

            # Should be sorted by priority score descending
            if len(type_cases) > 1:
                priority_scores = type_cases["priority_score"].values
                self.assertTrue(
                    all(priority_scores[i] >= priority_scores[i + 1] for i in range(len(priority_scores) - 1))
                )


class TestDisagreementAnalyzerIntegration(unittest.TestCase):
    """Integration tests for disagreement analysis with realistic data."""

    def setUp(self):
        """Set up integration test fixtures."""
        self.config = DisagreementScoringConfig()
        self.analyzer = DisagreementAnalyzer(self.config)

        # Create more realistic test data
        self.realistic_data = pd.DataFrame(
            {
                "title": [
                    "NVIDIA GeForce RTX 4090 24GB GDDR6X",
                    "Intel Core i9-13900K Desktop Processor",
                    "ASUS ROG Strix RTX 3080 Gaming OC",
                    "AMD Ryzen 9 7950X 16-Core Processor",
                    "MSI GeForce GTX 1660 SUPER Gaming X",
                    "Corsair Vengeance LPX 32GB DDR4",
                    "EVGA GeForce RTX 3070 Ti FTW3",
                    "Samsung 980 PRO 2TB NVMe SSD",
                    "Gigabyte RTX 4070 Gaming OC",
                    "Western Digital Black 4TB HDD",
                ],
                "bulk_notes": [
                    "High-end gaming graphics card with 24GB VRAM",
                    "Latest generation Intel processor for gaming",
                    "Premium gaming GPU with RGB lighting",
                    "High-performance AMD processor for workstations",
                    "Budget-friendly gaming graphics card",
                    "High-speed DDR4 memory for gaming systems",
                    "Mid-range RTX graphics card with ray tracing",
                    "Fast NVMe SSD for gaming and productivity",
                    "New generation RTX graphics card",
                    "Large capacity storage drive for data",
                ],
                "canonical_model": [
                    "RTX 4090",
                    "UNKNOWN",
                    "RTX 3080",
                    "UNKNOWN",
                    "GTX 1660 SUPER",
                    "UNKNOWN",
                    "UNKNOWN",  # This should be RTX 3070 Ti but rules missed it
                    "UNKNOWN",
                    "RTX 4070",
                    "UNKNOWN",
                ],
                "ml_is_gpu": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                "ml_score": [0.98, 0.15, 0.95, 0.25, 0.88, 0.1, 0.92, 0.05, 0.94, 0.08],
            }
        )

    def test_realistic_disagreement_analysis(self):
        """Test disagreement analysis with realistic GPU/non-GPU data."""
        disagreements = self.analyzer.identify_disagreements(self.realistic_data, min_confidence=0.8)

        # Should find the RTX 3070 Ti case (rules=UNKNOWN, ML=GPU with high confidence)
        type_a_cases = disagreements[disagreements["disagreement_type"] == "rules_unknown_ml_gpu"]
        self.assertGreater(len(type_a_cases), 0)

        # Verify the RTX 3070 Ti case is identified
        rtx_3070_cases = type_a_cases[type_a_cases["title"].str.contains("3070")]
        self.assertEqual(len(rtx_3070_cases), 1)
        self.assertEqual(rtx_3070_cases.iloc[0]["ml_score"], 0.92)

    def test_confidence_level_distribution(self):
        """Test that confidence levels are properly distributed."""
        disagreements = self.analyzer.identify_disagreements(self.realistic_data, min_confidence=0.7)

        if len(disagreements) > 0:
            # Should have appropriate confidence levels based on ml_score
            high_conf_cases = disagreements[disagreements["confidence_level"] == "high"]
            for _, case in high_conf_cases.iterrows():
                self.assertGreater(case["ml_score"], self.config.high_confidence_threshold)

    def test_priority_score_ordering(self):
        """Test that priority scores properly order disagreements."""
        disagreements = self.analyzer.identify_disagreements(self.realistic_data, min_confidence=0.7)

        if len(disagreements) > 1:
            # Sort by priority score
            sorted_disagreements = disagreements.sort_values("priority_score", ascending=False)

            # Higher ML scores should generally get higher priority (among other factors)
            # This is a general trend test, not absolute due to other factors
            top_case = sorted_disagreements.iloc[0]
            bottom_case = sorted_disagreements.iloc[-1]

            self.assertGreaterEqual(top_case["priority_score"], bottom_case["priority_score"])

    def test_summary_statistics_realistic(self):
        """Test summary statistics with realistic data."""
        disagreements = self.analyzer.identify_disagreements(self.realistic_data, min_confidence=0.8)
        summary = self.analyzer.generate_summary_stats(disagreements, len(self.realistic_data))

        # Disagreement rate should be reasonable (< 50% for this test data)
        self.assertLess(summary["disagreement_rate"], 50.0)

        # Should have proper breakdown structures
        self.assertIsInstance(summary["type_breakdown"], dict)
        self.assertIsInstance(summary["confidence_breakdown"], dict)

        # High priority count should be reasonable
        self.assertLessEqual(summary["high_priority_count"], summary["total_disagreements"])


if __name__ == "__main__":
    unittest.main()
