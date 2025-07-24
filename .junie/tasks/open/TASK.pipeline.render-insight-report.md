

# TASK.pipeline.render-insight-report.md

## 🧩 Task: Generate Insight Report from Scored GPU Dataset

Junie, your task is to implement a CLI command that generates a human-readable report from a fully scored dataset. The output should summarize key insights and statistical observations about the GPU market, helping operators quickly assess market conditions.

---

## 🎯 Objectives

- Add a new CLI subcommand: `glyphsieve report`
- Accept as input a scored CSV file (with `score`, `canonical_model`, `price_usd`, etc.)
- Output a Markdown (`.md`) and/or HTML report summarizing insights

---

## 🧠 Report Content Requirements

- 📈 Summary statistics:
  - Number of listings
  - Count of unique `canonical_model`
  - Price range, average, and median
  - Score distribution (min, max, mean)

- 🏆 Highlight Sections:
  - **Top 10 cards by score**
  - **Top 10 cards by score-per-dollar**
  - **Best value cards under $2000**
  - **Most common model**

- 📉 Anomalies:
  - Cards with identical models but widely varying prices
  - Any listing flagged as `DUPLICATE_SECONDARY` that had a higher score than its primary

- 📊 Optional: Inline chart (text-based or matplotlib-generated image)

---

## 📦 File Locations

- CLI: `glyphsieve/cli/report.py`
- Reporting logic: `glyphsieve/core/reporting.py`
- Output directory: default to `reports/YYYY-MM-DD/insight.md` (configurable)

---

## 🧪 Tests

- Validate that reports render without error
- Ensure values are accurate for a small fixture input
- Confirm file creation and output location

---

## ✅ Completion Criteria

- `uv run glyphsieve report --input scored.csv` generates `reports/YYYY-MM-DD/insight.md`
- Report includes all required sections and stats
- Formatting is clear, human-readable, and usable as part of downstream newsletter or dashboard

---

## ✍️ Notes

This is the first outward-facing summary layer of the GlyphSieve system. It’s the part humans will see — make it sharp, insightful, and structured.