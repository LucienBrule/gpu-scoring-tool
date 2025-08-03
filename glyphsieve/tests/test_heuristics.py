"""
Tests for the heuristics module.

This module contains tests for the heuristics functionality, including loading heuristic
configurations and evaluating heuristics on GPU data.
"""

import os
import tempfile

import pandas as pd
import pytest

from glyphsieve.core.heuristics import (
    QuantizationHeuristic,
    apply_heuristics,
    load_heuristic_config,
)
from glyphsieve.models.heuristic import QuantizationHeuristicConfig


def test_load_heuristic_config_default():
    """Test loading the default quantization heuristic configuration."""
    # Load the default configuration
    config = load_heuristic_config()

    # Check that we got a QuantizationHeuristicConfig object with default values
    assert isinstance(config, QuantizationHeuristicConfig)
    assert config.min_vram_gb == 24
    assert config.max_tdp_watts == 300
    assert config.min_mig_support == 1


def test_load_heuristic_config_custom_file():
    """Test loading a custom quantization heuristic configuration."""
    # Create a temporary YAML file with test data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(
            """
# Custom configuration
min_vram_gb: 32
max_tdp_watts: 250
min_mig_support: 4
        """
        )
        temp_file = f.name

    try:
        # Load the configuration from the custom file
        config = load_heuristic_config(temp_file)

        # Check that we got the expected values
        assert isinstance(config, QuantizationHeuristicConfig)
        assert config.min_vram_gb == 32
        assert config.max_tdp_watts == 250
        assert config.min_mig_support == 4

    finally:
        # Clean up the temporary file
        os.unlink(temp_file)


def test_quantization_heuristic_init_default():
    """Test initializing the quantization heuristic with default configuration."""
    # Initialize the heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Check that the configuration has the expected default values
    assert heuristic.config.min_vram_gb == 24
    assert heuristic.config.max_tdp_watts == 300
    assert heuristic.config.min_mig_support == 1


def test_quantization_heuristic_init_custom():
    """Test initializing the quantization heuristic with custom configuration."""
    # Create a custom configuration
    config = QuantizationHeuristicConfig(min_vram_gb=32, max_tdp_watts=250, min_mig_support=4)

    # Initialize the heuristic with the custom configuration
    heuristic = QuantizationHeuristic(config)

    # Check that the configuration has the expected values
    assert heuristic.config.min_vram_gb == 32
    assert heuristic.config.max_tdp_watts == 250
    assert heuristic.config.min_mig_support == 4


def test_quantization_heuristic_evaluate_capable():
    """Test evaluating the quantization heuristic on a capable GPU."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row representing a capable GPU
    row = {
        "canonical_model": "H100_PCIE_80GB",
        "vram_gb": 80,
        "tdp_watts": 300,  # Exactly at the threshold
        "mig_support": 7,
        "nvlink": False,
        "generation": "Hopper",
    }

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as quantization-capable
    assert "quantization_capable" in result
    assert result["quantization_capable"]


def test_quantization_heuristic_evaluate_not_capable_vram():
    """Test evaluating the quantization heuristic on a GPU with insufficient VRAM."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row representing a GPU with insufficient VRAM
    row = {
        "canonical_model": "RTX_A4000",
        "vram_gb": 16,  # Below the threshold
        "tdp_watts": 140,
        "mig_support": 0,
        "nvlink": False,
        "generation": "Ampere",
    }

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as not quantization-capable
    assert "quantization_capable" in result
    assert not result["quantization_capable"]


def test_quantization_heuristic_evaluate_not_capable_tdp():
    """Test evaluating the quantization heuristic on a GPU with excessive TDP."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row representing a GPU with excessive TDP
    row = {
        "canonical_model": "RTX_PRO_6000_BLACKWELL",
        "vram_gb": 96,
        "tdp_watts": 400,  # Above the threshold
        "mig_support": 4,
        "nvlink": True,
        "generation": "Blackwell",
    }

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as not quantization-capable
    assert "quantization_capable" in result
    assert not result["quantization_capable"]


def test_quantization_heuristic_evaluate_not_capable_mig():
    """Test evaluating the quantization heuristic on a GPU without MIG support."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row representing a GPU without MIG support
    row = {
        "canonical_model": "RTX_A5000",
        "vram_gb": 24,  # At the threshold
        "tdp_watts": 230,
        "mig_support": 0,  # Below the threshold
        "nvlink": True,
        "generation": "Ampere",
    }

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as not quantization-capable
    assert "quantization_capable" in result
    assert not result["quantization_capable"]


def test_quantization_heuristic_evaluate_boundary():
    """Test evaluating the quantization heuristic on a GPU at the boundary of capability."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row representing a GPU at the boundary of capability
    row = {
        "canonical_model": "RTX_4500_ADA",
        "vram_gb": 24,  # Exactly at the threshold
        "tdp_watts": 300,  # Exactly at the threshold
        "mig_support": 1,  # Exactly at the threshold
        "nvlink": False,
        "generation": "Ada",
    }

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as quantization-capable
    assert "quantization_capable" in result
    assert result["quantization_capable"]


def test_quantization_heuristic_evaluate_missing_fields():
    """Test evaluating the quantization heuristic on a row with missing fields."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row with missing fields
    row = {"canonical_model": "UNKNOWN_GPU"}

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as not quantization-capable
    assert "quantization_capable" in result
    assert not result["quantization_capable"]


def test_quantization_heuristic_evaluate_null_fields():
    """Test evaluating the quantization heuristic on a row with null fields."""
    # Create a heuristic with default configuration
    heuristic = QuantizationHeuristic()

    # Create a row with null fields
    row = {"canonical_model": "UNKNOWN_GPU", "vram_gb": None, "tdp_watts": None, "mig_support": None}

    # Evaluate the heuristic
    result = heuristic.evaluate(row)

    # Check that the GPU is flagged as not quantization-capable
    assert "quantization_capable" in result
    assert not result["quantization_capable"]


def test_apply_heuristics():
    """Test applying heuristics to a CSV file."""
    # Create a temporary CSV file with test data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(
            """canonical_model,vram_gb,tdp_watts,mig_support,nvlink,generation
H100_PCIE_80GB,80,350,7,false,Hopper
RTX_A6000,48,300,0,true,Ampere
RTX_A4000,16,140,0,false,Ampere
RTX_4500_ADA,24,210,4,false,Ada
        """
        )
        input_file = f.name

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        output_file = f.name

    try:
        # Apply the heuristics
        apply_heuristics(input_file, output_file)

        # Check that the output file exists
        assert os.path.exists(output_file)

        # Read the output file and check its content
        output_df = pd.read_csv(output_file)

        # Check that the original columns are preserved
        assert "canonical_model" in output_df.columns
        assert "vram_gb" in output_df.columns
        assert "tdp_watts" in output_df.columns
        assert "mig_support" in output_df.columns
        assert "nvlink" in output_df.columns
        assert "generation" in output_df.columns

        # Check that the new column is added
        assert "quantization_capable" in output_df.columns

        # Check that the heuristic is correctly applied
        h100_row = output_df[output_df["canonical_model"] == "H100_PCIE_80GB"].iloc[0]
        assert not h100_row["quantization_capable"]  # TDP > 300

        rtx_a6000_row = output_df[output_df["canonical_model"] == "RTX_A6000"].iloc[0]
        assert not rtx_a6000_row["quantization_capable"]  # MIG = 0

        rtx_a4000_row = output_df[output_df["canonical_model"] == "RTX_A4000"].iloc[0]
        assert not rtx_a4000_row["quantization_capable"]  # VRAM < 24, MIG = 0

        rtx_4500_ada_row = output_df[output_df["canonical_model"] == "RTX_4500_ADA"].iloc[0]
        assert rtx_4500_ada_row["quantization_capable"]  # Meets all criteria

    finally:
        # Clean up the temporary files
        os.unlink(input_file)
        os.unlink(output_file)


def test_apply_heuristics_input_file_not_found():
    """Test that applying heuristics to a non-existent file raises an error."""
    with pytest.raises(FileNotFoundError):
        apply_heuristics("non_existent_file.csv", "output.csv")


def test_apply_heuristics_custom_config():
    """Test applying heuristics with a custom configuration."""
    # Create a temporary CSV file with test data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(
            """canonical_model,vram_gb,tdp_watts,mig_support,nvlink,generation
RTX_4500_ADA,24,210,4,false,Ada
        """
        )
        input_file = f.name

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        output_file = f.name

    # Create a temporary configuration file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(
            """
# Custom configuration with stricter requirements
min_vram_gb: 32
max_tdp_watts: 200
min_mig_support: 7
        """
        )
        config_file = f.name

    try:
        # Apply the heuristics with the custom configuration
        apply_heuristics(input_file, output_file, config_file)

        # Read the output file and check its content
        output_df = pd.read_csv(output_file)

        # Check that the heuristic is correctly applied with the custom configuration
        rtx_4500_ada_row = output_df[output_df["canonical_model"] == "RTX_4500_ADA"].iloc[0]
        assert not rtx_4500_ada_row["quantization_capable"]  # VRAM < 32, TDP > 200, MIG < 7

    finally:
        # Clean up the temporary files
        os.unlink(input_file)
        os.unlink(output_file)
        os.unlink(config_file)
