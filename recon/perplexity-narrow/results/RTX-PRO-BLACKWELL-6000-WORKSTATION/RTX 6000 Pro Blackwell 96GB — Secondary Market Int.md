<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# RTX 6000 Pro Blackwell 96GB — Secondary Market Intelligence Report

Current market data shows **significant availability shortage** with **secondary market premiums** ranging from **4.9% to 11.0%** over retail pricing. The RTX Pro 6000 Blackwell workstation variant has emerged as the dominant offering in secondary markets, commanding median prices of **\$9,434** compared to server edition premiums reaching **\$10,650**.

## Summary Bullets

- **Limited secondary market volume**: Only 28 documented sales across 90-day period, indicating extreme supply constraints
- **Price stabilization**: Recent 14-day median of \$8,750 shows downward trend from June peak of \$10,565
- **Workstation dominance**: 86% of secondary sales are workstation edition; server editions command 13% premium
- **Regional arbitrage**: China-based listings average \$1,319 premium over US domestic sales
- **Seller concentration**: 7 sellers account for 50% of multi-unit sales, suggesting limited distribution channels
- **Performance value**: \$98.77/GB VRAM and \$81.04/TFLOPS FP32 in secondary markets vs. \$88.54/GB retail

![RTX Pro 6000 Blackwell Secondary Market Analysis - Pricing Trends, Variants, and Performance Metrics](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/c13655cb196b3a6aa7c04c24fcc1d348/1de7233e-e55c-401f-b8d6-35d138f39855/2c5673b4.png)

RTX Pro 6000 Blackwell Secondary Market Analysis - Pricing Trends, Variants, and Performance Metrics

## Active Listings \& Sold Comparisons

### Recent Sales Data (Last 90 Days)

| Date | Variant | Condition | Price (USD) | Seller Feedback | Location | Notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 2025-08-16 | Workstation | Brand New | \$8,699.95 | 99.6% (9.7K) | US | OEM packaging, 2-day shipping |
| 2025-08-12 | Server | Open Box | \$11,599.00 | 100% (8) | China | AI GPU targeting, free shipping |
| 2025-08-06 | Server | Brand New | \$11,800.00 | 97.3% (8K) | China | Highest recorded sale price |
| 2025-07-31 | Workstation | Brand New | \$8,599.99 | 100% (188) | US | Lowest new condition price |
| 2025-06-02 | Workstation | Brand New | \$10,565.00 | 100% (158) | US | Peak secondary market pricing |

### Pricing Statistics

**Overall Market (28 sales)**

- Mean: \$9,546.29 | Median: \$9,481.48
- Range: \$8,599.99 - \$11,800.00
- Standard Deviation: \$796.78

**By Variant**

- **Workstation** (24 units): Mean \$9,387.38 | Median \$9,434.47
- **Server** (4 units): Mean \$10,499.75 | Median \$10,649.50

**By Condition**

- **Brand New** (24 units): Mean \$9,489.82 | Range \$8,599.99-\$11,800.00
- **Pre-Owned** (3 units): Mean \$9,313.85 | Range \$8,620.60-\$9,920.96
- **Open Box** (1 unit): \$11,599.00


## Specifications \& Performance Metrics

### Target GPU Technical Specifications

| Specification | RTX Pro 6000 Blackwell |
| :-- | :-- |
| **Architecture** | NVIDIA Blackwell (GB202) |
| **CUDA Cores** | 24,064 |
| **Tensor Cores** | 752 (5th Gen) |
| **RT Cores** | 188 (4th Gen) |
| **VRAM** | 96GB GDDR7 with ECC |
| **Memory Bus** | 512-bit |
| **Memory Bandwidth** | 1,597 GB/s |
| **FP32 Performance** | 117 TFLOPS |
| **FP4 AI Performance** | 3.7 PFLOPS |
| **PCIe Interface** | PCIe 5.0 x16 |
| **NVLink Support** | **No** (PCIe-only architecture) |
| **MIG Support** | Up to 4 instances @ 24GB each |

### Variant Distinctions

**Workstation Edition (600W)**

