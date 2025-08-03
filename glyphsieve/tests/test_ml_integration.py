"""
Unit tests for ML integration functionality.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from glyphsieve.ml.predictor import predict_batch, predict_is_gpu, reset_model_cache
from glyphsieve.models.ml_config import MLConfig


class TestMLPredictor(unittest.TestCase):
    """Test cases for ML predictor functionality."""

    def setUp(self):
        """Reset model cache before each test."""
        reset_model_cache()

    def test_predict_is_gpu_no_model(self):
        """Test predict_is_gpu with no model file."""
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.side_effect = FileNotFoundError("Model not found")

            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertFalse(is_gpu)
            self.assertEqual(score, 0.0)

    def test_predict_is_gpu_with_model(self):
        """Test predict_is_gpu with mock model."""
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.2, 0.8]]  # 80% confidence
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertTrue(is_gpu)  # Above default 0.5 threshold
            self.assertEqual(score, 0.8)

    def test_predict_batch(self):
        """Test batch prediction functionality."""
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.1, 0.9], [0.7, 0.3]]
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            titles = ["RTX 4090", "CPU Intel"]
            bulk_notes = ["Gaming", "Processor"]
            results = predict_batch(titles, bulk_notes)

            self.assertEqual(len(results), 2)
            self.assertTrue(results[0][0])  # First should be GPU
            self.assertFalse(results[1][0])  # Second should not be GPU

    def test_threshold_override(self):
        """Test threshold override functionality."""
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.4, 0.6]]  # 60% confidence
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            # Test with default threshold (0.5) - should be True
            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertTrue(is_gpu)
            self.assertEqual(score, 0.6)

            # Test with higher threshold (0.7) - should be False
            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU", threshold=0.7)
            self.assertFalse(is_gpu)
            self.assertEqual(score, 0.6)

    def test_configuration_threshold(self):
        """Test threshold from configuration."""
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.4, 0.6]]  # 60% confidence
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.8, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            # Should use config threshold (0.8) - result should be False
            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertFalse(is_gpu)
            self.assertEqual(score, 0.6)

    def test_invalid_config_threshold(self):
        """Test fallback when config loading fails."""
        with patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class:
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.side_effect = Exception("Config loading failed")

            from glyphsieve.ml.predictor import _get_threshold

            threshold = _get_threshold()
            self.assertEqual(threshold, 0.5)  # Should fallback to default

    def test_model_without_predict_proba(self):
        """Test model that doesn't have predict_proba method."""
        mock_model = MagicMock()
        del mock_model.predict_proba  # Remove the method
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertFalse(is_gpu)
            self.assertEqual(score, 0.0)

    def test_prediction_error_handling(self):
        """Test error handling during prediction."""
        mock_model = MagicMock()
        mock_model.predict_proba.side_effect = Exception("Prediction error")
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
            patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
        ):
            mock_loader = MagicMock()
            mock_loader_class.return_value = mock_loader
            mock_loader.load.return_value = mock_config

            mock_pkl_loader = MagicMock()
            mock_pkl_loader_class.return_value = mock_pkl_loader
            mock_pkl_loader.load.return_value = mock_model

            is_gpu, score = predict_is_gpu("RTX 4090", "Gaming GPU")
            self.assertFalse(is_gpu)
            self.assertEqual(score, 0.0)

    def test_batch_length_mismatch(self):
        """Test batch prediction with mismatched input lengths."""
        titles = ["RTX 4090", "CPU Intel"]
        bulk_notes = ["Gaming"]  # One less item

        with self.assertRaises(ValueError):
            predict_batch(titles, bulk_notes)

    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        from glyphsieve.ml.predictor import _preprocess_text

        # Test normal case
        result = _preprocess_text("RTX 4090", "Gaming GPU")
        self.assertEqual(result, "rtx 4090 gaming gpu")

        # Test with None values
        result = _preprocess_text(None, "Gaming GPU")
        self.assertEqual(result, "gaming gpu")

        result = _preprocess_text("RTX 4090", None)
        self.assertEqual(result, "rtx 4090")

        # Test with empty strings
        result = _preprocess_text("", "")
        self.assertEqual(result, "")


