import pandas as pd
from datetime import datetime

# Compile the NVIDIA L4 pricing data into the requested CSV format
data = [
    # Retail Major
    ["NVIDIA L4", "New", 2524.99, 1, 1, "Newegg", "US domestic", "Current", "https://www.newegg.com/p/N82E16888892004", "Retail_Major", "Free shipping"],
    
    # Retail Specialist  
    ["NVIDIA L4", "New", 2549.00, 1, 1, "Router-Switch", "US domestic", "Current", "https://www.router-switch.com/nvidia-l4.html", "Retail_Specialist", "Global warehouses, up to $80 coupons available"],
    ["NVIDIA L4", "New", 3399.00, 1, 1, "Marigold Systems", "US domestic", "Stale", "https://www.marigoldsystems.com/products/nvidia-l4-24gb-single", "Retail_Specialist", "Out of stock"],
    ["NVIDIA L4", "New", 3150.00, 1, 1, "EuroPC", "EU", "Current", "https://www.europc.com/us/nvidia-l4-tensor-core-ai-computational", "Retail_Specialist", "£2519.99 inc VAT, £2099.99 ex VAT"],
    ["NVIDIA L4", "New", 3150.00, 1, 1, "Novatech UK", "EU", "Current", "https://www.novatech.co.uk/products/pny-nvidia-l4-24gb-gddr6", "Retail_Specialist", "£2519.99 inc VAT, financing available"],
    ["NVIDIA L4", "New", 2136.00, 1, 1, "ViperaTech", "US domestic", "Recent", "https://viperatech.com/shop/nvidia-l4-24g-pcie-tensor", "Retail_Specialist", "Sale price, was $3,081 - $945 savings"],
    ["NVIDIA L4", "New", 2487.50, 1, 1, "SabrePC", "US domestic", "Current", "https://www.sabrepc.com/900-2G193-0000-000-NVIDIA", "Retail_Specialist", "B2B pricing available, non-cancelable"],
    
    # Resale Business
    ["NVIDIA L4", "New", 2072.00, 10, 1, "eBay Business Seller", "Asia/HK", "Current", "https://www.ebay.de/itm/126436167844", "Resale_Business", "Chinese seller, 99.4% feedback, 11 sold"],
    ["NVIDIA L4", "Refurbished", 2599.00, 1, 1, "xByte Technologies", "US domestic", "Current", "https://www.newegg.com/p/2NS-0008-7B2V4", "Resale_Business", "Dell refurbished, 30-day return policy"],
    ["NVIDIA L4", "New", 2150.00, 10, 1, "eBay Business Seller", "Asia/HK", "Current", "https://www.ebay.co.uk/itm/204746958291", "Resale_Business", "98.5% feedback, 4.4K items sold"],
    ["NVIDIA L4", "New", 2425.00, 10, 1, "eBay Business Seller", "Asia/HK", "Current", "https://www.ebay.co.uk/itm/375843854373", "Resale_Business", "99.3% feedback, 12K items sold"],
    ["NVIDIA L4", "New", 5680.00, 2, 1, "Bonanza Seller", "US domestic", "Current", "https://www.bonanza.com/listings/Nvidia-Tesla-L4-24G", "Resale_Business", "30-day return, PayPal accepted"],
    
    # Enterprise/Liquidation
    ["NVIDIA L4", "New", 7566.00, 1, 1, "SHI (HPE)", "US domestic", "Current", "https://www.shi.com/product/45410419", "Liquidation", "MSRP listed, enterprise channel"],
    ["NVIDIA L4", "New", 7874.11, 1, 1, "SHI (Hitachi Vantara)", "US domestic", "Current", "https://www.shi.com/product/49450195", "Liquidation", "MSRP listed, enterprise channel"],
    ["NVIDIA L4", "New", 8107.99, 1, 1, "Zones (Cisco UCS)", "US domestic", "Current", "https://www.zones.com/site/product/index.html?id=115013295", "Liquidation", "Cisco UCS variant UCSX-GPU-L4"],
    ["NVIDIA L4", "New", 4729.99, 1, 1, "Newegg (HPE)", "US domestic", "Current", "https://www.newegg.com/hpe-s0k89c/p/N82E16816269085", "Liquidation", "HPE S0K89C model, 1-year warranty"],
    ["NVIDIA L4", "New", 11184.81, 1, 1, "Dell Singapore", "Asia/SG", "Current", "https://www.dell.com/en-sg/shop/nvidia-l4-pcie-72-watt", "Liquidation", "SGD price includes 9% GST"],
    
    # International 
    ["NVIDIA L4", "New", 1980.00, 1, 1, "eBay International", "EU", "Stale", "https://www.ebay.co.uk/itm/363551612404", "International", "€1,819.00, listing ended Jun 2025"],
    ["NVIDIA L4", "New", 2200.00, 879, 1, "Alibaba Sellers", "Asia/HK", "Current", "https://www.alibaba.com/showroom/l4-nvidia.html", "International", "879+ products available, various suppliers"],
]

# Create DataFrame
columns = ["Model", "Condition", "Price_USD", "Quantity", "Min_Order_Qty", "Seller", "Geographic_Region", "Listing_Age", "Source_URL", "Source_Type", "Bulk_Notes"]
df = pd.DataFrame(data, columns=columns)

# Add stock status and pricing anomaly flags
df['Stock_Status'] = ['In Stock', 'In Stock', 'Out of Stock', 'In Stock', 'In Stock', 'In Stock', 'In Stock', 
                      'In Stock', 'Limited Stock', 'In Stock', 'In Stock', 'In Stock', 
                      'In Stock', 'In Stock', 'In Stock', 'In Stock', 'In Stock', 'Out of Stock', 'In Stock']

df['Pricing_Anomaly_Flag'] = ['', '', 'Premium pricing - specialty retailer', '', '', 'Sale pricing - 30% discount', '', 
                               'Below typical range - may be gray market', '', '', '', 'Premium pricing - enterprise grade',
                               '3x typical price - enterprise MSRP', '3x typical price - enterprise MSRP', '3x typical price - enterprise MSRP',
                               'Above typical - enterprise channel', '4x typical price - includes enterprise markup',
                               'Below typical - ended listing', 'Bulk wholesale pricing']

# Display the compiled data
print("NVIDIA L4 GPU Pricing Data Compilation")
print("="*50)
print(f"Data compiled on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total listings found: {len(df)}")
print(f"Price range: ${df['Price_USD'].min():.2f} - ${df['Price_USD'].max():.2f}")
print(f"Average price: ${df['Price_USD'].mean():.2f}")
print(f"Median price: ${df['Price_USD'].median():.2f}")
print()

# Show source type distribution
print("Source Type Distribution:")
print(df['Source_Type'].value_counts())
print()

# Show price statistics by source type
print("Price Statistics by Source Type:")
price_stats = df.groupby('Source_Type')['Price_USD'].agg(['min', 'max', 'mean', 'count']).round(2)
print(price_stats)
print()

# Save to CSV
df.to_csv('nvidia_l4_pricing_data.csv', index=False)
print("Data saved to 'nvidia_l4_pricing_data.csv'")

# Display the CSV format
print("\nCSV Format Preview:")
print(df.to_string(index=False))