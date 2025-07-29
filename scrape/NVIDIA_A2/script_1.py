# Add additional data points from the latest search
additional_data = [
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1497,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "Router-Switch (Tesla A2)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "router-switch.com/tesla-a2.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "New Factory Sealed, 3 years warranty, 30/mo sold",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "Refurbished",
        "Price_USD": 1648,
        "Quantity": "2",
        "Min_Order_Qty": 1,
        "Seller": "Bonanza Seller",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "bonanza.com/listings/Nvidia-Tesla-A2-16G-Video-Card/1637846728",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "Seller refurbished, 30-day return, 6% discount w/ $60 spent",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1423,
        "Quantity": "Unknown",
        "Min_Order_Qty": 1,
        "Seller": "youyeetoo",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "youyeetoo.com/products/nvidia-a2-tensor-core-gpu",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Free delivery over $10K, entry-level GPU",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1750,
        "Quantity": "Unknown",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (Tech Trends)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "newegg.com/p/1FT-000P-005Y7",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "PNY NVIDIA TESLA A2, #1 Best Seller",
    },
]

# Load existing data and add new data
import pandas as pd

existing_df = pd.read_csv("nvidia_a2_pricing_data.csv")
new_df = pd.DataFrame(additional_data)

# Combine datasets
combined_df = pd.concat([existing_df, new_df], ignore_index=True)

# Update analysis
print("UPDATED NVIDIA A2 GPU Pricing Analysis:")
print("=" * 50)
print(f"Total listings found: {len(combined_df)}")
print(f"Price range: ${combined_df['Price_USD'].min()} - ${combined_df['Price_USD'].max()}")
print(f"Average price: ${combined_df['Price_USD'].mean():.2f}")
print(f"Median price: ${combined_df['Price_USD'].median():.2f}")
print()

# Exclude extreme outliers for better analysis
reasonable_df = combined_df[combined_df["Price_USD"] < 3000]  # Exclude enterprise pricing
print("ANALYSIS (Excluding Enterprise Outliers >$3000):")
print("=" * 50)
print(f"Listings analyzed: {len(reasonable_df)}")
print(f"Price range: ${reasonable_df['Price_USD'].min()} - ${reasonable_df['Price_USD'].max()}")
print(f"Average price: ${reasonable_df['Price_USD'].mean():.2f}")
print(f"Median price: ${reasonable_df['Price_USD'].median():.2f}")
print()

# Pricing by condition (reasonable prices only)
print("Pricing by Condition (Reasonable Range):")
print("=" * 40)
condition_analysis = reasonable_df.groupby("Condition")["Price_USD"].agg(["count", "min", "max", "mean"]).round(2)
print(condition_analysis)
print()

# Stock status analysis
print("Stock Status Analysis:")
print("=" * 25)
stock_counts = combined_df["Quantity"].value_counts()
print(stock_counts)
print()

# Geographic distribution
print("Geographic Distribution:")
print("=" * 30)
geo_analysis = combined_df.groupby("Geographic_Region")["Price_USD"].agg(["count", "mean"]).round(2)
print(geo_analysis)
print()

# Source type analysis (excluding outliers)
print("Source Type Analysis (Reasonable Prices):")
print("=" * 45)
source_analysis = reasonable_df.groupby("Source_Type")["Price_USD"].agg(["count", "min", "max", "mean"]).round(2)
print(source_analysis)
print()

# Save updated CSV
combined_df.to_csv("nvidia_a2_pricing_comprehensive.csv", index=False)
print("Updated data saved to: nvidia_a2_pricing_comprehensive.csv")

# Generate pricing anomaly flags
print("\nPRICING ANOMALY FLAGS:")
print("=" * 30)
mean_price = reasonable_df["Price_USD"].mean()
for idx, row in combined_df.iterrows():
    price = row["Price_USD"]
    if price > mean_price * 1.5:
        if price > 3000:
            print(f"⚠️  EXTREME PREMIUM: {row['Seller']} - ${price} (Enterprise/OEM pricing likely)")
        else:
            print(f"🔴 HIGH PRICE: {row['Seller']} - ${price} ({((price/mean_price - 1)*100):.0f}% above average)")
    elif price < mean_price * 0.6:
        print(
            f"🟡 LOW PRICE: {row['Seller']} - ${price} ({((1 - price/mean_price)*100):.0f}% below average - {row['Condition']})"
        )

print("\nNO DATA FOUND:")
print("=" * 15)
print("❌ Reddit r/hardwareswap: No specific A2 listings found in recent searches")
print("❌ ServerMonkey: Website requires JavaScript, could not access specific A2 pricing")
print("❌ WiredZone: No specific NVIDIA A2 listings found")
print("❌ Provantage: Only enterprise/OEM listings found (HPE branded)")

print("\nPARTIAL DATA:")
print("=" * 12)
print("🔸 B&H Photo: No direct A2 listings found, but carries professional GPUs")
print("🔸 Amazon: No direct price data found, though marketplace sellers present")
print("🔸 Insight.com: Listings exist but no current pricing displayed")
