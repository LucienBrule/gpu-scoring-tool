

# v1 Architecture – GPU Scoring Tool

This document describes the current architecture of the GPU Signal Scoring system as implemented in `v1`. It defines the structure, responsibilities, and flow of data through the system as it exists prior to the introduction of plugin-based modularization in `v2`.

---

## 🧠 Architectural Overview

The `v1` architecture is a monolithic yet cleanly organized implementation. Its focus is a **vertically complete pipeline for GPU listings**, from raw CSV scrape to scored and report-ready output.

---

## 🗂️ Key Components

### 1. `glyphsieve` (Python / CLI)
- Implemented as a `uv` Python package
- Built with `Click` for CLI orchestration
- Contains pipeline commands:
  - `clean`, `dedup`, `normalize`, `enrich`, `score`, `tag`, `report`, and `pipeline` (multi-step)
- Includes:
  - `models/` – Pydantic DTOs for listings
  - `core/` – Core logic per stage
  - `resources/` – Scoring weights, model specs
  - `tests/` – Unit tests for each pipeline stage

### 2. `glyphd` (Python / FastAPI)
- Also a `uv` Python project
- Loads scored CSV output from `glyphsieve`
- Exposes OpenAPI-compatible endpoints:
  - `/listings`
  - `/reports`
  - `/health`
- Used to generate a TypeScript client SDK

### 3. Web Frontend (TurboRepo / Next.js)
- Located in `web/apps/controlpanel`
- Uses OpenAPI-generated TS client from `packages/client`
- Displays score charts, insights, and integrates with backend API
- Built with Tailwind + TypeScript + Playwright tests

### 4. Reporting & Visualization (`sieveviz`)
- Contains historical CSVs and reports
- Used to generate matplotlib/plotly-style insight charts
- Not yet integrated into FastAPI/web pipeline (handled manually)

---

## 🔄 Data Flow

```
  CSV scrape →
  glyphsieve clean →
  normalize →
  enrich (with heuristics + specs) →
  score →
  report →
  scored CSVs →
  glyphd loads →
  controlpanel renders
```

All tasks are testable via CLI, `pytest`, and web integration testing (Playwright).

---

## 🎯 Goals of v1

- Prove vertical signal extraction stack for GPUs
- Validate scoring, normalization, and insight pipeline
- Ensure FastAPI ↔ TypeScript SDK ↔ Web integration works
- TDD pipeline foundation for future categories

---

## 🔜 Planned for v2

This v1 stack will soon evolve into a **plugin-loaded runtime** where:
- Categories (GPU, DPU, Server) are defined as discrete plugins
- `glyphd` becomes an interface-driven daemon with hotloaded category support
- Pipelines are dynamically routed via `--category` or API

See: [../v2/README.md](../v2/README.md)