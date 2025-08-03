"""
Unit tests for ML data extraction functionality.

Tests the binary labeling logic, data extraction, and validation functions.
"""

import os
import tempfile

import pandas as pd
import pytest

from glyphsieve.ml.data_extraction import (
    extract_training_data,
    is_nvidia_gpu,
    validate_training_data,
)


class TestNvidiaGpuLabeling:
    """Test the NVIDIA GPU binary labeling logic."""

    def test_nvidia_rtx_models(self):
        """Test that RTX models are correctly identified as NVIDIA GPUs."""
        assert is_nvidia_gpu("RTX_5090")
        assert is_nvidia_gpu("RTX_5080")
        assert is_nvidia_gpu("RTX_5070")
        assert is_nvidia_gpu("RTX_4090")
        assert is_nvidia_gpu("RTX_4080")
        assert is_nvidia_gpu("RTX_3090")

    def test_nvidia_a_series(self):
        """Test that A-series models are correctly identified as NVIDIA GPUs."""
        assert is_nvidia_gpu("A100_40GB_PCIE")
        assert is_nvidia_gpu("RTX_A6000")
        assert is_nvidia_gpu("RTX_A4000")
        assert is_nvidia_gpu("A40")

    def test_nvidia_l_series(self):
        """Test that L-series models are correctly identified as NVIDIA GPUs."""
        assert is_nvidia_gpu("L40")
        assert is_nvidia_gpu("L4")
        assert is_nvidia_gpu("L40S")

    def test_unknown_models(self):
        """Test that UNKNOWN models are not identified as GPUs."""
        assert not is_nvidia_gpu("UNKNOWN")
        assert not is_nvidia_gpu("")
        assert not is_nvidia_gpu(None)

    def test_non_nvidia_models(self):
        """Test that non-NVIDIA models are not identified as GPUs."""
        assert not is_nvidia_gpu("RX_7900_XTX")
        assert not is_nvidia_gpu("Intel_Arc_A770")
        assert not is_nvidia_gpu("GTX_1080")  # Doesn't start with RTX_
        assert not is_nvidia_gpu("Radeon_RX_6800")
        assert not is_nvidia_gpu("Intel_UHD_Graphics")

    def test_edge_cases(self):
        """Test edge cases for the labeling logic."""
        assert not is_nvidia_gpu("RTX")  # Not a canonical model
        assert not is_nvidia_gpu("A")  # Not a canonical model
        assert not is_nvidia_gpu("L")  # Not a canonical model
        assert not is_nvidia_gpu("rtx_5090")  # Case sensitive, not canonical
        assert not is_nvidia_gpu("NONEXISTENT_MODEL")  # Not in canonical models


