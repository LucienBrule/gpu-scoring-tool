

# TASK.pipeline.normalize-model-names.md

## 🧩 Task: Normalize Canonical GPU Model Names

Junie, your task is to implement the `normalize` subcommand of the `glyphsieve` CLI. This tool takes a cleaned CSV file (from the `clean` command), extracts the `title` field, and infers the most likely canonical GPU model name.

---

## 🎯 Objectives

- Add a `glyphsieve normalize` subcommand to the CLI.
- Input: CSV path with at least a `title` column.
- Output: CSV with added `canonical_model`, `match_type`, and `match_score` columns.

---

## 🧠 Matching Strategy

1. **Exact Match** — against a known map of canonical GPU names.
2. **Regex Heuristics** — for known series keywords (e.g., "A100", "4090").
3. **Fuzzy Matching** — use Levenshtein similarity via `rapidfuzz` to match model names approximately.

---

## 🧪 Output Columns

- `canonical_model`: standardized enum-like string (e.g., `RTX_A5000`)
- `match_type`: one of `exact`, `regex`, `fuzzy`, or `unknown`
- `match_score`: 1.0 for exact, ≤ 1.0 otherwise

If no match is found, use:
```csv
canonical_model,match_type,match_score
UNKNOWN,none,0.0
```

---

## 📦 Structure

- Logic in: `glyphsieve/src/glyphsieve/core/normalization.py`
- CLI entrypoint: `glyphsieve/src/glyphsieve/cli/normalize.py`
- Pattern definitions (optional): `glyphsieve/resources/gpu_models.json`

---

## 🧰 Dependencies

Add fuzzy matching dependency scoped to `glyphsieve`:
```bash
uv add rapidfuzz
```

---

## 🧪 Tests

- Add test cases in `glyphsieve/tests/` for:
  - Exact matches
  - Regex/heuristic matches
  - Fuzzy string inputs (e.g. "NVIDIA A 5OO0" → `RTX_A5000`)
  - No-match cases

Use `pytest` and either mock data or fixture CSVs.

---

## ✅ Completion Criteria

- Command runs via:
  ```bash
  uv run glyphsieve normalize --input file.csv --output output.csv
  ```
- Output CSV includes the new fields with correct values
- Test coverage is passing and readable
- Unmatched models are reported and handled gracefully

---

## ✍️ Notes

This task lays the foundation for GPU scoring and later valuation. The ability to reliably map real-world scraped `title` fields into `GpuSku` enums is central to the stack's downstream intelligence.

Close this task when complete and summarize notes or edge cases at the end.