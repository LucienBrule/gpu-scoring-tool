"""
Core normalization functionality for glyphsieve.

This module provides functions for normalizing GPU model names.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd
from rapidfuzz import fuzz

# Define canonical GPU model names based on the Final_Market_Value_GPU_Summary.csv
# These are transformed into enum-like strings (e.g., RTX_A5000)
CANONICAL_MODELS = {
    "H100_PCIE_80GB": ["NVIDIA H100 PCIe 80GB", "H100", "H100 PCIe", "H100 80GB"],
    "A100_40GB_PCIE": ["NVIDIA A100 40GB PCIe", "A100", "A100 PCIe", "A100 40GB"],
    "A800_40GB": ["NVIDIA A800 Active 40GB", "A800", "A800 40GB"],
    "RTX_PRO_6000_BLACKWELL": ["NVIDIA RTX PRO 6000 Blackwell", "RTX PRO 6000", "PRO 6000 Blackwell"],
    "RTX_6000_ADA": ["NVIDIA RTX 6000 Ada", "RTX 6000 Ada", "RTX 6000"],
    "A40": ["NVIDIA A40", "A40"],
    "RTX_A6000": ["RTX A6000", "A6000"],
    "L4": ["NVIDIA L4", "L4"],
    "RTX_4000_SFF_ADA": ["NVIDIA RTX 4000 SFF Ada", "RTX 4000 SFF", "RTX 4000 Ada"],
    "A2": ["NVIDIA A2", "A2"],
    "RTX_A4000": ["RTX A4000", "A4000"],
    "RTX_A2000_12GB": ["NVIDIA Rtx A2000 12Gb", "RTX A2000", "A2000 12GB", "A2000"],
}

# Regex patterns for GPU model detection
GPU_REGEX_PATTERNS = {
    "H100_PCIE_80GB": (
        r"(?i)h[\s-]*100.*(?:pcie|pci).*(?:80gb|memory)|" r"h[\s-]*100.*(?:80gb|memory)|" r"h[\s-]*100.*(?:pcie|pci)"
    ),
    "A100_40GB_PCIE": (
        r"(?i)a[\s-]*100.*(?:pcie|pci).*(?:40gb|memory)|" r"a[\s-]*100.*(?:40gb|memory)|" r"a[\s-]*100.*(?:pcie|pci)"
    ),
    "A800_40GB": r"(?i)a[\s-]*800.*(?:40gb|memory)|a[\s-]*800.*active",
    "RTX_PRO_6000_BLACKWELL": r"(?i)(?:rtx|nvidia).*pro.*60+0.*(?:blackwell|bw)|pro.*60+0.*(?:blackwell|bw)",
    "RTX_6000_ADA": r"(?i)(?:rtx|nvidia).*60+0.*(?:ada|generation)|rtx.*60+0",
    "A40": r"(?i)(?:nvidia\s+)?a[\s-]*40\b",
    "RTX_A6000": r"(?i)(?:rtx\s+)?a[\s-]*60+0\b",
    "L4": r"(?i)(?:nvidia\s+)?l[\s-]*4\b",
    "RTX_4000_SFF_ADA": r"(?i)(?:rtx|nvidia).*40+0.*(?:sff|ada)|rtx.*40+0",
    "A2": r"(?i)(?:nvidia\s+)?a[\s-]*2\b",
    "RTX_A4000": r"(?i)(?:rtx\s+)?a[\s-]*40+0\b",
    "RTX_A2000_12GB": r"(?i)(?:rtx\s+)?a[\s-]*20+0.*(?:12gb|12g\s*b)|rtx.*a[\s-]*20+0",
}


def load_gpu_models(file_path: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Load GPU model definitions from a JSON file if provided, otherwise use the built-in definitions.

    Args:
        file_path: Path to a JSON file containing GPU model definitions

    Returns:
        A dictionary mapping canonical model names to lists of alternative names
    """
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return CANONICAL_MODELS


