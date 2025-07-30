"""
Shopify subcommand for glyphsieve CLI.

This module provides CLI commands for processing Shopify JSON data exports
and converting them to pipeline-compatible CSV format.
"""

from pathlib import Path

import click
from rich.console import Console

from glyphsieve.core.ingest.shopify.wamatek_loader import WamatekShopifyLoader

# Initialize rich console for formatted output
console = Console()


@click.group()
def shopify():
    """
    Commands for processing Shopify data exports.

    This command group provides tools for converting Shopify JSON exports
    from various vendors into pipeline-compatible CSV format.
    """
    pass


@shopify.command("parse")
@click.option("--input", "-i", required=True, help="Path to Shopify JSON/JSONL file to process")
@click.option("--output", "-o", required=True, help="Path for output CSV file")
@click.option(
    "--vendor",
    "-v",
    default="wamatek",
    type=click.Choice(["wamatek"], case_sensitive=False),
    help="Shopify vendor type (default: wamatek)",
)
def parse(input: str, output: str, vendor: str):
    """
    Parse Shopify JSON data and convert to pipeline CSV format.

    This command processes Shopify JSON exports and transforms them into
    the standardized CSV format expected by the GPU scoring pipeline.

    Examples:
        glyphsieve shopify parse -i recon/wamatek.jsonl -o input.csv
        glyphsieve shopify parse -i data.json -o output.csv --vendor wamatek
    """
    input_path = Path(input)
    output_path = Path(output)

    # Validate input file exists
    if not input_path.exists():
        console.print(f"[red]Error: Input file not found: {input_path}[/red]")
        raise click.Abort()

    # Select appropriate loader based on vendor
    if vendor.lower() == "wamatek":
        loader = WamatekShopifyLoader()
    else:
        console.print(f"[red]Error: Unsupported vendor: {vendor}[/red]")
        raise click.Abort()

    try:
        console.print(f"[blue]Loading data from {input_path}...[/blue]")

        # Load data using the appropriate loader
        listings = loader.load(input_path)

        console.print(f"[green]Successfully loaded {len(listings)} listings[/green]")

        if len(listings) == 0:
            console.print("[yellow]Warning: No listings found in input file[/yellow]")

        # Convert to CSV format
        console.print(f"[blue]Writing CSV output to {output_path}...[/blue]")
        loader.to_input_csv(listings, output_path)

        console.print(f"[green]✓ Successfully converted {len(listings)} listings to CSV format[/green]")
        console.print(f"[green]Output written to: {output_path}[/green]")

        # Show sample of what was processed
        if listings:
            console.print("\n[blue]Sample processed listing:[/blue]")
            sample = listings[0]
            console.print(f"  Model: {sample.get('model', 'N/A')}")
            console.print(f"  Price: ${sample.get('price', 'N/A')}")
            console.print(f"  Condition: {sample.get('condition', 'N/A')}")
            console.print(f"  Seller: {sample.get('seller', 'N/A')}")

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except ValueError as e:
        console.print(f"[red]Error processing data: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise click.Abort()


# For backwards compatibility, also register parse as a direct command
# This allows both "shopify parse" and "shopify-parse" to work
@click.command("shopify-parse")
@click.option("--input", "-i", required=True, help="Path to Shopify JSON/JSONL file to process")
@click.option("--output", "-o", required=True, help="Path for output CSV file")
@click.option(
    "--vendor",
    "-v",
    default="wamatek",
    type=click.Choice(["wamatek"], case_sensitive=False),
    help="Shopify vendor type (default: wamatek)",
)
def shopify_parse_standalone(input: str, output: str, vendor: str):
    """
    Parse Shopify JSON data and convert to pipeline CSV format.

    This is a standalone version of the shopify parse command for backwards compatibility.
    """
    # Call the grouped version
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(parse, ["-i", input, "-o", output, "-v", vendor])
    if result.exit_code != 0:
        raise click.Abort()
