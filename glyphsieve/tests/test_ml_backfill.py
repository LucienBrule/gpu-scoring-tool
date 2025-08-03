"""
Unit tests for ML backfill functionality.

Tests cover single file processing, directory batch processing, error handling,
dry-run functionality, and validation as specified in TASK.ml.06.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from glyphsieve.ml.cli_backfill import BackfillProcessor, ml_backfill


class TestBackfillProcessor:
    """Test the BackfillProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.processor = BackfillProcessor()

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def create_test_csv(self, filename: str, data: dict, include_ml_columns: bool = False) -> Path:
        """Create a test CSV file."""
        df = pd.DataFrame(data)
        if include_ml_columns:
            df["ml_is_gpu"] = [1, 0] * (len(df) // 2 + 1)
            df["ml_score"] = [0.9, 0.1] * (len(df) // 2 + 1)
            df = df.iloc[: len(data[next(iter(data.keys()))])]  # Trim to original length

        file_path = self.temp_dir / filename
        df.to_csv(file_path, index=False)
        return file_path

    def test_validate_csv_format_valid(self):
        """Test CSV validation with valid format."""
        df = pd.DataFrame(
            {"title": ["NVIDIA RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"], "price": [1500, 300]}
        )

        result = self.processor._validate_csv_format(df, Path("test.csv"))
        assert result is True
        assert self.processor.stats["errors"] == 0

    def test_validate_csv_format_missing_columns(self):
        """Test CSV validation with missing required columns."""
        df = pd.DataFrame({"price": [1500, 300], "description": ["GPU", "CPU"]})

        result = self.processor._validate_csv_format(df, Path("test.csv"))
        assert result is False
        assert self.processor.stats["errors"] == 1

    def test_validate_csv_format_existing_ml_columns(self):
        """Test CSV validation with existing ML columns."""
        df = pd.DataFrame(
            {"title": ["NVIDIA RTX 4090"], "bulk_notes": ["Gaming GPU"], "ml_is_gpu": [1], "ml_score": [0.9]}
        )

        result = self.processor._validate_csv_format(df, Path("test.csv"))
        assert result is True
        assert self.processor.stats["warnings"] == 1

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_dataframe_success(self, mock_predict):
        """Test successful dataframe processing."""
        mock_predict.return_value = [(True, 0.9), (False, 0.1)]

        df = pd.DataFrame(
            {"title": ["NVIDIA RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"], "price": [1500, 300]}
        )

        result_df = self.processor._process_dataframe(df)

        # Check that ML columns were added
        assert "ml_is_gpu" in result_df.columns
        assert "ml_score" in result_df.columns

        # Check column order (ML columns should be last)
        expected_columns = ["title", "bulk_notes", "price", "ml_is_gpu", "ml_score"]
        assert list(result_df.columns) == expected_columns

        # Check values
        assert result_df["ml_is_gpu"].tolist() == [1, 0]
        assert result_df["ml_score"].tolist() == [0.9, 0.1]

        # Check stats
        assert self.processor.stats["rows_processed"] == 2
        assert self.processor.stats["ml_positive_predictions"] == 1

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_dataframe_existing_ml_columns(self, mock_predict):
        """Test processing dataframe that already has ML columns."""
        df = pd.DataFrame(
            {"title": ["NVIDIA RTX 4090"], "bulk_notes": ["Gaming GPU"], "ml_is_gpu": [1], "ml_score": [0.9]}
        )

        result_df = self.processor._process_dataframe(df)

        # Should return original dataframe unchanged
        pd.testing.assert_frame_equal(result_df, df)
        mock_predict.assert_not_called()

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_dataframe_chunked_processing(self, mock_predict):
        """Test chunked processing for large datasets."""
        # Create larger dataset
        data = {"title": [f"GPU {i}" for i in range(2500)], "bulk_notes": [f"Notes {i}" for i in range(2500)]}
        df = pd.DataFrame(data)

        # Mock predictions for chunks
        mock_predict.side_effect = [
            [(True, 0.9)] * 1000,  # First chunk
            [(False, 0.1)] * 1000,  # Second chunk
            [(True, 0.8)] * 500,  # Third chunk
        ]

        result_df = self.processor._process_dataframe(df, chunk_size=1000)

        # Check that predict_batch was called 3 times (for 3 chunks)
        assert mock_predict.call_count == 3

        # Check results
        assert len(result_df) == 2500
        assert "ml_is_gpu" in result_df.columns
        assert "ml_score" in result_df.columns

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_dataframe_error_handling(self, mock_predict):
        """Test error handling during prediction."""
        mock_predict.side_effect = Exception("Prediction failed")

        df = pd.DataFrame({"title": ["NVIDIA RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"]})

        result_df = self.processor._process_dataframe(df)

        # Should have default values for failed predictions
        assert result_df["ml_is_gpu"].tolist() == [0, 0]
        assert result_df["ml_score"].tolist() == [0.0, 0.0]
        assert self.processor.stats["errors"] == 1

    def test_create_backup(self):
        """Test backup file creation."""
        # Create original file
        original_file = self.temp_dir / "test.csv"
        original_file.write_text("test,data\n1,2\n")

        backup_path = self.processor._create_backup(original_file)

        assert backup_path.exists()
        assert backup_path.name == "test.backup.csv"
        assert backup_path.read_text() == "test,data\n1,2\n"

    def test_write_processing_log(self):
        """Test processing log creation."""
        file_path = self.temp_dir / "test.csv"

        self.processor._write_processing_log(file_path, 100, 25, 2, 1)

        log_file = Path("backfill_logs") / "test.log"
        assert log_file.exists()

        log_content = log_file.read_text()
        assert "Rows processed: 100" in log_content
        assert "ML-positive predictions: 25" in log_content
        assert "Warnings: 2" in log_content
        assert "Errors: 1" in log_content

        # Clean up
        shutil.rmtree("backfill_logs")

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_file_success(self, mock_predict):
        """Test successful single file processing."""
        mock_predict.return_value = [(True, 0.9), (False, 0.1)]

        # Create input file
        input_file = self.create_test_csv(
            "input.csv", {"title": ["NVIDIA RTX 4090", "Intel CPU"], "bulk_notes": ["Gaming GPU", "Processor"]}
        )

        output_file = self.temp_dir / "output.csv"

        result = self.processor.process_file(input_file, output_file)

        assert result is True
        assert output_file.exists()

        # Check output content
        output_df = pd.read_csv(output_file)
        assert "ml_is_gpu" in output_df.columns
        assert "ml_score" in output_df.columns
        assert len(output_df) == 2

    def test_process_file_input_not_exists(self):
        """Test processing non-existent input file."""
        input_file = self.temp_dir / "nonexistent.csv"
        output_file = self.temp_dir / "output.csv"

        result = self.processor.process_file(input_file, output_file)

        assert result is False
        assert self.processor.stats["errors"] == 1

    def test_process_file_output_exists_no_overwrite(self):
        """Test processing when output exists and overwrite is False."""
        input_file = self.create_test_csv("input.csv", {"title": ["NVIDIA RTX 4090"], "bulk_notes": ["Gaming GPU"]})

        output_file = self.temp_dir / "output.csv"
        output_file.write_text("existing,data\n")

        result = self.processor.process_file(input_file, output_file, overwrite=False)

        assert result is False
        assert self.processor.stats["errors"] == 1

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_process_file_overwrite_creates_backup(self, mock_predict):
        """Test that overwrite creates backup."""
        mock_predict.return_value = [(True, 0.9)]

        input_file = self.create_test_csv("input.csv", {"title": ["NVIDIA RTX 4090"], "bulk_notes": ["Gaming GPU"]})

        output_file = self.temp_dir / "output.csv"
        output_file.write_text("existing,data\n1,2\n")

        result = self.processor.process_file(input_file, output_file, overwrite=True)

        assert result is True
        backup_file = self.temp_dir / "output.backup.csv"
        assert backup_file.exists()
        assert backup_file.read_text() == "existing,data\n1,2\n"

    def test_process_file_dry_run(self):
        """Test dry run functionality."""
        input_file = self.create_test_csv("input.csv", {"title": ["NVIDIA RTX 4090"], "bulk_notes": ["Gaming GPU"]})

        output_file = self.temp_dir / "output.csv"

        result = self.processor.process_file(input_file, output_file, dry_run=True)

        assert result is True
        assert not output_file.exists()  # No file should be created in dry run

    def test_process_directory_success(self):
        """Test successful directory processing."""
        # Create input directory with CSV files
        input_dir = self.temp_dir / "input"
        input_dir.mkdir()

        self.create_test_csv("file1.csv", {"title": ["GPU 1"], "bulk_notes": ["Notes 1"]})
        self.create_test_csv("file2.csv", {"title": ["GPU 2"], "bulk_notes": ["Notes 2"]})

        # Move files to input directory
        (self.temp_dir / "file1.csv").rename(input_dir / "file1.csv")
        (self.temp_dir / "file2.csv").rename(input_dir / "file2.csv")

        output_dir = self.temp_dir / "output"

        with patch("glyphsieve.ml.cli_backfill.predict_batch") as mock_predict:
            mock_predict.return_value = [(True, 0.9)]

            results = self.processor.process_directory(input_dir, output_dir)

        assert len(results) == 2
        assert all(results)  # All files processed successfully
        assert (output_dir / "file1_ml_enhanced.csv").exists()
        assert (output_dir / "file2_ml_enhanced.csv").exists()

    def test_process_directory_no_csv_files(self):
        """Test directory processing with no CSV files."""
        input_dir = self.temp_dir / "input"
        input_dir.mkdir()

        # Create non-CSV file
        (input_dir / "readme.txt").write_text("Not a CSV")

        output_dir = self.temp_dir / "output"

        results = self.processor.process_directory(input_dir, output_dir)

        assert results == []

    def test_process_directory_nonexistent(self):
        """Test processing non-existent directory."""
        input_dir = self.temp_dir / "nonexistent"
        output_dir = self.temp_dir / "output"

        results = self.processor.process_directory(input_dir, output_dir)

        assert results == []

    def test_generate_summary_report(self):
        """Test summary report generation."""
        # Set up some stats
        self.processor.stats.update(
            {
                "files_processed": 5,
                "rows_processed": 1000,
                "ml_positive_predictions": 250,
                "errors": 2,
                "warnings": 1,
                "processing_time": 30.5,
            }
        )

        report_path = self.temp_dir / "summary.md"
        self.processor.generate_summary_report(report_path)

        assert report_path.exists()
        content = report_path.read_text()

        assert "Files processed: 5" in content
        assert "Rows processed: 1,000" in content
        assert "ML-positive predictions: 250" in content
        assert "Errors encountered: 2" in content
        assert "Warnings: 1" in content
        assert "Total processing time: 30.50 seconds" in content
        assert "Processing throughput:" in content
        assert "GPU prediction ratio: 25.00%" in content


class TestMLBackfillCLI:
    """Test the CLI interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.runner = CliRunner()

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def create_test_csv(self, filename: str, data: dict) -> Path:
        """Create a test CSV file."""
        df = pd.DataFrame(data)
        file_path = self.temp_dir / filename
        df.to_csv(file_path, index=False)
        return file_path

    def test_cli_missing_model(self):
        """Test CLI with missing model file."""
        input_file = self.create_test_csv("input.csv", {"title": ["GPU"], "bulk_notes": ["Notes"]})

        result = self.runner.invoke(ml_backfill, ["--input", str(input_file), "--model", "nonexistent_model.pkl"])

        assert result.exit_code != 0
        assert "Model file nonexistent_model.pkl does not exist" in result.output

    @patch("glyphsieve.ml.cli_backfill.Path.exists")
    @patch("glyphsieve.ml.cli_backfill.BackfillProcessor")
    def test_cli_single_file_success(self, mock_processor_class, mock_exists):
        """Test successful single file CLI processing."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor.process_file.return_value = True
        mock_processor.stats = {"files_processed": 1, "rows_processed": 100, "ml_positive_predictions": 25, "errors": 0}
        mock_processor_class.return_value = mock_processor

        input_file = self.create_test_csv("input.csv", {"title": ["GPU"], "bulk_notes": ["Notes"]})

        result = self.runner.invoke(
            ml_backfill, ["--input", str(input_file), "--output", str(self.temp_dir / "output.csv")]
        )

        assert result.exit_code == 0
        assert "File processed successfully" in result.output
        mock_processor.process_file.assert_called_once()

    @patch("glyphsieve.ml.cli_backfill.Path.exists")
    @patch("glyphsieve.ml.cli_backfill.BackfillProcessor")
    def test_cli_directory_processing(self, mock_processor_class, mock_exists):
        """Test directory processing via CLI."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor.process_directory.return_value = [True, True]
        mock_processor.stats = {"files_processed": 2, "rows_processed": 200, "ml_positive_predictions": 50, "errors": 0}
        mock_processor_class.return_value = mock_processor

        input_dir = self.temp_dir / "input"
        input_dir.mkdir()

        result = self.runner.invoke(ml_backfill, ["--input", str(input_dir), "--output", str(self.temp_dir / "output")])

        assert result.exit_code == 0
        assert "Successfully processed 2/2 files" in result.output
        mock_processor.process_directory.assert_called_once()

    @patch("glyphsieve.ml.cli_backfill.Path.exists")
    @patch("glyphsieve.ml.cli_backfill.BackfillProcessor")
    def test_cli_dry_run(self, mock_processor_class, mock_exists):
        """Test dry run via CLI."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor.process_file.return_value = True
        mock_processor.stats = {"files_processed": 0, "rows_processed": 0, "ml_positive_predictions": 0, "errors": 0}
        mock_processor_class.return_value = mock_processor

        input_file = self.create_test_csv("input.csv", {"title": ["GPU"], "bulk_notes": ["Notes"]})

        result = self.runner.invoke(ml_backfill, ["--input", str(input_file), "--dry-run"])

        assert result.exit_code == 0
        assert "DRY RUN MODE" in result.output
        mock_processor.process_file.assert_called_with(
            input_file, input_file.with_stem(f"{input_file.stem}_ml_enhanced"), False, True
        )

    @patch("glyphsieve.ml.cli_backfill.Path.exists")
    @patch("glyphsieve.ml.cli_backfill.BackfillProcessor")
    def test_cli_with_config(self, mock_processor_class, mock_exists):
        """Test CLI with config file."""
        mock_exists.return_value = True
        mock_processor = Mock()
        mock_processor.process_file.return_value = True
        mock_processor.stats = {"files_processed": 1, "rows_processed": 100, "ml_positive_predictions": 25, "errors": 0}
        mock_processor_class.return_value = mock_processor

        input_file = self.create_test_csv("input.csv", {"title": ["GPU"], "bulk_notes": ["Notes"]})
        config_file = self.temp_dir / "config.yaml"
        config_file.write_text("threshold: 0.8\n")

        result = self.runner.invoke(ml_backfill, ["--input", str(input_file), "--config", str(config_file)])

        assert result.exit_code == 0
        # Check that processor was initialized with config path
        mock_processor_class.assert_called_with("models/gpu_classifier_v2.pkl", str(config_file))


class TestBackfillIdempotency:
    """Test idempotent reprocessing behavior."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @patch("glyphsieve.ml.cli_backfill.predict_batch")
    def test_reprocessing_existing_ml_columns(self, mock_predict):
        """Test that reprocessing files with ML columns is idempotent."""
        # Create file with existing ML columns
        df = pd.DataFrame(
            {
                "title": ["NVIDIA RTX 4090", "Intel CPU"],
                "bulk_notes": ["Gaming GPU", "Processor"],
                "ml_is_gpu": [1, 0],
                "ml_score": [0.9, 0.1],
            }
        )

        input_file = self.temp_dir / "input.csv"
        df.to_csv(input_file, index=False)

        processor = BackfillProcessor()
        output_file = self.temp_dir / "output.csv"

        # Process the file
        result = processor.process_file(input_file, output_file)

        assert result is True

        # Check that predict_batch was not called (since ML columns exist)
        mock_predict.assert_not_called()

        # Check that output is identical to input
        output_df = pd.read_csv(output_file)
        input_df = pd.read_csv(input_file)
        pd.testing.assert_frame_equal(output_df, input_df)


if __name__ == "__main__":
    pytest.main([__file__])
