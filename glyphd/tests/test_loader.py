"""
Tests for the loader module.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from glyphd.core.loader import load_scored_listings, load_gpu_model_metadata, load_insight_report
from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO

# Sample data for testing
SAMPLE_SCORED_CSV = """canonical_model,vram_gb,mig_support,nvlink,tdp_watts,price,score
H100_PCIE_80GB,80,7,True,350,10000.0,0.7
A100_40GB_PCIE,40,7,False,250,8000.0,0.5185714285714286
"""

SAMPLE_MARKET_VALUE_CSV = """Model,Listing_Count,Min_Price,Median_Price,Max_Price,Avg_Price
NVIDIA H100 PCIe 80GB,7,23800.0,34995.0,49999.0,34024.71428571428
NVIDIA A100 40GB PCIe,6,12000.0,17429.495000000003,27589.26,18699.524999999998
"""

SAMPLE_GPU_SPECS_YAML = """gpus:
  - canonical_model: H100_PCIE_80GB
    vram_gb: 80
    tdp_watts: 350
    mig_support: 7
    nvlink: false
    generation: Hopper
    cuda_cores: 16896
    slot_width: 2
    pcie_generation: 5
"""

SAMPLE_INSIGHT_MD = """# GPU Market Insight Report
*Generated on 2025-07-24 12:27:10*

## 📈 Summary Statistics

- **Number of listings:** 5
- **Unique models:** 5
- **Price range:** $1000.00 - $10000.00

## 🏆 Top 10 Cards by Score

| Rank | Model | Score | VRAM (GB) | Price ($) |
|------|-------|-------|-----------|-----------|
| 1 | H100_PCIE_80GB | 0.7000 | 80 | 10000.00 |
| 2 | A100_40GB_PCIE | 0.5186 | 40 | 8000.00 |
"""

SAMPLE_SCORING_WEIGHTS_YAML = """vram_weight: 0.3
mig_weight: 0.2
nvlink_weight: 0.1
tdp_weight: 0.2
price_weight: 0.2
"""

def test_load_scored_listings():
    """Test loading scored listings from a CSV file."""
    # Create a temporary file path
    path = Path("test_scored.csv")

    # Mock the file operations
    with patch("builtins.open", mock_open(read_data=SAMPLE_SCORED_CSV)):
        with patch.object(Path, "exists", return_value=True):
            # Call the function
            listings = load_scored_listings(path)

            # Verify the results
            assert len(listings) == 2
            assert isinstance(listings[0], GPUListingDTO)
            assert listings[0].canonical_model == "H100_PCIE_80GB"
            assert listings[0].vram_gb == 80
            assert listings[0].mig_support == 7
            assert listings[0].nvlink is True
            assert listings[0].tdp_watts == 350
            assert listings[0].price == 10000.0
            assert listings[0].score == 0.7

def test_load_gpu_model_metadata():
    """Test loading GPU model metadata from a CSV file."""
    # Create a temporary file path
    path = Path("test_market_value.csv")

    # Mock the file operations
    with patch("builtins.open") as mock_file:
        # Configure the mock to return different content for different files
        def side_effect(p, *args, **kwargs):
            p_str = str(p)
            if p_str == str(path):
                return mock_open(read_data=SAMPLE_MARKET_VALUE_CSV)()
            elif p_str == "glyphsieve/src/glyphsieve/resources/gpu_specs.yaml":
                return mock_open(read_data=SAMPLE_GPU_SPECS_YAML)()
            raise FileNotFoundError(f"Mock file not found: {p}")

        mock_file.side_effect = side_effect

        with patch.object(Path, "exists", return_value=True):
            # Call the function
            models = load_gpu_model_metadata(path)

            # Verify the results
            assert len(models) == 2
            assert isinstance(models[0], GPUModelDTO)
            assert models[0].model == "NVIDIA H100 PCIe 80GB"
            assert models[0].listing_count == 7
            assert models[0].min_price == 23800.0
            assert models[0].median_price == 34995.0
            assert models[0].max_price == 49999.0
            assert models[0].avg_price == 34024.71428571428

def test_load_insight_report():
    """Test loading insight report from a markdown file."""
    # Create a temporary file path
    path = Path("test_insight.md")

    # Mock the file operations
    with patch("builtins.open") as mock_file:
        # Configure the mock to return different content for different files
        def side_effect(p, *args, **kwargs):
            p_str = str(p)
            if p_str == str(path):
                return mock_open(read_data=SAMPLE_INSIGHT_MD)()
            elif p_str == "glyphsieve/resources/scoring_weights.yaml":
                return mock_open(read_data=SAMPLE_SCORING_WEIGHTS_YAML)()
            raise FileNotFoundError(f"Mock file not found: {p}")

        mock_file.side_effect = side_effect

        with patch.object(Path, "exists", return_value=True):
            # Call the function
            report = load_insight_report(path)

            # Verify the results
            assert isinstance(report, ReportDTO)
            assert "GPU Market Insight Report" in report.markdown

            # Check that we have some summary stats
            assert len(report.summary_stats) > 0

            # The keys in summary_stats are extracted from the markdown
            # and may vary depending on the exact format of the markdown
            # So we'll just check that the values we expect are present
            assert "5" in report.summary_stats.values()
            assert "$1000.00 - $10000.00" in report.summary_stats.values()
            assert len(report.top_ranked) == 2
            assert report.top_ranked[0] == "H100_PCIE_80GB"
            assert report.top_ranked[1] == "A100_40GB_PCIE"
            assert report.scoring_weights["vram_weight"] == 0.3
            assert report.scoring_weights["mig_weight"] == 0.2
            assert report.scoring_weights["nvlink_weight"] == 0.1
            assert report.scoring_weights["tdp_weight"] == 0.2
            assert report.scoring_weights["price_weight"] == 0.2

def test_load_scored_listings_file_not_found():
    """Test loading scored listings when the file is not found."""
    # Create a temporary file path
    path = Path("nonexistent_file.csv")

    # Mock the file operations
    with patch.object(Path, "exists", return_value=False):
        # Call the function and expect an exception
        with pytest.raises(FileNotFoundError):
            load_scored_listings(path)

def test_load_gpu_model_metadata_file_not_found():
    """Test loading GPU model metadata when the file is not found."""
    # Create a temporary file path
    path = Path("nonexistent_file.csv")

    # Mock the file operations
    with patch.object(Path, "exists", return_value=False):
        # Call the function and expect an exception
        with pytest.raises(FileNotFoundError):
            load_gpu_model_metadata(path)

def test_load_insight_report_file_not_found():
    """Test loading insight report when the file is not found."""
    # Create a temporary file path
    path = Path("nonexistent_file.md")

    # Mock the file operations
    with patch.object(Path, "exists", return_value=False):
        # Call the function and expect an exception
        with pytest.raises(FileNotFoundError):
            load_insight_report(path)
