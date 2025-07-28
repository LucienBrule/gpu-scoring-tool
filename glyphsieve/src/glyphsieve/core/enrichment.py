"""
Enrichment module for glyphsieve.

This module provides functions for enriching normalized GPU listings with metadata.
"""

import os
from pathlib import Path
from typing import Optional

import pandas as pd

from glyphsieve.core.resources.yaml_loader import YamlLoader
from glyphsieve.models.gpu import GPURegistry


def load_gpu_specs(specs_file: Optional[str] = None) -> GPURegistry:
    """
    Load GPU specifications from a YAML file.

    Args:
        specs_file (Optional[str]): Path to the YAML file with GPU specifications.
            If None, uses the default file in the package resources.

    Returns:
        GPURegistry: Registry of GPU metadata

    Raises:
        FileNotFoundError: If the specs file does not exist
        ValueError: If the specs file is invalid
    """
    try:
        loader = YamlLoader()
        resource_name = specs_file or "gpu_specs.yaml"
        return loader.load(GPURegistry, resource_name)
    except FileNotFoundError as e:
        # Re-raise FileNotFoundError to maintain the original behavior
        raise FileNotFoundError(f"GPU specs file not found: {specs_file}") from e
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
    gpu_registry = load_gpu_specs(specs_file)
    # Convert the registry to a dictionary for easier lookup
    gpu_specs = {gpu.canonical_model: gpu for gpu in gpu_registry.gpus}

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
