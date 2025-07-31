#!/usr/bin/env python3
"""
Create a false positive replay set from the Wamatek dataset.
This script identifies suspicious matches and creates a curated test set for regression testing.
"""

import pandas as pd
import json
from collections import defaultdict

def analyze_false_positives():
    """Analyze the normalized data to identify false positives."""
    
    # Read the normalized data
    df = pd.read_csv('tmp/work/stage_normalized.csv')
    
    print("=== False Positive Analysis ===\n")
    print(f"Total records: {len(df)}")
    
    false_positives = []
    
    # 1. Low fuzzy match scores (likely false positives)
    print("1. Analyzing low fuzzy match scores...")
    low_fuzzy = df[(df['match_type'] == 'fuzzy') & (df['match_score'] < 0.7)]
    print(f"Found {len(low_fuzzy)} fuzzy matches with score < 0.7")
    
    for _, row in low_fuzzy.iterrows():
        false_positives.append({
            'original_title': row['title'],
            'original_model': row['model'],
            'matched_canonical': row['canonical_model'],
            'match_type': row['match_type'],
            'match_score': row['match_score'],
            'issue_type': 'low_fuzzy_score',
            'suggested_action': 'UNKNOWN',
            'reason': f'Fuzzy score {row["match_score"]:.3f} too low for reliable match',
            'source': 'Wamatek'
        })
    
    # 2. Cross-vendor matches (Intel/AMD matched to NVIDIA)
    print("2. Analyzing cross-vendor matches...")
    intel_matches = df[df['title'].str.contains('Intel', case=False, na=False) & 
                      (df['canonical_model'] != 'UNKNOWN')]
    amd_matches = df[df['title'].str.contains('AMD|Radeon', case=False, na=False) & 
                     (df['canonical_model'] != 'UNKNOWN')]
    
    print(f"Found {len(intel_matches)} Intel cards matched to NVIDIA models")
    print(f"Found {len(amd_matches)} AMD cards matched to NVIDIA models")
    
    for _, row in intel_matches.iterrows():
        false_positives.append({
            'original_title': row['title'],
            'original_model': row['model'],
            'matched_canonical': row['canonical_model'],
            'match_type': row['match_type'],
            'match_score': row['match_score'],
            'issue_type': 'cross_vendor_intel',
            'suggested_action': 'UNKNOWN',
            'reason': 'Intel GPU should not match NVIDIA models',
            'source': 'Wamatek'
        })
    
    for _, row in amd_matches.iterrows():
        false_positives.append({
            'original_title': row['title'],
            'original_model': row['model'],
            'matched_canonical': row['canonical_model'],
            'match_type': row['match_type'],
            'match_score': row['match_score'],
            'issue_type': 'cross_vendor_amd',
            'suggested_action': 'UNKNOWN',
            'reason': 'AMD GPU should not match NVIDIA models',
            'source': 'Wamatek'
        })
    
    # 3. Non-GPU items matched as GPUs
    print("3. Analyzing non-GPU items...")
    non_gpu_keywords = ['capture', 'bridge', 'streamer', 'recorder', 'tvbox', 'conferencing']
    for keyword in non_gpu_keywords:
        non_gpu_matches = df[df['title'].str.contains(keyword, case=False, na=False) & 
                            (df['is_valid_gpu'] == True)]
        print(f"Found {len(non_gpu_matches)} '{keyword}' items marked as valid GPUs")
        
        for _, row in non_gpu_matches.iterrows():
            false_positives.append({
                'original_title': row['title'],
                'original_model': row['model'],
                'matched_canonical': row['canonical_model'],
                'match_type': row['match_type'],
                'match_score': row['match_score'],
                'issue_type': f'non_gpu_{keyword}',
                'suggested_action': 'INVALID',
                'reason': f'Contains "{keyword}" - likely not a GPU',
                'source': 'Wamatek'
            })
    
    # 4. Suspicious model name patterns
    print("4. Analyzing suspicious model patterns...")
    
    # Very short model names that got matched
    short_models = df[(df['model'].str.len() < 10) & (df['match_type'] != 'none')]
    print(f"Found {len(short_models)} very short model names that got matched")
    
    for _, row in short_models.head(20).iterrows():  # Limit to first 20
        false_positives.append({
            'original_title': row['title'],
            'original_model': row['model'],
            'matched_canonical': row['canonical_model'],
            'match_type': row['match_type'],
            'match_score': row['match_score'],
            'issue_type': 'short_model_name',
            'suggested_action': 'REVIEW',
            'reason': f'Very short model name "{row["model"]}" may be incomplete',
            'source': 'Wamatek'
        })
    
    # 5. Add the resolved Intel Arc A310 case as an example
    print("5. Adding resolved false positive examples...")
    false_positives.append({
        'original_title': 'ASRock Intel Arc A310 Graphic Card - 4 GB GDDR6 - Low-profile',
        'original_model': 'ASRock Intel Arc A310',
        'matched_canonical': 'A100_40GB_PCIE',
        'match_type': 'fuzzy',
        'match_score': 0.6,
        'issue_type': 'resolved_cross_vendor',
        'suggested_action': 'UNKNOWN',
        'reason': 'Intel GPU was incorrectly fuzzy matched to NVIDIA A100 (RESOLVED)',
        'source': 'Wamatek'
    })
    
    print(f"\nTotal false positives identified: {len(false_positives)}")
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_fps = []
    for fp in false_positives:
        if fp['original_title'] not in seen_titles:
            seen_titles.add(fp['original_title'])
            unique_fps.append(fp)
    
    print(f"Unique false positives after deduplication: {len(unique_fps)}")
    
    # Limit to ~100 examples, prioritizing different issue types
    issue_type_counts = defaultdict(int)
    final_fps = []
    
    # First pass: include diverse issue types
    for fp in unique_fps:
        if len(final_fps) >= 100:
            break
        if issue_type_counts[fp['issue_type']] < 20:  # Max 20 per issue type
            final_fps.append(fp)
            issue_type_counts[fp['issue_type']] += 1
    
    print(f"Final curated set: {len(final_fps)} false positives")
    print("Issue type distribution:")
    for issue_type, count in issue_type_counts.items():
        print(f"  {issue_type}: {count}")
    
    return final_fps

def create_replay_csv(false_positives):
    """Create the replay CSV file."""
    
    # Convert to DataFrame
    df = pd.DataFrame(false_positives)
    
    # Reorder columns for better readability
    column_order = [
        'original_title', 'original_model', 'matched_canonical', 
        'match_type', 'match_score', 'issue_type', 'suggested_action', 
        'reason', 'source'
    ]
    df = df[column_order]
    
    # Save to CSV
    output_path = 'glyphsieve/replay/fp_set.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nFalse positive replay set saved to: {output_path}")
    print(f"Contains {len(df)} examples for regression testing")
    
    return output_path

if __name__ == "__main__":
    false_positives = analyze_false_positives()
    output_path = create_replay_csv(false_positives)
    
    print(f"\n=== Summary ===")
    print(f"Created false positive replay set at: {output_path}")
    print("This file can be used for:")
    print("- Regression testing of matching improvements")
    print("- ML training data annotation")
    print("- Benchmarking fuzzy/regex scoring performance")