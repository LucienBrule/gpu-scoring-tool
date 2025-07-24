# Create comprehensive CSV export with all scoring data
# Calculate all preset configurations for export

all_results = {}
detailed_data = []

for preset_name, weights in preset_configs.items():
    model = GPUScoringModel(weights)
    df_scored = model.calculate_scores(df)
    
    # Store results for each preset
    for _, row in df_scored.iterrows():
        detailed_data.append({
            'Preset_Config': preset_name,
            'Card_Name': row['Card_Name'],
            'Current_Retail_Price_USD': row['Current_Retail_Price_USD'],
            'VRAM_GB': row['VRAM_GB'],
            'MIG_Support': row['MIG_Support'],
            'TDP_Watts': row['TDP_Watts'],
            'Slot_Width': row['Slot_Width'],
            'NVLink_Support': row['NVLink_Support'],
            'CUDA_Cores': row['CUDA_Cores'],
            'Generation': row['Generation'],
            'PCIe_Generation': row['PCIe_Generation'],
            'Composite_Score': round(row['composite_score'], 2),
            'Price_Efficiency_Score': round(row['price_efficiency_score'], 2),
            'VRAM_Score': round(row['vram_score'], 2),
            'MIG_Score': round(row['mig_score'], 2),
            'Power_Efficiency_Score': round(row['power_efficiency_score'], 2),
            'Form_Factor_Score': round(row['form_factor_score'], 2),
            'Connectivity_Score': round(row['connectivity_score'], 2),
            'Weight_Price_Efficiency': weights['price_efficiency'],
            'Weight_VRAM_Capacity': weights['vram_capacity'],
            'Weight_MIG_Capability': weights['mig_capability'],
            'Weight_Power_Efficiency': weights['power_efficiency'],
            'Weight_Form_Factor': weights['form_factor'],
            'Weight_Connectivity': weights['connectivity']
        })

# Create comprehensive dataframe
detailed_df = pd.DataFrame(detailed_data)

# Save to CSV
detailed_df.to_csv('nvidia_gpu_comprehensive_scoring.csv', index=False)

print("Comprehensive CSV file created: nvidia_gpu_comprehensive_scoring.csv")
print(f"Total records: {len(detailed_df)}")
print(f"Presets included: {list(preset_configs.keys())}")
print(f"GPUs analyzed: {len(df)} unique cards")

# Show sample of the data
print("\nSample of comprehensive data (first 5 rows, key columns):")
sample_cols = ['Card_Name', 'Preset_Config', 'Composite_Score', 'Current_Retail_Price_USD', 
               'VRAM_GB', 'MIG_Support', 'TDP_Watts']
print(detailed_df[sample_cols].head().to_string(index=False))

# Create a summary table showing top card for each preset
print("\n" + "="*80)
print("TOP RECOMMENDATION FOR EACH USE CASE PRESET")
print("="*80)

summary_table = []
for preset in preset_configs.keys():
    preset_data = detailed_df[detailed_df['Preset_Config'] == preset]
    top_card = preset_data.loc[preset_data['Composite_Score'].idxmax()]
    
    summary_table.append({
        'Use_Case': preset.replace('_', ' ').title(),
        'Top_Recommendation': top_card['Card_Name'],
        'Score': top_card['Composite_Score'],
        'Price_USD': int(top_card['Current_Retail_Price_USD']),
        'VRAM_GB': int(top_card['VRAM_GB']),
        'MIG_Instances': int(top_card['MIG_Support']),
        'TDP_W': int(top_card['TDP_Watts']),
        'Slot_Width': int(top_card['Slot_Width'])
    })

summary_df = pd.DataFrame(summary_table)
print(summary_df.to_string(index=False))