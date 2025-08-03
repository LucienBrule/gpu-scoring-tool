#!/usr/bin/env python3
"""
Analyze the normalized Wamatek dataset to identify missing GPU models in the registry.
This script will help identify which GPU models need to be added to gpu_specs.yaml.
"""

from collections import Counter, defaultdict

import pandas as pd


def analyze_missing_gpus():
    """Analyze the normalized data to find missing GPU models."""

    # Read the normalized data
    df = pd.read_csv("tmp/work/stage_normalized.csv")

    print("=== GPU Registry Analysis ===\n")
    print(f"Total records: {len(df)}")
    print(f"Valid GPU records: {len(df[df['is_valid_gpu'] == True])}")
    print(f"Invalid GPU records: {len(df[df['is_valid_gpu'] == False])}")

    # Analyze UNKNOWN canonical models (potential missing models)
    unknown_models = df[df["canonical_model"] == "UNKNOWN"]
    print(f"\nUNKNOWN canonical models: {len(unknown_models)}")

    # Group by model name for UNKNOWN entries that are valid GPUs
    unknown_valid_gpus = unknown_models[unknown_models["is_valid_gpu"] == True]
    print(f"UNKNOWN but valid GPUs: {len(unknown_valid_gpus)}")

    if len(unknown_valid_gpus) > 0:
        print("\nTop UNKNOWN valid GPU models:")
        model_counts = Counter(unknown_valid_gpus["model"])
        for model, count in model_counts.most_common(20):
            print(f"  {model}: {count} occurrences")

    # Analyze fuzzy matches that might be incorrect
    print("\n=== Fuzzy Match Analysis ===")
    fuzzy_matches = df[df["match_type"] == "fuzzy"]
    print(f"Total fuzzy matches: {len(fuzzy_matches)}")

    # Group fuzzy matches by model -> canonical_model mapping
    fuzzy_mapping = defaultdict(list)
    for _, row in fuzzy_matches.iterrows():
        fuzzy_mapping[row["model"]].append((row["canonical_model"], row["match_score"]))

    print("\nPotentially incorrect fuzzy matches (low scores or suspicious mappings):")
    for model, mappings in fuzzy_mapping.items():
        # Get unique mappings
        unique_mappings = list(set(mappings))
        if len(unique_mappings) > 1 or any(score < 0.7 for _, score in unique_mappings):
            print(f"  {model}:")
            for canonical, score in unique_mappings:
                print(f"    -> {canonical} (score: {score:.3f})")

    # Look for specific patterns mentioned in the task
    print("\n=== Specific Model Analysis ===")

    # RTX 5000 series consumer cards
    rtx_5000_series = df[df["model"].str.contains(r"RTX 50[0-9][0-9]", case=False, na=False)]
    if len(rtx_5000_series) > 0:
        print(f"\nRTX 5000 series consumer cards: {len(rtx_5000_series)}")
        rtx_5000_mappings = Counter(zip(rtx_5000_series["model"], rtx_5000_series["canonical_model"]))
        for (model, canonical), count in rtx_5000_mappings.most_common(10):
            print(f"  {model} -> {canonical}: {count}")

    # RTX 4000 series consumer cards
    rtx_4000_series = df[df["model"].str.contains(r"RTX 40[0-9][0-9]", case=False, na=False)]
    if len(rtx_4000_series) > 0:
        print(f"\nRTX 4000 series consumer cards: {len(rtx_4000_series)}")
        rtx_4000_mappings = Counter(zip(rtx_4000_series["model"], rtx_4000_series["canonical_model"]))
        for (model, canonical), count in rtx_4000_mappings.most_common(10):
            print(f"  {model} -> {canonical}: {count}")

    # RTX 3000 series consumer cards
    rtx_3000_series = df[df["model"].str.contains(r"RTX 30[0-9][0-9]", case=False, na=False)]
    if len(rtx_3000_series) > 0:
        print(f"\nRTX 3000 series consumer cards: {len(rtx_3000_series)}")
        rtx_3000_mappings = Counter(zip(rtx_3000_series["model"], rtx_3000_series["canonical_model"]))
        for (model, canonical), count in rtx_3000_mappings.most_common(10):
            print(f"  {model} -> {canonical}: {count}")

    # A-series cards (A100, A10, etc.)
    a_series = df[df["model"].str.contains(r"\bA[0-9]+", case=False, na=False)]
    if len(a_series) > 0:
        print(f"\nA-series cards: {len(a_series)}")
        a_series_mappings = Counter(zip(a_series["model"], a_series["canonical_model"]))
        for (model, canonical), count in a_series_mappings.most_common(10):
            print(f"  {model} -> {canonical}: {count}")

    # T-series cards (T400, etc.)
    t_series = df[df["model"].str.contains(r"\bT[0-9]+", case=False, na=False)]
    if len(t_series) > 0:
        print(f"\nT-series cards: {len(t_series)}")
        t_series_mappings = Counter(zip(t_series["model"], t_series["canonical_model"]))
        for (model, canonical), count in t_series_mappings.most_common(10):
            print(f"  {model} -> {canonical}: {count}")

    # Look for specific models mentioned in the task
    print("\n=== Task-Specific Model Search ===")

    # Search for A100_40GB_PCIE pattern
    a100_40gb = df[df["title"].str.contains(r"A100.*40GB", case=False, na=False)]
    if len(a100_40gb) > 0:
        print(f"\nA100 40GB cards found: {len(a100_40gb)}")
        for _, row in a100_40gb.head(5).iterrows():
            print(f"  {row['title']} -> {row['canonical_model']}")

    # Search for RTX 4000 SFF Ada pattern
    rtx_4000_sff = df[df["title"].str.contains(r"RTX.*4000.*SFF", case=False, na=False)]
    if len(rtx_4000_sff) > 0:
        print(f"\nRTX 4000 SFF cards found: {len(rtx_4000_sff)}")
        for _, row in rtx_4000_sff.head(5).iterrows():
            print(f"  {row['title']} -> {row['canonical_model']}")

    # Search for RTX 5000 Ada pattern
    rtx_5000_ada = df[df["title"].str.contains(r"RTX.*5000.*Ada", case=False, na=False)]
    if len(rtx_5000_ada) > 0:
        print(f"\nRTX 5000 Ada cards found: {len(rtx_5000_ada)}")
        for _, row in rtx_5000_ada.head(5).iterrows():
            print(f"  {row['title']} -> {row['canonical_model']}")

    print("\n=== Summary ===")
    print("Models that likely need to be added to the registry:")

    # Collect all models that are UNKNOWN but valid GPUs
    missing_models = set()
    for model in unknown_valid_gpus["model"].unique():
        if not any(exclude in model.lower() for exclude in ["capture", "bridge", "streamer", "tvbox"]):
            missing_models.add(model)

    # Add models with suspicious fuzzy matches
    for model, mappings in fuzzy_mapping.items():
        unique_mappings = list(set(mappings))
        if any(score < 0.7 for _, score in unique_mappings):
            missing_models.add(model)

    print(f"\nTotal unique models to investigate: {len(missing_models)}")
    for model in sorted(missing_models):
        print(f"  - {model}")


if __name__ == "__main__":
    analyze_missing_gpus()
