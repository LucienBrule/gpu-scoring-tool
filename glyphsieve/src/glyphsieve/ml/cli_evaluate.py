"""
CLI interface for evaluating the binary GPU classifier.

This module provides the command-line interface for our model interrogation system.
As the evaluator's motto goes: "Trust, but verify. Then verify again with plots."
"""

import logging
from pathlib import Path

import click
import pandas as pd

from .evaluation import GPUClassifierEvaluator

# Configure logging with style
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _validate_evaluation_inputs(model_path: Path, test_path: Path) -> None:
    """Validate that input files exist."""
    if not model_path.exists():
        click.echo(f"❌ Error: Model file {model_path} does not exist", err=True)
        click.echo("💡 Hint: Run 'glyphsieve ml-train' first to create the model")
        raise click.Abort()

    if not test_path.exists():
        click.echo(f"❌ Error: Test data file {test_path} does not exist", err=True)
        click.echo("💡 Hint: Run 'glyphsieve ml-extract-training-set' first to create test data")
        raise click.Abort()


def _load_and_validate_test_data(test_path: Path) -> pd.DataFrame:
    """Load and validate test data."""
    click.echo(f"📊 Loading test data from {test_path}")
    try:
        test_df = pd.read_csv(test_path)
    except Exception as e:
        click.echo(f"❌ Error reading test CSV file: {e}", err=True)
        raise click.Abort()

    # Validate test data format
    required_columns = ["title", "bulk_notes", "is_gpu"]
    missing_columns = [col for col in required_columns if col not in test_df.columns]
    if missing_columns:
        click.echo(f"❌ Error: Missing required columns in test data: {missing_columns}", err=True)
        click.echo(f"📋 Available columns: {list(test_df.columns)}")
        raise click.Abort()

    if len(test_df) == 0:
        click.echo("❌ Error: Test dataset is empty", err=True)
        raise click.Abort()

    return test_df


def _display_test_dataset_info(test_df: pd.DataFrame) -> None:
    """Display test dataset information."""
    gpu_count = test_df["is_gpu"].sum()
    non_gpu_count = len(test_df) - gpu_count
    gpu_ratio = gpu_count / len(test_df)

    click.echo("📈 Test dataset summary:")
    click.echo(f"   Total samples: {len(test_df):,}")
    click.echo(f"   GPU samples: {gpu_count:,} ({gpu_ratio:.2%})")
    click.echo(f"   Non-GPU samples: {non_gpu_count:,}")


def _display_evaluation_results(results: dict) -> bool:
    """Display evaluation results and return whether criteria are met."""
    overall = results["overall_metrics"]
    cm = results["confusion_matrix"]

    click.echo("\n🎯 Evaluation Results:")
    click.echo(f"   Accuracy:  {overall['accuracy']:.4f}")
    click.echo(f"   Precision: {overall['precision']:.4f}")
    click.echo(f"   Recall:    {overall['recall']:.4f}")
    click.echo(f"   F1-Score:  {overall['f1_score']:.4f}")
    click.echo(f"   ROC-AUC:   {overall['roc_auc']:.4f}")

    # Check if performance meets criteria
    meets_criteria = overall["precision"] >= 0.95 and overall["recall"] >= 0.95 and overall["roc_auc"] >= 0.95

    if meets_criteria:
        click.echo("✅ Model meets all performance criteria (≥95% precision, recall, ROC-AUC)!")
    else:
        click.echo("⚠️  Model performance below target criteria")
        if overall["precision"] < 0.95:
            click.echo(f"   • Precision ({overall['precision']:.3f}) < 0.95")
        if overall["recall"] < 0.95:
            click.echo(f"   • Recall ({overall['recall']:.3f}) < 0.95")
        if overall["roc_auc"] < 0.95:
            click.echo(f"   • ROC-AUC ({overall['roc_auc']:.3f}) < 0.95")

    # Display confusion matrix
    click.echo("\n📊 Confusion Matrix:")
    click.echo(f"   True Negatives:  {cm['tn']:,}")
    click.echo(f"   False Positives: {cm['fp']:,}")
    click.echo(f"   False Negatives: {cm['fn']:,}")
    click.echo(f"   True Positives:  {cm['tp']:,}")

    return meets_criteria


def _generate_evaluation_outputs(
    evaluator, output_path: Path, plots: bool, failure_analysis: pd.DataFrame, top_k: int
) -> tuple[dict, str, str]:
    """Generate all evaluation outputs and return paths."""
    click.echo(f"\n💾 Saving evaluation results to {output_path}")

    # Generate visualizations if requested
    plot_files = {}
    if plots:
        click.echo("📈 Generating visualization plots...")
        try:
            plot_files = evaluator.generate_visualizations(str(output_path))
            click.echo("📁 Visualization files created:")
            for plot_name, plot_path in plot_files.items():
                click.echo(f"   📊 {Path(plot_path).name}")
        except Exception as e:
            click.echo(f"⚠️  Warning: Failed to generate plots: {e}", err=True)

    # Save failure analysis
    if not failure_analysis.empty:
        fp_fn_path = output_path / "fp_fn_sample.csv"
        failure_analysis.to_csv(fp_fn_path, index=False)
        click.echo(f"   📄 {fp_fn_path.name}")

    # Generate evaluation report
    click.echo("📝 Generating comprehensive evaluation report...")
    report_path = evaluator.generate_evaluation_report(str(output_path), failure_analysis)
    click.echo(f"   📋 {Path(report_path).name}")

    # Save metrics
    metrics_path = evaluator.save_metrics(str(output_path))
    click.echo(f"   📊 {Path(metrics_path).name}")

    return plot_files, report_path, metrics_path


