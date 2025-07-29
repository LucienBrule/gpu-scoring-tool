"""
Reporting module for glyphsieve.

This module provides functionality for generating human-readable reports from scored GPU datasets.
It includes functions for calculating statistics, generating highlight sections, and formatting
the report in Markdown.
"""

import os
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
from rich.console import Console

# Initialize rich console for formatted output
console = Console()


def calculate_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate summary statistics for a scored GPU dataset.

    Args:
        df: Input DataFrame with scored GPU listings

    Returns:
        Dict[str, Any]: Dictionary of summary statistics
    """
    stats = {
        "num_listings": len(df),
        "unique_models": df["canonical_model"].nunique(),
        "price_min": df["price"].min(),
        "price_max": df["price"].max(),
        "price_avg": df["price"].mean(),
        "price_median": df["price"].median(),
        "score_min": df["score"].min(),
        "score_max": df["score"].max(),
        "score_mean": df["score"].mean(),
        "most_common_model": df["canonical_model"].value_counts().idxmax(),
    }
    return stats


def get_top_cards_by_score(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get the top N cards by score.

    Args:
        df: Input DataFrame with scored GPU listings
        n: Number of cards to return

    Returns:
        pd.DataFrame: DataFrame with top N cards
    """
    return df.sort_values("score", ascending=False).head(n)


