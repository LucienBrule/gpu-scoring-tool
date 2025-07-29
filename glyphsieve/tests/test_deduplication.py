"""
Tests for the deduplication functionality.
"""
import os
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd

from glyphsieve.core.deduplication import dedup_csv, find_duplicates, generate_embeddings, normalize_url


class TestURLNormalization:
    """Tests for URL normalization functionality."""

    def test_normalize_empty_url(self):
        """Test that empty URLs are handled correctly."""
        assert normalize_url("") == ""
        assert normalize_url(None) == ""

    def test_normalize_ebay_url(self):
        """Test that eBay URLs are normalized correctly."""
        # Test with tracking parameters
        url = "https://www.ebay.com/itm/123456?campid=abc123&toolid=xyz"
        expected = "https://www.ebay.com/itm/123456"
        assert normalize_url(url) == expected

        # Test with different path structure
        url = "https://www.ebay.com/itm/123456/"
        expected = "https://www.ebay.com/itm/123456"
        assert normalize_url(url) == expected

    def test_normalize_other_url(self):
        """Test that non-eBay URLs are normalized correctly."""
        # Test with query parameters
        url = "https://example.com/product/gpu?ref=123&utm_source=google"
        expected = "https://example.com/product/gpu"
        assert normalize_url(url) == expected

        # Test without query parameters
        url = "https://example.com/product/gpu"
        expected = "https://example.com/product/gpu"
        assert normalize_url(url) == expected

class TestEmbeddings:
    """Tests for embedding generation functionality."""

    @patch('glyphsieve.core.deduplication.SentenceTransformer')
    def test_generate_embeddings(self, mock_transformer):
        """Test that embeddings are generated correctly."""
        # Mock the SentenceTransformer.encode method
        mock_instance = mock_transformer.return_value
        mock_instance.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])

        # Test with sample titles
        titles = ["NVIDIA RTX 3080", "NVIDIA GeForce RTX 3080"]
        embeddings = generate_embeddings(titles, "test-model")

        # Check that the model was called with the right parameters
        mock_transformer.assert_called_once_with("test-model")
        mock_instance.encode.assert_called_once_with(titles, show_progress_bar=True)

        # Check the result
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (2, 2)  # 2 titles, 2 dimensions per embedding

class TestDuplicateDetection:
    """Tests for duplicate detection functionality."""

    @patch('glyphsieve.core.deduplication.generate_embeddings')
    def test_find_duplicates_identical_titles(self, mock_generate_embeddings):
        """Test that identical titles are detected as duplicates."""
        # Create a test DataFrame with identical titles and same seller
        df = pd.DataFrame({
            'title': ['NVIDIA RTX 3080', 'NVIDIA RTX 3080'],
            'price': [800, 800],
            'url': ['https://example.com/1', 'https://example.com/2'],
            'seller': ['Seller A', 'Seller A']  # Same seller to trigger duplicate detection
        })

        # Mock the embeddings to simulate high similarity
        mock_generate_embeddings.return_value = np.array([[0.1, 0.2], [0.1, 0.2]])

        # Find duplicates - use the default threshold (0.85)
        result = find_duplicates(df)

        # Check that one primary and one secondary duplicate were found
        assert 'dedup_status' in result.columns
        assert 'dedup_group_id' in result.columns
        assert (result['dedup_status'] == 'DUPLICATE_PRIMARY').sum() == 1
        assert (result['dedup_status'] == 'DUPLICATE_SECONDARY').sum() == 1

    @patch('glyphsieve.core.deduplication.generate_embeddings')
    def test_find_duplicates_similar_titles(self, mock_generate_embeddings):
        """Test that similar titles are detected as duplicates."""
        # Create a test DataFrame with similar titles and same seller for first two
        df = pd.DataFrame({
            'title': ['NVIDIA RTX 3080', 'NVIDIA GeForce RTX 3080', 'AMD Radeon RX 6800'],
            'price': [800, 800, 700],
            'url': ['https://example.com/1', 'https://example.com/2', 'https://example.com/3'],
            'seller': ['Seller A', 'Seller A', 'Seller B']  # Same seller for first two to trigger duplicate detection
        })

        # Mock the embeddings to simulate high similarity for the first two titles
        # and low similarity for the third
        similarity_matrix = np.array([
            [1.0, 0.96, 0.5],
            [0.96, 1.0, 0.5],
            [0.5, 0.5, 1.0]
        ])

        # We need to patch cosine_similarity instead of generate_embeddings
        with patch('glyphsieve.core.deduplication.cosine_similarity', return_value=similarity_matrix):
            mock_generate_embeddings.return_value = np.array([[0.1, 0.2], [0.1, 0.21], [0.5, 0.6]])

            # Find duplicates - use the default threshold (0.85)
            result = find_duplicates(df)

            # Check that one primary, one secondary, and one unique were found
            assert (result['dedup_status'] == 'DUPLICATE_PRIMARY').sum() == 1
            assert (result['dedup_status'] == 'DUPLICATE_SECONDARY').sum() == 1
            assert (result['dedup_status'] == 'UNIQUE').sum() == 1

    @patch('glyphsieve.core.deduplication.generate_embeddings')
    def test_find_duplicates_identical_urls(self, mock_generate_embeddings):
        """Test that listings with identical URLs are detected as duplicates."""
        # Create a test DataFrame with different titles but identical URLs
        df = pd.DataFrame({
            'title': ['NVIDIA RTX 3080', 'RTX 3080 Graphics Card'],
            'price': [800, 820],
            'url': ['https://example.com/product', 'https://example.com/product']
        })

        # Mock the embeddings to simulate medium similarity
        similarity_matrix = np.array([
            [1.0, 0.85],
            [0.85, 1.0]
        ])

        # We need to patch cosine_similarity instead of generate_embeddings
        with patch('glyphsieve.core.deduplication.cosine_similarity', return_value=similarity_matrix):
            mock_generate_embeddings.return_value = np.array([[0.1, 0.2], [0.15, 0.25]])

            # Find duplicates - they should be detected due to identical URLs despite lower similarity
            result = find_duplicates(df)

            # Check that one primary and one secondary duplicate were found
            assert (result['dedup_status'] == 'DUPLICATE_PRIMARY').sum() == 1
            assert (result['dedup_status'] == 'DUPLICATE_SECONDARY').sum() == 1

class TestCSVProcessing:
    """Tests for CSV processing functionality."""

    @patch('glyphsieve.core.deduplication.find_duplicates')
    def test_dedup_csv(self, mock_find_duplicates):
        """Test that CSV files are processed correctly."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_input:
            temp_input_path = temp_input.name

            # Create a test DataFrame and write it to the temp file
            df = pd.DataFrame({
                'title': ['NVIDIA RTX 3080', 'NVIDIA GeForce RTX 3080', 'AMD Radeon RX 6800'],
                'price': [800, 800, 700],
                'url': ['https://example.com/1', 'https://example.com/2', 'https://example.com/3']
            })
            df.to_csv(temp_input_path, index=False)

        # Create a temporary output file
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_output:
            temp_output_path = temp_output.name

        try:
            # Mock the find_duplicates function to return a predefined result
            result_df = df.copy()
            result_df['dedup_status'] = ['DUPLICATE_PRIMARY', 'DUPLICATE_SECONDARY', 'UNIQUE']
            result_df['dedup_group_id'] = [1, 1, None]
            mock_find_duplicates.return_value = result_df

            # Process the CSV
            output_df = dedup_csv(temp_input_path, temp_output_path)

            # Check that find_duplicates was called with the right parameters
            mock_find_duplicates.assert_called_once()

            # Check the result
            assert isinstance(output_df, pd.DataFrame)
            assert 'dedup_status' in output_df.columns
            assert 'dedup_group_id' in output_df.columns

            # Check that the output file was created
            assert os.path.exists(temp_output_path)

            # Read the output file and check its contents
            output_df_from_file = pd.read_csv(temp_output_path)
            assert 'dedup_status' in output_df_from_file.columns
            assert 'dedup_group_id' in output_df_from_file.columns

        finally:
            # Clean up temporary files
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)
