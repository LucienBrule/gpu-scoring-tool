

# TASK.ml.05.fallback-path-for-unknowns

## Title

Implement fallback classification path for unknown or noisy entries during GPU identification.

## Context

The current normalization and enrichment pipeline may falsely identify non-GPU items or fail to resolve ambiguous entries. This results in polluting the scored dataset with irrelevant or misclassified entries. While `UNKNOWN_GPU` is a valid sentinel, we need a stronger fallback mechanism to gracefully catch edge cases and guide future improvements.

This task builds upon the embedded reranker (`TASK.ml.04.train-inference-reranker`) and is a prerequisite for future unsupervised cluster analysis of noisy GPU markets.

## Goals

- Define and implement a `FallbackClassifier` interface.
- Train or hardcode a simple classifier that takes in fuzzy metadata (title, seller, region, price) and predicts `is_gpu` as a binary flag.
- If prediction is `False`, skip or mark the entry with a new metadata tag: `{"rejected": true, "reason": "not_gpu_predicted"}`.
- Integrate this fallback after normalization but before enrichment or scoring.
- Update pipeline CLI to log fallback decision stats.

## Implementation Notes

- Use `scikit-learn`, `sentence-transformers`, or similar minimal tooling.
- Classifier can be bootstrapped with a small hand-labeled corpus and refined iteratively.
- In the future, upgrade to support uncertainty scores or similarity thresholds with known embeddings.
- Flag edge cases for review and future tuning.

## Acceptance Criteria

- Running `glyphsieve pipeline` on dirty data logs total rejected rows and fallback rate.
- At least 1 real-world test case is caught and flagged as `rejected`.
- Code is typed, tested, and lint-clean.
- No fallback logic bleeds into scoring models or contaminates valid entries.

## Related Tasks

- `TASK.ml.04.train-inference-reranker`
- `TASK.ml.03.annotate-is-gpu-labels`
- `TASK.loader.03.load-shopify-wamatek-json`

## Priority

High – this is critical for data quality and system trust.