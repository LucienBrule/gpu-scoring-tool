"""
Score subcommand for glyphsieve CLI.

This module provides a CLI command for scoring GPU listings based on various metrics.
"""
import os
import click
from rich.console import Console
from rich.table import Table
import pandas as pd

from glyphsieve.core.scoring import score_csv, load_scoring_weights, WeightedAdditiveScorer

# Initialize rich console for formatted output
console = Console()

@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file with enriched GPU listings")
@click.option("--output", "-o", help="Path for scored output CSV file (default: scored_<filename>.csv)")
@click.option("--weights", "-w", help="Path to YAML file with scoring weights")
@click.option("--strategy", "-s", default="weighted", help="Scoring strategy to use (currently only 'weighted' is supported)")
def score(input, output, weights, strategy):
    """
    Score GPU listings based on utility metrics.

    This command takes enriched GPU listings and assigns a composite utility score
    based on factors like VRAM, MIG support, NVLink, TDP, and price.

    The output CSV will include all original columns plus a 'score' column
    with values from 0.0 to 1.0, where higher values indicate better utility.
    """
    console.print("[bold blue]Running score command[/bold blue]")

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Set default output path if not provided
        if output is None:
            input_basename = os.path.basename(input)
            output = f"scored_{input_basename}"

        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        if weights:
            console.print(f"Weights file: {weights}")

        # Select scoring strategy (currently only weighted is supported)
        if strategy != "weighted":
            console.print(f"[bold yellow]Warning:[/bold yellow] Strategy '{strategy}' not recognized. Using 'weighted' strategy.")

        # Score the CSV
        scored_df = score_csv(input, output, weights)

        # Print summary statistics
        console.print("\n[bold]Scoring Summary:[/bold]")

        # Create a table with score statistics
        table = Table(title="Score Statistics")
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", style="green")

        # Add score statistics to the table
        table.add_row("Mean Score", f"{scored_df['score'].mean():.4f}")
        table.add_row("Median Score", f"{scored_df['score'].median():.4f}")
        table.add_row("Min Score", f"{scored_df['score'].min():.4f}")
        table.add_row("Max Score", f"{scored_df['score'].max():.4f}")

        console.print(table)

        # Print top 3 and bottom 3 cards
        console.print("\n[bold]Top 3 Cards:[/bold]")
        top_3 = scored_df.sort_values('score', ascending=False).head(3)
        for _, row in top_3.iterrows():
            model = row.get('canonical_model', 'Unknown')
            score = row['score']
            vram = row.get('vram_gb', 'N/A')
            price = row.get('price', 'N/A')
            console.print(f"[green]{model}[/green]: Score {score:.4f}, VRAM: {vram} GB, Price: ${price}")

        console.print("\n[bold]Bottom 3 Cards:[/bold]")
        bottom_3 = scored_df.sort_values('score').head(3)
        for _, row in bottom_3.iterrows():
            model = row.get('canonical_model', 'Unknown')
            score = row['score']
            vram = row.get('vram_gb', 'N/A')
            price = row.get('price', 'N/A')
            console.print(f"[red]{model}[/red]: Score {score:.4f}, VRAM: {vram} GB, Price: ${price}")

        console.print(f"\n[green]Success:[/green] Scored CSV written to '{output}'")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise
