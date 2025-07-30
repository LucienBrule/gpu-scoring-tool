# TASK.refine.04.create-fp-replay-set

## Title
Create False Positive Replay Set from Wamatek Dataset

## Context
During full dataset testing (`tmp/wamatek_full.csv`), a number of false positives were detected in model matching. These include misclassifications by both the regex and fuzzy systems.

To support reproducible debugging and future regression testing, we need a replayable test fixture containing the misclassified rows, complete with original input fields and expected match corrections.

## Goals
- Create a CSV or JSON file containing a curated set of ~50–100 false positives.
- Annotate each row with:
  - Original raw model name
  - Incorrectly matched canonical name
  - Suggested correct behavior (e.g., `should_be: "Unknown"`, or correct model string)
  - Source supplier (e.g. "Wamatek")
- Add this to a new directory: `glyphsieve/replay/fp_set.csv`

## Acceptance Criteria
- ✅ File exists at `glyphsieve/replay/fp_set.csv`
- ✅ Contains a representative variety of FPs (see `tmp/wamatek_full_score_filtered.csv`)
- ✅ Annotated correctly with intent and observed output
- ✅ Passes manual spot check by Operator
- ✅ Documented in README if needed

## Notes
This will be useful for:
- Future test harness development
- ML-assisted refinement (labeling)
- Regex/fuzzy scoring benchmarks
