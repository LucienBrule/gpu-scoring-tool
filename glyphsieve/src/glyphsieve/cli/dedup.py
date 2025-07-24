"""
Dedup subcommand for glyphsieve CLI.

This module provides a CLI command for deduplicating GPU listings.
"""
import os
import click
from rich.console import Console
from rich.table import Table

from glyphsieve.core.deduplication import dedup_csv, DEFAULT_SIMILARITY_THRESHOLD, DEFAULT_PRICE_EPSILON

# Initialize rich console for formatted output
console = Console()

@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file to deduplicate")
@click.option("--output", "-o", help="Path for deduplicated output CSV file (default: dedup_<filename>.csv)")
@click.option("--similarity", "-s", type=float, default=DEFAULT_SIMILARITY_THRESHOLD, 
              help=f"Similarity threshold (0.0-1.0, default: {DEFAULT_SIMILARITY_THRESHOLD})")
@click.option("--price-epsilon", "-p", type=float, default=DEFAULT_PRICE_EPSILON,
              help=f"Price difference tolerance as fraction (default: {DEFAULT_PRICE_EPSILON})")
@click.option("--model", "-m", default="all-MiniLM-L6-v2", 
              help="Sentence transformer model to use (default: all-MiniLM-L6-v2)")
def dedup(input, output, similarity, price_epsilon, model):
    """
    Deduplicate GPU listings using semantic similarity.
    
    This command identifies likely duplicate listings using semantic similarity on the 'title' column,
    along with other criteria like URL and price similarity. This is especially useful for marketplaces
    like eBay, where vendors may repost the same item multiple times with slight phrasing differences.
    
    The output CSV will include the original columns plus:
    - dedup_status: one of 'UNIQUE', 'DUPLICATE_PRIMARY', or 'DUPLICATE_SECONDARY'
    - dedup_group_id: identifier for groups of duplicates
    """
    console.print("[bold blue]Running deduplication command[/bold blue]")
    
    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return
        
        # Set default output path if not provided
        if output is None:
            input_basename = os.path.basename(input)
            output = f"dedup_{input_basename}"
        
        console.print(f"Input file: {input}")
        console.print(f"Output file: {output}")
        console.print(f"Similarity threshold: {similarity}")
        console.print(f"Price epsilon: {price_epsilon}")
        console.print(f"Model: {model}")
        
        # Process the CSV
        console.print("\n[bold]Generating embeddings and finding duplicates...[/bold]")
        df = dedup_csv(
            input, 
            output, 
            similarity_threshold=similarity,
            price_epsilon=price_epsilon,
            model_name=model
        )
        
        # Print a summary of the deduplication results
        dedup_counts = df['dedup_status'].value_counts().to_dict()
        
        table = Table(title="Deduplication Results")
        table.add_column("Status", style="cyan")
        table.add_column("Count", style="green")
        
        for status, count in dedup_counts.items():
            table.add_row(status, str(count))
        
        console.print(table)
        
        # Print number of duplicate groups
        if 'DUPLICATE_PRIMARY' in dedup_counts:
            console.print(f"\nFound {dedup_counts.get('DUPLICATE_PRIMARY', 0)} duplicate groups")
        
        # Print examples of each status type
        console.print("\n[bold]Examples of each status:[/bold]")
        for status in ['UNIQUE', 'DUPLICATE_PRIMARY', 'DUPLICATE_SECONDARY']:
            if status in dedup_counts and dedup_counts[status] > 0:
                example = df[df['dedup_status'] == status].iloc[0]
                console.print(f"[cyan]{status}[/cyan]: '{example['title']}'")
                
                # For duplicates, show the group
                if status in ['DUPLICATE_PRIMARY', 'DUPLICATE_SECONDARY']:
                    group_id = example['dedup_group_id']
                    group_size = len(df[df['dedup_group_id'] == group_id])
                    console.print(f"  Group ID: {group_id}, Size: {group_size}")
        
        console.print(f"\n[green]Success:[/green] Deduplicated CSV written to '{output}'")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise