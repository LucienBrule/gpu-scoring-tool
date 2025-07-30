# Task: Define and Tune Confidence Thresholds for Fuzzy Model Matching

## Objective

The goal of this task is to define and tune confidence thresholds for the fuzzy model matching step in the pipeline. This involves establishing a threshold value for the confidence score output by the fuzzy matching model, which determines whether a given match is accepted or rejected.

## Rationale

Tuning the confidence threshold is crucial to balance precision and recall in the matching process. A higher threshold can reduce false positives by filtering out low-confidence matches, but may also exclude some valid matches (reducing recall). Conversely, a lower threshold may increase recall but allow more false positives. The objective is to find an optimal threshold that suppresses false positives without significantly impacting the number of valid matches.

## Test File and Command

Use the following test file and command to run the pipeline and evaluate the effects of different threshold settings:

```
uv run glyphsieve pipeline --input tmp/wamatek_full.csv --output tmp/wamatek_full_score_filtered.csv --working-dir tmp/work --filter-invalid
```

## Acceptance Criteria

- The threshold logic for filtering fuzzy model matches is clearly defined and configurable in the codebase.
- The chosen threshold value is documented with an explanation of its selection and impact.
- The filtering reduces false positives without significantly reducing valid matches.
- Junie runs the pipeline with the new threshold settings, verifies accuracy improvements, and commits the updated code along with sample test outputs.
