#!/usr/bin/env python3
"""
Model Comparison Evaluator for V1 vs V2 GPU Classifiers

This script evaluates and compares the performance of:
- V1 Model: Title + bulk_notes classifier (gpu_classifier.pkl)
- V2 Model: Title-only classifier (gpu_classifier_v2.pkl)

The evaluation includes:
- Prediction comparison on wamatek_full.csv and perplexity_raw.csv
- Performance metrics and disagreement analysis
- Matplotlib visualizations
- Detailed reporting with insights
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set matplotlib style
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class ModelComparisonEvaluator:
    """
    Comprehensive evaluator for comparing V1 and V2 GPU classifiers.

    This class handles loading models, running predictions, generating metrics,
    creating visualizations, and producing detailed comparison reports.
    """

    def __init__(self, v1_model_path: str, v2_model_path: str, output_dir: str):
        """
        Initialize the evaluator with model paths and output directory.

        Args:
            v1_model_path: Path to V1 model (title + bulk_notes)
            v2_model_path: Path to V2 model (title-only)
            output_dir: Directory to save results and charts
        """
        self.v1_model_path = Path(v1_model_path)
        self.v2_model_path = Path(v2_model_path)
        self.output_dir = Path(output_dir)

        # Create output directories
        self.results_dir = self.output_dir / "results"
        self.charts_dir = self.output_dir / "charts"
        self.workdir = self.output_dir / "workdir"

        for dir_path in [self.results_dir, self.charts_dir, self.workdir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Model containers
        self.v1_model = None
        self.v2_model = None

        # Results storage
        self.evaluation_results = {}

    def load_models(self) -> None:
        """Load both V1 and V2 models."""
        logger.info("Loading models...")

        if not self.v1_model_path.exists():
            raise FileNotFoundError(f"V1 model not found: {self.v1_model_path}")
        if not self.v2_model_path.exists():
            raise FileNotFoundError(f"V2 model not found: {self.v2_model_path}")

        self.v1_model = joblib.load(self.v1_model_path)
        self.v2_model = joblib.load(self.v2_model_path)

        logger.info(f"✅ V1 model loaded from {self.v1_model_path}")
        logger.info(f"✅ V2 model loaded from {self.v2_model_path}")

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess input data for model evaluation.

        Args:
            df: Input DataFrame

        Returns:
            Preprocessed DataFrame
        """
        # Ensure required columns exist
        if "title" not in df.columns:
            raise ValueError("Input data must contain 'title' column")

        # Fill missing values
        df = df.copy()
        df["title"] = df["title"].fillna("")

        # Add bulk_notes if missing (for V1 model compatibility)
        if "bulk_notes" not in df.columns:
            df["bulk_notes"] = ""
        else:
            df["bulk_notes"] = df["bulk_notes"].fillna("")

        return df

    def prepare_v1_features(self, df: pd.DataFrame) -> pd.Series:
        """Prepare features for V1 model (title + bulk_notes)."""
        return df["title"].astype(str) + " " + df["bulk_notes"].astype(str)

    def prepare_v2_features(self, df: pd.DataFrame) -> pd.Series:
        """Prepare features for V2 model (title only)."""
        return df["title"].astype(str)

    def run_predictions(self, dataset_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Run predictions with both models on the given dataset.

        Args:
            dataset_name: Name of the dataset for reporting
            df: Input DataFrame

        Returns:
            Dictionary containing predictions and metrics
        """
        logger.info(f"Running predictions on {dataset_name} ({len(df)} rows)...")

        # Preprocess data
        df_processed = self.preprocess_data(df)

        # Prepare features for each model
        v1_features = self.prepare_v1_features(df_processed)
        v2_features = self.prepare_v2_features(df_processed)

        # Run predictions
        v1_predictions = self.v1_model.predict(v1_features)
        v1_probabilities = self.v1_model.predict_proba(v1_features)[:, 1]

        v2_predictions = self.v2_model.predict(v2_features)
        v2_probabilities = self.v2_model.predict_proba(v2_features)[:, 1]

        # Calculate agreement metrics
        agreement = (v1_predictions == v2_predictions).sum()
        agreement_rate = agreement / len(df_processed)

        # Find disagreements
        disagreements = df_processed[v1_predictions != v2_predictions].copy()
        disagreements["v1_prediction"] = v1_predictions[v1_predictions != v2_predictions]
        disagreements["v1_probability"] = v1_probabilities[v1_predictions != v2_predictions]
        disagreements["v2_prediction"] = v2_predictions[v1_predictions != v2_predictions]
        disagreements["v2_probability"] = v2_probabilities[v1_predictions != v2_predictions]

        # Compile results
        results = {
            "dataset_name": dataset_name,
            "total_samples": len(df_processed),
            "v1_predictions": v1_predictions,
            "v1_probabilities": v1_probabilities,
            "v2_predictions": v2_predictions,
            "v2_probabilities": v2_probabilities,
            "agreement_count": agreement,
            "agreement_rate": agreement_rate,
            "disagreement_count": len(disagreements),
            "disagreement_rate": 1 - agreement_rate,
            "disagreements": disagreements,
            "v1_gpu_count": v1_predictions.sum(),
            "v2_gpu_count": v2_predictions.sum(),
            "v1_gpu_rate": v1_predictions.mean(),
            "v2_gpu_rate": v2_predictions.mean(),
        }

        logger.info(f"✅ {dataset_name} predictions complete:")
        logger.info(f"   Agreement rate: {agreement_rate:.4f} ({agreement}/{len(df_processed)})")
        logger.info(f"   V1 GPU predictions: {v1_predictions.sum()} ({v1_predictions.mean():.4f})")
        logger.info(f"   V2 GPU predictions: {v2_predictions.sum()} ({v2_predictions.mean():.4f})")

        return results

    def create_comparison_charts(self, results: Dict[str, Any]) -> List[str]:
        """
        Create matplotlib charts comparing model performance.

        Args:
            results: Results dictionary from run_predictions

        Returns:
            List of chart file paths
        """
        dataset_name = results["dataset_name"]
        chart_files = []

        # 1. Agreement vs Disagreement Pie Chart
        fig, ax = plt.subplots(figsize=(10, 8))
        labels = ["Agreement", "Disagreement"]
        sizes = [results["agreement_count"], results["disagreement_count"]]
        colors = ["#2ecc71", "#e74c3c"]

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct="%1.2f%%", startangle=90, textprops={"fontsize": 12}
        )

        ax.set_title(f"Model Agreement Analysis - {dataset_name}", fontsize=16, fontweight="bold")

        # Add statistics text
        stats_text = f"""
        Total Samples: {results['total_samples']:,}
        Agreement: {results['agreement_count']:,} ({results['agreement_rate']:.2%})
        Disagreement: {results['disagreement_count']:,} ({results['disagreement_rate']:.2%})
        """
        ax.text(
            1.3,
            0.5,
            stats_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment="center",
            bbox=dict(boxstyle="round", facecolor="lightgray"),
        )

        chart_path = self.charts_dir / f"{dataset_name}_agreement_analysis.png"
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        chart_files.append(str(chart_path))

        # 2. GPU Prediction Comparison Bar Chart
        fig, ax = plt.subplots(figsize=(12, 8))

        models = ["V1 (Title + Bulk Notes)", "V2 (Title Only)"]
        gpu_counts = [results["v1_gpu_count"], results["v2_gpu_count"]]
        gpu_rates = [results["v1_gpu_rate"], results["v2_gpu_rate"]]

        x = np.arange(len(models))
        width = 0.35

        bars1 = ax.bar(x - width / 2, gpu_counts, width, label="GPU Count", color="#3498db")
        ax2 = ax.twinx()
        bars2 = ax2.bar(x + width / 2, gpu_rates, width, label="GPU Rate", color="#e67e22")

        ax.set_xlabel("Model", fontsize=12)
        ax.set_ylabel("GPU Predictions Count", fontsize=12, color="#3498db")
        ax2.set_ylabel("GPU Prediction Rate", fontsize=12, color="#e67e22")
        ax.set_title(f"GPU Prediction Comparison - {dataset_name}", fontsize=16, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(models)

        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(
                f"{int(height):,}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(
                f"{height:.3f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

        chart_path = self.charts_dir / f"{dataset_name}_gpu_prediction_comparison.png"
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        chart_files.append(str(chart_path))

        # 3. Probability Distribution Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # V1 probability distribution
        ax1.hist(results["v1_probabilities"], bins=50, alpha=0.7, color="#3498db", edgecolor="black")
        ax1.set_title("V1 Model - Probability Distribution", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Prediction Probability")
        ax1.set_ylabel("Frequency")
        ax1.grid(True, alpha=0.3)

        # V2 probability distribution
        ax2.hist(results["v2_probabilities"], bins=50, alpha=0.7, color="#e67e22", edgecolor="black")
        ax2.set_title("V2 Model - Probability Distribution", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Prediction Probability")
        ax2.set_ylabel("Frequency")
        ax2.grid(True, alpha=0.3)

        plt.suptitle(f"Prediction Probability Distributions - {dataset_name}", fontsize=16, fontweight="bold")

        chart_path = self.charts_dir / f"{dataset_name}_probability_distributions.png"
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        chart_files.append(str(chart_path))

        # 4. Disagreement Analysis Scatter Plot
        if len(results["disagreements"]) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))

            disagreements = results["disagreements"]

            # Create scatter plot of disagreements
            v1_disagree = disagreements[disagreements["v1_prediction"] == 1]
            v2_disagree = disagreements[disagreements["v2_prediction"] == 1]

            if len(v1_disagree) > 0:
                ax.scatter(
                    v1_disagree["v1_probability"],
                    v1_disagree["v2_probability"],
                    alpha=0.6,
                    c="#e74c3c",
                    s=50,
                    label=f"V1=GPU, V2=Non-GPU ({len(v1_disagree)})",
                )

            if len(v2_disagree) > 0:
                ax.scatter(
                    v2_disagree["v1_probability"],
                    v2_disagree["v2_probability"],
                    alpha=0.6,
                    c="#2ecc71",
                    s=50,
                    label=f"V1=Non-GPU, V2=GPU ({len(v2_disagree)})",
                )

            ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect Agreement")
            ax.set_xlabel("V1 Model Probability")
            ax.set_ylabel("V2 Model Probability")
            ax.set_title(f"Model Disagreement Analysis - {dataset_name}", fontsize=16, fontweight="bold")
            ax.legend()
            ax.grid(True, alpha=0.3)

            chart_path = self.charts_dir / f"{dataset_name}_disagreement_scatter.png"
            plt.tight_layout()
            plt.savefig(chart_path, dpi=300, bbox_inches="tight")
            plt.close()
            chart_files.append(str(chart_path))

        logger.info(f"✅ Created {len(chart_files)} charts for {dataset_name}")
        return chart_files

    def save_results(self, results: Dict[str, Any]) -> str:
        """
        Save detailed results to CSV files.

        Args:
            results: Results dictionary from run_predictions

        Returns:
            Path to main results file
        """
        dataset_name = results["dataset_name"]

        # Save disagreements to CSV
        if len(results["disagreements"]) > 0:
            disagreements_path = self.results_dir / f"{dataset_name}_disagreements.csv"
            results["disagreements"].to_csv(disagreements_path, index=False)
            logger.info(f"✅ Saved disagreements to {disagreements_path}")

        # Save summary results
        summary_data = {
            "metric": [
                "Total Samples",
                "Agreement Count",
                "Agreement Rate",
                "Disagreement Count",
                "Disagreement Rate",
                "V1 GPU Predictions",
                "V1 GPU Rate",
                "V2 GPU Predictions",
                "V2 GPU Rate",
            ],
            "value": [
                results["total_samples"],
                results["agreement_count"],
                f"{results['agreement_rate']:.4f}",
                results["disagreement_count"],
                f"{results['disagreement_rate']:.4f}",
                results["v1_gpu_count"],
                f"{results['v1_gpu_rate']:.4f}",
                results["v2_gpu_count"],
                f"{results['v2_gpu_rate']:.4f}",
            ],
        }

        summary_df = pd.DataFrame(summary_data)
        summary_path = self.results_dir / f"{dataset_name}_summary.csv"
        summary_df.to_csv(summary_path, index=False)

        logger.info(f"✅ Saved summary results to {summary_path}")
        return str(summary_path)

    def evaluate_dataset(self, dataset_path: str, dataset_name: str) -> Dict[str, Any]:
        """
        Complete evaluation pipeline for a single dataset.

        Args:
            dataset_path: Path to the dataset CSV file
            dataset_name: Name for the dataset

        Returns:
            Complete evaluation results
        """
        logger.info(f"🚀 Starting evaluation of {dataset_name}...")

        # Load dataset
        df = pd.read_csv(dataset_path)
        logger.info(f"Loaded {dataset_name}: {len(df)} rows, {len(df.columns)} columns")

        # Run predictions
        results = self.run_predictions(dataset_name, df)

        # Create charts
        chart_files = self.create_comparison_charts(results)
        results["chart_files"] = chart_files

        # Save results
        summary_path = self.save_results(results)
        results["summary_path"] = summary_path

        # Store in evaluation results
        self.evaluation_results[dataset_name] = results

        logger.info(f"✅ Completed evaluation of {dataset_name}")
        return results


def main():
    """Main execution function."""
    logger.info("🎯 Starting V1 vs V2 Model Comparison Evaluation")

    # Initialize evaluator
    evaluator = ModelComparisonEvaluator(
        v1_model_path="models/gpu_classifier.pkl",
        v2_model_path="models/gpu_classifier_v2.pkl",
        output_dir="v2_model_eval",
    )

    # Load models
    evaluator.load_models()

    # Evaluate datasets
    datasets = [
        ("v2_model_eval/input_files/wamatek_full.csv", "wamatek_full"),
        ("v2_model_eval/input_files/perplexity_raw.csv", "perplexity_raw"),
    ]

    for dataset_path, dataset_name in datasets:
        try:
            evaluator.evaluate_dataset(dataset_path, dataset_name)
        except Exception as e:
            logger.error(f"❌ Failed to evaluate {dataset_name}: {e}")
            continue

    logger.info("🎉 Model comparison evaluation completed!")
    logger.info("📁 Results saved to: v2_model_eval/")
    logger.info("📊 Charts saved to: v2_model_eval/charts/")
    logger.info("📋 Detailed results saved to: v2_model_eval/results/")


if __name__ == "__main__":
    main()
