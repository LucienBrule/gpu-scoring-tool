"""
Tests for the CLI pipeline commands.

This module contains tests for the CLI pipeline commands, including normalize, enrich, and score.
"""

import os
import tempfile

import pandas as pd
from click.testing import CliRunner

from glyphsieve.cli.enrich import enrich


def test_enrich_command_success():
    """Test the enrich command with valid input."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample input file
        input_file = os.path.join(temp_dir, "sample_normalized.csv")
        with open(input_file, "w") as f:
            f.write(
                """title,price,canonical_model,match_type,match_score
NVIDIA RTX A6000 48GB,4500,RTX_A6000,exact,1.0
NVIDIA RTX A5000 24GB,2400,RTX_A5000,exact,1.0
Unknown GPU,1000,UNKNOWN_GPU,none,0.0
"""
            )

        # Define output file
        output_file = os.path.join(temp_dir, "sample_enriched.csv")

        # Run the command
        result = runner.invoke(enrich, ["--input", input_file, "--output", output_file])

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the output file exists
        assert os.path.exists(output_file)

        # Check that the success message is printed
        # The rich console formatting may add newlines or other characters, so we just check if the output file path is in the output
        assert output_file in result.output
        assert "Enrichment complete" in result.output

        # Read the output file and check its content
        df = pd.read_csv(output_file)

        # Check that the required columns are present
        assert "vram_gb" in df.columns
        assert "tdp_w" in df.columns
        assert "mig_capable" in df.columns
        assert "slots" in df.columns
        assert "form_factor" in df.columns

        # Check that the metadata is correctly added for known models
        rtx_a6000_row = df[df["canonical_model"] == "RTX_A6000"].iloc[0]
        assert rtx_a6000_row["vram_gb"] == 48
        assert rtx_a6000_row["tdp_w"] == 300

        # Check that unknown models have warnings
        unknown_row = df[df["canonical_model"] == "UNKNOWN_GPU"].iloc[0]
        assert "not found in GPU registry" in unknown_row["warnings"]


def test_enrich_command_missing_input():
    """Test the enrich command with a missing input file."""
    runner = CliRunner()

    # Run the command with a non-existent input file
    result = runner.invoke(enrich, ["--input", "non_existent_file.csv", "--output", "output.csv"])

    # Check that the command failed gracefully
    assert result.exit_code == 0  # The command handles the error internally

    # Check that the error message is printed
    assert "Error: Input file 'non_existent_file.csv' does not exist." in result.output


def test_enrich_command_default_output():
    """Test the enrich command with default output path."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample input file
        input_file = os.path.join(temp_dir, "sample_normalized.csv")
        with open(input_file, "w") as f:
            f.write(
                """title,price,canonical_model,match_type,match_score
NVIDIA RTX A6000 48GB,4500,RTX_A6000,exact,1.0
"""
            )

        # Create the tmp/output directory
        os.makedirs("tmp/output", exist_ok=True)

        try:
            # Run the command without specifying an output file
            result = runner.invoke(enrich, ["--input", input_file])

            # Check that the command succeeded
            assert result.exit_code == 0

            # Check that the default output path is used
            assert "tmp/output/enriched_sample_normalized.csv" in result.output

            # Check that the file was created
            expected_output = os.path.join(os.getcwd(), "tmp/output", f"enriched_{os.path.basename(input_file)}")
            assert os.path.exists(expected_output)
        finally:
            # Clean up the created file
            expected_output = os.path.join(os.getcwd(), "tmp/output", f"enriched_{os.path.basename(input_file)}")
            if os.path.exists(expected_output):
                os.unlink(expected_output)


def test_enrich_command_create_parent_dirs():
    """Test that the enrich command creates parent directories for the output file."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample input file
        input_file = os.path.join(temp_dir, "sample_normalized.csv")
        with open(input_file, "w") as f:
            f.write(
                """title,price,canonical_model,match_type,match_score
NVIDIA RTX A6000 48GB,4500,RTX_A6000,exact,1.0
"""
            )

        # Define output file in a non-existent directory
        output_dir = os.path.join(temp_dir, "nested", "output", "dir")
        output_file = os.path.join(output_dir, "sample_enriched.csv")

        # Run the command
        result = runner.invoke(enrich, ["--input", input_file, "--output", output_file])

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the output directory was created
        assert os.path.exists(output_dir)

        # Check that the output file exists
        assert os.path.exists(output_file)


def test_enrich_command_invalid_input():
    """Test the enrich command with an invalid input file (missing canonical_model column)."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an invalid input file (missing canonical_model column)
        input_file = os.path.join(temp_dir, "invalid_input.csv")
        with open(input_file, "w") as f:
            f.write(
                """title,price
NVIDIA RTX A6000 48GB,4500
"""
            )

        # Define output file
        output_file = os.path.join(temp_dir, "output.csv")

        # Run the command
        result = runner.invoke(enrich, ["--input", input_file, "--output", output_file])

        # Check that the command failed
        assert result.exit_code != 0

        # Check that the error message is printed
        assert "Input CSV must contain a 'canonical_model' column" in result.output
