"""
Core cleaning functionality for glyphsieve.

This module provides functions for cleaning CSV headers and data.
"""

import os
from typing import Dict, Optional

import pandas as pd


def clean_header(header: str) -> str:
    """
    Clean a single header string by trimming whitespace, converting to lowercase,
    and replacing spaces with underscores.

    Args:
        header: The header string to clean

    Returns:
        The cleaned header string
    """
    # Trim whitespace
    cleaned = header.strip()
    # Convert to lowercase
    cleaned = cleaned.lower()
    # Replace spaces with underscores
    cleaned = cleaned.replace(" ", "_")
    return cleaned


def standardize_header(header: str) -> str:
    """
    Standardize common header names to a consistent format.

    Args:
        header: The cleaned header string (already lowercase with underscores)

    Returns:
        The standardized header string
    """
    # Define mapping for standard headers
    standard_headers = {
        "title": "title",
        "price": "price",
        "price_(usd)": "price_usd",
        "model_name": "model",
        "model": "model",
        "condition": "condition",
        # Add more standardized headers as needed
    }

    # Return the standardized header if it exists, otherwise return the original
    return standard_headers.get(header, header)


def clean_csv_headers(input_path: str, output_path: Optional[str] = None, dry_run: bool = False) -> Dict[str, str]:
    """
    Clean CSV headers by trimming whitespace, converting to lowercase,
    replacing spaces with underscores, and standardizing names.

    Args:
        input_path: Path to the input CSV file
        output_path: Path to the output CSV file (if None, defaults to 'cleaned_<filename>.csv')
        dry_run: If True, don't write the output file, just return the header mapping

    Returns:
        A dictionary mapping original headers to cleaned headers
    """
    # Set default output path if not provided
    if output_path is None:
        input_basename = os.path.basename(input_path)
        output_path = f"cleaned_{input_basename}"

    # Read the CSV file
    df = pd.read_csv(input_path)

    # Get the original headers
    original_headers = df.columns.tolist()

    # Clean and standardize headers
    header_mapping = {}
    new_headers = []

    for header in original_headers:
        cleaned_header = clean_header(header)
        standardized_header = standardize_header(cleaned_header)
        header_mapping[header] = standardized_header
        new_headers.append(standardized_header)

    # Rename the columns
    df.columns = new_headers

    # Write the cleaned CSV to the output path if not dry run
    if not dry_run:
        df.to_csv(output_path, index=False)

    return header_mapping
