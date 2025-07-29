"""
CLI commands for the GPU model registry.

This module provides commands for listing and querying the GPU model registry.
"""

import click
from rich.console import Console
from rich.table import Table

from glyphsieve.core.resources.base_resource_context import ResourceContext
from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.registry import GPUModelRegistry


class RegistryResourceContext(ResourceContext):
    """Resource context for the registry."""

    def get_loaders(self):
        """Return a mapping of file extensions to loader implementations."""
        return {".yaml": GlyphSieveYamlLoader(), ".yml": GlyphSieveYamlLoader()}


@click.group()
def registry():
    """
    Commands for working with the GPU model registry.

    This group provides commands for listing and querying the GPU model registry.
    """
    pass


@registry.command("list")
def list_registry():
    """
    List all GPU models in the registry.

    This command loads the GPU model registry and displays all models in a tabular format.
    """
    # Initialize the console for formatted output
    console = Console()

    # Load the registry
    registry = GPUModelRegistry()
    resource_context = RegistryResourceContext()

    try:
        registry.load(resource_context)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        return

    # Get all models
    models = registry.list()

    if not models:
        console.print("[yellow]No GPU models found in the registry.[/yellow]")
        return

    # Create a table for display
    table = Table(show_header=True, header_style="bold")
    table.add_column("name", style="cyan", no_wrap=True)
    table.add_column("vram_gb", justify="right")
    table.add_column("mig_capable", justify="center")
    table.add_column("tdp_w", justify="right")
    table.add_column("slots", justify="right")
    table.add_column("connectivity")

    # Add rows to the table
    for model in models:
        table.add_row(
            model.name,
            str(model.vram_gb),
            str(model.mig_capable).lower(),
            str(model.tdp_w),
            str(model.slots),
            model.connectivity or "",
        )

    # Print the table
    console.print(table)


@registry.command("lookup")
@click.argument("name")
def lookup_model(name):
    """
    Look up a GPU model by name.

    This command loads the GPU model registry and displays the details of a specific model.
    """
    # Initialize the console for formatted output
    console = Console()

    # Load the registry
    registry = GPUModelRegistry()
    resource_context = RegistryResourceContext()

    try:
        registry.load(resource_context)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        return

    # Look up the model
    model = registry.get(name)

    if not model:
        # Try fuzzy matching
        model = registry.closest_match(name)

        if model:
            console.print(f"[yellow]No exact match found for '{name}'. Showing closest match:[/yellow]")
        else:
            console.print(f"[bold red]Error:[/bold red] No GPU model found with name '{name}'")
            return

    # Create a table for display
    table = Table(show_header=True, header_style="bold")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    # Add rows to the table
    table.add_row("Name", model.name)
    table.add_row("VRAM (GB)", str(model.vram_gb))
    table.add_row("TDP (W)", str(model.tdp_w))
    table.add_row("Slots", str(model.slots))
    table.add_row("MIG Capable", str(model.mig_capable))
    table.add_row("Form Factor", model.form_factor)
    table.add_row("Connectivity", model.connectivity or "")

    if model.notes:
        table.add_row("Notes", model.notes)

    # Print the table
    console.print(table)
