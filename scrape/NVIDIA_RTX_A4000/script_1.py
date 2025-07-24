# Analysis of pricing anomalies and stock status
import pandas as pd

df = pd.read_csv('rtx_a4000_pricing_data.csv')

print("NVIDIA RTX A4000 PRICING ANALYSIS")
print("=" * 50)

# Historical context - MSRP was around $1,000 based on the search results
estimated_msrp = 1000
print(f"Estimated MSRP: ${estimated_msrp}")
print(f"Current market range: ${df[df['Price_USD'] > 0]['Price_USD'].min():.2f} - ${df['Price_USD'].max():.2f}")

print("\nPRICING ANOMALY FLAGS:")
print("-" * 30)

# Flag unusually low prices
low_threshold = estimated_msrp * 0.6  # 40% below MSRP
high_threshold = estimated_msrp * 1.4  # 40% above MSRP

low_price_flags = df[(df['Price_USD'] > 0) & (df['Price_USD'] < low_threshold)]
high_price_flags = df[(df['Price_USD'] > 0) & (df['Price_USD'] > high_threshold)]

print(f"\nUnusually LOW prices (< ${low_threshold:.0f}):")
for _, row in low_price_flags.iterrows():
    print(f"  • ${row['Price_USD']:.2f} - {row['Seller']} ({row['Condition']}) - {row['Geographic_Region']}")
    if row['Price_USD'] < 500:
        print(f"    ⚠️  WARNING: Price 50%+ below typical - may be liquidation/bulk/damaged")

print(f"\nUnusually HIGH prices (> ${high_threshold:.0f}):")
for _, row in high_price_flags.iterrows():
    print(f"  • ${row['Price_USD']:.2f} - {row['Seller']} ({row['Condition']}) - {row['Geographic_Region']}")
    if row['Price_USD'] > 1300:
        print(f"    ⚠️  WARNING: Price 30%+ above typical - may include premium warranty/service")

print("\nSTOCK STATUS SUMMARY:")
print("-" * 25)

# Count stock availability
out_of_stock = df[df['Condition'] == 'out of stock'].shape[0]
available_listings = df[df['Price_USD'] > 0].shape[0]
total_listings = df.shape[0]

print(f"Available listings: {available_listings}")
print(f"Out of stock: {out_of_stock}")
print(f"Total searched: {total_listings}")

# Geographic distribution
print("\nGEOGRAPHIC DISTRIBUTION:")
print("-" * 28)
geo_dist = df[df['Price_USD'] > 0].groupby('Geographic_Region').agg({
    'Price_USD': ['count', 'mean', 'min', 'max']
}).round(2)
geo_dist.columns = ['Count', 'Avg_Price', 'Min_Price', 'Max_Price']
print(geo_dist)

print("\nCONDITION ANALYSIS:")
print("-" * 20)
for condition in df['Condition'].unique():
    if condition != 'out of stock':
        cond_data = df[df['Condition'] == condition]
        avg_price = cond_data['Price_USD'].mean()
        count = len(cond_data)
        print(f"{condition.title()}: {count} listings, avg ${avg_price:.2f}")

print("\nAUTHENTICITY SIGNALS:")
print("-" * 22)
# Based on source analysis
retail_sources = df[df['Source_Type'].isin(['Retail_Major', 'Retail_Specialist'])]
business_resale = df[df['Source_Type'] == 'Resale_Business']
individual_resale = df[df['Source_Type'] == 'Resale_Individual']

print(f"Retail/Authorized: {len(retail_sources)} listings - Highest authenticity confidence")
print(f"Business Resellers: {len(business_resale)} listings - Good authenticity confidence")
print(f"Individual Sellers: {len(individual_resale)} listings - Verify authenticity")
print(f"International: {len(df[df['Source_Type'] == 'International'])} listings - Verify import compliance")

print(f"\nRecommended price range for procurement: ${low_price_flags['Price_USD'].max():.2f} - ${df[df['Condition'] == 'new']['Price_USD'].quantile(0.75):.2f}")