- Form factor: 5.4" H x 12" L, dual-slot
- Cooling: Double flow-through (active)
- Target: Desktop workstations
- Power connector: 1x PCIe CEM5 16-pin

**Max-Q Workstation Edition (300W)**

- Form factor: 4.4" H x 10.5" L, dual-slot
- Cooling: Blower-style (active)
- Target: Multi-GPU, dense configurations
- 50% power reduction for thermal efficiency

**Server Edition (400-600W configurable)**

- Form factor: 4.4" H x 10.5" L, dual-slot
- Cooling: Passive (requires chassis airflow)
- Target: Data center deployment
- Optimized for server rack environments


## Performance Cost Analysis

### \$/Performance Metrics (Secondary Market Median)

- **\$/GB VRAM**: \$98.77 (96GB total capacity)
- **\$/TFLOPS FP32**: \$81.04 (117 TFLOPS capability)
- **\$/TFLOPS FP4**: \$2.56 (3,700 TFLOPS FP4 AI)


### Retail vs. Secondary Market Comparison

| Retailer | Variant | Retail Price | Secondary Premium |
| :-- | :-- | :-- | :-- |
| Central Computer | Server | \$8,499.99 | **+11.0%** |
| Newegg | Workstation | \$8,995.99 | **+4.9%** |
| C3Aero | Workstation | \$10,899.00 | **-13.4%** |
| Hyperscalers | Server | \$11,605.00 | **-18.7%** |

**Secondary market shows mixed premium/discount** depending on variant and retailer positioning. Workstation edition secondary prices align closely with mid-tier retail, while server edition commands significant premiums in secondary channels.

## Integrated Systems Valuation

### Dell Precision Systems Analysis

**Dell Precision 7875 Tower** (Single RTX 6000 Ada)

- Configuration: AMD Pro 7945WX, 128GB RAM, 2.5TB NVMe
- Sale Price: \$6,449.99 (Pre-owned)
- System Base Value: \$5,604 (excluding GPU)
- **Implied GPU Value: \$845.99** (79.9% discount vs. standalone)

**Dell Precision 7875 Tower** (Dual RTX 6000 Ada)

- Configuration: Threadripper PRO 7975WX, 512GB RAM, 8TB NVMe
- Sale Price: \$18,497.64 (Pre-owned)
- System Base Value: \$10,896 (excluding GPUs)
- **Implied GPU Value: \$3,800.82 each** (9.5% discount vs. standalone)


### Supermicro Enterprise Integration

**20+ Validated Configurations** available with RTX Pro 6000 Blackwell:

**SYS-212GB-NR (MGX Reference Design)**

- Single-socket edge AI system
- Up to 4x RTX Pro 6000 Blackwell GPUs
- Power-optimized for edge deployment

**5U PCIe Accelerated Systems**

- Dual-socket server architecture
- Up to 8x RTX Pro 6000 Blackwell GPUs
- Data center AI and rendering workloads


## Risk \& Credibility Assessment

### Seller Analysis

**High-Volume Sellers** (Multiple sales):

- **novatechdirect**: 3 sales, 97.3% feedback, \$9,232 average
- **bonez5xtb**: 2 sales, 100% feedback, \$10,057 average
- **tesserae_pcs**: 2 sales, 100% feedback, \$9,374 average


### Risk Factors Identified

**Supply Chain Risks**

- **Limited availability**: 28 total sales across 90 days globally
- **Regional concentration**: 93% of sales from US-based sellers
- **High seller concentration**: Top 7 sellers control 50% of volume

**Authenticity Concerns**

- **No obvious counterfeits detected** in analyzed listings
- **OEM vs. retail packaging** variations noted
- **Engineering samples**: No ES/QS variants identified in dataset

**Import/Export Considerations**

- **China premium**: \$1,319 average markup over US pricing
- **VAT implications**: UK listings show equivalent pricing pressure
- **Warranty concerns**: International purchases may void coverage


## Market Outlook \& Availability

### Current Supply Constraints

- **Severe shortage indicators**: <1 unit/day average sales velocity
- **Retail backorders**: Multiple "out of stock" notifications at major retailers
- **Lead times**: 2-6 week delivery quoted by active sellers


