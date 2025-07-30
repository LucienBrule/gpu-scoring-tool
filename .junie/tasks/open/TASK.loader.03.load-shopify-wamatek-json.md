


# Task: Load Wamatek Shopify JSON and Convert to Input Format

## EPIC
Refer to: `EPIC.loader.shopify-source-loader.md`

## Goal
Implement a loader that ingests raw JSON data from Wamatek’s Shopify API and converts it into a normalized CSV suitable for pipeline input.

This loader is the first concrete implementation of the `SourceLoader` interface hierarchy. It should be structured as a subclass of `ShopifyJSONLoader`, itself a subclass of `SourceLoader`. The resulting CSV must match the schema of `input.csv` expected by the pipeline.

## Requirements
- Define `WamatekShopifyLoader`, which accepts a raw `.json` file exported from Wamatek's Shopify backend (found in `recon/`).
- Implement transformation logic to produce:
  - `input.csv`-style columns:
    - `model`
    - `condition`
    - `price`
    - `quantity`
    - `seller`
    - `geographic_region`
    - `listing_age`
    - `source_url`
    - `source_type`
    - `bulk_notes`
    - `title`
- Add a CLI entrypoint in `glyphsieve`:
  ```bash
  uv run glyphsieve load-shopify --source wamatek --input recon/wamatek-2025-07.json --output ./tmp/wamatek.csv
  ```
- Output must be a valid CSV compatible with the existing `pipeline` command.
- Implement default assumptions for missing or unstructured fields (e.g. fallback on vendor name for region, parse price and model from title if necessary).
- Document mapping assumptions clearly in code comments or inline docstrings.

## Implementation Notes
- The loader should live in `glyphsieve/core/loaders/shopify/` and be discoverable via the `SourceLoader` plugin registry.
- You may reuse Shopify JSON helpers across other future loaders.
- No API calls should be made — this task operates solely on static `.json` files.

## Acceptance Criteria
- Can run with sample JSON from `recon/wamatek*.json` to produce valid `input.csv` output.
- Pipeline CLI accepts the output without error.
- Code is lint-clean and passes all relevant test coverage.
- Implementation reuses the abstract loader hierarchy defined in `TASK.loader.01` and `TASK.loader.02`.