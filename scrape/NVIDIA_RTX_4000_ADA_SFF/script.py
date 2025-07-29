# Create comprehensive CSV data for NVIDIA RTX 4000 Ada SFF pricing analysis

import pandas as pd

# Create the pricing data based on the research findings
pricing_data = [
    # US Retail - Major
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1939.99,
        "In Stock",
        1,
        "CDW",
        "US",
        "Current",
        "https://www.cdw.com/product/nvidia-rtx-4000-ada-graphics-card-rtx-4000-sff-ada-20-gb/8377274",
        "Retail_Major",
        "Down from $2,623.99 - 26% discount",
    ],
    # US Retail - Specialist
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1581.80,
        "In Stock",
        1,
        "Connection",
        "US",
        "Current",
        "https://www.connection.com/product/pny-nvidia-rtx-4000-sff-ada-generation-pcie-4.0-x16-graphics-card-20gb-gddr6/vcnrtx4000adalp-pb/41615067",
        "Retail_Specialist",
        "Ships in 48 Hours",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1600.00,
        "Limited Stock",
        1,
        "ServerSupply",
        "US",
        "Current",
        "https://www.serversupply.com/GPU/GDDR6/20GB/PNY%20Technology/VCNRTX4000ADALP-PB_377624.htm",
        "Retail_Specialist",
        "Down from $1,850 - 13% off",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1382.01,
        "In Stock",
        8,
        "Channel Online",
        "US",
        "Current",
        "https://usm.channelonline.com/netcombsi/storesite/Products/overview/M024302451",
        "Retail_Specialist",
        "Bulk quantity available",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1299.99,
        "In Stock",
        1,
        "Central Computer",
        "US",
        "Current",
        "https://www.centralcomputer.com/pny-vcnrtx4000adalp-pb-nvidia-rtx-4000-sff-ada-graphics-card-20-gb-gddr6-ecc-2-slot-pcie-4-0-x16-mdp-1-4a.html",
        "Retail_Specialist",
        "14-day returns",
    ],
    # US Retail - Major (Newegg variants)
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1275.99,
        "In Stock",
        1,
        "Newegg - PNY",
        "US",
        "Current",
        "https://www.newegg.com/p/pl?d=rtx+4000+ada+sff",
        "Retail_Major",
        "Free shipping",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        2119.99,
        "In Stock",
        1,
        "Newegg - Tech Edge",
        "US",
        "Current",
        "https://www.newegg.com/p/1FT-0004-00904",
        "Retail_Major",
        "Industrial package, ships from China",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        2208.00,
        "In Stock",
        1,
        "Newegg - Leadtek",
        "US",
        "Current",
        "https://www.newegg.com/p/pl?d=rtx+4000+ada+sff",
        "Retail_Major",
        "Free shipping",
    ],
    # International Retail
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1959.70,
        "In Stock",
        1,
        "Computer Universe",
        "EU",
        "Current",
        "https://www.computeruniverse.net/en/p/2E17-07X",
        "International",
        "€1,461 - converted to USD",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1723.33,
        "In Stock",
        1,
        "Overclockers UK",
        "EU",
        "Current",
        "https://www.overclockers.co.uk/nvidia-rtx-4000-sff-ada-20gb-gddr6-pci-express-graphics-card-oem-gra-nvi-05600.html",
        "International",
        "£1,339.99 - converted to USD",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1489.48,
        "In Stock",
        2,
        "Alternate.de",
        "EU",
        "Current",
        "https://www.alternate.de/PNY/NVIDIA-RTX-4000-SFF-Ada-Generation-20GB-PB-Grafikkarte/html/product/1914392",
        "International",
        "€1,399 down from €1,509",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        2144.64,
        "In Stock",
        1,
        "MediaMarkt",
        "EU",
        "Current",
        "https://www.mediamarkt.de/de/product/_pny-vcnrtx4000adalp-pb-nvidia-grafikkarte-142765925.html",
        "International",
        "€1,600 - premium pricing",
    ],
    # Resale - eBay International
    [
        "NVIDIA RTX 4000 SFF Ada",
        "Used",
        1085.16,
        "Sold",
        1,
        "eBay US Seller",
        "US",
        "Recent",
        "https://www.benl.ebay.be/sch/i.html?_nkw=rtx+4000+sff+ada",
        "Resale_Individual",
        "EUR 1,019.45 - converted to USD, never used",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1267.06,
        "Sold",
        1,
        "eBay US Seller",
        "US",
        "Recent",
        "https://www.benl.ebay.be/sch/i.html?_nkw=rtx+4000+sff+ada",
        "Resale_Business",
        "EUR 1,189.36 - 13 sold",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1397.16,
        "Active",
        1,
        "eBay China Seller",
        "Asia",
        "Current",
        "https://www.benl.ebay.be/sch/i.html?_nkw=rtx+4000+sff+ada",
        "International",
        "EUR 1,310 - Founders Edition claim",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1713.54,
        "Active",
        1,
        "eBay China Seller",
        "Asia",
        "Current",
        "https://www.benl.ebay.be/sch/i.html?_nkw=rtx+4000+sff+ada",
        "International",
        "EUR 1,605.64 - Professional graphics",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        2837.06,
        "Ended",
        1,
        "eBay Japan Seller",
        "Asia",
        "Stale",
        "https://www.ebay.co.uk/itm/286151546995",
        "International",
        "Listing ended - high premium pricing",
    ],
    # Amazon Third Party (Historical data from CamelCamelCamel)
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1529.00,
        "Variable",
        1,
        "Amazon 3rd Party",
        "EU",
        "Current",
        "https://fr.camelcamelcamel.com/product/B0C2KNGV5L",
        "Resale_Business",
        "€1,435.27 current 3rd party price",
    ],
    [
        "NVIDIA RTX 4000 SFF Ada",
        "Used",
        1466.12,
        "Variable",
        1,
        "Amazon 3rd Party",
        "EU",
        "Recent",
        "https://fr.camelcamelcamel.com/product/B0C2KNGV5L",
        "Resale_Business",
        "€1,377.90 average used price",
    ],
    # Enterprise/OEM Sources
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        1999.00,
        "Available",
        1,
        "SHI",
        "US",
        "Current",
        "https://www.shi.com/product/46030307/NVIDIA-RTX-4000-SFF-Ada-Generation",
        "Retail_Specialist",
        "MSRP listed",
    ],
    # Out of Stock Sources
    [
        "NVIDIA RTX 4000 SFF Ada",
        "New",
        0,
        "Out of Stock",
        0,
        "WiredZone",
        "US",
        "Current",
        "https://www.wiredzone.com/shop/product/10029700-nvidia-900-5g192-2270-000-rtx4000-sff-ada-generation-20gb-memory-active-cooling-12766",
        "Retail_Specialist",
        "Out of stock - SFF version",
    ],
]

