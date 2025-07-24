# Fix the issue by ensuring all columns are preserved in the scoring model
class GPUScoringModelFixed:
    def __init__(self, weights=None):
        # Default weights - can be adjusted by user
        self.default_weights = {
            'price_efficiency': 0.25,      # Higher is better (performance per dollar)
            'vram_capacity': 0.20,         # More VRAM is better
            'mig_capability': 0.15,        # MIG instances (higher is better)
            'power_efficiency': 0.15,      # Lower TDP relative to performance is better
            'form_factor': 0.10,           # Smaller slot width is better
            'connectivity': 0.15           # NVLink + PCIe gen (higher is better)
        }
        
        self.weights = weights if weights else self.default_weights
        
    def normalize_metrics(self, df):
        """Normalize all metrics to 0-100 scale"""
        df_norm = df.copy()  # This preserves all original columns
        
        # Price efficiency: CUDA cores per dollar (higher is better)
        df_norm['price_efficiency_score'] = (df['CUDA_Cores'] / df['Current_Retail_Price_USD']) * 1000
        df_norm['price_efficiency_score'] = (df_norm['price_efficiency_score'] / df_norm['price_efficiency_score'].max()) * 100
        
        # VRAM capacity score (linear scaling)
        df_norm['vram_score'] = (df['VRAM_GB'] / df['VRAM_GB'].max()) * 100
        
        # MIG capability score
        df_norm['mig_score'] = (df['MIG_Support'] / 7) * 100  # Max 7 instances
        
        # Power efficiency: Performance per watt (CUDA cores per watt)
        df_norm['power_efficiency_score'] = df['CUDA_Cores'] / df['TDP_Watts']
        df_norm['power_efficiency_score'] = (df_norm['power_efficiency_score'] / df_norm['power_efficiency_score'].max()) * 100
        
        # Form factor score (smaller is better, so invert)
        df_norm['form_factor_score'] = (4 - df['Slot_Width']) / 3 * 100  # 1-slot = 100, 2-slot = 67, 3-slot = 33
        
        # Connectivity score (NVLink + PCIe generation)
        nvlink_score = df['NVLink_Support'] * 50  # NVLink adds 50 points
        pcie_score = (df['PCIe_Generation'] - 3) / 2 * 50  # PCIe 3.0 = 0, 4.0 = 25, 5.0 = 50
        df_norm['connectivity_score'] = nvlink_score + pcie_score
        
        return df_norm
    
    def calculate_scores(self, df):
        """Calculate weighted composite scores"""
        df_scored = self.normalize_metrics(df)
        
        # Calculate composite score
        df_scored['composite_score'] = (
            df_scored['price_efficiency_score'] * self.weights['price_efficiency'] +
            df_scored['vram_score'] * self.weights['vram_capacity'] +
            df_scored['mig_score'] * self.weights['mig_capability'] +
            df_scored['power_efficiency_score'] * self.weights['power_efficiency'] +
            df_scored['form_factor_score'] * self.weights['form_factor'] +
            df_scored['connectivity_score'] * self.weights['connectivity']
        )
        
        return df_scored

# Now create comprehensive CSV export with all scoring data
all_results = {}
detailed_data = []

for preset_name, weights in preset_configs.items():
    model = GPUScoringModelFixed(weights)
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
print("\nSample of comprehensive data (first 3 rows, key columns):")
sample_cols = ['Card_Name', 'Preset_Config', 'Composite_Score', 'Current_Retail_Price_USD', 
               'VRAM_GB', 'MIG_Support', 'TDP_Watts']
print(detailed_df[sample_cols].head(3).to_string(index=False))

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