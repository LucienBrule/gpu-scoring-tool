# TASK.loader.04.bad-row-analysis

## Title
Analyze and handle unqualified or invalid rows in Shopify JSON input data

## Context
Following the implementation of the Shopify source loader and successful parsing of `wamatek_sample.json`, we now have a dataset that includes a range of product types — not all of which are valid GPU listings. Some items include capture cards, accessories, and other hardware that cannot be matched to any known GPU model.

Currently, these "dirty" rows flow through the pipeline and are either:

- Marked as `UNKNOWN_GPU` in the normalization phase
- Trigger warnings during enrichment
- Receive null or low scores at the end

## Objective
Ensure that the pipeline handles invalid or noisy input gracefully, with explicit visibility into what happened and why. This enables downstream consumers (UI, analysts, operators) to identify and potentially exclude low-confidence or invalid items.

## Tasks

1. **Audit Pipeline Behavior for Dirty Rows**
   - Run the full pipeline on `wamatek_sample.json`.
   - Observe how clearly invalid rows behave at each stage:
     - `normalize`
     - `enrich`
     - `quantize`
     - `score`

2. **Update DTOs or Add Contextual Metadata**
   - Add a new field to the normalized or enriched row, such as:
     - `unknown_reason` or `normalization_warning`
     - `matched = false` or `confidence_score`

3. **Optional: Add CLI Flag for Filtering**
   - Add a `--filter-invalid` flag to exclude low-confidence or unmatched rows from being emitted in the final output CSV.

4. **Document Examples**
   - Log a few concrete examples of bad rows.
   - Show how they appear in `output.csv`, and whether their score is 0 or NaN.

## Definition of Done

- At least 3 example rows from `wamatek_sample.json` identified and traced through the pipeline.
- New warning/flag fields added to the output CSV schema.
- `uv run glyphsieve pipeline` produces traceable, enriched results for both good and bad rows.
- Code passes lint, pytest, and CLI smoke test.

## Related

- EPIC.loader.shopify-source-loader.md
- TASK.loader.02.define-shopify-json-loader.md
- TASK.loader.03.load-shopify-wamatek-json.md

## ✅ Task Completed

**Changes made:**
- Enhanced normalization process with `_detect_non_gpu_item()` function to identify non-GPU items using keyword detection
- Updated `GPUListingDTO` and `EnrichedGPUListingDTO` models to include `is_valid_gpu` and `unknown_reason` fields
- Modified `normalize_gpu_model()` function to return validation status and reason for unknown items
- Fixed enrichment stage to preserve `is_valid_gpu` and `unknown_reason` fields through the pipeline
- Added proper NaN handling in enrichment code to prevent Pydantic validation errors
- Implemented `--filter-invalid` CLI flag in pipeline command to exclude invalid items from final output
- Updated scoring module to include validation fields in output CSV

**Outcomes:**
- Successfully identified and traced 13 invalid items through the full pipeline from `wamatek_sample.json`
- Pipeline now filters 13 invalid rows and keeps 12 valid GPU listings when using `--filter-invalid` flag
- Invalid items properly categorized with specific reasons:
  - **Capture devices**: "AVerTV Hybrid TVBox 13", "Ezrecorder 330 Capture", "Live Streamer CAP 4K"
  - **Video equipment**: "Vaddio OneLINK Bridge for Vaddio HDBaseT Cameras"
  - **Incomplete GPU names**: "ASUS TUF GAMING GEFORCE RTX", "PNY GeForce RTX 5070 Ti"
  - **Unmatched GPU models**: "GEFORCE GT 710 2GB", "RADEON RX 550 2GB", etc.
- All pipeline stages (normalize → enrich → quantize → score) now handle invalid rows gracefully
- Output CSV includes explicit visibility into validation status and reasons for filtering

**Lessons learned:**
- Pandas CSV reading can introduce NaN values that require careful handling in Pydantic models
- Field preservation through pipeline stages requires explicit handling in each transformation step
- Non-GPU detection benefits from both keyword-based filtering and incomplete model name detection
- The `--filter-invalid` flag provides valuable data quality control for downstream consumers

**Follow-up needed:**
- None - all task requirements have been fully satisfied