def exact_match(title: str, models: Dict[str, List[str]]) -> Tuple[Optional[str], float]:
    """
    Attempt to find an exact match for the title in the models dictionary.

    Args:
        title: The title string to match
        models: Dictionary mapping canonical model names to lists of alternative names

    Returns:
        A tuple of (canonical_model, score) where score is 1.0 for exact matches
    """
    # Normalize the title for comparison
    normalized_title = title.lower().strip()

    # Check for exact matches in model names and alternatives
    for canonical, alternatives in models.items():
        # Check the canonical name itself
        if canonical.lower() == normalized_title:
            return canonical, 1.0

        # Check alternative names
        for alt in alternatives:
            if alt.lower() == normalized_title:
                return canonical, 1.0

            # Only consider it an exact match if the alternative is the entire title
            # or if it's a standalone word in the title (not part of another word)
            if normalized_title == alt.lower():
                return canonical, 1.0

    return None, 0.0


def regex_match(title: str, patterns: Dict[str, str]) -> Tuple[Optional[str], float]:
    """
    Attempt to match the title using regex patterns.

    Args:
        title: The title string to match
        patterns: Dictionary mapping canonical model names to regex patterns

    Returns:
        A tuple of (canonical_model, score) where score is 0.9 for regex matches
    """
    for canonical, pattern in patterns.items():
        if re.search(pattern, title):
            return canonical, 0.9

    return None, 0.0


def _calculate_fuzzy_score(text1: str, text2: str) -> float:
    """Calculate the best fuzzy match score between two strings using multiple algorithms."""
    token_score = fuzz.token_set_ratio(text1, text2)
    partial_score = fuzz.partial_ratio(text1, text2)
    return max(token_score, partial_score)


def _try_special_a2000_match(
    normalized_title: str, models: Dict[str, List[str]], threshold: float
) -> Tuple[Optional[str], float]:
    """Handle special case for A2000 vs A2 confusion."""
    if not ("a2000" in normalized_title or "a 2000" in normalized_title):
        return None, 0.0

    for canonical, alternatives in models.items():
        if canonical == "RTX_A2000_12GB":
            # Check canonical name
            score = fuzz.token_set_ratio(canonical.lower(), normalized_title)
            if score >= threshold:
                return canonical, 0.8 * (score / 100.0)

            # Check alternatives
            for alt in alternatives:
                score = fuzz.token_set_ratio(alt.lower(), normalized_title)
                if score >= threshold:
                    return canonical, 0.8 * (score / 100.0)

    return None, 0.0


def _find_best_fuzzy_match(normalized_title: str, models: Dict[str, List[str]]) -> Tuple[Optional[str], float]:
    """Find the best fuzzy match across all models and their alternatives."""
    best_match = None
    best_score = 0.0

    for canonical, alternatives in models.items():
        # Check canonical name
        score = _calculate_fuzzy_score(canonical.lower(), normalized_title)
        if score > best_score:
            best_match = canonical
            best_score = score

        # Check alternatives
        for alt in alternatives:
            score = _calculate_fuzzy_score(alt.lower(), normalized_title)
            if score > best_score:
                best_match = canonical
                best_score = score

    return best_match, best_score


def fuzzy_match(title: str, models: Dict[str, List[str]], threshold: float = 70.0) -> Tuple[Optional[str], float]:
    """
    Attempt to match the title using fuzzy string matching.

    Args:
        title: The title string to match
        models: Dictionary mapping canonical model names to lists of alternative names
        threshold: Minimum similarity score (0-100) to consider a match

    Returns:
        A tuple of (canonical_model, score) where score is normalized to 0.0-0.8 range
    """
    normalized_title = title.lower().strip()

    # Try special A2000 case first
    special_match, special_score = _try_special_a2000_match(normalized_title, models, threshold)
    if special_match:
        return special_match, special_score

    # Find best general fuzzy match
    best_match, best_score = _find_best_fuzzy_match(normalized_title, models)

    # Return match only if above threshold
    if best_score >= threshold:
        normalized_score = 0.8 * (best_score / 100.0)
        return best_match, normalized_score

    return None, 0.0


