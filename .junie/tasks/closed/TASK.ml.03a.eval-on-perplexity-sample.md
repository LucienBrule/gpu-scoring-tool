## TASK.ml.08.eval-on-perplexity-sample

**Goal**: Evaluate the trained binary GPU classifier on the smaller Perplexity dataset (174 listings).

---
### Steps

1. Load the Perplexity dataset from `data/perplexity_raw.csv`. This file contains 174 scraped listings from Perplexity.
2. Apply the trained `gpu_classifier.pkl` to each row. Use the trained model at `models/gpu_classifier.pkl`.
    - Use the same preprocessing and prediction logic.
3. Output predictions to a new file: `data/perplexity_predictions.csv`
    - Include columns: `title`, `bulk_notes`, `ml_is_gpu`, `ml_score`
    - You may use a CLI entry point like:
    `uv run glyphsieve ml-eval --input data/perplexity_raw.csv --model models/gpu_classifier.pkl --output data/perplexity_predictions.csv`
4. Generate a short report:
    - Count `ml_is_gpu == 1`
    - List top 10 by `ml_score` descending
    - List any predictions with score ∈ [0.4, 0.6] (ambiguous zone)
    - Save summary to `data/perplexity_eval.yaml` and include counts of ambiguous, positive, and negative predictions.
5. (Optional): Manually verify a handful of borderline cases.


[perplexity_raw.csv](../../../data/perplexity_raw.csv)
---

### Success Criteria

- Perplexity dataset scored with ML predictions.
- Outputs written to `data/perplexity_predictions.csv`.
- Summary printed to console or saved as `perplexity_eval.yaml`.
- Top 10 predictions visually verified for plausibility.

---

### Notes

- Do not retrain — only evaluate.
- If you spot anomalies (e.g. capture devices flagged as GPUs), note them.
- Log any rows where predictions are unexpected or scores are near decision boundary.
- Ensure model input vectorization is compatible with the trained TF-IDF vectorizer.

## ✅ Task Completed

**Changes made:**
- Executed comprehensive evaluation of trained GPU classifier on Perplexity dataset (173 listings)
- Generated `data/perplexity_predictions.csv` with required columns: title, bulk_notes, ml_is_gpu, ml_score
- Created detailed `data/perplexity_eval.yaml` with statistics, top predictions, and ambiguous cases
- Provided legendary Dr. J.A.R. "Junie" Weber persona narration throughout analysis

**Outcomes:**
- **123 positive predictions (71.1%)** classified as GPUs with confidence scores 0.096-0.991
- **Top 10 predictions dominated by RTX 6000 Ada** (scores 0.985-0.991) showing model's clear preference
- **32 ambiguous cases identified** in 0.4-0.6 score range, primarily NVIDIA A40, RTX A4000, and A2 models
- **Systematic misclassification discovered**: H100 and L4 data center GPUs incorrectly rejected (scores <0.22)

**Lessons learned:**
- Model exhibits strong bias toward consumer/workstation GPUs vs enterprise/data center hardware
- Training data clearly focused on RTX/Quadro series, not AI/HPC accelerators
- TF-IDF + Logistic Regression approach works well within training domain but fails on out-of-distribution GPU types
- Context from bulk_notes significantly influences classification decisions

**Follow-up needed:**
- Consider retraining with expanded dataset including data center GPUs (H100, A100, L4)
- Investigate feature engineering to better capture enterprise GPU characteristics
- Manual review of A40 inconsistencies to understand context-dependent classification patterns