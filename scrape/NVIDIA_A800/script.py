import pandas as pd
from datetime import datetime, timedelta

# Create pricing data based on research findings
# Note: MSRP is $19,999 based on multiple authoritative sources

pricing_data = []

# Add all the pricing data found from various sources
pricing_data.extend([
    # SHI - Retail Major
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 19999.00,
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'SHI.com',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.shi.com/product/46563369/NVIDIA-A800-40GB-Active',
        'Source_Type': 'Retail_Major',
        'Bulk_Notes': 'MSRP pricing, official distributor',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'Official NVIDIA partner, sealed retail box'
    },
    
    # B&H Photo - Retail Specialist
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 19999.00,
        'Quantity': 'Special Order',
        'Min_Order_Qty': 1,
        'Seller': 'B&H Photo',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.bhphotovideo.com/c/product/1803762-REG/pny_vcna800_pb_a800_40gb_active_graphics.html',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': '4-6 weeks expected availability, cannot cancel/return',
        'Stock_Status': 'Pre-order',
        'Authentication_Signals': 'Authorized dealer, PNY retail packaging'
    },
    
    # Zones.com - Enterprise pricing with NVAIE subscription
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 14124.99,
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'Zones.com',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.zones.com/site/product/index.html?id=114978286',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'Includes 3-year NVIDIA AI Enterprise subscription',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'NVIDIA authorized partner, bulk packaging'
    },
    
    # Zones.com - Alternative listing
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 14117.99,
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'Zones.com',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.zones.com/site/product/index.html?id=301534092NEW',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'Includes 3-year NVIDIA AI Enterprise subscription',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'NVIDIA authorized partner, bulk packaging'
    },
    
    # Zones.com - PNY Black Box version
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 17256.99,
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'Zones.com',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.zones.com/site/product/index.html?id=114101413',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'PNY black box packaging and accessories',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'PNY official packaging, 3-year warranty'
    },
    
    # Central Computer - Out of Stock
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 14399.99,
        'Quantity': 'Out of Stock',
        'Min_Order_Qty': 1,
        'Seller': 'Central Computer',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.centralcomputer.com/pny-nvidia-a800-40gb-active-graphic-card-ecc-pcie-4-0-dual-slot-240w-vcna800-pb.html',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'PNY model VCNA800-PB',
        'Stock_Status': 'Out of Stock',
        'Authentication_Signals': 'Authorized retailer, 3-year warranty'
    },
    
    # HP Connection/GovConnection - Enterprise
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 21475.25,
        'Quantity': 'Out of Stock',
        'Min_Order_Qty': 1,
        'Seller': 'HP Connection',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.connection.com/product/hp-nvidia-a800-pcie-4.0-x16-graphics-card-40gb-hbm2/8d6c0aa/41770375',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'HP branded version (8D6C0AA)',
        'Stock_Status': 'Out of Stock',
        'Authentication_Signals': 'HP official partner, enterprise warranty'
    },
    
    # Provantage - Enterprise Specialist
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 14493.57,
        'Quantity': 'Special Order',
        'Min_Order_Qty': 1,
        'Seller': 'Provantage',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.provantage.com/pny-technologies-vcna800-pb~7PNY92EK.htm',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': '28% discount from MSRP, PNY black box packaging',
        'Stock_Status': 'Special Order',
        'Authentication_Signals': 'NVIDIA authorized dealer, factory new'
    },
    
    # Trade India - International supplier
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 5500.00,
        'Quantity': 'In Stock',
        'Min_Order_Qty': 1,
        'Seller': 'Genius Teknolojl Ticaret Limited Sirketi',
        'Geographic_Region': 'Turkey/International',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.tradeindia.com/products/a800-40gb-active-graphics-card-9243263.html',
        'Source_Type': 'International',
        'Bulk_Notes': 'Supply ability: 3 per day, 10-day delivery, Payment: T/T, PayPal, Western Union',
        'Stock_Status': 'In Stock',
        'Authentication_Signals': 'Requires verification - significantly below market price'
    },
    
    # UK Scan - European Retailer
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 17400.00,  # Approximate USD conversion from £13,799.99
        'Quantity': 'Pre-order',
        'Min_Order_Qty': 1,
        'Seller': 'Scan.co.uk',
        'Geographic_Region': 'UK/EU',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.scan.co.uk/products/40gb-pny-nvidia-a800-active-6912-cuda-432-tensor-hbm2-195-tflops-fp32-3118-tflops-tf32-retail',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'PNY retail packaging, financing available, 36-month warranty',
        'Stock_Status': 'Pre-order',
        'Authentication_Signals': 'PNY authorized partner, retail packaging'
    },
    
    # Japan Price Comparison (Kakaku.com)
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 13200.00,  # Conversion from ¥1,980,000 (lowest price)
        'Quantity': 'In Stock',
        'Min_Order_Qty': 1,
        'Seller': 'Japanese retailers (aggregated)',
        'Geographic_Region': 'Japan/Asia',
        'Listing_Age': 'Current',
        'Source_URL': 'https://kakaku.com/item/K0001605271/',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'Price range ¥1,980,000-¥2,666,750 across multiple retailers',
        'Stock_Status': 'In Stock',
        'Authentication_Signals': 'Multiple authorized Japanese retailers'
    },
    
    # Singapore SourceIT - Asian market
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 'Price on request',
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'SourceIT Singapore',
        'Geographic_Region': 'Singapore/Asia',
        'Listing_Age': 'Recent',
        'Source_URL': 'https://sourceit.com.sg/products/nvidia-a800-pcie-40-gb-active-cooling-ampere-900-51001-2500-000',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'Local warranty, detailed specifications listed',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'Local warranty, professional specifications'
    },
    
    # Avendor - Enterprise supplier
    {
        'Model': 'NVIDIA A800 Active 40GB',
        'Condition': 'New',
        'Price_USD': 'Quote required',
        'Quantity': 'Available',
        'Min_Order_Qty': 1,
        'Seller': 'Avendor',
        'Geographic_Region': 'US domestic',
        'Listing_Age': 'Current',
        'Source_URL': 'https://www.avendor.com/products/nvidia-nvidia-a800-graphic-card-40-gb-hbm2',
        'Source_Type': 'Retail_Specialist',
        'Bulk_Notes': 'Detailed technical specifications, quote-based pricing',
        'Stock_Status': 'Available',
        'Authentication_Signals': 'Enterprise-focused, detailed technical specs'
    }
])

