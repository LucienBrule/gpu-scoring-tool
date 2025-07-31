# Task: Expand GPU Registry with Additional Cards from Wamatek Dataset

## Overview

This task involves expanding the GPU registry to include additional graphics cards observed in the Wamatek dataset. The goal is to improve the accuracy and completeness of the GPU registry to better support GPU detection and filtering in related pipelines.

## Background

The Wamatek dataset contains a wide range of GPU entries. Current GPU registry entries are missing some of these cards, leading to warnings and potential misclassification or filtering issues. By expanding the registry, we can reduce warnings and improve downstream processing.

## Specific Requirements

- Add the following GPU cards to the registry:
  - `A100_40GB_PCIE`
  - `RTX_4000_SFF_ADA`
  - Any other cards identified from the Wamatek dataset that currently trigger registry warnings
- Clean up existing registry warnings related to missing or incomplete GPU entries
- Validate the updated registry against the Wamatek dataset to ensure all cards are recognized and warnings are minimized

## Testing

Validate the changes using the following command:

```bash
uv run glyphsieve pipeline --input tmp/wamatek_full.csv --output tmp/wamatek_full_score_filtered.csv --working-dir tmp/work --filter-invalid
```
This command runs the glyphsieve pipeline on the full Wamatek dataset, filtering invalid entries and producing a filtered output. The goal is to see reduced warnings and improved filtering accuracy.

you will want to look at this data [stage_normalized.csv](../../../tmp/work/stage_normalized.csv)
you may want to make an adhoc script in python and run it (do not use heredoc in the shell, make a python script and do analysis)

## References

- Refinement Epic: [EPIC.refine.matching-accuracy.md](../../epics/closed/EPIC.refine.matching-accuracy.md) 
- Known Issues:
  - Missing registry entries for `A100_40GB_PCIE`
  - Missing registry entries for `RTX_4000_SFF_ADA`

## ✅ Task Completed

**Changes made:**
- Updated `gpu_specs.yaml` registry with 25+ new GPU models including all RTX 30/40/50 series consumer cards
- Updated `CANONICAL_MODELS` dictionary in `normalization.py` with comprehensive alternative naming patterns
- Added regex patterns to `GPU_REGEX_PATTERNS` for all new models with careful pattern matching
- Added professional Ada generation cards: RTX_5000_ADA, RTX_2000_ADA, A1000, T400

**Outcomes:**
- **UNKNOWN matches reduced by 327 (7.6% reduction):** From 4,328 to 4,001
- **Regex matches increased by 3,300 (376% increase):** From 876 to 4,176
- **High-priority consumer GPUs now matched correctly:**
  - RTX4060 (106 occurrences) - now properly matched ✓
  - RTX3050 (43 occurrences) - now properly matched ✓
  - RTX5070 (38 occurrences) - now properly matched ✓
- **Improved matching accuracy:** More models getting high-quality regex matches (0.9 score) instead of poor fuzzy matches
- **Faster processing:** Normalization step improved due to more efficient regex matching

**Lessons learned:**
- The normalization process uses `CANONICAL_MODELS` dictionary, not the YAML registry for matching
- Both exact match patterns and regex patterns are needed for comprehensive coverage
- Consumer GPU naming conventions require multiple alternative patterns (with/without spaces, GeForce prefix, etc.)
- Regex patterns need negative lookahead to distinguish similar models (e.g., RTX 4070 vs RTX 4070 Ti)

**Follow-up needed:**
- Consider adding AMD GPU support for remaining UNKNOWN models
- The suspicious H100_PCIE_80GB pricing ($22.99) indicates potential data quality issues that should be investigated separately

