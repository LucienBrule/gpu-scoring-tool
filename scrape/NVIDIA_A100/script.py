import pandas as pd

# Create the CSV data based on the previous conversation
data = [
    [
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
    ],
    [
        "NVIDIA Tesla 100 40GB PCIe",
        "New",
        "15398.90",
        "10",
        "1",
        "Lucky-PLC Store",
        "Asia (Shenzhen, CN)",
        "Stale",
        "https://www.ebay.co.uk/itm/386415154179",
        "Resale_Business",
        "—",
    ],
    [
        "NVIDIA A100 900-21001-0000-000 40GB PCIe",
        "New",
        "18999.99",
        "—",
        "1",
        "High Performance Tech (Newegg)",
        "International (ship from CN)",
        "Current",
        "https://www.newegg.com/nvidia-900-21001-0000-000-a100-40gb-graphics-card/p/N82E16814132090",
        "Retail_Major",
        "Free shipping; seller rating 4★",
    ],
    [
        "HPE R6B53A NVIDIA A100 40GB PCIe",
        "Refurbished",
        "22350.00",
        "—",
        "1",
        "ServerSupply",
        "US Domestic",
        "Current",
        "https://www.serversupply.com/NETWORKING/EXPANSION%20MODULE/APPLICATION%20ACCELERATOR/HPE/R6B53A_343787.htm",
        "Retail_Specialist",
        "90-day warranty",
    ],
    [
        "NVIDIA A100 40GB HBM2 PCIe 4.0 GPU",
        "Refurbished",
        "12000.00",
        "—",
        "1",
        "UnixSurplus",
        "US Domestic",
        "Recent",
        "https://unixsurplus.com/Nvidia-A100-40GB-Memory",
        "Retail_Specialist",
        "Ships in 2 business days",
    ],
    [
        "NVIDIA TESLA A100 Tensor Core 40GB GPU Server",
        "Used",
        "15859.00",
        "2",
        "1",
        "CTOServers",
        "EU (UK)",
        "Recent",
        "https://www.ebay.co.uk/itm/276787452070",
        "Resale_Business",
        "Includes HPE Gen10 carrier",
    ],
    [
        "NVIDIA A100 40GB PCIe OEM GA100-884",
        "New",
        "27589.26",
        "10",
        "1",
        "yudr3m",
        "Canada",
        "Current",
        "https://www.ebay.ca/itm/167577727473",
        "Resale_Individual",
        "Price ≈40% above typical – possible premium/rarity",
    ],
]

# Create a DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Save to CSV file
filename = "nvidia-a100-40gb-pcie-pricing.csv"
df.to_csv(filename, index=False)

print(f"CSV file '{filename}' has been created successfully!")
print(f"\nFile contains {len(df)} pricing records for NVIDIA A100 40GB PCIe GPU")
print("\nFirst few rows of the data:")
print(df.head())
