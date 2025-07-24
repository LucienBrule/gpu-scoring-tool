import plotly.graph_objects as go
import json
import pandas as pd

# Data from the JSON
data_json = [
  {"Card_Name": "RTX 6000 Ada", "VRAM_GB": 48, "Price_Efficiency_Score": 23.2, "Power_Efficiency_Score": 56.8, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 50.8, "Current_Price": 7200, "TDP": 300},
  {"Card_Name": "RTX 5000 Ada", "VRAM_GB": 32, "Price_Efficiency_Score": 17.7, "Power_Efficiency_Score": 48.0, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 42.3, "Current_Price": 6650, "TDP": 250},
  {"Card_Name": "RTX 4500 Ada", "VRAM_GB": 24, "Price_Efficiency_Score": 30.1, "Power_Efficiency_Score": 34.3, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 39.2, "Current_Price": 2350, "TDP": 210},
  {"Card_Name": "RTX 4000 Ada SFF", "VRAM_GB": 20, "Price_Efficiency_Score": 45.2, "Power_Efficiency_Score": 82.3, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 46.8, "Current_Price": 1250, "TDP": 70},
  {"Card_Name": "RTX A6000", "VRAM_GB": 48, "Price_Efficiency_Score": 20.0, "Power_Efficiency_Score": 33.6, "MIG_Support": 0, "Slot_Width": 2, "Composite_Score": 43.6, "Current_Price": 4950, "TDP": 300},
  {"Card_Name": "RTX A5000", "VRAM_GB": 24, "Price_Efficiency_Score": 31.4, "Power_Efficiency_Score": 33.3, "MIG_Support": 0, "Slot_Width": 2, "Composite_Score": 42.8, "Current_Price": 2400, "TDP": 230},
  {"Card_Name": "RTX A4000", "VRAM_GB": 16, "Price_Efficiency_Score": 56.6, "Power_Efficiency_Score": 41.2, "MIG_Support": 0, "Slot_Width": 1, "Composite_Score": 37.7, "Current_Price": 1000, "TDP": 140},
  {"Card_Name": "L40S", "VRAM_GB": 48, "Price_Efficiency_Score": 11.2, "Power_Efficiency_Score": 48.6, "MIG_Support": 7, "Slot_Width": 2, "Composite_Score": 45.5, "Current_Price": 15000, "TDP": 350},
  {"Card_Name": "L40", "VRAM_GB": 48, "Price_Efficiency_Score": 13.9, "Power_Efficiency_Score": 56.8, "MIG_Support": 7, "Slot_Width": 1, "Composite_Score": 50.8, "Current_Price": 12000, "TDP": 300},
  {"Card_Name": "H100 PCIe 80GB", "VRAM_GB": 80, "Price_Efficiency_Score": 5.2, "Power_Efficiency_Score": 45.3, "MIG_Support": 7, "Slot_Width": 2, "Composite_Score": 53.9, "Current_Price": 30000, "TDP": 350},
  {"Card_Name": "H800 PCIe 80GB", "VRAM_GB": 80, "Price_Efficiency_Score": 4.5, "Power_Efficiency_Score": 39.1, "MIG_Support": 7, "Slot_Width": 2, "Composite_Score": 52.8, "Current_Price": 30000, "TDP": 350},
  {"Card_Name": "A800 40GB", "VRAM_GB": 40, "Price_Efficiency_Score": 4.9, "Power_Efficiency_Score": 33.6, "MIG_Support": 7, "Slot_Width": 2, "Composite_Score": 47.5, "Current_Price": 20000, "TDP": 300},
  {"Card_Name": "A40", "VRAM_GB": 48, "Price_Efficiency_Score": 22.0, "Power_Efficiency_Score": 33.6, "MIG_Support": 7, "Slot_Width": 2, "Composite_Score": 45.9, "Current_Price": 4500, "TDP": 300},
  {"Card_Name": "L4", "VRAM_GB": 24, "Price_Efficiency_Score": 20.2, "Power_Efficiency_Score": 100.0, "MIG_Support": 7, "Slot_Width": 1, "Composite_Score": 53.8, "Current_Price": 3500, "TDP": 72},
  {"Card_Name": "A2", "VRAM_GB": 16, "Price_Efficiency_Score": 11.8, "Power_Efficiency_Score": 56.0, "MIG_Support": 7, "Slot_Width": 1, "Composite_Score": 43.4, "Current_Price": 2800, "TDP": 60},
  {"Card_Name": "RTX 4090", "VRAM_GB": 24, "Price_Efficiency_Score": 91.4, "Power_Efficiency_Score": 34.1, "MIG_Support": 0, "Slot_Width": 3, "Composite_Score": 44.7, "Current_Price": 1650, "TDP": 450},
  {"Card_Name": "RTX 5090", "VRAM_GB": 32, "Price_Efficiency_Score": 100.0, "Power_Efficiency_Score": 35.5, "MIG_Support": 0, "Slot_Width": 2, "Composite_Score": 51.2, "Current_Price": 2000, "TDP": 575},
  {"Card_Name": "RTX PRO 6000 Blackwell", "VRAM_GB": 96, "Price_Efficiency_Score": 21.2, "Power_Efficiency_Score": 48.0, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 62.7, "Current_Price": 8900, "TDP": 400},
  {"Card_Name": "RTX PRO 5000 Blackwell", "VRAM_GB": 48, "Price_Efficiency_Score": 23.6, "Power_Efficiency_Score": 45.0, "MIG_Support": 4, "Slot_Width": 2, "Composite_Score": 45.4, "Current_Price": 6000, "TDP": 320},
  {"Card_Name": "T1000 8GB", "VRAM_GB": 8, "Price_Efficiency_Score": 29.4, "Power_Efficiency_Score": 16.8, "MIG_Support": 0, "Slot_Width": 1, "Composite_Score": 30.1, "Current_Price": 280, "TDP": 50},
  {"Card_Name": "T600", "VRAM_GB": 4, "Price_Efficiency_Score": 39.3, "Power_Efficiency_Score": 15.0, "MIG_Support": 0, "Slot_Width": 1, "Composite_Score": 32.5, "Current_Price": 150, "TDP": 40}
]

