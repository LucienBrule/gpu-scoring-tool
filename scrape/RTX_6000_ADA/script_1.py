import pandas as pd
import numpy as np

# Read the CSV file we just created
df = pd.read_csv('rtx_6000_ada_pricing_analysis.csv')

print("=" * 70)
print("NVIDIA RTX 6000 Ada COMPREHENSIVE PRICING ANALYSIS")
print("=" * 70)
print()

# MSRP Information
msrp = 6800.00
print(f"OFFICIAL MSRP: ${msrp:,.2f}")
print(f"Expected Price Range: ${msrp * 0.9:,.2f} - ${msrp * 1.3:,.2f}")
print()

# Remove extreme outliers for better analysis
df_filtered = df[df['Price_USD'] < 25000]  # Remove Jensen-signed card and extreme outliers
legitimate_prices = df_filtered[df_filtered['Price_USD'] < 15000]

print("MARKET ANALYSIS (Excluding Collectibles):")
print("-" * 45)
print(f"Number of legitimate listings: {len(legitimate_prices)}")
print(f"Price range: ${legitimate_prices['Price_USD'].min():,.2f} - ${legitimate_prices['Price_USD'].max():,.2f}")
print(f"Average price: ${legitimate_prices['Price_USD'].mean():,.2f}")
print(f"Median price: ${legitimate_prices['Price_USD'].median():,.2f}")
print(f"Standard deviation: ${legitimate_prices['Price_USD'].std():,.2f}")
print()

# Geographic analysis
print("GEOGRAPHIC PRICE BREAKDOWN:")
print("-" * 35)
geo_analysis = legitimate_prices.groupby('Geographic_Region')['Price_USD'].agg(['count', 'mean', 'min', 'max'])
for region, stats in geo_analysis.iterrows():
    print(f"{region}:")
    print(f"  Listings: {stats['count']}")
    print(f"  Avg Price: ${stats['mean']:,.2f}")
    print(f"  Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")
    print()

# Source type analysis
print("SOURCE TYPE ANALYSIS:")
print("-" * 25)
source_analysis = legitimate_prices.groupby('Source_Type')['Price_USD'].agg(['count', 'mean'])
for source, stats in source_analysis.iterrows():
    print(f"{source}: {stats['count']} listings, Avg: ${stats['mean']:,.2f}")
print()

# Authentication and warranty signals
print("AUTHENTICATION & WARRANTY SIGNALS:")
print("-" * 40)
auth_signals = {
    'Sealed retail box': ['retail packaging', 'factory sealed', 'new retail box'],
    'OEM/bulk packaging': ['oem packaging', 'bulk'],  
    'Refurbished/tested': ['refurbished', 'tested'],
    'As-is/untested': ['as-is', 'no returns'],
    'Warranty mentioned': ['warranty', 'support']
}

for signal, keywords in auth_signals.items():
    count = 0
    for _, row in df.iterrows():
        bulk_notes = str(row['Bulk_Notes']).lower()
        if any(keyword in bulk_notes for keyword in keywords):
            count += 1
    print(f"{signal}: {count} listings")

print()
print("RECOMMENDATIONS & FLAGS:")
print("-" * 30)

# Best value options
print("💰 BEST VALUE OPTIONS:")
mainstream_prices = legitimate_prices[
    (legitimate_prices['Price_USD'] >= msrp * 0.9) & 
    (legitimate_prices['Price_USD'] <= msrp * 1.2) &
    (legitimate_prices['Source_Type'].isin(['Retail_Major', 'Retail_Specialist']))
]

if len(mainstream_prices) > 0:
    for _, row in mainstream_prices.nsmallest(3, 'Price_USD').iterrows():
        print(f"  ${row['Price_USD']:,.2f} - {row['Seller']} ({row['Source_Type']})")
else:
    print("  Limited mainstream retail availability at MSRP")

print()
print("🚨 CAUTION FLAGS:")
suspicious_low = legitimate_prices[legitimate_prices['Price_USD'] < msrp * 0.7]
for _, row in suspicious_low.iterrows():
    reason = "Significantly below MSRP"
    if 'liquidat' in str(row['Bulk_Notes']).lower():
        reason += " - possible liquidation"
    if 'asia/hk' in str(row['Geographic_Region']).lower():  
        reason += " - international seller"
    print(f"  ${row['Price_USD']:,.2f} at {row['Seller']} - {reason}")

print()
print("📊 MARKET INSIGHTS:")
print("-" * 20)

availability_count = df[df['Quantity'].str.contains('Stock|Available', case=False, na=False)].shape[0]
total_listings = len(df)
print(f"• Stock availability: {availability_count}/{total_listings} listings show available inventory")

retail_avg = legitimate_prices[legitimate_prices['Source_Type'].str.contains('Retail', case=False)]['Price_USD'].mean()
resale_avg = legitimate_prices[legitimate_prices['Source_Type'].str.contains('Resale', case=False)]['Price_USD'].mean()

if not np.isnan(retail_avg) and not np.isnan(resale_avg):
    print(f"• Retail vs Resale: Retail avg ${retail_avg:,.2f}, Resale avg ${resale_avg:,.2f}")

us_listings = legitimate_prices[legitimate_prices['Geographic_Region'] == 'US Domestic']
intl_listings = legitimate_prices[legitimate_prices['Geographic_Region'] != 'US Domestic']

if len(us_listings) > 0 and len(intl_listings) > 0:
    us_avg = us_listings['Price_USD'].mean()
    intl_avg = intl_listings['Price_USD'].mean()
    print(f"• US vs International: US avg ${us_avg:,.2f}, International avg ${intl_avg:,.2f}")

print()
print("⚠️  DATA QUALITY NOTES:")
print("-" * 25)
print("• Official MSRP: $6,800 (NVIDIA, confirmed by multiple sources)")
print("• Expected range validated against Tom's Hardware, Puget Systems")
print(f"• {len(df)} total sources searched across retail, resale, and enterprise")
print("• Prices reflect July 2025 market conditions")
print("• Some international prices may include VAT/duties")

print()
print("🎯 PROCUREMENT RECOMMENDATIONS:")
print("-" * 35)
print("1. Target price range: $6,800 - $7,500 for legitimate new units")
print("2. Verify seller reputation for international sources")
print("3. Consider Dell pre-built option at $6,305 + system cost")
print("4. Avoid pricing significantly below $5,000 without verification")
print("5. Factor in shipping, duties, and warranty coverage")

print("\n" + "=" * 70)