

# TASK.sieveviz.sync-with-scored-output.md

## 🧩 Task: Sync SieveViz with Scored Dataset Output

Junie, your task is to modify the `sieveviz` front-end to dynamically reflect the latest output from the scored pipeline. The visualization layer must accurately display GPU scoring data, heuristics, and model metadata.

---

## 🎯 Objectives

- Update `sieveviz/app.js` to load data from the current `scored.csv` or enriched dataset
- Parse the following key fields:
  - `canonical_model`
  - `score`
  - `price_usd`
  - `vram_gb`
  - `tdp_watts`
  - `mig_support`
  - `quantization_capable` (if present)
- Use this data to populate the current visualizations and add missing insights

---

## 📊 Visualizations to Sync

- Scatter plot: `price_usd` vs `score`
- Color-coded clustering by `quantization_capable` or `generation`
- Tooltip info panel should display:
  - Model name
  - Score
  - Price
  - Metadata fields (VRAM, MIG, etc.)

---

## 📦 Implementation Details

- Front-end code lives in `sieveviz/`
- Output CSV will be produced by `glyphsieve pipeline` or `glyphsieve score`
- Ensure `index.html` renders the current state from CSV (either embedded or loaded dynamically)
- Ensure JS schema aligns with the current Pydantic output model

---

## 🧪 Completion Criteria

- `sieveviz/index.html` renders data from latest pipeline output
- All expected fields are visible in the graph or on-hover details
- Dataset updates trigger clean visual refresh
- No stale or hardcoded rows remain in `app.js`

---

## ✍️ Notes

This syncs the visual cortex of the system. Make sure users viewing this tool are seeing the same structure and insights that the backend generates.