# Create a tunable scoring model for NVIDIA GPUs
class GPUScoringModel:
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
        df_norm = df.copy()
        
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
    
    def get_top_cards(self, df, n=10):
        """Get top N cards by composite score"""
        df_scored = self.calculate_scores(df)
        return df_scored.nlargest(n, 'composite_score')[
            ['Card_Name', 'composite_score', 'Current_Retail_Price_USD', 'VRAM_GB', 
             'MIG_Support', 'TDP_Watts', 'Slot_Width', 'NVLink_Support']
        ]

# Initialize the model with default weights
scoring_model = GPUScoringModel()

# Calculate scores for all GPUs
df_with_scores = scoring_model.calculate_scores(df)

print("GPU Scoring Model Results (Default Weights)")
print("=" * 60)
print(f"Weight Configuration:")
for key, value in scoring_model.weights.items():
    print(f"  {key}: {value:.2f}")
print()

# Show top 15 cards
top_cards = scoring_model.get_top_cards(df, 15)
print("Top 15 Cards by Composite Score:")
print(top_cards.round(2))