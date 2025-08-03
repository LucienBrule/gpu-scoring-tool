"""
Title-only GPU classifier training module.

This module provides a specialized trainer that uses only the 'title' field
for GPU classification, excluding 'bulk_notes' and other auxiliary signals.
This stress-tests the model's language generalization ability under minimal
signal conditions.

As the ML wisdom goes: "Constraints breed creativity, and creativity breeds robustness."
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


class TitleOnlyGPUClassifierTrainer:
    """
    Binary GPU classifier trainer using only title text.

    This is the minimalist's approach to GPU classification - no bulk_notes,
    no auxiliary signals, just pure title-based pattern recognition.
    Sometimes less is more, and constraints reveal true signal strength.
    """

    def __init__(self, cv_folds: int = 5, random_state: int = 42):
        """
        Initialize the title-only trainer.

        Args:
            cv_folds: Number of cross-validation folds
            random_state: Random seed for reproducibility
        """
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.pipeline = None
        self.best_params = None
        self.cv_results = None

        # Hyperparameter grid for title-only training
        # Slightly adjusted for the reduced signal space
        self.param_grid = {
            "tfidf__max_features": [1000, 5000, 10000],
            "tfidf__ngram_range": [(1, 1), (1, 2), (1, 3)],  # Added trigrams for title context
            "tfidf__min_df": [1, 2],  # Lower min_df for sparse titles
            "tfidf__max_df": [0.95, 0.98],  # Higher max_df to retain more signal
            "classifier__C": [0.1, 1.0, 10.0, 100.0],  # Extended C range for regularization
            "classifier__solver": ["liblinear", "lbfgs"],
        }

        logger.info(f"Initialized TitleOnlyGPUClassifierTrainer with {cv_folds}-fold CV")

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for title-only classification.

        Since we only have titles, every character matters more.
        We're more conservative with preprocessing to preserve signal.

        Args:
            text: Raw text to preprocess

        Returns:
            Cleaned and normalized text
        """
        if pd.isna(text) or text == "":
            return ""

        # Convert to lowercase
        text = str(text).lower()

        # Remove special characters but keep spaces, alphanumeric, and common GPU terms
        # This regex is a transformer with minimal trauma - we need every signal we can get
        text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _prepare_features(self, df: pd.DataFrame) -> pd.Series:
        """
        Prepare text features using only the title field.

        This is where we embrace the constraint - no bulk_notes safety net,
        just pure title-based signal extraction. Every word counts.

        Args:
            df: DataFrame with 'title' column

        Returns:
            Series of preprocessed title text
        """
        # Use only title field - no concatenation with bulk_notes
        title_text = df["title"].fillna("").astype(str)

        # Apply preprocessing to each title
        return title_text.apply(self._preprocess_text)

    def _create_pipeline(self) -> Pipeline:
        """
        Create the TF-IDF + Logistic Regression pipeline for title-only training.

        This is our neural pathway from title text to binary decisions.
        Optimized for the reduced signal space of titles alone.

        Returns:
            Scikit-learn pipeline ready for training
        """
        return Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        lowercase=True,
                        stop_words="english",  # Remove common English words
                        dtype=np.float32,  # Memory efficiency matters
                        # Default parameters will be overridden by grid search
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        random_state=self.random_state,
                        max_iter=2000,  # Increased for potential convergence issues
                        class_weight="balanced",  # Handle class imbalance gracefully
                    ),
                ),
            ]
        )

    def train(self, train_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the title-only binary GPU classifier with hyperparameter optimization.

        This is where we discover if titles alone can carry the classification burden.
        No safety nets, no auxiliary signals - just pure linguistic pattern matching.

        Args:
            train_df: Training DataFrame with 'title' and 'is_gpu' columns

        Returns:
            Dictionary containing training results and metrics

        Raises:
            ValueError: If required columns are missing or data is invalid
        """
        logger.info("Starting title-only binary GPU classifier training")

        # Validate input data - only title and is_gpu required
        required_columns = ["title", "is_gpu"]
        missing_columns = [col for col in required_columns if col not in train_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        if len(train_df) == 0:
            raise ValueError("Training dataset is empty")

        # Prepare features and labels
        logger.info("Preparing title-only text features...")
        X = self._prepare_features(train_df)
        y = train_df["is_gpu"].values

        # Log class distribution (because balance is everything)
        class_counts = pd.Series(y).value_counts()
        logger.info(f"Class distribution - GPU: {class_counts.get(1, 0)}, Non-GPU: {class_counts.get(0, 0)}")

        # Create pipeline
        pipeline = self._create_pipeline()

        # Perform grid search with cross-validation
        logger.info(f"Starting {self.cv_folds}-fold cross-validation grid search...")
        logger.info(f"Testing {self._get_param_combinations()} parameter combinations")
        logger.info("⚠️  Title-only training may show reduced performance vs. full-feature model")

        grid_search = GridSearchCV(
            pipeline,
            self.param_grid,
            cv=self.cv_folds,
            scoring="f1",  # F1-score balances precision and recall
            n_jobs=-1,  # Use all available cores
            verbose=1,  # Show progress
            return_train_score=True,
        )

        # Fit the grid search
        grid_search.fit(X, y)

        # Store results
        self.pipeline = grid_search.best_estimator_
        self.best_params = grid_search.best_params_

        # Perform detailed cross-validation on best model
        logger.info("Performing detailed cross-validation on best model...")
        cv_results = cross_validate(
            self.pipeline,
            X,
            y,
            cv=self.cv_folds,
            scoring=["precision", "recall", "f1", "accuracy"],
            return_train_score=True,
        )

        self.cv_results = cv_results

        # Calculate mean scores
        cv_score_means = {
            metric: np.mean(scores) for metric, scores in cv_results.items() if metric.startswith("test_")
        }
        cv_score_stds = {
            f"{metric}_std": np.std(scores) for metric, scores in cv_results.items() if metric.startswith("test_")
        }

        # Prepare results dictionary
        results = {
            "model_type": "title_only_gpu_classifier",
            "training_timestamp": datetime.now().isoformat(),
            "dataset_size": len(train_df),
            "class_distribution": {
                "gpu_count": int(class_counts.get(1, 0)),
                "non_gpu_count": int(class_counts.get(0, 0)),
            },
            "cv_folds": self.cv_folds,
            "best_params": self.best_params,
            "cv_score_means": cv_score_means,
            "cv_score_stds": cv_score_stds,
            "param_combinations_tested": self._get_param_combinations(),
            "total_fits": self._get_param_combinations() * self.cv_folds,
        }

        # Log final results
        f1_score = cv_score_means["test_f1"]
        precision = cv_score_means["test_precision"]
        recall = cv_score_means["test_recall"]
        accuracy = cv_score_means["test_accuracy"]

        logger.info("🎯 Title-only training completed!")
        logger.info(f"   F1-Score: {f1_score:.4f}")
        logger.info(f"   Precision: {precision:.4f}")
        logger.info(f"   Recall: {recall:.4f}")
        logger.info(f"   Accuracy: {accuracy:.4f}")

        if f1_score >= 0.90:
            logger.info("✅ Excellent! Title-only model achieved target performance (≥0.90 F1)")
        else:
            logger.info(f"📊 Title-only F1-score: {f1_score:.4f} (may be lower than full-feature model)")
            logger.info("💡 This is expected - titles alone carry less signal than title+bulk_notes")

        return results

    def _get_param_combinations(self) -> int:
        """Calculate total number of parameter combinations."""
        combinations = 1
        for param_values in self.param_grid.values():
            combinations *= len(param_values)
        return combinations

    def save_model(self, model_path: str, metrics_path: Optional[str] = None) -> None:
        """
        Save the trained title-only model and metrics.

        Args:
            model_path: Path to save the model file
            metrics_path: Optional path to save metrics (defaults to same dir as model)

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.pipeline is None:
            raise ValueError("Model must be trained before saving")

        # Create output directory if it doesn't exist
        model_path_obj = Path(model_path)
        model_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save model
        logger.info(f"Saving title-only model to {model_path}")
        joblib.dump(self.pipeline, model_path)

        # Save metrics
        if metrics_path is None:
            metrics_path = model_path_obj.parent / "metrics_title_only.yaml"
        else:
            metrics_path = Path(metrics_path)

        if self.cv_results is not None:
            # Prepare metrics for YAML serialization
            metrics = {
                "model_info": {
                    "type": "title_only_gpu_classifier",
                    "training_timestamp": datetime.now().isoformat(),
                    "model_path": str(model_path),
                    "cv_folds": self.cv_folds,
                    "random_state": self.random_state,
                },
                "best_hyperparameters": self.best_params,
                "cross_validation_scores": {
                    "precision_mean": float(np.mean(self.cv_results["test_precision"])),
                    "precision_std": float(np.std(self.cv_results["test_precision"])),
                    "recall_mean": float(np.mean(self.cv_results["test_recall"])),
                    "recall_std": float(np.std(self.cv_results["test_recall"])),
                    "f1_mean": float(np.mean(self.cv_results["test_f1"])),
                    "f1_std": float(np.std(self.cv_results["test_f1"])),
                    "accuracy_mean": float(np.mean(self.cv_results["test_accuracy"])),
                    "accuracy_std": float(np.std(self.cv_results["test_accuracy"])),
                },
                "hyperparameter_search": {
                    "param_combinations_tested": self._get_param_combinations(),
                    "total_fits": self._get_param_combinations() * self.cv_folds,
                },
            }

            logger.info(f"Saving title-only metrics to {metrics_path}")
            with open(metrics_path, "w") as f:
                yaml.dump(metrics, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def load_model(model_path: str) -> Pipeline:
        """
        Load a trained title-only model.

        Args:
            model_path: Path to the saved model file

        Returns:
            Loaded scikit-learn pipeline

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logger.info(f"Loading title-only model from {model_path}")
        return joblib.load(model_path)

    def predict(self, titles: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions using the trained title-only model.

        Args:
            titles: Series of title text to classify

        Returns:
            Tuple of (predictions, probabilities)

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.pipeline is None:
            raise ValueError("Model must be trained before making predictions")

        # Preprocess titles
        processed_titles = titles.apply(self._preprocess_text)

        # Make predictions
        predictions = self.pipeline.predict(processed_titles)
        probabilities = self.pipeline.predict_proba(processed_titles)[:, 1]  # Probability of GPU class

        return predictions, probabilities
