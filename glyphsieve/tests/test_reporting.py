"""
Tests for the reporting module.

This module contains tests for the reporting functionality in glyphsieve.
"""
import os

import pandas as pd
import pytest

from glyphsieve.core.reporting import (
    calculate_summary_statistics,
    find_duplicate_anomalies,
    find_price_anomalies,
    generate_markdown_report,
    generate_report,
    get_best_value_cards_under_price,
    get_top_cards_by_score,
    get_top_cards_by_score_per_dollar,
)


def test_calculate_summary_statistics():
    """Test the calculate_summary_statistics function."""
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'mig_support': 7,
            'nvlink': True,
            'tdp_watts': 350,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'mig_support': 7,
            'nvlink': False,
            'tdp_watts': 250,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1500.0,
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1600.0,
            'score': 0.3
        }
    ])
    
    # Calculate statistics
    stats = calculate_summary_statistics(df)
    
    # Check that all expected statistics are present
    assert "num_listings" in stats
    assert "unique_models" in stats
    assert "price_min" in stats
    assert "price_max" in stats
    assert "price_avg" in stats
    assert "price_median" in stats
    assert "score_min" in stats
    assert "score_max" in stats
    assert "score_mean" in stats
    assert "most_common_model" in stats
    
    # Check that the values are correct
    assert stats["num_listings"] == 4
    assert stats["unique_models"] == 3
    assert stats["price_min"] == 1500.0
    assert stats["price_max"] == 10000.0
    assert stats["price_avg"] == (10000.0 + 8000.0 + 1500.0 + 1600.0) / 4
    assert stats["price_median"] == (1600.0 + 8000.0) / 2
    assert stats["score_min"] == 0.3
    assert stats["score_max"] == 0.7
    assert stats["score_mean"] == (0.7 + 0.5 + 0.3 + 0.3) / 4
    assert stats["most_common_model"] == "RTX_4090"


def test_get_top_cards_by_score():
    """Test the get_top_cards_by_score function."""
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'price': 1500.0,
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_3090',
            'vram_gb': 24,
            'price': 1000.0,
            'score': 0.2
        }
    ])
    
    # Get top cards
    top_cards = get_top_cards_by_score(df, n=2)
    
    # Check that we got the right number of cards
    assert len(top_cards) == 2
    
    # Check that they're in the right order
    assert top_cards.iloc[0]['canonical_model'] == 'H100_PCIE_80GB'
    assert top_cards.iloc[1]['canonical_model'] == 'A100_40GB_PCIE'


def test_get_top_cards_by_score_per_dollar():
    """Test the get_top_cards_by_score_per_dollar function."""
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'price': 1500.0,
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_3090',
            'vram_gb': 24,
            'price': 1000.0,
            'score': 0.2
        }
    ])
    
    # Get top cards by score per dollar
    top_cards = get_top_cards_by_score_per_dollar(df, n=2)
    
    # Check that we got the right number of cards
    assert len(top_cards) == 2
    
    # Check that they're in the right order (RTX_3090 has best score per dollar)
    assert top_cards.iloc[0]['canonical_model'] == 'RTX_3090'
    assert top_cards.iloc[1]['canonical_model'] == 'RTX_4090'
    
    # Check that score_per_dollar was calculated correctly
    assert top_cards.iloc[0]['score_per_dollar'] == 0.2 / 1000.0
    assert top_cards.iloc[1]['score_per_dollar'] == 0.3 / 1500.0


def test_get_best_value_cards_under_price():
    """Test the get_best_value_cards_under_price function."""
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'price': 1500.0,
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_3090',
            'vram_gb': 24,
            'price': 1000.0,
            'score': 0.2
        }
    ])
    
    # Get best value cards under $2000
    best_value = get_best_value_cards_under_price(df, price_limit=2000.0, n=2)
    
    # Check that we got the right number of cards
    assert len(best_value) == 2
    
    # Check that they're in the right order and under the price limit
    assert best_value.iloc[0]['canonical_model'] == 'RTX_4090'
    assert best_value.iloc[1]['canonical_model'] == 'RTX_3090'
    assert best_value.iloc[0]['price'] <= 2000.0
    assert best_value.iloc[1]['price'] <= 2000.0


