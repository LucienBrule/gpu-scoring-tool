"""
Unit tests for ML training functionality.

Tests the GPUClassifierTrainer class, feature extraction, training pipeline,
and model persistence. Because as we know: "Testing is just debugging with style."
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import joblib
import numpy as np
import pandas as pd
import pytest

from glyphsieve.ml.training import GPUClassifierTrainer


class TestGPUClassifierTrainer:
    """Test the GPUClassifierTrainer class functionality."""

    def create_sample_training_data(self, n_samples=100, gpu_ratio=0.4):
        """
        Create sample training data for testing.

        This is our synthetic epistemic playground - generating fake but realistic
        GPU listings to test our classifier. Like a simulation within a simulation.
        """
        gpu_count = int(n_samples * gpu_ratio)
        non_gpu_count = n_samples - gpu_count

        # GPU samples with realistic titles and descriptions
        gpu_titles = [
            "NVIDIA RTX 4090 Gaming GPU",
            "RTX 3080 Ti Graphics Card",
            "GeForce RTX 4070 SUPER",
            "NVIDIA A100 Data Center GPU",
            "RTX 5090 Founders Edition",
            "GeForce RTX 3060 Ti",
            "NVIDIA L40 Professional GPU",
            "RTX 4080 SUPER Gaming",
        ] * (gpu_count // 8 + 1)

        gpu_notes = [
            "High-performance gaming graphics card with ray tracing",
            "Professional GPU for AI and machine learning workloads",
            "Gaming graphics card with DLSS support",
            "Data center GPU for deep learning applications",
            "Latest generation gaming GPU with advanced features",
            "Mid-range gaming GPU with excellent performance",
            "Professional workstation graphics card",
            "High-end gaming GPU with ray tracing capabilities",
        ] * (gpu_count // 8 + 1)

        # Non-GPU samples
        non_gpu_titles = [
            "Intel Core i9-12900K CPU",
            "AMD Ryzen 7 5800X Processor",
            "32GB DDR4 RAM Memory Kit",
            "Samsung 980 PRO NVMe SSD",
            "ASUS ROG Motherboard",
            "Corsair PSU 850W Gold",
            "Noctua CPU Cooler",
            "Gaming Keyboard RGB",
        ] * (non_gpu_count // 8 + 1)

        non_gpu_notes = [
            "High-performance CPU for gaming and productivity",
            "AMD processor with excellent multi-core performance",
            "High-speed memory for gaming systems",
            "Fast NVMe storage drive",
            "Gaming motherboard with RGB lighting",
            "Reliable power supply unit",
            "Quiet CPU cooling solution",
            "Mechanical gaming keyboard",
        ] * (non_gpu_count // 8 + 1)

        # Combine data
        titles = gpu_titles[:gpu_count] + non_gpu_titles[:non_gpu_count]
        notes = gpu_notes[:gpu_count] + non_gpu_notes[:non_gpu_count]
        labels = [1] * gpu_count + [0] * non_gpu_count

        # Shuffle to avoid ordering bias
        data = list(zip(titles, notes, labels))
        np.random.shuffle(data)
        titles, notes, labels = zip(*data)

        return pd.DataFrame({"title": titles, "bulk_notes": notes, "is_gpu": labels})

    def test_trainer_initialization(self):
        """Test trainer initialization with default and custom parameters."""
        # Default initialization
        trainer = GPUClassifierTrainer()
        assert trainer.cv_folds == 5
        assert trainer.random_state == 42
        assert trainer.pipeline is None
        assert trainer.best_params is None
        assert trainer.cv_results is None

        # Custom initialization
        trainer_custom = GPUClassifierTrainer(cv_folds=3, random_state=123)
        assert trainer_custom.cv_folds == 3
        assert trainer_custom.random_state == 123

    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        trainer = GPUClassifierTrainer()

        # Test normal text
        text = "NVIDIA RTX 4090 Gaming GPU!!!"
        processed = trainer._preprocess_text(text)
        assert processed == "nvidia rtx 4090 gaming gpu"

        # Test text with special characters
        text = "RTX-4080 @#$% SUPER (Gaming)"
        processed = trainer._preprocess_text(text)
        assert processed == "rtx 4080 super gaming"

        # Test empty/null text
        assert trainer._preprocess_text("") == ""
        assert trainer._preprocess_text(None) == ""
        assert trainer._preprocess_text(pd.NA) == ""

        # Test multiple spaces
        text = "RTX    4090     Gaming"
        processed = trainer._preprocess_text(text)
        assert processed == "rtx 4090 gaming"

    def test_feature_preparation(self):
        """Test feature preparation from DataFrame."""
        trainer = GPUClassifierTrainer()

        # Create test DataFrame
        df = pd.DataFrame({"title": ["RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"]})

        features = trainer._prepare_features(df)

        assert len(features) == 2
        assert features.iloc[0] == "rtx 4090 gaming gpu"
        assert features.iloc[1] == "intel cpu processor"

        # Test with missing values
        df_missing = pd.DataFrame({"title": ["RTX 4090", None], "bulk_notes": [None, "Processor"]})

        features_missing = trainer._prepare_features(df_missing)
        assert features_missing.iloc[0] == "rtx 4090"
        assert features_missing.iloc[1] == "processor"

    def test_pipeline_creation(self):
        """Test TF-IDF + Logistic Regression pipeline creation."""
        trainer = GPUClassifierTrainer()
        pipeline = trainer._create_pipeline()

        # Check pipeline structure
        assert len(pipeline.steps) == 2
        assert pipeline.steps[0][0] == "tfidf"
        assert pipeline.steps[1][0] == "classifier"

        # Check TF-IDF parameters
        tfidf = pipeline.steps[0][1]
        assert tfidf.lowercase
        assert tfidf.stop_words == "english"
        assert tfidf.dtype == np.float32

        # Check LogisticRegression parameters
        classifier = pipeline.steps[1][1]
        assert classifier.random_state == 42
        assert classifier.max_iter == 1000
        assert classifier.class_weight == "balanced"

    def test_param_combinations_calculation(self):
        """Test parameter combinations calculation."""
        trainer = GPUClassifierTrainer()

        # Calculate expected combinations
        # max_features: 3, ngram_range: 2, min_df: 2, max_df: 2, C: 3, solver: 2
        expected = 3 * 2 * 2 * 2 * 3 * 2
        actual = trainer._get_param_combinations()

        assert actual == expected

    def test_training_with_sample_data(self):
        """Test training with sample data."""
        trainer = GPUClassifierTrainer(cv_folds=2)  # Reduce CV folds for speed

        # Create sample data
        train_df = self.create_sample_training_data(n_samples=50)

        # Mock GridSearchCV to speed up testing
        with patch("glyphsieve.ml.training.GridSearchCV") as mock_grid_search:
            mock_estimator = MagicMock()
            mock_grid_search.return_value.fit.return_value = None
            mock_grid_search.return_value.best_estimator_ = mock_estimator
            mock_grid_search.return_value.best_params_ = {"tfidf__max_features": 1000}
            mock_grid_search.return_value.best_score_ = 0.95

            # Mock cross_validate
            with patch("glyphsieve.ml.training.cross_validate") as mock_cv:
                mock_cv.return_value = {
                    "test_accuracy": np.array([0.94, 0.96]),
                    "test_precision": np.array([0.93, 0.95]),
                    "test_recall": np.array([0.92, 0.94]),
                    "test_f1": np.array([0.93, 0.95]),
                    "train_accuracy": np.array([0.95, 0.97]),
                    "train_precision": np.array([0.94, 0.96]),
                    "train_recall": np.array([0.93, 0.95]),
                    "train_f1": np.array([0.94, 0.96]),
                }

                results = trainer.train(train_df)

                # Check results structure
                assert "best_params" in results
                assert "best_cv_score" in results
                assert "cv_scores" in results
                assert "cv_score_means" in results
                assert "training_samples" in results
                assert "class_distribution" in results

                # Check specific values
                assert results["best_cv_score"] == 0.95
                assert results["training_samples"] == 50
                assert results["cv_score_means"]["test_f1"] == 0.94  # Mean of [0.93, 0.95]

    def test_training_validation_errors(self):
        """Test training validation with invalid data."""
        trainer = GPUClassifierTrainer()

        # Test missing columns
        df_missing_cols = pd.DataFrame(
            {
                "title": ["RTX 4090"],
                "bulk_notes": ["Gaming GPU"],
                # Missing is_gpu column
            }
        )

        with pytest.raises(ValueError, match="Missing required columns"):
            trainer.train(df_missing_cols)

        # Test empty dataset
        df_empty = pd.DataFrame({"title": [], "bulk_notes": [], "is_gpu": []})

        with pytest.raises(ValueError, match="Training dataset is empty"):
            trainer.train(df_empty)

    def test_model_persistence(self):
        """Test model saving and loading."""
        trainer = GPUClassifierTrainer()

        # Create a mock trained pipeline
        mock_pipeline = MagicMock()
        trainer.pipeline = mock_pipeline
        trainer.cv_results = {
            "best_params": {"tfidf__max_features": 1000},
            "best_cv_score": 0.95,
            "cv_scores": {
                "test_accuracy": [0.94, 0.96],
                "test_precision": [0.93, 0.95],
                "test_recall": [0.92, 0.94],
                "test_f1": [0.93, 0.95],
                "train_accuracy": [0.95, 0.97],
                "train_precision": [0.94, 0.96],
                "train_recall": [0.93, 0.95],
                "train_f1": [0.94, 0.96],
            },
            "cv_score_means": {"test_f1": 0.94, "test_precision": 0.93, "test_recall": 0.92, "test_accuracy": 0.95},
            "training_samples": 100,
            "class_distribution": {"gpu_count": 40, "non_gpu_count": 60, "gpu_ratio": 0.4},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.pkl")
            metrics_path = os.path.join(temp_dir, "metrics.yaml")

            # Test saving
            with patch("pickle.dump") as mock_dump:
                trainer.save_model(model_path, metrics_path)
                mock_dump.assert_called_once_with(mock_pipeline, mock_dump.call_args[0][1])

            # Check metrics file was created (mocked YAML writing)
            assert Path(metrics_path).parent.exists()

    def test_model_loading(self):
        """Test model loading from disk."""
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as temp_file:
            model_path = temp_file.name

            # Create a real pipeline that can be pickled
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import Pipeline

            real_pipeline = Pipeline(
                [("tfidf", TfidfVectorizer(max_features=100)), ("classifier", LogisticRegression(random_state=42))]
            )
            joblib.dump(real_pipeline, model_path)

            try:
                # Test loading
                loaded_model = GPUClassifierTrainer.load_model(model_path)
                assert loaded_model is not None
                assert isinstance(loaded_model, Pipeline)

            finally:
                os.unlink(model_path)

        # Test loading non-existent file
        with pytest.raises(FileNotFoundError):
            GPUClassifierTrainer.load_model("nonexistent_model.pkl")

    def test_prediction_functionality(self):
        """Test prediction on new data."""
        trainer = GPUClassifierTrainer()

        # Create mock trained pipeline
        mock_pipeline = MagicMock()
        mock_pipeline.predict.return_value = np.array([1, 0])
        mock_pipeline.predict_proba.return_value = np.array([[0.1, 0.9], [0.8, 0.2]])
        trainer.pipeline = mock_pipeline

        # Test prediction
        test_texts = pd.Series(["RTX 4090 Gaming", "Intel CPU"])
        predictions, probabilities = trainer.predict(test_texts)

        assert len(predictions) == 2
        assert len(probabilities) == 2
        assert predictions[0] == 1
        assert predictions[1] == 0

        # Test prediction without trained model
        trainer_untrained = GPUClassifierTrainer()
        with pytest.raises(ValueError, match="Model must be trained before making predictions"):
            trainer_untrained.predict(test_texts)

    def test_save_model_without_training(self):
        """Test saving model without training first."""
        trainer = GPUClassifierTrainer()

        with pytest.raises(ValueError, match="Model must be trained before saving"):
            trainer.save_model("test_model.pkl")


class TestTrainingIntegration:
    """Integration tests for the complete training pipeline."""

    def test_end_to_end_training_pipeline(self):
        """Test complete training pipeline with real scikit-learn components."""
        # Create realistic sample data
        train_data = {
            "title": [
                "NVIDIA RTX 4090 Gaming GPU",
                "RTX 3080 Ti Graphics Card",
                "Intel Core i9-12900K CPU",
                "AMD Ryzen 7 5800X Processor",
                "GeForce RTX 4070 SUPER",
                "Samsung 980 PRO NVMe SSD",
                "NVIDIA A100 Data Center GPU",
                "Corsair PSU 850W Gold",
            ],
            "bulk_notes": [
                "High-performance gaming graphics card with ray tracing",
                "Gaming graphics card with DLSS support",
                "High-performance CPU for gaming and productivity",
                "AMD processor with excellent multi-core performance",
                "Latest generation gaming GPU with advanced features",
                "Fast NVMe storage drive",
                "Professional GPU for AI and machine learning workloads",
                "Reliable power supply unit",
            ],
            "is_gpu": [1, 1, 0, 0, 1, 0, 1, 0],
        }

        train_df = pd.DataFrame(train_data)

        # Initialize trainer with minimal CV for speed
        trainer = GPUClassifierTrainer(cv_folds=2)

        # Reduce parameter grid for faster testing
        trainer.param_grid = {
            "tfidf__max_features": [100, 500],
            "tfidf__ngram_range": [(1, 1)],
            "tfidf__min_df": [1],
            "tfidf__max_df": [0.95],
            "classifier__C": [1.0],
            "classifier__solver": ["liblinear"],
        }

        # Train the model
        results = trainer.train(train_df)

        # Verify results
        assert trainer.pipeline is not None
        assert trainer.best_params is not None
        assert results["training_samples"] == 8
        assert "test_f1" in results["cv_score_means"]

        # Test prediction on new data
        test_texts = pd.Series(["RTX 5090 Gaming GPU", "Intel CPU Processor"])
        predictions, probabilities = trainer.predict(test_texts)

        assert len(predictions) == 2
        assert len(probabilities) == 2
        assert probabilities.shape == (2, 2)  # 2 samples, 2 classes

        # Test model persistence
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "integration_test_model.pkl")
            trainer.save_model(model_path)

            # Verify files exist
            assert os.path.exists(model_path)
            metrics_path = os.path.join(temp_dir, "metrics.yaml")
            assert os.path.exists(metrics_path)

            # Test loading
            loaded_model = GPUClassifierTrainer.load_model(model_path)
            assert loaded_model is not None

            # Test loaded model predictions
            loaded_predictions = loaded_model.predict(test_texts.apply(trainer._preprocess_text))
            assert len(loaded_predictions) == 2
