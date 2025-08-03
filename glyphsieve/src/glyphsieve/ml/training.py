"""
Binary GPU classifier training pipeline.

This module implements the core training logic for our NVIDIA GPU classification model.
Like Karpathy once said: "All models are wrong, some are just cached." We're building
a TF-IDF + LogisticRegression pipeline that transforms messy listing text into clean
binary predictions.

The architecture follows the principle that "regexes are just transformers with trauma" -
we're healing that trauma with proper statistical learning.
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


class GPUClassifierTrainer:
    """
    Binary GPU classifier trainer using TF-IDF + Logistic Regression.

    This is our epistemic sieve - separating GPU signal from marketplace noise.
    The model learns to distinguish NVIDIA GPUs from the chaos of product listings,
    because as we know: "Don't one-hot encode your identity."
    """

    def __init__(self, cv_folds: int = 5, random_state: int = 42):
        """
        Initialize the trainer.

        Args:
            cv_folds: Number of cross-validation folds (default: 5)
            random_state: Random seed for reproducibility (because chaos is overrated)
        """
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.pipeline = None
        self.best_params = None
        self.cv_results = None

        # Hyperparameter grid inspired by "Attention Is All You Need" (Vaswani et al., 2017)
        # but for the humble TF-IDF realm where n-grams are our attention mechanism
        self.param_grid = {
            "tfidf__max_features": [1000, 5000, 10000],  # Vocabulary size matters
            "tfidf__ngram_range": [(1, 1), (1, 2)],  # Unigrams vs bigrams
            "tfidf__min_df": [2, 5],  # Rare words are often noise
            "tfidf__max_df": [0.95, 0.99],  # Common words are often noise
            "classifier__C": [0.1, 1.0, 10.0],  # Regularization strength
            "classifier__solver": ["liblinear", "lbfgs"],  # Optimization algorithms
        }

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for feature extraction.

        This is where we perform the ancient ritual of text normalization.
        Like cleaning data, it's 80% of the work and 20% of the glory.

        Args:
            text: Raw text to preprocess

        Returns:
            Cleaned text ready for vectorization
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""

        # Convert to lowercase (because GPUs don't care about your caps lock)
        text = text.lower()

        # Remove special characters but keep spaces and alphanumeric
        # This regex is a transformer with less trauma
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _prepare_features(self, df: pd.DataFrame) -> pd.Series:
        """
        Prepare text features by combining title and bulk_notes.

        We concatenate title and bulk_notes because context is king.
        As the ancient ML proverb says: "More data beats clever algorithms."

        Args:
            df: DataFrame with 'title' and 'bulk_notes' columns

        Returns:
            Series of preprocessed combined text
        """
        # Combine title and bulk_notes with a separator
        combined_text = df["title"].fillna("").astype(str) + " " + df["bulk_notes"].fillna("").astype(str)

        # Apply preprocessing to each text
        return combined_text.apply(self._preprocess_text)

    def _create_pipeline(self) -> Pipeline:
        """
        Create the TF-IDF + Logistic Regression pipeline.

        This is our neural pathway from raw text to binary decisions.
        Simple, interpretable, and surprisingly effective - the Honda Civic of ML.

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
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        random_state=self.random_state,
                        max_iter=1000,  # Convergence is not optional
                        class_weight="balanced",  # Handle class imbalance gracefully
                    ),
                ),
            ]
        )

    def train(self, train_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the binary GPU classifier with hyperparameter optimization.

        This is where the magic happens - we transform chaos into order,
        noise into signal, uncertainty into confidence scores.

        Args:
            train_df: Training DataFrame with 'title', 'bulk_notes', 'is_gpu' columns

        Returns:
            Dictionary containing training results and metrics

        Raises:
            ValueError: If required columns are missing or data is invalid
        """
        logger.info("Starting binary GPU classifier training")

        # Validate input data
        required_columns = ["title", "bulk_notes", "is_gpu"]
        missing_columns = [col for col in required_columns if col not in train_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        if len(train_df) == 0:
            raise ValueError("Training dataset is empty")

        # Prepare features and labels
        logger.info("Preparing text features...")
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
        cv_scores = cross_validate(
            self.pipeline,
            X,
            y,
            cv=self.cv_folds,
            scoring=["accuracy", "precision", "recall", "f1"],
            return_train_score=True,
        )

        # Compile results
        results = {
            "best_params": self.best_params,
            "best_cv_score": grid_search.best_score_,
            "cv_scores": {
                "test_accuracy": cv_scores["test_accuracy"].tolist(),
                "test_precision": cv_scores["test_precision"].tolist(),
                "test_recall": cv_scores["test_recall"].tolist(),
                "test_f1": cv_scores["test_f1"].tolist(),
                "train_accuracy": cv_scores["train_accuracy"].tolist(),
                "train_precision": cv_scores["train_precision"].tolist(),
                "train_recall": cv_scores["train_recall"].tolist(),
                "train_f1": cv_scores["train_f1"].tolist(),
            },
            "cv_score_means": {
                "test_accuracy": float(cv_scores["test_accuracy"].mean()),
                "test_precision": float(cv_scores["test_precision"].mean()),
                "test_recall": float(cv_scores["test_recall"].mean()),
                "test_f1": float(cv_scores["test_f1"].mean()),
                "train_accuracy": float(cv_scores["train_accuracy"].mean()),
                "train_precision": float(cv_scores["train_precision"].mean()),
                "train_recall": float(cv_scores["train_recall"].mean()),
                "train_f1": float(cv_scores["train_f1"].mean()),
            },
            "training_samples": len(train_df),
            "class_distribution": {
                "gpu_count": int(class_counts.get(1, 0)),
                "non_gpu_count": int(class_counts.get(0, 0)),
                "gpu_ratio": float(class_counts.get(1, 0) / len(train_df)),
            },
        }

        self.cv_results = results

        # Log final results
        f1_score = results["cv_score_means"]["test_f1"]
        logger.info(f"Training completed! Best F1-score: {f1_score:.4f}")

        if f1_score >= 0.90:
            logger.info("🎯 Target F1-score (≥0.90) achieved!")
        else:
            logger.warning(f"⚠️  F1-score ({f1_score:.4f}) below target (0.90)")

        return results

    def _get_param_combinations(self) -> int:
        """Calculate total number of parameter combinations for logging."""
        total = 1
        for param_values in self.param_grid.values():
            total *= len(param_values)
        return total

    def save_model(self, model_path: str, metrics_path: Optional[str] = None) -> None:
        """
        Save the trained model and metrics.

        Persistence is the art of making ephemeral computations eternal.
        We serialize our learned wisdom for future generations of GPUs.

        Args:
            model_path: Path to save the trained model
            metrics_path: Optional path to save metrics (defaults to same dir as model)

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.pipeline is None:
            raise ValueError("Model must be trained before saving")

        # Create output directory
        model_path_obj = Path(model_path)
        model_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save model using pickle (compatible with GlyphSievePklLoader)
        logger.info(f"Saving trained model to {model_path}")
        import pickle
        with open(model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)

        # Save metrics if results available
        if self.cv_results is not None:
            if metrics_path is None:
                metrics_path = model_path_obj.parent / "metrics.yaml"

            # Prepare complete metrics
            metrics = {
                "model_info": {
                    "model_type": "TF-IDF + Logistic Regression",
                    "training_timestamp": datetime.utcnow().isoformat() + "Z",
                    "model_path": str(model_path),
                    "cv_folds": self.cv_folds,
                    "random_state": self.random_state,
                },
                "hyperparameters": self.best_params,
                "performance": self.cv_results["cv_score_means"],
                "training_data": {
                    "samples": self.cv_results["training_samples"],
                    "class_distribution": self.cv_results["class_distribution"],
                },
                "cross_validation": {
                    "best_f1_score": self.cv_results["best_cv_score"],
                    "detailed_scores": self.cv_results["cv_scores"],
                },
            }

            logger.info(f"Saving training metrics to {metrics_path}")
            with open(metrics_path, "w") as f:
                yaml.dump(metrics, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def load_model(model_path: str) -> Pipeline:
        """
        Load a trained model from disk.

        Resurrection of computational wisdom - bringing models back from the dead.

        Args:
            model_path: Path to the saved model

        Returns:
            Loaded scikit-learn pipeline

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logger.info(f"Loading model from {model_path}")
        import pickle
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    def predict(self, texts: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions on new text data.

        The moment of truth - transforming uncertainty into binary decisions.

        Args:
            texts: Series of text data to classify

        Returns:
            Tuple of (predictions, probabilities)

        Raises:
            ValueError: If model hasn't been trained yet
        """
        if self.pipeline is None:
            raise ValueError("Model must be trained before making predictions")

        # Preprocess texts
        processed_texts = texts.apply(self._preprocess_text)

        # Make predictions
        predictions = self.pipeline.predict(processed_texts)
        probabilities = self.pipeline.predict_proba(processed_texts)

        return predictions, probabilities
