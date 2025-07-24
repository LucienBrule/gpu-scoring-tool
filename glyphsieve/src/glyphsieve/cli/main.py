"""
Main CLI module for glyphsieve.
"""
import click
from rich.console import Console

from glyphsieve import __version__

# Initialize rich console for formatted output
console = Console()

@click.group()
@click.version_option(version=__version__)
def main():
    """
    glyphsieve: GPU data processing and scoring tool.
    
    This CLI provides commands for cleaning, normalizing, and scoring GPU data.
    """
    pass

# Import subcommands
from glyphsieve.cli.clean import clean
from glyphsieve.cli.normalize import normalize
from glyphsieve.cli.score import score

# Add subcommands to the main group
main.add_command(clean)
main.add_command(normalize)
main.add_command(score)

if __name__ == "__main__":
    main()