@click.command("ml-evaluate")
@click.option(
    "--model",
    "-m",
    default="models/gpu_classifier_v2.pkl",
    help="Path to trained model file (default: models/gpu_classifier_v2.pkl)",
)
@click.option(
    "--test-data",
    "-t",
    default="glyphsieve/ml/data/test.csv",
    help="Path to test CSV file (default: glyphsieve/ml/data/test.csv)",
)
@click.option(
    "--output-dir",
    "-o",
    default="models/evaluation/",
    help="Output directory for evaluation results (default: models/evaluation/)",
)
@click.option("--plots", is_flag=True, help="Generate visualization plots (confusion matrix, ROC, PR curves)")
@click.option(
    "--metrics-format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Format for metrics export (default: yaml)",
)
@click.option("--top-k", default=20, help="Number of top failure cases to analyze (default: 20)")
@click.option("--verbose", "-v", is_flag=True, help="Enable detailed logging")
def ml_evaluate(
    model: str, test_data: str, output_dir: str, plots: bool, metrics_format: str, top_k: int, verbose: bool
) -> None:
    """
    Evaluate binary GPU classifier on held-out test set.

    This command puts the model through rigorous evaluation to uncover any
    hidden flaws, overfitting, or blindspots. We calculate comprehensive metrics,
    generate publication-ready visualizations, and analyze failure cases.

    The evaluator's creed: "Every perfect score is a bug until proven otherwise."

    Example usage:
        uv run glyphsieve ml-evaluate --model models/gpu_classifier_v2.pkl \\
            --test-data glyphsieve/ml/data/test.csv --plots --verbose
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled - prepare for comprehensive analysis")

    try:
        # Validate input files
        model_path = Path(model)
        test_path = Path(test_data)
        _validate_evaluation_inputs(model_path, test_path)

        # Load and validate test data
        test_df = _load_and_validate_test_data(test_path)
        _display_test_dataset_info(test_df)

        # Initialize evaluator and load model
        click.echo("🔍 Initializing GPU classifier evaluator")
        evaluator = GPUClassifierEvaluator()
        click.echo(f"🤖 Loading trained model from {model_path}")
        evaluator.load_model(str(model_path))

        # Run evaluation
        click.echo("🚀 Starting comprehensive model evaluation...")
        click.echo("⏳ This may take a moment - we're being thorough...")
        with click.progressbar(length=1, label="Evaluating model") as bar:
            results = evaluator.evaluate_model(test_df)
            bar.update(1)

        # Display results and check criteria
        meets_criteria = _display_evaluation_results(results)

        # Analyze failure cases
        click.echo(f"\n🔍 Analyzing top-{top_k} failure cases...")
        failure_analysis = evaluator.analyze_failures(top_k=top_k)

        if not failure_analysis.empty:
            fp_count = len(failure_analysis[failure_analysis["error_type"] == "FP"])
            fn_count = len(failure_analysis[failure_analysis["error_type"] == "FN"])
            click.echo(f"   False Positives analyzed: {fp_count}")
            click.echo(f"   False Negatives analyzed: {fn_count}")
        else:
            click.echo("   🎉 No failure cases found - perfect performance!")

        # Generate outputs
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        plot_files, report_path, metrics_path = _generate_evaluation_outputs(
            evaluator, output_path, plots, failure_analysis, top_k
        )

        # Success message with assessment
        overall = results["overall_metrics"]
        click.echo("\n🎉 Evaluation completed successfully!")

        if overall["f1_score"] == 1.0 and overall["roc_auc"] == 1.0:
            click.echo("🤔 Perfect scores detected - this warrants investigation!")
            click.echo("💡 Check the evaluation report for detailed analysis")
        elif meets_criteria:
            click.echo("🔮 Model performance is excellent and ready for production")
        else:
            click.echo("📈 Model shows room for improvement - see report for recommendations")

        # Next steps hint
        click.echo("\n💡 Next steps:")
        click.echo(f"   • Review evaluation report: {Path(report_path).name}")
        if plot_files:
            click.echo("   • Examine visualization plots for insights")
        if not failure_analysis.empty:
            click.echo("   • Analyze failure cases in fp_fn_sample.csv")
        click.echo("   • Consider model integration if performance is satisfactory")

    except click.Abort:
        raise
    except Exception as e:
        logger.error(f"Evaluation failed with unexpected error: {e}")
        click.echo(f"💥 Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            click.echo(f"🔍 Full traceback:\n{traceback.format_exc()}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ml_evaluate()
