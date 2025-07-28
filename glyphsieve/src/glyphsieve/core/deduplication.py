"""
Core deduplication functionality for glyphsieve.

This module provides functions for identifying duplicate GPU listings
using semantic similarity on titles and other metadata.
"""

import urllib.parse
from typing import List

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
    if "ebay.com" in parsed.netloc:
        # Keep only the item ID part for eBay URLs
        path_parts = parsed.path.split("/")
        if "itm" in path_parts:
            idx = path_parts.index("itm")
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


def _find_similar_indices(similarity_matrix: np.ndarray, i: int, threshold: float) -> List[int]:
    """Find indices of listings similar to the given index based on similarity matrix."""
    similar_indices = []
    for j in range(len(similarity_matrix)):
        if i != j and similarity_matrix[i, j] >= threshold:
            similar_indices.append(j)
    return similar_indices


def _check_url_duplicate(df: pd.DataFrame, i: int, j: int) -> bool:
    """Check if two listings have identical normalized URLs."""
    if "url" not in df.columns:
        return False

    url_i = normalize_url(df.iloc[i]["url"])
    url_j = normalize_url(df.iloc[j]["url"])
    return url_i and url_j and url_i == url_j


def _check_price_duplicate(df: pd.DataFrame, i: int, j: int, price_epsilon: float) -> bool:
    """Check if two listings have similar prices within the given epsilon."""
    if "price" not in df.columns:
        return False

    price_i = df.iloc[i]["price"]
    price_j = df.iloc[j]["price"]

    # Handle non-numeric or missing prices
    if (
        pd.isna(price_i)
        or pd.isna(price_j)
        or not isinstance(price_i, int | float)
        or not isinstance(price_j, int | float)
    ):
        return False

    # Calculate relative price difference
    if price_i > 0:
        rel_diff = abs(price_i - price_j) / price_i
        return rel_diff <= price_epsilon

    return False


def _check_seller_duplicate(
    df: pd.DataFrame, i: int, j: int, similarity_matrix: np.ndarray, similarity_threshold: float
) -> bool:
    """Check if two listings are from the same seller with high similarity."""
    if "seller" not in df.columns:
        return False

    seller_i = df.iloc[i]["seller"]
    seller_j = df.iloc[j]["seller"]

    if pd.isna(seller_i) or pd.isna(seller_j) or seller_i != seller_j:
        return False

    # If same seller and very similar title, likely a duplicate
    return similarity_matrix[i, j] >= similarity_threshold - 0.05


def _is_duplicate_listing(
    df: pd.DataFrame, i: int, j: int, similarity_matrix: np.ndarray, similarity_threshold: float, price_epsilon: float
) -> bool:
    """Check if two listings are duplicates based on various criteria."""
    # Check URL match first (strongest indicator)
    if _check_url_duplicate(df, i, j):
        return True

    # Check price similarity
    if _check_price_duplicate(df, i, j, price_epsilon):
        return True

    # Check seller and similarity combination
    if _check_seller_duplicate(df, i, j, similarity_matrix, similarity_threshold):
        return True

    return False


def _find_duplicate_indices(
    df: pd.DataFrame,
    i: int,
    similar_indices: List[int],
    similarity_matrix: np.ndarray,
    similarity_threshold: float,
    price_epsilon: float,
) -> List[int]:
    """Find actual duplicates from the list of similar indices."""
    duplicates = []
    for j in similar_indices:
        if _is_duplicate_listing(df, i, j, similarity_matrix, similarity_threshold, price_epsilon):
            duplicates.append(j)
    return duplicates


def _mark_duplicate_group(
    df: pd.DataFrame, primary_idx: int, duplicate_indices: List[int], group_id: int, processed_indices: set
) -> None:
    """Mark a group of duplicates in the DataFrame."""
    # Mark the current listing as primary
    df.at[primary_idx, "dedup_status"] = "DUPLICATE_PRIMARY"
    df.at[primary_idx, "dedup_group_id"] = group_id
    processed_indices.add(primary_idx)

    # Mark all duplicates as secondary
    for j in duplicate_indices:
        df.at[j, "dedup_status"] = "DUPLICATE_SECONDARY"
        df.at[j, "dedup_group_id"] = group_id
        processed_indices.add(j)


def find_duplicates(
    df: pd.DataFrame,
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    price_epsilon: float = DEFAULT_PRICE_EPSILON,
    model_name: str = "all-MiniLM-L6-v2",
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
    if "title" not in df.columns:
        raise ValueError("Input DataFrame must contain a 'title' column")

    # Create a copy to avoid modifying the original
    result_df = df.copy()

    # Add deduplication columns
    result_df["dedup_status"] = "UNIQUE"
    result_df["dedup_group_id"] = None

    # Generate embeddings for all titles
    embeddings = generate_embeddings(result_df["title"].tolist(), model_name)

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
        similar_indices = _find_similar_indices(similarity_matrix, i, similarity_threshold)

        if not similar_indices:
            continue

        # Find actual duplicates from similar listings
        duplicates = _find_duplicate_indices(
            result_df, i, similar_indices, similarity_matrix, similarity_threshold, price_epsilon
        )

        # If duplicates found, create a group
        if duplicates:
            group_id += 1
            _mark_duplicate_group(result_df, i, duplicates, group_id, processed_indices)

    return result_df


def dedup_csv(
    input_path: str,
    output_path: str,
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    price_epsilon: float = DEFAULT_PRICE_EPSILON,
    model_name: str = "all-MiniLM-L6-v2",
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
    if "title" not in df.columns:
        raise ValueError("Input CSV must contain a 'title' column")

    # Find duplicates
    result_df = find_duplicates(
        df, similarity_threshold=similarity_threshold, price_epsilon=price_epsilon, model_name=model_name
    )

    # Write the deduplicated data to the output file
    result_df.to_csv(output_path, index=False)

    return result_df
