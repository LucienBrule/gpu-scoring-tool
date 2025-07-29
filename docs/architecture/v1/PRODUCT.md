# v1 Product Overview – GPU Scoring Tool

## 🎯 Purpose

This system was built to address a gap in the observability and valuation of second-hand and enterprise-grade GPU
hardware — a space underserved by traditional e-commerce analytics or enterprise IT tools.

It serves as an intelligent signal pipeline for understanding:

- **Current market value of GPU hardware**
- **Quantized model inference capacity per unit**
- **Energy efficiency and performance per dollar**
- **Shifts in liquidation cycles, vendor strategy, and SKU arbitrage opportunities**

The core intent is **operational, analytical, and economic clarity** in a fragmented and noisy secondhand GPU market.

---

## 🧑‍💻 Who It's For

- **Lucien (Operator):** Strategic AI hardware procurement, real-time inventory profiling, system design calibration
- **Solien (Assistant):** Pipeline reasoning, insight generation, memory consolidation
- **General Audience / Technical Researchers:** Signal modeling, LLM inference benchmarking, lab operators, arbitrage
  hunters, and infrastructure procurement analysts

---

## 🛠️ What It Does

- Ingests scraped CSV pricing data across vendors and marketplaces
- Cleans, deduplicates, and normalizes GPU listings
- Enriches listings with known spec sheets and heuristics (e.g. quantization fit)
- Applies scoring based on VRAM, power, MiG support, and observed market price
- Emits reports, scatter plots, and scoring summaries
- Powers a fully automated frontend and backend API

The result is a **declarative understanding of price-performance** per GPU SKU.

---

## 🧠 What It Tracks

Each listing is converted into a signal-rich data row, capturing:

- VRAM (GB)
- Power (W)
- MIG capability
- Price (market adjusted)
- Quantization fit (7B / 13B / 70B at 4-bit)
- Seller geography, listing age, stock condition
- Derived metrics: $/GB, $/MiG, Models per Watt, etc.

This allows tracking:

- Market inflation / deflation across categories
- Sleepers and overvalued SKUs
- Price convergence between consumer and enterprise lines
- Lifecycle phase transitions (e.g. Ada → Blackwell)

---

## 📊 Hypothesis

> "There exists a quantifiable arbitrage window at the intersection of model quantization, inference performance, and
> enterprise GPU liquidation."

We hypothesize that:

- MiG-capable GPUs with 20–48GB VRAM are disproportionately valuable in 4-bit inference pipelines
- Sellers liquidate at bulk regardless of latent capacity
- Scoring can reveal undervalued cards before consumer pressure catches up

---

## ✅ Validation

- Early runs confirmed A2, RTX 4000 Ada SFF, and L4 as underrated
- Identified price distortion zones and false value signals (e.g. signed H100s at $40K)
- Structured GPU knowledge into a DTO-backed schema for reproducibility
- Pipeline produces consistent outputs for insight generation and integration

---

## 🔁 Feedback Loop

This system is designed to learn from itself:

- Scores inform procurement and resale strategy
- Listings are crawled and re-evaluated over time
- Quantization heuristics evolve with model landscape
- Everything can be re-run on new data or weights

---

## 🗺️ Product Outlook

This is the first layer of a broader infrastructure signal engine.  
v1 proves vertical viability.  
v2 introduces horizontal scale across:

- DPUs
- POWER servers
- x86 enterprise racks
- Emerging inference chipsets

The product is not just a scraper.  
It's an **intent-aware market observability tool**, tuned to a future where inference economics shape systems
architecture itself.