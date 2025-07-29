import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Load the data
data = [
    {
        "Card_Name": "RTX 6000 Ada",
        "Price_Efficiency_Score": 23.2,
        "Composite_Score": 50.8,
        "VRAM_GB": 48,
        "Generation": "Ada",
        "Current_Price": 7200,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "RTX 5000 Ada",
        "Price_Efficiency_Score": 17.7,
        "Composite_Score": 42.3,
        "VRAM_GB": 32,
        "Generation": "Ada",
        "Current_Price": 6650,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "RTX 4500 Ada",
        "Price_Efficiency_Score": 30.1,
        "Composite_Score": 39.2,
        "VRAM_GB": 24,
        "Generation": "Ada",
        "Current_Price": 2350,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "RTX 4000 Ada SFF",
        "Price_Efficiency_Score": 45.2,
        "Composite_Score": 46.8,
        "VRAM_GB": 20,
        "Generation": "Ada",
        "Current_Price": 1250,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "RTX A6000",
        "Price_Efficiency_Score": 20.0,
        "Composite_Score": 43.6,
        "VRAM_GB": 48,
        "Generation": "Ampere",
        "Current_Price": 4950,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "RTX A5000",
        "Price_Efficiency_Score": 31.4,
        "Composite_Score": 42.8,
        "VRAM_GB": 24,
        "Generation": "Ampere",
        "Current_Price": 2400,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "RTX A4000",
        "Price_Efficiency_Score": 56.6,
        "Composite_Score": 37.7,
        "VRAM_GB": 16,
        "Generation": "Ampere",
        "Current_Price": 1000,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "L40S",
        "Price_Efficiency_Score": 11.2,
        "Composite_Score": 45.5,
        "VRAM_GB": 48,
        "Generation": "Ada",
        "Current_Price": 15000,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "L40",
        "Price_Efficiency_Score": 13.9,
        "Composite_Score": 50.8,
        "VRAM_GB": 48,
        "Generation": "Ada",
        "Current_Price": 12000,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "H100 PCIe 80GB",
        "Price_Efficiency_Score": 5.2,
        "Composite_Score": 53.9,
        "VRAM_GB": 80,
        "Generation": "Hopper",
        "Current_Price": 30000,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "H800 PCIe 80GB",
        "Price_Efficiency_Score": 4.5,
        "Composite_Score": 52.8,
        "VRAM_GB": 80,
        "Generation": "Hopper",
        "Current_Price": 30000,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "A800 40GB",
        "Price_Efficiency_Score": 4.9,
        "Composite_Score": 47.5,
        "VRAM_GB": 40,
        "Generation": "Ampere",
        "Current_Price": 20000,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "A40",
        "Price_Efficiency_Score": 22.0,
        "Composite_Score": 45.9,
        "VRAM_GB": 48,
        "Generation": "Ampere",
        "Current_Price": 4500,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "L4",
        "Price_Efficiency_Score": 20.2,
        "Composite_Score": 53.8,
        "VRAM_GB": 24,
        "Generation": "Ada",
        "Current_Price": 3500,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "A2",
        "Price_Efficiency_Score": 11.8,
        "Composite_Score": 43.4,
        "VRAM_GB": 16,
        "Generation": "Ampere",
        "Current_Price": 2800,
        "MIG_Support": 7,
    },
    {
        "Card_Name": "RTX 4090",
        "Price_Efficiency_Score": 91.4,
        "Composite_Score": 44.7,
        "VRAM_GB": 24,
        "Generation": "Ada",
        "Current_Price": 1650,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "RTX 5090",
        "Price_Efficiency_Score": 100.0,
        "Composite_Score": 51.2,
        "VRAM_GB": 32,
        "Generation": "Blackwell",
        "Current_Price": 2000,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "RTX PRO 6000 Blackwell",
        "Price_Efficiency_Score": 21.2,
        "Composite_Score": 62.7,
        "VRAM_GB": 96,
        "Generation": "Blackwell",
        "Current_Price": 8900,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "RTX PRO 5000 Blackwell",
        "Price_Efficiency_Score": 23.6,
        "Composite_Score": 45.4,
        "VRAM_GB": 48,
        "Generation": "Blackwell",
        "Current_Price": 6000,
        "MIG_Support": 4,
    },
    {
        "Card_Name": "T1000 8GB",
        "Price_Efficiency_Score": 29.4,
        "Composite_Score": 30.1,
        "VRAM_GB": 8,
        "Generation": "Turing",
        "Current_Price": 280,
        "MIG_Support": 0,
    },
    {
        "Card_Name": "T600",
        "Price_Efficiency_Score": 39.3,
        "Composite_Score": 32.5,
        "VRAM_GB": 4,
        "Generation": "Turing",
        "Current_Price": 150,
        "MIG_Support": 0,
    },
]

df = pd.DataFrame(data)

# Define colors for generations using brand colors
generation_colors = {
    "Ada": "#1FB8CD",
    "Ampere": "#DB4545",
    "Blackwell": "#2E8B57",
    "Hopper": "#5D878F",
    "Turing": "#D2BA4C",
}

# Create the scatter plot
fig = go.Figure()

# Add scatter points for each generation
for gen in df["Generation"].unique():
    gen_data = df[df["Generation"] == gen]

    fig.add_trace(
        go.Scatter(
            x=gen_data["Price_Efficiency_Score"],
            y=gen_data["Composite_Score"],
            mode="markers",
            name=gen,
            marker=dict(
                size=gen_data["VRAM_GB"] * 0.8,  # Scale VRAM to appropriate point size
                color=generation_colors[gen],
                sizemode="diameter",
                line=dict(width=1, color="white"),
            ),
            customdata=np.column_stack(
                (gen_data["Card_Name"], gen_data["Current_Price"], gen_data["VRAM_GB"], gen_data["MIG_Support"])
            ),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            + "Price Eff: %{x}<br>"
            + "Composite: %{y}<br>"
            + "Price: $%{customdata[1]:,}<br>"
            + "VRAM: %{customdata[2]}GB<br>"
            + "MIG Support: %{customdata[3]}<extra></extra>",
            cliponaxis=False,
        )
    )

# Add trend line
X = df["Price_Efficiency_Score"].values.reshape(-1, 1)
y = df["Composite_Score"].values
reg = LinearRegression().fit(X, y)
x_trend = np.linspace(df["Price_Efficiency_Score"].min(), df["Price_Efficiency_Score"].max(), 100)
y_trend = reg.predict(x_trend.reshape(-1, 1))

fig.add_trace(
    go.Scatter(
        x=x_trend,
        y=y_trend,
        mode="lines",
        name="Trend",
        line=dict(color="gray", width=2, dash="dash"),
        showlegend=False,
        hoverinfo="skip",
        cliponaxis=False,
    )
)

# Update layout
fig.update_layout(
    title="GPU Price Eff vs Performance",
    xaxis_title="Price Eff Score",
    yaxis_title="Composite Score",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
)

# Update axes
fig.update_xaxes(range=[0, 105])
fig.update_yaxes(range=[25, 70])

# Save the chart
fig.write_image("gpu_performance_chart.png")
fig.show()
