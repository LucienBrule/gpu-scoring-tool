## EPIC: Frontend UI/UX for GPU Scoring Tool

### 🧠 Overview

The **Control Panel** in `web/apps/controlpanel/` is the public face of the GPU Scoring Tool.  
Its mission is to let operators — and eventually customers — browse live scorecards, compare historical listings, and
surface buying insights produced by the Python backend.  
Junie‑Web owns every pixel in this surface, from component library to Playwright coverage. The backend is consumed
exclusively through the generated OpenAPI client; Junie‑Web never edits backend code.

---

### 📦 Current State

| Capability                     | Status                                                     |
|--------------------------------|------------------------------------------------------------|
| Next.js 15 App Router scaffold | ✅ running & hot‑reloading                                  |
| Tailwind + shadcn/ui           | ✅ configured                                               |
| Generated client (`@client`)   | ✅ functional                                               |
| Health route (`GET /health`)   | ✅ wrapped & rendered                                       |
| Test split                     | ✅ `pnpm test:unit` (Vitest) / `pnpm test:e2e` (Playwright) |
| Full‑stack dev loop            | ✅ `.junie/scripts/docker-stack.sh up`                      |

---

### 🔭 Strategic Direction

#### 1️⃣ Bring the Frontend to Life

| ID                                     | Description                                                     | Acceptance                           |
|----------------------------------------|-----------------------------------------------------------------|--------------------------------------|
| `TASK.ui.01.add-navbar`                | Global navbar (Home / Reports / About) with responsive styling. | Links navigate without reload.       |
| `TASK.client.01.wrap-health-endpoint`  | React hook `useHealth()` using `@client` to poll `/health`.     | Unit test returns `"ok"`.            |
| `TASK.client.02.wrap-reports-endpoint` | Hook `useReports({ filters })` hitting `/reports`.              | Returns typed `GpuReportRow[]`.      |
| `TASK.ui.02.render-reports-view`       | `/reports` page displaying sortable table from `useReports`.    | Playwright test asserts rows render. |

#### 2️⃣ Support Discovery via OpenAPI

| ID                                                     | Description                                                                     |
|--------------------------------------------------------|---------------------------------------------------------------------------------|
| `TASK.discovery.01.generate-client-hooks-from-openapi` | Script scans `openapi.json`, emits typed hooks in `web/packages/client/hooks/`. |
| `TASK.discovery.02.list-consumable-endpoints`          | Markdown summary of GET routes ready for UI, committed to `docs/`.              |

#### 3️⃣ Build Strong Dev Loops

* **Codegen:** `pnpm run codegen` regenerates `web/generated/client-generated/` and re‑exports via `@client`.
* **Safe Processes:** Run long servers through `safe-run.sh`
  ```bash
  ./.junie/scripts/safe-run.sh -n controlpanel -b -- pnpm dev --filter controlpanel
  ./.junie/scripts/docker-stack.sh up   # backend + frontend
  ```
* **Testing:**
    - Fast feedback: `pnpm test:unit` (no backend needed)
    - Integration: `docker-stack.sh up` then `pnpm test:e2e`

---

### 🔧 Constraints

* **No raw `fetch()`** – always call the generated client.
* **`web/generated/` is read‑only.**
* Use Tailwind + shadcn/ui; keep shared components in `web/packages/ui`.
* All persistent processes must be launched via `.junie/scripts/safe-run.sh`.
* Playwright specs live in `apps/controlpanel/tests/integration/` and must clean up after themselves.

---

### ✅ Success Criteria

1. Navbar routes work on mobile & desktop.
2. `/reports` table displays live, paginated data via `useReports`.
3. `pnpm build --filter controlpanel` succeeds with zero TypeScript errors.
4. `pnpm test:unit` and `pnpm test:e2e` both pass locally & in CI.
5. Each completed task moves its file to `.junie/tasks/closed/` with a summary block.

---

### 🛠 Quick Commands

```bash
# Dev server (frontend only)
pnpm dev --filter controlpanel

# Full stack (backend + frontend)
./.junie/scripts/docker-stack.sh up   # stop with `down`

# Lint & format
pnpm lint --filter controlpanel
pnpm format --filter controlpanel
```

Happy shipping, Junie‑Web! 🚀