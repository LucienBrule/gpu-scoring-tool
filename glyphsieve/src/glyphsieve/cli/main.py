"""
Main CLI module for glyphsieve.
"""

import click
from rich.console import Console

from glyphsieve import __version__
from glyphsieve.cli.clean import clean
from glyphsieve.cli.dedup import dedup
from glyphsieve.cli.enrich import enrich
from glyphsieve.cli.normalize import normalize
from glyphsieve.cli.pipeline import pipeline
from glyphsieve.cli.report import report
from glyphsieve.cli.score import score
from glyphsieve.cli.tag import tag

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


# Add subcommands to the main group
main.add_command(clean)
main.add_command(normalize)
main.add_command(score)
main.add_command(enrich)
main.add_command(dedup)
main.add_command(pipeline)
main.add_command(report)
main.add_command(tag)

if __name__ == "__main__":
    main()
