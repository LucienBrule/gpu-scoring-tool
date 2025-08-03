"""
ML predictor module for GPU classification.

This module provides the core prediction functionality for the trained binary GPU classifier,
with model loading, caching, and graceful fallback handling.
"""

import logging
from typing import List, Optional, Tuple

from glyphsieve.core.resources.pkl_loader import GlyphSievePklLoader
from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.ml_config import MLConfig

logger = logging.getLogger(__name__)


class ModelCache:
    """Singleton class to manage ML model loading and caching."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model_cache = None
            cls._instance._model_load_attempted = False
            cls._instance._model_load_warning_logged = False
        return cls._instance

    def get_model(self):
        """Get the cached model, loading it if necessary."""
        if self._model_load_attempted:
            return self._model_cache

        self._model_load_attempted = True

        try:
            # Load ML configuration
            config = self._load_ml_config()

            # Use pkl loader to load model from resources
            pkl_loader = GlyphSievePklLoader()
            self._model_cache = pkl_loader.load(config.model_path)

            # Validate that the model has the required predict_proba method
            if not hasattr(self._model_cache, "predict_proba"):
                if not self._model_load_warning_logged:
                    logger.warning(
                        "Loaded model does not have 'predict_proba' method. ML predictions will default to (False, 0.0)"
                    )
                    self._model_load_warning_logged = True
                self._model_cache = None
                return None

            logger.info(f"Successfully loaded ML model from resources: '{config.model_path}'")
            return self._model_cache

        except Exception as e:
            if not self._model_load_warning_logged:
                logger.warning(f"Failed to load ML model: {e}. ML predictions will default to (False, 0.0)")
                self._model_load_warning_logged = True
            self._model_cache = None
            return None

    def reset_cache(self):
        """Reset the model cache. Useful for testing."""
        self._model_cache = None
        self._model_load_attempted = False
        self._model_load_warning_logged = False

    @staticmethod
    def _load_ml_config() -> MLConfig:
        """Load ML configuration from YAML file."""
        loader = GlyphSieveYamlLoader()
        return loader.load(MLConfig, "configs/ml_config.yaml")


def _get_threshold() -> float:
    """Get the ML threshold from configuration."""
    try:
        loader = GlyphSieveYamlLoader()
        config = loader.load(MLConfig, "configs/ml_config.yaml")
        return config.threshold
    except Exception as e:
        logger.warning(f"Failed to load ML config for threshold: {e}. Using default 0.5")
        return 0.5


def _preprocess_text(title: str, bulk_notes: str) -> str:
    """Preprocess text input for the model."""
    # Concatenate title and bulk_notes, handle None values
    title = title or ""
    bulk_notes = bulk_notes or ""

    # Lowercase and concatenate as specified in requirements
    combined_text = f"{title.lower()} {bulk_notes.lower()}".strip()
    return combined_text


def predict_is_gpu(title: str, bulk_notes: str, threshold: Optional[float] = None) -> Tuple[bool, float]:
    """
    Predict if a listing is an NVIDIA GPU using the trained ML model.

    Args:
        title (str): Listing title
        bulk_notes (str): Supplemental notes
        threshold (float, optional): Confidence threshold. If None, uses environment variable or default 0.5

    Returns:
        tuple:
            - is_gpu (bool): True if confidence >= threshold
            - score (float): Model probability that listing is an NVIDIA GPU (0.0 - 1.0)

    Notes:
        - Text will be lowercased and concatenated as input to the model.
        - Will fallback to (False, 0.0) if model is unavailable.
    """
    # Load model (with caching)
    model_cache = ModelCache()
    model = model_cache.get_model()

    if model is None:
        return False, 0.0

    # Get threshold
    if threshold is None:
        threshold = _get_threshold()

    try:
        # Preprocess input
        processed_text = _preprocess_text(title, bulk_notes)

        # Make prediction
        # Model expects a list of strings for batch prediction
        probabilities = model.predict_proba([processed_text])

        # Extract probability for positive class (GPU)
        # Assuming binary classification where index 1 is the positive class
        if len(probabilities) > 0 and len(probabilities[0]) >= 2:
            score = float(probabilities[0][1])  # Probability of positive class
        else:
            # Fallback if prediction format is unexpected
            logger.warning("Unexpected prediction format from model, defaulting to (False, 0.0)")
            return False, 0.0

        # Apply threshold
        is_gpu = score >= threshold

        return is_gpu, score

    except Exception as e:
        logger.warning(f"Error during ML prediction: {e}. Defaulting to (False, 0.0)")
        return False, 0.0


def predict_batch(
    titles: List[str], bulk_notes_list: List[str], threshold: Optional[float] = None
) -> List[Tuple[bool, float]]:
    """
    Predict GPU classification for a batch of listings.

    Args:
        titles: List of listing titles
        bulk_notes_list: List of supplemental notes (must be same length as titles)
        threshold: Confidence threshold. If None, uses environment variable or default 0.5

    Returns:
        List of (is_gpu, score) tuples
    """
    if len(titles) != len(bulk_notes_list):
        raise ValueError("titles and bulk_notes_list must have the same length")

    # Load model (with caching)
    model_cache = ModelCache()
    model = model_cache.get_model()

    if model is None:
        return [(False, 0.0)] * len(titles)

    # Get threshold
    if threshold is None:
        threshold = _get_threshold()

    try:
        # Preprocess all inputs
        processed_texts = [_preprocess_text(title, bulk_notes) for title, bulk_notes in zip(titles, bulk_notes_list)]

        # Make batch prediction
        probabilities = model.predict_proba(processed_texts)

        results = []
        for prob_array in probabilities:
            if len(prob_array) >= 2:
                score = float(prob_array[1])  # Probability of positive class
                is_gpu = score >= threshold
                results.append((is_gpu, score))
            else:
                # Fallback for unexpected format
                results.append((False, 0.0))

        return results

    except Exception as e:
        logger.warning(f"Error during batch ML prediction: {e}. Defaulting to all (False, 0.0)")
        return [(False, 0.0)] * len(titles)


def reset_model_cache():
    """Reset the model cache. Useful for testing."""
    model_cache = ModelCache()
    model_cache.reset_cache()
