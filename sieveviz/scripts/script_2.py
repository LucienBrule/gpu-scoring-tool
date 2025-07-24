# Create different scoring presets for different use cases
preset_configs = {
    'balanced': {
        'price_efficiency': 0.25,
        'vram_capacity': 0.20,
        'mig_capability': 0.15,
        'power_efficiency': 0.15,
        'form_factor': 0.10,
        'connectivity': 0.15
    },
    'ai_training': {
        'price_efficiency': 0.15,
        'vram_capacity': 0.30,
        'mig_capability': 0.25,
        'power_efficiency': 0.10,
        'form_factor': 0.05,
        'connectivity': 0.15
    },
    'budget_conscious': {
        'price_efficiency': 0.40,
        'vram_capacity': 0.15,
        'mig_capability': 0.10,
        'power_efficiency': 0.20,
        'form_factor': 0.10,
        'connectivity': 0.05
    },
    'enterprise_efficiency': {
        'price_efficiency': 0.20,
        'vram_capacity': 0.20,
        'mig_capability': 0.30,
        'power_efficiency': 0.15,
        'form_factor': 0.10,
        'connectivity': 0.05
    },
    'compact_workstation': {
        'price_efficiency': 0.20,
        'vram_capacity': 0.15,
        'mig_capability': 0.10,
        'power_efficiency': 0.25,
        'form_factor': 0.25,
        'connectivity': 0.05
    }
}

# Test different configurations
results_summary = {}

for preset_name, weights in preset_configs.items():
    model = GPUScoringModel(weights)
    top_5 = model.get_top_cards(df, 5)
    results_summary[preset_name] = {
        'weights': weights,
        'top_cards': top_5['Card_Name'].tolist(),
        'scores': top_5['composite_score'].tolist()
    }

# Display results for different presets
print("GPU Recommendations by Use Case")
print("=" * 60)

for preset_name, results in results_summary.items():
    print(f"\n{preset_name.upper().replace('_', ' ')} Configuration:")
    print(f"Top 5 Recommendations:")
    for i, (card, score) in enumerate(zip(results['top_cards'], results['scores']), 1):
        print(f"  {i}. {card} (Score: {score:.1f})")

# Create detailed scoring breakdown for top cards
print("\n" + "="*80)
print("DETAILED SCORING BREAKDOWN - BALANCED CONFIGURATION")
print("="*80)

balanced_model = GPUScoringModel(preset_configs['balanced'])
df_detailed = balanced_model.calculate_scores(df)

# Select top 10 cards for detailed breakdown
top_10_detailed = df_detailed.nlargest(10, 'composite_score')

breakdown_cols = ['Card_Name', 'composite_score', 'price_efficiency_score', 
                 'vram_score', 'mig_score', 'power_efficiency_score', 
                 'form_factor_score', 'connectivity_score']

print(top_10_detailed[breakdown_cols].round(1).to_string(index=False))