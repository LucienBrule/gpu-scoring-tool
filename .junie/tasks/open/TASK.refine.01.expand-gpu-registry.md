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

## References

- Refinement Epic: [Link to Refinement Epic](https://example.com/refinement-epic)
- Known Issues:
  - Missing registry entries for `A100_40GB_PCIE`
  - Missing registry entries for `RTX_4000_SFF_ADA`

Please ensure the registry updates are backward compatible and thoroughly tested before merging.
