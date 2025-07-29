import numpy as np
import pandas as pd

# Create comprehensive pricing data for NVIDIA H100 PCIe 80GB based on collected research
pricing_data = []

# Add retail specialist sources
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 34995,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "ServerSupply.com",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.serversupply.com/GPU/HBM2E/80GB/NVIDIA/900-21010-0000-000_387928.htm",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Standard enterprise pricing",
    }
)

pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 29500,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "Newegg (PNY)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.newegg.com/p/pl?d=h100",
        "Source_Type": "Retail_Major",
        "Bulk_Notes": "PNY branded model NVH100TCGPU-KIT",
    }
)

pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 39879,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "High Performance Tech (Newegg)",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Recent: <7 days",
        "Source_URL": "https://www.newegg.com/p/1VK-0066-00022",
        "Source_Type": "Resale_Business",
        "Bulk_Notes": "Third-party seller on Newegg marketplace",
    }
)

# Add enterprise/specialist sources
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": "Contact for Quote",
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "CDW",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.cdw.com/product/pny-nvidia-h100-graphic-card-80-gb-hbm3/7367181",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Enterprise pricing available on request",
    }
)

pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": "Contact for Quote",
        "Quantity": "Not in stock",
        "Min_Order_Qty": 1,
        "Seller": "WiredZone",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.wiredzone.com/shop/product/10025500-nvidia-900-21010-0000-000-graphics-processing-unit-gpu-h100-80gb-hbm2e-memory-fhfl-10753",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Needs approval before purchase",
    }
)

pricing_data.append(
    {
        "Model": "NVIDIA H100 NVL 94GB",
        "Condition": "New",
        "Price_USD": "Contact for Quote",
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "Provantage",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.provantage.com/pny-technologies-nvh100nvltcgpu-kit~7PNY92MT.htm",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Needs approval before purchase",
    }
)

# Add resale/individual sources
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New/Sealed",
        "Price_USD": 24000,
        "Quantity": 1,
        "Min_Order_Qty": 1,
        "Seller": "Individual (Reddit r/hardwareswap)",
        "Geographic_Region": "US domestic (NYC)",
        "Listing_Age": "Recent: <7 days",
        "Source_URL": "https://www.reddit.com/r/hardwareswap/comments/1ifkbr4/usany_h_nvidia_h100_80gb_pcie_w_local_cash/",
        "Source_Type": "Resale_Individual",
        "Bulk_Notes": "OBO - willing to travel in USA, local cash preferred",
    }
)

# Add international sources
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 36000,
        "Quantity": "Pre-order",
        "Min_Order_Qty": 1,
        "Seller": "G-Dep (Japan)",
        "Geographic_Region": "Asia/Japan",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "Referenced in PC Gamer article",
        "Source_Type": "International",
        "Bulk_Notes": "Japanese retailer, 4,745,950 yen (~$36,000",
    }
)

# Add Alibaba sources
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 23800,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "Alibaba Supplier",
        "Geographic_Region": "Asia/China",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.alibaba.com/showroom/nvidia-h100-80gb-gpu.html",
        "Source_Type": "International",
        "Bulk_Notes": "High Performance H-100 PCIe 80GB, 3 years warranty",
    }
)

pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB",
        "Condition": "New",
        "Price_USD": 49999,
        "Quantity": "Available",
        "Min_Order_Qty": 1,
        "Seller": "Shenzhen Jiechuang (Alibaba)",
        "Geographic_Region": "Asia/China",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.alibaba.com/product-detail/High-Quality-Computing-Graphic-Card-80GB_1600969217202.html",
        "Source_Type": "International",
        "Bulk_Notes": "Volume pricing: 1-4 pcs $49,999, 5-99 pcs $45,666, 100+ pcs $39,999",
    }
)

# Add system configurations showing individual GPU pricing
pricing_data.append(
    {
        "Model": "NVIDIA H100 PCIe 80GB (8-GPU system)",
        "Condition": "New",
        "Price_USD": 325000,
        "Quantity": "Out of Stock",
        "Min_Order_Qty": 1,
        "Seller": "Tyan/Newegg",
        "Geographic_Region": "US domestic",
        "Listing_Age": "Current: 7-30 days",
        "Source_URL": "https://www.newegg.com/p/pl?d=h100",
        "Source_Type": "Retail_Specialist",
        "Bulk_Notes": "Complete 8-GPU system (~$40,625 per GPU)",
    }
)

# Create DataFrame
df = pd.DataFrame(pricing_data)

print("NVIDIA H100 PCIe 80GB Pricing Analysis")
print("=" * 50)
print(f"Total listings found: {len(df)}")
print(f"Sources analyzed: {df['Source_Type'].nunique()} different source types")
print(f"Geographic regions covered: {df['Geographic_Region'].nunique()}")

# Display the CSV format
print("\nFormatted CSV Data:")
print("=" * 50)
df.to_csv("h100_pricing_data.csv", index=False)
print(df.to_csv(index=False))

# Analysis of pricing ranges
numeric_prices = []
for price in df["Price_USD"]:
    if isinstance(price, (int, float)):
        numeric_prices.append(price)
    elif price == 325000:  # 8-GPU system
        numeric_prices.append(price / 8)  # Per GPU estimate

if numeric_prices:
    print("\nPricing Analysis:")
    print(f"Minimum price found: ${min(numeric_prices):,.2f}")
    print(f"Maximum price found: ${max(numeric_prices):,.2f}")
    print(f"Average price: ${np.mean(numeric_prices):,.2f}")
    print(f"Median price: ${np.median(numeric_prices):,.2f}")
