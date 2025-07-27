

## 🎯 Task: Add End-to-End Pipeline Execution to `glyphsieve` CLI

Junie, your task is to implement a new CLI command that chains together the core stages of the GPU data pipeline:

- cleaning
- normalization
- enrichment
- scoring
- insight report generation

This command will allow a user to process a scraped CSV file from start to finish using a single invocation.

---

## 🧪 Requirements

- Add a new `@app.command()` to the `glyphsieve.cli` named `pipeline`
- The command must accept:
  - `--input` (path to raw CSV)
  - `--output` (path to final scored CSV)
  - `--report` (optional path to insight report file)
  - `--debug` (flag to emit intermediate CSVs)
- The pipeline must:
  - Invoke the same logic used by existing CLI subcommands
  - Chain the output of each stage to the next
  - Use in-memory data passing when possible (avoid file IO where not required)
- Implement test coverage in `tests/cli/` using `CliRunner`
- If `--debug` is passed:
  - Emit intermediate CSVs to the output directory:
    - `01.cleaned.csv`
    - `02.normalized.csv`
    - `03.scored.csv`

---

## 🔄 Example

```bash
uv run glyphsieve pipeline \
  --input scrape/NVIDIA_A2/a2_raw.csv \
  --output analysis/a2_scored.csv \
  --report analysis/a2_report.md \
  --debug
```

---

## 🔍 Additional Notes

- This command should call into existing `clean`, `normalize`, `score`, and `generate-report` modules rather than duplicating logic.
- You must call these stages as internal functions, not subprocesses or CLI shell-outs.
- Output format should match the structure used in prior reports.
- You may reuse or wrap DTOs to pass in-memory between stages.

---

## ✅ Completion Criteria

- CLI command `glyphsieve pipeline` exists and accepts all expected flags
- The pipeline executes successfully on real scraped input
- All intermediate stages pass data in-memory when possible
- `--debug` files are emitted with numbered filenames if the flag is used
- Tests are present under `tests/cli/` using `CliRunner`
- Pipeline completion is verified with a scored CSV and optional report output