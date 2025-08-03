"""
Tests for ML Configuration System

This module tests the ML configuration loading and conditional logic
in the ml_signal.py module.
"""

from unittest.mock import Mock, patch

import pytest

from glyphsieve.ml.ml_signal import _load_ml_config, predict_is_gpu
from glyphsieve.models.ml_config import MLConfig


class TestMLConfig:
    """Test ML configuration loading and validation."""

    def test_ml_config_model_validation(self):
        """Test MLConfig model validation with valid data."""
        config_data = {"model_path": "models/gpu_classifier_v2.pkl", "threshold": 0.3, "enabled": True}

        config = MLConfig.model_validate(config_data)

        assert config.model_path == "models/gpu_classifier_v2.pkl"
        assert config.threshold == 0.3
        assert config.enabled is True

    def test_ml_config_default_values(self):
        """Test MLConfig model with default values."""
        config_data = {"model_path": "models/gpu_classifier_v2.pkl"}

        config = MLConfig.model_validate(config_data)

        assert config.model_path == "models/gpu_classifier_v2.pkl"
        assert config.threshold == 0.2  # default value
        assert config.enabled is True  # default value

    def test_ml_config_threshold_validation(self):
        """Test MLConfig threshold validation."""
        # Test valid threshold
        config_data = {"model_path": "models/gpu_classifier_v2.pkl", "threshold": 0.5}
        config = MLConfig.model_validate(config_data)
        assert config.threshold == 0.5

        # Test invalid threshold (too low)
        with pytest.raises(ValueError):
            MLConfig.model_validate({"model_path": "models/gpu_classifier_v2.pkl", "threshold": -0.1})

        # Test invalid threshold (too high)
        with pytest.raises(ValueError):
            MLConfig.model_validate({"model_path": "models/gpu_classifier_v2.pkl", "threshold": 1.1})

    @patch("glyphsieve.ml.ml_signal.GlyphSieveYamlLoader")
    def test_load_ml_config_success(self, mock_loader_class):
        """Test successful ML config loading."""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader

        expected_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.2, enabled=True)
        mock_loader.load.return_value = expected_config

        config = _load_ml_config()

        assert config == expected_config
        mock_loader.load.assert_called_once_with(MLConfig, "configs/ml_config.yaml")


class TestMLSignal:
    """Test ML signal functionality with configuration."""

    @patch("glyphsieve.ml.ml_signal._load_ml_config")
    def test_predict_is_gpu_disabled_config(self, mock_load_config):
        """Test that ML stage is skipped when disabled in config."""
        # Configure ML as disabled
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.2, enabled=False)
        mock_load_config.return_value = mock_config

        result = predict_is_gpu("NVIDIA RTX 4090", "Gaming GPU")

        assert result == (False, 0.0)
        mock_load_config.assert_called_once()

    @patch("glyphsieve.ml.ml_signal._load_ml_config")
    @patch("glyphsieve.ml.predictor.predict_is_gpu")
    def test_predict_is_gpu_enabled_config(self, mock_predictor, mock_load_config):
        """Test that ML prediction is called when enabled in config."""
        # Configure ML as enabled
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.3, enabled=True)
        mock_load_config.return_value = mock_config

        # Mock predictor response
        mock_predictor.return_value = (True, 0.8)

        result = predict_is_gpu("NVIDIA RTX 4090", "Gaming GPU")

        assert result == (True, 0.8)
        mock_load_config.assert_called_once()
        mock_predictor.assert_called_once_with("NVIDIA RTX 4090", "Gaming GPU", 0.3)

    @patch("glyphsieve.ml.ml_signal._load_ml_config")
    @patch("glyphsieve.ml.predictor.predict_is_gpu")
    def test_predict_is_gpu_threshold_override(self, mock_predictor, mock_load_config):
        """Test that explicit threshold overrides config threshold."""
        # Configure ML with threshold 0.3
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.3, enabled=True)
        mock_load_config.return_value = mock_config

        # Mock predictor response
        mock_predictor.return_value = (True, 0.8)

        # Call with explicit threshold
        result = predict_is_gpu("NVIDIA RTX 4090", "Gaming GPU", threshold=0.7)

        assert result == (True, 0.8)
        mock_load_config.assert_called_once()
        # Should use explicit threshold, not config threshold
        mock_predictor.assert_called_once_with("NVIDIA RTX 4090", "Gaming GPU", 0.7)

    @patch("glyphsieve.ml.ml_signal._load_ml_config")
    @patch("glyphsieve.ml.predictor.predict_is_gpu")
    def test_predict_is_gpu_uses_config_threshold(self, mock_predictor, mock_load_config):
        """Test that config threshold is used when no explicit threshold provided."""
        # Configure ML with custom threshold
        mock_config = MLConfig(model_path="models/gpu_classifier_v2.pkl", threshold=0.4, enabled=True)
        mock_load_config.return_value = mock_config

        # Mock predictor response
        mock_predictor.return_value = (False, 0.3)

        result = predict_is_gpu("Some product", "Not a GPU")

        assert result == (False, 0.3)
        mock_load_config.assert_called_once()
        # Should use config threshold
        mock_predictor.assert_called_once_with("Some product", "Not a GPU", 0.4)