class TestDataExtraction:
    """Test the data extraction functionality."""

    def create_test_csv(self, data):
        """Helper to create a temporary CSV file with test data."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        df = pd.DataFrame(data)
        df.to_csv(temp_file.name, index=False)
        temp_file.close()
        return temp_file.name

    def test_extract_training_data_basic(self):
        """Test basic data extraction functionality."""
        test_data = {
            "title": ["MSI RTX 5090", "Intel Arc A770", "AMD RX 7900 XTX"],
            "bulk_notes": ["GPU card", "Graphics card", "Gaming GPU"],
            "canonical_model": ["RTX_5090", "UNKNOWN", "UNKNOWN"],
        }

        csv_path = self.create_test_csv(test_data)

        try:
            training_df, metadata = extract_training_data(csv_path)

            # Check DataFrame structure
            assert list(training_df.columns) == ["title", "bulk_notes", "is_gpu"]
            assert len(training_df) == 3

            # Check labeling
            assert training_df.iloc[0]["is_gpu"] == 1  # RTX_5090
            assert training_df.iloc[1]["is_gpu"] == 0  # UNKNOWN
            assert training_df.iloc[2]["is_gpu"] == 0  # UNKNOWN

            # Check metadata
            assert metadata["total_rows_processed"] == 3
            assert metadata["rows_after_cleaning"] == 3
            assert metadata["skipped_rows"] == 0
            assert metadata["gpu_count"] == 1
            assert metadata["non_gpu_count"] == 2
            assert metadata["label_spec_version"] == "v1.0"

        finally:
            os.unlink(csv_path)

    def test_extract_training_data_with_missing_values(self):
        """Test data extraction with missing values."""
        test_data = {
            "title": ["MSI RTX 5090", "", "AMD RX 7900 XTX", "NVIDIA A100"],
            "bulk_notes": ["GPU card", "Graphics card", "", "AI GPU"],
            "canonical_model": ["RTX_5090", "UNKNOWN", "UNKNOWN", "A100_40GB_PCIE"],
        }

        csv_path = self.create_test_csv(test_data)

        try:
            training_df, metadata = extract_training_data(csv_path)

            # Should skip rows with empty title or bulk_notes
            assert len(training_df) == 2  # Only first and last rows
            assert metadata["total_rows_processed"] == 4
            assert metadata["rows_after_cleaning"] == 2
            assert metadata["skipped_rows"] == 2
            assert metadata["gpu_count"] == 2  # RTX_5090 and A100_40GB_PCIE
            assert metadata["non_gpu_count"] == 0

        finally:
            os.unlink(csv_path)

    def test_extract_training_data_missing_columns(self):
        """Test data extraction with missing required columns."""
        test_data = {
            "title": ["MSI RTX 5090"],
            "bulk_notes": ["GPU card"],
            # Missing canonical_model column
        }

        csv_path = self.create_test_csv(test_data)

        try:
            with pytest.raises(ValueError, match="Missing required columns"):
                extract_training_data(csv_path)
        finally:
            os.unlink(csv_path)


class TestTrainingDataValidation:
    """Test the training data validation functionality."""

    def test_validate_training_data_valid(self):
        """Test validation with valid training data."""
        valid_df = pd.DataFrame(
            {"title": ["MSI RTX 5090", "Intel Arc A770"], "bulk_notes": ["GPU card", "Graphics card"], "is_gpu": [1, 0]}
        )

        # Should not raise any exception
        validate_training_data(valid_df)

    def test_validate_training_data_wrong_columns(self):
        """Test validation with wrong column names."""
        invalid_df = pd.DataFrame({"product_name": ["MSI RTX 5090"], "description": ["GPU card"], "is_gpu": [1]})

        with pytest.raises(ValueError, match="Expected columns"):
            validate_training_data(invalid_df)

    def test_validate_training_data_wrong_column_order(self):
        """Test validation with wrong column order."""
        invalid_df = pd.DataFrame({"is_gpu": [1], "title": ["MSI RTX 5090"], "bulk_notes": ["GPU card"]})

        with pytest.raises(ValueError, match="Expected columns"):
            validate_training_data(invalid_df)

    def test_validate_training_data_wrong_dtype(self):
        """Test validation with wrong data type for is_gpu."""
        invalid_df = pd.DataFrame(
            {"title": ["MSI RTX 5090"], "bulk_notes": ["GPU card"], "is_gpu": ["yes"]}  # String instead of int
        )

        with pytest.raises(ValueError, match="is_gpu column should be integer"):
            validate_training_data(invalid_df)

    def test_validate_training_data_invalid_labels(self):
        """Test validation with invalid label values."""
        invalid_df = pd.DataFrame(
            {"title": ["MSI RTX 5090"], "bulk_notes": ["GPU card"], "is_gpu": [2]}  # Should only be 0 or 1
        )

        with pytest.raises(ValueError, match="is_gpu should only contain 0 and 1"):
            validate_training_data(invalid_df)

    def test_validate_training_data_missing_values(self):
        """Test validation with missing values."""
        invalid_df = pd.DataFrame(
            {"title": ["MSI RTX 5090", None], "bulk_notes": ["GPU card", "Graphics card"], "is_gpu": [1, 0]}
        )

        with pytest.raises(ValueError, match="should not contain missing values"):
            validate_training_data(invalid_df)

    def test_validate_training_data_empty_strings(self):
        """Test validation with empty strings."""
        invalid_df = pd.DataFrame(
            {"title": ["MSI RTX 5090", ""], "bulk_notes": ["GPU card", "Graphics card"], "is_gpu": [1, 0]}
        )

        with pytest.raises(ValueError, match="should not contain empty strings"):
            validate_training_data(invalid_df)
