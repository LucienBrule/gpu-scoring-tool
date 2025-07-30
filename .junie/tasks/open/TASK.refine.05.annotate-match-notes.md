

# TASK.refine.05.annotate-match-notes

## Title
Add Annotation Field to Capture Match Heuristics and Notes

## Epic
EPIC.refine.labeling-accuracy

## Objective
Introduce a `match_notes` field during the normalization phase that captures insight into how a given match was determined — e.g., regex pattern used, fuzzy match source string, or disambiguation notes. This is meant to support transparency, later ML training, and debugging.

## Motivation
Currently, it is difficult to trace how a match was made during normalization. This makes it harder to evaluate false positives and refine the matching rules. Capturing a `match_notes` field in the normalized and enriched output will allow for better auditing, debugging, and machine learning signal attribution.

## Requirements
- Modify the normalization logic in glyphsieve to optionally emit a `match_notes` field alongside `canonical_model` and `match_type`.
- This field may include:
  - `"regex: matched pattern RTX_6000"`  
  - `"fuzzy: matched 'RTX Pro 6000' with score 0.72"`
  - `"manual override: supplier metadata"`
- Update DTOs and CSV writer logic to include the field.
- Ensure downstream stages in the pipeline (enrich, quantize, score) do not break if the field is present.
- If available, include the match_notes in the final output of the pipeline (optional).

## Deliverables
- Updated normalization logic with annotation support
- Updated output CSV schemas
- At least one test case confirming `match_notes` is present and meaningful
- No regressions in tests or output

## Handoff Instructions
- Run `uv run glyphsieve pipeline --input sample/sample_normalized.csv --output tmp/notes_test.csv --working-dir tmp/work`
- Visually inspect CSV for a `match_notes` column and validate its values
- Confirm tests pass and code is lint-clean

## Notes
- You may reference the heuristics from `normalizer.py` and `regex_model_matcher.py`
- Consider future extensibility: this field may later be ingested as part of training metadata