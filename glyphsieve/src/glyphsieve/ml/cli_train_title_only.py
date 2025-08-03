"""
CLI interface for training the title-only binary GPU classifier.

This module provides the command-line interface for training our minimalist
GPU classifier using only title text. As the constraint-loving ML proverb goes:
"Give a person bulk_notes, they'll classify with ease. Take it away, and they'll
discover the true power of titles."
"""

import logging
from pathlib import Path

import click
import pandas as pd

from .train_title_only import TitleOnlyGPUClassifierTrainer

# Configure logging with style
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _validate_and_load_training_data(input_path: Path) -> pd.DataFrame:
    """Validate and load training data for title-only training."""
    if not input_path.exists():
        click.echo(f"❌ Error: Training file {input_path} does not exist", err=True)
        click.echo("💡 Hint: Use the same normalized CSV from previous ML experiments")
        raise click.Abort()

    click.echo(f"📊 Loading training data from {input_path}")
    try:
        train_df = pd.read_csv(input_path)
    except Exception as e:
        click.echo(f"❌ Error reading CSV file: {e}", err=True)
        raise click.Abort()

    # Validate data format - only title and is_gpu required for title-only training
    required_columns = ["title", "is_gpu"]
    missing_columns = [col for col in required_columns if col not in train_df.columns]
    if missing_columns:
        click.echo(f"❌ Error: Missing required columns: {missing_columns}", err=True)
        click.echo(f"📋 Available columns: {list(train_df.columns)}")
        click.echo("💡 Title-only training requires 'title' and 'is_gpu' columns")
        raise click.Abort()

    if len(train_df) == 0:
        click.echo("❌ Error: Training dataset is empty", err=True)
        raise click.Abort()

    return train_df


def _display_dataset_info(train_df: pd.DataFrame) -> None:
    """Display training dataset information for title-only training."""
    gpu_count = train_df["is_gpu"].sum()
    non_gpu_count = len(train_df) - gpu_count
    gpu_ratio = gpu_count / len(train_df)

    click.echo("📈 Title-only dataset summary:")
    click.echo(f"   Total samples: {len(train_df):,}")
    click.echo(f"   GPU samples: {gpu_count:,} ({gpu_ratio:.2%})")
    click.echo(f"   Non-GPU samples: {non_gpu_count:,}")

    # Check for missing titles
    missing_titles = train_df["title"].isna().sum()
    if missing_titles > 0:
        click.echo(f"   ⚠️  Missing titles: {missing_titles:,} ({missing_titles/len(train_df):.2%})")
        click.echo("   💡 Missing titles will be treated as empty strings")


def _display_training_results(results: dict, verbose: bool) -> None:
    """Display title-only training results and hyperparameters."""
    f1_score = results["cv_score_means"]["test_f1"]
    precision = results["cv_score_means"]["test_precision"]
    recall = results["cv_score_means"]["test_recall"]
    accuracy = results["cv_score_means"]["test_accuracy"]

    click.echo("\n🎯 Title-only Training Results:")
    click.echo(f"   F1-Score: {f1_score:.4f}")
    click.echo(f"   Precision: {precision:.4f}")
    click.echo(f"   Recall: {recall:.4f}")
    click.echo(f"   Accuracy: {accuracy:.4f}")

    # Check if target achieved
    if f1_score >= 0.90:
        click.echo("✅ Excellent! Title-only model achieved target performance (≥0.90)!")
        click.echo("🏆 This suggests titles alone carry strong GPU classification signal")
    else:
        click.echo(f"📊 Title-only F1-score ({f1_score:.4f}) below target (0.90)")
        click.echo("💡 This is expected - titles alone may carry less signal than title+bulk_notes")
        click.echo("🔍 Consider this a stress-test of linguistic pattern recognition")

    # Display best hyperparameters
    if verbose:
        click.echo("\n🔧 Best hyperparameters for title-only model:")
        for param, value in results["best_params"].items():
            click.echo(f"   {param}: {value}")


def _save_model_and_display_files(trainer, output_path: Path, metrics_path: str) -> None:
    """Save title-only model and display created files."""
    click.echo(f"\n💾 Saving title-only model to {output_path}")

    try:
        trainer.save_model(str(output_path), metrics_path)

        # Display saved files
        metrics_path_obj = Path(metrics_path)
        click.echo("📁 Files created:")
        click.echo(f"   🤖 Model (v2): {output_path}")
        if metrics_path_obj.exists():
            click.echo(f"   📊 Metrics: {metrics_path_obj}")

    except Exception as e:
        click.echo(f"❌ Error saving title-only model: {e}", err=True)
        raise click.Abort()


