import pandas as pd
from datetime import datetime

# Create a comprehensive dataset based on all the search results
data = []

# Retail Major sources
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 5499,
    'Quantity': 'Multiple',
    'Min_Order_Qty': 1,
    'Seller': 'Newegg (PNY)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.newegg.com/p/pl?d=rtx+a6000',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Free shipping, multiple SKUs available'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 4399,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Newegg (PNY OEM)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.newegg.com/p/N82E16814133822',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'OEM version, replacement only return policy'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 6680,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Newegg (Third Party)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.newegg.com/p/pl?d=rtx+a6000',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Higher-end SKU or different vendor'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 8899,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Newegg (Boxed)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.newegg.com/p/pl?d=rtx+a6000',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Boxed retail version with accessories'
})

# B&H Photo
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 'Out of Stock',
    'Quantity': 0,
    'Min_Order_Qty': 1,
    'Seller': 'B&H Photo',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.bhphotovideo.com/c/product/1607840-REG/pny_technologies_vcnrtxa6000_pb_nvidia_rtx_a6000_graphic.html',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Out of stock'
})

# Retail Specialist sources
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 'Quote Required',
    'Quantity': 'Available',
    'Min_Order_Qty': 1,
    'Seller': 'CDW',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.cdw.com/product/nvidia-rtx-a6000-graphics-card-rtx-a6000-48-gb/7928471',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': 'Enterprise focus, quote-based pricing'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 7500,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'ServerSupply',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.serversupply.com/GPU/GDDR6/48GB/PNY%20Technology/VCNRTXA6000-SB_379239.htm',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': 'New factory sealed'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 3199,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Router-Switch.com',
    'Geographic_Region': 'International',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.router-switch.com/nvidia-rtx-6000.html',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': 'Global warehouses, coupons available'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'Delivery Unknown',
    'Price_USD': 5580,
    'Quantity': 'Delivery Unknown',
    'Min_Order_Qty': 1,
    'Seller': 'ComputerUniverse (EU)',
    'Geographic_Region': 'EU',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.computeruniverse.net/en/p/2E17-06A',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': 'EUR price converted, delivery date unknown'
})

# WiredZone - Out of stock
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 'Out of Stock',
    'Quantity': 0,
    'Min_Order_Qty': 1,
    'Seller': 'WiredZone',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.wiredzone.com/shop/product/10021351',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': 'Out of stock'
})

# Resale sources
data.append({
    'Model': 'RTX A6000',
    'Condition': 'Refurbished',
    'Price_USD': 4738,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Newegg (Compeve)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://www.newegg.com/p/2VV-000K-00127',
    'Source_Type': 'Resale_Business',
    'Bulk_Notes': 'Refurbished with specs listed'
})

# Amazon pricing data from CamelCamelCamel
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 4924,
    'Quantity': 'Varies',
    'Min_Order_Qty': 1,
    'Seller': 'Amazon (3rd Party New)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://camelcamelcamel.com/product/B09BDH8VZV',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Current 3rd party new price as of July 2025'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'Used',
    'Price_USD': 4439,
    'Quantity': 'Varies',
    'Min_Order_Qty': 1,
    'Seller': 'Amazon (3rd Party Used)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://camelcamelcamel.com/product/B09BDH8VZV',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': 'Current 3rd party used price as of July 2025'
})

# PCPartPicker aggregated data
data.append({
    'Model': 'RTX A6000',
    'Condition': 'New',
    'Price_USD': 3849,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Amazon (PCPartPicker)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://pcpartpicker.com/product/HWt9TW/pny-rtx-a-series-rtx-a6000-48-gb-video-card-vcnrtxa6000-pb',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': '10 new listings from $3849-4999'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'Used',
    'Price_USD': 3449,
    'Quantity': 'In Stock',
    'Min_Order_Qty': 1,
    'Seller': 'Amazon (PCPartPicker Used)',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://pcpartpicker.com/product/HWt9TW/pny-rtx-a-series-rtx-a6000-48-gb-video-card-vcnrtxa6000-pb',
    'Source_Type': 'Retail_Major',
    'Bulk_Notes': '4 used listings from $3449-4499'
})