def _detect_non_gpu_item(title: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if an item is clearly not a GPU based on keywords.

    Args:
        title: The title string to analyze

    Returns:
        A tuple of (is_non_gpu, reason) where is_non_gpu is True if the item is not a GPU
    """
    title_lower = title.lower()

    # Keywords that indicate non-GPU items
    non_gpu_keywords = {
        "capture": "capture device",
        "tvbox": "TV tuner/capture device",
        "tv box": "TV tuner/capture device",
        "bridge": "networking/video bridge device",
        "streamer": "streaming device",
        "recorder": "recording device",
        "conferencing": "video conferencing equipment",
        "onelink": "video bridge device",
        "hdbaset": "video transmission device",
        "usb 3.0": "USB device (likely capture card)",
        "avertv": "TV tuner device",
        "ezrecorder": "recording device",
        "vaddio": "video conferencing equipment",
    }

    for keyword, reason in non_gpu_keywords.items():
        if keyword in title_lower:
            return True, f"Contains '{keyword}' - likely {reason}"

    # Check for incomplete GPU model names (common issue)
    gpu_prefixes = ["rtx", "gtx", "geforce", "quadro", "tesla", "radeon"]
    has_gpu_prefix = any(prefix in title_lower for prefix in gpu_prefixes)

    if has_gpu_prefix:
        # Check if it's an incomplete model name
        if (
            title_lower.endswith(" rtx")
            or title_lower.endswith(" geforce")
            or ("geforce rtx" in title_lower and not any(char.isdigit() for char in title_lower[-10:]))
        ):
            return True, "Incomplete GPU model name - missing specific model number"

    return False, None


def normalize_gpu_model(title: str, models_file: Optional[str] = None) -> Tuple[str, str, float, bool, Optional[str]]:
    """
    Normalize a GPU model name from a title string.

    Args:
        title: The title string to normalize
        models_file: Optional path to a JSON file containing GPU model definitions

    Returns:
        A tuple of (canonical_model, match_type, match_score, is_valid_gpu, unknown_reason)
    """
    # Check if this is clearly not a GPU item
    is_non_gpu, non_gpu_reason = _detect_non_gpu_item(title)
    if is_non_gpu:
        return "UNKNOWN", "none", 0.0, False, non_gpu_reason

    # Load models
    models = load_gpu_models(models_file)

    # Try exact match first
    model, score = exact_match(title, models)
    if model:
        return model, "exact", score, True, None

    # Try regex match next
    model, score = regex_match(title, GPU_REGEX_PATTERNS)
    if model:
        return model, "regex", score, True, None

    # Try fuzzy match last
    model, score = fuzzy_match(title, models)
    if model:
        return model, "fuzzy", score, True, None

    # No match found - assume it's a GPU but we couldn't identify the model
    return "UNKNOWN", "none", 0.0, True, "Could not match to any known GPU model"


def normalize_csv(input_path: str, output_path: str, models_file: Optional[str] = None) -> pd.DataFrame:
    """
    Normalize GPU model names in a CSV file.

    Args:
        input_path: Path to the input CSV file
        output_path: Path to the output CSV file
        models_file: Optional path to a JSON file containing GPU model definitions

    Returns:
        A pandas DataFrame with the normalized data
    """
    # Read the CSV file
    df = pd.read_csv(input_path)

    # Ensure the title column exists
    if "title" not in df.columns:
        raise ValueError("Input CSV must contain a 'title' column")

    # Create new columns for normalized data
    df["canonical_model"] = None
    df["match_type"] = None
    df["match_score"] = None
    df["is_valid_gpu"] = None
    df["unknown_reason"] = None

    # Normalize each title
    for idx, row in df.iterrows():
        model, match_type, score, is_valid_gpu, unknown_reason = normalize_gpu_model(row["title"], models_file)
        df.at[idx, "canonical_model"] = model
        df.at[idx, "match_type"] = match_type
        df.at[idx, "match_score"] = score
        df.at[idx, "is_valid_gpu"] = is_valid_gpu
        df.at[idx, "unknown_reason"] = unknown_reason

    # Write the normalized data to the output file
    df.to_csv(output_path, index=False)

    return df
