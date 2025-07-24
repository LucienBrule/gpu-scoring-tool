# GPU Scoring Tool / GlyphSieve (v0.1.0)

This repository is the research implementation and operational pipeline for modeling, scoring, and analyzing the **real-world value of GPUs** across market layers — from hyperscaler decommission to resale arbitrage and forward deployment in inference systems.

---

## 🧠 Purpose

NVIDIA's MSRP and press-facing GPU hierarchy no longer reflect actual market performance or value. In practice:

- Cards are scored by what *they can actually do* (quantized inference, MIG partitioning, power profile)
- Pricing data is fragmented, noisy, and buried in a mix of retail, gray-market, and bulk resale
- High-value cards often hide behind obscure SKUs (e.g. OEM-only, export-banned, repackaged server editions)

**This tool exists to fix that.**

We:
- Scrape GPU listings from known and emerging inventory nodes
- Normalize messy data into a structured schema
- Score cards based on what matters for inference, not marketing
- Visualize pricing topology, anomalies, and gravitational efficiency fields
- Map the global silicon dumpening event in real time

---

## 🛠️ Project Layout

```
gpu-scoring-tool/
├── glyphsieve/         → Python package for cleaning, normalizing, and scoring raw scraped GPU data
├── sieveviz/           → Visualization layer: charts, market plots, price-to-score topology, etc.
├── scrape/             → Per-SKU pricing datasets + scripts (hand-collected or scraped)
├── recon/              → Human OSINT folders (e.g. seller profiles like halbry)
├── .junie/             → AI task coordination and structured memory assistant (Junie)
```

---

## 🧩 Technologies

- Python 3.12 with [`uv`](https://github.com/astral-sh/uv) for reproducible environments
- `glyphsieve`: main module under `src/`, contains the core pipeline logic
- CSV/JSON scraped data as inputs
- Typer-based CLI tooling (planned)
- Kotlin/TypeScript interop for DTO definitions and structured pipelines (planned)
- Junie: internal agent layer for structured automation

---

## 🔮 Future Direction

- Build `sieveflow`: a lightweight DAG system for running staged scraping + normalization jobs
- Live eBay inventory watchers per seller
- Integrate model quantization footprint scoring (how many LoRAs per card?)
- Scoring-as-a-service: run cards against current market + cluster tier
- GPU topology engine for rack planning (RackViz integration)
- DaemonOS-ready stream: serve cleaned GPU field signals into higher-order inference daemons

---

## ✨ Why This Exists

Because there’s signal in the noise.

Because inference hardware is being dumped, disguised, and mispriced.

And because somewhere in all that mess is **a rational field** —  
and we're going to map it.

Welcome to GlyphSieve.
