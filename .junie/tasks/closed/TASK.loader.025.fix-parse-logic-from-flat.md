# TASK.loader.025.fix-parse-logic-from-flat

## Goal

Ensure the `shopify-parse` command can successfully process the updated flat JSON format used in `recon/wamatek/wamatek_sample.json`.

## Background

Originally, the parser was designed for a `.jsonl` format or a different structure. The new format is a single JSON file with a top-level `"products"` key pointing to an array of Shopify product entries.

## Task Instructions

- Investigate why the current command fails with "Aborted!" when run on the new sample file.
- Adjust the parser logic to correctly read and iterate through the `"products"` array in the input file.
- Confirm the following command works end-to-end and produces the expected output CSV:

```
uv run glyphsieve shopify-parse --input recon/wamatek/wamatek_sample.json --output tmp/test_full_subset.csv
```

## Acceptance Criteria

- The command above succeeds without aborting.
- Output CSV is generated and includes data parsed from the sample file.
- Parser gracefully handles the flat JSON structure.

## Tips

- Use debugging output (e.g., `print()` statements or Python breakpoints) to inspect file loading and structure.
- Be sure to handle exceptions cleanly and verify that the input is a valid list under `data["products"]`.

## ✅ Task Completed

**Changes made:**
- Modified the `load()` method in `WamatekShopifyLoader` to support both JSONL format and flat JSON format
- Added logic to first attempt parsing as a single JSON object with top-level "products" array
- Falls back to original JSONL parsing if flat JSON parsing fails
- Updated docstring to reflect support for both formats

**Outcomes:**
- The `shopify-parse` command now successfully processes `recon/wamatek/wamatek_sample.json`
- Generated CSV output with 26 product listings from the sample file
- All existing tests (11/11) continue to pass, ensuring no regressions
- Parser gracefully handles both flat JSON structure and original JSONL format

**Lessons learned:**
- The original parser was designed for JSONL format (line-by-line JSON objects) but the sample file used flat JSON format
- Backward compatibility was maintained by implementing format detection and fallback logic
- The fix enables processing of real-world Shopify API exports that use flat JSON structure

**Follow-up needed:**
- None - task requirements fully satisfied
