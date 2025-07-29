import pandas as pd

# Compile the pricing data I found into the requested CSV format
pricing_data = [
    # Retail Major
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 975,
        "Quantity": "Unknown",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (PNY)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "newegg.com/p/1FT-000P-005Y7",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "Free delivery",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1070,
        "Quantity": "Unknown",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (TECH EDGE)",
        "Geographic_Region": "Asia/China",
        "Listing_Age": "Current",
        "Source_URL": "newegg.com/p/0XP-00VH-000G9",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "Ships from China",
    },
    # Retail Specialist
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 889,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "Router-Switch.com",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "router-switch.com/nvidia-a2.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "New Factory Sealed, Global Warehouses",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "Unavailable",
        "Price_USD": 1399,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "C3aero.com",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "c3aero.com/products/pny-nvidia-a2-graphics-card-16gb-gddr6",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Unavailable - pricing reference only",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 5576,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "CDW Canada",
        "Geographic_Region": "Canada",
        "Listing_Age": "Current",
        "Source_URL": "cdw.ca/product/nvidia-a2-gpu-computing-processor-a2-16-gb/7474786",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Enterprise pricing, converted from CAD 7193.99",
    },
    # Resale Business
    {
        "Model": "NVIDIA A2",
        "Condition": "Refurbished",
        "Price_USD": 699,
        "Quantity": "Unknown",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (ServerQue)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "newegg.com/nvidia-tesla-a2-graphics-card/p/1WK-00TY-00082",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "30-day return policy",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "Refurbished",
        "Price_USD": 750,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "ServerSupply",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current",
        "Source_URL": "serversupply.com/GPU/GDDR6/16%20GIGABIT/NVIDIA/900-2G179-0020-000_395854.htm",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "90 days warranty, refurbished condition",
    },
    # International
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1947,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "LDLC (France)",
        "Geographic_Region": "EU",
        "Listing_Age": "Current",
        "Source_URL": "ldlc.com/en/product/PB00482177.html",
        "Source_Type": "International",
        "Bulk_Notes": "Converted from €1539.95, 3-year warranty",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 1912,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "Novatech (UK)",
        "Geographic_Region": "EU",
        "Listing_Age": "Current",
        "Source_URL": "novatech.co.uk/products/pny-nvidia-a2-16gb-gddr6-ecc-data-centre-gpu/tcsa2matx-pb.html",
        "Source_Type": "International",
        "Bulk_Notes": "Converted from £1560.20 inc VAT, UK pricing",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "New",
        "Price_USD": 730,
        "Quantity": "1+",
        "Min_Order_Qty": 1,
        "Seller": "Alibaba Supplier",
        "Geographic_Region": "Asia/China",
        "Listing_Age": "Current",
        "Source_URL": "alibaba.com/showroom/nvidia-a2-gpu.html",
        "Source_Type": "International",
        "Bulk_Notes": "$730-750 range, original for AI/HPC",
    },
    # Resale Individual (eBay)
    {
        "Model": "NVIDIA A2",
        "Condition": "Used",
        "Price_USD": 521,
        "Quantity": "1",
        "Min_Order_Qty": 1,
        "Seller": "eBay UK Seller",
        "Geographic_Region": "EU",
        "Listing_Age": "Current",
        "Source_URL": "ebay.co.uk/shop/nvidia-a2",
        "Source_Type": "Resale_Individual",
        "Bulk_Notes": "Converted from £399, used condition, China seller",
    },
    {
        "Model": "NVIDIA A2",
        "Condition": "Refurbished",
        "Price_USD": 780,
        "Quantity": "1",
        "Min_Order_Qty": 1,
        "Seller": "eBay UK Dell Seller",
        "Geographic_Region": "EU",
        "Listing_Age": "Current",
        "Source_URL": "ebay.co.uk/shop/nvidia-a2",
        "Source_Type": "Resale_Individual",
        "Bulk_Notes": "Converted from £600, Dell branded, refurbished",
    },
]

# Create DataFrame
df = pd.DataFrame(pricing_data)

# Display the data
print("NVIDIA A2 GPU Pricing Data Summary:")
print("=" * 50)
print(f"Total listings found: {len(df)}")
print(f"Price range: ${df['Price_USD'].min()} - ${df['Price_USD'].max()}")
print(f"Average price: ${df['Price_USD'].mean():.2f}")
print(f"Median price: ${df['Price_USD'].median():.2f}")
print()

# Group by source type
print("Pricing by Source Type:")
print("=" * 30)
source_summary = df.groupby("Source_Type")["Price_USD"].agg(["count", "min", "max", "mean"]).round(2)
print(source_summary)
print()

# Group by condition
print("Pricing by Condition:")
print("=" * 25)
condition_summary = df.groupby("Condition")["Price_USD"].agg(["count", "min", "max", "mean"]).round(2)
print(condition_summary)
print()

# Save to CSV
df.to_csv("nvidia_a2_pricing_data.csv", index=False)
print("Data saved to: nvidia_a2_pricing_data.csv")
print()

# Display the full CSV format as requested
print("CSV Output:")
print("=" * 50)
print(df.to_csv(index=False))