### Price Trajectory Analysis

- **Peak pricing**: June 2025 (\$10,565 maximum)
- **Current stabilization**: August 2025 (\$8,700-\$8,750 range)
- **Downward pressure**: Recent 14-day median 13% below peak


## Confusions Resolved

### Ada vs. Blackwell Clarification

- **RTX 6000 Ada**: 48GB GDDR6, older generation, ~\$4,200 secondary market
- **RTX Pro 6000 Blackwell**: 96GB GDDR7, current generation, ~\$9,400 secondary market
- **No cross-compatibility** between generations for accessories/cooling


### SXM vs. PCIe Architecture

- **RTX Pro 6000 Blackwell**: PCIe-only design, **no SXM variant available**
- **No NVLink support**: Multi-GPU configurations rely on PCIe bandwidth only
- **No conversion cards needed**: Direct PCIe 5.0 installation (backward compatible with PCIe 4.0)


### Workstation vs. Server Variants

- **Same silicon**: All variants use identical GB202 die configuration
- **Power scaling**: 300W (Max-Q) vs. 600W (Workstation/Server)
- **Cooling differences**: Active vs. passive thermal solutions
- **No performance hardware differences**: Same CUDA/Tensor/RT core counts


## Limitations \& Assumptions

### Data Coverage Gaps

- **eBay focus**: Limited coverage of other secondary platforms (Facebook Marketplace, Craigslist)
- **Enterprise channels**: No visibility into B2B/OEM direct sales
- **International markets**: Limited data from EU/APAC secondary markets


### Verification Limitations

- **Photo verification**: Unable to confirm VRAM capacity from listing images
- **Seller reliability**: Feedback scores may not reflect GPU-specific experience
- **Condition accuracy**: Pre-owned condition assessments vary by seller standards


### Market Timing Considerations

- **Seasonal effects**: Analysis spans summer months, may not reflect Q4/Q1 enterprise budget cycles
- **Technology cycle**: Positioned early in Blackwell generation lifecycle
- **Competition impact**: AMD and Intel next-gen releases may affect pricing dynamics

The RTX Pro 6000 Blackwell secondary market demonstrates characteristics of a **supply-constrained, high-value professional GPU** with **limited distribution channels** and **significant regional pricing variations**. Current secondary market pricing suggests **sustainable demand at \$8,500-\$9,500 range** for workstation variants, with server editions commanding premiums justified by enterprise deployment requirements.

<div style="text-align: center">⁂</div>

[^1]: https://www.tomshardware.com/pc-components/gpus/nvidia-rtx-pro-6000-blackwell-appears-online-with-an-eye-watering-price-tag-of-over-usd11-000

[^2]: https://www.centralcomputer.com/nvidia-rtx-pro-6000-96gb-blackwell-server-edition-gddr6-24064-cuda-cores-pci-express-5-0-x16-600w-blackwell-workstation.html

[^3]: https://finance.yahoo.com/news/nvidia-rtx-pro-6000d-b40-130753186.html

[^4]: https://www.reddit.com/r/LocalLLaMA/comments/1j6nct7/estimating_how_much_the_new_nvidia_rtx_pro_6000/

[^5]: https://www.newegg.com/p/N82E16888892011

[^6]: https://www.tomshardware.com/pc-components/gpus/nvidias-rtx-blackwell-workstation-gpu-spotted-with-96gb-gddr7-proviz-gpu-with-a-512-bit-bus

[^7]: https://boxx.com/nvidia-rtx-pro

[^8]: https://www.nvidia.com/en-us/data-center/rtx-pro-6000-blackwell-server-edition/

[^9]: https://www.pny.com/nvidia-rtx-pro-6000-blackwell-ws

[^10]: https://www.exxactcorp.com/blog/hpc/comparing-nvidia-tensor-core-gpus

[^11]: https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000-family/

[^12]: https://www.dell.com/en-us/shop/nvidia-rtx-pro-6000-blackwell-600w/apd/ad368558/graphic-video-cards

[^13]: https://www.reddit.com/r/hardware/comments/1kf8czv/nvidia_rtx_pro_6000_blackwell_gpus_now_available/

[^14]: https://www.ebay.co.uk/itm/187326516645

[^15]: https://store.supermicro.com/us_en/supermicro-rtx-pro-6000-gpu-nvrtxpro-6k-b-se.html

[^16]: https://www.techradar.com/pro/nvidias-most-expensive-blackwell-card-gets-massive-price-cut-but-it-is-not-the-rtx-5090

[^17]: https://www.ebay.com.au/itm/365693961885

[^18]: https://hothardware.com/news/nvidia-rtx-pro-6000-blackwell-cards-96gb-gddr7-listed-8k

[^19]: https://c3aero.com/products/nvidia-rtx-pro-6000-blackwell-workstation-edition

[^20]: https://www.ebay.co.uk/itm/277286426701

[^21]: https://www.youtube.com/watch?v=ZCvjw8B6rcg

[^22]: https://www.tomshardware.com/pc-components/gpus/nvidia-rtx-pro-6000-blackwell-gpu-is-listed-for-usd8-565-at-us-retailer-26-percent-more-expensive-than-the-last-gen-rtx-6000-ada

[^23]: https://www.ebay.ca/sch/i.html?_nkw=rtx+6000\&Brand=\&_dcat=179

[^24]: https://www.reddit.com/r/nvidia/comments/1j6s3x5/nvidia_rtx_pro_6000_blackwell_leaked_24064_cores/

[^25]: https://www.reddit.com/r/LocalLLaMA/comments/1jgnye9/rtx_pro_blackwell_pricing_listed/

[^26]: https://www.ebay.co.uk/itm/297446583707

[^27]: https://www.youtube.com/watch?v=WUw9XUOAFaY

[^28]: https://www.ebay.de/itm/116697630002

[^29]: https://www.reddit.com/r/nvidia/comments/1jgn6i6/i_tracked_the_prices_of_sold_nvidia_geforce_5090/

[^30]: https://www.storagereview.com/news/enterprise-to-sff-nvidia-launches-rtx-pro-6000-4000-sff-and-2000-blackwell-gpus

[^31]: https://www.leadtek.com/eng/news/product_news_detail/1811

[^32]: http://www.hyperscalers.com/NVIDIA-RTX-PRO-6000-Blackwell-Server-Edition

[^33]: https://www.amax.com/nvidia-rtx-pro-6000-blackwell-server-edition-vs-nvidia-l40s/

[^34]: https://www.cdw.com/product/nvidia-rtx-pro-6000-blackwell-server-edition-graphics-card-rtx-pro-60/8379294

[^35]: https://www.tomshardware.com/pc-components/gpus/you-can-install-nvidias-fastest-ai-gpu-into-a-pcie-slot-with-an-sxm-to-pcie-adapter-nvidia-h100-sxm-can-fit-into-regular-x16-pcie-slots

[^36]: https://nvidianews.nvidia.com/news/nvidia-rtx-pro-servers-with-blackwell-coming-to-worlds-most-popular-enterprise-systems

[^37]: https://www.velocitymicro.com/blog/rtx-6000-pro-blackwell/

[^38]: https://www.supermicro.com/en/support/resources/gpu

[^39]: https://www.supermicro.com/en/accelerators/nvidia-certified-systems

[^40]: https://www.pny.com/nvidia-rtx-a6000

[^41]: https://www.ebay.co.uk/itm/388519337764?chn=ps\&_ul=GB\&mkevt=1\&mkcid=28\&google_free_listing_action=view_item

[^42]: https://www.ebay.ca/itm/175799451821

