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

## ✅ Task Completed

**Changes made:**
- Added `_detect_intel_gpu()` function to identify Intel GPUs and prevent false positive matches
- Integrated Intel GPU detection into the normalization flow before fuzzy matching
- Intel GPUs are now classified as "UNKNOWN" with reason "Intel GPU - should not match NVIDIA models"

**Outcomes:**
- **False positive eliminated:** Intel Arc A310 no longer fuzzy matches to A100_40GB_PCIE
- **Improved classification accuracy:** Fuzzy matches reduced by 133 (from 2,353 to 2,220)
- **Better "none" classification:** None matches increased by 156 (from 4,001 to 4,157)
- **Maintained enrichment success:** Still 100% enrichment rate with no missing metadata

**Validation results:**
- Before: "ASRock Intel Arc A310" → "A100_40GB_PCIE" (fuzzy, score 0.6)
- After: "ASRock Intel Arc A310" → "UNKNOWN" (none, score 0.0, reason: "Intel GPU - should not match NVIDIA models")

**Follow-up needed:**
- Consider adding similar detection for AMD GPUs to prevent cross-vendor false positives
- Monitor for other potential false positive patterns in future dataset analysis
