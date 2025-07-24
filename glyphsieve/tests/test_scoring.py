"""
Tests for the scoring module.

This module contains tests for the scoring functionality in glyphsieve.
"""
import os
import tempfile
import json
import yaml
import pandas as pd
import pytest
from pathlib import Path

from glyphsieve.core.scoring import (
    ScoringWeights,
    load_scoring_weights,
    ScoringStrategy,
    WeightedAdditiveScorer,
    score_csv
)


def test_scoring_weights():
    """Test the ScoringWeights model."""
    # Test default weights
    weights = ScoringWeights()
    assert weights.vram_weight == 0.3
    assert weights.mig_weight == 0.2
    assert weights.nvlink_weight == 0.1
    assert weights.tdp_weight == 0.2
    assert weights.price_weight == 0.2
    
    # Test custom weights
    custom_weights = ScoringWeights(
        vram_weight=0.4,
        mig_weight=0.1,
        nvlink_weight=0.2,
        tdp_weight=0.1,
        price_weight=0.2,
        max_vram_gb=100,
        max_mig_partitions=8,
        max_tdp_watts=800,
        max_price=20000.0
    )
    assert custom_weights.vram_weight == 0.4
    assert custom_weights.mig_weight == 0.1
    assert custom_weights.nvlink_weight == 0.2
    assert custom_weights.tdp_weight == 0.1
    assert custom_weights.price_weight == 0.2
    assert custom_weights.max_vram_gb == 100
    assert custom_weights.max_mig_partitions == 8
    assert custom_weights.max_tdp_watts == 800
    assert custom_weights.max_price == 20000.0


def test_load_scoring_weights(tmp_path):
    """Test loading scoring weights from a file."""
    # Test loading default weights when no file is provided
    weights = load_scoring_weights()
    assert weights.vram_weight == 0.3
    assert weights.mig_weight == 0.2
    assert weights.nvlink_weight == 0.1
    assert weights.tdp_weight == 0.2
    assert weights.price_weight == 0.2
    
    # Test loading weights from a file
    weights_file = tmp_path / "test_weights.yaml"
    with open(weights_file, 'w') as f:
        yaml.dump({
            "vram_weight": 0.4,
            "mig_weight": 0.1,
            "nvlink_weight": 0.2,
            "tdp_weight": 0.1,
            "price_weight": 0.2,
            "max_vram_gb": 100,
            "max_mig_partitions": 8,
            "max_tdp_watts": 800,
            "max_price": 20000.0
        }, f)
    
    weights = load_scoring_weights(weights_file)
    assert weights.vram_weight == 0.4
    assert weights.mig_weight == 0.1
    assert weights.nvlink_weight == 0.2
    assert weights.tdp_weight == 0.1
    assert weights.price_weight == 0.2
    assert weights.max_vram_gb == 100
    assert weights.max_mig_partitions == 8
    assert weights.max_tdp_watts == 800
    assert weights.max_price == 20000.0
    
    # Test error handling for non-existent file
    with pytest.raises(FileNotFoundError):
        load_scoring_weights("non_existent_file.yaml")


def test_weighted_additive_scorer():
    """Test the WeightedAdditiveScorer."""
    scorer = WeightedAdditiveScorer()
    weights = ScoringWeights()
    
    # Test scoring a row with all fields present
    row = {
        'vram_gb': 80,
        'mig_support': 7,
        'nvlink': True,
        'tdp_watts': 350,
        'price': 5000.0
    }
    score = scorer.score_listing(row, weights)
    assert 0.0 <= score <= 1.0
    
    # Test scoring a row with high values (should get a high score)
    high_row = {
        'vram_gb': 80,  # Max VRAM
        'mig_support': 7,  # Max MIG support
        'nvlink': True,  # Has NVLink
        'tdp_watts': 100,  # Low TDP (good)
        'price': 1000.0  # Low price (good)
    }
    high_score = scorer.score_listing(high_row, weights)
    assert high_score > 0.7  # Should be a high score
    
    # Test scoring a row with low values (should get a low score)
    low_row = {
        'vram_gb': 8,  # Low VRAM
        'mig_support': 0,  # No MIG support
        'nvlink': False,  # No NVLink
        'tdp_watts': 600,  # High TDP (bad)
        'price': 9000.0  # High price (bad)
    }
    low_score = scorer.score_listing(low_row, weights)
    assert low_score < 0.3  # Should be a low score
    
    # Test that high_score > low_score
    assert high_score > low_score


def test_score_listing_edge_cases():
    """Test edge cases for the score_listing function."""
    scorer = WeightedAdditiveScorer()
    weights = ScoringWeights()
    
    # Test missing fields
    row_missing_fields = {
        'vram_gb': 24,
        # Missing mig_support
        'nvlink': True,
        # Missing tdp_watts
        # Missing price
    }
    score = scorer.score_listing(row_missing_fields, weights)
    assert 0.0 <= score <= 1.0
    
    # Test zero values
    row_zero_values = {
        'vram_gb': 0,
        'mig_support': 0,
        'nvlink': False,
        'tdp_watts': 0,
        'price': 0
    }
    score = scorer.score_listing(row_zero_values, weights)
    assert 0.0 <= score <= 1.0
    
    # Test negative values (should be handled gracefully)
    row_negative_values = {
        'vram_gb': -10,
        'mig_support': -1,
        'nvlink': False,
        'tdp_watts': -200,
        'price': -1000
    }
    score = scorer.score_listing(row_negative_values, weights)
    assert 0.0 <= score <= 1.0


