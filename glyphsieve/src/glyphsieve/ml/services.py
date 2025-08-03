"""
ML services for training dataset extraction and processing.

This module contains the business logic for ML operations, separated from CLI concerns.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

from .data_extraction import extract_training_data, validate_training_data
from .train_test_split import get_split_summary, stratified_split

logger = logging.getLogger(__name__)


class MLDatasetService:
    """Service for ML dataset operations."""

    def __init__(self):
        """Initialize the ML dataset service."""
        pass

    def extract_training_dataset(
        self, input_path: str, output_dir: str, test_size: float = 0.2, random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        Extract labeled training dataset from normalized GPU data.

        Args:
            input_path: Path to the stage_normalized.csv file
            output_dir: Output directory for training datasets
            test_size: Fraction of data to use for test set
            random_seed: Random seed for reproducible splits

        Returns:
            Dictionary with extraction results and metadata

        Raises:
            ValueError: If input file doesn't exist or has invalid format
            FileNotFoundError: If input file is not found
        """
        logger.info("Starting training dataset extraction")

        # Validate input file exists
        input_path_obj = Path(input_path)
        if not input_path_obj.exists():
            raise FileNotFoundError(f"Input file {input_path} does not exist")

        # Create output directory
        output_path_obj = Path(output_dir)
        output_path_obj.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {output_path_obj}")

        # Extract training data
        logger.info("Extracting and labeling training data...")
        training_df, extraction_metadata = extract_training_data(str(input_path_obj))

        # Validate training data
        validate_training_data(training_df)

        # Perform train/test split
        logger.info("Performing stratified train/test split...")
        train_df, test_df, split_metadata = stratified_split(training_df, test_size=test_size, random_seed=random_seed)

        # Get split summary
        split_summary = get_split_summary(train_df, test_df)

        # Save CSV files
        training_set_path = output_path_obj / "training_set.csv"
        train_path = output_path_obj / "train.csv"
        test_path = output_path_obj / "test.csv"

        logger.info("Saving CSV files...")
        training_df.to_csv(training_set_path, index=False)
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)

        # Prepare complete metadata
        dataset_info = self._prepare_dataset_metadata(
            input_path_obj, output_path_obj, extraction_metadata, split_metadata, split_summary, test_size, random_seed
        )

        # Save metadata YAML
        metadata_path = output_path_obj / "dataset_info.yaml"
        logger.info("Saving metadata...")
        with open(metadata_path, "w") as f:
            yaml.dump(dataset_info, f, default_flow_style=False, sort_keys=False)

        # Prepare result summary
        result = {
            "success": True,
            "input_file": str(input_path_obj),
            "output_directory": str(output_path_obj),
            "files_created": {
                "training_set": str(training_set_path),
                "train_set": str(train_path),
                "test_set": str(test_path),
                "metadata": str(metadata_path),
            },
            "extraction_metadata": extraction_metadata,
            "split_metadata": split_metadata,
            "split_summary": split_summary,
            "dataset_info": dataset_info,
        }

        logger.info("Training dataset extraction completed successfully")
        return result

    def _prepare_dataset_metadata(
        self,
        input_path: Path,
        output_path: Path,
        extraction_metadata: Dict[str, Any],
        split_metadata: Dict[str, Any],
        split_summary: Dict[str, Any],
        test_size: float,
        random_seed: int,
    ) -> Dict[str, Any]:
        """
        Prepare complete dataset metadata.

        Args:
            input_path: Input file path
            output_path: Output directory path
            extraction_metadata: Metadata from data extraction
            split_metadata: Metadata from train/test split
            split_summary: Summary statistics from split
            test_size: Test set size fraction
            random_seed: Random seed used

        Returns:
            Complete dataset metadata dictionary
        """
        return {
            "creation_timestamp": datetime.utcnow().isoformat() + "Z",
            "input_file": str(input_path),
            "output_directory": str(output_path),
            "label_spec_version": extraction_metadata["label_spec_version"],
            # Extraction metadata
            "total_rows_processed": extraction_metadata["total_rows_processed"],
            "rows_after_cleaning": extraction_metadata["rows_after_cleaning"],
            "skipped_rows": extraction_metadata["skipped_rows"],
            # Class distribution
            "gpu_count": extraction_metadata["gpu_count"],
            "non_gpu_count": extraction_metadata["non_gpu_count"],
            "gpu_ratio": extraction_metadata["gpu_ratio"],
            # Split information
            "train_test_split": {
                "test_size": test_size,
                "random_seed": random_seed,
                "train_samples": split_summary["train_samples"],
                "test_samples": split_summary["test_samples"],
                "train_gpu_count": split_summary["train_gpu_count"],
                "train_non_gpu_count": split_summary["train_non_gpu_count"],
                "test_gpu_count": split_summary["test_gpu_count"],
                "test_non_gpu_count": split_summary["test_non_gpu_count"],
                "train_gpu_ratio": split_summary["train_gpu_ratio"],
                "test_gpu_ratio": split_summary["test_gpu_ratio"],
                "balance_preserved": bool(split_metadata["balance_preserved"]),
                "max_balance_difference": split_metadata["max_balance_difference"],
            },
            # Output files
            "output_files": {
                "training_set": "training_set.csv",
                "train_set": "train.csv",
                "test_set": "test.csv",
                "metadata": "dataset_info.yaml",
            },
        }

    def get_extraction_summary(self, result: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the extraction results.

        Args:
            result: Result dictionary from extract_training_dataset

        Returns:
            Formatted summary string
        """
        extraction = result["extraction_metadata"]
        split = result["split_summary"]
        split_meta = result["split_metadata"]

        summary_lines = [
            "✅ Training dataset extraction completed successfully!",
            "",
            "Summary:",
            f"  Input file: {result['input_file']}",
            f"  Total rows processed: {extraction['total_rows_processed']:,}",
            f"  Rows after cleaning: {extraction['rows_after_cleaning']:,}",
            f"  Skipped rows: {extraction['skipped_rows']:,}",
            f"  GPU samples: {extraction['gpu_count']:,} ({extraction['gpu_ratio']:.2%})",
            f"  Non-GPU samples: {extraction['non_gpu_count']:,}",
            "",
            "Train/Test Split:",
            f"  Train samples: {split['train_samples']:,} ({split['train_gpu_ratio']:.2%} GPU)",
            f"  Test samples: {split['test_samples']:,} ({split['test_gpu_ratio']:.2%} GPU)",
            f"  Balance preserved: {'✓' if split_meta['balance_preserved'] else '✗'}",
            "",
            "Output files:",
        ]

        for file_path in result["files_created"].values():
            summary_lines.append(f"  📄 {file_path}")

        return "\n".join(summary_lines)
