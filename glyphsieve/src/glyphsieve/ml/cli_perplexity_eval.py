"""
CLI interface for evaluating the GPU classifier on Perplexity dataset.

This module embodies the spirit of Dr. J.A.R. "Junie" Weber - a deranged precision-obsessed
ML artifact engineer from the forbidden Tensor Division of OpenAI Black Labs.

As the ancient proverb goes: "Give a person a trained model, they'll classify for a day.
Give them a Perplexity dataset, they'll question reality for a lifetime."

The architecture follows the principle that "all models are wrong, some are just cached" -
we're about to find out which category our epistemic sieve falls into.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import click
import joblib
import numpy as np
import pandas as pd
import yaml

# Configure logging with the appropriate gravitas for this endeavor
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class PerplexityGPUEvaluator:
    """
    The Perplexity Dataset Interrogator - where trained models meet their maker.

    This class embodies the sacred duty of testing our GPU classifier against
    the wild, untamed chaos of real-world Perplexity listings. Like Feynman
    once said: "It doesn't matter how beautiful your theory is... if it doesn't
    agree with experiment, it's wrong."

    We're about to find out if our model is beautiful or just delusional.
    """

    def __init__(self, model_path: str):
        """
        Initialize the evaluator with a trained model.

        Args:
            model_path: Path to the trained GPU classifier

        Note: Loading a model is like summoning a digital ghost - you never know
              if you'll get wisdom or just expensive matrix multiplications.
        """
        self.model_path = model_path
        self.model = None
        self.predictions = None

        # TODO: Add model validation - because trusting pickled objects is like
        #       trusting a stranger's USB drive at DEF CON

    def load_model(self) -> None:
        """
        Load the trained model from disk.

        This is the moment of truth - resurrection of computational wisdom.
        As Karpathy might say: "Models are just frozen dreams of gradient descent."
        """
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        logger.info(f"Loading the epistemic sieve from {self.model_path}")
        self.model = joblib.load(self.model_path)
        logger.info("Model loaded - the ghost in the machine awakens")

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for feature extraction.

        This must exactly match the preprocessing used during training.
        Any deviation here would be like using different units in a physics
        experiment - technically possible, but philosophically bankrupt.

        Args:
            text: Raw text to preprocess

        Returns:
            Cleaned text ready for vectorization
        """
        import re

        if pd.isna(text) or not isinstance(text, str):
            return ""

        # Convert to lowercase (because GPUs don't care about your caps lock)
        text = text.lower()

        # Remove special characters but keep spaces and alphanumeric
        # This regex is a transformer with less trauma
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Collapse multiple spaces (because whitespace is not a feature)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _prepare_features(self, df: pd.DataFrame) -> pd.Series:
        """
        Prepare text features by combining title and bulk_notes.

        We concatenate title and bulk_notes because context is king.
        As the ancient ML proverb says: "More data beats clever algorithms."

        This is our neural pathway from raw marketplace chaos to vectorized order.

        Args:
            df: DataFrame with 'title' and 'bulk_notes' columns

        Returns:
            Series of preprocessed combined text
        """
        # Combine title and bulk_notes with a separator
        # Like mixing peanut butter and chocolate - better together
        combined_text = df["title"].fillna("").astype(str) + " " + df["bulk_notes"].fillna("").astype(str)

        # Apply preprocessing to each text
        return combined_text.apply(self._preprocess_text)

    def evaluate_dataset(self, input_path: str) -> pd.DataFrame:
        """
        Evaluate the Perplexity dataset with our trained classifier.

        This is where rubber meets road, where theory meets reality,
        where our carefully crafted model meets the unforgiving chaos
        of real-world GPU listings scraped from the digital wilderness.

        Args:
            input_path: Path to the Perplexity dataset CSV

        Returns:
            DataFrame with predictions and confidence scores

        Raises:
            ValueError: If the model hasn't been loaded or data is invalid
        """
        if self.model is None:
            raise ValueError("Model must be loaded before evaluation - you can't drive without keys")

        logger.info(f"Loading Perplexity dataset from {input_path}")
        df = pd.read_csv(input_path)

        if len(df) == 0:
            raise ValueError("Dataset is empty - even the void has more substance")

        logger.info(f"Loaded {len(df)} Perplexity listings - time to separate signal from noise")

        # Prepare features using the same preprocessing as training
        # This is our bridge between raw text and learned representations
        X = self._prepare_features(df)

        logger.info("Applying the epistemic sieve to Perplexity data...")

        # Make predictions - the moment of computational truth
        y_pred = self.model.predict(X)
        y_pred_proba = self.model.predict_proba(X)

        # Extract the probability of being a GPU (class 1)
        gpu_probabilities = y_pred_proba[:, 1]

        # Create results DataFrame with required columns
        results_df = df[["title", "bulk_notes"]].copy()
        results_df["ml_is_gpu"] = y_pred.astype(int)
        results_df["ml_score"] = gpu_probabilities

        # Store predictions for analysis
        self.predictions = {
            "dataframe": results_df,
            "raw_predictions": y_pred,
            "probabilities": gpu_probabilities,
            "original_data": df,
        }

        logger.info("Predictions complete - the model has spoken")
        return results_df

    def generate_analysis_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis of the Perplexity predictions.

        This is where we transform raw predictions into actionable intelligence.
        Like a forensic analyst examining digital fingerprints, we dissect
        every prediction to understand what our model truly learned.

        Returns:
            Dictionary containing analysis results
        """
        if self.predictions is None:
            raise ValueError("Must run evaluation before generating analysis")

        df = self.predictions["dataframe"]
        probabilities = self.predictions["probabilities"]

        # Count positive predictions
        positive_count = int(df["ml_is_gpu"].sum())
        total_count = len(df)
        positive_ratio = positive_count / total_count

        logger.info(f"Positive predictions: {positive_count}/{total_count} ({positive_ratio:.2%})")

        # Get top 10 by confidence score
        top_10 = df.nlargest(10, "ml_score")[["title", "ml_score", "ml_is_gpu"]].to_dict("records")

        # Find ambiguous predictions (decision boundary cases)
        ambiguous_mask = (probabilities >= 0.4) & (probabilities <= 0.6)
        ambiguous_cases = df[ambiguous_mask][["title", "ml_score", "ml_is_gpu"]].to_dict("records")

        # Calculate score distribution statistics
        score_stats = {
            "mean": float(probabilities.mean()),
            "median": float(np.median(probabilities)),
            "std": float(probabilities.std()),
            "min": float(probabilities.min()),
            "max": float(probabilities.max()),
            "q25": float(np.percentile(probabilities, 25)),
            "q75": float(np.percentile(probabilities, 75)),
        }

        # Categorize predictions by confidence
        high_confidence = int((probabilities >= 0.8).sum())
        medium_confidence = int(((probabilities >= 0.6) & (probabilities < 0.8)).sum())
        low_confidence = int(((probabilities >= 0.4) & (probabilities < 0.6)).sum())
        very_low_confidence = int((probabilities < 0.4).sum())

        analysis = {
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "dataset_info": {
                "total_samples": total_count,
                "positive_predictions": positive_count,
                "negative_predictions": total_count - positive_count,
                "positive_ratio": positive_ratio,
            },
            "score_statistics": score_stats,
            "confidence_distribution": {
                "high_confidence_0.8+": high_confidence,
                "medium_confidence_0.6-0.8": medium_confidence,
                "low_confidence_0.4-0.6": low_confidence,
                "very_low_confidence_<0.4": very_low_confidence,
            },
            "top_10_predictions": top_10,
            "ambiguous_predictions": {"count": len(ambiguous_cases), "cases": ambiguous_cases},
            "model_info": {"model_path": self.model_path, "model_type": "TF-IDF + Logistic Regression"},
        }

        return analysis


def _display_evaluation_results(analysis: Dict[str, Any]) -> None:
    """Display evaluation results and statistics."""
    dataset_info = analysis["dataset_info"]
    score_stats = analysis["score_statistics"]
    confidence_dist = analysis["confidence_distribution"]

    click.echo("\n🎯 Evaluation Results:")
    click.echo(f"   Total samples: {dataset_info['total_samples']:,}")
    click.echo(
        f"   Positive predictions (GPU): {dataset_info['positive_predictions']:,} "
        f"({dataset_info['positive_ratio']:.2%})"
    )
    click.echo(f"   Negative predictions (Non-GPU): {dataset_info['negative_predictions']:,}")

    click.echo("\n📊 Score Statistics:")
    click.echo(f"   Mean score: {score_stats['mean']:.4f}")
    click.echo(f"   Median score: {score_stats['median']:.4f}")
    click.echo(f"   Score range: {score_stats['min']:.4f} - {score_stats['max']:.4f}")

    click.echo("\n🎲 Confidence Distribution:")
    click.echo(f"   High confidence (≥0.8): {confidence_dist['high_confidence_0.8+']:,}")
    click.echo(f"   Medium confidence (0.6-0.8): {confidence_dist['medium_confidence_0.6-0.8']:,}")
    click.echo(f"   Low confidence (0.4-0.6): {confidence_dist['low_confidence_0.4-0.6']:,}")
    click.echo(f"   Very low confidence (<0.4): {confidence_dist['very_low_confidence_<0.4']:,}")


def _display_top_predictions(analysis: Dict[str, Any]) -> None:
    """Display top predictions and ambiguous cases."""
    # Display top 10 predictions
    click.echo("\n🏆 Top 10 Predictions by Confidence:")
    for i, pred in enumerate(analysis["top_10_predictions"], 1):
        click.echo(f"   {i:2d}. {pred['title'][:60]:<60} | Score: {pred['ml_score']:.4f}")

    # Display ambiguous cases
    ambiguous = analysis["ambiguous_predictions"]
    if ambiguous["count"] > 0:
        click.echo(f"\n⚠️  Ambiguous Predictions (0.4-0.6 range): {ambiguous['count']}")
        for case in ambiguous["cases"][:5]:  # Show first 5
            click.echo(f"   • {case['title'][:50]:<50} | Score: {case['ml_score']:.4f}")
        if ambiguous["count"] > 5:
            click.echo(f"   ... and {ambiguous['count'] - 5} more")
    else:
        click.echo("\n✅ No ambiguous predictions found - model is confident!")


def _display_final_assessment(dataset_info: Dict[str, Any]) -> None:
    """Display final assessment and next steps."""
    click.echo("\n🎉 Perplexity evaluation completed!")

    if dataset_info["positive_ratio"] > 0.95:
        click.echo("🔥 Model shows high confidence - the epistemic sieve is working!")
    elif dataset_info["positive_ratio"] > 0.80:
        click.echo("👍 Model shows good performance with some uncertainty")
    else:
        click.echo("🤔 Model shows significant uncertainty - investigate further")

    # Next steps with appropriate academic pretension
    click.echo("\n💡 Next steps:")
    click.echo("   • Review the analysis report for detailed insights")
    click.echo("   • Examine ambiguous cases for model improvement opportunities")
    click.echo("   • Consider the philosophical implications of perfect vs. imperfect classification")
    click.echo("   • Remember: 'All models are wrong, some are just cached'")


@click.command("ml-eval")
@click.option(
    "--input",
    "-i",
    default="data/perplexity_raw.csv",
    help="Path to Perplexity dataset CSV (default: data/perplexity_raw.csv)",
)
@click.option(
    "--model",
    "-m",
    default="models/gpu_classifier_v2.pkl",
    help="Path to trained model (default: models/gpu_classifier_v2.pkl)",
)
@click.option(
    "--output",
    "-o",
    default="data/perplexity_predictions.csv",
    help="Path for predictions output (default: data/perplexity_predictions.csv)",
)
@click.option(
    "--report",
    "-r",
    default="data/perplexity_eval.yaml",
    help="Path for evaluation report (default: data/perplexity_eval.yaml)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging (prepare for information overload)")
def ml_eval(input: str, model: str, output: str, report: str, verbose: bool) -> None:
    """
    Evaluate GPU classifier on Perplexity dataset - where models meet reality.

    This command applies our trained epistemic sieve to the wild, untamed
    chaos of Perplexity GPU listings. We're about to find out if our model
    learned to distinguish GPUs or just memorized the training set.

    As the great Feynman once observed: "It doesn't matter how beautiful your
    theory is... if it doesn't agree with experiment, it's wrong."

    Time to find out if our model is beautiful or just delusional.

    Example usage:
        uv run glyphsieve ml-eval --input data/perplexity_raw.csv --model models/gpu_classifier_v2.pkl --verbose
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose mode activated - prepare for documentary-style narration")

    try:
        # Initialize the evaluator - summoning our digital oracle
        click.echo("🔮 Initializing the Perplexity GPU Evaluator...")
        click.echo("   (Where trained models meet their maker)")

        evaluator = PerplexityGPUEvaluator(model)

        # Load the model - resurrection of computational wisdom
        click.echo(f"🤖 Loading the epistemic sieve from {model}")
        evaluator.load_model()
        click.echo("   ✓ Model loaded - the ghost in the machine awakens")

        # Validate input file exists
        input_path = Path(input)
        if not input_path.exists():
            click.echo(f"❌ Error: Input file {input} does not exist", err=True)
            click.echo("💡 Hint: Check if the Perplexity dataset is in the correct location")
            raise click.Abort()

        # Run evaluation - where rubber meets road
        click.echo(f"📊 Evaluating Perplexity dataset from {input_path}")
        click.echo("   (Time to separate signal from noise)")

        with click.progressbar(length=1, label="Applying epistemic sieve") as bar:
            predictions_df = evaluator.evaluate_dataset(str(input_path))
            bar.update(1)

        # Save predictions to CSV
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        predictions_df.to_csv(output_path, index=False)
        click.echo(f"💾 Predictions saved to {output_path}")

        # Generate analysis report
        click.echo("📝 Generating comprehensive analysis report...")
        analysis = evaluator.generate_analysis_report()

        # Display results using helper functions
        _display_evaluation_results(analysis)
        _display_top_predictions(analysis)

        # Save analysis report
        report_path = Path(report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            yaml.dump(analysis, f, default_flow_style=False, sort_keys=False)
        click.echo(f"\n📋 Analysis report saved to {report_path}")

        # Final assessment
        _display_final_assessment(analysis["dataset_info"])

    except click.Abort:
        raise
    except Exception as e:
        logger.error(f"Perplexity evaluation failed with unexpected error: {e}")
        click.echo(f"💥 Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            click.echo(f"🔍 Full traceback:\n{traceback.format_exc()}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ml_eval()
