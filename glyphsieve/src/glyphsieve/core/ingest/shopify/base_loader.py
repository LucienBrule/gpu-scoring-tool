"""
Abstract base class for Shopify JSON loaders.

This module defines the ShopifyJSONLoader abstract base class that provides
common functionality for parsing Shopify JSON exports from various vendors.
"""

import json
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from ..base_loader import SourceLoader


class ShopifyJSONLoader(SourceLoader):
    """
    Abstract base class for Shopify JSON data loaders.

    This class provides common functionality for parsing Shopify JSON exports
    and serves as the base for vendor-specific implementations. It handles
    both flat JSON format (single object with 'products' array) and JSONL
    format (line-by-line JSON objects).
    """

    def load(self, source: str | Path) -> list[dict]:
        """
        Load raw data from Shopify JSON file.

        Supports both JSONL format (each line contains a JSON object with a
        'products' array) and flat JSON format (single JSON object with a
        top-level 'products' array). Each product can have multiple variants.

        Args:
            source: Path to the Shopify JSON/JSONL file

        Returns:
            List of dictionaries containing extracted listing data

        Raises:
            FileNotFoundError: If the source file cannot be found
            ValueError: If the JSON data is malformed
        """
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source}")

        try:
            with open(source_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return self._parse_content(content)
        except Exception as e:
            raise ValueError(f"Error reading source file: {e}")

    def _parse_content(self, content: str) -> list[dict]:
        """
        Parse JSON content in either flat or JSONL format.

        Args:
            content: Raw file content as string

        Returns:
            List of dictionaries containing extracted listing data
        """
        # Try flat JSON format first
        flat_listings = self._try_parse_flat_json(content)
        if flat_listings is not None:
            return flat_listings

        # Fall back to JSONL format
        return self._parse_jsonl_format(content)

    def _try_parse_flat_json(self, content: str) -> list[dict] | None:
        """
        Try to parse content as a single JSON object with 'products' array.

        Args:
            content: Raw file content as string

        Returns:
            List of listings if successful, None if not flat JSON format
        """
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "products" in data:
                return self._extract_listings_from_products(data.get("products", []))
        except json.JSONDecodeError:
            pass
        return None

    def _parse_jsonl_format(self, content: str) -> list[dict]:
        """
        Parse content as JSONL format (line-by-line JSON objects).

        Args:
            content: Raw file content as string

        Returns:
            List of dictionaries containing extracted listing data
        """
        listings = []
        for line_num, raw_line in enumerate(content.split("\n"), 1):
            line = raw_line.strip()
            if not line:
                continue

            line_listings = self._parse_jsonl_line(line, line_num)
            if line_listings:
                listings.extend(line_listings)

        return listings

    def _parse_jsonl_line(self, line: str, line_num: int) -> list[dict] | None:
        """
        Parse a single line from JSONL format.

        Args:
            line: Single line of JSON content
            line_num: Line number for error reporting

        Returns:
            List of listings from this line, or None if parsing failed
        """
        try:
            data = json.loads(line)
            products = data.get("products", [])
            return self._extract_listings_from_products(products)
        except json.JSONDecodeError as e:
            print(f"Warning: Skipping malformed JSON at line {line_num}: {e}")
            return None

    def _extract_listings_from_products(self, products: list) -> list[dict]:
        """
        Extract listings from a list of products.

        Args:
            products: List of product dictionaries

        Returns:
            List of dictionaries containing extracted listing data
        """
        listings = []
        for product in products:
            product_listings = self._extract_product_listings(product)
            listings.extend(product_listings)
        return listings

    @abstractmethod
    def _extract_product_listings(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract listing data from a single product and its variants.

        This method must be implemented by vendor-specific subclasses to handle
        the specific structure and field mapping for each vendor's Shopify data.

        Args:
            product: Product dictionary from Shopify JSON

        Returns:
            List of listing dictionaries, one per variant
        """
        pass

    @abstractmethod
    def _extract_model(self, title: str) -> str:
        """
        Extract GPU model from product title using vendor-specific heuristics.

        Args:
            title: Product title string

        Returns:
            Extracted GPU model name
        """
        pass

    @abstractmethod
    def _infer_condition(self, title: str, tags: List[str]) -> str:
        """
        Infer product condition from title and tags using vendor-specific logic.

        Args:
            title: Product title string
            tags: List of product tags

        Returns:
            Inferred condition (e.g., "New", "Used", "Refurbished")
        """
        pass

    @abstractmethod
    def _extract_price(self, variant: Dict[str, Any]) -> float:
        """
        Extract price from variant data using vendor-specific field mapping.

        Args:
            variant: Variant dictionary from product data

        Returns:
            Price as float value
        """
        pass

    @abstractmethod
    def _extract_quantity(self, variant: Dict[str, Any]) -> str:
        """
        Extract quantity/availability from variant data.

        Args:
            variant: Variant dictionary from product data

        Returns:
            Quantity/availability string (e.g., "Available", "Unavailable")
        """
        pass