def get_top_cards_by_score_per_dollar(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get the top N cards by score per dollar.

    Args:
        df: Input DataFrame with scored GPU listings
        n: Number of cards to return

    Returns:
        pd.DataFrame: DataFrame with top N cards by score per dollar
    """
    # Create a copy to avoid modifying the original
    result_df = df.copy()

    # Calculate score per dollar (avoid division by zero)
    result_df["score_per_dollar"] = result_df.apply(
        lambda row: row["score"] / row["price"] if row["price"] > 0 else 0, axis=1
    )

    return result_df.sort_values("score_per_dollar", ascending=False).head(n)


def get_best_value_cards_under_price(df: pd.DataFrame, price_limit: float = 2000.0, n: int = 10) -> pd.DataFrame:
    """
    Get the best value cards under a price limit.

    Args:
        df: Input DataFrame with scored GPU listings
        price_limit: Maximum price
        n: Number of cards to return

    Returns:
        pd.DataFrame: DataFrame with best value cards under the price limit
    """
    # Filter cards under the price limit
    filtered_df = df[df["price"] <= price_limit]

    # Sort by score and return top N
    return filtered_df.sort_values("score", ascending=False).head(n)


def find_price_anomalies(df: pd.DataFrame, threshold: float = 0.3) -> pd.DataFrame:
    """
    Find cards with identical models but widely varying prices.

    Args:
        df: Input DataFrame with scored GPU listings
        threshold: Threshold for price variation (as a fraction of the mean price)

    Returns:
        pd.DataFrame: DataFrame with price anomalies
    """
    # Group by canonical_model and calculate price statistics
    price_stats = df.groupby("canonical_model")["price"].agg(["mean", "std", "count"])

    # Filter for models with multiple listings and significant price variation
    anomalies = price_stats[(price_stats["count"] > 1) & (price_stats["std"] > threshold * price_stats["mean"])]

    # Get the listings for these models
    if not anomalies.empty:
        return df[df["canonical_model"].isin(anomalies.index)]
    else:
        return pd.DataFrame()


def find_duplicate_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find listings flagged as DUPLICATE_SECONDARY that had a higher score than their primary.

    Args:
        df: Input DataFrame with scored GPU listings

    Returns:
        pd.DataFrame: DataFrame with duplicate anomalies
    """
    # Check if the DataFrame has the duplicate_flag column
    if "duplicate_flag" not in df.columns:
        return pd.DataFrame()

    # Find DUPLICATE_SECONDARY listings
    secondary_dupes = df[df["duplicate_flag"] == "DUPLICATE_SECONDARY"]

    # If there are no secondary duplicates, return empty DataFrame
    if secondary_dupes.empty:
        return pd.DataFrame()

    # Find anomalies where secondary has higher score than primary
    anomalies = []

    for _, row in secondary_dupes.iterrows():
        # Find the primary listing (assuming there's a primary_id column)
        if "primary_id" in df.columns:
            primary = df[df["id"] == row["primary_id"]]
            if not primary.empty and primary.iloc[0]["score"] < row["score"]:
                anomalies.append(row)

    return pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


def _generate_header_section() -> List[str]:
    """Generate the report header with title and timestamp."""
    now = datetime.now()
    return ["# GPU Market Insight Report", f"*Generated on {now.strftime('%Y-%m-%d %H:%M:%S')}*", ""]


def _generate_summary_section(stats: dict) -> List[str]:
    """Generate the summary statistics section."""
    return [
        "## 📈 Summary Statistics",
        "",
        f"- **Number of listings:** {stats['num_listings']}",
        f"- **Unique models:** {stats['unique_models']}",
        f"- **Price range:** ${stats['price_min']:.2f} - ${stats['price_max']:.2f}",
        f"- **Average price:** ${stats['price_avg']:.2f}",
        f"- **Median price:** ${stats['price_median']:.2f}",
        f"- **Score range:** {stats['score_min']:.4f} - {stats['score_max']:.4f}",
        f"- **Average score:** {stats['score_mean']:.4f}",
        f"- **Most common model:** {stats['most_common_model']}",
        "",
    ]


def _generate_top_cards_section(top_by_score: pd.DataFrame) -> List[str]:
    """Generate the top cards by score section."""
    lines = [
        "## 🏆 Top 10 Cards by Score",
        "",
        "| Rank | Model | Score | VRAM (GB) | Price ($) |",
        "|------|-------|-------|-----------|-----------|",
    ]

    for i, (_, row) in enumerate(top_by_score.iterrows(), 1):
        model = row.get("canonical_model", "Unknown")
        score = row.get("score", 0)
        vram = row.get("vram_gb", "N/A")
        price = row.get("price", "N/A")
        lines.append(f"| {i} | {model} | {score:.4f} | {vram} | {price:.2f} |")

    lines.append("")
    return lines


def _generate_score_per_dollar_section(top_by_score_per_dollar: pd.DataFrame) -> List[str]:
    """Generate the top cards by score-per-dollar section."""
    lines = [
        "## 💰 Top 10 Cards by Score-per-Dollar",
        "",
        "| Rank | Model | Score/$ | Score | Price ($) |",
        "|------|-------|---------|-------|-----------|",
    ]

    for i, (_, row) in enumerate(top_by_score_per_dollar.iterrows(), 1):
        model = row.get("canonical_model", "Unknown")
        score = row.get("score", 0)
        price = row.get("price", "N/A")
        score_per_dollar = row.get("score_per_dollar", 0)
        lines.append(f"| {i} | {model} | {score_per_dollar:.6f} | {score:.4f} | {price:.2f} |")

    lines.append("")
    return lines


def _generate_best_value_section(best_value_under_2000: pd.DataFrame) -> List[str]:
    """Generate the best value cards under $2000 section."""
    lines = ["## 🔥 Best Value Cards Under $2000", ""]

    if not best_value_under_2000.empty:
        lines.extend(
            ["| Rank | Model | Score | VRAM (GB) | Price ($) |", "|------|-------|-------|-----------|-----------|"]
        )

        for i, (_, row) in enumerate(best_value_under_2000.iterrows(), 1):
            model = row.get("canonical_model", "Unknown")
            score = row.get("score", 0)
            vram = row.get("vram_gb", "N/A")
            price = row.get("price", "N/A")
            lines.append(f"| {i} | {model} | {score:.4f} | {vram} | {price:.2f} |")
    else:
        lines.append("*No cards found under $2000*")

    lines.append("")
    return lines


def _generate_price_anomalies_section(price_anomalies: pd.DataFrame) -> List[str]:
    """Generate the price anomalies section."""
    lines = ["## 📉 Price Anomalies", "*Cards with identical models but widely varying prices*", ""]

    if not price_anomalies.empty:
        model_groups = price_anomalies.groupby("canonical_model")

        lines.extend(
            [
                "| Model | Min Price ($) | Max Price ($) | Difference ($) | Difference (%) |",
                "|-------|---------------|---------------|----------------|----------------|",
            ]
        )

        for model, group in model_groups:
            min_price = group["price"].min()
            max_price = group["price"].max()
            diff = max_price - min_price
            pct_diff = (diff / min_price) * 100 if min_price > 0 else float("inf")
            lines.append(f"| {model} | {min_price:.2f} | {max_price:.2f} | {diff:.2f} | {pct_diff:.2f}% |")
    else:
        lines.append("*No significant price anomalies found*")

    lines.append("")
    return lines


def _generate_duplicate_anomalies_section(duplicate_anomalies: pd.DataFrame, df: pd.DataFrame) -> List[str]:
    """Generate the duplicate anomalies section."""
    lines = [
        "## 🔄 Duplicate Anomalies",
        "*Listings flagged as DUPLICATE_SECONDARY with higher scores than their primary*",
        "",
    ]

    if not duplicate_anomalies.empty:
        lines.extend(
            [
                "| Secondary Model | Secondary Score | Primary Model | Primary Score |",
                "|-----------------|-----------------|---------------|---------------|",
            ]
        )

        for _, row in duplicate_anomalies.iterrows():
            sec_model = row.get("canonical_model", "Unknown")
            sec_score = row.get("score", 0)

            # Find primary info (assuming there's a primary_id column)
            if "primary_id" in df.columns:
                primary = df[df["id"] == row["primary_id"]]
                if not primary.empty:
                    prim_model = primary.iloc[0].get("canonical_model", "Unknown")
                    prim_score = primary.iloc[0].get("score", 0)
                    lines.append(f"| {sec_model} | {sec_score:.4f} | {prim_model} | {prim_score:.4f} |")
    else:
        lines.append("*No duplicate anomalies found*")

    lines.append("")
    return lines


def _generate_quantization_capacity_section(df: pd.DataFrame) -> List[str]:
    """
    Generate the quantization capacity section.

    This section shows the number of models of different sizes (7B, 13B, 70B) that can fit
    on each GPU based on its VRAM.

    Args:
        df: Input DataFrame with quantization capacity data

    Returns:
        List[str]: Lines of markdown text for the section
    """
    lines = [
        "## 🧠 Quantization Capacity",
        "*Number of models of different sizes that can fit on each GPU based on VRAM*",
        "",
    ]

    # Check if quantization capacity columns exist
    if (
        "quantization_capacity.7b" in df.columns
        and "quantization_capacity.13b" in df.columns
        and "quantization_capacity.70b" in df.columns
    ):
        # Get top 10 GPUs by 7B model capacity
        top_by_7b = df.sort_values("quantization_capacity.7b", ascending=False).head(10)

        if not top_by_7b.empty:
            lines.extend(
                [
                    "| Model | VRAM (GB) | 7B Models | 13B Models | 70B Models |",
                    "|-------|-----------|-----------|------------|------------|",
                ]
            )

            for _, row in top_by_7b.iterrows():
                model = row.get("canonical_model", "Unknown")
                vram = row.get("vram_gb", 0)
                cap_7b = row.get("quantization_capacity.7b", 0)
                cap_13b = row.get("quantization_capacity.13b", 0)
                cap_70b = row.get("quantization_capacity.70b", 0)

                lines.append(f"| {model} | {vram} | {cap_7b} | {cap_13b} | {cap_70b} |")
        else:
            lines.append("*No quantization capacity data available*")
    else:
        lines.append("*Quantization capacity data not included in this report*")

    lines.append("")
    return lines


def generate_markdown_report(df: pd.DataFrame, output_path: str) -> str:
    """
    Generate a Markdown report from a scored GPU dataset.

    Args:
        df: Input DataFrame with scored GPU listings
        output_path: Path to save the report

    Returns:
        str: Path to the generated report
    """
    # Calculate statistics
    stats = calculate_summary_statistics(df)
    top_by_score = get_top_cards_by_score(df)
    top_by_score_per_dollar = get_top_cards_by_score_per_dollar(df)
    best_value_under_2000 = get_best_value_cards_under_price(df)
    price_anomalies = find_price_anomalies(df)
    duplicate_anomalies = find_duplicate_anomalies(df)

    # Generate each section
    report = []
    report.extend(_generate_header_section())
    report.extend(_generate_summary_section(stats))
    report.extend(_generate_top_cards_section(top_by_score))
    report.extend(_generate_score_per_dollar_section(top_by_score_per_dollar))
    report.extend(_generate_best_value_section(best_value_under_2000))

    # Add quantization capacity section if data is available
    if all(
        col in df.columns
        for col in ["quantization_capacity.7b", "quantization_capacity.13b", "quantization_capacity.70b"]
    ):
        report.extend(_generate_quantization_capacity_section(df))

    report.extend(_generate_price_anomalies_section(price_anomalies))
    report.extend(_generate_duplicate_anomalies_section(duplicate_anomalies, df))

    # Write report to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(report))

    return output_path


def generate_report(
    input_file: str, output_dir: Optional[str] = None, output_format: str = "md", quantize_capacity: bool = False
) -> str:
    """
    Generate a report from a scored GPU dataset.

    Args:
        input_file: Path to input CSV file with scored GPU listings
        output_dir: Directory to save the report (default: reports/YYYY-MM-DD/)
        output_format: Output format (md or html, default: md)
        quantize_capacity: Whether to include quantization capacity in the report (default: False)

    Returns:
        str: Path to the generated report
    """
    # Load the input CSV
    df = pd.read_csv(input_file)

    # Apply quantization capacity calculation if requested
    if quantize_capacity and "vram_gb" in df.columns:
        from glyphsieve.core.heuristics import (
            QuantizationCapacityHeuristic,
            load_quantization_capacity_config,
        )

        # Create a temporary file for the calculation
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Load configuration and create heuristic
            config = load_quantization_capacity_config()
            heuristic = QuantizationCapacityHeuristic(config)

            # Apply the heuristic to each row
            for idx, row in df.iterrows():
                result = heuristic.evaluate(row.to_dict())
                if "quantization_capacity" in result:
                    capacity = result["quantization_capacity"]
                    # Store the capacity values in the DataFrame
                    df.at[idx, "quantization_capacity.7b"] = capacity.model_7b
                    df.at[idx, "quantization_capacity.13b"] = capacity.model_13b
                    df.at[idx, "quantization_capacity.70b"] = capacity.model_70b

            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        except Exception as e:
            console = Console()
            console.print(f"[yellow]Warning: Could not calculate quantization capacity: {e}[/yellow]")
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # Set default output directory if not provided
    if output_dir is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = f"reports/{today}"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Set output path based on format
    if output_format.lower() == "html":
        output_path = os.path.join(output_dir, "insight.html")
        # TODO: Implement HTML report generation
        raise NotImplementedError("HTML report generation is not yet implemented")
    else:  # Default to Markdown
        output_path = os.path.join(output_dir, "insight.md")
        return generate_markdown_report(df, output_path)
