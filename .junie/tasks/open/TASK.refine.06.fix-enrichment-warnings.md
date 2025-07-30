

# TASK.refine.06.fix-enrichment-warnings

## Title

Fix Enrichment Warnings for Unregistered Models

## Epic

EPIC.refine.model-normalization-matching

## Goal

Eliminate spurious enrichment warnings emitted during pipeline execution by ensuring all matched models are properly registered in the GPU registry and any misaligned matches are corrected.

## Background

The enrichment stage currently logs warnings when matched models (from normalization or fuzzy matching) are not found in the GPU registry. For example:

- `Model 'A100_40GB_PCIE' not found in GPU registry`
- `Model 'RTX_4000_SFF_ADA' not found in GPU registry`

These warnings indicate either:
- The registry is missing known models that *should* be registered.
- The matcher is emitting incorrect model keys due to fuzziness or outdated regex.

These discrepancies erode trust in the pipeline’s output and prevent score propagation.

## Tasks

- [ ] Audit recent enrichment runs (e.g. `tmp/wamatek_full.csv`) and collect all unique models that triggered warnings.
- [ ] Categorize each warning as either:
  - ❗ *Missing model that should be registered* → Add it to the registry.
  - ⚠ *Spurious match (false positive)* → Fix the matching rule or regex.
- [ ] For each ❗ case, ensure the new model has a valid `GPUModelDTO` entry.
- [ ] For each ⚠ case, update `canonical_model_map.yaml` and/or regex rules.
- [ ] Add test fixture(s) with known-to-warn models to assert clean enrichment.

## DX Notes

- To trigger the warnings:

```bash
uv run glyphsieve pipeline \
  --input tmp/wamatek_full.csv \
  --output tmp/wamatek_full_score_filtered.csv \
  --working-dir tmp/work \
  --filter-invalid
```

- Relevant files:
  - `glyphsieve/core/matching/`
  - `glyphsieve/resources/gpu_specs.yaml`
  - `glyphsieve/resources/canonical_model_map.yaml`
  - `glyphsieve/tests/test_enrichment.py`

## Success Criteria

- No enrichment warnings for common FP/FN matches.
- Registry fully contains all known matched models.
- Model normalization pipeline cleanly aligns enrichment, scoring, and reporting steps.

## Tags

lint:gls005  
quality:high  
priority:medium  
requires:registry