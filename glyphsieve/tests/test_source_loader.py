"""
Tests for the SourceLoader interface and implementations.

This module tests the abstract SourceLoader interface and its concrete
implementations, particularly the DummySourceLoader used for testing.
"""

import csv
import tempfile
from pathlib import Path

import pytest

from glyphsieve.core.ingest.base_loader import DummySourceLoader, SourceLoader


class TestSourceLoaderInterface:
    """Test the SourceLoader abstract interface."""

    def test_source_loader_is_abstract(self):
        """Test that SourceLoader cannot be instantiated directly."""
        with pytest.raises(TypeError):
            SourceLoader()

    def test_source_loader_requires_load_implementation(self):
        """Test that concrete implementations must implement load method."""

        class IncompleteLoader(SourceLoader):
            def to_input_csv(self, rows, output_path):
                pass

        with pytest.raises(TypeError):
            IncompleteLoader()

    def test_source_loader_requires_to_input_csv_implementation(self):
        """Test that concrete implementations must implement to_input_csv method."""

        class IncompleteLoader(SourceLoader):
            def load(self, source):
                return []

        with pytest.raises(TypeError):
            IncompleteLoader()

    def test_complete_implementation_can_be_instantiated(self):
        """Test that complete implementations can be instantiated."""

        class CompleteLoader(SourceLoader):
            def load(self, source):
                return []

            def to_input_csv(self, rows, output_path):
                pass

        # Should not raise an exception
        loader = CompleteLoader()
        assert isinstance(loader, SourceLoader)


class TestDummySourceLoader:
    """Test the DummySourceLoader implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.loader = DummySourceLoader()

    def test_dummy_loader_instantiation(self):
        """Test that DummySourceLoader can be instantiated."""
        assert isinstance(self.loader, SourceLoader)
        assert isinstance(self.loader, DummySourceLoader)

    def test_load_returns_expected_data(self):
        """Test that load method returns the expected hardcoded data."""
        data = self.loader.load("dummy_source")

        # Should return a list of dictionaries
        assert isinstance(data, list)
        assert len(data) == 3  # Expected number of test records

        # Each item should be a dictionary
        for item in data:
            assert isinstance(item, dict)

        # Check that all expected fields are present
        expected_fields = {
            "model",
            "condition",
            "price",
            "quantity",
            "seller",
            "geographic_region",
            "listing_age",
            "source_url",
            "source_type",
            "bulk_notes",
            "title",
        }

        for item in data:
            assert set(item.keys()) == expected_fields

    def test_load_ignores_source_parameter(self):
        """Test that load method ignores the source parameter."""
        data1 = self.loader.load("source1")
        data2 = self.loader.load("source2")
        data3 = self.loader.load(Path("/some/path"))

        # All calls should return identical data
        assert data1 == data2 == data3

    def test_load_returns_valid_gpu_data(self):
        """Test that load method returns realistic GPU data."""
        data = self.loader.load("dummy")

        # Check first record for expected content
        first_record = data[0]
        assert "NVIDIA RTX" in first_record["model"]
        assert first_record["condition"] in ["New", "Used", "Refurbished"]
        assert isinstance(first_record["price"], int | float)
        assert first_record["price"] > 0
        assert first_record["quantity"] in ["Available", "Unavailable"]
        assert first_record["source_url"].startswith("https://")

    def test_to_input_csv_creates_valid_file(self):
        """Test that to_input_csv creates a valid CSV file."""
        data = self.loader.load("dummy")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.csv"

            # Should not raise an exception
            self.loader.to_input_csv(data, output_path)

            # File should exist
            assert output_path.exists()
            assert output_path.is_file()

    def test_to_input_csv_creates_directory_if_needed(self):
        """Test that to_input_csv creates parent directories if they don't exist."""
        data = self.loader.load("dummy")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "test_output.csv"

            # Parent directory doesn't exist initially
            assert not output_path.parent.exists()

            self.loader.to_input_csv(data, output_path)

            # Directory should be created and file should exist
            assert output_path.parent.exists()
            assert output_path.exists()

    def test_to_input_csv_has_correct_headers(self):
        """Test that the CSV file has the correct headers in the right order."""
        data = self.loader.load("dummy")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.csv"
            self.loader.to_input_csv(data, output_path)

            with open(output_path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)

                expected_headers = [
                    "model",
                    "condition",
                    "price",
                    "quantity",
                    "seller",
                    "geographic_region",
                    "listing_age",
                    "source_url",
                    "source_type",
                    "bulk_notes",
                    "title",
                ]

                assert headers == expected_headers

    def test_to_input_csv_has_correct_data(self):
        """Test that the CSV file contains the correct data."""
        data = self.loader.load("dummy")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.csv"
            self.loader.to_input_csv(data, output_path)

            with open(output_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                csv_data = list(reader)

                # Should have same number of rows
                assert len(csv_data) == len(data)

                # Check that data matches (converting price back to float for comparison)
                for original, csv_row in zip(data, csv_data):
                    assert csv_row["model"] == original["model"]
                    assert csv_row["condition"] == original["condition"]
                    assert float(csv_row["price"]) == original["price"]
                    assert csv_row["quantity"] == original["quantity"]
                    assert csv_row["seller"] == original["seller"]
                    assert csv_row["geographic_region"] == original["geographic_region"]
                    assert csv_row["listing_age"] == original["listing_age"]
                    assert csv_row["source_url"] == original["source_url"]
                    assert csv_row["source_type"] == original["source_type"]
                    assert csv_row["bulk_notes"] == original["bulk_notes"]
                    assert csv_row["title"] == original["title"]

    def test_end_to_end_workflow(self):
        """Test the complete workflow from load to CSV output."""
        # Load data
        data = self.loader.load("test_source")
        assert len(data) > 0

        # Write to CSV
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "workflow_test.csv"
            self.loader.to_input_csv(data, output_path)

            # Verify the file can be read back correctly
            with open(output_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                csv_data = list(reader)

                # Should have same number of records
                assert len(csv_data) == len(data)

                # All records should have all required fields
                expected_fields = {
                    "model",
                    "condition",
                    "price",
                    "quantity",
                    "seller",
                    "geographic_region",
                    "listing_age",
                    "source_url",
                    "source_type",
                    "bulk_notes",
                    "title",
                }

                for row in csv_data:
                    assert set(row.keys()) == expected_fields
                    # All fields should have non-empty values
                    for field, value in row.items():
                        assert value is not None
                        assert str(value).strip() != ""

    def test_to_input_csv_with_empty_data(self):
        """Test that to_input_csv handles empty data gracefully."""
        empty_data = []

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "empty_test.csv"

            # Should not raise an exception
            self.loader.to_input_csv(empty_data, output_path)

            # File should exist with just headers
            assert output_path.exists()

            with open(output_path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)

                # Should have headers
                assert len(headers) == 11

                # Should have no data rows
                data_rows = list(reader)
                assert len(data_rows) == 0
