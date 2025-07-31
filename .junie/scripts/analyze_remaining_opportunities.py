#!/usr/bin/env python3
"""
Analyze the current pipeline state to identify remaining refinement opportunities.
"""

import pandas as pd
from collections import Counter, defaultdict

def analyze_remaining_opportunities():
    """Analyze the current state and identify refinement opportunities."""
    
    # Read the latest results
    df = pd.read_csv('tmp/work_r2/stage_normalized.csv')
    
    print("=== Current Pipeline State Analysis ===")
    print(f"Total records: {len(df)}")
    
    # Match type distribution
    print(f"\nMatch type distribution:")
    match_counts = df['match_type'].value_counts()
    for match_type, count in match_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {match_type}: {count} ({percentage:.1f}%)")
    
    # Fuzzy match quality analysis
    print(f"\n=== Fuzzy Match Quality Analysis ===")
    fuzzy_df = df[df['match_type'] == 'fuzzy']
    if len(fuzzy_df) > 0:
        print(f"Total fuzzy matches: {len(fuzzy_df)}")
        
        # Score distribution
        low_conf = len(fuzzy_df[fuzzy_df['match_score'] < 0.7])
        med_conf = len(fuzzy_df[(fuzzy_df['match_score'] >= 0.7) & (fuzzy_df['match_score'] < 0.8)])
        high_conf = len(fuzzy_df[fuzzy_df['match_score'] >= 0.8])
        
        print(f"  Low confidence (< 0.7): {low_conf}")
        print(f"  Medium confidence (0.7-0.8): {med_conf}")
        print(f"  High confidence (>= 0.8): {high_conf}")
        
        # Top problematic fuzzy matches
        if low_conf > 0:
            print(f"\nTop low-confidence fuzzy matches:")
            low_fuzzy = fuzzy_df[fuzzy_df['match_score'] < 0.7]
            fuzzy_patterns = Counter(zip(low_fuzzy['model'], low_fuzzy['canonical_model']))
            for (model, canonical), count in fuzzy_patterns.most_common(10):
                avg_score = low_fuzzy[(low_fuzzy['model'] == model) & 
                                    (low_fuzzy['canonical_model'] == canonical)]['match_score'].mean()
                print(f"  {model} -> {canonical}: {count} matches (avg score: {avg_score:.3f})")
    
    # UNKNOWN analysis
    print(f"\n=== UNKNOWN Model Analysis ===")
    unknown_df = df[df['canonical_model'] == 'UNKNOWN']
    valid_unknown = unknown_df[unknown_df['is_valid_gpu'] == True]
    invalid_unknown = unknown_df[unknown_df['is_valid_gpu'] == False]
    
    print(f"Total UNKNOWN: {len(unknown_df)}")
    print(f"  Valid GPUs (missing models): {len(valid_unknown)}")
    print(f"  Invalid items (correctly filtered): {len(invalid_unknown)}")
    
    if len(valid_unknown) > 0:
        print(f"\nTop missing GPU models:")
        model_counts = Counter(valid_unknown['model'])
        for model, count in model_counts.most_common(15):
            print(f"  {model}: {count} occurrences")
    
    # Cross-vendor analysis
    print(f"\n=== Cross-Vendor Analysis ===")
    
    # Check for any remaining AMD/Intel false positives
    amd_fps = df[df['title'].str.contains('AMD|Radeon|RX', case=False, na=False) & 
                 (df['canonical_model'] != 'UNKNOWN')]
    intel_fps = df[df['title'].str.contains('Intel|Arc', case=False, na=False) & 
                   (df['canonical_model'] != 'UNKNOWN')]
    
    print(f"AMD GPUs still matching NVIDIA models: {len(amd_fps)}")
    print(f"Intel GPUs still matching NVIDIA models: {len(intel_fps)}")
    
    # Pattern analysis for potential improvements
    print(f"\n=== Pattern Analysis for Improvements ===")
    
    # Look for specific GPU families that might need attention
    gpu_families = {
        'GTX 10 Series': r'GTX 10[0-9][0-9]',
        'Quadro RTX': r'Quadro RTX',
        'Tesla K/M/P Series': r'Tesla [KMP][0-9]+',
        'Titan Series': r'Titan',
        'RTX A Series': r'RTX A[0-9]+',
        'Professional Cards': r'Quadro|Tesla|RTX A|RTX [0-9]{4}',
    }
    
    for family_name, pattern in gpu_families.items():
        family_matches = df[df['title'].str.contains(pattern, case=False, na=False)]
        if len(family_matches) > 0:
            unknown_in_family = len(family_matches[family_matches['canonical_model'] == 'UNKNOWN'])
            fuzzy_in_family = len(family_matches[family_matches['match_type'] == 'fuzzy'])
            total_in_family = len(family_matches)
            
            if unknown_in_family > 0 or fuzzy_in_family > 10:
                print(f"  {family_name}: {total_in_family} total, {unknown_in_family} UNKNOWN, {fuzzy_in_family} fuzzy")
    
    # Identify specific improvement opportunities
    print(f"\n=== Recommended Improvements ===")
    
    opportunities = []
    
    # 1. High-volume UNKNOWN models
    if len(valid_unknown) > 0:
        top_unknown = Counter(valid_unknown['model']).most_common(5)
        high_volume_unknown = [model for model, count in top_unknown if count >= 5]
        if high_volume_unknown:
            opportunities.append(f"Add missing models: {', '.join(high_volume_unknown[:3])}")
    
    # 2. Low-confidence fuzzy matches
    if low_conf > 50:
        opportunities.append(f"Improve {low_conf} low-confidence fuzzy matches")
    
    # 3. Cross-vendor issues
    if len(amd_fps) > 0 or len(intel_fps) > 0:
        opportunities.append(f"Fix remaining cross-vendor false positives")
    
    # 4. Pattern improvements
    if len(fuzzy_df) > 300:
        opportunities.append("Convert high-volume fuzzy matches to regex patterns")
    
    print("Priority opportunities:")
    for i, opp in enumerate(opportunities, 1):
        print(f"  {i}. {opp}")
    
    return {
        'total_records': len(df),
        'fuzzy_matches': len(fuzzy_df),
        'low_confidence_fuzzy': low_conf,
        'unknown_valid': len(valid_unknown),
        'cross_vendor_fps': len(amd_fps) + len(intel_fps),
        'opportunities': opportunities
    }

if __name__ == "__main__":
    results = analyze_remaining_opportunities()