@click.command("ml-train-title-only")
@click.option(
    "--input",
    "-i",
    default="tmp/work/stage_normalized.csv",
    help="Path to training CSV file (default: tmp/work/stage_normalized.csv)",
)
@click.option(
    "--output",
    "-o",
    default="models/gpu_classifier_v2.pkl",
    help="Path to save trained model (default: models/gpu_classifier_v2.pkl)",
)
@click.option(
    "--metrics",
    "-m",
    default="models/metrics_title_only.yaml",
    help="Path to save metrics (default: models/metrics_title_only.yaml)",
)
@click.option("--cv-folds", default=5, help="Number of cross-validation folds (default: 5)")
@click.option("--verbose", "-v", is_flag=True, help="Enable detailed logging")
def ml_train_title_only(input: str, output: str, metrics: str, cv_folds: int, verbose: bool) -> None:
    """
    Train title-only binary GPU classifier with TF-IDF and Logistic Regression.

    This command trains a minimalist GPU classifier using ONLY the title field,
    excluding bulk_notes and other auxiliary signals. This stress-tests the
    model's language generalization ability under constraint conditions.

    The title-only approach:
    1. Uses only 'title' text for feature extraction
    2. Applies conservative preprocessing to preserve signal
    3. Employs extended hyperparameter search for reduced signal space
    4. Saves model as v2 to distinguish from full-feature v1
    5. Documents performance delta for robustness analysis

    This is perfect for:
    - Testing model robustness under minimal signal conditions
    - Preparing for deployment on sparse or noisy data sources
    - Understanding the true discriminative power of product titles
    - Creating a lightweight backup classifier

    Example usage:
        uv run glyphsieve ml-train-title-only \\
          --input tmp/work/stage_normalized.csv \\
          --output models/gpu_classifier_v2.pkl \\
          --metrics models/metrics_title_only.yaml \\
          --verbose
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled - prepare for title-only training insights")

    try:
        # Validate and load training data
        input_path = Path(input)
        train_df = _validate_and_load_training_data(input_path)
        _display_dataset_info(train_df)

        # Initialize title-only trainer
        click.echo(f"🧠 Initializing title-only GPU classifier trainer with {cv_folds}-fold CV")
        click.echo("🎯 Training constraint: TITLE FIELD ONLY (no bulk_notes)")
        trainer = TitleOnlyGPUClassifierTrainer(cv_folds=cv_folds)

        click.echo("🚀 Starting title-only training process...")
        click.echo("⏳ This may take longer due to extended hyperparameter search...")
        click.echo("🔍 Testing trigrams and extended regularization for sparse signal space")

        with click.progressbar(length=1, label="Training title-only classifier") as bar:
            results = trainer.train(train_df)
            bar.update(1)

        # Display results and save model
        _display_training_results(results, verbose)
        output_path = Path(output)
        _save_model_and_display_files(trainer, output_path, metrics)

        # Success message with style
        click.echo("\n🎉 Title-only training completed successfully!")
        click.echo("🔮 Your minimalist GPU classifier is ready for constraint-based inference")

        # Performance comparison hint
        click.echo("\n📊 Performance Analysis:")
        f1_score = results["cv_score_means"]["test_f1"]
        click.echo(f"   Title-only F1-Score: {f1_score:.4f}")
        click.echo("   💡 Compare this with v1 (title+bulk_notes) model performance")
        click.echo("   📈 Performance delta reveals bulk_notes signal contribution")

        # Next steps hint
        click.echo("\n💡 Next steps:")
        click.echo("   • Compare disagreement patterns with v1 model")
        click.echo("   • Apply v2 model to perplexity.csv or other sparse sources")
        click.echo("   • Consider v2 as secondary signal in normalizer pipeline")
        click.echo("   • Analyze feature importance to understand title-only patterns")

    except click.Abort:
        raise
    except Exception as e:
        logger.error(f"Title-only training failed with unexpected error: {e}")
        click.echo(f"💥 Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            click.echo(f"🔍 Full traceback:\n{traceback.format_exc()}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ml_train_title_only()