def test_find_price_anomalies():
    """Test the find_price_anomalies function."""
    # Create a test DataFrame with price anomalies
    df = pd.DataFrame([
        {
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_4090',
            'price': 2500.0,  # Significant price difference
            'score': 0.3
        },
        {
            'canonical_model': 'RTX_3090',
            'price': 1000.0,
            'score': 0.2
        },
        {
            'canonical_model': 'RTX_3090',
            'price': 1100.0,  # Small price difference, not an anomaly
            'score': 0.2
        }
    ])
    
    # Find price anomalies with default threshold
    anomalies = find_price_anomalies(df)
    
    # Check that we found the RTX 4090 as an anomaly
    assert len(anomalies) > 0
    assert 'RTX_4090' in anomalies['canonical_model'].values
    
    # Check that RTX 3090 is not an anomaly with default threshold
    assert 'RTX_3090' not in anomalies['canonical_model'].values
    
    # Test with a lower threshold to catch the RTX 3090 as well
    anomalies_low_threshold = find_price_anomalies(df, threshold=0.05)
    assert 'RTX_3090' in anomalies_low_threshold['canonical_model'].values


def test_find_duplicate_anomalies():
    """Test the find_duplicate_anomalies function."""
    # Create a test DataFrame with duplicate anomalies
    df = pd.DataFrame([
        {
            'id': 1,
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 0.3,
            'duplicate_flag': 'PRIMARY'
        },
        {
            'id': 2,
            'canonical_model': 'RTX_4090',
            'price': 1600.0,
            'score': 0.4,  # Higher score than primary
            'duplicate_flag': 'DUPLICATE_SECONDARY',
            'primary_id': 1
        },
        {
            'id': 3,
            'canonical_model': 'RTX_3090',
            'price': 1000.0,
            'score': 0.2,
            'duplicate_flag': 'PRIMARY'
        },
        {
            'id': 4,
            'canonical_model': 'RTX_3090',
            'price': 1100.0,
            'score': 0.1,  # Lower score than primary, not an anomaly
            'duplicate_flag': 'DUPLICATE_SECONDARY',
            'primary_id': 3
        }
    ])
    
    # Find duplicate anomalies
    anomalies = find_duplicate_anomalies(df)
    
    # Check that we found the RTX 4090 secondary as an anomaly
    assert len(anomalies) == 1
    assert anomalies.iloc[0]['id'] == 2
    
    # Test with a DataFrame that doesn't have the required columns
    df_no_dupes = pd.DataFrame([
        {
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 0.3
        }
    ])
    no_anomalies = find_duplicate_anomalies(df_no_dupes)
    assert len(no_anomalies) == 0


def test_generate_markdown_report(tmp_path):
    """Test the generate_markdown_report function."""
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'mig_support': 7,
            'nvlink': True,
            'tdp_watts': 350,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'mig_support': 7,
            'nvlink': False,
            'tdp_watts': 250,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1500.0,
            'score': 0.3
        }
    ])
    
    # Set up output path
    output_dir = tmp_path / "reports"
    output_dir.mkdir()
    output_path = output_dir / "test_report.md"
    
    # Generate the report
    report_path = generate_markdown_report(df, output_path)
    
    # Check that the report was created
    assert os.path.exists(report_path)
    
    # Check that the report contains expected sections
    with open(report_path, 'r') as f:
        content = f.read()
        assert "# GPU Market Insight Report" in content
        assert "## 📈 Summary Statistics" in content
        assert "## 🏆 Top 10 Cards by Score" in content
        assert "## 💰 Top 10 Cards by Score-per-Dollar" in content
        assert "## 🔥 Best Value Cards Under $2000" in content
        assert "## 📉 Price Anomalies" in content
        assert "## 🔄 Duplicate Anomalies" in content


def test_generate_report(tmp_path):
    """Test the generate_report function."""
    # Create a test CSV file
    input_file = tmp_path / "test_input.csv"
    
    # Create test data
    test_data = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'mig_support': 7,
            'nvlink': True,
            'tdp_watts': 350,
            'price': 10000.0,
            'score': 0.7
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'mig_support': 7,
            'nvlink': False,
            'tdp_watts': 250,
            'price': 8000.0,
            'score': 0.5
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1500.0,
            'score': 0.3
        }
    ])
    
    # Write test data to the input file
    test_data.to_csv(input_file, index=False)
    
    # Set up output directory
    output_dir = tmp_path / "reports"
    
    # Generate the report
    report_path = generate_report(input_file, output_dir, "md")
    
    # Check that the report was created
    assert os.path.exists(report_path)
    
    # Check that the report contains expected sections
    with open(report_path, 'r') as f:
        content = f.read()
        assert "# GPU Market Insight Report" in content
        assert "## 📈 Summary Statistics" in content
        assert "## 🏆 Top 10 Cards by Score" in content
        
    # Test with default output directory
    with pytest.raises(NotImplementedError):
        # This should raise NotImplementedError for HTML format
        generate_report(input_file, output_format="html")