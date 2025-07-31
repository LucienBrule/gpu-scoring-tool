# EPIC: Refine Matching Accuracy and Pre-ML Classification Quality

## 🎯 Goal

Strengthen the accuracy of canonical model matching and ensure label quality before introducing ML-based classification. The goal is to reduce false positives, expand valid model coverage, and enhance registry precision—laying a clean foundation for ML pipelines.

---

## 📦 Why This Matters

Before training any classifier on `is_valid_gpu`, `model_id`, or other supervised tasks, our current match pipeline (regex + fuzzy) must:
- Avoid mislabeling Intel/Arc/Media encoders as GPUs
- Detect and capture real models like RTX 5000 Ada, A10, L40, A400, etc.
- Reduce “greedy” regex behavior causing misclassification
- Improve human interpretability of match reasoning (score bands, notes)

---

## 🧱 Tasks

### ✅ TASK.audit.01.sqloader
Add `SqlLoader` abstraction to unify schema loading under ResourceContext instead of using `Path(__file__)`. Improves testability and compliance.

### ✅ TASK.audit.02.no-path-file-only-resources
Ensure `Path(__file__)` is eliminated across the codebase in favor of proper `ResourceContext` abstraction.

### 🆕 TASK.refine.01.expand-gpu-registry
Add missing models to `gpu_specs.yaml` including:
- A10, A16, L40, L40S
- RTX 5000 Ada, RTX 2000 Ada, T400, A1000
- RTX PRO 6000 Blackwell
- RTX 4060–5090 (consumer cards)
Flag these for low scoring if needed, but label them correctly.

### 🆕 TASK.refine.02.patch-regex-patterns
Harden regex patterns to:
- Reduce FP matches from “A2” (Live Gamer), “A40” (Intel ARC), “A400” (low-end cards)
- Add assertions like `\b` or anchor terms
- Introduce ignore-lists or disambiguators for known false positives

### 🆕 TASK.refine.03.confidence-thresholds
Support CLI flag: `--min-confidence-score`. Records under this score are marked with `low_confidence = true`. Also document fuzzy score bands in output CSV.

### 🆕 TASK.refine.04.create-fp-replay-set
Create a test file `test/assets/fp_replay.json` containing known false positive titles. Use this to assert non-matching in unit tests for regex and fuzzy passes.

### 🆕 TASK.refine.05.annotate-match-notes
Extend match DTO to include:
- `match_notes: Optional[str]`
- `reason_filtered: Optional[str]`
These improve explainability and agent debugging.

### 🆕 TASK.refine.06.fix-missing-registry-warnings
Resolve missing model entries triggering enrichment warnings:
- `Model 'A100_40GB_PCIE' not found in GPU registry`
- `Model 'RTX_4000_SFF_ADA' not found in GPU registry`
These models must exist in `gpu_specs.yaml` to ensure clean enrichment.

---

## 🤖 ML Preparation Benefits

Once complete:
- We’ll have a reliable `is_valid_gpu` column for classifier training
- Match results will be clear, with less noise and fewer mislabeled entries
- Registry will support all observed real-world entries
- Agents (Junie, Goose) can operate on cleaner match surfaces and prepare training sets more confidently

---

## 🔚 Exit Criteria

- All known false positives neutralized or explained
- Registry expanded and reviewed
- Fuzzy match thresholds adjustable
- `test/assets/fp_replay.json` prevents regression
- Tasks above marked complete
- No enrichment warnings due to missing models in registry

---

Owner: Operator  
Status: IN_PROGRESS  
Labels: [refactor, matching, ml-prep, fuzzy, registry]

---

## 🧪 Test Command

Run the following to validate the full 10K Wamatek dataset:

```bash
uv run glyphsieve pipeline --input tmp/wamatek_full.csv --output tmp/wamatek_full_score_filtered.csv --working-dir tmp/work --filter-invalid
```