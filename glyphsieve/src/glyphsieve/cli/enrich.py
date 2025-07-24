"""
Enrich subcommand for glyphsieve CLI.

This module provides a CLI command for enriching normalized GPU listings with metadata.
"""
import os
import click
from rich.console import Console
from rich.table import Table

from glyphsieve.core.enrichment import enrich_csv

# Initialize rich console for formatted output
console = Console()

@click.command()
@click.option("--input", "-i", required=True, help="Path to normalized CSV file to enrich")
@click.option("--output", "-o", help="Path for enriched output CSV file (default: enriched_<filename>.csv)")
@click.option("--specs-file", "-s", help="Path to YAML file with GPU specifications")
def enrich(input, output, specs_file):
    """
    Enrich normalized GPU listings with metadata.
    
    This command takes a normalized CSV file with a 'canonical_model' column and enriches
    each row by joining it with known GPU metadata such as VRAM, TDP, generation, and
    feature flags (e.g. MIG, NVLink).
    
    The output CSV will include the original columns plus:
    - vram_gb: VRAM capacity in GB
    - tdp_watts: Thermal Design Power in watts
    - mig_support: MIG support level (0, 4, or 7)
    - nvlink: Boolean indicating NVLink support
    - generation: GPU architecture generation (e.g. Ada, Ampere, Hopper, Blackwell)
    """
    console.print("[bold blue]Running enrich command[/bold blue]")
    
    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return
        
        # Set default output path if not provided
        if output is None:
            input_basename = os.path.basename(input)
            output = f"enriched_{input_basename}"
            
            # Create tmp/output directory if it doesn't exist
            os.makedirs("tmp/output", exist_ok=True)
            
            # Use tmp/output directory for default output
            output = os.path.join("tmp/output", output)
        
        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        if specs_file:
            console.print(f"Specs file: {specs_file}")
        
        # Enrich the CSV
        df = enrich_csv(input, output, specs_file)
        
        # Print a summary of the enrichment results
        enriched_count = df[df["vram_gb"].notnull()].shape[0]
        missing_count = df[df["vram_gb"].isnull()].shape[0]
        total_count = df.shape[0]
        
        table = Table(title="Enrichment Results")
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")
        
        table.add_row(
            "Enriched Rows",
            str(enriched_count),
            f"{enriched_count / total_count * 100:.1f}%"
        )
        table.add_row(
            "Missing Metadata",
            str(missing_count),
            f"{missing_count / total_count * 100:.1f}%"
        )
        table.add_row(
            "Total Rows",
            str(total_count),
            "100.0%"
        )
        
        console.print(table)
        
        # Print examples of enriched rows
        if enriched_count > 0:
            console.print("\n[bold]Examples of enriched rows:[/bold]")
            example = df[df["vram_gb"].notnull()].iloc[0]
            console.print(f"[cyan]Model:[/cyan] {example['canonical_model']}")
            console.print(f"[cyan]VRAM:[/cyan] {example['vram_gb']} GB")
            console.print(f"[cyan]TDP:[/cyan] {example['tdp_watts']} watts")
            console.print(f"[cyan]MIG Support:[/cyan] {example['mig_support']}")
            console.print(f"[cyan]NVLink:[/cyan] {example['nvlink']}")
            console.print(f"[cyan]Generation:[/cyan] {example['generation']}")
        
        # Print examples of missing metadata
        if missing_count > 0:
            console.print("\n[bold]Examples of rows with missing metadata:[/bold]")
            example = df[df["vram_gb"].isnull()].iloc[0]
            console.print(f"[cyan]Model:[/cyan] {example['canonical_model']}")
        
        console.print(f"\n[green]Success:[/green] Enriched CSV written to '{output}'")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise