"""
Abstract base class and test implementation for source loaders.

This module defines the SourceLoader abstract interface that all vendor-specific
data loaders must implement, along with a DummySourceLoader for testing purposes.
"""

import csv
from abc import ABC, abstractmethod
from pathlib import Path


class SourceLoader(ABC):
    """
    Abstract base class for loading data from vendor-specific sources.

    This interface defines the contract that all source loaders must implement
    to convert vendor-specific data formats into pipeline-compatible CSV inputs.
    Each loader is responsible for extracting data from its specific source format
    and transforming it into the standardized input schema expected by the pipeline.
    """

    @abstractmethod
    def load(self, source: str | Path) -> list[dict]:
        """
        Load raw data from the specified source.

        This method should read data from the given source (file path, URL, etc.)
        and return it as a list of dictionaries. Each dictionary represents a single
        record/listing that will be processed by the pipeline.

        Args:
            source: Path to the data source (file path, URL, etc.)

        Returns:
            List of dictionaries containing the raw data records

        Raises:
            FileNotFoundError: If the source file/resource cannot be found
            ValueError: If the source data is malformed or cannot be parsed
        """
        pass

    @abstractmethod
    def to_input_csv(self, rows: list[dict], output_path: Path) -> None:
        """
        Convert loaded data to pipeline-compatible CSV format.

        This method takes the raw data loaded by the load() method and transforms
        it into a CSV file that matches the expected input schema for the pipeline.
        The output CSV must contain the following columns in order:
        model, condition, price, quantity, seller, geographic_region, listing_age,
        source_url, source_type, bulk_notes, title

        Args:
            rows: List of dictionaries containing the raw data
            output_path: Path where the output CSV file should be written

        Raises:
            ValueError: If the data cannot be transformed to the expected format
            IOError: If the output file cannot be written
        """
        pass


class DummySourceLoader(SourceLoader):
    """
    Test-only implementation of SourceLoader for development and testing.

    This loader returns hardcoded sample data that matches the expected pipeline
    input format. It's intended for testing the loader interface and pipeline
    integration without requiring real vendor data sources.
    """

    def load(self, source: str | Path) -> list[dict]:
        """
        Load hardcoded test data.

        Returns a fixed set of sample GPU listings for testing purposes.
        The source parameter is ignored in this implementation.

        Args:
            source: Ignored in this implementation

        Returns:
            List of sample GPU listing dictionaries
        """
        return [
            {
                "model": "NVIDIA RTX 4090",
                "condition": "New",
                "price": 1599.99,
                "quantity": "Available",
                "seller": "Test Vendor A",
                "geographic_region": "USA",
                "listing_age": "Current",
                "source_url": "https://example.com/rtx4090",
                "source_type": "Retail_Major",
                "bulk_notes": "Test listing for development",
                "title": "NVIDIA RTX 4090 Graphics Card",
            },
            {
                "model": "NVIDIA RTX 4080",
                "condition": "New",
                "price": 1199.99,
                "quantity": "Available",
                "seller": "Test Vendor B",
                "geographic_region": "USA",
                "listing_age": "Current",
                "source_url": "https://example.com/rtx4080",
                "source_type": "Retail_Specialist",
                "bulk_notes": "Another test listing",
                "title": "NVIDIA RTX 4080 Graphics Card",
            },
            {
                "model": "NVIDIA RTX 4070",
                "condition": "Used",
                "price": 899.99,
                "quantity": "Unavailable",
                "seller": "Test Individual",
                "geographic_region": "USA",
                "listing_age": "Recent",
                "source_url": "https://example.com/rtx4070",
                "source_type": "Resale_Individual",
                "bulk_notes": "Used condition test case",
                "title": "NVIDIA RTX 4070 Graphics Card",
            },
        ]

    def to_input_csv(self, rows: list[dict], output_path: Path) -> None:
        """
        Write the data to a CSV file in pipeline-compatible format.

        Converts the list of dictionaries to a CSV file with the expected
        column headers and data format for the pipeline.

        Args:
            rows: List of dictionaries containing the data
            output_path: Path where the CSV file should be written
        """
        # Define the expected column order for the pipeline
        fieldnames = [
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

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the CSV file
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
