

# TASK.ml.04.train-embedding-reranker

## Title
Train Embedding-Based Reranker for Semantic GPU Listing Resolution

## Context

In the enrichment pipeline, fuzzy matching is currently rule-based and prone to false positives. We intend to supplement or replace this mechanism with a semantic reranker that uses learned embeddings to improve the resolution of listing → canonical GPU model assignments.

This reranker will use pre-trained sentence transformers (e.g. `all-MiniLM-L6-v2`) or similar lightweight models to embed title, vendor, and description fields. It will learn to differentiate true vs. false matches based on cosine similarity between listing embeddings and canonical model descriptors.

This task builds upon:

- `TASK.ml.01.annotate-training-data`
- `TASK.ml.02.train-binary-gpu-classifier`
- `TASK.ml.03.extract-embedding-features`

## Goals

- Build a reranker model that improves top-1 prediction accuracy of listing-to-model assignment.
- Output a probability/confidence score for each canonical candidate per listing.
- Reduce false positives from fuzzy heuristics.

## Inputs

- Annotated listing examples (`is_gpu=1`) from prior tasks
- Canonical GPU specs from the registry (via `GPUModelDTO`)
- Embeddings extracted for both (via `TASK.ml.03.extract-embedding-features`)

## Deliverables

- A training script under `glyphsieve/ml/reranker_train.py` or equivalent
- A saved `reranker_model.onnx` or Torch `.pt` file
- Inference utility: `predict_match_score(listing_embedding, candidate_embeddings) -> ranked list`
- Evaluation report with metrics (precision@1, recall@3, ROC-AUC, etc.)

## Considerations

- Must work with cosine similarity or optionally train a small MLP on top of embeddings
- Should be small enough to run in production context (e.g. < 50ms inference)
- May require balancing dataset to avoid overfitting to popular models

## Acceptance Criteria

- ✅ Reranker script trains without errors on preprocessed embedding dataset
- ✅ Evaluation metrics are saved to `reports/reranker_metrics.json`
- ✅ Inference module can be imported and used by enrich pipeline
- ✅ Top-1 canonical match accuracy improves over baseline fuzzy matcher by ≥15%
- ✅ All code passes lint, ruff, pytest

## Related

- EPIC.ml.reranking-augmentation
- TASK.ml.01.annotate-training-data
- TASK.ml.02.train-binary-gpu-classifier
- TASK.ml.03.extract-embedding-features