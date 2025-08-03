"""
Binary GPU classifier evaluation pipeline.

This module implements comprehensive evaluation for our NVIDIA GPU classification model.
As the ancient ML wisdom states: "In evaluation we trust, but verify everything twice."
We're here to interrogate the model's claims of perfection and find the truth beneath.

The evaluator's creed: "Every perfect score is a bug until proven otherwise."
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import joblib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

logger = logging.getLogger(__name__)

# Set matplotlib style for publication-ready plots

matplotlib.use("Agg")  # Use non-interactive backend
plt.style.use("default")  # Use default style instead of seaborn
sns.set_palette("husl")


class GPUClassifierEvaluator:
    """
    Binary GPU classifier evaluator with comprehensive metrics and failure analysis.

    This is our truth-seeking missile - designed to find flaws, overfitting, and
    blindspots that the model won't admit. As Karpathy might say: "Trust, but verify.
    Then verify again with different data."
    """

    def __init__(self, random_state: int = 42):
        """
        Initialize the evaluator.

        Args:
            random_state: Random seed for reproducible evaluation
        """
        self.random_state = random_state
        self.model = None
        self.test_results = None

    def load_model(self, model_path: str) -> None:
        """
        Load trained model from disk.

        Args:
            model_path: Path to the trained model file

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logger.info(f"Loading model from {model_path}")
        self.model = joblib.load(model_path)
        logger.info("Model loaded successfully")

    def evaluate_model(self, test_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive evaluation on test dataset.

        This is where we put the model through its paces - no mercy, no shortcuts.
        We calculate every metric that matters and some that don't, because in
        evaluation, paranoia is a feature, not a bug.

        Args:
            test_df: Test DataFrame with 'title', 'bulk_notes', 'is_gpu' columns

        Returns:
            Dictionary containing comprehensive evaluation results

        Raises:
            ValueError: If model hasn't been loaded or data is invalid
        """
        if self.model is None:
            raise ValueError("Model must be loaded before evaluation")

        # Validate test data
        required_columns = ["title", "bulk_notes", "is_gpu"]
        missing_columns = [col for col in required_columns if col not in test_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        if len(test_df) == 0:
            raise ValueError("Test dataset is empty")

        logger.info(f"Evaluating model on {len(test_df)} test samples")

        # Prepare features (same preprocessing as training)
        X_test = self._prepare_features(test_df)
        y_true = test_df["is_gpu"].values

        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)

        # Calculate comprehensive metrics
        results = self._calculate_metrics(y_true, y_pred, y_pred_proba)

        # Add dataset info
        results["dataset_info"] = {
            "test_samples": len(test_df),
            "gpu_samples": int(y_true.sum()),
            "non_gpu_samples": int(len(test_df) - y_true.sum()),
            "gpu_ratio": float(y_true.mean()),
        }

        # Store results for further analysis
        self.test_results = {
            "y_true": y_true,
            "y_pred": y_pred,
            "y_pred_proba": y_pred_proba,
            "test_df": test_df,
            "metrics": results,
        }

        logger.info("Model evaluation completed")
        return results

    def _prepare_features(self, df: pd.DataFrame) -> pd.Series:
        """
        Prepare text features by combining title and bulk_notes.

        This must match the exact preprocessing used during training.
        Any deviation here would be like comparing apples to quantum mechanics.

        Args:
            df: DataFrame with 'title' and 'bulk_notes' columns

        Returns:
            Series of preprocessed combined text
        """
        # Combine title and bulk_notes with a separator
        combined_text = df["title"].fillna("").astype(str) + " " + df["bulk_notes"].fillna("").astype(str)

        # Apply the same preprocessing as training
        return combined_text.apply(self._preprocess_text)

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for feature extraction.

        This must exactly match the preprocessing used during training.
        Even a single character difference could doom our evaluation.

        Args:
            text: Raw text to preprocess

        Returns:
            Cleaned text ready for vectorization
        """
        import re

        if pd.isna(text) or not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove special characters but keep spaces and alphanumeric
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray) -> Dict[str, Any]:
        """
        Calculate comprehensive evaluation metrics.

        We calculate every metric known to ML-kind, because you never know
        which one will reveal the model's dirty secrets.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Prediction probabilities

        Returns:
            Dictionary with all calculated metrics
        """
        # Basic classification metrics
        precision = precision_score(y_true, y_pred, average="binary")
        recall = recall_score(y_true, y_pred, average="binary")
        f1 = f1_score(y_true, y_pred, average="binary")
        accuracy = accuracy_score(y_true, y_pred)

        # Per-class metrics
        precision_per_class = precision_score(y_true, y_pred, average=None)
        recall_per_class = recall_score(y_true, y_pred, average=None)
        f1_per_class = f1_score(y_true, y_pred, average=None)

        # ROC and PR metrics
        roc_auc = roc_auc_score(y_true, y_pred_proba[:, 1])
        avg_precision = average_precision_score(y_true, y_pred_proba[:, 1])

        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()

        # Additional derived metrics
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0  # Negative Predictive Value

        # Classification report for detailed analysis
        class_report = classification_report(y_true, y_pred, output_dict=True)

        return {
            "overall_metrics": {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
                "specificity": float(specificity),
                "npv": float(npv),
                "roc_auc": float(roc_auc),
                "average_precision": float(avg_precision),
            },
            "per_class_metrics": {
                "non_gpu": {
                    "precision": float(precision_per_class[0]),
                    "recall": float(recall_per_class[0]),
                    "f1_score": float(f1_per_class[0]),
                },
                "gpu": {
                    "precision": float(precision_per_class[1]),
                    "recall": float(recall_per_class[1]),
                    "f1_score": float(f1_per_class[1]),
                },
            },
            "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp), "matrix": cm.tolist()},
            "classification_report": class_report,
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def generate_visualizations(self, output_dir: str) -> Dict[str, str]:
        """
        Generate comprehensive evaluation visualizations.

        We create plots that would make Edward Tufte weep with joy.
        Every pixel serves a purpose, every color tells a story.

        Args:
            output_dir: Directory to save visualization files

        Returns:
            Dictionary mapping plot names to file paths

        Raises:
            ValueError: If evaluation hasn't been run yet
        """
        if self.test_results is None:
            raise ValueError("Must run evaluation before generating visualizations")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        plot_files = {}

        # 1. Confusion Matrix
        plot_files["confusion_matrix"] = self._plot_confusion_matrix(output_path)

        # 2. ROC Curve
        plot_files["roc_curve"] = self._plot_roc_curve(output_path)

        # 3. Precision-Recall Curve
        plot_files["pr_curve"] = self._plot_precision_recall_curve(output_path)

        logger.info(f"Generated {len(plot_files)} visualization files in {output_dir}")
        return plot_files

    def _plot_confusion_matrix(self, output_path: Path) -> str:
        """Generate confusion matrix visualization."""
        cm = np.array(self.test_results["metrics"]["confusion_matrix"]["matrix"])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Raw counts
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax1,
            xticklabels=["Non-GPU", "GPU"],
            yticklabels=["Non-GPU", "GPU"],
        )
        ax1.set_title("Confusion Matrix (Raw Counts)")
        ax1.set_ylabel("True Label")
        ax1.set_xlabel("Predicted Label")

        # Normalized
        cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        sns.heatmap(
            cm_norm,
            annot=True,
            fmt=".3f",
            cmap="Blues",
            ax=ax2,
            xticklabels=["Non-GPU", "GPU"],
            yticklabels=["Non-GPU", "GPU"],
        )
        ax2.set_title("Confusion Matrix (Normalized)")
        ax2.set_ylabel("True Label")
        ax2.set_xlabel("Predicted Label")

        plt.tight_layout()

        file_path = output_path / "confusion_matrix.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return str(file_path)

    def _plot_roc_curve(self, output_path: Path) -> str:
        """Generate ROC curve visualization."""
        y_true = self.test_results["y_true"]
        y_pred_proba = self.test_results["y_pred_proba"][:, 1]

        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        roc_auc = self.test_results["metrics"]["overall_metrics"]["roc_auc"]

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC Curve (AUC = {roc_auc:.3f})")
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Random Classifier")

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic (ROC) Curve")
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)

        file_path = output_path / "roc_curve.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return str(file_path)

    def _plot_precision_recall_curve(self, output_path: Path) -> str:
        """Generate precision-recall curve visualization."""
        y_true = self.test_results["y_true"]
        y_pred_proba = self.test_results["y_pred_proba"][:, 1]

        precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
        avg_precision = self.test_results["metrics"]["overall_metrics"]["average_precision"]

        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color="darkorange", lw=2, label=f"PR Curve (AP = {avg_precision:.3f})")

        # Baseline (random classifier)
        baseline = y_true.mean()
        plt.axhline(y=baseline, color="navy", linestyle="--", lw=2, label=f"Random Classifier (AP = {baseline:.3f})")

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall Curve")
        plt.legend(loc="lower left")
        plt.grid(True, alpha=0.3)

        file_path = output_path / "pr_curve.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return str(file_path)

    def analyze_failures(self, top_k: int = 20) -> pd.DataFrame:
        """
        Analyze top false positive and false negative cases.

        This is where we dig into the model's mistakes and try to understand
        what makes it tick (or more importantly, what makes it fail).

        Args:
            top_k: Number of top cases to extract for each error type

        Returns:
            DataFrame with failure analysis

        Raises:
            ValueError: If evaluation hasn't been run yet
        """
        if self.test_results is None:
            raise ValueError("Must run evaluation before analyzing failures")

        y_true = self.test_results["y_true"]
        y_pred = self.test_results["y_pred"]
        y_pred_proba = self.test_results["y_pred_proba"][:, 1]
        test_df = self.test_results["test_df"]

        # Identify false positives and false negatives
        fp_mask = (y_true == 0) & (y_pred == 1)
        fn_mask = (y_true == 1) & (y_pred == 0)

        failure_cases = []

        # Extract false positives (sorted by confidence - highest first)
        if fp_mask.any():
            fp_indices = np.where(fp_mask)[0]
            fp_scores = y_pred_proba[fp_indices]
            fp_sorted_indices = fp_indices[np.argsort(fp_scores)[::-1]]

            for rank, idx in enumerate(fp_sorted_indices[:top_k], 1):
                failure_cases.append(
                    {
                        "title": test_df.iloc[idx]["title"],
                        "bulk_notes": test_df.iloc[idx]["bulk_notes"],
                        "true_label": int(y_true[idx]),
                        "predicted_label": int(y_pred[idx]),
                        "prediction_score": float(y_pred_proba[idx]),
                        "error_type": "FP",
                        "confidence_rank": rank,
                    }
                )

        # Extract false negatives (sorted by confidence - lowest first)
        if fn_mask.any():
            fn_indices = np.where(fn_mask)[0]
            fn_scores = y_pred_proba[fn_indices]
            fn_sorted_indices = fn_indices[np.argsort(fn_scores)]

            for rank, idx in enumerate(fn_sorted_indices[:top_k], 1):
                failure_cases.append(
                    {
                        "title": test_df.iloc[idx]["title"],
                        "bulk_notes": test_df.iloc[idx]["bulk_notes"],
                        "true_label": int(y_true[idx]),
                        "predicted_label": int(y_pred[idx]),
                        "prediction_score": float(y_pred_proba[idx]),
                        "error_type": "FN",
                        "confidence_rank": rank,
                    }
                )

        failure_df = pd.DataFrame(failure_cases)

        logger.info(f"Analyzed {len(failure_cases)} failure cases " f"({fp_mask.sum()} FP, {fn_mask.sum()} FN)")

        return failure_df

    def generate_evaluation_report(self, output_dir: str, failure_analysis: pd.DataFrame) -> str:
        """
        Generate comprehensive evaluation report in Markdown format.

        This is our magnum opus - a report so thorough it would make
        a PhD committee weep with admiration (or boredom).

        Args:
            output_dir: Directory to save the report
            failure_analysis: DataFrame with failure case analysis

        Returns:
            Path to the generated report file
        """
        if self.test_results is None:
            raise ValueError("Must run evaluation before generating report")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        metrics = self.test_results["metrics"]
        dataset_info = metrics["dataset_info"]
        overall = metrics["overall_metrics"]
        cm = metrics["confusion_matrix"]

        # Generate report content
        report_lines = [
            "# Binary GPU Classifier Evaluation Report",
            "",
            f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "**Model:** GPU Binary Classifier (TF-IDF + Logistic Regression)",
            f"**Test Set Size:** {dataset_info['test_samples']:,} samples",
            "",
            "## Executive Summary",
            "",
            f"The binary GPU classifier was evaluated on {dataset_info['test_samples']:,} held-out test samples, "
            f"achieving an **F1-score of {overall['f1_score']:.4f}** and **ROC-AUC of {overall['roc_auc']:.4f}**.",
            "",
            "### Key Performance Metrics",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| **Accuracy** | {overall['accuracy']:.4f} |",
            f"| **Precision** | {overall['precision']:.4f} |",
            f"| **Recall** | {overall['recall']:.4f} |",
            f"| **F1-Score** | {overall['f1_score']:.4f} |",
            f"| **Specificity** | {overall['specificity']:.4f} |",
            f"| **ROC-AUC** | {overall['roc_auc']:.4f} |",
            f"| **Average Precision** | {overall['average_precision']:.4f} |",
            "",
            "## Dataset Composition",
            "",
            f"- **Total Samples:** {dataset_info['test_samples']:,}",
            f"- **GPU Samples:** {dataset_info['gpu_samples']:,} ({dataset_info['gpu_ratio']:.2%})",
            f"- **Non-GPU Samples:** {dataset_info['non_gpu_samples']:,} ({1-dataset_info['gpu_ratio']:.2%})",
            "",
            "## Confusion Matrix Analysis",
            "",
            "| | Predicted Non-GPU | Predicted GPU |",
            "|---|---|---|",
            f"| **Actual Non-GPU** | {cm['tn']} (TN) | {cm['fp']} (FP) |",
            f"| **Actual GPU** | {cm['fn']} (FN) | {cm['tp']} (TP) |",
            "",
            f"- **True Positives (TP):** {cm['tp']} - Correctly identified GPUs",
            f"- **True Negatives (TN):** {cm['tn']} - Correctly identified non-GPUs",
            f"- **False Positives (FP):** {cm['fp']} - Non-GPUs incorrectly classified as GPUs",
            f"- **False Negatives (FN):** {cm['fn']} - GPUs incorrectly classified as non-GPUs",
            "",
        ]

        # Add failure analysis if available
        if not failure_analysis.empty:
            fp_count = len(failure_analysis[failure_analysis["error_type"] == "FP"])
            fn_count = len(failure_analysis[failure_analysis["error_type"] == "FN"])

            report_lines.extend(
                [
                    "## Failure Analysis",
                    "",
                    f"Analyzed top-{max(fp_count, fn_count)} failure cases by prediction confidence:",
                    "",
                    f"- **False Positives:** {fp_count} cases analyzed",
                    f"- **False Negatives:** {fn_count} cases analyzed",
                    "",
                    "### Common Failure Patterns",
                    "",
                    "*(Analysis of failure patterns would be added here based on manual review)*",
                    "",
                ]
            )

        # Add performance assessment
        report_lines.extend(
            [
                "## Performance Assessment",
                "",
                self._generate_performance_assessment(overall),
                "",
                "## Recommendations",
                "",
                self._generate_recommendations(overall, cm),
                "",
                "## Visualizations",
                "",
                "The following visualizations are available in the evaluation directory:",
                "",
                "- `confusion_matrix.png` - Confusion matrix (raw counts and normalized)",
                "- `roc_curve.png` - ROC curve with AUC score",
                "- `pr_curve.png` - Precision-Recall curve with average precision",
                "",
                "---",
                "",
                "*This report was generated automatically by the GPU Classifier Evaluator.*",
            ]
        )

        # Write report to file
        report_path = output_path / "evaluation_report.md"
        with open(report_path, "w") as f:
            f.write("\n".join(report_lines))

        logger.info(f"Evaluation report saved to {report_path}")
        return str(report_path)

    def _generate_performance_assessment(self, metrics: Dict[str, float]) -> str:
        """Generate performance assessment text based on metrics."""
        f1_score = metrics["f1_score"]
        roc_auc = metrics["roc_auc"]
        precision = metrics["precision"]
        recall = metrics["recall"]

        if f1_score >= 0.95 and roc_auc >= 0.95:
            assessment = "**EXCELLENT** - The model demonstrates exceptional performance across all metrics."
        elif f1_score >= 0.90 and roc_auc >= 0.90:
            assessment = "**GOOD** - The model shows strong performance suitable for production use."
        elif f1_score >= 0.80 and roc_auc >= 0.80:
            assessment = "**ACCEPTABLE** - The model performance is adequate but may benefit from improvement."
        else:
            assessment = "**NEEDS IMPROVEMENT** - The model performance is below acceptable thresholds."

        details = []
        if precision < 0.95:
            details.append(f"Precision ({precision:.3f}) indicates some false positive issues.")
        if recall < 0.95:
            details.append(f"Recall ({recall:.3f}) suggests some GPUs are being missed.")
        if roc_auc < 0.95:
            details.append(f"ROC-AUC ({roc_auc:.3f}) indicates room for improvement in ranking quality.")

        result = assessment
        if details:
            result += "\n\n**Areas for attention:**\n" + "\n".join(f"- {detail}" for detail in details)

        return result

    def _generate_recommendations(self, metrics: Dict[str, float], cm: Dict[str, int]) -> str:
        """Generate recommendations based on evaluation results."""
        recommendations = []

        if metrics["f1_score"] >= 0.95:
            recommendations.append("✅ **Ready for Production** - Performance meets deployment criteria.")
        else:
            recommendations.append("⚠️ **Additional Training Needed** - Consider collecting more training data.")

        if cm["fp"] > 0:
            recommendations.append(f"🔍 **Investigate False Positives** - {cm['fp']} non-GPUs misclassified as GPUs.")

        if cm["fn"] > 0:
            recommendations.append(f"🔍 **Investigate False Negatives** - {cm['fn']} GPUs missed by the classifier.")

        if metrics["roc_auc"] < 0.95:
            recommendations.append(
                "📈 **Improve Feature Engineering** - Consider additional text features or preprocessing."
            )

        recommendations.append("📊 **Monitor Performance** - Track metrics on new data to detect drift.")

        return "\n".join(recommendations)

    def save_metrics(self, output_dir: str) -> str:
        """
        Save evaluation metrics to YAML file for programmatic inspection.

        Args:
            output_dir: Directory to save metrics file

        Returns:
            Path to the saved metrics file
        """
        if self.test_results is None:
            raise ValueError("Must run evaluation before saving metrics")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        metrics_path = output_path / "metrics.yaml"

        with open(metrics_path, "w") as f:
            yaml.dump(self.test_results["metrics"], f, default_flow_style=False, sort_keys=False)

        logger.info(f"Metrics saved to {metrics_path}")
        return str(metrics_path)
