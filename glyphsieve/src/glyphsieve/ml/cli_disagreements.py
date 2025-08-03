"""
CLI command for identifying and analyzing disagreements between rule-based and ML classification.

This module provides the `ml-disagreements` command that identifies cases where the
rule-based normalization system and ML classifier disagree on GPU classification.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

import click
import pandas as pd

from .disagreement_analysis import DisagreementAnalyzer, load_disagreement_config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _validate_parameters(min_confidence: float, max_rows: int) -> None:
    """Validate input parameters."""
    if min_confidence < 0.0 or min_confidence > 1.0:
        click.echo("❌ Error: min-confidence must be between 0.0 and 1.0", err=True)
        raise click.Abort()

    if max_rows <= 0:
        click.echo("❌ Error: max-rows must be positive", err=True)
        raise click.Abort()


def _load_and_validate_data(input_path: Path) -> pd.DataFrame:
    """Load and validate input data."""
    if not input_path.exists():
        click.echo(f"❌ Error: Input file {input_path} does not exist", err=True)
        click.echo("💡 Hint: Run normalization with --use-ml flag first")
        raise click.Abort()

    click.echo(f"📊 Loading input data from {input_path}")
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        click.echo(f"❌ Error reading input CSV file: {e}", err=True)
        raise click.Abort()

    # Validate required columns
    required_columns = ["canonical_model", "ml_is_gpu", "ml_score", "title", "bulk_notes"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        click.echo(f"❌ Error: Missing required columns: {missing_columns}", err=True)
        click.echo(f"📋 Available columns: {list(df.columns)}")
        click.echo("💡 Hint: Ensure input file has ML predictions (run with --use-ml)")
        raise click.Abort()

    if len(df) == 0:
        click.echo("❌ Error: Input dataset is empty", err=True)
        raise click.Abort()

    return df


def _display_dataset_info(df: pd.DataFrame, min_confidence: float) -> None:
    """Display dataset information."""
    total_rows = len(df)
    ml_predictions = df["ml_is_gpu"].sum()
    rule_gpus = len(df[df["canonical_model"] != "UNKNOWN"])

    click.echo("📈 Input dataset summary:")
    click.echo(f"   Total rows: {total_rows:,}")
    click.echo(f"   ML GPU predictions: {ml_predictions:,}")
    click.echo(f"   Rule-based GPU classifications: {rule_gpus:,}")
    click.echo(f"   Using confidence threshold: {min_confidence}")


def _generate_outputs(
    disagreements: pd.DataFrame,
    output_path: Path,
    max_rows: int,
    debug_json: bool,
    summary_stats: Dict[str, Any],
    analyzer: DisagreementAnalyzer,
    config: Any,
) -> None:
    """Generate all output files."""
    # Sort disagreements by priority and confidence
    disagreements_sorted = disagreements.sort_values(["priority_score", "ml_score"], ascending=[False, False])

    # Limit output rows if requested
    if len(disagreements_sorted) > max_rows:
        click.echo(f"📝 Limiting output to top {max_rows} disagreements " f"(from {len(disagreements_sorted)} total)")
        disagreements_output = disagreements_sorted.head(max_rows)
    else:
        disagreements_output = disagreements_sorted

    # Prepare output columns
    output_columns = [
        "title",
        "bulk_notes",
        "canonical_model",
        "ml_is_gpu",
        "ml_score",
        "disagreement_type",
        "confidence_level",
        "priority_score",
    ]

    # Ensure all columns exist
    for col in output_columns:
        if col not in disagreements_output.columns:
            click.echo(f"⚠️  Warning: Column {col} not found in disagreements data")

    # Write disagreements CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    click.echo(f"💾 Writing disagreements to {output_path}")
    disagreements_output[output_columns].to_csv(output_path, index=False)

    # Generate debug JSON if requested
    if debug_json:
        debug_path = output_path.with_suffix(".debug.json")
        click.echo(f"🐛 Writing debug JSON to {debug_path}")

        # Get top 50 disagreements for debug
        top_disagreements = disagreements_sorted.head(50)
        debug_data = {
            "summary": summary_stats,
            "top_disagreements": top_disagreements.to_dict("records"),
            "config": config.dict(),
        }

        with open(debug_path, "w") as f:
            json.dump(debug_data, f, indent=2, default=str)

    # Generate summary report
    summary_path = output_path.parent / "disagreement_summary.md"
    click.echo(f"📋 Writing summary report to {summary_path}")
    _generate_summary_report(summary_path, summary_stats, analyzer, disagreements, config)

    # Final status
    click.echo("\n✅ Disagreement analysis complete!")
    click.echo(f"   📄 Disagreements CSV: {output_path}")
    click.echo(f"   📋 Summary report: {summary_path}")
    if debug_json:
        click.echo(f"   🐛 Debug JSON: {debug_path}")

    click.echo("\n🎯 Next steps:")
    click.echo(f"   1. Review high-priority disagreements in {output_path}")
    click.echo(f"   2. Check summary insights in {summary_path}")
    click.echo("   3. Use findings to improve rule-based or ML systems")


@click.command("ml-disagreements")
@click.option(
    "--input",
    "-i",
    required=True,
    help="Path to normalized CSV with ML columns (required)",
)
@click.option(
    "--output",
    "-o",
    default="disagreements.csv",
    help="Path for disagreements CSV output (default: disagreements.csv)",
)
@click.option(
    "--min-confidence",
    "-c",
    default=0.7,
    type=float,
    help="Minimum ML confidence threshold (default: 0.7)",
)
@click.option(
    "--max-rows",
    "-m",
    default=1000,
    type=int,
    help="Limit output rows for large datasets (default: 1000)",
)
@click.option(
    "--debug-json",
    is_flag=True,
    help="Generate debug JSON file with full metadata for top disagreements",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable detailed logging",
)
def ml_disagreements(
    input: str,
    output: str,
    min_confidence: float,
    max_rows: int,
    debug_json: bool,
    verbose: bool,
) -> None:
    """
    Identify and score disagreements between rule-based and ML classification systems.

    This command analyzes normalized CSV files with ML predictions to find cases where
    the rule-based system and ML classifier disagree. These disagreements represent
    potential improvements to either system and require analyst review.

    Two types of disagreements are identified:
    - Type A: Rules classify as UNKNOWN but ML predicts is_gpu = 1
    - Type B: Rules classify as known GPU but ML predicts is_gpu = 0

    Example usage:
        uv run glyphsieve ml-disagreements \\
            --input tmp/work/normalized_with_ml.csv \\
            --output tmp/analysis/disagreements.csv \\
            --min-confidence 0.7 \\
            --max-rows 1000
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled - detailed disagreement analysis")

    try:
        # Validate input parameters
        _validate_parameters(min_confidence, max_rows)

        # Load and validate input data
        input_path = Path(input)
        df = _load_and_validate_data(input_path)

        # Display dataset info
        _display_dataset_info(df, min_confidence)

        # Load configuration
        click.echo("⚙️  Loading disagreement scoring configuration")
        try:
            config = load_disagreement_config()
        except Exception as e:
            click.echo(f"❌ Error loading configuration: {e}", err=True)
            raise click.Abort()

        # Initialize analyzer and identify disagreements
        analyzer = DisagreementAnalyzer(config)
        click.echo("🔍 Analyzing disagreements between rule-based and ML systems...")
        with click.progressbar(length=1, label="Identifying disagreements") as bar:
            disagreements = analyzer.identify_disagreements(df, min_confidence)
            bar.update(1)

        if len(disagreements) == 0:
            click.echo("✅ No disagreements found!")
            click.echo("   This indicates strong agreement between systems.")
            click.echo("   Consider lowering --min-confidence to find more cases.")
            return

        # Generate and display summary statistics
        summary_stats = analyzer.generate_summary_stats(disagreements, len(df))
        click.echo("\n📊 Disagreement Analysis Summary:")
        click.echo(f"   Total disagreements: {summary_stats['total_disagreements']:,}")
        click.echo(f"   Disagreement rate: {summary_stats['disagreement_rate']:.2f}%")
        click.echo(f"   High priority cases: {summary_stats['high_priority_count']:,}")

        if summary_stats["disagreement_rate"] > 3.0:
            click.echo("⚠️  Warning: Disagreement rate exceeds 3% target threshold")
        else:
            click.echo("✅ Disagreement rate within acceptable range (<3%)")

        # Generate all outputs
        output_path = Path(output)
        _generate_outputs(disagreements, output_path, max_rows, debug_json, summary_stats, analyzer, config)

    except click.Abort:
        raise
    except Exception as e:
        logger.exception("Unexpected error during disagreement analysis")
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


