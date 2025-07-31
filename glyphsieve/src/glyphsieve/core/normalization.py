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
    "A10": ["NVIDIA A10", "A10"],
    "RTX_A6000": ["RTX A6000", "A6000"],
    "L4": ["NVIDIA L4", "L4"],
    "L40S": ["NVIDIA L40S", "L40S"],
    "L40": ["NVIDIA L40", "L40"],
    "RTX_4000_SFF_ADA": ["NVIDIA RTX 4000 SFF Ada", "RTX 4000 SFF", "RTX 4000 Ada"],
    "A2": ["NVIDIA A2", "A2"],
    "A16": ["NVIDIA A16", "A16"],
    "RTX_A4000": ["RTX A4000", "A4000"],
    "RTX_A2000_12GB": ["NVIDIA Rtx A2000 12Gb", "RTX A2000", "A2000 12GB", "A2000"],
    
    # Professional Ada Generation Cards
    "RTX_5000_ADA": ["NVIDIA RTX 5000 Ada", "RTX 5000 Ada", "RTX 5000"],
    "RTX_4500_ADA": ["NVIDIA RTX 4500 Ada", "RTX 4500 Ada", "RTX 4500"],
    "RTX_2000_ADA": ["NVIDIA RTX 2000 Ada", "RTX 2000 Ada", "RTX 2000"],
    "A1000": ["NVIDIA RTX A1000", "RTX A1000", "A1000"],
    "T400": ["NVIDIA T400", "T400"],
    
    # Professional Ampere Cards
    "RTX_A5500": ["NVIDIA RTX A5500", "RTX A5500", "A5500"],
    
    # RTX 50 Series Consumer Cards
    "RTX_5090": ["NVIDIA GeForce RTX 5090", "RTX 5090", "RTX5090", "GeForce RTX 5090"],
    "RTX_5080": ["NVIDIA GeForce RTX 5080", "RTX 5080", "RTX5080", "GeForce RTX 5080"],
    "RTX_5070_TI": ["NVIDIA GeForce RTX 5070 Ti", "RTX 5070 Ti", "RTX5070TI", "RTX 5070 TI", "GeForce RTX 5070 Ti"],
    "RTX_5070": ["NVIDIA GeForce RTX 5070", "RTX 5070", "RTX5070", "GeForce RTX 5070"],
    
    # RTX 40 Series Consumer Cards
    "RTX_4090": ["NVIDIA GeForce RTX 4090", "RTX 4090", "RTX4090", "GeForce RTX 4090"],
    "RTX_4080_SUPER": ["NVIDIA GeForce RTX 4080 SUPER", "RTX 4080 SUPER", "RTX4080SUPER", "GeForce RTX 4080 SUPER"],
    "RTX_4080": ["NVIDIA GeForce RTX 4080", "RTX 4080", "RTX4080", "GeForce RTX 4080"],
    "RTX_4070_TI_SUPER": ["NVIDIA GeForce RTX 4070 Ti SUPER", "RTX 4070 Ti SUPER", "RTX4070TISUPER", "GeForce RTX 4070 Ti SUPER"],
    "RTX_4070_TI": ["NVIDIA GeForce RTX 4070 Ti", "RTX 4070 Ti", "RTX4070TI", "RTX 4070 TI", "GeForce RTX 4070 Ti"],
    "RTX_4070_SUPER": ["NVIDIA GeForce RTX 4070 SUPER", "RTX 4070 SUPER", "RTX4070SUPER", "GeForce RTX 4070 SUPER"],
    "RTX_4070": ["NVIDIA GeForce RTX 4070", "RTX 4070", "RTX4070", "GeForce RTX 4070"],
    "RTX_4060_TI": ["NVIDIA GeForce RTX 4060 Ti", "RTX 4060 Ti", "RTX4060TI", "RTX 4060 TI", "GeForce RTX 4060 Ti"],
    "RTX_4060": ["NVIDIA GeForce RTX 4060", "RTX 4060", "RTX4060", "GeForce RTX 4060"],
    
    # RTX 30 Series Consumer Cards
    "RTX_3090_TI": ["NVIDIA GeForce RTX 3090 Ti", "RTX 3090 Ti", "RTX3090TI", "RTX 3090 TI", "GeForce RTX 3090 Ti"],
    "RTX_3090": ["NVIDIA GeForce RTX 3090", "RTX 3090", "RTX3090", "GeForce RTX 3090"],
    "RTX_3080_TI": ["NVIDIA GeForce RTX 3080 Ti", "RTX 3080 Ti", "RTX3080TI", "RTX 3080 TI", "GeForce RTX 3080 Ti"],
    "RTX_3080": ["NVIDIA GeForce RTX 3080", "RTX 3080", "RTX3080", "GeForce RTX 3080"],
    "RTX_3070_TI": ["NVIDIA GeForce RTX 3070 Ti", "RTX 3070 Ti", "RTX3070TI", "RTX 3070 TI", "GeForce RTX 3070 Ti"],
    "RTX_3070": ["NVIDIA GeForce RTX 3070", "RTX 3070", "RTX3070", "GeForce RTX 3070"],
    "RTX_3060_TI": ["NVIDIA GeForce RTX 3060 Ti", "RTX 3060 Ti", "RTX3060TI", "RTX 3060 TI", "GeForce RTX 3060 Ti"],
    "RTX_3060": ["NVIDIA GeForce RTX 3060", "RTX 3060", "RTX3060", "GeForce RTX 3060"],
    "RTX_3050": ["NVIDIA GeForce RTX 3050", "RTX 3050", "RTX3050", "GeForce RTX 3050"],
    
    # RTX 20 Series Consumer Cards
    "RTX_2080_TI": ["NVIDIA GeForce RTX 2080 Ti", "RTX 2080 Ti", "RTX2080TI", "RTX 2080 TI", "GeForce RTX 2080 Ti"],
    "RTX_2080_SUPER": ["NVIDIA GeForce RTX 2080 SUPER", "RTX 2080 SUPER", "RTX2080SUPER", "GeForce RTX 2080 SUPER"],
    "RTX_2080": ["NVIDIA GeForce RTX 2080", "RTX 2080", "RTX2080", "GeForce RTX 2080"],
    "RTX_2070_SUPER": ["NVIDIA GeForce RTX 2070 SUPER", "RTX 2070 SUPER", "RTX2070SUPER", "GeForce RTX 2070 SUPER"],
    "RTX_2070": ["NVIDIA GeForce RTX 2070", "RTX 2070", "RTX2070", "GeForce RTX 2070"],
    "RTX_2060_SUPER": ["NVIDIA GeForce RTX 2060 SUPER", "RTX 2060 SUPER", "RTX2060SUPER", "GeForce RTX 2060 SUPER"],
    "RTX_2060": ["NVIDIA GeForce RTX 2060", "RTX 2060", "RTX2060", "GeForce RTX 2060"],
    
    # GTX 10/16 Series Consumer Cards
    "GTX_1070": ["NVIDIA GeForce GTX 1070", "GTX 1070", "GTX1070", "GeForce GTX 1070"],
    "GTX_1660_TI": ["NVIDIA GeForce GTX 1660 Ti", "GTX 1660 Ti", "GTX1660TI", "GTX 1660 TI", "GeForce GTX 1660 Ti"],
    "GTX_1660_SUPER": ["NVIDIA GeForce GTX 1660 SUPER", "GTX 1660 SUPER", "GTX1660SUPER", "GeForce GTX 1660 SUPER"],
    "GTX_1660": ["NVIDIA GeForce GTX 1660", "GTX 1660", "GTX1660", "GeForce GTX 1660"],
    "GTX_1650_SUPER": ["NVIDIA GeForce GTX 1650 SUPER", "GTX 1650 SUPER", "GTX1650SUPER", "GeForce GTX 1650 SUPER"],
    "GTX_1650": ["NVIDIA GeForce GTX 1650", "GTX 1650", "GTX1650", "GeForce GTX 1650"],
    
    # GT Series Legacy Cards
    "GT_1030": ["NVIDIA GeForce GT 1030", "GT 1030", "GT1030", "GeForce GT 1030"],
    "GT_730": ["NVIDIA GeForce GT 730", "GT 730", "GT730", "GeForce GT 730"],
    "GT_710": ["NVIDIA GeForce GT 710", "GT 710", "GT710", "GeForce GT 710"],
    
    # Quadro T Series Professional Cards
    "T2000": ["NVIDIA Quadro T2000", "Quadro T2000", "T2000"],
    "T1000": ["NVIDIA Quadro T1000", "Quadro T1000", "T1000"],
    "T600": ["NVIDIA Quadro T600", "Quadro T600", "T600"],
    
    # Quadro Legacy Professional Cards
    "QUADRO_M5000": ["NVIDIA Quadro M5000", "Quadro M5000", "M5000"],
    "QUADRO_K5200": ["NVIDIA Quadro K5200", "Quadro K5200", "K5200"],
    
    # Grid/Tesla Legacy Cards
    "GRID_P4": ["NVIDIA GRID P4", "GRID P4", "P4"],
    
    # RTX A Series Professional Cards
    "RTX_A400": ["NVIDIA RTX A400", "RTX A400", "A400"],
    
    # Quadro RTX Series Professional Cards
    "RTX_8000": ["NVIDIA Quadro RTX 8000", "Quadro RTX 8000", "RTX 8000", "RTX8000"],
    
    # Tesla Series Legacy Cards
    "T4": ["NVIDIA Tesla T4", "Tesla T4", "T4"],
    "K1": ["NVIDIA Tesla K1", "Tesla K1", "GRID K1", "K1"],
    "K2": ["NVIDIA Tesla K2", "Tesla K2", "GRID K2", "K2"],
    "M6": ["NVIDIA Tesla M6", "Tesla M6", "M6"],
    "M60": ["NVIDIA Tesla M60", "Tesla M60", "M60"],
    "P40": ["NVIDIA Tesla P40", "Tesla P40", "P40"],
    "V100": ["NVIDIA Tesla V100", "Tesla V100", "V100"],
    
    # Legacy GeForce Cards (for better low-confidence fuzzy match handling)
    "GEFORCE_210": ["NVIDIA GeForce 210", "GeForce 210", "210"],
    "GEFORCE_GT_1030": ["NVIDIA GeForce GT 1030", "GeForce GT 1030", "GT 1030"],
}

# Regex patterns for GPU model detection
GPU_REGEX_PATTERNS = {
    "H100_PCIE_80GB": (
        r"(?i)h[\s-]*100.*(?:pcie|pci).*(?:80gb|memory)|" r"h[\s-]*100.*(?:80gb|memory)|" r"h[\s-]*100.*(?:pcie|pci)"
    ),
    "A100_40GB_PCIE": (
        r"(?i)(?:cisco\s+)?(?:nvidia\s+)?(?:tesla\s+)?a[\s-]*100.*(?:pcie|pci).*(?:40gb|80gb|memory)|" r"(?:cisco\s+)?(?:nvidia\s+)?(?:tesla\s+)?a[\s-]*100.*(?:40gb|80gb|memory)|" r"(?:cisco\s+)?(?:nvidia\s+)?(?:tesla\s+)?a[\s-]*100.*(?:pcie|pci)|" r"(?:cisco\s+)?(?:nvidia\s+)?(?:tesla\s+)?a[\s-]*100\b(?!\s*0)"
    ),
    "A800_40GB": r"(?i)a[\s-]*800.*(?:40gb|memory)|a[\s-]*800.*active",
    "RTX_PRO_6000_BLACKWELL": r"(?i)(?:rtx|nvidia).*pro.*60+0\b",
    "RTX_6000_ADA": r"(?i)(?:rtx|nvidia).*60+0.*(?:ada|generation)\b",
    "A40": r"(?i)(?:nvidia\s+)?a[\s-]*40\b",
    "A10": r"(?i)(?:nvidia\s+)?a[\s-]*10\b",
    "RTX_A6000": r"(?i)(?:rtx\s+)?a[\s-]*60+0\b",
    "L4": r"(?i)(?:nvidia\s+)?l[\s-]*4\b(?!.*(?:tesla|grid|k1|k2|m6|m60|p40|v100|t4))",
    "L40S": r"(?i)(?:nvidia\s+)?l[\s-]*40s\b",
    "L40": r"(?i)(?:nvidia\s+)?l[\s-]*40\b(?!\s*s)",
    "RTX_4000_SFF_ADA": r"(?i)(?:rtx|nvidia).*40+0.*(?:sff|ada)|rtx.*40+0",
    "A2": r"(?i)(?:nvidia\s+)?a[\s-]*2\b(?!\s*6)",
    "A16": r"(?i)(?:nvidia\s+)?a[\s-]*16\b",
    "RTX_A4000": r"(?i)(?:rtx\s+)?a[\s-]*40+0\b",
    "RTX_A2000_12GB": r"(?i)(?:rtx\s+)?a[\s-]*20+0.*(?:12gb|12g\s*b)|rtx.*a[\s-]*20+0",
    
    # Professional Ada Generation Cards
    "RTX_5000_ADA": r"(?i)(?:rtx|nvidia).*5000.*(?:ada|generation)|rtx.*5000.*ada",
    "RTX_4500_ADA": r"(?i)(?:rtx|nvidia).*4500.*(?:ada|generation)|rtx.*4500",
    "RTX_2000_ADA": r"(?i)(?:rtx|nvidia).*20+0.*(?:ada|generation)|rtx.*20+0.*ada",
    "A1000": r"(?i)(?:nvidia\s+)?(?:rtx\s+)?a[\s-]*10+0\b(?!.*a100)",
    "T400": r"(?i)(?:nvidia\s+)?t[\s-]*40+0\b",
    
    # Professional Ampere Cards
    "RTX_A5500": r"(?i)(?:nvidia\s+)?(?:rtx\s+)?a[\s-]*55+0\b",
    
    # RTX 50 Series Consumer Cards
    "RTX_5090": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*50+90\b",
    "RTX_5080": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*50+80\b",
    "RTX_5070_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*50+70[\s-]*ti\b",
    "RTX_5070": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*50+70\b(?!\s*ti)",
    
    # RTX 40 Series Consumer Cards
    "RTX_4090": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+90\b",
    "RTX_4080_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+80[\s-]*super\b",
    "RTX_4080": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+80\b(?!\s*super)",
    "RTX_4070_TI_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+70[\s-]*ti[\s-]*super\b",
    "RTX_4070_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+70[\s-]*ti\b(?!\s*super)",
    "RTX_4070_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+70[\s-]*super\b",
    "RTX_4070": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+70\b(?!\s*(?:ti|super))",
    "RTX_4060_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+60[\s-]*ti\b",
    "RTX_4060": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*40+60\b(?!\s*ti)",
    
    # RTX 30 Series Consumer Cards
    "RTX_3090_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+90[\s-]*ti\b",
    "RTX_3090": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+90\b(?!\s*ti)",
    "RTX_3080_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+80[\s-]*ti\b",
    "RTX_3080": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+80\b(?!\s*ti)",
    "RTX_3070_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+70[\s-]*ti\b",
    "RTX_3070": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+70\b(?!\s*ti)",
    "RTX_3060_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+60[\s-]*ti\b",
    "RTX_3060": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+60\b(?!\s*ti)",
    "RTX_3050": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*30+50\b",
    
    # RTX 20 Series Consumer Cards
    "RTX_2080_TI": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+80[\s-]*ti\b",
    "RTX_2080_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+80[\s-]*super\b",
    "RTX_2080": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+80\b(?!\s*(?:ti|super))",
    "RTX_2070_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+70[\s-]*super\b",
    "RTX_2070": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+70\b(?!\s*super)",
    "RTX_2060_SUPER": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+60[\s-]*super\b",
    "RTX_2060": r"(?i)(?:geforce\s+)?(?:rtx|nvidia)[\s-]*20+60\b(?!\s*super)",
    
    # GTX 10/16 Series Consumer Cards
    "GTX_1070": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*10+70\b",
    "GTX_1660_TI": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*16+60[\s-]*ti\b",
    "GTX_1660_SUPER": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*16+60[\s-]*super\b",
    "GTX_1660": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*16+60\b(?!\s*(?:ti|super))",
    "GTX_1650_SUPER": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*16+50[\s-]*super\b",
    "GTX_1650": r"(?i)(?:geforce\s+)?(?:gtx|nvidia)[\s-]*16+50\b(?!\s*super)",
    
    # GT Series Legacy Cards
    "GT_1030": r"(?i)(?:geforce\s+)?(?:gt|nvidia)[\s-]*10+30\b",
    "GT_730": r"(?i)(?:geforce\s+)?(?:gt|nvidia)[\s-]*7+30\b",
    "GT_710": r"(?i)(?:geforce\s+)?(?:gt|nvidia)[\s-]*7+10\b",
    
    # Quadro T Series Professional Cards
    "T2000": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?t[\s-]*20+0\b",
    "T1000": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?t[\s-]*10+0\b",
    "T600": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?t[\s-]*60+0\b",
    
    # Quadro Legacy Professional Cards
    "QUADRO_M5000": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?m[\s-]*50+0\b",
    "QUADRO_K5200": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?k[\s-]*52+0\b",
    
    # Grid/Tesla Legacy Cards
    "GRID_P4": r"(?i)(?:nvidia\s+)?(?:grid\s+)?p[\s-]*4\b",
    
    # RTX A Series Professional Cards
    "RTX_A400": r"(?i)(?:nvidia\s+)?(?:rtx\s+)?a[\s-]*40+0\b(?!.*(?:rtx\s+a40+0|a40+0))",
    
    # Quadro RTX Series Professional Cards
    "RTX_8000": r"(?i)(?:nvidia\s+)?(?:quadro\s+)?(?:rtx\s+)?8[\s-]*0+0+\b",
    
    # Tesla Series Legacy Cards
    "T4": r"(?i)(?:nvidia\s+)?(?:tesla\s+)?t[\s-]*4\b",
    "K1": r"(?i)(?:nvidia\s+)?(?:tesla\s+|grid\s+)?k[\s-]*1\b",
    "K2": r"(?i)(?:nvidia\s+)?(?:tesla\s+|grid\s+)?k[\s-]*2\b",
    "M6": r"(?i)(?:nvidia\s+)?(?:tesla\s+)?m[\s-]*6\b",
    "M60": r"(?i)(?:nvidia\s+)?(?:tesla\s+)?m[\s-]*60\b",
    "P40": r"(?i)(?:nvidia\s+)?(?:tesla\s+)?p[\s-]*40\b",
    "V100": r"(?i)(?:nvidia\s+)?(?:tesla\s+)?v[\s-]*100\b",
    
    # Legacy GeForce Cards (for better low-confidence fuzzy match handling)
    "GEFORCE_210": r"(?i)(?:nvidia\s+)?(?:geforce\s+)?2+10\b",
    "GEFORCE_GT_1030": r"(?i)(?:nvidia\s+)?(?:geforce\s+)?(?:gt\s+)?10+30\b",
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


def exact_match(title: str, models: Dict[str, List[str]]) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Attempt to find an exact match for the title in the models dictionary.

    Args:
        title: The title string to match
        models: Dictionary mapping canonical model names to lists of alternative names

    Returns:
        A tuple of (canonical_model, score, match_notes) where score is 1.0 for exact matches
    """
    # Normalize the title for comparison
    normalized_title = title.lower().strip()

    # Check for exact matches in model names and alternatives
    for canonical, alternatives in models.items():
        # Check the canonical name itself
        if canonical.lower() == normalized_title:
            return canonical, 1.0, f"exact: matched canonical name '{canonical}'"

        # Check alternative names
        for alt in alternatives:
            if alt.lower() == normalized_title:
                return canonical, 1.0, f"exact: matched alternative '{alt}'"

            # Only consider it an exact match if the alternative is the entire title
            # or if it's a standalone word in the title (not part of another word)
            if normalized_title == alt.lower():
                return canonical, 1.0, f"exact: matched alternative '{alt}'"

    return None, 0.0, None


def regex_match(title: str, patterns: Dict[str, str]) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Attempt to match the title using regex patterns.

    Args:
        title: The title string to match
        patterns: Dictionary mapping canonical model names to regex patterns

    Returns:
        A tuple of (canonical_model, score, match_notes) where score is 0.9 for regex matches
    """
    for canonical, pattern in patterns.items():
        match = re.search(pattern, title)
        if match:
            matched_text = match.group(0)
            return canonical, 0.9, f"regex: matched pattern '{canonical}' on text '{matched_text}'"

    return None, 0.0, None


def _calculate_fuzzy_score(text1: str, text2: str) -> float:
    """Calculate the best fuzzy match score between two strings using multiple algorithms."""
    token_score = fuzz.token_set_ratio(text1, text2)
    partial_score = fuzz.partial_ratio(text1, text2)
    return max(token_score, partial_score)


def _try_special_a2000_match(
    normalized_title: str, models: Dict[str, List[str]], threshold: float
) -> Tuple[Optional[str], float, Optional[str]]:
    """Handle special case for A2000 vs A2 confusion."""
    if not ("a2000" in normalized_title or "a 2000" in normalized_title):
        return None, 0.0, None

    for canonical, alternatives in models.items():
        if canonical == "RTX_A2000_12GB":
            # Check canonical name
            score = fuzz.token_set_ratio(canonical.lower(), normalized_title)
            if score >= threshold:
                return canonical, 0.8 * (score / 100.0), f"fuzzy: special A2000 match to canonical '{canonical}' with score {score:.1f}"

            # Check alternatives
            for alt in alternatives:
                score = fuzz.token_set_ratio(alt.lower(), normalized_title)
                if score >= threshold:
                    return canonical, 0.8 * (score / 100.0), f"fuzzy: special A2000 match to alternative '{alt}' with score {score:.1f}"

    return None, 0.0, None


def _find_best_fuzzy_match(normalized_title: str, models: Dict[str, List[str]]) -> Tuple[Optional[str], float, Optional[str]]:
    """Find the best fuzzy match across all models and their alternatives."""
    best_match = None
    best_score = 0.0
    best_matched_string = None

    for canonical, alternatives in models.items():
        # Check canonical name
        score = _calculate_fuzzy_score(canonical.lower(), normalized_title)
        if score > best_score:
            best_match = canonical
            best_score = score
            best_matched_string = canonical

        # Check alternatives
        for alt in alternatives:
            score = _calculate_fuzzy_score(alt.lower(), normalized_title)
            if score > best_score:
                best_match = canonical
                best_score = score
                best_matched_string = alt

    return best_match, best_score, best_matched_string


def fuzzy_match(title: str, models: Dict[str, List[str]], threshold: float = 80.0) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Attempt to match the title using fuzzy string matching.

    Args:
        title: The title string to match
        models: Dictionary mapping canonical model names to lists of alternative names
        threshold: Minimum similarity score (0-100) to consider a match

    Returns:
        A tuple of (canonical_model, score, match_notes) where score is normalized to 0.0-0.8 range
    """
    normalized_title = title.lower().strip()

    # Try special A2000 case first
    special_match, special_score, special_notes = _try_special_a2000_match(normalized_title, models, threshold)
    if special_match:
        return special_match, special_score, special_notes

    # Find best general fuzzy match
    best_match, best_score, best_matched_string = _find_best_fuzzy_match(normalized_title, models)

    # Return match only if above threshold
    if best_score >= threshold:
        normalized_score = 0.8 * (best_score / 100.0)
        match_notes = f"fuzzy: matched '{best_matched_string}' with score {best_score:.1f}"
        return best_match, normalized_score, match_notes

    return None, 0.0, None


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
        # NVLINK accessories and connectors
        "nvlink": "NVLINK bridge/connector accessory",
        "brg": "bridge accessory",
        "scb": "connector/bridge accessory",
        # Gaming/capture devices
        "gamer": "gaming/capture device",
        "live gamer": "capture device",
        "encoder": "video encoder device",
        "jpeg 2000": "video encoder device",
        # Sync devices
        "sync": "synchronization device",
        "quadro sync": "GPU synchronization accessory",
        # AMX and professional AV equipment
        "amx": "AMX professional AV equipment",
        "nmx": "AMX network media extension equipment",
        "harman pro": "professional audio/video equipment",
        # Black Box and video capture devices
        "black box": "Black Box video capture/transmission device",
        "acs": "video capture device",
        "video capturing": "video capture device",
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


def _detect_intel_gpu(title: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if an item is an Intel GPU that should not be fuzzy matched to NVIDIA models.

    Args:
        title: The title string to analyze

    Returns:
        A tuple of (is_intel_gpu, reason) where is_intel_gpu is True if the item is an Intel GPU
    """
    title_lower = title.lower()
    
    # Intel GPU indicators
    intel_indicators = ["intel"]
    
    # Check if this contains Intel GPU indicators
    if any(indicator in title_lower for indicator in intel_indicators):
        # Intel GPU patterns - expanded to include more models
        gpu_patterns = [
            "arc", "xe", "iris", "uhd", "hd graphics",  # Intel GPU families
            "a310", "a380", "a750", "a770",  # Arc discrete models
            "flex", "data center gpu",  # Data center GPUs
            "max", "ponte vecchio",  # High-end compute GPUs
        ]
        if any(pattern in title_lower for pattern in gpu_patterns):
            return True, "Intel GPU - should not match NVIDIA models"
        
        # Also check for Intel GPU naming patterns
        intel_patterns = [
            r"intel.*gpu",  # "Intel Data Center GPU", "Intel GPU", etc.
            r"intel.*graphics",  # "Intel Graphics", etc.
        ]
        for pattern in intel_patterns:
            if re.search(pattern, title_lower):
                return True, "Intel GPU - should not match NVIDIA models"
    
    # Check for standalone Arc branding (without Intel keyword) - enhanced patterns
    if "arc" in title_lower:
        arc_patterns = ["a310", "a380", "a750", "a770", "a580", "a350"]  # Extended Arc models
        if any(pattern in title_lower for pattern in arc_patterns):
            return True, "Intel GPU - should not match NVIDIA models"
    
    # Check for ASRock Intel Arc pattern specifically (high-volume issue)
    if "asrock" in title_lower and "arc" in title_lower:
        return True, "Intel GPU - should not match NVIDIA models"
    
    return False, None


def _detect_amd_gpu(title: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if an item is an AMD GPU that should not be fuzzy matched to NVIDIA models.

    Args:
        title: The title string to analyze

    Returns:
        A tuple of (is_amd_gpu, reason) where is_amd_gpu is True if the item is an AMD GPU
    """
    title_lower = title.lower()
    
    # AMD GPU indicators - check for explicit AMD branding first
    amd_indicators = ["amd", "radeon", "ati"]
    has_amd_branding = any(indicator in title_lower for indicator in amd_indicators)
    
    # AMD GPU model patterns that are distinctive enough to identify without branding
    distinctive_amd_patterns = [
        r"rx\s*\d{4}",  # RX followed by 4 digits (RX 7600, RX 6800, etc.)
        r"rx\s*\d{4}\s*xt",  # RX with XT suffix (RX 7600 XT, RX 6700 XT, etc.)
        r"rx\s*\d{4}\s*gre",  # RX with GRE suffix
        r"rx\s*\d{4}\s*pro",  # RX with Pro suffix
        r"r[579]\s*\d{3}",  # R5/R7/R9 followed by 3 digits
        r"vega\s*\d+",  # Vega series
        r"pro\s*w\d+",  # Pro W series
        r"rx\s*9\d{3}",  # RX 9000 series (RX 9070, etc.)
    ]
    
    # Check distinctive patterns first (these are clearly AMD even without branding)
    for pattern in distinctive_amd_patterns:
        if re.search(pattern, title_lower):
            return True, "AMD GPU - should not match NVIDIA models"
    
    # Check for specific high-volume problematic models
    high_volume_amd_models = [
        "rx 7600 xt", "rx 6700 xt", "rx 6600 xt", "rx 7600", 
        "rx 7700 xt", "rx 7800 xt", "rx 9070", "rx 6300"
    ]
    
    for model in high_volume_amd_models:
        if model in title_lower:
            return True, "AMD GPU - should not match NVIDIA models"
    
    # If we have AMD branding, check for additional GPU patterns
    if has_amd_branding:
        gpu_patterns = ["rx", "r9", "r7", "r5", "vega", "navi", "rdna", "pro w", "wx", "firepro"]
        if any(pattern in title_lower for pattern in gpu_patterns):
            return True, "AMD GPU - should not match NVIDIA models"
    
    return False, None


def normalize_gpu_model(title: str, models_file: Optional[str] = None, fuzzy_threshold: float = 80.0) -> Tuple[str, str, float, bool, Optional[str], Optional[str]]:
    """
    Normalize a GPU model name from a title string.

    Args:
        title: The title string to normalize
        models_file: Optional path to a JSON file containing GPU model definitions
        fuzzy_threshold: Minimum similarity score (0-100) for fuzzy matching

    Returns:
        A tuple of (canonical_model, match_type, match_score, is_valid_gpu, unknown_reason, match_notes)
    """
    # Check if this is clearly not a GPU item
    is_non_gpu, non_gpu_reason = _detect_non_gpu_item(title)
    if is_non_gpu:
        return "UNKNOWN", "none", 0.0, False, non_gpu_reason, None

    # Check if this is an Intel GPU that shouldn't be fuzzy matched to NVIDIA models
    is_intel_gpu, intel_reason = _detect_intel_gpu(title)
    if is_intel_gpu:
        return "UNKNOWN", "none", 0.0, True, intel_reason, None

    # Check if this is an AMD GPU that shouldn't be fuzzy matched to NVIDIA models
    is_amd_gpu, amd_reason = _detect_amd_gpu(title)
    if is_amd_gpu:
        return "UNKNOWN", "none", 0.0, True, amd_reason, None

    # Load models
    models = load_gpu_models(models_file)

    # Try exact match first
    model, score, match_notes = exact_match(title, models)
    if model:
        return model, "exact", score, True, None, match_notes

    # Try regex match next
    model, score, match_notes = regex_match(title, GPU_REGEX_PATTERNS)
    if model:
        return model, "regex", score, True, None, match_notes

    # Try fuzzy match last
    model, score, match_notes = fuzzy_match(title, models, fuzzy_threshold)
    if model:
        return model, "fuzzy", score, True, None, match_notes

    # No match found - assume it's a GPU but we couldn't identify the model
    return "UNKNOWN", "none", 0.0, True, "Could not match to any known GPU model", None


def normalize_csv(input_path: str, output_path: str, models_file: Optional[str] = None, fuzzy_threshold: float = 80.0) -> pd.DataFrame:
    """
    Normalize GPU model names in a CSV file.

    Args:
        input_path: Path to the input CSV file
        output_path: Path to the output CSV file
        models_file: Optional path to a JSON file containing GPU model definitions
        fuzzy_threshold: Minimum similarity score (0-100) for fuzzy matching

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
    df["match_notes"] = None

    # Normalize each title
    for idx, row in df.iterrows():
        model, match_type, score, is_valid_gpu, unknown_reason, match_notes = normalize_gpu_model(row["title"], models_file, fuzzy_threshold)
        df.at[idx, "canonical_model"] = model
        df.at[idx, "match_type"] = match_type
        df.at[idx, "match_score"] = score
        df.at[idx, "is_valid_gpu"] = is_valid_gpu
        df.at[idx, "unknown_reason"] = unknown_reason
        df.at[idx, "match_notes"] = match_notes

    # Write the normalized data to the output file
    df.to_csv(output_path, index=False)

    return df
