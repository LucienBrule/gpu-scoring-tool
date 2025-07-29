# ADC 1 — Unified Resource Access & Full‑Stack Integration: **Glyphd ↔ Controlpanel**

| Item | Value |
|------|-------|
| **Status** | **Accepted** |
| **Decision Date** | 2025‑07‑28 |
| **Applies to Version / Tag** | `v0.1.0‑integration‑passed` |
| **Authors / Reviewers** | Core maintainers of `gpu‑scoring‑tool` |

---

## 1  Context

Before this milestone the GPU Scoring Tool prototype suffered from a collection of systemic integration issues:

| Pain‑point | Symptoms / Risks |
|------------|-----------------|
| **Hard‑coded file paths** | `Path(__file__).parent / "../../../glyphsieve/resources"` leaked implementation details, broke container builds, and crossed bounded‑context lines. |
| **Monolithic FastAPI router** | A single `router.py` contained unrelated endpoints, complicating ownership and testability. |
| **Mock‑heavy tests & weak E2E story** | Playwright tests asserted DOM only, bypassing the generated OpenAPI client; many pytest cases mocked internals instead of exercising real flows. |
| **Docker proxy friction** | The Next.js frontend (controlpanel) required CORS work‑arounds and manual port tweaking to reach glyphd in Docker. |
| **Inconsistent OpenAPI** | Route prefixes (`/api/api/...`) and DTO drift made the Swagger contract unreliable. |

Collectively these problems impeded feature velocity and threatened reliability as feature work accelerated toward **v1**.

---

## 2  Decision

We adopted a cohesive **“resource‑context + modular boundary”** architecture:

1. **Domain‑aware `ResourceContext` abstraction**
    * Introduced `BaseResourceContext` dispatching by file extension (`.yaml`, `.csv`, `.md`) and enforcing DTO type safety.
    * Added abstract loaders (`BaseYamlLoader`, `BaseCsvLoader`, `BaseMarkdownLoader`) that resolve files via `importlib.resources.files()`.
    * Implemented concrete variants:
        * `GlyphSieveYamlLoader`, `GlyphSieveCsvLoader` (inside `glyphsieve`)
        * `GlyphdYamlLoader`, `GlyphdCsvLoader` (inside `glyphd`)
    * Result: no code in glyphd or glyphsieve accesses package internals via paths.

2. **Modular FastAPI routers**
    * Split the former monolith into `api/routes/health.py`, `listings.py`, `models.py`, `report.py`.
    * Registered under a single “root” router with prefix `/api`, eliminating double prefixes.

3. **End‑to‑end test realism**
    * Regenerated OpenAPI client (`@openapitools/typescript-fetch`) and forced Playwright tests to consume it.
    * Rewrote legacy pytest cases to hit the real loaders instead of stubbing file paths; introduced fixture CSV/YAML resources where necessary.

4. **Docker Compose reliability**
    * Assigned deterministic service names (`glyphd`, `controlpanel`) and hostnames.
    * Added nginx‑style proxy logic in Next.js dev server (via `NEXT_PUBLIC_INTERNAL_API_HOST`) so the browser talks to `http://glyphd:8080` inside the compose network without CORS.
    * Health‑check endpoints (`/api/health`, `/internal-api/health`) wired to Compose `healthcheck` primitives for fast feedback.

---

## 3  Consequences

| Area | Outcome |
|------|---------|
| **Tests** | ✅ **74 / 74 pytest tests pass** in 6 s. |
| **E2E** | ✅ **1 / 1 Playwright test passes** (chromium). |
| **Static analysis** | Ruff + Black + isort clean; custom lints GLS001–GLS005 satisfied. |
| **OpenAPI** | `/openapi.json` validates (OAS 3.1); no duplicate prefixes. |
| **Runtime** | `docker compose up --build` launches working stack; Swagger UI, Next.js integration page, and `/integration-test` confirm live data flow. |
| **Maintenance** | DTOs and resources now decoupled; additional resource types/actions can register loaders without touching callers. |

---

## 4  Trade‑offs & Constraints

| Topic | Notes |
|-------|-------|
| **Mock strategy** | Tests now patch `ResourceContext.loader_for()` instead of `open()`‐calls; clearer but marginally more verbose. |
| **Markdown parsing** | `insight.md` still parsed via ad‑hoc regex; slated to migrate to YAML or database in **v2**. |
| **Pydantic warnings** | Config deprecation warnings (class‑based `Config`) remain; will be handled during the planned Pydantic v3 migration. |
| **Loader registration cost** | Each new resource extension requires a loader class and registration—acceptable for the current team size and explicitness. |

---

## 5  Impact & Future Work

* **Foundation for v2 plugin architecture** — The context/loader pattern will generalise to “category plugins” (GPU ≫ CPU ≫ ASIC etc.) without path rewrites.
* **Stronger change safety** — OpenAPI + generated clients + E2E create a contract harness for refactors.
* **Dev‑prod parity** — Dockerised stack mirrors CI; contributors can run `make dev` and obtain identical behaviour.
* **Migration vectors** — Resource locations can later move to S3 or a DB by swapping loader implementations; FastAPI route modules can be version‑tagged for backwards compatibility.

---

## 6  References

| Item | Link / Value |
|------|--------------|
| **Git tag** | `v0.1.0-integration-passed` |
| **Key commit** | `baf3e8c “feat(integration): finalize glyphd ↔ controlpanel API integration”` |
| **Subsystems touched** | `glyphd`, `glyphsieve`, `web/apps/controlpanel`, `.docker/`, `tests/`, `.ci/` |
| **Exemplar E2E test** | `web/apps/controlpanel/tests/integration/health.spec.ts` |
| **Swagger UI** | `http://localhost:8080/docs` (after compose up) |
| **OpenAPI JSON** | `http://localhost:8080/openapi.json` |
| **Pytest report** | 74 passed – see CI artifact `pytest-report.html` |
| **Playwright HTML report** | see CI artifact `playwright-report/index.html` |

---

## 7  Decision

**We accept this architecture as the baseline for all subsequent development (v0.1.x ➜ v1).**  
The milestone resolves critical integration debt, institutes enforceable boundaries, and provides confidence via comprehensive automated verification.