# Convert to DataFrame
df = pd.DataFrame(data_json)

# Define color mapping for MIG support
color_map = {0: '#DB4545', 4: '#D2BA4C', 7: '#2E8B57'}  # red, yellow, green

# Define symbol mapping for slot width
symbol_map = {1: 'circle', 2: 'square', 3: 'diamond'}

# Create separate traces for each combination of MIG support and slot width
fig = go.Figure()

# Get unique combinations
mig_levels = df['MIG_Support'].unique()
slot_widths = df['Slot_Width'].unique()

for mig in sorted(mig_levels):
    for slot in sorted(slot_widths):
        subset = df[(df['MIG_Support'] == mig) & (df['Slot_Width'] == slot)]
        if len(subset) > 0:
            # Create hover text with price formatting
            hover_text = []
            for _, row in subset.iterrows():
                price_formatted = f"${row['Current_Price']/1000:.1f}k" if row['Current_Price'] < 1000000 else f"${row['Current_Price']/1000000:.1f}m"
                hover_text.append(
                    f"Card: {row['Card_Name']}<br>" +
                    f"Comp Score: {row['Composite_Score']}<br>" +
                    f"Price: {price_formatted}<br>" +
                    f"TDP: {row['TDP']}W"
                )
            
            # Determine legend group names
            mig_label = f"MIG {mig}"
            slot_label = f"{slot}-slot"
            
            fig.add_trace(go.Scatter3d(
                x=subset['VRAM_GB'],
                y=subset['Price_Efficiency_Score'],
                z=subset['Power_Efficiency_Score'],
                mode='markers',
                marker=dict(
                    color=color_map[mig],
                    symbol=symbol_map[slot],
                    size=8,
                    line=dict(width=1, color='white')
                ),
                name=f"{mig_label}, {slot_label}",
                hovertemplate='%{customdata}<extra></extra>',
                customdata=hover_text
            ))

# Update layout
fig.update_layout(
    title="GPU Analysis: VRAM vs Efficiencies",
    scene=dict(
        xaxis_title="VRAM (GB)",
        yaxis_title="Price Eff",
        zaxis_title="Power Eff",
        camera=dict(
            eye=dict(x=1.2, y=1.2, z=1.2)
        )
    ),
    legend=dict(
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='left',
        x=1.02
    )
)

# Save the chart
fig.write_image("gpu_analysis_3d.png")