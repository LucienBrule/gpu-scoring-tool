# TASK.ml.01.dataset-curation-annotate-isgpu

## Title
Dataset Curation & Annotation: is_gpu Labeling for Binary Classifier

## Epic
EPIC.ml.enrichment-pipeline-bootstrap

## Overview
This task initiates the ML enrichment pipeline by producing a training dataset for a binary classifier that determines whether a given listing represents a GPU or not.

We aim to support downstream classification by creating high-quality, human-verified annotations of real-world listing data from suppliers like Wamatek. This will serve as the foundational truth table for training a lightweight “Hotdog / Not Hotdog”-style detector.

## Goal
Curate and annotate a dataset of real product listings with an `is_gpu: [0,1]` label indicating whether each row is a GPU.

## Input
- `recon/wamatek/wamatek_sample.json`: already flattened array of Shopify product objects.
- Fields of interest: `title`, `tags`, `vendor`, `product_type`, `body_html`, `price`, and `variants`.

## Output
- `sample_isgpu.csv`: A CSV file where each row corresponds to a product, with relevant fields and a final `is_gpu` column.
- Each row must be manually or heuristically labeled with 1 (is GPU) or 0 (not a GPU).
- Optional: Use heuristics for initial labeling, but allow for manual correction and overrides.

## Implementation Notes
- Write a simple script or notebook to:
  - Load the flattened Wamatek JSON.
  - Extract relevant fields.
  - Apply simple heuristics to auto-label (`is_gpu = 1 if "RTX" or "NVIDIA" or "GPU" in title`).
  - Output a CSV with the above format.
- Manually review and correct a sample of at least 200 entries to ensure balanced representation.
- Count final label distribution in the CSV.

## Acceptance Criteria
- [ ] `sample_isgpu.csv` is committed to `recon/annotated/`.
- [ ] CSV contains a minimum of 200 labeled rows.
- [ ] Labels are approximately balanced (no more than 70/30 skew).
- [ ] Labeling script or notebook is committed to `tools/ml/` or `notebooks/`.
- [ ] Junie passes lint, test (if script), and includes a one-line summary of label distribution.
