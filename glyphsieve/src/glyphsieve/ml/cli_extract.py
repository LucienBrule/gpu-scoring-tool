"""
CLI interface for extracting labeled training datasets.

This module provides the command-line interface for the ml-extract-training-set
command that processes normalized GPU data into training datasets.
"""

import logging

import click

from .services import MLDatasetService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@click.command("ml-extract-training-set")
@click.option("--input", "-i", required=True, help="Path to the stage_normalized.csv file")
@click.option("--output", "-o", required=True, help="Output directory for training datasets")
@click.option("--test-size", default=0.2, help="Fraction of data to use for test set (default: 0.2 for 80/20 split)")
@click.option("--random-seed", default=42, help="Random seed for reproducible splits")
def ml_extract_training_set(input: str, output: str, test_size: float, random_seed: int) -> None:
    """
    Extract labeled training dataset from normalized GPU data.

    This command reads the normalized CSV file, applies binary labeling logic
    for NVIDIA GPUs, performs data quality checks, and creates stratified
    train/test splits.

    Outputs:
    - training_set.csv: Complete labeled dataset
    - train.csv: Training split (80% by default)
    - test.csv: Test split (20% by default)
    - dataset_info.yaml: Metadata and statistics
    """
    try:
        # Delegate all business logic to the service
        service = MLDatasetService()
        result = service.extract_training_dataset(
            input_path=input, output_dir=output, test_size=test_size, random_seed=random_seed
        )

        # Display results to user
        summary = service.get_extraction_summary(result)
        click.echo(f"\n{summary}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        logger.error(f"Training dataset extraction failed: {e}")
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ml_extract_training_set()
