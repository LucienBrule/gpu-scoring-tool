

# EPIC: Enrichment ML – GPU Binary Classifier & Semantic Reranker

## Summary

This epic introduces a lightweight machine learning subsystem into the GPU Scoring Tool pipeline. The goal is to improve the accuracy of GPU detection and matching during normalization and enrichment phases using a hybrid approach: binary classification and semantic reranking.

## Motivation

The current normalization pipeline relies heavily on heuristic string matching and rule-based logic. While effective in most cases, it may yield false positives (misclassifying non-GPU items) and miss subtle variants of known GPU models. By adding a learning-based filter layer, we can improve robustness and generalizability, especially as data sources grow more heterogeneous (e.g. Shopify JSON from vendors like Wamatek).

## Goals

- ✅ Train a binary classifier to detect whether a listing likely refers to a GPU.
- ✅ Generate a UUID per row and carry it through the pipeline for traceability.
- ✅ Optionally embed listing metadata (title, notes, region, seller) and rerank potential GPU matches via cosine similarity.
- ✅ Integrate these models into the enrichment pipeline with minimal dependencies and fast inference.

## Tasks

- [ ] TASK.ml.01.dataset-curation-annotate-isgpu.md
- [ ] TASK.ml.02.train-lightweight-binary-classifier.md
- [ ] TASK.ml.03.integrate-binary-classifier-into-pipeline.md
- [ ] TASK.ml.04.train-embedding-reranker.md
- [ ] TASK.ml.05.fallback-path-for-unknowns.md

## Architecture

- Classifier input: Cleaned listing row (title, seller, price, etc).
- Output: `is_gpu: bool` prediction with confidence score.
- Embedding model: SentenceTransformer (e.g. `all-MiniLM-L6-v2` or lighter).
- Output reranker: cosine distance match against canonical GPU embeddings.

## Impact

This will reduce false positives, enable scalable source ingestion, and provide a clear semantic firewall before downstream enrichment stages. It also enables future multi-agent (Goose/Junie) parallelization and provenance-aware feedback loops.

## Owner

This epic is owned by the Operator (Lucien) and will be primarily implemented by Junie, with support from Goose in future embedding/model orchestration tasks.
