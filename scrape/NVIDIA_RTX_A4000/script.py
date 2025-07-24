import pandas as pd
from datetime import datetime

# Compile all the pricing data I've gathered from the searches
rtx_a4000_data = [
    # Retail Major
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1149.99, "Quantity": "unknown", "Min_Order_Qty": 1, 
     "Seller": "B&H Photo", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.bhphotovideo.com/c/product/1644218-REG/pny_technologies_vcnrtxa4000_pb_nvidia_rtx_a4000_graphics.html", 
     "Source_Type": "Retail_Major", "Bulk_Notes": "Back-ordered, expected availability May 02, 2025"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1295.00, "Quantity": "unknown", "Min_Order_Qty": 1, 
     "Seller": "Newegg (Tech Trends)", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.newegg.com/pny-technologies-inc-vcnrtxa4000-pb-rtx-a4000-16gb-graphics-card/p/N82E16814132091", 
     "Source_Type": "Retail_Major", "Bulk_Notes": "In stock"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 691.19, "Quantity": 0, "Min_Order_Qty": 1, 
     "Seller": "Micro Center", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.microcenter.com/product/652306/pny-nvidia-rtx-a4000-single-fan-16gb-gddr6-pcie-40-graphics-card", 
     "Source_Type": "Retail_Major", "Bulk_Notes": "Not Available - Out of Stock"},
    
    # Retail Specialist
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1230.99, "Quantity": "unknown", "Min_Order_Qty": 1, 
     "Seller": "Zones.com", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.zones.com/site/product/index.html?id=109402324", 
     "Source_Type": "Retail_Specialist", "Bulk_Notes": "Enterprise pricing available"},
    
    {"Model": "RTX A4000", "Condition": "out of stock", "Price_USD": 0, "Quantity": 0, "Min_Order_Qty": 1, 
     "Seller": "Supermicro", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://store.supermicro.com/us_en/supermicro-nvidia-rtx-a4000-16gb-gddr6-graphics-card-gpu-nvqrtx-a4000.html", 
     "Source_Type": "Retail_Specialist", "Bulk_Notes": "Out of stock"},
    
    # Resale Individual (eBay individual sellers)
    {"Model": "RTX A4000", "Condition": "used", "Price_USD": 535, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "rburla (eBay Canada)", "Geographic_Region": "Canada", "Listing_Age": "Recent", 
     "Source_URL": "https://www.ebay.ca/itm/375373064015", 
     "Source_Type": "Resale_Individual", "Bulk_Notes": "SOLD listing - C$727.00"},
    
    {"Model": "RTX A4000", "Condition": "used", "Price_USD": 550, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "eBay Individual", "Geographic_Region": "Canada", "Listing_Age": "Recent", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "Resale_Individual", "Bulk_Notes": "C$750.00 or Best Offer"},
    
    {"Model": "RTX A4000", "Condition": "used", "Price_USD": 785, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "OfferUp Gastonia NC", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://offerup.com/item/detail/57292b4a-bd29-3a68-8c3c-0e5f348846f0", 
     "Source_Type": "Resale_Individual", "Bulk_Notes": "Local pickup only"},
    
    {"Model": "RTX A4000", "Condition": "used", "Price_USD": 615, "Quantity": 2, "Min_Order_Qty": 1, 
     "Seller": "Dell (Reddit HardwareSwap)", "Geographic_Region": "US domestic", "Listing_Age": "Recent", 
     "Source_URL": "https://www.reddit.com/r/hardwareswap/comments/1ix0bmh/usamah_nvidia_quado_rtx_a4000_16gb_gddr6_pcie/", 
     "Source_Type": "Resale_Individual", "Bulk_Notes": "Dell P/N: 0HGP0F, Boston MA"},
    
    # Resale Business (eBay stores)
    {"Model": "RTX A4000", "Condition": "refurbished", "Price_USD": 739.97, "Quantity": 9, "Min_Order_Qty": 1, 
     "Seller": "ReSpec.io Store (eBay)", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/itm/156035032609", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "Professionally renewed, 1yr warranty, 418 sold"},
    
    {"Model": "RTX A4000", "Condition": "refurbished", "Price_USD": 735, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "HP Refurbished (eBay)", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "C$999.37, 6 sold"},
    
    {"Model": "RTX A4000", "Condition": "refurbished", "Price_USD": 750, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "Newegg Refurbished", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.newegg.com/p/1FT-000P-005P8", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "Tech Trends seller, $828.99"},
    
    {"Model": "RTX A4000", "Condition": "refurbished", "Price_USD": 1019.78, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "eBay Business Seller", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "C$1,019.78, 7 sold"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 933, "Quantity": 4, "Min_Order_Qty": 1, 
     "Seller": "Lenovo (eBay)", "Geographic_Region": "Canada", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "C$1,269.00, 15% off original price"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1000, "Quantity": 1, "Min_Order_Qty": 1, 
     "Seller": "eBay Sealed Box", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "Resale_Business", "Bulk_Notes": "C$1,358.34 or Best Offer, sealed box"},
    
    # International (Alibaba, HK resellers)
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1095.00, "Quantity": 20, "Min_Order_Qty": 1, 
     "Seller": "mujitech3 (eBay China)", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.co.uk/itm/374527189182", 
     "Source_Type": "International", "Bulk_Notes": "New, never used, Chinese seller"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1360, "Quantity": "unknown", "Min_Order_Qty": 1, 
     "Seller": "China eBay Seller", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://www.ebay.ca/sch/i.html?_nkw=rtx+a4000", 
     "Source_Type": "International", "Bulk_Notes": "C$1,849.19, from China"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 720, "Quantity": "1+", "Min_Order_Qty": 1, 
     "Seller": "Alibaba Seller 1", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://www.alibaba.com/showroom/a4000.html", 
     "Source_Type": "International", "Bulk_Notes": "$720-729 range"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 790, "Quantity": "1+", "Min_Order_Qty": 1, 
     "Seller": "Alibaba Seller 2", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://www.alibaba.com/showroom/rtx-a400.html", 
     "Source_Type": "International", "Bulk_Notes": "$790-920 range"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 900, "Quantity": "1+", "Min_Order_Qty": 1, 
     "Seller": "Alibaba Seller 3", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://chinese.alibaba.com/g/rtx-a4000-price.html", 
     "Source_Type": "International", "Bulk_Notes": "$900-935 range"},
    
    {"Model": "RTX A4000", "Condition": "used", "Price_USD": 450, "Quantity": "1+", "Min_Order_Qty": 1, 
     "Seller": "Alibaba Seller 4", "Geographic_Region": "Asia/HK", "Listing_Age": "Current", 
     "Source_URL": "https://chinese.alibaba.com/g/rtx-a4000-price.html", 
     "Source_Type": "International", "Bulk_Notes": "$458-833 range, mixed A2000/A4000"},
    
    # EU Sources
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1140, "Quantity": "few", "Min_Order_Qty": 1, 
     "Seller": "Computer Universe", "Geographic_Region": "EU", "Listing_Age": "Current", 
     "Source_URL": "https://www.computeruniverse.net/en/p/2E17-06M", 
     "Source_Type": "International", "Bulk_Notes": "€1,097.00, Germany, in stock"},
    
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 400, "Quantity": "3+", "Min_Order_Qty": 3, 
     "Seller": "Eurolots Wholesale", "Geographic_Region": "EU", "Listing_Age": "Current", 
     "Source_URL": "https://www.blog.eurolots.com/wholesale-video-cards", 
     "Source_Type": "Liquidation", "Bulk_Notes": "€400.00 VAT Excl., wholesale pricing, min 3 pieces"},
    
    # Price aggregators
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 944.00, "Quantity": "in stock", "Min_Order_Qty": 1, 
     "Seller": "Pangoly Aggregator", "Geographic_Region": "US domestic", "Listing_Age": "Current", 
     "Source_URL": "https://pangoly.com/en/price-history/pny-nvidia-rtx-a4000", 
     "Source_Type": "Retail_Specialist", "Bulk_Notes": "Used from $689.99"},
    
    # Router-Switch.com
    {"Model": "RTX A4000", "Condition": "new", "Price_USD": 1049.00, "Quantity": "in stock", "Min_Order_Qty": 1, 
     "Seller": "Router-Switch.com", "Geographic_Region": "International", "Listing_Age": "Current", 
     "Source_URL": "https://www.router-switch.com/fr/nvidia-rtx-a4000.html", 
     "Source_Type": "Retail_Specialist", "Bulk_Notes": "Global warehouses, bulk savings available"},
]

# Create DataFrame
df = pd.DataFrame(rtx_a4000_data)

# Display the data
print("RTX A4000 Pricing Data Compilation:")
print("=" * 80)
print(f"Total listings found: {len(df)}")
print(f"Price range: ${df[df['Price_USD'] > 0]['Price_USD'].min():.2f} - ${df['Price_USD'].max():.2f}")
print(f"Average price (excl. $0): ${df[df['Price_USD'] > 0]['Price_USD'].mean():.2f}")
print(f"Median price (excl. $0): ${df[df['Price_USD'] > 0]['Price_USD'].median():.2f}")
print("\nPrice by condition:")
condition_stats = df[df['Price_USD'] > 0].groupby('Condition')['Price_USD'].agg(['count', 'mean', 'min', 'max']).round(2)
print(condition_stats)

print("\nSource type distribution:")
source_stats = df.groupby('Source_Type').size()
print(source_stats)

# Save to CSV
df.to_csv('rtx_a4000_pricing_data.csv', index=False)
print(f"\nData saved to rtx_a4000_pricing_data.csv")

# Display first few rows to verify format
print("\nFirst 5 rows of data:")
print(df.head())