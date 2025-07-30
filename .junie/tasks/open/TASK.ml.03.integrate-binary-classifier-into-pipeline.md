

# TASK.ml.03.integrate-binary-classifier-into-pipeline

## Title
Integrate binary GPU classifier into the glyphsieve pipeline

## Summary
This task integrates the trained binary classification model (developed in `TASK.ml.02`) into the glyphsieve pipeline. The classifier will serve as an early filtering step to distinguish GPU vs non-GPU entries, improving downstream normalization, enrichment, and scoring fidelity.

## Motivation
Many entries in marketplace datasets are irrelevant (e.g. RAM, accessories, unrelated SKUs) and pollute the pipeline. Fuzzy matchers occasionally yield false positives, and maintaining high recall leads to noisy outputs. A binary classifier provides an efficient, learned decision layer to gate entries before they proceed into the heavier pipeline stages.

## Acceptance Criteria

- [ ] Classifier is invoked as part of `glyphsieve.pipeline.clean` or `glyphsieve.pipeline.filter`.
- [ ] Entries identified as non-GPU are excluded or flagged appropriately (TBD: soft vs hard reject).
- [ ] Classifier decision is optionally written into output CSV as a `is_gpu: [0|1]` column.
- [ ] CLI exposes a flag to disable classification (e.g. `--skip-classifier`) for debugging and audits.
- [ ] Classifier must load from a stable, versioned model artifact (e.g. `.pt` or `.pkl`).
- [ ] Model loading and inference logic must be testable via unit tests.
- [ ] At least one end-to-end test demonstrates filtering effect (e.g. mixed Wamatek sample with known non-GPU entries).

## Reference Tasks

- [`TASK.ml.01.label-gpu-candidates`](./TASK.ml.01.label-gpu-candidates.md)
- [`TASK.ml.02.train-binary-gpu-classifier`](./TASK.ml.02.train-binary-gpu-classifier.md)

## Notes

- Consider deferring non-GPU entries to a `rejected/` folder or audit log for analysis.
- Log classifier confidence score alongside binary label for interpretability if available.
- If Torch is used, ensure `no_grad()` is wrapped around inference.