# Create partial data entries for sources with limited info
partial_data = [
    {
        'Source': 'CDW',
        'Model_Available': 'Yes',
        'Notes': 'Product page exists but no pricing displayed - likely quote-based',
        'URL': 'https://www.cdw.com/product/pny-nvidia-a800-graphic-card-40-gb-hbm2-low-profile/7840537'
    },
    {
        'Source': 'Dell',
        'Model_Available': 'Yes', 
        'Notes': 'Dell branded A800 available but pricing not public',
        'URL': 'https://www.dell.com/en-us/shop/dell-nvidia-rtx-a800-40-gb-hbm2-full-height-pcie-40x16-graphics-card/apd/490-bkfy/graphic-video-cards'
    },
    {
        'Source': 'WiredZone',
        'Model_Available': 'No',
        'Notes': 'Only A800 80GB model listed, 40GB model not available',
        'URL': 'https://www.wiredzone.com/shop/product/10025506-nvidia-900-21001-0030-100-graphics-processing-unit-gpu-a800-80gb-hbm2-memory-10759'
    },
    {
        'Source': 'ServerMonkey',
        'Model_Available': 'No results',
        'Notes': 'No A800 40GB Active listings found in search results',
        'URL': 'N/A'
    }
]

# Convert to DataFrame for CSV export
df = pd.DataFrame(pricing_data)

# Display summary statistics
print("=== NVIDIA A800 40GB Active Pricing Data Summary ===")
print(f"Total listings found: {len(df)}")
print(f"MSRP: $19,999.00")
print()

# Filter out non-numeric prices for analysis
numeric_prices = df[df['Price_USD'].astype(str).str.replace(',','').str.replace('$','').str.isnumeric()]
if len(numeric_prices) > 0:
    prices = numeric_prices['Price_USD'].astype(float)
    print(f"Price range: ${prices.min():,.2f} - ${prices.max():,.2f}")
    print(f"Average price: ${prices.mean():,.2f}")
    print(f"Median price: ${prices.median():,.2f}")
    print()

# Count by source type
print("Source Type Distribution:")
print(df['Source_Type'].value_counts())
print()

# Count by region
print("Geographic Distribution:")
print(df['Geographic_Region'].value_counts())
print()

# Count by stock status
print("Stock Status Distribution:")
print(df['Stock_Status'].value_counts())
print()

# Identify pricing anomalies
print("=== Pricing Anomaly Flags ===")
numeric_df = df[pd.to_numeric(df['Price_USD'], errors='coerce').notna()]
if len(numeric_df) > 0:
    numeric_df['Price_USD'] = pd.to_numeric(numeric_df['Price_USD'])
    msrp = 19999.00
    
    # Flag significant deviations
    for idx, row in numeric_df.iterrows():
        price = row['Price_USD']
        deviation = ((price - msrp) / msrp) * 100
        
        if abs(deviation) > 20:  # More than 20% deviation
            status = "SIGNIFICANTLY LOW" if deviation < -20 else "PREMIUM PRICING"
            print(f"⚠️ {status}: {row['Seller']} - ${price:,.2f} ({deviation:+.1f}% vs MSRP)")
            if deviation < -60:
                print(f"   ⚠️ POTENTIAL AUTHENTICITY CONCERN: Price 60%+ below MSRP")

print("\n=== NO DATA FOUND ===")
print("ServerMonkey: No A800 40GB Active listings found in search results")

print("\n=== PARTIAL DATA ===")
for item in partial_data:
    print(f"{item['Source']}: {item['Notes']}")

# Export to CSV
df.to_csv('nvidia_a800_40gb_pricing_data.csv', index=False)
print(f"\n✅ Data exported to 'nvidia_a800_40gb_pricing_data.csv'")
print(f"✅ Total sources searched: 10+ platforms across retail, enterprise, and international markets")