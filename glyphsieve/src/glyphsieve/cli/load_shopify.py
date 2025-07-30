"""
Load Shopify command for glyphsieve CLI.

This module provides the load-shopify command for processing Shopify JSON data exports
and converting them to pipeline-compatible CSV format.
"""

from pathlib import Path

import click
from rich.console import Console

from glyphsieve.core.ingest.shopify.wamatek_loader import WamatekShopifyLoader

# Initialize rich console for formatted output
console = Console()


@click.command("load-shopify")
@click.option(
    "--source",
    required=True,
    type=click.Choice(["wamatek"], case_sensitive=False),
    help="Shopify source vendor (e.g., wamatek)",
)
@click.option("--input", required=True, help="Path to Shopify JSON file to process")
@click.option("--output", required=True, help="Path for output CSV file")
def load_shopify(source: str, input: str, output: str):
    """
    Load Shopify JSON data and convert to pipeline CSV format.

    This command processes Shopify JSON exports and transforms them into
    the standardized CSV format expected by the GPU scoring pipeline.

    Examples:
        glyphsieve load-shopify --source wamatek \\
            --input recon/wamatek/wamatek_sample.json \\
            --output tmp/test_full_subset.csv
    """
    input_path = Path(input)
    output_path = Path(output)

    # Validate input file exists
    if not input_path.exists():
        console.print(f"[red]Error: Input file not found: {input_path}[/red]")
        raise click.Abort()

    # Select appropriate loader based on source
    if source.lower() == "wamatek":
        loader = WamatekShopifyLoader()
    else:
        console.print(f"[red]Error: Unsupported source: {source}[/red]")
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
