"""
Enrichment module for glyphsieve.

This module provides functions for enriching normalized GPU listings with metadata.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.gpu import (
    EnrichedGPUListingDTO,
    GPUListingDTO,
    GPUMetadata,
    GPURegistry,
)


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
        loader = GlyphSieveYamlLoader()
        resource_name = specs_file or "gpu_specs.yaml"
        return loader.load(GPURegistry, resource_name)
    except FileNotFoundError as e:
        # Re-raise FileNotFoundError to maintain the original behavior
        raise FileNotFoundError(f"GPU specs file not found: {specs_file}") from e
    except Exception as e:
        raise ValueError(f"Invalid GPU specs file: {e!s}")


def enrich_listings(records: List[GPUListingDTO], specs_file: Optional[str] = None) -> List[EnrichedGPUListingDTO]:
    """
    Enrich GPU listings with metadata from the GPU registry.

    Args:
        records: List of GPU listings to enrich
        specs_file: Optional path to a YAML file with GPU specifications

    Returns:
        List of enriched GPU listings

    Raises:
        ValueError: If the specs file is invalid
    """
    # Load GPU specifications
    gpu_registry = load_gpu_specs(specs_file)
    # Convert the registry to a dictionary for easier lookup
    gpu_specs: Dict[str, GPUMetadata] = {gpu.canonical_model: gpu for gpu in gpu_registry.gpus}

    enriched_records: List[EnrichedGPUListingDTO] = []

    # Enrich each record with metadata
    for record in records:
        canonical_model = record.canonical_model

        # Initialize with default values
        enriched_data = {
            "title": record.title,
            "price": record.price,
            "canonical_model": record.canonical_model,
            "match_type": record.match_type,
            "match_score": record.match_score,
            "vram_gb": 0,
            "tdp_w": 0,
            "mig_capable": 0,
            "slots": 1,
            "form_factor": "Standard",
            "nvlink": False,
            "generation": None,
            "cuda_cores": None,
            "pcie_generation": None,
            "notes": None,
            "warnings": None,
        }

        # If the model is found in the registry, update with actual values
        if canonical_model in gpu_specs:
            gpu = gpu_specs[canonical_model]

            enriched_data["vram_gb"] = gpu.vram_gb
            enriched_data["tdp_w"] = gpu.tdp_watts
            enriched_data["mig_capable"] = gpu.mig_support
            enriched_data["nvlink"] = gpu.nvlink
            enriched_data["generation"] = gpu.generation

            # Handle optional fields
            if gpu.slot_width is not None:
                enriched_data["slots"] = gpu.slot_width

            if gpu.cuda_cores is not None:
                enriched_data["cuda_cores"] = gpu.cuda_cores

            if gpu.pcie_generation is not None:
                enriched_data["pcie_generation"] = gpu.pcie_generation

            # Determine form factor based on model name or other attributes
            if "_SFF" in canonical_model:
                enriched_data["form_factor"] = "SFF"
            elif gpu.slot_width == 1:
                enriched_data["form_factor"] = "Single-slot"
            elif gpu.slot_width == 2:
                enriched_data["form_factor"] = "Dual-slot"

        else:
            # Model not found in registry
            enriched_data["warnings"] = f"Model '{canonical_model}' not found in GPU registry"

        # Create the enriched record
        enriched_record = EnrichedGPUListingDTO(**enriched_data)
        enriched_records.append(enriched_record)

    return enriched_records


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

    # Convert DataFrame to list of GPUListingDTO objects
    records = []
    for _, row in df.iterrows():
        # Create a dictionary with the required fields
        record_data = {
            "title": row.get("title", "Unknown"),
            "price": float(row.get("price", 0.0)),
            "canonical_model": row["canonical_model"],
            "match_type": row.get("match_type", "unknown"),
            "match_score": float(row.get("match_score", 0.0)),
        }
        records.append(GPUListingDTO(**record_data))

    # Enrich the records
    enriched_records = enrich_listings(records, specs_file)

    # Preserve all original columns that aren't in the enriched DataFrame
    # Create a mapping from canonical_model to enriched record
    enriched_map = {record.canonical_model: record.model_dump() for record in enriched_records}

    # Create a new DataFrame with all original columns
    result_df = df.copy()

    # Add or update enriched columns
    for idx, row in result_df.iterrows():
        canonical_model = row["canonical_model"]
        if canonical_model in enriched_map:
            enriched_data = enriched_map[canonical_model]
            # Add all enriched fields except those that are already in the original DataFrame
            for key, value in enriched_data.items():
                if key not in ["title", "price", "canonical_model", "match_type", "match_score"]:
                    result_df.at[idx, key] = value

    # Write the enriched DataFrame to the output file
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    result_df.to_csv(output_file, index=False)

    return result_df
