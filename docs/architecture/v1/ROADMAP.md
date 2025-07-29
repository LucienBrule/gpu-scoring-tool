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

| Phase | Objective | Key Tasks / Epics | Status |
|-------|-----------|-------------------|--------|
| **1. Pipeline FOO** | CLI pipeline from CSV → scored report | `pipeline.*` tasks (clean, dedup, enrich, quantize, score, chain) | ✔ Complete |
| **2. API Persistence** | FastAPI + raw-SQL SQLite store | `persist.sqlite-store` epic (import, query, metadata) | ✔ Complete |
| **3. REST Ingestion** | Accept pipeline output via REST | `EPIC.ingest.rest-import-api` | 🟡 In progress (`import_id` wiring) |
| **4. Web Insights** | Render scored data in UI | `EPIC.web.frontend-ui-ux` (reports view, filters, E2E tests) | 🟡 Queued |
| **5. Delta Forecasting** | Track price deltas over time | `forecast.core-delta-history` | 🔜 Next |
| **6. Full-Stack E2E** | Golden-path regression suite | `web.end-to-end-integration-test` + CI | 🔜 Next |

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