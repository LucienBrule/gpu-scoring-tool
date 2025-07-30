# Task: Patch Regex Patterns for GPU Model Normalization

## Purpose
Patch and enhance the regex matching patterns used in GPU model normalization to reduce false positives and false negatives.

## Motivation
Based on findings from the Wamatek dataset, current regex rules misclassify models like `A100_40GB_PCIE`, `RTX_4000_SFF_ADA`, and fail to match legitimate variants such as `RTX PRO 6000 BLACKWELL`.

## Acceptance Criteria
- Update regex definitions to support stricter inclusion and exclusion logic (e.g., exclude `"INTEL"` and `"T400"` when matching `A40`, or validate `"Pro"` and `"Blackwell"` in RTX matches).
- Add positive assertions for untracked-but-legitimate GPUs (e.g., `L40`, `L40S`, `A16`, `A10`, `T4`, `Quadro RTX 8000`, etc.).
- Validate changes against full 10k Wamatek dataset using:
  ```
  uv run glyphsieve pipeline --input tmp/wamatek_full.csv --output tmp/wamatek_full_score_filtered.csv --working-dir tmp/work --filter-invalid
  ```
- Suppress or resolve warnings: `Model 'A100_40GB_PCIE' not found in GPU registry`, etc.
- Confirm that enrichment and normalization stages have fewer misclassifications than previous runs.

## Dependencies
- Linked Epic: `EPIC.refine.model-normalization-accuracy.md`
- Related Task: `TASK.refine.01.gpu-registry-additions.md`