def _generate_summary_report(
    output_path: Path,
    summary_stats: Dict[str, Any],
    analyzer: DisagreementAnalyzer,
    disagreements: pd.DataFrame,
    config: Any,
) -> None:
    """
    Generate a comprehensive summary report in Markdown format.

    Args:
        output_path: Path to write the summary report
        summary_stats: Summary statistics dictionary
        analyzer: DisagreementAnalyzer instance
        disagreements: DataFrame with all disagreements
        config: Disagreement scoring configuration
    """
    with open(output_path, "w") as f:
        f.write("# Disagreement Analysis Summary Report\n\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Overall statistics
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Total disagreements found**: {summary_stats['total_disagreements']:,}\n")
        f.write(f"- **Disagreement rate**: {summary_stats['disagreement_rate']:.2f}%\n")
        f.write(f"- **High priority cases**: {summary_stats['high_priority_count']:,}\n")
        f.write(f"- **Average priority score**: {summary_stats.get('avg_priority_score', 0):.2f}\n\n")

        # Target assessment
        if summary_stats["disagreement_rate"] <= 3.0:
            f.write("✅ **Status**: Disagreement rate is within the target threshold (<3%)\n\n")
        else:
            f.write("⚠️ **Status**: Disagreement rate exceeds target threshold (>3%)\n\n")

        # Breakdown by type
        f.write("## Breakdown by Disagreement Type\n\n")
        for disagreement_type, count in summary_stats["type_breakdown"].items():
            percentage = (count / summary_stats["total_disagreements"]) * 100
            f.write(f"- **{disagreement_type}**: {count:,} cases ({percentage:.1f}%)\n")
        f.write("\n")

        # Breakdown by confidence
        f.write("## Breakdown by Confidence Level\n\n")
        for confidence_level, count in summary_stats["confidence_breakdown"].items():
            percentage = (count / summary_stats["total_disagreements"]) * 100
            f.write(f"- **{confidence_level}**: {count:,} cases ({percentage:.1f}%)\n")
        f.write("\n")

        # Top disagreements by type
        f.write("## Top 10 Disagreements by Type\n\n")
        top_by_type = analyzer.get_top_disagreements_by_type(disagreements, 10)

        for disagreement_type, top_cases in top_by_type.items():
            f.write(f"### {disagreement_type.replace('_', ' ').title()}\n\n")
            if len(top_cases) > 0:
                for idx, (_, row) in enumerate(top_cases.head(5).iterrows(), 1):
                    title = str(row["title"])[:100] + "..." if len(str(row["title"])) > 100 else str(row["title"])
                    f.write(
                        f"{idx}. **Priority {row['priority_score']:.1f}** | ML Score: {row['ml_score']:.3f} | {title}\n"
                    )
            else:
                f.write("No cases found.\n")
            f.write("\n")

        # Recommendations
        f.write("## Recommendations for System Improvements\n\n")

        if "rules_unknown_ml_gpu" in summary_stats["type_breakdown"]:
            count = summary_stats["type_breakdown"]["rules_unknown_ml_gpu"]
            f.write("### Rules System Enhancement\n")
            f.write(f"- Found {count} cases where rules classified as UNKNOWN but ML identified as GPU\n")
            f.write("- Consider expanding rule patterns to capture these missed GPU cases\n")
            f.write("- Review high-confidence ML predictions for new rule patterns\n\n")

        if "rules_gpu_ml_unknown" in summary_stats["type_breakdown"]:
            count = summary_stats["type_breakdown"]["rules_gpu_ml_unknown"]
            f.write("### ML Model Enhancement\n")
            f.write(f"- Found {count} cases where rules identified GPU but ML classified as non-GPU\n")
            f.write("- Consider retraining ML model with additional features\n")
            f.write("- Review rule-based classifications for potential false positives\n\n")

        # Statistical patterns
        f.write("## Statistical Analysis of Disagreement Patterns\n\n")

        if len(disagreements) > 0:
            # Confidence distribution
            high_conf = len(disagreements[disagreements["confidence_level"] == "high"])
            med_conf = len(disagreements[disagreements["confidence_level"] == "medium"])
            low_conf = len(disagreements[disagreements["confidence_level"] == "low"])

            f.write("### Confidence Distribution\n")
            f.write(f"- High confidence disagreements: {high_conf} ({high_conf / len(disagreements) * 100:.1f}%)\n")
            f.write(f"- Medium confidence disagreements: {med_conf} ({med_conf / len(disagreements) * 100:.1f}%)\n")
            f.write(f"- Low confidence disagreements: {low_conf} ({low_conf / len(disagreements) * 100:.1f}%)\n\n")

            # Priority distribution
            high_priority = len(disagreements[disagreements["priority_score"] > 7])
            med_priority = len(
                disagreements[(disagreements["priority_score"] >= 4) & (disagreements["priority_score"] <= 7)]
            )
            low_priority = len(disagreements[disagreements["priority_score"] < 4])

            f.write("### Priority Distribution\n")
            f.write(f"- High priority (>7): {high_priority} cases\n")
            f.write(f"- Medium priority (4-7): {med_priority} cases\n")
            f.write(f"- Low priority (<4): {low_priority} cases\n\n")

        # Configuration used
        f.write("## Configuration Used\n\n")
        f.write(f"- High confidence threshold: {config.high_confidence_threshold}\n")
        f.write(f"- Medium confidence threshold: {config.medium_confidence_threshold}\n")
        f.write("- Priority scoring weights:\n")
        f.write(f"  - Confidence weight: {config.confidence_weight}\n")
        f.write(f"  - Disagreement type weight: {config.disagreement_type_weight}\n")
        f.write(f"  - Text complexity weight: {config.text_complexity_weight}\n")
        f.write(f"  - Frequency weight: {config.frequency_weight}\n")
