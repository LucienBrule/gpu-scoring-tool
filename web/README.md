# GPU Scoring Tool – Frontend

A Next.js (`app/` router) UI powered by **Turborepo** + **pnpm**.  
This app (codename **Control Panel**) visualises pricing and scoring data from the GPU Scoring Tool backend via a generated OpenAPI client.

---

## 🧠 Project Overview

* **Apps** live in `web/apps/` – today that’s just **`controlpanel/`**.  
* **Packages** live in `web/packages/` – shared UI components (`ui`), a thin client wrapper (`client`), etc.  
* **Generated code** lives in `web/generated/client-generated/` and is **read‑only**.

The frontend **never** modifies backend code or Python resources. It *consumes* the API only through the generated client.

---

## 📁 Directory Structure

| Path                              | Purpose                                                     |
|-----------------------------------|-------------------------------------------------------------|
| `web/apps/controlpanel/`          | Next.js frontend (TypeScript + Tailwind CSS)                |
| `web/packages/ui/`                | Shared React component library (shadcn/ui, Tailwind)        |
| `web/packages/client/`            | Manual wrapper that re‑exports the generated OpenAPI client |
| `web/generated/client-generated/` | Auto‑generated API client – **do not edit**                 |

---

## ⚙️ Dev & Build Workflow

```bash
# One‑off install
pnpm install

# Start the dev server (foreground)
pnpm dev --filter controlpanel

# …or start it safely in background via Junie helper
./.junie/scripts/safe-run.sh -n controlpanel -b -- pnpm dev --filter controlpanel

# Stop the background process
./.junie/scripts/safe-run.sh -k controlpanel

# Build for production
pnpm build --filter controlpanel

# Lint & format
pnpm lint --filter controlpanel
```

*No `uv`, no Python, no Docker is required for typical frontend work.*

---

## 🧪 Testing

| Type                | Location                                   | Command                    |
|---------------------|--------------------------------------------|----------------------------|
| Unit / component    | `*.test.ts(x)` within `apps/controlpanel/` | `pnpm test:unit`           |
| E2E / integration   | `apps/controlpanel/tests/`                 | `pnpm test:e2e`            |

Unit tests do not require the backend to be running. E2E tests require `http://localhost:8080` to be reachable.

▶️ **E2E Backend Requirement**

Playwright tests require the backend API to be running at **`http://localhost:8080`**.  
You **must** start the backend before running integration specs:

```bash
# From monorepo root:
docker compose up -d --build glyphd
```

Junie must never run the backend manually via `uv`. Always use Docker for consistent test environments.

---

## 📦 API Client Usage

```ts
import {ListingsApi} from '@client/generated';

const api = new ListingsApi();
const {data} = await api.listListings();
```

* Never edit files inside `web/generated/client-generated/`.  
* If the backend schema changes, run `pnpm run codegen` from the monorepo root to regenerate.

---

## ✔️ Done Checklist

A change is **ready to merge** when:

1. `pnpm build --filter controlpanel` completes without errors.  
2. `pnpm test:unit` and `pnpm test:e2e` pass (unit + Playwright).  
3. `pnpm lint --filter controlpanel` reports zero issues.  
4. Any associated Junie task is moved to `.junie/tasks/closed/` with a completion summary.

Happy shipping! 🚀