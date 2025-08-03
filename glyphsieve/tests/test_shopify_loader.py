"""
Tests for Shopify loader implementations.

This module contains tests for the WamatekShopifyLoader and related functionality.
"""

import csv
import json
import tempfile
from pathlib import Path

import pytest

from glyphsieve.core.ingest.shopify.wamatek_loader import WamatekShopifyLoader


class TestWamatekShopifyLoader:
    """Test cases for WamatekShopifyLoader."""

    def setup_method(self):
        """Set up test fixtures."""
        self.loader = WamatekShopifyLoader()

    def test_load_valid_json(self):
        """Test loading valid JSON data."""
        # Create sample JSON data matching Wamatek format
        sample_data = {
            "products": [
                {
                    "title": "MSI RTX 4090 Gaming X Trio",
                    "tags": ["Graphic Cards", "Video Cards"],
                    "vendor": "MSI",
                    "handle": "msi-rtx-4090-gaming-x-trio",
                    "variants": [
                        {
                            "id": 123456,
                            "title": "Default Title",
                            "sku": "MSI-RTX4090-001",
                            "available": True,
                            "price": "1599.99",
                            "compare_at_price": "1699.99",
                        }
                    ],
                }
            ]
        }

        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            json.dump(sample_data, f)
            temp_path = f.name

        try:
            # Load data
            listings = self.loader.load(temp_path)

            # Verify results
            assert len(listings) == 1
            listing = listings[0]

            assert listing["model"] == "RTX 4090"
            assert listing["condition"] == "New"
            assert listing["price"] == 1599.99
            assert listing["quantity"] == "Available"
            assert listing["seller"] == "Wamatek"
            assert listing["geographic_region"] == "USA"
            assert listing["listing_age"] == "Current"
            assert listing["source_type"] == "Shopify_Wamatek"
            assert "wamatek.com" in listing["source_url"]
            assert listing["title"] == "MSI RTX 4090 Gaming X Trio"

        finally:
            Path(temp_path).unlink()

    def test_load_multiple_products_and_variants(self):
        """Test loading multiple products with multiple variants."""
        sample_data = {
            "products": [
                {
                    "title": "NVIDIA RTX 4080 SUPER",
                    "tags": ["Graphics"],
                    "vendor": "NVIDIA",
                    "handle": "nvidia-rtx-4080-super",
                    "variants": [
                        {"id": 1, "available": True, "price": "999.99", "sku": "RTX4080S-001"},
                        {"id": 2, "available": False, "price": "1099.99", "sku": "RTX4080S-002"},
                    ],
                },
                {
                    "title": "AMD RX 7900 XTX",
                    "tags": ["AMD", "Graphics"],
                    "vendor": "AMD",
                    "handle": "amd-rx-7900-xtx",
                    "variants": [{"id": 3, "available": True, "price": "899.99", "sku": "RX7900XTX-001"}],
                },
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            json.dump(sample_data, f)
            temp_path = f.name

        try:
            listings = self.loader.load(temp_path)

            # Should have 3 listings total (2 variants + 1 variant)
            assert len(listings) == 3

            # Check first product variants
            rtx_listings = [listing for listing in listings if "RTX 4080" in listing["model"]]
            assert len(rtx_listings) == 2
            assert rtx_listings[0]["quantity"] == "Available"
            assert rtx_listings[1]["quantity"] == "Unavailable"

            # Check second product
            amd_listings = [listing for listing in listings if "RX 7900" in listing["model"]]
            assert len(amd_listings) == 1
            assert amd_listings[0]["model"] == "RX 7900 XTX"

        finally:
            Path(temp_path).unlink()

    def test_model_extraction_heuristics(self):
        """Test model extraction from various title formats."""
        test_cases = [
            ("MSI RTX 4090 Gaming X Trio", "RTX 4090"),
            ("NVIDIA GeForce RTX 4080 SUPER", "RTX 4080 SUPER"),
            ("AMD Radeon RX 7900 XTX", "RX 7900 XTX"),
            ("ASUS GTX 1660 Ti", "GTX 1660 Ti"),
            ("Some Random GPU Title", "Some Random GPU Title"),  # Fallback
            ("", "Unknown"),  # Empty title
        ]

        for title, expected_model in test_cases:
            result = self.loader._extract_model(title)
            assert expected_model in result, f"Expected '{expected_model}' in '{result}' for title '{title}'"

    def test_condition_inference(self):
        """Test condition inference from title and tags."""
        test_cases = [
            ("RTX 4090 New", [], "New"),
            ("RTX 4090 Refurbished", [], "Refurbished"),
            ("RTX 4090", ["refurb"], "Refurbished"),
            ("RTX 4090 Used", [], "Used"),
            ("RTX 4090", ["pre-owned"], "Used"),
            ("RTX 4090 Open Box", [], "Open Box"),
            ("RTX 4090", ["openbox"], "Open Box"),
            ("RTX 4090", ["graphics", "cards"], "New"),  # Default
        ]

        for title, tags, expected_condition in test_cases:
            result = self.loader._infer_condition(title, tags)
            assert result == expected_condition, f"Expected '{expected_condition}' for title '{title}' and tags {tags}"

    def test_price_extraction(self):
        """Test price extraction from variant data."""
        test_cases = [
            ({"price": "1599.99"}, 1599.99),
            ({"price": "0"}, 0.0),
            ({"price": ""}, 0.0),
            ({"price": "invalid"}, 0.0),
            ({}, 0.0),  # Missing price
        ]

        for variant, expected_price in test_cases:
            result = self.loader._extract_price(variant)
            assert result == expected_price

    def test_quantity_extraction(self):
        """Test quantity/availability extraction."""
        test_cases = [
            ({"available": True}, "Available"),
            ({"available": False}, "Unavailable"),
            ({}, "Unavailable"),  # Missing available field
        ]

        for variant, expected_quantity in test_cases:
            result = self.loader._extract_quantity(variant)
            assert result == expected_quantity

    def test_to_input_csv(self):
        """Test CSV output generation."""
        # Sample listing data
        listings = [
            {
                "model": "RTX 4090",
                "condition": "New",
                "price": 1599.99,
                "quantity": "Available",
                "seller": "Wamatek",
                "geographic_region": "USA",
                "listing_age": "Current",
                "source_url": "https://wamatek.com/products/rtx-4090",
                "source_type": "Shopify_Wamatek",
                "bulk_notes": "SKU: RTX4090-001, Vendor: NVIDIA",
                "title": "NVIDIA RTX 4090 Graphics Card",
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.csv"

            # Generate CSV
            self.loader.to_input_csv(listings, output_path)

            # Verify file was created
            assert output_path.exists()

            # Verify CSV content
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 1
                row = rows[0]

                # Check all expected columns are present
                expected_columns = [
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

                for col in expected_columns:
                    assert col in row

                # Check specific values
                assert row["model"] == "RTX 4090"
                assert row["condition"] == "New"
                assert row["price"] == "1599.99"
                assert row["seller"] == "Wamatek"

    def test_load_file_not_found(self):
        """Test handling of missing source file."""
        with pytest.raises(FileNotFoundError):
            self.loader.load("nonexistent_file.json")

    def test_load_malformed_json(self):
        """Test handling of malformed JSON."""
        # Create file with malformed JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write('{"invalid": json}\n')
            f.write('{"products": []}\n')  # Valid line
            temp_path = f.name

        try:
            # Should skip malformed line and process valid one
            listings = self.loader.load(temp_path)
            assert len(listings) == 0  # No products in valid line

        finally:
            Path(temp_path).unlink()

    def test_missing_fields_handling(self):
        """Test graceful handling of missing fields."""
        sample_data = {
            "products": [
                {
                    # Missing title, tags, vendor, handle
                    "variants": [
                        {
                            # Missing price, available, sku
                            "id": 123
                        }
                    ]
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            json.dump(sample_data, f)
            temp_path = f.name

        try:
            listings = self.loader.load(temp_path)

            assert len(listings) == 1
            listing = listings[0]

            # Should have default/fallback values
            assert listing["model"] == "Unknown"
            assert listing["condition"] == "New"
            assert listing["price"] == 0.0
            assert listing["quantity"] == "Unavailable"
            assert listing["title"] == ""

        finally:
            Path(temp_path).unlink()

    def test_empty_products_array(self):
        """Test handling of empty products array."""
        sample_data = {"products": []}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            json.dump(sample_data, f)
            temp_path = f.name

        try:
            listings = self.loader.load(temp_path)
            assert len(listings) == 0

        finally:
            Path(temp_path).unlink()
