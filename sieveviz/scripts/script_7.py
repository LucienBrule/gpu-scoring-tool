# Create a summary table showing top card for each preset
print("TOP GPU RECOMMENDATIONS BY USE CASE")
print("=" * 80)

summary_table = []
for preset in preset_configs.keys():
    preset_data = detailed_df[detailed_df['Preset_Config'] == preset]
    top_card = preset_data.loc[preset_data['Composite_Score'].idxmax()]
    
    summary_table.append({
        'Use_Case': preset.replace('_', ' ').title(),
        'Top_Recommendation': top_card['Card_Name'],
        'Score': round(top_card['Composite_Score'], 1),
        'Price_USD': f"${int(top_card['Current_Retail_Price_USD']):,}",
        'VRAM_GB': f"{int(top_card['VRAM_GB'])}GB",
        'MIG_Instances': int(top_card['MIG_Support']),
        'TDP_W': f"{int(top_card['TDP_Watts'])}W",
        'Slot_Width': f"{int(top_card['Slot_Width'])} slot"
    })

summary_df = pd.DataFrame(summary_table)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("KEY INSIGHTS FROM THE ANALYSIS")
print("=" * 80)

# Analysis insights
insights = [
    "1. BALANCED CONFIGURATION: RTX PRO 6000 Blackwell dominates with 96GB VRAM and MIG support",
    "2. AI TRAINING: High-VRAM cards (H100, RTX PRO 6000) excel due to memory-intensive workloads",
    "3. BUDGET CONSCIOUS: RTX 5090 offers best performance-per-dollar with 32GB VRAM",
    "4. ENTERPRISE EFFICIENCY: L4 leads with exceptional MIG support and power efficiency",
    "5. COMPACT WORKSTATION: L4 excels with single-slot design and strong efficiency metrics"
]

for insight in insights:
    print(insight)

print("\n" + "=" * 80)
print("SCORING METHODOLOGY SUMMARY")
print("=" * 80)

methodology = """
PRICE EFFICIENCY: CUDA cores per dollar (normalized to 100-point scale)
VRAM CAPACITY: Linear scaling based on memory size (larger is better)
MIG CAPABILITY: Multi-instance GPU support (0-7 instances, scaled to 100)
POWER EFFICIENCY: CUDA cores per watt (higher is better)
FORM FACTOR: Slot width penalty (1-slot=100, 2-slot=67, 3-slot=33)
CONNECTIVITY: NVLink (50 pts) + PCIe generation (up to 50 pts)

COMPOSITE SCORE: Weighted sum of all normalized metrics
"""

print(methodology)

# Create a value analysis table
print("VALUE ANALYSIS: TOP 10 PRICE-PERFORMANCE RATIOS")
print("=" * 60)

# Get balanced config data
balanced_data = detailed_df[detailed_df['Preset_Config'] == 'balanced'].copy()
balanced_data['Score_Per_Dollar'] = balanced_data['Composite_Score'] / balanced_data['Current_Retail_Price_USD'] * 1000

top_value = balanced_data.nlargest(10, 'Score_Per_Dollar')[
    ['Card_Name', 'Composite_Score', 'Current_Retail_Price_USD', 'Score_Per_Dollar']
]

for _, row in top_value.iterrows():
    print(f"{row['Card_Name']:<25} Score: {row['Composite_Score']:5.1f} | "
          f"Price: ${row['Current_Retail_Price_USD']:>6,} | "
          f"Value: {row['Score_Per_Dollar']:5.2f} pts/$k")

print("\n" + "=" * 80)