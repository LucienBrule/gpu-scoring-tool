"""
CLI interface for ML backfill operations on normalized CSV files.

This module provides batch processing capabilities to add ML predictions to existing
normalized CSV files that were processed before ML integration was available.
"""

import logging
import shutil
import time
from pathlib import Path
from typing import List, Optional

import click
import pandas as pd
from tqdm import tqdm

from .predictor import predict_batch

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class BackfillProcessor:
    """Handles ML backfill operations for normalized CSV files."""

    def __init__(self, model_path: str = "models/gpu_classifier.pkl", config_path: Optional[str] = None):
        self.model_path = model_path
        self.config = self._load_config(config_path) if config_path else {}
        self.stats = {
            "files_processed": 0,
            "rows_processed": 0,
            "ml_positive_predictions": 0,
            "errors": 0,
            "warnings": 0,
            "processing_time": 0.0,
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration using GlyphSieveYamlLoader."""
        try:
            # For now, return empty dict as we don't have a specific config model
            # This can be extended when config schema is defined
            # loader = GlyphSieveYamlLoader()
            return {}
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return {}

    def _validate_csv_format(self, df: pd.DataFrame, file_path: Path) -> bool:
        """Validate that CSV has required columns for ML processing."""
        required_columns = ["title", "bulk_notes"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            logger.error(f"Missing required columns in {file_path}: {missing_columns}")
            self.stats["errors"] += 1
            return False

        # Check if ML columns already exist
        ml_columns = ["ml_is_gpu", "ml_score"]
        existing_ml_columns = [col for col in ml_columns if col in df.columns]

        if existing_ml_columns:
            logger.warning(f"ML columns already exist in {file_path}: {existing_ml_columns}")
            self.stats["warnings"] += 1

        return True

    def _process_dataframe(self, df: pd.DataFrame, chunk_size: int = 1000) -> pd.DataFrame:
        """Process dataframe by adding ML predictions in chunks."""
        # Skip if ML columns already exist
        if "ml_is_gpu" in df.columns and "ml_score" in df.columns:
            logger.info("ML columns already exist, skipping ML processing")
            return df

        # Prepare data for prediction
        titles = df["title"].fillna("").astype(str).tolist()
        bulk_notes = df["bulk_notes"].fillna("").astype(str).tolist()

        ml_predictions = []
        ml_scores = []

        # Process in chunks for memory efficiency
        total_chunks = (len(df) + chunk_size - 1) // chunk_size

        with tqdm(total=len(df), desc="Processing rows", unit="rows") as pbar:
            for i in range(0, len(df), chunk_size):
                end_idx = min(i + chunk_size, len(df))
                chunk_titles = titles[i:end_idx]
                chunk_notes = bulk_notes[i:end_idx]

                try:
                    # Get predictions for chunk
                    predictions = predict_batch(chunk_titles, chunk_notes)

                    for is_gpu, score in predictions:
                        ml_predictions.append(int(is_gpu))
                        ml_scores.append(float(score))
                        if is_gpu:
                            self.stats["ml_positive_predictions"] += 1

                except Exception as e:
                    logger.error(f"Error processing chunk {i // chunk_size + 1}/{total_chunks}: {e}")
                    # Fill with default values for failed chunk
                    chunk_size_actual = end_idx - i
                    ml_predictions.extend([0] * chunk_size_actual)
                    ml_scores.extend([0.0] * chunk_size_actual)
                    self.stats["errors"] += 1

                pbar.update(end_idx - i)

        # Add ML columns to dataframe (preserve existing column order)
        result_df = df.copy()
        result_df["ml_is_gpu"] = ml_predictions
        result_df["ml_score"] = ml_scores

        self.stats["rows_processed"] += len(df)
        return result_df

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup of original file."""
        backup_path = file_path.with_suffix(f".backup{file_path.suffix}")
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path

    def _write_processing_log(
        self, file_path: Path, rows_processed: int, ml_positive: int, warnings: int, errors: int
    ) -> None:
        """Write per-file processing log."""
        log_dir = Path("backfill_logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"{file_path.stem}.log"

        with open(log_file, "w") as f:
            f.write(f"Backfill Log for {file_path}\n")
            f.write(f"Processed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Rows processed: {rows_processed}\n")
            f.write(f"ML-positive predictions: {ml_positive}\n")
            f.write(f"Warnings: {warnings}\n")
            f.write(f"Errors: {errors}\n")

    def process_file(self, input_path: Path, output_path: Path, overwrite: bool = False, dry_run: bool = False) -> bool:
        """Process a single CSV file."""
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_path}")
            self.stats["errors"] += 1
            return False

        if output_path.exists() and not overwrite and not dry_run:
            logger.error(f"Output file exists and overwrite not specified: {output_path}")
            self.stats["errors"] += 1
            return False

        try:
            # Load CSV
            logger.info(f"Loading {input_path}")
            df = pd.read_csv(input_path)

            if not self._validate_csv_format(df, input_path):
                return False

            if dry_run:
                logger.info(f"DRY RUN: Would process {len(df)} rows from {input_path}")
                logger.info(f"DRY RUN: Would write to {output_path}")
                return True

            # Create backup if overwriting
            if overwrite and output_path.exists():
                self._create_backup(output_path)

            # Process dataframe
            start_time = time.time()
            processed_df = self._process_dataframe(df)
            processing_time = time.time() - start_time
            self.stats["processing_time"] += processing_time

            # Write output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            processed_df.to_csv(output_path, index=False)

            # Write processing log
            ml_positive = (processed_df.get("ml_is_gpu", pd.Series([0])) == 1).sum()
            self._write_processing_log(input_path, len(df), ml_positive, 0, 0)

            self.stats["files_processed"] += 1
            logger.info(f"Successfully processed {input_path} -> {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            self.stats["errors"] += 1
            return False

    def process_directory(
        self,
        input_dir: Path,
        output_dir: Path,
        suffix: str = "_ml_enhanced",
        overwrite: bool = False,
        dry_run: bool = False,
    ) -> List[bool]:
        """Process all CSV files in a directory."""
        if not input_dir.exists():
            logger.error(f"Input directory does not exist: {input_dir}")
            return []

        csv_files = list(input_dir.glob("*.csv"))
        if not csv_files:
            logger.warning(f"No CSV files found in {input_dir}")
            return []

        logger.info(f"Found {len(csv_files)} CSV files to process")

        results = []
        for csv_file in tqdm(csv_files, desc="Processing files", unit="files"):
            output_file = output_dir / f"{csv_file.stem}{suffix}.csv"
            result = self.process_file(csv_file, output_file, overwrite, dry_run)
            results.append(result)

        return results

    def generate_summary_report(self, output_path: Path = Path("backfill_summary.md")) -> None:
        """Generate summary report of backfill operation."""
        with open(output_path, "w") as f:
            f.write("# ML Backfill Summary Report\n\n")
            f.write(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Processing Statistics\n\n")
            f.write(f"- Files processed: {self.stats['files_processed']}\n")
            f.write(f"- Rows processed: {self.stats['rows_processed']:,}\n")
            f.write(f"- ML-positive predictions: {self.stats['ml_positive_predictions']:,}\n")
            f.write(f"- Errors encountered: {self.stats['errors']}\n")
            f.write(f"- Warnings: {self.stats['warnings']}\n")
            f.write(f"- Total processing time: {self.stats['processing_time']:.2f} seconds\n")

            if self.stats["rows_processed"] > 0:
                throughput = self.stats["rows_processed"] / max(self.stats["processing_time"], 0.001)
                gpu_ratio = self.stats["ml_positive_predictions"] / self.stats["rows_processed"]
                f.write(f"- Processing throughput: {throughput:.0f} rows/second\n")
                f.write(f"- GPU prediction ratio: {gpu_ratio:.2%}\n")

        logger.info(f"Summary report written to {output_path}")


@click.command()
@click.option(
    "--input",
    "-i",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to CSV file or directory containing CSV files",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(path_type=Path),
    help="Path for output file or directory (default: same as input with suffix)",
)
@click.option(
    "--model",
    "-m",
    "model_path",
    default="models/gpu_classifier_v2.pkl",
    help="Path to ML model (default: models/gpu_classifier_v2.pkl)",
)
@click.option("--suffix", "-s", default="_ml_enhanced", help="Suffix for output files (default: _ml_enhanced)")
@click.option("--overwrite", is_flag=True, help="Overwrite existing files (creates backup)")
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files")
@click.option(
    "--config",
    "-c",
    "config_path",
    type=click.Path(exists=True),
    help="Optional path to YAML config file for prediction thresholds",
)
def ml_backfill(
    input_path: Path,
    output_path: Optional[Path],
    model_path: str,
    suffix: str,
    overwrite: bool,
    dry_run: bool,
    config_path: Optional[str],
) -> None:
    """Add ML predictions to existing normalized CSV files.

    This command processes normalized CSV files and adds ml_is_gpu and ml_score columns
    while preserving the existing column order and data integrity.

    Examples:

    \b
    # Backfill single file (dry run first)
    glyphsieve ml-backfill -i data.csv --dry-run

    \b
    # Actual backfill
    glyphsieve ml-backfill -i data.csv -o data_enhanced.csv

    \b
    # Batch backfill directory
    glyphsieve ml-backfill -i input_dir/ -o output_dir/
    """
    start_time = time.time()

    # Validate model exists
    if not Path(model_path).exists():
        click.echo(f"❌ Error: Model file {model_path} does not exist", err=True)
        click.echo("💡 Hint: Run 'glyphsieve ml-train' first to create the model")
        raise click.Abort()

    # Initialize processor
    processor = BackfillProcessor(model_path, config_path)

    # Determine if input is file or directory
    is_directory = input_path.is_dir()

    if dry_run:
        click.echo("🔍 DRY RUN MODE - No files will be modified")

    if is_directory:
        # Directory processing
        if output_path is None:
            output_path = input_path.parent / f"{input_path.name}_enhanced"

        click.echo(f"📁 Processing directory: {input_path}")
        click.echo(f"📁 Output directory: {output_path}")

        if not dry_run:
            output_path.mkdir(parents=True, exist_ok=True)

        results = processor.process_directory(input_path, output_path, suffix, overwrite, dry_run)

        success_count = sum(results)
        click.echo(f"✅ Successfully processed {success_count}/{len(results)} files")

    else:
        # Single file processing
        if output_path is None:
            output_path = input_path.with_stem(f"{input_path.stem}{suffix}")

        click.echo(f"📄 Processing file: {input_path}")
        click.echo(f"📄 Output file: {output_path}")

        success = processor.process_file(input_path, output_path, overwrite, dry_run)

        if success:
            click.echo("✅ File processed successfully")
        else:
            click.echo("❌ File processing failed")
            raise click.Abort()

    # Display statistics
    total_time = time.time() - start_time
    click.echo("\n📊 Processing Summary:")
    click.echo(f"   Files processed: {processor.stats['files_processed']}")
    click.echo(f"   Rows processed: {processor.stats['rows_processed']:,}")
    click.echo(f"   ML-positive predictions: {processor.stats['ml_positive_predictions']:,}")
    click.echo(f"   Errors: {processor.stats['errors']}")
    click.echo(f"   Total time: {total_time:.2f} seconds")

    if processor.stats["rows_processed"] > 0:
        gpu_ratio = processor.stats["ml_positive_predictions"] / processor.stats["rows_processed"]
        throughput = processor.stats["rows_processed"] / max(total_time, 0.001)
        click.echo(f"   GPU prediction ratio: {gpu_ratio:.2%}")
        click.echo(f"   Throughput: {throughput:.0f} rows/second")

    # Generate summary report
    if not dry_run:
        processor.generate_summary_report()
        click.echo("📋 Summary report: backfill_summary.md")


if __name__ == "__main__":
    ml_backfill()
