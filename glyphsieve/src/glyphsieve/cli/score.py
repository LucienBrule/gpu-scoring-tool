"""
Score subcommand for glyphsieve CLI.

This module provides a CLI command for scoring GPU listings based on various metrics.
"""

import os
from typing import Any, Dict, Optional

import click
import pandas as pd
from rich.console import Console
from rich.table import Table

from glyphsieve.core.scoring import score_csv

# Initialize rich console for formatted output
console = Console()


def validate_input_file(input_file: str) -> bool:
    """Validate that the input file exists."""
    if not os.path.exists(input_file):
        console.print(f"[bold red]Error:[/bold red] Input file '{input_file}' does not exist.")
        return False
    return True


def get_default_output_path(input_file: str) -> str:
    """Get the default output path if none is provided."""
    input_basename = os.path.basename(input_file)
    return f"scored_{input_basename}"


def get_scoring_strategy(strategy_name: str) -> Any:
    """Get the scoring strategy based on the strategy name."""
    from glyphsieve.core.scoring import (
        EnhancedWeightedScorer,
        WeightedAdditiveScorer,
    )

    if strategy_name == "weighted":
        return WeightedAdditiveScorer()
    elif strategy_name == "enhanced":
        return EnhancedWeightedScorer()
    else:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] Strategy '{strategy_name}' not recognized. "
            f"Using 'enhanced' strategy."
        )
        return EnhancedWeightedScorer()


def collect_weight_overrides(
    weight_vram: Optional[float],
    weight_mig: Optional[float],
    weight_nvlink: Optional[float],
    weight_tdp: Optional[float],
    weight_price: Optional[float],
    weight_quantization: Optional[float],
) -> Dict[str, float]:
    """Collect weight overrides from command line options."""
    weight_overrides = {}

    if weight_vram is not None:
        weight_overrides["vram_weight"] = weight_vram
        console.print(f"Overriding VRAM weight: {weight_vram}")

    if weight_mig is not None:
        weight_overrides["mig_weight"] = weight_mig
        console.print(f"Overriding MIG weight: {weight_mig}")

    if weight_nvlink is not None:
        weight_overrides["nvlink_weight"] = weight_nvlink
        console.print(f"Overriding NVLink weight: {weight_nvlink}")

    if weight_tdp is not None:
        weight_overrides["tdp_weight"] = weight_tdp
        console.print(f"Overriding TDP weight: {weight_tdp}")

    if weight_price is not None:
        weight_overrides["price_weight"] = weight_price
        console.print(f"Overriding price weight: {weight_price}")

    if weight_quantization is not None:
        weight_overrides["quantization_weight"] = weight_quantization
        console.print(f"Overriding quantization weight: {weight_quantization}")

    return weight_overrides


def print_score_statistics(scored_df: pd.DataFrame) -> None:
    """Print summary statistics for the scored DataFrame."""
    console.print("\n[bold]Scoring Summary:[/bold]")

    # Create a table with score statistics
    table = Table(title="Score Statistics")
    table.add_column("Statistic", style="cyan")
    table.add_column("Raw Score", style="yellow")
    table.add_column("Quantization Score", style="blue")
    table.add_column("Final Score", style="green")

    # Add score statistics to the table
    table.add_row(
        "Mean",
        f"{scored_df['raw_score'].mean():.4f}",
        f"{scored_df['quantization_score'].mean():.4f}",
        f"{scored_df['final_score'].mean():.2f}",
    )
    table.add_row(
        "Median",
        f"{scored_df['raw_score'].median():.4f}",
        f"{scored_df['quantization_score'].median():.4f}",
        f"{scored_df['final_score'].median():.2f}",
    )
    table.add_row(
        "Min",
        f"{scored_df['raw_score'].min():.4f}",
        f"{scored_df['quantization_score'].min():.4f}",
        f"{scored_df['final_score'].min():.2f}",
    )
    table.add_row(
        "Max",
        f"{scored_df['raw_score'].max():.4f}",
        f"{scored_df['quantization_score'].max():.4f}",
        f"{scored_df['final_score'].max():.2f}",
    )

    console.print(table)