# eBay and Reddit resale data
data.append({
    'Model': 'RTX A6000',
    'Condition': 'Used',
    'Price_USD': 3200,
    'Quantity': 'Individual',
    'Min_Order_Qty': 1,
    'Seller': 'Reddit r/homelabsales',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Stale',
    'Source_URL': 'https://www.reddit.com/r/homelabsales/comments/17e5b2u/w_used_rtx_a6000/',
    'Source_Type': 'Resale_Individual',
    'Bulk_Notes': 'User mentions typical eBay range 3200-3400'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'Used',
    'Price_USD': 3500,
    'Quantity': 'Individual',
    'Min_Order_Qty': 1,
    'Seller': 'Reddit r/homelabsales seller',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Stale',
    'Source_URL': 'https://www.reddit.com/r/homelabsales/comments/10fqo4f/fs_usw_nvidia_quadro_a6000/',
    'Source_Type': 'Resale_Individual',
    'Bulk_Notes': 'Individual seller, shipped US'
})

data.append({
    'Model': 'Server with RTX A6000',
    'Condition': 'Used',
    'Price_USD': 9664, # £7495 converted at ~1.29 rate
    'Quantity': 4,
    'Min_Order_Qty': 1,
    'Seller': 'eBay UK (CTOServers)',
    'Geographic_Region': 'EU',
    'Listing_Age': 'Recent',
    'Source_URL': 'https://www.ebay.co.uk/itm/276839971749',
    'Source_Type': 'Resale_Business',
    'Bulk_Notes': 'Complete server with A6000, HPE ProLiant DL380 Gen10'
})

# Cloud/hosting pricing for reference
data.append({
    'Model': 'RTX A6000',
    'Condition': 'Cloud Rental',
    'Price_USD': 1.89, # per hour
    'Quantity': 'Available',
    'Min_Order_Qty': 1,
    'Seller': 'DigitalOcean',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.digitalocean.com/pricing/additional-gpus',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': '$1.89/hour, 45GiB RAM, 8 vCPUs'
})

data.append({
    'Model': 'RTX A6000',
    'Condition': 'Cloud Rental',
    'Price_USD': 373, # per month
    'Quantity': 'Available',
    'Min_Order_Qty': 1,
    'Seller': 'GPU-Mart',
    'Geographic_Region': 'US domestic',
    'Listing_Age': 'Current',
    'Source_URL': 'https://www.gpu-mart.com/blog/best-gpus-for-ai-inference-2025',
    'Source_Type': 'Retail_Specialist',
    'Bulk_Notes': '$373/month dedicated server, 32% discount available'
})

# Create DataFrame
df = pd.DataFrame(data)

# Display the data
print("NVIDIA RTX A6000 (Ampere) Pricing Data - July 2025")
print("=" * 60)
print(f"Total listings found: {len(df)}")
print()

# Filter out non-purchase listings
purchase_df = df[~df['Price_USD'].isin(['Out of Stock', 'Quote Required', 'Cloud Rental'])]
numeric_prices = purchase_df[pd.to_numeric(purchase_df['Price_USD'], errors='coerce').notna()]

if len(numeric_prices) > 0:
    min_price = numeric_prices['Price_USD'].astype(float).min()
    max_price = numeric_prices['Price_USD'].astype(float).max()
    avg_price = numeric_prices['Price_USD'].astype(float).mean()
    
    print(f"Price Range: ${min_price:,.0f} - ${max_price:,.0f}")
    print(f"Average Price: ${avg_price:,.0f}")
    print()

# Count by source type
source_counts = df['Source_Type'].value_counts()
print("Listings by Source Type:")
for source, count in source_counts.items():
    print(f"  {source}: {count}")
print()

# Count by condition
condition_counts = df['Condition'].value_counts()
print("Listings by Condition:")
for condition, count in condition_counts.items():
    print(f"  {condition}: {count}")
print()

# Save to CSV
df.to_csv('rtx_a6000_pricing_data.csv', index=False)
print("Data saved to rtx_a6000_pricing_data.csv")

# Display full table for verification
print("\nFull Dataset:")
print(df.to_string(index=False))