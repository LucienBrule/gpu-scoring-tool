import pandas as pd

# Let's compile all the GPU data we've gathered into a comprehensive dataset
gpu_data = {
    "Card_Name": [
        "RTX 6000 Ada",
        "RTX 5000 Ada",
        "RTX 4500 Ada",
        "RTX 4000 Ada SFF",
        "RTX A6000",
        "RTX A5500",
        "RTX A5000",
        "RTX A4500",
        "RTX A4000",
        "RTX A2000 12GB",
        "RTX A2000 6GB",
        "L40S",
        "L40",
        "A800 40GB",
        "A40",
        "H100 PCIe 80GB",
        "H800 PCIe 80GB",
        "T1000 8GB",
        "T1000 4GB",
        "T600",
        "T400",
        "L4",
        "A2",
        "RTX 4090",
        "RTX 5090",
        # Upcoming Blackwell Pro cards (estimated/announced specs)
        "RTX PRO 6000 Blackwell",
        "RTX PRO 5000 Blackwell",
        "RTX PRO 4500 Blackwell",
        "RTX PRO 4000 Blackwell",
    ],
    "Current_Retail_Price_USD": [
        7200,
        6650,
        2350,
        1250,  # Ada series current prices
        4950,
        2500,
        2400,
        1800,
        1000,
        620,
        560,  # Ampere A series
        15000,
        12000,
        20000,
        4500,
        30000,
        30000,  # Data center cards
        280,
        250,
        150,
        120,
        3500,
        2800,  # Entry level/edge cards
        1650,
        2000,  # Consumer cards accepted
        8900,
        6000,
        4000,
        2500,  # Upcoming Blackwell Pro (estimated)
    ],
    "VRAM_GB": [
        48,
        32,
        24,
        20,  # Ada series
        48,
        24,
        24,
        20,
        16,
        12,
        6,  # Ampere A series
        48,
        48,
        40,
        48,
        80,
        80,  # Data center
        8,
        4,
        4,
        2,
        24,
        16,  # Entry level
        24,
        32,  # Consumer
        96,
        48,
        32,
        24,  # Blackwell Pro
    ],
    "MIG_Support": [
        4,
        4,
        4,
        4,  # Ada series (4 instances each)
        0,
        0,
        0,
        0,
        0,
        0,
        0,  # Ampere A series (no MIG except A100-based)
        7,
        7,
        7,
        7,
        7,
        7,  # Data center cards
        0,
        0,
        0,
        0,
        7,
        7,  # Entry level (L4 and A2 have MIG)
        0,
        0,  # Consumer
        4,
        4,
        4,
        4,  # Blackwell Pro (expected 4 instances)
    ],
    "TDP_Watts": [
        300,
        250,
        210,
        70,  # Ada series
        300,
        230,
        230,
        200,
        140,
        70,
        70,  # Ampere A series
        350,
        300,
        300,
        300,
        350,
        350,  # Data center
        50,
        50,
        40,
        30,
        72,
        60,  # Entry level
        450,
        575,  # Consumer
        400,
        320,
        250,
        180,  # Blackwell Pro (estimated)
    ],
    "Slot_Width": [
        2,
        2,
        2,
        2,  # Ada series
        2,
        2,
        2,
        2,
        1,
        2,
        2,  # Ampere A series (A4000 is single slot)
        2,
        1,
        2,
        2,
        2,
        2,  # Data center (L40 is single slot)
        1,
        1,
        1,
        1,
        1,
        1,  # Entry level (all single slot)
        3,
        2,  # Consumer (4090 is 3-slot, 5090 is 2-slot)
        2,
        2,
        2,
        2,  # Blackwell Pro
    ],
    "NVLink_Support": [
        1,
        0,
        0,
        0,  # Ada series (only RTX 6000 Ada has NVLink)
        1,
        1,
        1,
        1,
        0,
        0,
        0,  # Ampere A series (A6000 down to A4500 have NVLink)
        0,
        0,
        1,
        0,
        0,
        0,  # Data center (A800 has NVLink, others PCIe only)
        0,
        0,
        0,
        0,
        0,
        0,  # Entry level
        0,
        0,  # Consumer
        1,
        0,
        0,
        0,  # Blackwell Pro (only top card has NVLink)
    ],
    "CUDA_Cores": [
        18176,
        12800,
        7680,
        6144,  # Ada series
        10752,
        7424,
        8192,
        7168,
        6144,
        3328,
        3328,  # Ampere A series
        18176,
        18176,
        10752,
        10752,
        16896,
        14592,  # Data center
        896,
        896,
        640,
        512,
        7680,
        3584,  # Entry level
        16384,
        21760,  # Consumer
        20480,
        15360,
        10240,
        7680,  # Blackwell Pro (estimated)
    ],
    "Generation": [
        "Ada",
        "Ada",
        "Ada",
        "Ada",
        "Ampere",
        "Ampere",
        "Ampere",
        "Ampere",
        "Ampere",
        "Ampere",
        "Ampere",
        "Ada",
        "Ada",
        "Ampere",
        "Ampere",
        "Hopper",
        "Hopper",
        "Turing",
        "Turing",
        "Turing",
        "Turing",
        "Ada",
        "Ampere",
        "Ada",
        "Blackwell",
        "Blackwell",
        "Blackwell",
        "Blackwell",
        "Blackwell",
    ],
    "PCIe_Generation": [
        4,
        4,
        4,
        4,  # Ada series
        4,
        4,
        4,
        4,
        4,
        4,
        4,  # Ampere A series
        4,
        4,
        4,
        4,
        5,
        5,  # Data center (H100/H800 are PCIe 5)
        3,
        3,
        3,
        3,
        4,
        4,  # Entry level
        4,
        5,  # Consumer (5090 is PCIe 5)
        5,
        5,
        5,
        5,  # Blackwell Pro
    ],
}

# Create DataFrame
df = pd.DataFrame(gpu_data)
print("GPU Database created with", len(df), "cards")
print("\nFirst few rows:")
print(df.head())

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe())
