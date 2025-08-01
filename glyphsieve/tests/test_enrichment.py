"""
Tests for the enrichment module.

This module contains tests for the enrichment functionality, including loading GPU specs
and enriching GPU listings with metadata.
"""

import os
import tempfile

import pandas as pd
import pytest

from glyphsieve.core.enrichment import enrich_csv, enrich_listings, load_gpu_specs
from glyphsieve.models.gpu import EnrichedGPUListingDTO, GPUListingDTO, GPUMetadata, GPURegistry


def test_load_gpu_specs():
    """Test loading GPU specifications from the default YAML file."""
    # Load the specs from the default file
    gpu_registry = load_gpu_specs()

    # Check that we got a GPURegistry object
    assert isinstance(gpu_registry, GPURegistry)
    assert len(gpu_registry.gpus) > 0

    # Convert to dictionary for easier testing
    gpu_specs = {gpu.canonical_model: gpu for gpu in gpu_registry.gpus}

    # Check that the keys are canonical model names and values are GPUMetadata objects
    for model_name, gpu in gpu_specs.items():
        assert isinstance(model_name, str)
        assert isinstance(gpu, GPUMetadata)

    # Check that some expected models are present
    assert "RTX_A6000" in gpu_specs
    assert "H100_PCIE_80GB" in gpu_specs

    # Check that the metadata has the expected fields
    rtx_a6000 = gpu_specs["RTX_A6000"]
    assert rtx_a6000.vram_gb == 48
    assert rtx_a6000.tdp_watts == 300
    assert rtx_a6000.mig_support == 0
    assert rtx_a6000.nvlink == True
    assert rtx_a6000.generation == "Ampere"


def test_load_gpu_specs_custom_file():
    """Test loading GPU specifications from a custom YAML file."""
    # Create a temporary YAML file with test data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(
            """
gpus:
  - canonical_model: TEST_GPU
    vram_gb: 16
    tdp_watts: 150
    mig_support: 4
    nvlink: true
    generation: Test
        """
        )
        temp_file = f.name

    try:
        # Load the specs from the custom file
        gpu_registry = load_gpu_specs(temp_file)

        # Check that we got a GPURegistry object with the expected data
        assert isinstance(gpu_registry, GPURegistry)
        assert len(gpu_registry.gpus) == 1

        # Convert to dictionary for easier testing
        gpu_specs = {gpu.canonical_model: gpu for gpu in gpu_registry.gpus}

        assert "TEST_GPU" in gpu_specs

        test_gpu = gpu_specs["TEST_GPU"]
        assert test_gpu.vram_gb == 16
        assert test_gpu.tdp_watts == 150
        assert test_gpu.mig_support == 4
        assert test_gpu.nvlink == True
        assert test_gpu.generation == "Test"

    finally:
        # Clean up the temporary file
        os.unlink(temp_file)


def test_load_gpu_specs_file_not_found():
    """Test that loading from a non-existent file raises an error."""
    with pytest.raises(FileNotFoundError):
        load_gpu_specs("non_existent_file.yaml")


def test_enrich_listings():
    """Test enriching GPU listings with metadata."""
    # Create test listings
    listings = [
        GPUListingDTO(
            title="NVIDIA RTX A6000 48GB",
            price=4500.0,
            canonical_model="RTX_A6000",
            match_type="exact",
            match_score=1.0,
        ),
        GPUListingDTO(
            title="NVIDIA RTX A5000 24GB",
            price=2400.0,
            canonical_model="RTX_A5000",
            match_type="exact",
            match_score=1.0,
        ),
        GPUListingDTO(
            title="Unknown GPU", price=1000.0, canonical_model="UNKNOWN_GPU", match_type="none", match_score=0.0
        ),
    ]

    # Enrich the listings
    enriched_listings = enrich_listings(listings)

    # Check that we got the expected number of enriched listings
    assert len(enriched_listings) == 3
    assert all(isinstance(listing, EnrichedGPUListingDTO) for listing in enriched_listings)

    # Check that the metadata is correctly added for known models
    rtx_a6000 = next(listing for listing in enriched_listings if listing.canonical_model == "RTX_A6000")
    assert rtx_a6000.vram_gb == 48
    assert rtx_a6000.tdp_w == 300
    assert rtx_a6000.mig_capable == 0
    assert rtx_a6000.nvlink == True
    assert rtx_a6000.generation == "Ampere"
    assert rtx_a6000.slots == 2
    assert rtx_a6000.form_factor == "Dual-slot"
    assert rtx_a6000.warnings is None

    rtx_a5000 = next(listing for listing in enriched_listings if listing.canonical_model == "RTX_A5000")
    assert rtx_a5000.vram_gb == 24
    assert rtx_a5000.tdp_w == 230
    assert rtx_a5000.mig_capable == 0
    assert rtx_a5000.nvlink == True
    assert rtx_a5000.generation == "Ampere"
    assert rtx_a5000.slots == 2
    assert rtx_a5000.form_factor == "Dual-slot"
    assert rtx_a5000.warnings is None

    # Check that unknown models have default values and warnings
    unknown = next(listing for listing in enriched_listings if listing.canonical_model == "UNKNOWN_GPU")
    assert unknown.vram_gb == 0
    assert unknown.tdp_w == 0
    assert unknown.mig_capable == 0
    assert unknown.nvlink == False
    assert unknown.generation is None
    assert unknown.slots == 1
    assert unknown.form_factor == "Standard"
    assert unknown.warnings is not None
    assert "not found in GPU registry" in unknown.warnings