def test_score_dataframe():
    """Test scoring a DataFrame."""
    scorer = WeightedAdditiveScorer()
    weights = ScoringWeights()
    
    # Create a test DataFrame
    df = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'mig_support': 7,
            'nvlink': True,
            'tdp_watts': 350,
            'price': 10000.0
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'mig_support': 7,
            'nvlink': False,
            'tdp_watts': 250,
            'price': 8000.0
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1500.0
        }
    ])
    
    # Score the DataFrame
    scored_df = scorer.score_dataframe(df, weights)
    
    # Check that the score column was added
    assert 'score' in scored_df.columns
    
    # Check that all scores are between 0 and 1
    assert all(0.0 <= score <= 1.0 for score in scored_df['score'])
    
    # Check that the H100 has a higher score than the RTX 4090
    h100_score = scored_df.loc[scored_df['canonical_model'] == 'H100_PCIE_80GB', 'score'].iloc[0]
    rtx4090_score = scored_df.loc[scored_df['canonical_model'] == 'RTX_4090', 'score'].iloc[0]
    assert h100_score > rtx4090_score


def test_score_csv():
    """Test the score_csv function."""
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_input:
        # Create test data
        test_data = pd.DataFrame([
            {
                'canonical_model': 'H100_PCIE_80GB',
                'vram_gb': 80,
                'mig_support': 7,
                'nvlink': True,
                'tdp_watts': 350,
                'price': 10000.0
            },
            {
                'canonical_model': 'A100_40GB_PCIE',
                'vram_gb': 40,
                'mig_support': 7,
                'nvlink': False,
                'tdp_watts': 250,
                'price': 8000.0
            },
            {
                'canonical_model': 'RTX_4090',
                'vram_gb': 24,
                'mig_support': 0,
                'nvlink': False,
                'tdp_watts': 450,
                'price': 1500.0
            }
        ])
        
        # Write test data to the temporary file
        test_data.to_csv(temp_input.name, index=False)
    
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_output:
        pass
    
    try:
        # Score the CSV
        result_df = score_csv(temp_input.name, temp_output.name)
        
        # Check that the output file exists and has the expected columns
        assert os.path.exists(temp_output.name)
        output_df = pd.read_csv(temp_output.name)
        assert 'score' in output_df.columns
        
        # Check that all scores are between 0 and 1
        assert all(0.0 <= score <= 1.0 for score in output_df['score'])
        
        # Check that the H100 has a higher score than the RTX 4090
        h100_score = output_df.loc[output_df['canonical_model'] == 'H100_PCIE_80GB', 'score'].iloc[0]
        rtx4090_score = output_df.loc[output_df['canonical_model'] == 'RTX_4090', 'score'].iloc[0]
        assert h100_score > rtx4090_score
        
    finally:
        # Clean up temporary files
        os.unlink(temp_input.name)
        os.unlink(temp_output.name)


def test_score_csv_with_weights_file(tmp_path):
    """Test the score_csv function with a custom weights file."""
    # Create a temporary weights file
    weights_file = tmp_path / "test_weights.yaml"
    with open(weights_file, 'w') as f:
        yaml.dump({
            "vram_weight": 0.5,  # Higher weight for VRAM
            "mig_weight": 0.1,
            "nvlink_weight": 0.1,
            "tdp_weight": 0.1,
            "price_weight": 0.2,
            "max_vram_gb": 80,
            "max_mig_partitions": 7,
            "max_tdp_watts": 700,
            "max_price": 10000.0
        }, f)
    
    # Create a temporary CSV file for testing
    input_file = tmp_path / "test_input.csv"
    output_file = tmp_path / "test_output.csv"
    
    # Create test data
    test_data = pd.DataFrame([
        {
            'canonical_model': 'H100_PCIE_80GB',
            'vram_gb': 80,
            'mig_support': 7,
            'nvlink': True,
            'tdp_watts': 350,
            'price': 10000.0
        },
        {
            'canonical_model': 'A100_40GB_PCIE',
            'vram_gb': 40,
            'mig_support': 7,
            'nvlink': False,
            'tdp_watts': 250,
            'price': 8000.0
        },
        {
            'canonical_model': 'RTX_4090',
            'vram_gb': 24,
            'mig_support': 0,
            'nvlink': False,
            'tdp_watts': 450,
            'price': 1500.0
        }
    ])
    
    # Write test data to the input file
    test_data.to_csv(input_file, index=False)
    
    # Score the CSV with the custom weights file
    result_df = score_csv(input_file, output_file, weights_file)
    
    # Check that the output file exists and has the expected columns
    assert os.path.exists(output_file)
    output_df = pd.read_csv(output_file)
    assert 'score' in output_df.columns
    
    # Check that all scores are between 0 and 1
    assert all(0.0 <= score <= 1.0 for score in output_df['score'])
    
    # With higher VRAM weight, the H100 should have an even higher score compared to RTX 4090
    h100_score = output_df.loc[output_df['canonical_model'] == 'H100_PCIE_80GB', 'score'].iloc[0]
    rtx4090_score = output_df.loc[output_df['canonical_model'] == 'RTX_4090', 'score'].iloc[0]
    assert h100_score > rtx4090_score