def print_top_cards(scored_df: pd.DataFrame) -> None:
    """Print the top 3 cards by final score."""
    console.print("\n[bold]Top 3 Cards (by Final Score):[/bold]")
    top_3 = scored_df.sort_values("final_score", ascending=False).head(3)
    for _, row in top_3.iterrows():
        print_card_info(row, color="green")


def print_bottom_cards(scored_df: pd.DataFrame) -> None:
    """Print the bottom 3 cards by final score."""
    console.print("\n[bold]Bottom 3 Cards (by Final Score):[/bold]")
    bottom_3 = scored_df.sort_values("final_score").head(3)
    for _, row in bottom_3.iterrows():
        print_card_info(row, color="red")


def print_card_info(row: pd.Series, color: str) -> None:
    """Print information about a card with the specified color."""
    model = row.get("canonical_model", "Unknown")
    raw_score = row.get("raw_score", 0.0)
    quant_score = row.get("quantization_score", 0.0)
    final_score = row.get("final_score", 0.0)
    vram = row.get("vram_gb", "N/A")
    price = row.get("price", "N/A")
    console.print(
        f"[{color}]{model}[/{color}]: Final Score {final_score:.2f}, "
        f"Raw Score {raw_score:.4f}, Quant Score {quant_score:.4f}, "
        f"VRAM: {vram} GB, Price: ${price}"
    )


@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file with enriched GPU listings")
@click.option("--output", "-o", help="Path for scored output CSV file (default: scored_<filename>.csv)")
@click.option("--weights", "-w", help="Path to YAML file with scoring weights")
@click.option(
    "--strategy",
    "-s",
    default="enhanced",
    help="Scoring strategy to use ('enhanced' or 'weighted', default: 'enhanced')",
)
@click.option("--weight-vram", type=float, help="Override weight for VRAM capacity")
@click.option("--weight-mig", type=float, help="Override weight for MIG support")
@click.option("--weight-nvlink", type=float, help="Override weight for NVLink support")
@click.option("--weight-tdp", type=float, help="Override weight for TDP (inverse)")
@click.option("--weight-price", type=float, help="Override weight for price (inverse)")
@click.option("--weight-quantization", type=float, help="Override weight for quantization capacity")
def score(
    input,
    output,
    weights,
    strategy,
    weight_vram,
    weight_mig,
    weight_nvlink,
    weight_tdp,
    weight_price,
    weight_quantization,
):
    """
    Score GPU listings based on utility metrics.

    This command takes enriched GPU listings and assigns a composite utility score
    based on factors like VRAM, MIG support, NVLink, TDP, price, and quantization capacity.

    The output CSV will include the following columns:
    - model: Canonical model name
    - raw_score: Raw score before quantization adjustment
    - quantization_score: Score adjustment based on quantization capacity
    - final_score: Final score after all adjustments (0-100 scale)

    You can override the default weights using the --weight-* options.
    """
    console.print("[bold blue]Running score command[/bold blue]")

    try:
        # Validate input file exists
        if not validate_input_file(input):
            return

        # Set default output path if not provided
        if output is None:
            output = get_default_output_path(input)

        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        if weights:
            console.print(f"Weights file: {weights}")

        # Select scoring strategy
        scoring_strategy = get_scoring_strategy(strategy)

        # Collect weight overrides
        weight_overrides = collect_weight_overrides(
            weight_vram, weight_mig, weight_nvlink, weight_tdp, weight_price, weight_quantization
        )

        # Score the CSV
        scored_df = score_csv(input, output, weights, scoring_strategy, weight_overrides)

        # Print summary statistics
        print_score_statistics(scored_df)

        # Print top and bottom cards
        print_top_cards(scored_df)
        print_bottom_cards(scored_df)

        console.print(f"\n[green]Success:[/green] Scored CSV written to '{output}'")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise
