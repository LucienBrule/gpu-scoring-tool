"""
Normalize subcommand for glyphsieve CLI.

This module provides a CLI command for normalizing GPU model names.
"""

import os

import click
from rich.console import Console
from rich.table import Table

from glyphsieve.core.normalization import normalize_csv

# Initialize rich console for formatted output
console = Console()


@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file to normalize")
@click.option("--output", "-o", help="Path for normalized output CSV file (default: normalized_<filename>.csv)")
@click.option("--models-file", "-m", help="Path to JSON file with GPU model definitions")
@click.option("--use-ml", is_flag=True, help="Enable ML predictions and append ml_is_gpu, ml_score columns")
@click.option(
    "--ml-threshold", type=float, help="ML confidence threshold (0.0-1.0). Overrides GLYPHSIEVE_ML_THRESHOLD env var"
)
def normalize(input, output, models_file, use_ml, ml_threshold):
    """
    Normalize GPU model names in cleaned data.

    This command takes cleaned data with a 'title' column and normalizes the GPU model names
    by matching them against known models using exact, regex, and fuzzy matching strategies.

    The output CSV will include the original columns plus:
    - canonical_model: standardized enum-like string (e.g., RTX_A5000)
    - match_type: one of 'exact', 'regex', 'fuzzy', or 'none'
    - match_score: 1.0 for exact matches, ≤ 1.0 for other matches
    """
    console.print("[bold blue]Running normalize command[/bold blue]")

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Set default output path if not provided
        if output is None:
            input_basename = os.path.basename(input)
            output = f"normalized_{input_basename}"

        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        if models_file:
            console.print(f"Models file: {models_file}")

        # Normalize the CSV
        df = normalize_csv(input, output, models_file, use_ml=use_ml, ml_threshold=ml_threshold)

        # Print a summary of the normalization results
        match_counts = df["match_type"].value_counts().to_dict()

        table = Table(title="Normalization Results")
        table.add_column("Match Type", style="cyan")
        table.add_column("Count", style="green")

        for match_type, count in match_counts.items():
            table.add_row(match_type, str(count))

        console.print(table)

        # Print examples of each match type
        console.print("\n[bold]Examples of matches:[/bold]")
        for match_type in ["exact", "regex", "fuzzy", "none"]:
            if match_type in match_counts and match_counts[match_type] > 0:
                example = df[df["match_type"] == match_type].iloc[0]
                console.print(
                    f"[cyan]{match_type.upper()}[/cyan]: '{example['title']}' → "
                    f"'{example['canonical_model']}' (score: {example['match_score']:.2f})"
                )

        console.print(f"\n[green]Success:[/green] Normalized CSV written to '{output}'")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise
