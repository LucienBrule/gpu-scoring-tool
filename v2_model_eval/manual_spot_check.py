#!/usr/bin/env python3
"""
Manual Spot Check Script for V1 vs V2 Model Predictions

This script provides an interactive interface for manually inspecting
model predictions and disagreements to validate model behavior and
identify patterns in classification differences.
"""

import logging
import random
from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ManualSpotChecker:
    """
    Interactive spot checker for manual validation of model predictions.

    Provides tools for sampling predictions, inspecting disagreements,
    and generating manual validation reports.
    """

    def __init__(self, v1_model_path: str, v2_model_path: str):
        """
        Initialize the spot checker with model paths.

        Args:
            v1_model_path: Path to V1 model
            v2_model_path: Path to V2 model
        """
        self.v1_model_path = Path(v1_model_path)
        self.v2_model_path = Path(v2_model_path)

        # Load models
        self.v1_model = joblib.load(self.v1_model_path)
        self.v2_model = joblib.load(self.v2_model_path)

        logger.info("✅ Models loaded successfully")

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        Prepare features for both models.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (v1_features, v2_features)
        """
        # Ensure required columns exist and fill missing values
        df = df.copy()
        df["title"] = df["title"].fillna("")

        if "bulk_notes" not in df.columns:
            df["bulk_notes"] = ""
        else:
            df["bulk_notes"] = df["bulk_notes"].fillna("")

        # Prepare features
        v1_features = df["title"].astype(str) + " " + df["bulk_notes"].astype(str)
        v2_features = df["title"].astype(str)

        return v1_features, v2_features

    def get_predictions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get predictions from both models and add to DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with prediction columns added
        """
        result_df = df.copy()

        # Prepare features
        v1_features, v2_features = self.prepare_features(df)

        # Get predictions
        result_df["v1_prediction"] = self.v1_model.predict(v1_features)
        result_df["v1_probability"] = self.v1_model.predict_proba(v1_features)[:, 1]
        result_df["v2_prediction"] = self.v2_model.predict(v2_features)
        result_df["v2_probability"] = self.v2_model.predict_proba(v2_features)[:, 1]

        # Add agreement flag
        result_df["models_agree"] = result_df["v1_prediction"] == result_df["v2_prediction"]

        return result_df

    def display_sample(self, row: pd.Series, index: int = None) -> None:
        """
        Display a formatted sample for manual inspection.

        Args:
            row: DataFrame row to display
            index: Optional index number for display
        """
        print("=" * 80)
        if index is not None:
            print(f"SAMPLE #{index}")
        print("=" * 80)

        # Basic info
        print(f"📋 TITLE: {row.get('title', 'N/A')}")
        print(f"📝 BULK NOTES: {row.get('bulk_notes', 'N/A')}")
        print(f"💰 PRICE: ${row.get('price', 'N/A')}")
        print(f"🏪 SELLER: {row.get('seller', 'N/A')}")
        print(f"🌍 REGION: {row.get('geographic_region', 'N/A')}")

        print("\n" + "-" * 40)
        print("MODEL PREDICTIONS")
        print("-" * 40)

        # V1 predictions
        v1_pred = "GPU" if row.get("v1_prediction", 0) == 1 else "Non-GPU"
        v1_prob = row.get("v1_probability", 0)
        print(f"🤖 V1 (Title + Bulk): {v1_pred} (confidence: {v1_prob:.4f})")

        # V2 predictions
        v2_pred = "GPU" if row.get("v2_prediction", 0) == 1 else "Non-GPU"
        v2_prob = row.get("v2_probability", 0)
        print(f"🎯 V2 (Title Only):   {v2_pred} (confidence: {v2_prob:.4f})")

        # Agreement status
        agree = row.get("models_agree", True)
        status = "✅ AGREE" if agree else "❌ DISAGREE"
        print(f"🔄 Agreement: {status}")

        if not agree:
            print(f"📊 Confidence Gap: {abs(v1_prob - v2_prob):.4f}")

        print("=" * 80)
        print()

    def spot_check_random_samples(self, df: pd.DataFrame, n_samples: int = 10) -> None:
        """
        Display random samples for manual inspection.

        Args:
            df: DataFrame with predictions
            n_samples: Number of samples to display
        """
        print(f"🎲 RANDOM SAMPLE SPOT CHECK ({n_samples} samples)")
        print("=" * 80)

        # Get random samples
        sample_indices = random.sample(range(len(df)), min(n_samples, len(df)))

        for i, idx in enumerate(sample_indices, 1):
            row = df.iloc[idx]
            self.display_sample(row, i)

            # Pause for manual review
            input("Press Enter to continue to next sample...")

    def spot_check_disagreements(self, df: pd.DataFrame, max_samples: int = None) -> None:
        """
        Display all disagreement cases for manual inspection.

        Args:
            df: DataFrame with predictions
            max_samples: Maximum number of disagreements to show
        """
        disagreements = df[~df["models_agree"]].copy()

        if len(disagreements) == 0:
            print("✅ No disagreements found - models agree on all predictions!")
            return

        n_show = len(disagreements) if max_samples is None else min(max_samples, len(disagreements))

        print(f"❌ DISAGREEMENT SPOT CHECK ({n_show}/{len(disagreements)} cases)")
        print("=" * 80)

        for i, (_, row) in enumerate(disagreements.head(n_show).iterrows(), 1):
            self.display_sample(row, i)

            # Get manual assessment
            print("🤔 MANUAL ASSESSMENT:")
            print("   1 = GPU (correct)")
            print("   0 = Non-GPU (correct)")
            print("   s = Skip")
            print("   q = Quit spot check")

            while True:
                user_input = input("Your assessment: ").strip().lower()
                if user_input in ["1", "0", "s", "q"]:
                    break
                print("Please enter 1, 0, s, or q")

            if user_input == "q":
                break
            elif user_input == "s":
                continue
            else:
                manual_label = int(user_input)
                v1_correct = row["v1_prediction"] == manual_label
                v2_correct = row["v2_prediction"] == manual_label

                print("📊 Manual Assessment Results:")
                print(f"   V1 Model: {'✅ Correct' if v1_correct else '❌ Incorrect'}")
                print(f"   V2 Model: {'✅ Correct' if v2_correct else '❌ Incorrect'}")

                if v1_correct and v2_correct:
                    print("   🤔 Both models correct - interesting disagreement!")
                elif not v1_correct and not v2_correct:
                    print("   😬 Both models incorrect - challenging case!")
                elif v2_correct:
                    print("   🎯 V2 (Title-only) model wins!")
                else:
                    print("   🤖 V1 (Full-feature) model wins!")

            print("\n" + "=" * 80 + "\n")
            input("Press Enter to continue to next disagreement...")

    def spot_check_high_confidence_errors(self, df: pd.DataFrame, confidence_threshold: float = 0.8) -> None:
        """
        Display cases where models have high confidence but disagree.

        Args:
            df: DataFrame with predictions
            confidence_threshold: Minimum confidence to consider "high"
        """
        # Find high-confidence disagreements
        disagreements = df[~df["models_agree"]].copy()
        high_conf_disagreements = disagreements[
            (disagreements["v1_probability"] > confidence_threshold)
            | (disagreements["v2_probability"] > confidence_threshold)
        ]

        if len(high_conf_disagreements) == 0:
            print(f"✅ No high-confidence disagreements found (threshold: {confidence_threshold})")
            return

        print(f"🔥 HIGH-CONFIDENCE DISAGREEMENTS (confidence > {confidence_threshold})")
        print("=" * 80)

        for i, (_, row) in enumerate(high_conf_disagreements.iterrows(), 1):
            self.display_sample(row, i)
            input("Press Enter to continue...")

    def generate_spot_check_report(self, df: pd.DataFrame, output_path: str = "spot_check_report.md") -> None:
        """
        Generate a markdown report with spot check findings.

        Args:
            df: DataFrame with predictions
            output_path: Path to save the report
        """
        disagreements = df[~df["models_agree"]].copy()

        report_content = f"""# Manual Spot Check Report

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dataset:** {len(df)} samples analyzed  
**Disagreements:** {len(disagreements)} cases ({len(disagreements)/len(df)*100:.2f}%)

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Samples | {len(df):,} |
| Model Agreements | {len(df) - len(disagreements):,} ({(len(df) - len(disagreements))/len(df)*100:.2f}%) |
| Model Disagreements | {len(disagreements):,} ({len(disagreements)/len(df)*100:.2f}%) |
| V1 GPU Predictions | {df['v1_prediction'].sum():,} ({df['v1_prediction'].mean()*100:.2f}%) |
| V2 GPU Predictions | {df['v2_prediction'].sum():,} ({df['v2_prediction'].mean()*100:.2f}%) |

## Disagreement Patterns

"""

        if len(disagreements) > 0:
            # Analyze disagreement patterns
            v1_gpu_v2_non = len(
                disagreements[(disagreements["v1_prediction"] == 1) & (disagreements["v2_prediction"] == 0)]
            )
            v1_non_v2_gpu = len(
                disagreements[(disagreements["v1_prediction"] == 0) & (disagreements["v2_prediction"] == 1)]
            )

            report_content += f"""
| Pattern | Count | Percentage |
|---------|-------|------------|
| V1=GPU, V2=Non-GPU | {v1_gpu_v2_non} | {v1_gpu_v2_non/len(disagreements)*100:.1f}% |
| V1=Non-GPU, V2=GPU | {v1_non_v2_gpu} | {v1_non_v2_gpu/len(disagreements)*100:.1f}% |

### Sample Disagreement Cases

"""

            # Show top 5 disagreements by confidence gap
            disagreements["confidence_gap"] = abs(disagreements["v1_probability"] - disagreements["v2_probability"])
            top_disagreements = disagreements.nlargest(5, "confidence_gap")

            for i, (_, row) in enumerate(top_disagreements.iterrows(), 1):
                v1_pred = "GPU" if row["v1_prediction"] == 1 else "Non-GPU"
                v2_pred = "GPU" if row["v2_prediction"] == 1 else "Non-GPU"

                report_content += f"""
#### Case {i}: {row.get('title', 'N/A')}

- **Title:** {row.get('title', 'N/A')}
- **Bulk Notes:** {row.get('bulk_notes', 'N/A')}
- **V1 Prediction:** {v1_pred} (confidence: {row['v1_probability']:.4f})
- **V2 Prediction:** {v2_pred} (confidence: {row['v2_probability']:.4f})
- **Confidence Gap:** {row['confidence_gap']:.4f}

"""

        report_content += """
## Manual Review Guidelines

When manually reviewing disagreements:

1. **Focus on Title Clarity:** Is the GPU model clearly stated in the title?
2. **Assess Bulk Notes Quality:** Do bulk notes add helpful information or introduce noise?
3. **Consider Context:** Does the listing context (seller, price, etc.) support the prediction?
4. **Evaluate Confidence:** Are high-confidence predictions more reliable?

## Recommendations

Based on spot check findings:

- Use V2 model when bulk_notes contain promotional/shipping language
- Use V1 model when bulk_notes contain technical specifications
- Consider ensemble approach for maximum robustness
- Monitor disagreement patterns in production

---

*Report generated by Manual Spot Checker v1.0*
"""

        # Save report
        output_path = Path(output_path)
        with open(output_path, "w") as f:
            f.write(report_content)

        logger.info(f"✅ Spot check report saved to {output_path}")


