# Task: Legacy GPU Registry Expansion for FP Rate Improvement

## Overview

This adhoc task focuses on reducing false positive (FP) rates in the Wamatek dataset by expanding the GPU registry with missing legacy GPU models. Analysis of the false positive replay set reveals that many legacy GPUs (GT series, GTX 1660 series, Quadro T series) are incorrectly fuzzy matching to modern RTX cards due to missing registry entries.

## Background

Current FP analysis shows several problematic patterns:
- GT 710/730 cards fuzzy matching to RTX 5070 (score ~0.66)
- GT 1030 cards fuzzy matching to H100_PCIE_80GB (score 0.60)
- GTX 1660 Ti fuzzy matching to RTX 4060 Ti (score 0.67)
- Quadro T1000 fuzzy matching to A40 (score 0.64)
- AMD GPUs still matching to NVIDIA models despite Intel GPU detection

## Specific Requirements

### Primary Goal: Add Missing Legacy GPU Models
- **GT Series**: GT 710, GT 730, GT 1030
- **GTX 16 Series**: GTX 1660, GTX 1660 Ti, GTX 1660 Super
- **Quadro T Series**: T1000, T600, T2000
- **RTX 20 Series**: RTX 2060, RTX 2070, RTX 2080 (if missing)

### Secondary Goal: Improve Cross-Vendor Detection
- Enhance AMD GPU detection similar to Intel GPU detection
- Prevent AMD Radeon cards from fuzzy matching to NVIDIA models
- Add regex patterns for common AMD naming conventions

### Success Criteria
- **Reduce fuzzy match FPs by 25%**: Target reduction in low-confidence fuzzy matches (<0.7 score)
- **Increase regex match coverage**: More legacy models should get high-confidence regex matches
- **Eliminate cross-vendor matches**: AMD GPUs should not match NVIDIA canonical models
- **Maintain enrichment success**: 100% enrichment rate should be preserved

## Implementation Approach

1. **Registry Expansion**: Add missing models to `gpu_specs.yaml` with appropriate specifications
2. **Normalization Updates**: Add corresponding entries to `CANONICAL_MODELS` and `GPU_REGEX_PATTERNS`
3. **AMD Detection**: Implement `_detect_amd_gpu()` function similar to Intel detection
4. **Validation**: Test against full Wamatek dataset and measure improvements

## Testing

Validate improvements using:
```bash
uv run glyphsieve pipeline --input tmp/wamatek_full.csv --output tmp/wamatek_full_score_filtered.csv --working-dir tmp/work --filter-invalid
```

Compare before/after metrics:
- Total fuzzy matches with score < 0.7
- Cross-vendor false positives
- Overall match type distribution
- Processing time and enrichment success rate

## Expected Impact

- **Improved Signal Quality**: Legacy GPUs will get proper canonical matches instead of noisy fuzzy matches
- **Better ML Preparation**: Cleaner training data for future ML classification tasks
- **Reduced Processing Noise**: Fewer low-confidence matches to investigate
- **Enhanced User Experience**: More accurate GPU identification and pricing

## References

- Parent Epic: [EPIC.refine.matching-accuracy.md](../../epics/closed/EPIC.refine.matching-accuracy.md)
- False Positive Analysis: [fp_set.csv](../../../glyphsieve/replay/fp_set.csv)
- Related Tasks: TASK.refine.01 (completed), TASK.refine.02 (completed)

---

**Priority**: High  
**Effort**: Medium  
**Impact**: High FP reduction, improved signal extraction  
**Labels**: [refine, legacy-gpu, fp-reduction, registry-expansion]

## ✅ Task Completed

**Changes made:**
- Added 21 legacy GPU models to `gpu_specs.yaml`: RTX 20 series, GTX 16 series, GT series, Quadro T series
- Updated `CANONICAL_MODELS` dictionary with comprehensive alternative naming patterns for all legacy models
- Added regex patterns to `GPU_REGEX_PATTERNS` for high-confidence matching of legacy GPUs
- Implemented `_detect_amd_gpu()` function to prevent AMD GPUs from fuzzy matching to NVIDIA models
- Integrated AMD detection into normalization flow alongside existing Intel detection

**Outcomes:**
- **Major FP reduction achieved:** Fuzzy matches decreased by 1,040 (46.8% reduction from 2,220 to 1,180)
- **Increased high-confidence matches:** Regex matches increased by 658 (15.8% increase from 4,176 to 4,834)
- **Better cross-vendor classification:** AMD and Intel GPUs now properly classified as UNKNOWN instead of false matching
- **Maintained enrichment success:** 100% enrichment rate preserved with 0 missing metadata entries
- **Improved signal quality:** Legacy GPUs now get proper canonical matches instead of noisy fuzzy matches

**Specific improvements:**
- GT 710/730/1030 cards: Now get regex matches instead of fuzzy matching to RTX 5070/H100
- GTX 1660 Ti cards: Now get regex matches instead of fuzzy matching to RTX 4060 Ti
- Quadro T1000 cards: Now get regex matches instead of fuzzy matching to A40
- AMD Radeon cards: Now classified as UNKNOWN instead of matching NVIDIA models
- RTX 20 series cards: Now have proper registry entries and matching patterns

**Impact on ML preparation:**
- **Cleaner training data:** 46.8% reduction in low-confidence fuzzy matches improves data quality
- **Better feature extraction:** More models have proper canonical classification for downstream analysis
- **Reduced noise:** Fewer false positive matches to investigate and filter out
- **Enhanced signal:** Legacy GPU pricing data now properly categorized and enriched

**Follow-up opportunities:**
- Consider adding more legacy models (GTX 10 series, older Quadro cards) if found in future datasets
- Monitor for other cross-vendor false positive patterns
- Use improved matching accuracy for ML classifier training data preparation