[^43]: https://www.ebay.com/itm/187283507862?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EWZSE4P6ZGDSYS977Q\&hash=item2b9af78a96:g:nnoAAOSwEi5oIuwN\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1dbHQf6pvjbm%2FSSdB7KKPO0zAtO%2BEXdTCPOEQm7nHkTN38t7%2FWRbEh1D9whuW5Eyzl2sns3JxV3EBCXBcArg302d8N%2Fv%2FXsSSrxU1MmBD1Uh6raERtuN%2Bfi5bJvL1TEkLsUGFtjAvHFKqNAy97olms1B5GsUY17guh5qdQ3uh%2Fy4Mnf4A6DHDmtj5d0v7omhrvcQmPlAhitNQ4JGtuGn7b5cSlHrmjD%2FpnHjlbX%2BqYz88DMAUITjk0If%2F5dsbz42n2LQBuEY8SCw0H8I41z4H%2BcrIaK%2BuW7p%2FYxCIPz5COOFKOWfWPMugiaM%2BHtDd6nvTc%3D%7Ctkp%3ABk9SR8iXnNmWZg

[^44]: https://www.ebay.com/itm/135932167654?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EYHJ7YBCZY63H7ZCGQ\&hash=item1fa63045e6:g:P0UAAOSwB8ZoLlPy\&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1cVChgtmNKdPT1LzhWpZG582GWnzqSzJs%2FjHjMlJMZogN%2Bb4Qgj2wuV55rvg82FRlGVPipBqm3UNjzLGlxpiMe0QR77Ufx7HyLtQXEk6wV6es54z4zxiwMhWdxov90wWNTXBOIbiGdJBEWoyqPrBLK%2FocmmeZ3uT%2F2H3A3dQ1c4KX6EeiVHFUlM87ulTjEDbgBGBgpO17P4lNZiJK0jIc8X6yC7BsxcYR3Ka%2F8piYN%2FjZbR7X85%2BpN8nG73Zxt15xGmVN9YLQIbkmtOyRxe%2FzJE%7Ctkp%3ABk9SR86XnNmWZg

[^45]: https://www.ebay.com/itm/116701947956?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EW5CEAAAWE0D078N0K\&hash=item1b2bfa6834:g:VcgAAeSw75Fof07M\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1daQ69JUeEN0hY1lKNkaeeDispmwBzsGtdEasgq3E8v8b7WPQa80wsjl0JsgEOaG1gz9%2F9O8OEgMuY%2BySajeb9FP9wxrlYU1xlwR04lzRgdjti9ho2xxYnf2%2Fh0JPoQeItu4i6%2BeH7QwdBcUoNuyaia1N1oZAVIuz5r%2Bpajjp8wZFswoT8nRFL1QTZEDhk6QotKHaedDAkyVDk3Ii5n1ebLGYoZQYL8H1VHsywYe6AKvfyaPGWSO8VnZa%2FwX1elrmmHfIdpRZreIMamU%2FV41VWXV0tto4pPdLSwpu0KBhzBtnnIDqOP8wyTu4lmdEtW9%2F4%3D%7Ctkp%3ABk9SR8qXnNmWZg

[^46]: https://www.ebay.com/itm/197422418492?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EWJ2TV0VVP8J46RK7R\&hash=item2df74b0a3c:g:uPkAAOSwD2xoJ614\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1d9FKUCPjdLgRMQC9ExhiBJ9PARfPxbXVWYcstZY7sgIubwx97xZBdaGedci4HaSvNYMK4C1i3PWH%2FmtOpKwO%2Fq%2F8z59BKVKNMFVybJt1ltyxreS%2FC2v%2BYfROL1qBNWrKi0yjn14Myp3ynitNGomOcubrQ1sMfqvNosc%2F5zmb7jyRUs0PpUYmtR3r0mCxTZBSMxxEqGsYEPiAJrfGka%2F%2BLlmByHCjvpgrPECZtbiC4SxmwPgmOe4rjjMkLoWWEwO738DYfmk410DfqQfj7iM0A4A0OGMxKzzY2iAYDle35awXMZGyDxVNf90dLWHlSCgRI%3D%7Ctkp%3ABk9SR8iXnNmWZg

