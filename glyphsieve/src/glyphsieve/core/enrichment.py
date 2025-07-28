"""
Enrichment module for glyphsieve.

This module provides functions for enriching normalized GPU listings with metadata.
"""

import os
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yaml

from glyphsieve.models.gpu import GPUMetadata, GPURegistry


def load_gpu_specs(specs_file: Optional[str] = None) -> Dict[str, GPUMetadata]:
    """
    Load GPU specifications from a YAML file.

    Args:
        specs_file (Optional[str]): Path to the YAML file with GPU specifications.
            If None, uses the default file in the package resources.

    Returns:
        Dict[str, GPUMetadata]: Dictionary of GPU metadata indexed by canonical model name

    Raises:
        FileNotFoundError: If the specs file does not exist
        ValueError: If the specs file is invalid
    """
    if specs_file is None:
        # Use the default specs file in the package resources
        specs_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "gpu_specs.yaml")

    if not os.path.exists(specs_file):
        raise FileNotFoundError(f"GPU specs file not found: {specs_file}")

    try:
        with open(specs_file, "r") as f:
            specs_data = yaml.safe_load(f)

        # Validate the data using Pydantic
        registry = GPURegistry(**specs_data)
        return registry.to_dict()

    except Exception as e:
        raise ValueError(f"Invalid GPU specs file: {e!s}")


def enrich_csv(input_file: str | Path, output_file: str | Path, specs_file: Optional[str] = None) -> pd.DataFrame:
    """
    Enrich a normalized CSV file with GPU metadata.

    Args:
        input_file (Union[str, Path]): Path to the input CSV file
        output_file (Union[str, Path]): Path to the output CSV file
        specs_file (Optional[str]): Path to the YAML file with GPU specifications

    Returns:
        pd.DataFrame: The enriched DataFrame

    Raises:
        FileNotFoundError: If the input file does not exist
        ValueError: If the input file does not contain a 'canonical_model' column
    """
    # Load the input CSV
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)

    # Check if the input CSV has the required column
    if "canonical_model" not in df.columns:
        raise ValueError("Input CSV must contain a 'canonical_model' column")

    # Load GPU specifications
    gpu_specs = load_gpu_specs(specs_file)

    # Add metadata columns with default values
    df["vram_gb"] = None
    df["tdp_watts"] = None
    df["mig_support"] = None
    df["nvlink"] = None
    df["generation"] = None

    # Enrich each row with metadata
    for idx, row in df.iterrows():
        canonical_model = row["canonical_model"]
        if canonical_model in gpu_specs:
            gpu = gpu_specs[canonical_model]
            df.at[idx, "vram_gb"] = gpu.vram_gb
            df.at[idx, "tdp_watts"] = gpu.tdp_watts
            df.at[idx, "mig_support"] = gpu.mig_support
            df.at[idx, "nvlink"] = gpu.nvlink
            df.at[idx, "generation"] = gpu.generation

    # Write the enriched DataFrame to the output file
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False)

    return df
