"""
Wamatek Shopify loader implementation.

This module contains the WamatekShopifyLoader class that transforms Wamatek-style
Shopify JSON listings into pipeline-compatible format.
"""

import re
from pathlib import Path
from typing import Any, Dict, List

from .base_loader import ShopifyJSONLoader


class WamatekShopifyLoader(ShopifyJSONLoader):
    """
    Loader for Wamatek Shopify JSON data.

    This loader parses JSON exports from Wamatek's Shopify store and transforms
    them into pipeline-compatible CSV format. It handles product listings with
    variants and extracts GPU model information, pricing, and availability.
    """

    def _extract_product_listings(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract listing data from a single product and its variants.

        Args:
            product: Product dictionary from Shopify JSON

        Returns:
            List of listing dictionaries, one per variant
        """
        listings = []

        # Extract base product information
        title = product.get("title", "")
        tags = product.get("tags", [])
        vendor = product.get("vendor", "")
        handle = product.get("handle", "")

        # Extract model from title using heuristics
        model = self._extract_model(title)

        # Infer condition from tags and title
        condition = self._infer_condition(title, tags)

        # Process each variant
        variants = product.get("variants", [])
        for variant in variants:
            if not isinstance(variant, dict):
                continue

            # Extract variant-specific data
            price = self._extract_price(variant)
            quantity = self._extract_quantity(variant)

            # Build source URL
            source_url = f"https://wamatek.com/products/{handle}"

            listing = {
                "model": model,
                "condition": condition,
                "price": price,
                "quantity": quantity,
                "seller": "Wamatek",
                "geographic_region": "USA",
                "listing_age": "Current",
                "source_url": source_url,
                "source_type": "Shopify_Wamatek",
                "bulk_notes": f"SKU: {variant.get('sku', 'N/A')}, Vendor: {vendor}",
                "title": title,
            }

            listings.append(listing)

        return listings

    def _extract_model(self, title: str) -> str:
        """
        Extract GPU model from product title using heuristics.

        Args:
            title: Product title string

        Returns:
            Extracted model name or original title if no pattern matches
        """
        if not title:
            return "Unknown"

        # Common GPU model patterns
        patterns = [
            # NVIDIA patterns
            r"(RTX\s*\d{4}(?:\s*Ti)?(?:\s*SUPER)?)",
            r"(GTX\s*\d{4}(?:\s*Ti)?(?:\s*SUPER)?)",
            r"(NVIDIA\s+(?:GeForce\s+)?(?:RTX|GTX)\s*\d{4}(?:\s*Ti)?(?:\s*SUPER)?)",
            # AMD patterns
            r"(RX\s*\d{4}(?:\s*XTX|\s*XT)?)",
            r"(Radeon\s+RX\s*\d{4}(?:\s*XTX|\s*XT)?)",
            # Generic patterns
            r"(\w+\s+\w+\s+\d{4})",  # Brand Model Number
        ]

        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Fallback: return first few words that might contain model info
        words = title.split()[:4]  # Take first 4 words
        return " ".join(words) if words else title

    def _infer_condition(self, title: str, tags: List[str]) -> str:
        """
        Infer product condition from title and tags.

        Args:
            title: Product title
            tags: List of product tags

        Returns:
            Inferred condition string
        """
        text_to_check = f"{title} {' '.join(tags)}".lower()

        # Check for condition keywords
        if any(keyword in text_to_check for keyword in ["refurbished", "refurb", "renewed"]):
            return "Refurbished"
        elif any(keyword in text_to_check for keyword in ["used", "pre-owned", "second-hand"]):
            return "Used"
        elif any(keyword in text_to_check for keyword in ["open box", "openbox"]):
            return "Open Box"
        else:
            return "New"  # Default assumption for retail listings

    def _extract_price(self, variant: Dict[str, Any]) -> float:
        """
        Extract price from variant data.

        Args:
            variant: Variant dictionary

        Returns:
            Price as float, or 0.0 if not available
        """
        price_str = variant.get("price", "0")
        try:
            return float(price_str)
        except (ValueError, TypeError):
            return 0.0

    def _extract_quantity(self, variant: Dict[str, Any]) -> str:
        """
        Extract quantity/availability from variant data.

        Args:
            variant: Variant dictionary

        Returns:
            Quantity string indicating availability
        """
        available = variant.get("available", False)

        if available:
            return "Available"
        else:
            return "Unavailable"

    def to_input_csv(self, rows: list[dict], output_path: Path) -> None:
        """
        Convert loaded data to pipeline-compatible CSV format.

        Args:
            rows: List of dictionaries containing the listing data
            output_path: Path where the output CSV file should be written

        Raises:
            ValueError: If the data cannot be transformed to the expected format
            IOError: If the output file cannot be written
        """
        import csv

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

        try:
            # Write the CSV file
            with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in rows:
                    # Ensure all required fields are present
                    csv_row = {}
                    for field in fieldnames:
                        csv_row[field] = row.get(field, "")

                    writer.writerow(csv_row)

        except Exception as e:
            raise OSError(f"Error writing CSV file: {e}")
