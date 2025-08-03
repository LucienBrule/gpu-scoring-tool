"""
CLI interface for training the binary GPU classifier.

This module provides the command-line interface for training our epistemic sieve.
As the ancient proverb goes: "Give a person a regex, they'll match for a day.
Teach them TF-IDF, they'll classify for a lifetime."
"""

import logging
from pathlib import Path

import click
import pandas as pd

from .training import GPUClassifierTrainer

# Configure logging with style
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _validate_and_load_training_data(input_path: Path) -> pd.DataFrame:
    """Validate and load training data."""
    if not input_path.exists():
        click.echo(f"❌ Error: Training file {input_path} does not exist", err=True)
        click.echo("💡 Hint: Run 'glyphsieve ml-extract-training-set' first to create training data")
        raise click.Abort()

    click.echo(f"📊 Loading training data from {input_path}")
    try:
        train_df = pd.read_csv(input_path)
    except Exception as e:
        click.echo(f"❌ Error reading CSV file: {e}", err=True)
        raise click.Abort()

    # Validate data format
    required_columns = ["title", "bulk_notes", "is_gpu"]
    missing_columns = [col for col in required_columns if col not in train_df.columns]
    if missing_columns:
        click.echo(f"❌ Error: Missing required columns: {missing_columns}", err=True)
        click.echo(f"📋 Available columns: {list(train_df.columns)}")
        raise click.Abort()

    if len(train_df) == 0:
        click.echo("❌ Error: Training dataset is empty", err=True)
        raise click.Abort()

    return train_df


def _display_dataset_info(train_df: pd.DataFrame) -> None:
    """Display training dataset information."""
    gpu_count = train_df["is_gpu"].sum()
    non_gpu_count = len(train_df) - gpu_count
    gpu_ratio = gpu_count / len(train_df)

    click.echo("📈 Dataset summary:")
    click.echo(f"   Total samples: {len(train_df):,}")
    click.echo(f"   GPU samples: {gpu_count:,} ({gpu_ratio:.2%})")
    click.echo(f"   Non-GPU samples: {non_gpu_count:,}")


def _display_training_results(results: dict, verbose: bool) -> None:
    """Display training results and hyperparameters."""
    f1_score = results["cv_score_means"]["test_f1"]
    precision = results["cv_score_means"]["test_precision"]
    recall = results["cv_score_means"]["test_recall"]
    accuracy = results["cv_score_means"]["test_accuracy"]

    click.echo("\n🎯 Training Results:")
    click.echo(f"   F1-Score: {f1_score:.4f}")
    click.echo(f"   Precision: {precision:.4f}")
    click.echo(f"   Recall: {recall:.4f}")
    click.echo(f"   Accuracy: {accuracy:.4f}")

    # Check if target achieved
    if f1_score >= 0.90:
        click.echo("✅ Target F1-score (≥0.90) achieved!")
    else:
        click.echo(f"⚠️  F1-score ({f1_score:.4f}) below target (0.90)")
        click.echo("💡 Consider collecting more training data or adjusting hyperparameters")

    # Display best hyperparameters
    if verbose:
        click.echo("\n🔧 Best hyperparameters:")
        for param, value in results["best_params"].items():
            click.echo(f"   {param}: {value}")


def _save_model_and_display_files(trainer, output_path: Path) -> None:
    """Save model and display created files."""
    click.echo(f"\n💾 Saving model to {output_path}")

    try:
        trainer.save_model(str(output_path))

        # Display saved files
        metrics_path = output_path.parent / "metrics.yaml"
        click.echo("📁 Files created:")
        click.echo(f"   🤖 Model: {output_path}")
        if metrics_path.exists():
            click.echo(f"   📊 Metrics: {metrics_path}")

    except Exception as e:
        click.echo(f"❌ Error saving model: {e}", err=True)
        raise click.Abort()


@click.command("ml-train")
@click.option(
    "--input",
    "-i",
    default="glyphsieve/ml/data/train.csv",
    help="Path to training CSV file (default: glyphsieve/ml/data/train.csv)",
)
@click.option(
    "--output",
    "-o",
    default="models/gpu_classifier_v2.pkl",
    help="Path to save trained model (default: models/gpu_classifier_v2.pkl)",
)
@click.option("--cv-folds", default=5, help="Number of cross-validation folds (default: 5)")
@click.option("--verbose", "-v", is_flag=True, help="Enable detailed logging")
def ml_train(input: str, output: str, cv_folds: int, verbose: bool) -> None:
    """
    Train binary GPU classifier with TF-IDF and Logistic Regression.

    This command transforms raw listing text into learned representations,
    then trains a classifier to distinguish NVIDIA GPUs from the noise.

    The process involves:
    1. Text preprocessing (because clean data is happy data)
    2. TF-IDF feature extraction (turning words into vectors)
    3. Hyperparameter grid search (finding the sweet spot)
    4. Cross-validation (because overfitting is the enemy)
    5. Model persistence (making knowledge immortal)

    Example usage:
        uv run glyphsieve ml-train --input data/train.csv --output models/gpu_classifier_v2.pkl --verbose
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled - prepare for information overload")

    try:
        # Validate and load training data
        input_path = Path(input)
        train_df = _validate_and_load_training_data(input_path)
        _display_dataset_info(train_df)

        # Initialize trainer and train model
        click.echo(f"🧠 Initializing GPU classifier trainer with {cv_folds}-fold CV")
        trainer = GPUClassifierTrainer(cv_folds=cv_folds)

        click.echo("🚀 Starting training process...")
        click.echo("⏳ This may take a few minutes depending on dataset size...")

        with click.progressbar(length=1, label="Training classifier") as bar:
            results = trainer.train(train_df)
            bar.update(1)

        # Display results and save model
        _display_training_results(results, verbose)
        output_path = Path(output)
        _save_model_and_display_files(trainer, output_path)

        # Success message with style
        click.echo("\n🎉 Training completed successfully!")
        click.echo("🔮 Your GPU classifier is ready to transform chaos into order")

        # Next steps hint
        click.echo("\n💡 Next steps:")
        click.echo("   • Run 'glyphsieve ml-evaluate' to test on held-out data")
        click.echo("   • Use the model in the normalization pipeline")
        click.echo("   • Check metrics.yaml for detailed performance analysis")

    except click.Abort:
        raise
    except Exception as e:
        logger.error(f"Training failed with unexpected error: {e}")
        click.echo(f"💥 Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            click.echo(f"🔍 Full traceback:\n{traceback.format_exc()}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ml_train()