[^47]: https://www.ebay.com/itm/127272130232?_skw=rtx+pro+6000+blackwell+completed\&epid=22080398307\&itmmeta=01K2TS71EW4J06HS2SNZG87MJ3\&hash=item1da20296b8:g:iWUAAeSwRYdoiDOQ\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1e38hvjtrJe4N5v6Xza95Cqr6%2FirJoIWhbdmFizXH%2Ba3X7a%2F5vgVSuHLZuzmMk0lzhyqbFxPhMhzMzjieWBNRCfbqb%2BAf8d2N452Oi7J7lpv5J02rO%2BbGCXOVx5SGUNoDLPG79IH57fUfecc4shZ%2BaT9Qj2ICVbnxucNCmXhsAJHNfmonK4SfrxwV1T8Rs9YvhRHc8K0vx%2BRVnz4TUIJCkP7TbMrsnn%2FiYz8uG5t%2FaVe8qRxWYWAnpYpDOK6HqcCBr8ZgaEkGxvxjg%2BnNNuCeqdbHHhzvbws1HO5zKer%2BAedt6EANpdiycO6lKwhClXXfY%3D%7Ctkp%3ABk9SR8iXnNmWZg

[^48]: https://www.ebay.com/itm/297360076281?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EW7VV1TVMDR3ME63NR\&hash=item453c0aadf9:g:N-8AAOSw0cZoOJyC\&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1cP5SSV5HzZZMnz--ZCH5Z5HnXAroB3%2FTeqkfrdumNuCrglb%2FgUbmE7%2BLvyML4v6HodSxVg05QBpAewm88376lSaDgWj8vzwujoa5wda0BVnh4xzDHf6ClVO%2BfpGWAj4piRY%2FIVqqqNLDIgRwbGG0kb0dAkl8BNJHsoX6UF4wtPucl2LC9%2Bt9agC%2BC84Lo21U52YXGT3KUuOO1iS40DFg5XxRFEDYHrZVLEkXv2iBlDJNAtRZd1AfUAjl7qdoixflH6enZmSyqUIJKL7QCJWFTA%7Ctkp%3ABk9SR8iXnNmWZg

[^49]: https://www.ebay.com/itm/376329309843?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EWZ51X555S4RD88JC5\&hash=item579ef98e93:g:3-sAAOSwv5toSWGt\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1fmFCyOmlk9DOyZ1M4tD3sulc6Y4gqDOXlxpczkt6Y4SBuThHiumyESFSia7KkHquGYyFrMS02%2FkENeiL4ckwnZ9uXTGeNenxVIk%2F2fKkVZXfi9TD%2Bf9IppuEQx8R%2Fpo1yp%2FjS43%2F9kSAxGCPvtV7CjmeTHtIZoxzgT0OEAwt0CXq0PM9mmmRdIzCGbTixsD5E%2BLA73pmJV9KAHiJy9Epg%2B%2BSgFm39pyw5Hrijc%2BuUn4M7wYLVzw4E93Nt6VjkQ%2BgwNW5JxI8Op3YCw1L2TyWk8UquQtlSknZS5YaFFReI7AjquwsdnZkUYgRvu6EF%2Fz%2FU%3D%7Ctkp%3ABk9SR8qXnNmWZg

[^50]: https://www.ebay.com/itm/205571695330?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EWMPFC7SVC9GEPGVKZ\&hash=item2fdd0722e2:g:3RkAAOSwsW9oU1zx\&itmprp=enc%3AAQAKAAABAFkggFvd1GGDu0w3yXCmi1fmsiLPGKbA0dxMf74CClECFK9JvDqvhtfHwQga1d1zXLEtt2UIfewl9kjqJYU6JIkrdFHXtJ%2BTZoaVxntlhI6JaP8QPN7vqPBirI5HiJAEFqMHM3iD2%2B8knUUdZbp8v2h1SgbsTLD1BTRX4c9ABXslhlAd9fGhF0RYqIHFDl1J0qNh31BE5n2gQP%2B%2FUkBAtW06ix9Dh2bZ4Of9enzrmfynnQXtMN7rRu8%2FMq%2BHY0%2Fk33X1gBzFQMJWaWoE4nBRT9czAiPwEB2ZrQ4aDA0NSc8XbrPFYGUnI9PMb%2BZeZndHFwEaaz0P3TNJKw1HuVIoeLQ%3D%7Ctkp%3ABk9SR8qXnNmWZg

