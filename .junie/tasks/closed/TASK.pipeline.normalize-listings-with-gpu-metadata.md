# TASK.pipeline.normalize-listings-with-gpu-metadata.md

## 🧩 Task: Enrich Normalized Listings with GPU Metadata

Junie, your task is to take a CSV of normalized GPU listings (produced by the `normalize` subcommand) and enrich each row by joining it with known GPU metadata such as VRAM, TDP, generation, and feature flags (e.g. MIG, NVLink).

---

## 🎯 Objectives

- Implement a new `glyphsieve enrich` subcommand
- Accept an input CSV (must include a `canonical_model` column)
- Join each row with structured GPU specs loaded at runtime
- Output a CSV with additional metadata columns:
  - `vram_gb`
  - `tdp_watts`
  - `mig_support`
  - `nvlink`
  - `generation` (e.g. Ada, Ampere, Hopper, Blackwell)

---

## 🧱 Metadata Structure

- Create a GPU metadata registry using **Pydantic DTOs** loaded from a `gpu_specs.yaml` file
- Each record in the YAML file should represent one canonical model
- Use schema validation to ensure clean input
- Store Pydantic models in `glyphsieve/models/gpu.py` and YAML in `glyphsieve/resources/gpu_specs.yaml`

---

## 📁 Reference Data

You may extract initial GPU metadata from:
- `sieveviz/app.js` — existing data model of known GPUs and their properties
- `sieveviz/Final_Market_Value_GPU_Summary.csv` — CSV version of canonical model + MSRP + tags

Feel free to adapt these into your DTO schema and derive additional attributes as needed.

---

## 🧪 Completion Criteria

- `uv run glyphsieve enrich --input normalized.csv --output enriched.csv` runs successfully
- Output CSV includes appended metadata columns for each row
- Missing models handled gracefully with default or empty values
- Pydantic model schema loads cleanly from YAML and validates at startup
- Use `gpu_model_map[canonical_model]` or equivalent for fast lookup

---

## 🧪 Tests

- Add test cases that load `gpu_specs.yaml` and validate:
  - DTO schema parsing
  - Lookup behavior
  - Enrichment output against known inputs

---

## ✍️ Notes

This task prepares the dataset for scoring and decision-making. You are now building the semantic layer — attaching static meaning to dynamic market data. Make it precise and reusable.

---

## ✅ Task Completion Summary

**Date Completed:** July 24, 2023

### 🔍 Implementation Details

1. Created Pydantic models for GPU metadata in `glyphsieve/models/gpu.py`
2. Created a YAML file with GPU specifications in `glyphsieve/resources/gpu_specs.yaml`
3. Implemented core enrichment functionality in `glyphsieve/core/enrichment.py`
4. Added a new `enrich` subcommand in `glyphsieve/cli/enrich.py`
5. Registered the subcommand in `glyphsieve/cli/main.py`
6. Added comprehensive tests in `glyphsieve/tests/test_enrichment.py`
7. Created a `tmp/output` directory for temporary output files
8. Updated guidelines to include the point about not polluting the repo root

### 🧪 Testing Results

All tests pass successfully, confirming that:
- GPU specs can be loaded from YAML files
- CSV files can be enriched with GPU metadata
- Error handling works as expected
- The CLI command functions correctly

### 📊 Usage Example

```bash
uv run glyphsieve enrich --input normalized.csv --output enriched.csv
```

This command enriches a normalized CSV file with GPU metadata, adding columns for VRAM, TDP, MIG support, NVLink, and generation.
