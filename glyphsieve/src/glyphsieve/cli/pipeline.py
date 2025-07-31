"""
Pipeline subcommand for glyphsieve CLI.

This module provides a CLI command for running the full pipeline: clean → normalize → enrich → score.
"""

import os
import tempfile
import time
from typing import Dict, Optional, Tuple

import click
import pandas as pd
from rich.console import Console
from rich.table import Table

from glyphsieve.core.cleaning import clean_csv_headers
from glyphsieve.core.deduplication import dedup_csv
from glyphsieve.core.enrichment import enrich_csv
from glyphsieve.core.heuristics import apply_quantization_capacity
from glyphsieve.core.normalization import normalize_csv
from glyphsieve.core.scoring import score_csv

# Initialize rich console for formatted output
console = Console()


def run_clean_step(input_file: str, output_file: str) -> Dict[str, str]:
    """Run the clean step of the pipeline."""
    console.print("\n[bold blue]Step 1: Clean[/bold blue]")
    step_start = time.time()
    header_mapping = clean_csv_headers(input_file, output_file)
    step_duration = time.time() - step_start
    console.print(f"[green]Cleaned CSV written to '{output_file}'[/green] ({step_duration:.2f}s)")

    # Print the header mapping
    table = Table(title="Detected columns")
    table.add_column("Original", style="cyan")
    table.add_column("Cleaned", style="green")
    for original, cleaned in header_mapping.items():
        table.add_row(f'"{original}"', f'"{cleaned}"')
    console.print(table)

    return header_mapping


def run_normalize_step(input_file: str, output_file: str, models_file: Optional[str], fuzzy_threshold: float = 80.0) -> pd.DataFrame:
    """Run the normalize step of the pipeline."""
    console.print("\n[bold blue]Step 2: Normalize[/bold blue]")
    step_start = time.time()
    df = normalize_csv(input_file, output_file, models_file, fuzzy_threshold)
    step_duration = time.time() - step_start
    console.print(f"[green]Normalized CSV written to '{output_file}'[/green] ({step_duration:.2f}s)")

    # Print a summary of the normalization results
    match_counts = df["match_type"].value_counts().to_dict()
    table = Table(title="Normalization Results")
    table.add_column("Match Type", style="cyan")
    table.add_column("Count", style="green")
    for match_type, count in match_counts.items():
        table.add_row(match_type, str(count))
    console.print(table)

    return df


def run_dedup_step(input_file: str, output_file: str) -> pd.DataFrame:
    """Run the deduplication step of the pipeline."""
    console.print("\n[bold blue]Optional Step: Dedup[/bold blue]")
    step_start = time.time()
    df = dedup_csv(input_file, output_file)
    step_duration = time.time() - step_start
    console.print(f"[green]Deduplicated CSV written to '{output_file}'[/green] ({step_duration:.2f}s)")

    return df


def run_enrich_step(input_file: str, output_file: str, specs_file: Optional[str]) -> pd.DataFrame:
    """Run the enrich step of the pipeline."""
    console.print("\n[bold blue]Step 3: Enrich[/bold blue]")
    step_start = time.time()
    df = enrich_csv(input_file, output_file, specs_file)
    step_duration = time.time() - step_start
    console.print(f"[green]Enriched CSV written to '{output_file}'[/green] ({step_duration:.2f}s)")

    # Print a summary of the enrichment results
    enriched_count = df[df["vram_gb"].notnull()].shape[0]
    missing_count = df[df["vram_gb"].isnull()].shape[0]
    total_count = df.shape[0]

    table = Table(title="Enrichment Results")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="green")
    table.add_column("Percentage", style="yellow")

    table.add_row("Enriched Rows", str(enriched_count), f"{enriched_count / total_count * 100:.1f}%")
    table.add_row("Missing Metadata", str(missing_count), f"{missing_count / total_count * 100:.1f}%")
    table.add_row("Total Rows", str(total_count), "100.0%")

    console.print(table)

    return df


def run_quantization_step(
    input_file: str, output_file: str, specs_file: Optional[str], force: bool
) -> Tuple[str, bool]:
    """Run the quantization capacity step of the pipeline."""
    console.print("\n[bold blue]Optional Step: Quantization Capacity[/bold blue]")
    step_start = time.time()
    success = False

    try:
        apply_quantization_capacity(input_file, output_file, specs_file, force)
        step_duration = time.time() - step_start
        console.print(
            f"[green]Quantization capacity computed and added to output CSV → "
            f"{output_file}[/green] ({step_duration:.2f}s)"
        )
        success = True
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        console.print("[yellow]Continuing without quantization capacity...[/yellow]")
        output_file = input_file

    return output_file, success


def run_score_step(input_file: str, output_file: str, weights_file: Optional[str]) -> pd.DataFrame:
    """Run the score step of the pipeline."""
    console.print("\n[bold blue]Step 4: Score[/bold blue]")
    step_start = time.time()
    scored_df = score_csv(input_file, output_file, weights_file)
    step_duration = time.time() - step_start
    console.print(f"[green]Scored CSV written to '{output_file}'[/green] ({step_duration:.2f}s)")

    # Print summary statistics
    table = Table(title="Score Statistics")
    table.add_column("Statistic", style="cyan")
    table.add_column("Value", style="green")

    # Add score statistics to the table
    table.add_row("Mean Score", f"{scored_df['score'].mean():.4f}")
    table.add_row("Median Score", f"{scored_df['score'].median():.4f}")
    table.add_row("Min Score", f"{scored_df['score'].min():.4f}")
    table.add_row("Max Score", f"{scored_df['score'].max():.4f}")

    console.print(table)

    # Print top 3 cards
    console.print("\n[bold]Top 3 Cards:[/bold]")
    top_3 = scored_df.sort_values("score", ascending=False).head(3)
    for _, row in top_3.iterrows():
        model = row.get("canonical_model", "Unknown")
        score = row["score"]
        vram = row.get("vram_gb", "N/A")
        price = row.get("price", "N/A")
        console.print(f"[green]{model}[/green]: Score {score:.4f}, VRAM: {vram} GB, Price: ${price}")

    return scored_df


