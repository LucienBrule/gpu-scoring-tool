"""
Tests for the normalization module.
"""

import os
import tempfile

import pandas as pd
import pytest

from glyphsieve.core.normalization import (
    CANONICAL_MODELS,
    GPU_REGEX_PATTERNS,
    exact_match,
    fuzzy_match,
    normalize_csv,
    normalize_gpu_model,
    regex_match,
)

# Test data for exact matches
EXACT_MATCH_CASES = [
    ("NVIDIA H100 PCIe 80GB", "H100_PCIE_80GB"),
    ("H100", "H100_PCIE_80GB"),
    ("A100 40GB", "A100_40GB_PCIE"),
    ("NVIDIA A800 Active 40GB", "A800_40GB"),
    ("RTX A6000", "RTX_A6000"),
    ("A40", "A40"),
]

# Test data for regex matches
REGEX_MATCH_CASES = [
    ("NVIDIA H100 PCIe with 80GB memory", "H100_PCIE_80GB"),
    ("A100 PCIe GPU with 40GB VRAM", "A100_40GB_PCIE"),
    ("NVIDIA A800 40GB GPU", "A800_40GB"),
    ("NVIDIA RTX PRO 6000 Blackwell GPU", "RTX_PRO_6000_BLACKWELL"),
    ("RTX 6000 Ada Generation", "RTX_6000_ADA"),
]

# Test data for fuzzy matches
FUZZY_MATCH_CASES = [
    # These are now matched by regex due to the more flexible regex patterns
    # But we still want to test the fuzzy matching functionality
    ("NVIDIA GeForce RTX 6000 Ada", "RTX_6000_ADA"),
    ("NVIDIA Tesla A100 40GB", "A100_40GB_PCIE"),
    ("NVIDIA Quadro RTX A6000", "RTX_A6000"),
    ("NVIDIA Data Center GPU A40", "A40"),
    # Use a more specific example for A2000 to avoid confusion with A2
    ("NVIDIA RTX A2000 12GB Workstation GPU", "RTX_A2000_12GB"),
]

# Test data for no matches
NO_MATCH_CASES = [
    "Random text with no GPU model",
    "CPU Intel i9-12900K",
    "Memory 32GB DDR5",
    "Storage 2TB NVMe SSD",
]


def test_exact_match():
    """Test exact matching of GPU model names."""
    for title, expected in EXACT_MATCH_CASES:
        model, score = exact_match(title, CANONICAL_MODELS)
        assert model == expected
        assert score == 1.0


def test_regex_match():
    """Test regex matching of GPU model names."""
    for title, expected in REGEX_MATCH_CASES:
        model, score = regex_match(title, GPU_REGEX_PATTERNS)
        assert model == expected
        assert score == 0.9


def test_fuzzy_match():
    """Test fuzzy matching of GPU model names."""
    for title, expected in FUZZY_MATCH_CASES:
        model, score = fuzzy_match(title, CANONICAL_MODELS)
        assert model == expected
        assert score > 0.0
        assert score <= 0.8


def test_no_match():
    """Test cases where no match should be found."""
    for title in NO_MATCH_CASES:
        # Exact match
        model, score = exact_match(title, CANONICAL_MODELS)
        assert model is None
        assert score == 0.0

        # Regex match
        model, score = regex_match(title, GPU_REGEX_PATTERNS)
        assert model is None
        assert score == 0.0

        # Fuzzy match (with high threshold to ensure no match)
        model, score = fuzzy_match(title, CANONICAL_MODELS, threshold=95.0)
        assert model is None
        assert score == 0.0


def test_normalize_gpu_model():
    """Test the normalize_gpu_model function."""
    # Test exact match
    model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model("NVIDIA H100 PCIe 80GB")
    assert model == "H100_PCIE_80GB"
    assert match_type == "exact"
    assert score == 1.0
    assert is_valid_gpu is True
    assert unknown_reason is None

    # Test regex match
    model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model("NVIDIA H100 PCIe with 80GB memory")
    assert model == "H100_PCIE_80GB"
    assert match_type == "regex"
    assert score == 0.9
    assert is_valid_gpu is True
    assert unknown_reason is None

    # Test regex match for hyphenated model number (previously expected to be fuzzy)
    model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model("NVIDIA H-100 PCIE")
    assert model == "H100_PCIE_80GB"
    assert match_type == "regex"
    assert score == 0.9
    assert is_valid_gpu is True
    assert unknown_reason is None

    # Test fuzzy match with a different example
    model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model("NVIDIA GeForce RTX 6000 Ada")
    assert model == "RTX_6000_ADA"
    # This could be matched by either fuzzy or regex, so we're flexible on the match type
    assert match_type in ["fuzzy", "regex"]
    assert score > 0.0
    assert score <= 0.9
    assert is_valid_gpu is True
    assert unknown_reason is None

    # Test no match
    model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model("Random text with no GPU model")
    assert model == "UNKNOWN"
    assert match_type == "none"
    assert score == 0.0
    assert is_valid_gpu is True
    assert unknown_reason == "Could not match to any known GPU model"


def test_normalize_csv():
    """Test the normalize_csv function."""
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_input:
        # Create test data
        test_data = pd.DataFrame(
            {
                "title": [
                    "NVIDIA H100 PCIe 80GB",
                    "NVIDIA A100 40GB PCIe",
                    "NVIDIA H100 PCIe with 80GB memory",
                    "NVIDIA H-100 PCIE",
                    "Random text with no GPU model",
                ],
                "price": [10000, 8000, 9500, 9000, 100],
            }
        )

        # Write test data to the temporary file
        test_data.to_csv(temp_input.name, index=False)

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_output:
        pass

    try:
        # Normalize the CSV
        _result_df = normalize_csv(temp_input.name, temp_output.name)

        # Check that the output file exists and has the expected columns
        assert os.path.exists(temp_output.name)
        output_df = pd.read_csv(temp_output.name)
        assert "canonical_model" in output_df.columns
        assert "match_type" in output_df.columns
        assert "match_score" in output_df.columns

        # Check that the normalization results are as expected
        assert output_df.loc[0, "canonical_model"] == "H100_PCIE_80GB"
        assert output_df.loc[0, "match_type"] == "exact"
        assert output_df.loc[0, "match_score"] == 1.0

        assert output_df.loc[1, "canonical_model"] == "A100_40GB_PCIE"
        assert output_df.loc[1, "match_type"] == "exact"
        assert output_df.loc[1, "match_score"] == 1.0

        assert output_df.loc[2, "canonical_model"] == "H100_PCIE_80GB"
        assert output_df.loc[2, "match_type"] == "regex"
        assert output_df.loc[2, "match_score"] == 0.9

        assert output_df.loc[3, "canonical_model"] == "H100_PCIE_80GB"
        # This is now matched by regex due to the more flexible regex patterns
        assert output_df.loc[3, "match_type"] == "regex"
        assert output_df.loc[3, "match_score"] == 0.9

        assert output_df.loc[4, "canonical_model"] == "UNKNOWN"
        assert output_df.loc[4, "match_type"] == "none"
        assert output_df.loc[4, "match_score"] == 0.0

    finally:
        # Clean up temporary files
        os.unlink(temp_input.name)
        os.unlink(temp_output.name)


def test_normalize_csv_with_models_file(tmp_path):
    """Test the normalize_csv function with a custom models file."""
    # Create a temporary models file
    models_file = tmp_path / "test_models.json"
    with open(models_file, "w") as f:
        f.write(
            """
        {
            "TEST_MODEL": ["Test GPU", "TestGPU"],
            "OTHER_MODEL": ["Other GPU", "OtherGPU"]
        }
        """
        )

    # Create a temporary CSV file for testing
    input_file = tmp_path / "test_input.csv"
    output_file = tmp_path / "test_output.csv"

    # Create test data
    test_data = pd.DataFrame({"title": ["Test GPU", "Other GPU", "Unknown GPU"], "price": [1000, 800, 500]})

    # Write test data to the temporary file
    test_data.to_csv(input_file, index=False)

    # Normalize the CSV with the custom models file
    _result_df = normalize_csv(input_file, output_file, models_file)

    # Check that the output file exists and has the expected columns
    assert os.path.exists(output_file)
    output_df = pd.read_csv(output_file)

    # Check that the normalization results are as expected
    assert output_df.loc[0, "canonical_model"] == "TEST_MODEL"
    assert output_df.loc[0, "match_type"] == "exact"
    assert output_df.loc[0, "match_score"] == 1.0

    assert output_df.loc[1, "canonical_model"] == "OTHER_MODEL"
    assert output_df.loc[1, "match_type"] == "exact"
    assert output_df.loc[1, "match_score"] == 1.0

    assert output_df.loc[2, "canonical_model"] == "UNKNOWN"
    assert output_df.loc[2, "match_type"] == "none"
    assert output_df.loc[2, "match_score"] == 0.0


def test_error_handling():
    """Test error handling in the normalize_csv function."""
    # Test with non-existent input file
    with pytest.raises(FileNotFoundError):
        normalize_csv("non_existent_file.csv", "output.csv")

    # Test with input file that doesn't have a 'title' column
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_input:
        # Create test data without a 'title' column
        test_data = pd.DataFrame({"model": ["NVIDIA H100", "NVIDIA A100"], "price": [10000, 8000]})

        # Write test data to the temporary file
        test_data.to_csv(temp_input.name, index=False)

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_output:
        pass

    try:
        # Should raise a ValueError because the input file doesn't have a 'title' column
        with pytest.raises(ValueError, match="Input CSV must contain a 'title' column"):
            normalize_csv(temp_input.name, temp_output.name)
    finally:
        # Clean up temporary files
        os.unlink(temp_input.name)
        os.unlink(temp_output.name)
