# Create a comprehensive CSV of NVIDIA A40 pricing data

import pandas as pd

# Create pricing data based on the search results
pricing_data = [
    # Retail Sources - Major/Specialist
    {
        "Model": "NVIDIA A40",
        "Condition": "New",
        "Price_USD": 6439,
        "Quantity": "In Stock",
        "Min_Order_Qty": 1,
        "Seller": "Router-Switch.com",
        "Geographic_Region": "US",
        "Listing_Age": "Stale",
        "Source_URL": "https://www.router-switch.com/nvidia-a40.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Up to $80 coupons available",
    },
    {
        "Model": "NVIDIA A40 (Dell)",
        "Condition": "Refurbished",
        "Price_USD": 5999,
        "Quantity": "3",
        "Min_Order_Qty": 1,
        "Seller": "Xbyte.com",
        "Geographic_Region": "US",
        "Listing_Age": "Current",
        "Source_URL": "https://www.xbyte.com/products/cat-23978/",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Was $9,999 - Dell OEM",
    },
    {
        "Model": "NVIDIA A40",
        "Condition": "New",
        "Price_USD": 5170,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "Newegg Direct",
        "Geographic_Region": "US",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.newegg.com/p/pl?d=nvidia+a40",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "Free shipping",
    },
    {
        "Model": "PNY NVIDIA A40",
        "Condition": "New",
        "Price_USD": 5599,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "Newegg",
        "Geographic_Region": "US",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.newegg.com/p/pl?d=nvidia+a40",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "Free shipping",
    },
    {
        "Model": "NVIDIA A40",
        "Condition": "New",
        "Price_USD": 5499,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "C3Aero LLC",
        "Geographic_Region": "US",
        "Listing_Age": "Stale",
        "Source_URL": "https://c3aero.com/products/nvidia-a40-datacenter-gpu",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "PNY Partner",
    },
    {
        "Model": "NVIDIA A40",
        "Condition": "Refurbished",
        "Price_USD": 5999,
        "Quantity": "Limited",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (Dell)",
        "Geographic_Region": "US",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.newegg.com/p/pl?d=nvidia+a40",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "Dell refurbished",
    },
    # Enterprise/CDW/Provantage (no public pricing)
    {
        "Model": "NVIDIA A40",
        "Condition": "New",
        "Price_USD": "Quote",
        "Quantity": "Available",
        "Min_Order_Qty": "Varies",
        "Seller": "CDW",
        "Geographic_Region": "US",
        "Listing_Age": "Current",
        "Source_URL": "https://www.cdw.com/product/nvidia-a40-gpu-computing-processor-nvidia-a40-48-gb/7005474",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Enterprise pricing - quote required",
    },
    {
        "Model": "Cisco Tesla A40 RTX",
        "Condition": "New",
        "Price_USD": "Quote",
        "Quantity": "Available",
        "Min_Order_Qty": 10000,
        "Seller": "Provantage",
        "Geographic_Region": "US",
        "Listing_Age": "Current",
        "Source_URL": "https://www.provantage.com/cisco-systems-ucsc-gpu-a40-d~7CSC62R5.htm",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Min $10,000 Cisco purchase required",
    },
    # eBay Listings - International
    {
        "Model": "NVIDIA Tesla A40",
        "Condition": "New (Opened)",
        "Price_USD": 7749,
        "Quantity": "1",
        "Min_Order_Qty": 1,
        "Seller": "binhua158 (eBay)",
        "Geographic_Region": "Asia/CN",
        "Listing_Age": "Stale",
        "Source_URL": "https://www.ebay.com.au/itm/296430453835",
        "Source_Type": "International",
        "Bulk_Notes": "Ships from China, no returns",
    },
    {
        "Model": "NVIDIA Tesla A40",
        "Condition": "New",
        "Price_USD": 13200,
        "Quantity": "47",
        "Min_Order_Qty": 1,
        "Seller": "MemoryPartner_Deals (eBay)",
        "Geographic_Region": "Asia/CN",
        "Listing_Age": "Stale",
        "Source_URL": "https://www.ebay.com.au/itm/374192509164",
        "Source_Type": "International",
        "Bulk_Notes": "60-day returns, bulk available",
    },
    {
        "Model": "NVIDIA A40",
        "Condition": "New",
        "Price_USD": 6300,
        "Quantity": "1",
        "Min_Order_Qty": 1,
        "Seller": "heinzsoft (eBay.de)",
        "Geographic_Region": "EU",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.ebay.de/itm/286207081910",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "Ended - no longer available",
    },
    # Reddit/Forums Discussion
    {
        "Model": "NVIDIA Tesla A40",
        "Condition": "Used",
        "Price_USD": 4900,
        "Quantity": "Discussion",
        "Min_Order_Qty": 1,
        "Seller": "Reddit r/homelabsales",
        "Geographic_Region": "US/UK",
        "Listing_Age": "Stale",
        "Source_URL": "https://www.reddit.com/r/homelabsales/comments/12aue6s/pc_nvidia_tesla_a40_48gb/",
        "Source_Type": "Resale_Individual",
        "Bulk_Notes": "Discussion: fair price $4200-4500, recent eBay $4900",
    },
    # Used/Refurbished Sources
    {
        "Model": "NVIDIA A40",
        "Condition": "Refurbished",
        "Price_USD": "Out of Stock",
        "Quantity": "0",
        "Min_Order_Qty": 1,
        "Seller": "PCServerAndParts",
        "Geographic_Region": "US",
        "Listing_Age": "Recent",
        "Source_URL": "https://pcserverandparts.com/nvidia-a40-gpu-accelerator-48gb-gddr6-tesla-ampere-used-pg133c-900-2g133-0000-000-699-2g133-0200-c00/",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "90-day warranty",
    },
    {
        "Model": "Dell NVIDIA A40",
        "Condition": "Refurbished",
        "Price_USD": "Quote",
        "Quantity": "3",
        "Min_Order_Qty": 1,
        "Seller": "Bytestock",
        "Geographic_Region": "UK",
        "Listing_Age": "Recent",
        "Source_URL": "https://shop.bytestock.com/dell-nvidia-a40-ampere-48gb-gddr6-passive-gpu-graphics-card-w6gx6-tcsa40m-pm",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "30-70% off MSRP, Dell OEM",
    },
    # UK/EU Pricing
    {
        "Model": "PNY NVIDIA A40",
        "Condition": "New",
        "Price_USD": 7700,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "Zoro.co.uk",
        "Geographic_Region": "UK",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.idealo.co.uk/compare/201658583/pny-nvidia-a40-48g.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "£6,199.99 + shipping",
    },
    {
        "Model": "PNY NVIDIA A40",
        "Condition": "New",
        "Price_USD": 7342,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "Novatech",
        "Geographic_Region": "UK",
        "Listing_Age": "Current",
        "Source_URL": "https://www.novatech.co.uk/products/pny-nvidia-a40-48gb-gddr6-ecc-data-centre-gpu/tcsa40m-pb.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "£6,496.50 inc. VAT, 24-month financing",
    },
    {
        "Model": "PNY NVIDIA A40",
        "Condition": "New",
        "Price_USD": 7840,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "LDLC",
        "Geographic_Region": "EU",
        "Listing_Age": "Stale",
        "Source_URL": "https://www.ldlc.com/en/product/PB00462697.html",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "€6,849.95, 3-year warranty",
    },
    # Liquidation/Special
    {
        "Model": "NVIDIA A40",
        "Condition": "Liquidation",
        "Price_USD": 5500,
        "Quantity": "Limited",
        "Min_Order_Qty": 1,
        "Seller": "Instagram Liquidation",
        "Geographic_Region": "US",
        "Listing_Age": "Recent",
        "Source_URL": "https://www.instagram.com/p/C_A-nytyi1y/",
        "Source_Type": "Liquidation",
        "Bulk_Notes": "Liquidation sale - limited availability",
    },
]

# Convert to DataFrame
df = pd.DataFrame(pricing_data)

# Clean up price column for better sorting
df["Price_Sort"] = pd.to_numeric(df["Price_USD"].replace("Quote", 0).replace("Out of Stock", 0), errors="coerce")

# Sort by price (excluding quotes and out of stock)
df_sorted = df.sort_values("Price_Sort", ascending=True)

# Save to CSV
df_sorted.to_csv("nvidia_a40_pricing_data.csv", index=False)

print("CSV file created: nvidia_a40_pricing_data.csv")
print("\nSummary of findings:")
print(f"Total listings found: {len(df)}")

# Price statistics (excluding quotes and zero values)
valid_prices = df_sorted[df_sorted["Price_Sort"] > 0]["Price_Sort"]
if len(valid_prices) > 0:
    print(f"Price range: ${valid_prices.min():,.0f} - ${valid_prices.max():,.0f}")
    print(f"Average price: ${valid_prices.mean():,.0f}")
    print(f"Median price: ${valid_prices.median():,.0f}")

# Show the CSV structure
print("\nFirst few rows of the CSV:")
print(df_sorted[["Model", "Condition", "Price_USD", "Seller", "Source_Type"]].head(10))