@click.command()
@click.option("--input", "-i", required=True, help="Path to raw CSV file to process")
@click.option("--output", "-o", required=True, help="Path for final scored output CSV file")
@click.option("--working-dir", "-w", help="Directory to store intermediate outputs (default: temporary directory)")
@click.option("--dedup", is_flag=True, help="Insert deduplication into the pipeline")
@click.option("--models-file", "-m", help="Path to JSON file with GPU model definitions for normalization")
@click.option("--specs-file", "-s", help="Path to YAML file with GPU specifications for enrichment")
@click.option("--weights-file", "-wf", help="Path to YAML file with scoring weights")
@click.option("--quantize-capacity", is_flag=True, help="Calculate quantization capacity for each GPU")
@click.option(
    "--force-quantize", is_flag=True, help="Force recalculation of quantization capacity if it already exists"
)
@click.option("--filter-invalid", is_flag=True, help="Exclude invalid or non-GPU items from the final output")
@click.option("--min-confidence-score", type=float, default=80.0, help="Minimum confidence score (0-100) for fuzzy matching")
def pipeline(
    input,
    output,
    working_dir,
    dedup,
    models_file,
    specs_file,
    weights_file,
    quantize_capacity,
    force_quantize,
    filter_invalid,
    min_confidence_score,
):
    """
    Run the full pipeline: clean → normalize → enrich → score.

    This command chains together the individual pipeline steps to process raw GPU data
    into a fully scored dataset. Intermediate files are stored in the specified working
    directory or a temporary directory if not specified.

    The pipeline steps are:
    1. clean: Clean CSV headers
    2. normalize: Normalize GPU model names
    3. enrich: Enrich with GPU metadata
    4. score: Score based on utility metrics

    If --dedup is specified, deduplication is performed after normalization.
    """
    console.print("[bold green]Running full pipeline[/bold green]")

    start_time = time.time()

    try:
        # Validate input file exists
        if not os.path.exists(input):
            console.print(f"[bold red]Error:[/bold red] Input file '{input}' does not exist.")
            return

        # Create working directory if specified, otherwise use a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            working_directory = working_dir if working_dir else temp_dir
            os.makedirs(working_directory, exist_ok=True)

            console.print(f"Input file: {input}")
            console.print(f"Output file: {output}")
            console.print(f"Working directory: {working_directory}")

            # Define intermediate file paths
            cleaned_file = os.path.join(working_directory, "stage_clean.csv")
            normalized_file = os.path.join(working_directory, "stage_normalized.csv")
            deduped_file = os.path.join(working_directory, "stage_deduped.csv")
            enriched_file = os.path.join(working_directory, "stage_enriched.csv")
            quant_file = os.path.join(working_directory, "stage_quantized.csv")

            # Step 1: Clean
            run_clean_step(input, cleaned_file)

            # Step 2: Normalize
            run_normalize_step(cleaned_file, normalized_file, models_file, min_confidence_score)

            # Optional Step: Dedup
            if dedup:
                run_dedup_step(normalized_file, deduped_file)
                input_for_enrich = deduped_file
            else:
                input_for_enrich = normalized_file

            # Step 3: Enrich
            run_enrich_step(input_for_enrich, enriched_file, specs_file)

            # Optional Step: Quantization Capacity
            if quantize_capacity:
                input_for_score, _ = run_quantization_step(enriched_file, quant_file, specs_file, force_quantize)
            else:
                input_for_score = enriched_file

            # Step 4: Score
            scored_df = run_score_step(input_for_score, output, weights_file)

            # Optional Step: Filter invalid rows
            if filter_invalid:
                console.print("\n[bold yellow]Optional Step: Filter Invalid Rows[/bold yellow]")
                step_start = time.time()

                # Read the scored data to apply filtering
                if "is_valid_gpu" in scored_df.columns:
                    original_count = len(scored_df)
                    valid_df = scored_df[scored_df["is_valid_gpu"]]
                    filtered_count = len(valid_df)
                    removed_count = original_count - filtered_count

                    # Write the filtered data back to the output file
                    valid_df.to_csv(output, index=False)

                    step_duration = time.time() - step_start
                    console.print(
                        f"[green]Filtered {removed_count} invalid rows, kept {filtered_count} "
                        f"valid GPU listings[/green] ({step_duration:.2f}s)"
                    )

                    if removed_count > 0:
                        console.print(
                            "[yellow]Removed items include capture devices, incomplete model names, "
                            "and other non-GPU products[/yellow]"
                        )
                else:
                    console.print("[yellow]Warning: is_valid_gpu column not found, skipping filtering[/yellow]")

            # Calculate total duration
            total_duration = time.time() - start_time
            console.print(f"\n[bold green]Pipeline completed successfully in {total_duration:.2f} seconds[/bold green]")
            console.print(f"Final output written to: {output}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise
