"""
Tag subcommand for glyphsieve CLI.

This module provides CLI commands for tagging GPU listings with heuristic-based flags.
"""

import os

import click
import pandas as pd
from rich.console import Console
from rich.table import Table

from glyphsieve.core.heuristics import apply_heuristics

# Initialize rich console for formatted output
console = Console()


@click.group()
def tag():
    """
    Tag GPU listings with heuristic-based flags.

    This command group provides subcommands for applying various heuristics
    to GPU listings, such as quantization capability.
    """
    pass


@tag.command()
@click.option("--input", "-i", required=True, help="Path to CSV file to tag")
@click.option("--output", "-o", help="Path for tagged output CSV file (default: quantization_tagged_<filename>.csv)")
@click.option("--config-file", "-c", help="Path to YAML file with quantization heuristic configuration")
def quantization(input, output, config_file):
    """
    Tag GPU listings as quantization-capable.

    This command takes a CSV file with GPU listings (must have vram_gb, tdp_watts, and mig_support columns)
    and adds a 'quantization_capable' column indicating whether each GPU is suitable for
    quantized LLM hosting or multi-session low-bit inference.

    A GPU is considered quantization-capable if it meets all of the following criteria:
    - VRAM >= min_vram_gb (default: 24 GB)
    - TDP <= max_tdp_watts (default: 300 watts)
    - MIG support >= min_mig_support (default: 1, where 0=none, 1-7=supported)

    These thresholds can be customized via a configuration file.
    """
    console.print("[bold blue]Running tag-quantization command[/bold blue]")

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Set default output path if not provided
        if output is None:
            input_basename = os.path.basename(input)
            output = f"quantization_tagged_{input_basename}"

            # Create tmp/output directory if it doesn't exist
            os.makedirs("tmp/output", exist_ok=True)

            # Use tmp/output directory for default output
            output = os.path.join("tmp/output", output)

        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        if config_file:
            console.print(f"Config file: {config_file}")

        # Apply the quantization heuristic
        apply_heuristics(input, output, config_file)

        # Load the tagged file to display results

        df = pd.read_csv(output)

        # Print a summary of the tagging results
        if "quantization_capable" in df.columns:
            capable_count = df[df["quantization_capable"]].shape[0]
            not_capable_count = df[not df["quantization_capable"]].shape[0]
            total_count = df.shape[0]

            table = Table(title="Quantization Capability Results")
            table.add_column("Category", style="cyan")
            table.add_column("Count", style="green")
            table.add_column("Percentage", style="yellow")

            table.add_row("Quantization Capable", str(capable_count), f"{capable_count / total_count * 100:.1f}%")
            table.add_row("Not Capable", str(not_capable_count), f"{not_capable_count / total_count * 100:.1f}%")
            table.add_row("Total Rows", str(total_count), "100.0%")

            console.print(table)

            # Print examples of capable GPUs
            if capable_count > 0:
                console.print("\n[bold]Examples of quantization-capable GPUs:[/bold]")
                example = df[df["quantization_capable"]].iloc[0]
                console.print(f"[cyan]Model:[/cyan] {example.get('canonical_model', 'N/A')}")
                console.print(f"[cyan]VRAM:[/cyan] {example.get('vram_gb', 'N/A')} GB")
                console.print(f"[cyan]TDP:[/cyan] {example.get('tdp_watts', 'N/A')} watts")
                console.print(f"[cyan]MIG Support:[/cyan] {example.get('mig_support', 'N/A')}")

            # Print examples of non-capable GPUs
            if not_capable_count > 0:
                console.print("\n[bold]Examples of non-capable GPUs:[/bold]")
                example = df[not df["quantization_capable"]].iloc[0]
                console.print(f"[cyan]Model:[/cyan] {example.get('canonical_model', 'N/A')}")
                console.print(f"[cyan]VRAM:[/cyan] {example.get('vram_gb', 'N/A')} GB")
                console.print(f"[cyan]TDP:[/cyan] {example.get('tdp_watts', 'N/A')} watts")
                console.print(f"[cyan]MIG Support:[/cyan] {example.get('mig_support', 'N/A')}")
        else:
            console.print("[bold yellow]Warning:[/bold yellow] No 'quantization_capable' column found in output file.")

        console.print(f"\n[green]Success:[/green] Tagged CSV written to '{output}'")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise
