"""
Core deduplication functionality for glyphsieve.

This module provides functions for identifying duplicate GPU listings
using semantic similarity on titles and other metadata.
"""
import re
import urllib.parse
from typing import Dict, List, Tuple, Optional, Any, Set
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Constants
DEFAULT_SIMILARITY_THRESHOLD = 0.85  # Lowered from 0.95 to better detect similar titles
DEFAULT_PRICE_EPSILON = 0.05  # 5% price difference tolerance

def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing tracking parameters and standardizing format.

    Args:
        url: The URL to normalize

    Returns:
        A normalized URL string
    """
    if not url or pd.isna(url):
        return ""

    # Parse the URL
    parsed = urllib.parse.urlparse(url)

    # Handle eBay URLs specially
    if 'ebay.com' in parsed.netloc:
        # Keep only the item ID part for eBay URLs
        path_parts = parsed.path.split('/')
        if 'itm' in path_parts:
            idx = path_parts.index('itm')
            if idx + 1 < len(path_parts):
                # Return just the domain and item ID
                return f"https://www.ebay.com/itm/{path_parts[idx+1]}"

    # For other URLs, remove query parameters but keep the path
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def generate_embeddings(titles: List[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Generate embeddings for a list of titles using a sentence transformer model.

    Args:
        titles: List of title strings to embed
        model_name: Name of the sentence transformer model to use

    Returns:
        A numpy array of embeddings
    """
    model = SentenceTransformer(model_name)
    return model.encode(titles, show_progress_bar=True)

def find_duplicates(
    df: pd.DataFrame,
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    price_epsilon: float = DEFAULT_PRICE_EPSILON,
    model_name: str = "all-MiniLM-L6-v2"
) -> pd.DataFrame:
    """
    Find duplicate listings in a DataFrame based on title similarity and other criteria.

    Args:
        df: DataFrame containing GPU listings with at least a 'title' column
        similarity_threshold: Threshold for cosine similarity (0.0-1.0)
        price_epsilon: Tolerance for price differences (as a fraction)
        model_name: Name of the sentence transformer model to use

    Returns:
        A DataFrame with added deduplication columns
    """
    # Ensure required columns exist
    if 'title' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'title' column")

    # Create a copy to avoid modifying the original
    result_df = df.copy()

    # Add deduplication columns
    result_df['dedup_status'] = 'UNIQUE'
    result_df['dedup_group_id'] = None

    # Generate embeddings for all titles
    embeddings = generate_embeddings(result_df['title'].tolist(), model_name)

    # Compute pairwise similarity matrix
    similarity_matrix = cosine_similarity(embeddings)

    # Track processed indices to avoid redundant work
    processed_indices = set()
    group_id = 0

    # Iterate through each listing
    for i in range(len(result_df)):
        if i in processed_indices:
            continue

        # Find similar listings based on title embeddings
        similar_indices = []
        for j in range(len(result_df)):
            if i != j and similarity_matrix[i, j] >= similarity_threshold:
                similar_indices.append(j)

        # If no similar listings found, mark as unique and continue
        if not similar_indices:
            continue

        # Check additional criteria for each similar listing
        duplicates = []
        for j in similar_indices:
            is_duplicate = False

            # Check if URLs are identical after normalization
            if 'url' in result_df.columns:
                url_i = normalize_url(result_df.iloc[i]['url'])
                url_j = normalize_url(result_df.iloc[j]['url'])
                if url_i and url_j and url_i == url_j:
                    is_duplicate = True

            # Check if prices are identical or very similar
            if 'price' in result_df.columns and not is_duplicate:
                price_i = result_df.iloc[i]['price']
                price_j = result_df.iloc[j]['price']

                # Handle non-numeric or missing prices
                if (not pd.isna(price_i) and not pd.isna(price_j) and 
                    isinstance(price_i, (int, float)) and isinstance(price_j, (int, float))):
                    # Calculate relative price difference
                    if price_i > 0:
                        rel_diff = abs(price_i - price_j) / price_i
                        if rel_diff <= price_epsilon:
                            is_duplicate = True

            # Check if seller is the same (if seller column exists)
            if 'seller' in result_df.columns and not is_duplicate:
                seller_i = result_df.iloc[i]['seller']
                seller_j = result_df.iloc[j]['seller']
                if not pd.isna(seller_i) and not pd.isna(seller_j) and seller_i == seller_j:
                    # If same seller and very similar title, likely a duplicate
                    if similarity_matrix[i, j] >= similarity_threshold - 0.05:  # Lower threshold for seller match
                        is_duplicate = True

            # If any criteria matched, add to duplicates list
            if is_duplicate:
                duplicates.append(j)

        # If duplicates found, create a group
        if duplicates:
            group_id += 1

            # Mark the current listing as primary
            result_df.at[i, 'dedup_status'] = 'DUPLICATE_PRIMARY'
            result_df.at[i, 'dedup_group_id'] = group_id
            processed_indices.add(i)

            # Mark all duplicates as secondary
            for j in duplicates:
                result_df.at[j, 'dedup_status'] = 'DUPLICATE_SECONDARY'
                result_df.at[j, 'dedup_group_id'] = group_id
                processed_indices.add(j)

    return result_df

def dedup_csv(
    input_path: str,
    output_path: str,
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    price_epsilon: float = DEFAULT_PRICE_EPSILON,
    model_name: str = "all-MiniLM-L6-v2"
) -> pd.DataFrame:
    """
    Deduplicate GPU listings in a CSV file.

    Args:
        input_path: Path to the input CSV file
        output_path: Path to the output CSV file
        similarity_threshold: Threshold for cosine similarity (0.0-1.0)
        price_epsilon: Tolerance for price differences (as a fraction)
        model_name: Name of the sentence transformer model to use

    Returns:
        A pandas DataFrame with the deduplicated data
    """
    # Read the CSV file
    df = pd.read_csv(input_path)

    # Ensure the title column exists
    if 'title' not in df.columns:
        raise ValueError("Input CSV must contain a 'title' column")

    # Find duplicates
    result_df = find_duplicates(
        df,
        similarity_threshold=similarity_threshold,
        price_epsilon=price_epsilon,
        model_name=model_name
    )

    # Write the deduplicated data to the output file
    result_df.to_csv(output_path, index=False)

    return result_df
