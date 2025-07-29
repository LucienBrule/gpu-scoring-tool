# TASK.models.cleanup-unify-gpu-registry

## Title
Remove redundant `gpu_models.yaml` and unify registry to use `gpu_specs.yaml`

## Status
Open

## Priority
High

## Assignee
Junie

## Tags
[registry, cleanup, models, yaml, gpu]

---

## 🧠 Context

We currently maintain two separate files that define GPU metadata:

- `gpu_specs.yaml`: canonical GPU specification dataset used throughout the enrichment pipeline
- `gpu_models.yaml`: an outdated, redundant copy used exclusively by the registry CLI

This violates the principle of a single source of truth and creates inconsistency across the system.

---

## 🎯 Goal

- Migrate the registry CLI (`registry.gpu-model-spec-schema`) to use `gpu_specs.yaml` instead of `gpu_models.yaml`
- Remove `gpu_models.yaml` from the codebase
- Ensure test coverage remains valid and passes
- Confirm that the CLI continues to list the correct models and schema is valid

---

## 🛠️ Tasks

- Refactor registry loading to use `gpu_specs.yaml`
  - Locate and update `registry.gpu-model-spec-schema` implementation to point at `gpu_specs.yaml`.
  - Remove references to `gpu_models.yaml` in code.
- Update field mappings:
  - Ensure `name`, `vram_gb`, `mig_capable`, `tdp_w`, `slots`, `connectivity` fields map correctly from `gpu_specs.yaml`.
  - Add validation to catch missing or renamed fields.
- Migrate or remove tests:
  - Update existing tests to refer to `gpu_specs.yaml`.
  - Add a fixture for `gpu_specs.yaml` sample data.
  - Delete any fixtures or tests referencing `gpu_models.yaml`.
- Remove `gpu_models.yaml` file from repository.
- Final verification:
  - Confirm CLI output matches sample entries.
  - Confirm no regressions in other subsystems.

---

## ✅ Acceptance Criteria

- CLI `registry list` outputs identical rows as before, sourced from `gpu_specs.yaml`.
- All CI checks pass: tests, linting, formatting.
- `gpu_models.yaml` is deleted and no longer referenced.
- Registry documentation updated to reflect new source file.

---

## Impact

This cleanup enforces a single source of truth for GPU metadata, reducing maintenance overhead and potential inconsistencies. Future enhancements to the GPU registry will be centralized in `gpu_specs.yaml`.

---

## 🧪 Dev & DX Loop

```bash
# Verify registry output
uv run glyphsieve registry list
# Run tests for registry and cleanup
pytest tests/test_registry.py
ruff check glyphsieve/src
isort glyphsieve/src
black glyphsieve/src
flake8 glyphsieve/src # IMPROTANT (will lint for architecture violations (GLS))
```
