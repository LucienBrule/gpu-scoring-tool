"""
Core normalization functionality for glyphsieve.

This module provides functions for normalizing GPU model names.
"""
import os
import re
import json
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
from rapidfuzz import fuzz, process

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
    "RTX_A2000_12GB": ["NVIDIA Rtx A2000 12Gb", "RTX A2000", "A2000 12GB", "A2000"]
}

# Regex patterns for GPU model detection
GPU_REGEX_PATTERNS = {
    "H100_PCIE_80GB": r"(?i)h[\s-]*100.*(?:pcie|pci).*(?:80gb|memory)|h[\s-]*100.*(?:80gb|memory)|h[\s-]*100.*(?:pcie|pci)",
    "A100_40GB_PCIE": r"(?i)a[\s-]*100.*(?:pcie|pci).*(?:40gb|memory)|a[\s-]*100.*(?:40gb|memory)|a[\s-]*100.*(?:pcie|pci)",
    "A800_40GB": r"(?i)a[\s-]*800.*(?:40gb|memory)|a[\s-]*800.*active",
    "RTX_PRO_6000_BLACKWELL": r"(?i)(?:rtx|nvidia).*pro.*60+0.*(?:blackwell|bw)|pro.*60+0.*(?:blackwell|bw)",
    "RTX_6000_ADA": r"(?i)(?:rtx|nvidia).*60+0.*(?:ada|generation)|rtx.*60+0",
    "A40": r"(?i)(?:nvidia\s+)?a[\s-]*40\b",
    "RTX_A6000": r"(?i)(?:rtx\s+)?a[\s-]*60+0\b",
    "L4": r"(?i)(?:nvidia\s+)?l[\s-]*4\b",
    "RTX_4000_SFF_ADA": r"(?i)(?:rtx|nvidia).*40+0.*(?:sff|ada)|rtx.*40+0",
    "A2": r"(?i)(?:nvidia\s+)?a[\s-]*2\b",
    "RTX_A4000": r"(?i)(?:rtx\s+)?a[\s-]*40+0\b",
    "RTX_A2000_12GB": r"(?i)(?:rtx\s+)?a[\s-]*20+0.*(?:12gb|12g\s*b)|rtx.*a[\s-]*20+0"
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
        with open(file_path, 'r') as f:
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
    best_match = None
    best_score = 0.0

    # Normalize the title for comparison
    normalized_title = title.lower().strip()

    # Special case for A2000 vs A2 confusion
    if "a2000" in normalized_title or "a 2000" in normalized_title:
        # Prioritize A2000 over A2 for titles containing "a2000"
        for canonical, alternatives in models.items():
            if canonical == "RTX_A2000_12GB":
                score = fuzz.token_set_ratio(canonical.lower(), normalized_title)
                if score >= threshold:
                    normalized_score = 0.8 * (score / 100.0)
                    return canonical, normalized_score

                for alt in alternatives:
                    score = fuzz.token_set_ratio(alt.lower(), normalized_title)
                    if score >= threshold:
                        normalized_score = 0.8 * (score / 100.0)
                        return canonical, normalized_score

    # Check against all model names and alternatives
    for canonical, alternatives in models.items():
        # Check the canonical name itself
        score = fuzz.token_set_ratio(canonical.lower(), normalized_title)
        if score > best_score:
            best_match = canonical
            best_score = score

        # Also try partial ratio for better matching of substrings
        partial_score = fuzz.partial_ratio(canonical.lower(), normalized_title)
        if partial_score > best_score:
            best_match = canonical
            best_score = partial_score

        # Check alternative names
        for alt in alternatives:
            score = fuzz.token_set_ratio(alt.lower(), normalized_title)
            if score > best_score:
                best_match = canonical
                best_score = score

            # Also try partial ratio for better matching of substrings
            partial_score = fuzz.partial_ratio(alt.lower(), normalized_title)
            if partial_score > best_score:
                best_match = canonical
                best_score = partial_score

    # Only return a match if it's above the threshold
    if best_score >= threshold:
        # Normalize score to 0.0-0.8 range (since exact is 1.0 and regex is 0.9)
        normalized_score = 0.8 * (best_score / 100.0)
        return best_match, normalized_score

    return None, 0.0

def normalize_gpu_model(title: str, models_file: Optional[str] = None) -> Tuple[str, str, float]:
    """
    Normalize a GPU model name from a title string.

    Args:
        title: The title string to normalize
        models_file: Optional path to a JSON file containing GPU model definitions

    Returns:
        A tuple of (canonical_model, match_type, match_score)
    """
    # Load models
    models = load_gpu_models(models_file)

    # Try exact match first
    model, score = exact_match(title, models)
    if model:
        return model, "exact", score

    # Try regex match next
    model, score = regex_match(title, GPU_REGEX_PATTERNS)
    if model:
        return model, "regex", score

    # Try fuzzy match last
    model, score = fuzzy_match(title, models)
    if model:
        return model, "fuzzy", score

    # No match found
    return "UNKNOWN", "none", 0.0

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
    if 'title' not in df.columns:
        raise ValueError("Input CSV must contain a 'title' column")

    # Create new columns for normalized data
    df['canonical_model'] = None
    df['match_type'] = None
    df['match_score'] = None

    # Normalize each title
    for idx, row in df.iterrows():
        model, match_type, score = normalize_gpu_model(row['title'], models_file)
        df.at[idx, 'canonical_model'] = model
        df.at[idx, 'match_type'] = match_type
        df.at[idx, 'match_score'] = score

    # Write the normalized data to the output file
    df.to_csv(output_path, index=False)

    return df
