"""
Report subcommand for glyphsieve CLI.

This module provides a CLI command for generating human-readable reports from scored GPU datasets.
"""
import os
import click
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from glyphsieve.core.reporting import generate_report

# Initialize rich console for formatted output
console = Console()

@click.command()
@click.option("--input", "-i", required=True, help="Path to CSV file with scored GPU listings")
@click.option("--output-dir", "-o", help="Directory to save the report (default: reports/YYYY-MM-DD/)")
@click.option("--format", "-f", default="md", type=click.Choice(["md", "html"]), help="Output format (md or html)")
def report(input, output_dir, format):
    """
    Generate a human-readable report from a scored GPU dataset.

    This command takes a scored GPU dataset and generates a report summarizing key insights
    and statistical observations about the GPU market. The report includes summary statistics,
    highlight sections for top cards, and anomaly detection.

    The output is a Markdown (.md) or HTML file with formatted tables and sections.
    """
    console.print("[bold blue]Running report command[/bold blue]")

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Generate the report
        output_path = generate_report(input, output_dir, format)
        
        # Print success message
        console.print(Panel.fit(
            f"[green]Report generated successfully![/green]\n\n"
            f"Report saved to: [bold]{output_path}[/bold]",
            title="Report Generation Complete",
            border_style="green"
        ))
        
    except NotImplementedError as e:
        console.print(f"[bold yellow]Warning:[/bold yellow] {str(e)}")
        console.print("Falling back to Markdown format.")
        
        # Try again with Markdown format
        output_path = generate_report(input, output_dir, "md")
        console.print(f"[green]Report generated in Markdown format:[/green] {output_path}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise