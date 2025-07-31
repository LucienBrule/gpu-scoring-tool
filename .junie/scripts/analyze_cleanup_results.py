#!/usr/bin/env python3
"""
Analyze the results of the cleanup task to see how flagged items are now being handled.
"""

import pandas as pd

def analyze_cleanup_results():
    """Analyze the cleanup results."""
    
    # Read the new results
    df = pd.read_csv('tmp/work_cleanup/stage_normalized.csv')
    
    # Check specific flagged items
    flagged_items = [
        ('RX 7600 XT', 'AMD GPU false positive'),
        ('Intel Data Center GPU Flex 140', 'Intel GPU false positive'),
        ('NVIDIA NVLINK A SERIES 3S SCB', 'NVLINK accessory'),
        ('LIVE GAMER ULTRA 2.1 GC553G2', 'Capture device'),
        ('RTX PRO 6000', 'RTX PRO 6000 mismatching'),
        ('RTX A400', 'RTX A400 mismatching'),
        ('Tesla T4', 'Tesla T4 mismatching'),
        ('Quadro Sync', 'Sync device')
    ]
    
    print('=== Analysis of Previously Flagged Items ===\n')
    
    for search_term, issue_type in flagged_items:
        matches = df[df['title'].str.contains(search_term, case=False, na=False)]
        if len(matches) > 0:
            row = matches.iloc[0]
            print(f'Issue: {issue_type}')
            print(f'  Title: {row["title"]}')
            print(f'  Model: {row["model"]}')
            print(f'  Canonical: {row["canonical_model"]}')
            print(f'  Match Type: {row["match_type"]}')
            print(f'  Match Score: {row["match_score"]}')
            print(f'  Valid GPU: {row["is_valid_gpu"]}')
            if pd.notna(row['unknown_reason']):
                print(f'  Reason: {row["unknown_reason"]}')
            if pd.notna(row['match_notes']):
                print(f'  Notes: {row["match_notes"]}')
            print()
        else:
            print(f'Issue: {issue_type} - NO MATCHES FOUND')
            print()
    
    # Overall statistics
    print('=== Overall Pipeline Statistics ===')
    print(f'Total records: {len(df)}')
    print(f'\nMatch type distribution:')
    for match_type, count in df['match_type'].value_counts().items():
        print(f'  {match_type}: {count}')
    
    print(f'\nValid GPU distribution:')
    for valid, count in df['is_valid_gpu'].value_counts().items():
        print(f'  {valid}: {count}')
    
    # Check for remaining issues
    print('\n=== Remaining Issues Analysis ===')
    
    # Low confidence fuzzy matches
    low_fuzzy = df[(df['match_type'] == 'fuzzy') & (df['match_score'] < 0.7)]
    print(f'Low confidence fuzzy matches (< 0.7): {len(low_fuzzy)}')
    
    # AMD/Intel still matching NVIDIA
    amd_matches = df[df['title'].str.contains('AMD|Radeon|RX', case=False, na=False) & 
                     (df['canonical_model'] != 'UNKNOWN')]
    intel_matches = df[df['title'].str.contains('Intel', case=False, na=False) & 
                       (df['canonical_model'] != 'UNKNOWN')]
    
    print(f'AMD GPUs still matching NVIDIA models: {len(amd_matches)}')
    print(f'Intel GPUs still matching NVIDIA models: {len(intel_matches)}')
    
    if len(amd_matches) > 0:
        print('Sample AMD false positives:')
        for _, row in amd_matches.head(3).iterrows():
            print(f'  {row["model"]} -> {row["canonical_model"]}')
    
    if len(intel_matches) > 0:
        print('Sample Intel false positives:')
        for _, row in intel_matches.head(3).iterrows():
            print(f'  {row["model"]} -> {row["canonical_model"]}')

if __name__ == "__main__":
    analyze_cleanup_results()