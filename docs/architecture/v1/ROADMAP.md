# GPU Scoring Tool — v 1 Roadmap

*(Last updated : 2025-07-29)*

---

## 🎯 Mission

Deliver a **fully-automated, end-to-end pipeline** that:

1. Ingests raw scraped GPU-pricing CSVs.
2. Cleans, deduplicates, enriches, quantizes, and scores each listing.
3. Persists results to a SQLite-backed FastAPI service (`glyphd`).
4. Exposes live data and basic analytics through a Next.js UI (`controlpanel`).
5. Provides the foundation for delta-based forecasting in a coming v 2.

---

## 🛣️ Phase Plan

| Phase                    | Objective                             | Key Tasks / Epics                                                 | Status                              |
|--------------------------|---------------------------------------|-------------------------------------------------------------------|-------------------------------------|
| **1. Pipeline FOO**      | CLI pipeline from CSV → scored report | `pipeline.*` tasks (clean, dedup, enrich, quantize, score, chain) | ✔ Complete                          |
| **2. API Persistence**   | FastAPI + raw-SQL SQLite store        | `persist.sqlite-store` epic (import, query, metadata)             | ✔ Complete                          |
| **3. REST Ingestion**    | Accept pipeline output via REST       | `EPIC.ingest.rest-import-api`                                     | 🟡 In progress (`import_id` wiring) |
| **4. Web Insights**      | Render scored data in UI              | `EPIC.web.frontend-ui-ux` (reports view, filters, E2E tests)      | 🟡 Queued                           |
| **5. Delta Forecasting** | Track price deltas over time          | `forecast.core-delta-history`                                     | 🔜 Next                             |
| **6. Full-Stack E2E**    | Golden-path regression suite          | `web.end-to-end-integration-test` + CI                            | 🔜 Next                             |

---

## 🔑 Success Criteria for v 1

- **One-command pipeline**  
  `uv run glyphsieve pipeline --input raw.csv --output scored.csv` produces lint-clean output.

- **Durable ingestion**  
  `POST /api/import` stores listings with `import_id` & timestamp; `GET /api/listings` returns filtered JSON.

- **Live insights UI**  
  `/reports` page shows model, price, score, quant capacity, heuristics; supports filter + sort; Playwright E2E passes.

- **Delta groundwork**  
  Snapshot + delta tables created; first delta record persists between successive imports.

- **Quality gate**  
  `ruff`, `flake8`, `black`, `isort`, `pytest`, Playwright, and Docker compose CI all green.

---

## 📈 Out-of-Scope (v 2 Targets)

- Category plugins (POWER9 servers, DPUs, etc.).
- Postgres or DuckDB storage options.
- Real-time websocket updates / push-based UI.
- Advanced forecasting models (ARIMA, Prophet, LLM-based signals).
- RBAC / multi-tenant auth.

---

*Prepared by: Timekeeper + Operator*  
*Date: 2025-07-29*

---

## 📌 Addendum: Status Summary as of 2025-08-01

### ✅ Completed (Beyond Original Roadmap)

- Title-based ML classifier (`is_gpu`) integrated into pipeline via modular `ml_signal.py`.
- Manual spot-check CLI for model disagreement review.
- Agent-driven dev loop (`.junie`) with process safety, task tracking, and dual-agent workflows.
- Frontend:
  - Generated OpenAPI client hooks via `tanstack-query`.
  - `/reports` page functional with live data and filtering.
  - Playwright integration tests pass for all views.
  - `docker-stack.sh` enables isolated frontend/backend dev.
- CLI:
  - Full `uv run glyphsieve pipeline` runs reliably end-to-end.
  - ML training, evaluation, and inference exposed via CLI.
- Quality Gate:
  - All tests (`pytest`, `Playwright`) pass.
  - Linting (`ruff`, `black`, `isort`, `flake8`) and CI-ready.
  - Typed DTOs, structured resource loading, and clear CLI surface.

### 🟡 Outstanding (v1 Hardening / Finalization)

- Delta forecasting tables and import comparison logic.
- Golden-path CI test suite (`web.end-to-end-integration-test`).
- Frontend polish:
  - Empty state rendering
  - Improved visual layout and mobile responsiveness
- ML v2 (stretch): Improved classifier trained on title-only + edge cases.
- UI-driven import execution or data upload (admin view).
- Additional report views (e.g., historical deltas, heatmaps).
- ADR for model-based enrichment and signal fusion.

---

## ✅ Definition of Done for v1

Version 1 of the GPU Scoring Tool is considered complete when the following criteria are satisfied:

- [ ] **Delta Forecasting Core**
  - Delta-aware tables implemented and verified
  - Imports compared chronologically with previous baselines
  - At least one scored listing shows price delta metadata

- [ ] **E2E Integration Test Suite**
  - End-to-end Playwright tests assert correct behavior across the stack
  - CI passes reliably against golden-path test data

- [ ] **Frontend Polish**
  - `/reports` page renders cleanly with empty states and mobile layout support
  - Common components styled for readability and minimalism

- [ ] **Operator Flow Improvements**
  - CLI-based import flow mirrors UI
  - Admin mode supports manual CSV uploads or re-runs

- [ ] **Signal Alignment**
  - ML v2 optionally integrated as secondary sieve signal
  - ADR published for long-term signal fusion + learning loops

Once all criteria are checked, v1 will be locked for stability and benchmarked across imported datasets.