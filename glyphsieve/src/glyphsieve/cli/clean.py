"""
Clean subcommand for glyphsieve CLI.

This module provides a CLI command for cleaning CSV headers.
"""

import os

import click
from rich.console import Console
from rich.table import Table

from glyphsieve.core.cleaning import clean_csv_headers

# Initialize rich console for formatted output
console = Console()


@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file to clean")
@click.option("--output", "-o", help="Path for cleaned output CSV file (default: cleaned_<filename>.csv)")
@click.option("--dry-run", is_flag=True, help="Print detected header transformation without writing file")
def clean(input, output, dry_run):
    """
    Clean CSV headers for further processing.

    This command cleans CSV headers by trimming whitespace, converting to lowercase,
    replacing spaces with underscores, and standardizing common header names.
    """
    console.print("[bold green]Running clean command[/bold green]")

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Clean the CSV headers
        header_mapping = clean_csv_headers(input, output, dry_run)

        # Print the header mapping
        table = Table(title="Detected columns")
        table.add_column("Original", style="cyan")
        table.add_column("Cleaned", style="green")

        for original, cleaned in header_mapping.items():
            table.add_row(f'"{original}"', f'"{cleaned}"')

        console.print(table)

        if dry_run:
            console.print("[yellow]Dry run mode:[/yellow] No file was written.")
        else:
            output_path = output if output else f"cleaned_{os.path.basename(input)}"
            console.print(f"[green]Success:[/green] Cleaned CSV written to '{output_path}'")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise
