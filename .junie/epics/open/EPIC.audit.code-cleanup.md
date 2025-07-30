# EPIC: Audit & Code Cleanup

## Summary

This epic captures a structured code quality audit pass across the `gpu-scoring-tool` codebase. It includes architectural consistency checks, refactor surfacing, lint conformance, and resource loading correctness. These tasks aim to ensure the codebase remains agent-operable, semantically clean, and resilient to scale.

## Motivation

Following the successful integration and deployment of the `persist.sqlite-store` epic, we identified several quality-of-life issues and refactors that will improve the long-term maintainability and symbolic coherence of the system. This includes removing lingering uses of `Path(__file__)`, inconsistencies in how `.sql` and `.yaml` resources are loaded, and opportunities to enforce uniform resource access via `ResourceContext`.

This epic also prepares the system for parallel agent contribution by minimizing surface-level ambiguity or redundancy.

## Scope

- Lint and complexity warnings cleanup
- Proper resource resolution across `.sql`, `.yaml`, `.json`, and `.csv`
- Elimination of direct path manipulations in favor of contextualized loaders
- Preparation for Junie + Goose parallelization
- Optional introduction of a `SqlLoader` using `importlib.resources`

## Tasks

- `TASK.audit.01.sqloader.md` – Introduce `SqlLoader` class to resolve `.sql` files via `importlib.resources` and integrate with `ResourceContext`.
- `TASK.audit.02.no-path-file-only-resources.md` – Sweep codebase for direct `Path(__file__)` or manual file path logic and refactor to use appropriate resource loading patterns.

## Agent Notes

Junie and Goose may both run in parallel on this epic in the future. Ensure tasks are non-overlapping and limited in scope. Each task should update the epic with a short note upon completion.

## Acceptance Criteria

- All audit tasks completed
- No remaining uses of `Path(__file__)` or manual relative paths
- All resources accessed via context-aware loader
- Lint: `flake8`, `ruff`, `black`, `isort` all pass cleanly
- Future agents can operate without guesswork or local filesystem assumptions

## Owner

Operator: Lucien Brulé  
Daemon: Solien