class TestMLIntegration(unittest.TestCase):
    """Test cases for ML integration with normalization pipeline."""

    def setUp(self):
        """Reset model cache before each test."""
        reset_model_cache()

    def test_normalize_csv_with_ml(self):
        """Test normalize_csv with ML integration enabled."""
        from glyphsieve.core.normalization import normalize_csv

        # Create test CSV data
        test_data = pd.DataFrame(
            {
                "title": ["RTX 4090 Gaming", "Intel CPU i7", "GTX 1080"],
                "bulk_notes": ["Graphics card", "Processor", "GPU"],
            }
        )

        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.1, 0.9], [0.8, 0.2], [0.3, 0.7]]

        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as input_file,
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as output_file,
        ):

            # Write test data
            test_data.to_csv(input_file.name, index=False)

            with patch("glyphsieve.ml.predictor.predict_batch") as mock_predict_batch:
                # Mock the predict_batch function to return our expected results
                mock_predict_batch.return_value = [(True, 0.9), (False, 0.2), (True, 0.7)]

                # Test with ML enabled
                result_df = normalize_csv(input_file.name, output_file.name, use_ml=True, ml_threshold=0.6)

                # Check that ML columns were added
                self.assertIn("ml_is_gpu", result_df.columns)
                self.assertIn("ml_score", result_df.columns)

                # Check ML predictions (threshold 0.6)
                self.assertEqual(result_df["ml_is_gpu"].tolist(), [1, 0, 1])  # 0.9 > 0.6, 0.2 < 0.6, 0.7 > 0.6
                self.assertEqual(result_df["ml_score"].tolist(), [0.9, 0.2, 0.7])

            # Cleanup
            os.unlink(input_file.name)
            os.unlink(output_file.name)

    def test_normalize_csv_without_ml(self):
        """Test normalize_csv without ML integration."""
        from glyphsieve.core.normalization import normalize_csv

        # Create test CSV data
        test_data = pd.DataFrame({"title": ["RTX 4090 Gaming", "Intel CPU i7"]})

        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as input_file,
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as output_file,
        ):

            # Write test data
            test_data.to_csv(input_file.name, index=False)

            # Test without ML
            result_df = normalize_csv(input_file.name, output_file.name, use_ml=False)

            # Check that ML columns were NOT added
            self.assertNotIn("ml_is_gpu", result_df.columns)
            self.assertNotIn("ml_score", result_df.columns)

            # Cleanup
            os.unlink(input_file.name)
            os.unlink(output_file.name)

    def test_normalize_csv_missing_bulk_notes(self):
        """Test normalize_csv with missing bulk_notes column."""
        from glyphsieve.core.normalization import normalize_csv

        # Create test CSV data without bulk_notes
        test_data = pd.DataFrame({"title": ["RTX 4090 Gaming", "Intel CPU i7"]})

        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.1, 0.9], [0.8, 0.2]]
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.5, enabled=True)

        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as input_file,
            tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as output_file,
        ):

            # Write test data
            test_data.to_csv(input_file.name, index=False)

            with (
                patch("glyphsieve.ml.predictor.GlyphSieveYamlLoader") as mock_loader_class,
                patch("glyphsieve.ml.predictor.GlyphSievePklLoader") as mock_pkl_loader_class,
            ):
                mock_loader = MagicMock()
                mock_loader_class.return_value = mock_loader
                mock_loader.load.return_value = mock_config

                mock_pkl_loader = MagicMock()
                mock_pkl_loader_class.return_value = mock_pkl_loader
                mock_pkl_loader.load.return_value = mock_model

                # Should work without bulk_notes column
                result_df = normalize_csv(input_file.name, output_file.name, use_ml=True)

                # Check that ML columns were added
                self.assertIn("ml_is_gpu", result_df.columns)
                self.assertIn("ml_score", result_df.columns)

            # Cleanup
            os.unlink(input_file.name)
            os.unlink(output_file.name)


if __name__ == "__main__":
    unittest.main()
