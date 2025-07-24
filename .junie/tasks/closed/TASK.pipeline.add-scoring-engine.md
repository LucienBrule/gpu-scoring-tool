# TASK.pipeline.add-scoring-engine.md

## 🧩 Task: Implement GPU Scoring Engine

Junie, your task is to implement a `score` subcommand for the `glyphsieve` CLI that assigns a composite utility score to each GPU listing. The scoring model should reflect practical inference value and operational desirability, not just MSRP or performance hype.

---

## 🎯 Objectives

- Add a `glyphsieve score` CLI subcommand
- Accept an input CSV with enriched listings (must include metadata such as `vram_gb`, `tdp_watts`, `mig_support`, etc.)
- Output a CSV with an appended `score` column

---

## 🧠 Scoring Heuristics (Initial Model)

Implement the scoring function as a weighted additive model using fields such as:
- VRAM (normalized)
- MIG support (binary or partition count)
- NVLink (binary)
- TDP (inverse power scaling)
- Price (normalized against MSRP or market median)

The scoring weights should be:
- Defined using a Pydantic model (e.g. `ScoringWeights`)
- Loadable from a `resources/scoring_weights.yaml` file by default
- Optionally overridable at runtime by passing a `ScoringWeights` object

You should implement the scoring engine using the **Strategy Pattern**:
- Define an abstract scoring interface using `abc.ABC`
- Implement the initial weighted additive model as a concrete subclass
- Allow CLI or future invocations to select from different scoring strategies dynamically
- This enables future extensions like rack-efficiency scoring, quantization-fit scoring, or resale valuation scoring

This ensures scoring logic is clean, configurable, testable, and modular for future growth.

---

## 📦 Structure

- Scoring logic: `glyphsieve/src/glyphsieve/core/scoring.py`
- CLI command: `glyphsieve/src/glyphsieve/cli/score.py`
- Optional: scoring weight constants or config in `resources/scoring_weights.yaml`

---

## 🧪 Output

- Appends a `score` column (float, 0.0–1.0 scale)
- Prints a few top/bottom cards after scoring for debug visibility
- Writes output CSV to file or stdout

---

## 🧪 Tests

- Validate scoring logic against controlled enriched input
- Ensure edge cases (missing fields, zero TDP) are handled gracefully
- Provide tests in `glyphsieve/tests/test_scoring.py`

---

## ✅ Completion Criteria

- `uv run glyphsieve score --input enriched.csv --output scored.csv` works
- `score` column appears in output
- Code is modular, testable, and robust
- Tests pass via `uv run pytest`

---

## ✍️ Notes

This completes the core arc: clean → normalize → enrich → score. Junie may adjust weighting logic or scoring components based on system feedback or improvements.

---

## ✅ Task Completion Summary

I've successfully implemented the GPU scoring engine with the following components:

1. Created a `ScoringWeights` Pydantic model for configurable scoring weights
2. Implemented the Strategy Pattern with an abstract `ScoringStrategy` class and a concrete `WeightedAdditiveScorer` implementation
3. Added a `score_csv` function that loads a CSV, scores it, and writes the output
4. Created a YAML configuration file for default scoring weights
5. Implemented the CLI command with options for input/output files and custom weights
6. Added comprehensive tests for all components, including edge cases
7. Verified that the implementation meets all completion criteria

The scoring engine successfully assigns scores between 0.0 and 1.0 to GPU listings based on their VRAM, MIG support, NVLink capability, TDP, and price. The implementation is modular, testable, and robust, with proper error handling and documentation.