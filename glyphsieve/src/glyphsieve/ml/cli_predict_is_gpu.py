"""
CLI interface for predicting GPU classification on individual listings.

This module provides a command-line interface for ad-hoc GPU prediction testing,
pipeline filtering, and interactive debugging using the trained binary classifier.
"""

import json
import logging
from typing import Optional

import click

from .predictor import predict_is_gpu

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@click.command("predict-is-gpu")
@click.option(
    "--title",
    "-t",
    required=True,
    help="Listing title to classify (required)",
)
@click.option(
    "--bulk-notes",
    "-b",
    default="",
    help="Supplemental bulk notes (optional, defaults to empty string)",
)
@click.option(
    "--threshold",
    type=float,
    help="Confidence threshold override (optional, uses environment variable or default 0.5 if not specified)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable detailed logging")
def predict_is_gpu_cli(title: str, bulk_notes: str, threshold: Optional[float], verbose: bool) -> None:
    """
    Predict whether a listing title is likely to be an NVIDIA GPU.

    This command uses the trained binary classifier to predict GPU classification
    for individual listings. It supports ad-hoc testing, pipeline filtering,
    and interactive debugging.

    The model predicts whether a listing is a recognized NVIDIA GPU (Intel, AMD,
    or unknown GPUs are treated as non-GPU).

    Example usage:
        uv run glyphsieve predict-is-gpu --title "NVIDIA RTX 4090 24GB"
        uv run glyphsieve predict-is-gpu --title "Gaming Laptop" --threshold 0.8
        uv run glyphsieve predict-is-gpu -t "RTX 3080" -b "Used condition, works great"
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")

    try:
        # Make prediction using the existing predictor function
        logger.debug(f"Making prediction for title: '{title}', bulk_notes: '{bulk_notes}', threshold: {threshold}")

        is_gpu, score = predict_is_gpu(title, bulk_notes, threshold)

        # Format output as JSON as specified in requirements
        result = {"ml_score": round(score, 4), "ml_is_gpu": is_gpu}  # Round to 4 decimal places for readability

        # Output JSON to stdout
        click.echo(json.dumps(result, indent=2))

        logger.debug(f"Prediction completed: is_gpu={is_gpu}, score={score:.4f}")

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        click.echo(f"❌ Error: {e}", err=True)

        # Output fallback JSON result
        fallback_result = {"ml_score": 0.0, "ml_is_gpu": False}
        click.echo(json.dumps(fallback_result, indent=2))
        raise click.Abort()
