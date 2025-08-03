"""
Main CLI module for glyphsieve.
"""

import click
from rich.console import Console

from glyphsieve import __version__
from glyphsieve.cli.clean import clean
from glyphsieve.cli.dedup import dedup
from glyphsieve.cli.enrich import enrich
from glyphsieve.cli.load_shopify import load_shopify
from glyphsieve.cli.normalize import normalize
from glyphsieve.cli.pipeline import pipeline
from glyphsieve.cli.registry import registry
from glyphsieve.cli.report import report
from glyphsieve.cli.score import score
from glyphsieve.cli.shopify import shopify, shopify_parse_standalone
from glyphsieve.cli.tag import tag
from glyphsieve.ml.cli_backfill import ml_backfill
from glyphsieve.ml.cli_disagreements import ml_disagreements
from glyphsieve.ml.cli_evaluate import ml_evaluate
from glyphsieve.ml.cli_extract import ml_extract_training_set
from glyphsieve.ml.cli_perplexity_eval import ml_eval
from glyphsieve.ml.cli_predict_is_gpu import predict_is_gpu_cli
from glyphsieve.ml.cli_train_title_only import ml_train_title_only
from glyphsieve.ml.train_gpu_classifier import ml_train

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
main.add_command(load_shopify)
main.add_command(pipeline)
main.add_command(registry)
main.add_command(report)
main.add_command(shopify)
main.add_command(shopify_parse_standalone)
main.add_command(tag)
main.add_command(ml_extract_training_set)
main.add_command(ml_train)
main.add_command(ml_train_title_only)
main.add_command(ml_evaluate)
main.add_command(ml_eval)
main.add_command(ml_disagreements)
main.add_command(ml_backfill)
main.add_command(predict_is_gpu_cli)

if __name__ == "__main__":
    main()