def main():
    """Main interactive spot check interface."""
    print("🔍 V1 vs V2 Model Manual Spot Checker")
    print("=" * 50)

    # Initialize spot checker
    checker = ManualSpotChecker(
        v1_model_path="../models/gpu_classifier.pkl", v2_model_path="../models/gpu_classifier_v2.pkl"
    )

    # Load datasets
    datasets = {
        "1": ("input_files/wamatek_full.csv", "Wamatek Full Dataset"),
        "2": ("input_files/perplexity_raw.csv", "Perplexity Raw Dataset"),
    }

    print("\nAvailable datasets:")
    for key, (path, name) in datasets.items():
        print(f"  {key}. {name}")

    dataset_choice = input("\nSelect dataset (1 or 2): ").strip()

    if dataset_choice not in datasets:
        print("Invalid choice. Exiting.")
        return

    dataset_path, dataset_name = datasets[dataset_choice]

    print(f"\n📊 Loading {dataset_name}...")
    df = pd.read_csv(dataset_path)
    df_with_predictions = checker.get_predictions(df)

    print(f"✅ Loaded {len(df)} samples with predictions")

    # Interactive menu
    while True:
        print("\n" + "=" * 50)
        print("SPOT CHECK OPTIONS")
        print("=" * 50)
        print("1. Random sample spot check")
        print("2. Review all disagreements")
        print("3. High-confidence disagreements")
        print("4. Generate spot check report")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            n_samples = input("Number of random samples (default 10): ").strip()
            n_samples = int(n_samples) if n_samples.isdigit() else 10
            checker.spot_check_random_samples(df_with_predictions, n_samples)

        elif choice == "2":
            max_samples = input("Max disagreements to review (default all): ").strip()
            max_samples = int(max_samples) if max_samples.isdigit() else None
            checker.spot_check_disagreements(df_with_predictions, max_samples)

        elif choice == "3":
            threshold = input("Confidence threshold (default 0.8): ").strip()
            threshold = float(threshold) if threshold else 0.8
            checker.spot_check_high_confidence_errors(df_with_predictions, threshold)

        elif choice == "4":
            output_file = input("Report filename (default spot_check_report.md): ").strip()
            output_file = output_file if output_file else "spot_check_report.md"
            checker.generate_spot_check_report(df_with_predictions, output_file)

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
