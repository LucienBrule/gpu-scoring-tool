"""
Unit tests for ML evaluation functionality.

Tests the GPUClassifierEvaluator class, metrics calculation, visualization generation,
and failure analysis. Because as we know: "In evaluation we trust, but test everything."
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import joblib
import numpy as np
import pandas as pd
import pytest
import yaml

from glyphsieve.ml.evaluation import GPUClassifierEvaluator


class TestGPUClassifierEvaluator:
    """Test the GPUClassifierEvaluator class functionality."""

    def create_sample_test_data(self, n_samples=100, gpu_ratio=0.4, add_errors=False):
        """
        Create sample test data for evaluation testing.

        Args:
            n_samples: Number of samples to generate
            gpu_ratio: Ratio of GPU samples
            add_errors: Whether to add some prediction errors for testing
        """
        gpu_count = int(n_samples * gpu_ratio)
        non_gpu_count = n_samples - gpu_count

        # GPU samples
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

    def create_mock_model(self, perfect_predictions=True):
        """Create a mock model for testing."""
        mock_model = MagicMock()

        def mock_predict(X):
            # For testing, we'll create predictions based on whether 'gpu' is in the text
            predictions = []
            for text in X:
                # Simple heuristic: if 'gpu', 'rtx', 'geforce', or 'nvidia' in text, predict GPU
                text_lower = text.lower()
                if any(keyword in text_lower for keyword in ["gpu", "rtx", "geforce", "nvidia", "a100", "l40"]):
                    predictions.append(1)
                else:
                    predictions.append(0)
            return np.array(predictions)

        def mock_predict_proba(X):
            # Create probability scores
            predictions = mock_predict(X)
            probabilities = []
            for pred in predictions:
                if pred == 1:
                    # High confidence for GPU predictions
                    prob = np.random.uniform(0.8, 0.99)
                    probabilities.append([1 - prob, prob])
                else:
                    # High confidence for non-GPU predictions
                    prob = np.random.uniform(0.8, 0.99)
                    probabilities.append([prob, 1 - prob])
            return np.array(probabilities)

        mock_model.predict = mock_predict
        mock_model.predict_proba = mock_predict_proba

        return mock_model

    def test_evaluator_initialization(self):
        """Test evaluator initialization."""
        evaluator = GPUClassifierEvaluator()
        assert evaluator.random_state == 42
        assert evaluator.model is None
        assert evaluator.test_results is None

        # Test custom random state
        evaluator_custom = GPUClassifierEvaluator(random_state=123)
        assert evaluator_custom.random_state == 123

    def test_load_model(self):
        """Test model loading functionality."""
        evaluator = GPUClassifierEvaluator()

        # Test loading non-existent model
        with pytest.raises(FileNotFoundError):
            evaluator.load_model("nonexistent_model.pkl")

        # Test loading valid model
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
                evaluator.load_model(model_path)
                assert evaluator.model is not None
                assert isinstance(evaluator.model, Pipeline)
            finally:
                os.unlink(model_path)

    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        evaluator = GPUClassifierEvaluator()

        # Test normal text
        text = "NVIDIA RTX 4090 Gaming GPU!!!"
        processed = evaluator._preprocess_text(text)
        assert processed == "nvidia rtx 4090 gaming gpu"

        # Test text with special characters
        text = "RTX-4080 @#$% SUPER (Gaming)"
        processed = evaluator._preprocess_text(text)
        assert processed == "rtx 4080 super gaming"

        # Test empty/null text
        assert evaluator._preprocess_text("") == ""
        assert evaluator._preprocess_text(None) == ""
        assert evaluator._preprocess_text(pd.NA) == ""

        # Test multiple spaces
        text = "RTX    4090     Gaming"
        processed = evaluator._preprocess_text(text)
        assert processed == "rtx 4090 gaming"

    def test_feature_preparation(self):
        """Test feature preparation from DataFrame."""
        evaluator = GPUClassifierEvaluator()

        # Create test DataFrame
        df = pd.DataFrame({"title": ["RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"]})

        features = evaluator._prepare_features(df)

        assert len(features) == 2
        assert features.iloc[0] == "rtx 4090 gaming gpu"
        assert features.iloc[1] == "intel cpu processor"

        # Test with missing values
        df_missing = pd.DataFrame({"title": ["RTX 4090", None], "bulk_notes": [None, "Processor"]})

        features_missing = evaluator._prepare_features(df_missing)
        assert features_missing.iloc[0] == "rtx 4090"
        assert features_missing.iloc[1] == "processor"

    def test_evaluate_model_validation(self):
        """Test model evaluation input validation."""
        evaluator = GPUClassifierEvaluator()

        # Test without loaded model
        test_df = self.create_sample_test_data(10)
        with pytest.raises(ValueError, match="Model must be loaded before evaluation"):
            evaluator.evaluate_model(test_df)

        # Load mock model
        evaluator.model = self.create_mock_model()

        # Test missing columns
        df_missing_cols = pd.DataFrame(
            {
                "title": ["RTX 4090"],
                "bulk_notes": ["Gaming GPU"],
                # Missing is_gpu column
            }
        )

        with pytest.raises(ValueError, match="Missing required columns"):
            evaluator.evaluate_model(df_missing_cols)

        # Test empty dataset
        df_empty = pd.DataFrame({"title": [], "bulk_notes": [], "is_gpu": []})

        with pytest.raises(ValueError, match="Test dataset is empty"):
            evaluator.evaluate_model(df_empty)

    def test_evaluate_model_basic(self):
        """Test basic model evaluation functionality."""
        evaluator = GPUClassifierEvaluator()
        evaluator.model = self.create_mock_model()

        # Create test data
        test_df = self.create_sample_test_data(50)

        # Run evaluation
        results = evaluator.evaluate_model(test_df)

        # Check results structure
        assert "overall_metrics" in results
        assert "per_class_metrics" in results
        assert "confusion_matrix" in results
        assert "dataset_info" in results
        assert "classification_report" in results

        # Check overall metrics
        overall = results["overall_metrics"]
        required_metrics = [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "specificity",
            "npv",
            "roc_auc",
            "average_precision",
        ]
        for metric in required_metrics:
            assert metric in overall
            assert 0.0 <= overall[metric] <= 1.0

        # Check dataset info
        dataset_info = results["dataset_info"]
        assert dataset_info["test_samples"] == 50
        assert dataset_info["gpu_samples"] + dataset_info["non_gpu_samples"] == 50

        # Check confusion matrix
        cm = results["confusion_matrix"]
        assert "tn" in cm and "fp" in cm and "fn" in cm and "tp" in cm
        assert cm["tn"] + cm["fp"] + cm["fn"] + cm["tp"] == 50

        # Check that test results are stored
        assert evaluator.test_results is not None
        assert "y_true" in evaluator.test_results
        assert "y_pred" in evaluator.test_results
        assert "y_pred_proba" in evaluator.test_results

    def test_metrics_calculation(self):
        """Test metrics calculation with known data."""
        evaluator = GPUClassifierEvaluator()

        # Create known test case
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_pred = np.array([1, 0, 0, 0, 1, 1])  # 1 FN, 1 FP
        y_pred_proba = np.array([[0.1, 0.9], [0.7, 0.3], [0.8, 0.2], [0.9, 0.1], [0.2, 0.8], [0.3, 0.7]])

        results = evaluator._calculate_metrics(y_true, y_pred, y_pred_proba)

        # Check specific values
        assert results["confusion_matrix"]["tp"] == 2  # True positives
        assert results["confusion_matrix"]["tn"] == 2  # True negatives
        assert results["confusion_matrix"]["fp"] == 1  # False positives
        assert results["confusion_matrix"]["fn"] == 1  # False negatives

        # Check that precision and recall are calculated correctly
        # Precision = TP / (TP + FP) = 2 / (2 + 1) = 0.667
        # Recall = TP / (TP + FN) = 2 / (2 + 1) = 0.667
        assert abs(results["overall_metrics"]["precision"] - 2 / 3) < 0.001
        assert abs(results["overall_metrics"]["recall"] - 2 / 3) < 0.001

    def test_failure_analysis(self):
        """Test failure case analysis."""
        evaluator = GPUClassifierEvaluator()

        # Test without evaluation results
        with pytest.raises(ValueError, match="Must run evaluation before analyzing failures"):
            evaluator.analyze_failures()

        # Create mock test results with known failures
        test_df = pd.DataFrame(
            {
                "title": ["GPU1", "CPU1", "GPU2", "CPU2"],
                "bulk_notes": ["Graphics", "Processor", "Gaming", "Intel"],
                "is_gpu": [1, 0, 1, 0],
            }
        )

        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([0, 1, 1, 0])  # FN at index 0, FP at index 1
        y_pred_proba = np.array(
            [
                [0.6, 0.4],  # FN with low confidence
                [0.3, 0.7],  # FP with high confidence
                [0.2, 0.8],  # Correct
                [0.9, 0.1],  # Correct
            ]
        )

        evaluator.test_results = {
            "y_true": y_true,
            "y_pred": y_pred,
            "y_pred_proba": y_pred_proba,
            "test_df": test_df,
            "metrics": {},
        }

        # Analyze failures
        failure_df = evaluator.analyze_failures(top_k=5)

        # Should have 2 failure cases
        assert len(failure_df) == 2

        # Check failure types
        fp_cases = failure_df[failure_df["error_type"] == "FP"]
        fn_cases = failure_df[failure_df["error_type"] == "FN"]

        assert len(fp_cases) == 1
        assert len(fn_cases) == 1

        # Check that FP case has higher confidence than FN case
        fp_score = fp_cases.iloc[0]["prediction_score"]
        fn_score = fn_cases.iloc[0]["prediction_score"]
        assert fp_score > fn_score  # FP should have higher confidence (0.7 > 0.4)

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.close")
    def test_visualization_generation(self, mock_close, mock_savefig):
        """Test visualization generation."""
        evaluator = GPUClassifierEvaluator()

        # Test without evaluation results
        with pytest.raises(ValueError, match="Must run evaluation before generating visualizations"):
            evaluator.generate_visualizations("test_dir")

        # Create mock test results
        evaluator.test_results = {
            "y_true": np.array([1, 0, 1, 0]),
            "y_pred": np.array([1, 0, 1, 1]),
            "y_pred_proba": np.array([[0.1, 0.9], [0.8, 0.2], [0.2, 0.8], [0.3, 0.7]]),
            "metrics": {
                "overall_metrics": {"roc_auc": 0.85, "average_precision": 0.80},
                "confusion_matrix": {"matrix": [[1, 1], [0, 2]]},
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            plot_files = evaluator.generate_visualizations(temp_dir)

            # Check that all expected plots are generated
            expected_plots = ["confusion_matrix", "roc_curve", "pr_curve"]
            for plot_name in expected_plots:
                assert plot_name in plot_files
                assert temp_dir in plot_files[plot_name]

            # Check that matplotlib functions were called
            assert mock_savefig.call_count == 3  # One for each plot
            assert mock_close.call_count == 3

    def test_evaluation_report_generation(self):
        """Test evaluation report generation."""
        evaluator = GPUClassifierEvaluator()

        # Test without evaluation results
        with pytest.raises(ValueError, match="Must run evaluation before generating report"):
            evaluator.generate_evaluation_report("test_dir", pd.DataFrame())

        # Create mock test results
        evaluator.test_results = {
            "metrics": {
                "overall_metrics": {
                    "accuracy": 0.95,
                    "precision": 0.90,
                    "recall": 0.85,
                    "f1_score": 0.875,
                    "specificity": 0.96,
                    "npv": 0.92,
                    "roc_auc": 0.88,
                    "average_precision": 0.82,
                },
                "dataset_info": {"test_samples": 100, "gpu_samples": 40, "non_gpu_samples": 60, "gpu_ratio": 0.4},
                "confusion_matrix": {"tn": 58, "fp": 2, "fn": 3, "tp": 37},
            }
        }

        # Create empty failure analysis
        failure_analysis = pd.DataFrame()

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = evaluator.generate_evaluation_report(temp_dir, failure_analysis)

            # Check that report file was created
            assert os.path.exists(report_path)
            assert report_path.endswith("evaluation_report.md")

            # Check report content
            with open(report_path, "r") as f:
                content = f.read()

            # Check for key sections
            assert "# Binary GPU Classifier Evaluation Report" in content
            assert "## Executive Summary" in content
            assert "## Key Performance Metrics" in content
            assert "## Confusion Matrix Analysis" in content
            assert "## Performance Assessment" in content
            assert "## Recommendations" in content

            # Check for specific metrics
            assert "0.9500" in content  # Accuracy
            assert "0.9000" in content  # Precision
            assert "0.8500" in content  # Recall

    def test_metrics_saving(self):
        """Test metrics saving to YAML."""
        evaluator = GPUClassifierEvaluator()

        # Test without evaluation results
        with pytest.raises(ValueError, match="Must run evaluation before saving metrics"):
            evaluator.save_metrics("test_dir")

        # Create mock test results
        test_metrics = {
            "overall_metrics": {"accuracy": 0.95, "f1_score": 0.90},
            "confusion_matrix": {"tp": 10, "tn": 15, "fp": 2, "fn": 3},
        }

        evaluator.test_results = {"metrics": test_metrics}

        with tempfile.TemporaryDirectory() as temp_dir:
            metrics_path = evaluator.save_metrics(temp_dir)

            # Check that metrics file was created
            assert os.path.exists(metrics_path)
            assert metrics_path.endswith("metrics.yaml")

            # Check metrics content
            with open(metrics_path, "r") as f:
                loaded_metrics = yaml.safe_load(f)

            assert loaded_metrics["overall_metrics"]["accuracy"] == 0.95
            assert loaded_metrics["overall_metrics"]["f1_score"] == 0.90
            assert loaded_metrics["confusion_matrix"]["tp"] == 10


class TestEvaluationIntegration:
    """Integration tests for the complete evaluation pipeline."""

    def test_end_to_end_evaluation(self):
        """Test complete evaluation pipeline with real components."""
        # Create realistic test data
        test_data = {
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

        test_df = pd.DataFrame(test_data)

        # Create evaluator and mock model
        evaluator = GPUClassifierEvaluator()
        mock_model = MagicMock()

        # Create realistic predictions (mostly correct)
        def mock_predict(X):
            predictions = []
            for text in X:
                text_lower = text.lower()
                if any(keyword in text_lower for keyword in ["gpu", "rtx", "geforce", "nvidia", "a100"]):
                    predictions.append(1)
                else:
                    predictions.append(0)
            return np.array(predictions)

        def mock_predict_proba(X):
            predictions = mock_predict(X)
            probabilities = []
            for pred in predictions:
                if pred == 1:
                    prob = 0.9
                    probabilities.append([1 - prob, prob])
                else:
                    prob = 0.9
                    probabilities.append([prob, 1 - prob])
            return np.array(probabilities)

        mock_model.predict = mock_predict
        mock_model.predict_proba = mock_predict_proba
        evaluator.model = mock_model

        # Run evaluation
        results = evaluator.evaluate_model(test_df)

        # Verify results
        assert results["dataset_info"]["test_samples"] == 8
        assert "overall_metrics" in results
        assert "confusion_matrix" in results

        # Test failure analysis
        failure_analysis = evaluator.analyze_failures(top_k=5)
        assert isinstance(failure_analysis, pd.DataFrame)

        # Test report generation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate report
            report_path = evaluator.generate_evaluation_report(temp_dir, failure_analysis)
            assert os.path.exists(report_path)

            # Save metrics
            metrics_path = evaluator.save_metrics(temp_dir)
            assert os.path.exists(metrics_path)

            # Test visualization generation (mocked)
            with patch("matplotlib.pyplot.savefig"), patch("matplotlib.pyplot.close"):
                plot_files = evaluator.generate_visualizations(temp_dir)
                assert len(plot_files) == 3  # confusion_matrix, roc_curve, pr_curve
