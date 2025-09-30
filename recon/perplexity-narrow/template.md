# Perplexity Narrow Recon Template

**Target GPU:** <insert one from the list below>

## Objective

Build an up-to-date, evidence-backed profile of pricing and availability for the Target GPU across secondary markets (with emphasis on eBay), and produce normalized $/perf and $/GB comparisons. Treat integrated servers (HGX/DGX/OEM) as vertical nodes (CPU/RAM/PSU/NIC value included), not just “a pile of GPUs.”

## Scope (what to gather)

1. Active listings (global): eBay (US/EU/UK/JP/CN), major refurbishers/resellers.
2. Sold/Completed listings: last 90 days for comps; flag last 14 days for freshest trend.
3. Integrated chassis (if applicable): Supermicro/Inspur/Gigabyte/Dell/HPE systems with the Target GPU preinstalled OR “BYO GPU” variants.
4. Converted cards (if applicable): SXM→PCIe conversions/carriers for the Target GPU; capture adapter/power/cooling details.
5. Spec anchors (for $/perf): VRAM size/type, mem bandwidth, FP16/FP8 availability, MIG/NVLink presence, PCIe generation, typical TDP.

## Key terms & distinctions (use to disambiguate search/results)

- **SXM vs PCIe:** SXM = mezzanine module for HGX baseboards (often NVLink/NVSwitch). PCIe = standard add-in card.
- **Converted SXM:** SXM module on a carrier → PCIe card; often 48V power or special DC-DC; no NVLink exposed.
- **Integrated node:** Complete server with CPUs (e.g., EPYC Genoa/Milan), RAM, NVMe, NICs, PSUs, rails, the HGX baseboard, retimer risers, and flyover cables.
- **MIG:** Multi-Instance GPU (hard partitioning of GPU).
- **NVLink/NVSwitch:** High-bandwidth GPU↔GPU fabric on SXM systems (e.g., A100 HGX).
- **Workstation vs Server variant (RTX 6000 Blackwell):** Workstation ~600W air-cooled; Server/“Max-Q” ~300W passive; Server variant may support MIG (verify).
- **Ada vs Blackwell (RTX 6000):** Ada = 48GB; Blackwell = 96GB GDDR7. Avoid conflation.

## Data collection requirements

### A) Listing table (active + sold) — capture the following per listing

- `date_seen` and (for sold) `date_sold`
- `marketplace` (eBay US/EU/UK/JP/CN, etc.)
- `title_raw`, `link`, `seller_name`, `seller_feedback_%`, `seller_feedback_count`
- `price_native`, `currency`, `shipping_native`, `tax_est_native` → normalize to USD (`price_usd_total`)
- `condition` (new/used/refurb/“pulled”), `warranty` (Y/N, duration)
- `form_factor` (PCIe | SXM | Converted SXM→PCIe)
- `variant` (workstation | server | OEM L40-style if mislisted)
- `vram_gb`, `mem_type` (HBM2/e/3, GDDR6/7), `pcie_gen`, `nvlink` (Y/N), `mig_support` (Y/N/Unknown)
- `tdp_w` or `tbp_w` if stated, `compute_capability` if stated
- `pn_model` (part number / FRU), `oem_brand` (Dell/HPE/Supermicro/Gigabyte/Inspur), `bios/firmware_notes`
- `includes` (cables/risers/HGX baseboard/CPUs/RAM/rails/NIC), `missing_parts`
- `photo_evidence` (grab the image showing labels/PNs; store URL)
- `notes` (e.g., “SXM to PCIe carrier, 48V DC-DC on board”; “BYO GPU chassis”; “engineering sample”; “mining use”)

### B) Integrated chassis valuation (if present)

- Parse the BOM: CPU model(s) & core count, motherboard model (e.g., H12DGO-6), RAM size & speed, NVMe/backplane/NICs (CX-6/CX-7), PSUs, rails.
- Provide replacement value estimates for each BOM line from recent comps (±20%) and compute `system_base_value_usd` (excluding GPUs).
- Derive implied GPU cost: `price_usd_total − system_base_value_usd` and per-GPU `implied_gpu_usd`.

### C) Statistics & normalization

- Compute median, mean, min/max, IQR for `price_usd_total` (by condition and region).
- Compute $/GB_VRAM and $/TFLOP_FP16 (and $/TFLOP_FP8 if the Target GPU supports FP8; otherwise N/A).
- Flag outliers (beyond 1.5×IQR) and mislistings (Ada vs Blackwell mixups, wrong VRAM).

### D) Risk/credibility checks

- Seller credibility (feedback %, count, return policy), stock levels (multi-quantity), and “no returns/as-is” flags.
- Identify engineering samples (ES/QS) and disclaimers.
- For conversions: note power requirements (48V DC-DC), cooling expectations, firmware/driver caveats.
- Region caveats (CN export, VAT, import taxes, shipping lead times, RMA feasibility).

## $/Perf anchor (for later cross-card comparison)

- Pull authoritative spec throughput: FP16 (all), FP8 (if applicable), memory bandwidth, CUDA core count.
- If multiple official numbers exist (e.g., SXM @400W vs PCIe @300W), record both; prefer official datasheets or respected vendor summaries.
- Compute:

```
usd_per_tflops_fp16 = price_usd_total / fp16_tflops
usd_per_tflops_fp8  = price_usd_total / fp8_tflops   # if supported
usd_per_gb_vram     = price_usd_total / vram_gb
```

- For integrated systems, compute two $/perf metrics: (a) raw listing price and (b) implied GPU price after subtracting system base value.

## Time & freshness

- Prioritize last 14 days (active and sold) to catch current market movement; then include last 90 days for trend/variance.
- Note shortages (“OOS everywhere”), sudden price cliffs/spikes, and seasonality (e.g., fiscal-year offloading).

## Output format

1. Summary bullets (5–10 lines): current price bands, notable anomalies, availability outlook, any “too good to be true” flags.
2. Pricing table (CSV/Markdown): one row per listing (active & sold) with all fields above; normalize prices to USD and include shipping/tax in `price_usd_total`.
3. Stats table: medians/means by condition & region; $/GB and $/TFLOP metrics.
4. Integrated chassis table: BOM valuation, implied GPU cost per unit.
5. Evidence pack: the top 10–20 most relevant listing URLs (active + sold), plus direct links to images showing PN labels/VRAM, and at least one OEM datasheet for specs.
6. Confusions resolved: short section explicitly clarifying any Ada vs Blackwell mixups, SXM vs PCIe confusion, and workstation vs server variants.
7. Assumptions & limitations: call out any missing data, unverifiable claims, or regions not covered.

## Quality bar & guardrails

- De-duplicate cross-listed items (same seller/listing mirrored across regions).
- Verify VRAM size in photos (48GB vs 96GB) to avoid Ada/Blackwell confusion.
- Treat ultra-low prices with skepticism unless seller reputation & photos are solid.
- Prefer sold comps over asking prices for value estimates.
- Record date stamps and include at least one screenshot link per critical listing (Wayback or image URL ok).