[^51]: https://www.ebay.com/itm/317134735432?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EWXQ6VZWXG2CBS5245\&hash=item49d6b40848:g:O3IAAeSwA1VojGY9\&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1f3Ih6HNND48oBbfKqKyMPxsiN5kq0SkDMxx%2BcZjM%2BtBIFzSb9vYI5Pxxg7ZrXtHDMl4%2FcBngNxdtmAhq%2B8f6gyQno8SLJxU50JMwd5mgxiM3YIALUwM1Ns4cqFJ%2Fy47%2Bb%2BYv2nHiLrJaN%2F55f%2B1G4vp%2FGsUqFolRQkT98nQcc0y%2Fqefhrz5eoDrCWpwoaWAK0QVXB4fYi8uqtbluji%2BLa7%2BksaAjoFxpFJilbLBy9joDquXhGWgjhYNIbcu1uN2OvQ%2B3AfNiDRZkH9BZF7fBpc%7Ctkp%3ABk9SR8qXnNmWZg

[^52]: https://www.ebay.com/itm/376393400362?_skw=rtx+pro+6000+blackwell+completed\&itmmeta=01K2TS71EW8QQ3C23TZRK2J03V\&hash=item57a2cb802a:g:plEAAeSwUONoZ5~G\&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1c%2FqI2Z746Ong697Zwe87Ogco3PejO9bc1t2XltIWYqfrA%2BZbJt7nEQMsFhBDeWXir3ITZ5T%2FPUCcKwlOBng7Xdi8AI4kegdKeAkaGgudTpvWZZOO7fHnz%2FRdP7efmf3e239G7qzVrPt%2FiWU%2F7kGNS2bM4QG1Axi8X74%2BzVerBOAK63c8CqH5EQfYRyZ56z7EeVF8bdpX5HAOonQpwkvpgWqPk8KpvL4Gzodxe8mCBjHN4a--uMYYV%2FRR2Z8SSoi1uCM3mo9MVB7RrYtVtrXW3Z%7Ctkp%3ABk9SR8qXnNmWZg

[^53]: https://www.prnewswire.com/news-releases/supermicro-now-accepting-orders-on-portfolio-of-more-than-20-systems-optimized-for-the-new-nvidia-rtx-pro-6000-blackwell-server-edition-gpus-accelerating-the-deployment-of-enterprise-ai-factories-302458725.html

[^54]: https://www.tomshardware.com/pc-components/gpus/nvidia-rtx-pro-6000-up-close-blackwell-rtx-workstation-max-q-workstation-and-server-variants-shown

[^55]: https://www.reddit.com/r/LocalLLaMA/comments/1ly4xvb/gpu_upgradeneed_suggestionupgrading_current/

[^56]: https://www.arccompute.io/solutions/hardware/nvidia-rtx-pro-6000-blackwell-servers

[^57]: https://www.pugetsystems.com/labs/articles/nvidia-rtx-pro-6000-blackwell-max-q-vs-workstation-for-content-creation/

[^58]: https://forum.level1techs.com/t/wip-blackwell-rtx-6000-pro-max-q-quickie-setup-guide-on-ubuntu-24-04-lts-25-04/230521?page=2

[^59]: https://www.supermicro.com/en/pressreleases/supermicro-now-accepting-orders-portfolio-more-20-systems-optimized-new-nvidia-rtx

[^60]: https://ir.supermicro.com/news/news-details/2025/Supermicro-Now-Accepting-Orders-on-Portfolio-of-More-Than-20-Systems-Optimized-for-the-New-NVIDIA-RTX-PRO-6000-Blackwell-Server-Edition-GPUs-Accelerating-the-Deployment-of-Enterprise-AI-Factories/default.aspx

[^61]: https://www.pny.com/nvidia-rtx-pro-6000-blackwell-max-q

[^62]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/c13655cb196b3a6aa7c04c24fcc1d348/6f10fdc1-d4d4-4826-af58-c104e1ba7008/c3afd0b9.csv

[^63]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/c13655cb196b3a6aa7c04c24fcc1d348/66efdc8a-3a3f-4431-b5b8-20e9c3052d02/58325eb7.csv

