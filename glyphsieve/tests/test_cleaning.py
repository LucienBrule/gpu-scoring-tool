"""
Tests for the cleaning module.
"""
import os
import tempfile
from io import StringIO

import pandas as pd

from glyphsieve.core.cleaning import clean_csv_headers, clean_header, standardize_header


def test_clean_header():
    """Test the clean_header function."""
    # Test trimming whitespace
    assert clean_header("  Title  ") == "title"
    
    # Test converting to lowercase
    assert clean_header("PRICE") == "price"
    
    # Test replacing spaces with underscores
    assert clean_header("Model Name") == "model_name"
    
    # Test all transformations together
    assert clean_header("  Price (USD)  ") == "price_(usd)"


def test_standardize_header():
    """Test the standardize_header function."""
    # Test standard headers
    assert standardize_header("title") == "title"
    assert standardize_header("price") == "price"
    assert standardize_header("price_(usd)") == "price_usd"
    assert standardize_header("model_name") == "model"
    
    # Test non-standard header (should return the original)
    assert standardize_header("some_random_header") == "some_random_header"


def test_clean_csv_headers():
    """Test the clean_csv_headers function."""
    # Create a sample CSV content
    csv_content = """Title,Price (USD),Model Name,Condition
GPU 1,100.00,RTX 3080,New
GPU 2,200.00,RTX 3090,Used"""
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
        temp_file.write(csv_content.encode('utf-8'))
        temp_file_path = temp_file.name
    
    try:
        # Test with default output path (dry run)
        header_mapping = clean_csv_headers(temp_file_path, dry_run=True)
        
        # Check the header mapping
        expected_mapping = {
            "Title": "title",
            "Price (USD)": "price_usd",
            "Model Name": "model",
            "Condition": "condition"
        }
        assert header_mapping == expected_mapping
        
        # Test with custom output path
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as output_file:
            output_path = output_file.name
        
        try:
            clean_csv_headers(temp_file_path, output_path)
            
            # Check that the output file exists and has the correct headers
            assert os.path.exists(output_path)
            
            df = pd.read_csv(output_path)
            assert list(df.columns) == ["title", "price_usd", "model", "condition"]
            
            # Check that the data is preserved
            assert df.shape == (2, 4)
            assert df.iloc[0]["title"] == "GPU 1"
            assert df.iloc[0]["price_usd"] == 100.00
            assert df.iloc[0]["model"] == "RTX 3080"
            assert df.iloc[0]["condition"] == "New"
        
        finally:
            # Clean up the output file
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_clean_csv_headers_with_stringio():
    """Test the clean_csv_headers function with StringIO."""
    # Create a sample CSV content using StringIO
    csv_content = StringIO("""Title,Price (USD),Model Name,Condition
GPU 1,100.00,RTX 3080,New
GPU 2,200.00,RTX 3090,Used""")
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
        temp_file.write(csv_content.getvalue().encode('utf-8'))
        temp_file_path = temp_file.name
    
    try:
        # Test with default output path
        header_mapping = clean_csv_headers(temp_file_path)
        
        # Check the header mapping
        expected_mapping = {
            "Title": "title",
            "Price (USD)": "price_usd",
            "Model Name": "model",
            "Condition": "condition"
        }
        assert header_mapping == expected_mapping
        
        # Check that the output file exists
        expected_output_path = f"cleaned_{os.path.basename(temp_file_path)}"
        assert os.path.exists(expected_output_path)
        
        # Clean up the output file
        if os.path.exists(expected_output_path):
            os.unlink(expected_output_path)
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)