def test_enrich_listings_sff_model():
    """Test enriching GPU listings with SFF models."""
    # Create test listing with SFF in the model name
    listing = GPUListingDTO(
        title="NVIDIA RTX 4000 SFF Ada",
        price=1500.0,
        canonical_model="RTX_4000_ADA_SFF",
        match_type="exact",
        match_score=1.0,
    )

    # Enrich the listing
    enriched_listings = enrich_listings([listing])

    # Check that the form factor is correctly set to SFF
    assert len(enriched_listings) == 1
    assert enriched_listings[0].form_factor == "SFF"


def test_enrich_csv():
    """Test enriching a CSV file with GPU metadata."""
    # Create a temporary CSV file with test data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(
            """id,title,price,canonical_model,match_type,match_score
1,NVIDIA RTX A6000 48GB,4500,RTX_A6000,exact,1.0
2,NVIDIA RTX A5000 24GB,2400,RTX_A5000,exact,1.0
3,Unknown GPU,1000,UNKNOWN_GPU,none,0.0
        """
        )
        input_file = f.name

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        output_file = f.name

    try:
        # Enrich the CSV
        _df = enrich_csv(input_file, output_file)

        # Check that the output file exists and has the expected content
        assert os.path.exists(output_file)

        # Read the output file and check its content
        output_df = pd.read_csv(output_file)

        # Check that the original columns are preserved
        assert "id" in output_df.columns
        assert "title" in output_df.columns
        assert "price" in output_df.columns
        assert "canonical_model" in output_df.columns
        assert "match_type" in output_df.columns
        assert "match_score" in output_df.columns

        # Check that the new columns are added
        assert "vram_gb" in output_df.columns
        assert "tdp_w" in output_df.columns
        assert "mig_capable" in output_df.columns
        assert "slots" in output_df.columns
        assert "form_factor" in output_df.columns
        assert "nvlink" in output_df.columns
        assert "generation" in output_df.columns
        assert "warnings" in output_df.columns

        # Check that the metadata is correctly added for known models
        rtx_a6000_row = output_df[output_df["canonical_model"] == "RTX_A6000"].iloc[0]
        assert rtx_a6000_row["vram_gb"] == 48
        assert rtx_a6000_row["tdp_w"] == 300
        assert rtx_a6000_row["mig_capable"] == 0
        assert rtx_a6000_row["slots"] == 2
        assert rtx_a6000_row["form_factor"] == "Dual-slot"
        assert rtx_a6000_row["nvlink"] == True
        assert rtx_a6000_row["generation"] == "Ampere"

        rtx_a5000_row = output_df[output_df["canonical_model"] == "RTX_A5000"].iloc[0]
        assert rtx_a5000_row["vram_gb"] == 24
        assert rtx_a5000_row["tdp_w"] == 230
        assert rtx_a5000_row["mig_capable"] == 0
        assert rtx_a5000_row["slots"] == 2
        assert rtx_a5000_row["form_factor"] == "Dual-slot"
        assert rtx_a5000_row["nvlink"] == True
        assert rtx_a5000_row["generation"] == "Ampere"

        # Check that unknown models have default values and warnings
        unknown_row = output_df[output_df["canonical_model"] == "UNKNOWN_GPU"].iloc[0]
        assert unknown_row["vram_gb"] == 0
        assert unknown_row["tdp_w"] == 0
        assert unknown_row["mig_capable"] == 0
        assert unknown_row["slots"] == 1
        assert unknown_row["form_factor"] == "Standard"
        assert unknown_row["nvlink"] == False
        assert pd.isna(unknown_row["generation"])
        assert "not found in GPU registry" in unknown_row["warnings"]

    finally:
        # Clean up the temporary files
        os.unlink(input_file)
        os.unlink(output_file)


def test_enrich_csv_input_file_not_found():
    """Test that enriching from a non-existent file raises an error."""
    with pytest.raises(FileNotFoundError):
        enrich_csv("non_existent_file.csv", "output.csv")


def test_enrich_csv_missing_canonical_model_column():
    """Test that enriching a CSV without a canonical_model column raises an error."""
    # Create a temporary CSV file without a canonical_model column
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(
            """id,title,price
1,NVIDIA RTX A6000 48GB,4500
        """
        )
        input_file = f.name

    try:
        # Attempt to enrich the CSV
        with pytest.raises(ValueError):
            enrich_csv(input_file, "output.csv")

    finally:
        # Clean up the temporary file
        os.unlink(input_file)