# Create DataFrame
columns = [
    "Model",
    "Condition",
    "Price_USD",
    "Quantity",
    "Min_Order_Qty",
    "Seller",
    "Geographic_Region",
    "Listing_Age",
    "Source_URL",
    "Source_Type",
    "Bulk_Notes",
]
df = pd.DataFrame(pricing_data, columns=columns)

# Sort by price for better analysis
df_sorted = df.sort_values("Price_USD")

# Display the data
print("NVIDIA RTX 4000 Ada SFF Pricing Data Summary:")
print("=" * 60)
print(f"Total listings found: {len(df)}")
print(f"Price range: ${df[df['Price_USD'] > 0]['Price_USD'].min():.2f} - ${df['Price_USD'].max():.2f}")
print(f"Average price (excluding $0): ${df[df['Price_USD'] > 0]['Price_USD'].mean():.2f}")
print(f"Median price (excluding $0): ${df[df['Price_USD'] > 0]['Price_USD'].median():.2f}")
print()

print("Stock Status Summary:")
stock_summary = df["Quantity"].value_counts()
print(stock_summary)
print()

print("Source Type Distribution:")
source_summary = df["Source_Type"].value_counts()
print(source_summary)
print()

print("Geographic Distribution:")
geo_summary = df["Geographic_Region"].value_counts()
print(geo_summary)
print()

# Save to CSV
df_sorted.to_csv("nvidia_rtx_4000_sff_ada_pricing.csv", index=False)
print("Data saved to 'nvidia_rtx_4000_sff_ada_pricing.csv'")
print()

# Display the first 10 rows
print("Sample of collected data (first 10 rows):")
print(df_sorted.head(10).to_string(index=False))
