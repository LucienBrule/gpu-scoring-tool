# Junie‑Web Guidelines (v0.2.0)

Welcome, Junie‑Web!  
These rules apply **only** to the `web/` workspace of the monorepo. Your entire universe is the Turbo/Next.js frontend;
everything Python‑side is invisible to you.

---

## 🧠 Project Overview

The frontend is a **Next.js (App Router)** application living in a *Turborepo* workspace managed by **pnpm**.  
Junie‑Web’s job is to:

1. Evolve UI/UX in `web/apps/controlpanel/`.
2. Maintain shared UI and client logic in `web/packages/`.
3. **Consume (never edit) the auto‑generated OpenAPI client** in `web/generated/`.
4. Keep tests, linting, and type‑safety green at all times.

---

## 📁 Directory Structure

| Path                     | What it contains                                       | Edit policy   |
|--------------------------|--------------------------------------------------------|---------------|
| `web/apps/controlpanel/` | Main Next.js app (routes, pages, components, Tailwind) | **Yes**       |
| `web/packages/`          | Shared libraries (`ui`, `client`, etc.)                | **Yes**       |
| `web/generated/`         | OpenAPI‑generated TypeScript client                    | **Read‑only** |

> **Tip:** Need a new package? Create it under `web/packages/` and wire it via Turborepo workspaces in `package.json`.

---

## ⚙️ Tooling & Runtime

| Purpose          | Command                            |
|------------------|------------------------------------|
| Dev server       | `pnpm dev --filter controlpanel`   |
| Production build | `pnpm build --filter controlpanel` |
| Unit tests only  | `pnpm run test:unit`               |
| Lint & format    | `pnpm lint`                        |

### Safe background runs

Use `.junie/scripts/safe-run.sh` instead of raw foreground processes:

```bash
# Start dev server in background
./.junie/scripts/safe-run.sh -n controlpanel -b -- pnpm dev --filter controlpanel

# Stop it later
./.junie/scripts/safe-run.sh -k controlpanel
```

*No* `uv`, *no* Python, *no* Docker required for normal frontend work (unless explicitly tasked).

### Using saferun with the dockerstack command

Use '.junie/scripts/dockerstack.sh' to interact with a wrapped version of docker compose.
```bash
# Start the stack and build
./.junie/scripts/safe-run.sh -n dockerstack -b -- .junie/scripts/docker-stack.sh up --build

# Inspect logs from the stack output
tail -n 20 .junie/logs/dockerstack.log 

# Wait for approximately 30 seconds (if building)
sleep 30

# Inspect the logs from the stack output again (to make sure its running)
tail -n 20 .junie/logs/dockerstack.log 

# Stop it later
./.junie/scripts/safe-run.sh -n dockerstack -b -- .junie/scripts/docker-stack.sh down
```

The docker stack supports hot reloading of code on change via volume mount. You do not necessarily need to rebuild on code changes.
If you make a large change or need to reinstall node_modules, you may find you need to restart the stack (down and up)
---

## 🧪 Testing

- **Unit tests**: colocate `*.test.ts(x)` next to components in `apps/controlpanel/`.
- **Playwright specs** (integration tests): live under `apps/controlpanel/tests/` and require the backend to be running.
- You can run unit tests only with:

```bash
pnpm run --filter controlpanel test:unit
```

> Junie‑Web must run **only unit tests** by default.  
> Do **not** run Playwright integration tests (`test:e2e`) unless explicitly instructed by the task.

- All tests must pass in CI and locally before closing a task:

```bash
pnpm run --filter controlpanel test:e2e       # Playwright integration tests (backend must be running)
pnpm run --filter controlpanel test:unit      # Component/unit tests only
```

### Playwright Usage Guidelines

When using Playwright for integration testing or debugging:

- **Screenshots are not supported** in this environment. Do not attempt to use `page.screenshot()` or similar methods for debugging.
- Use Playwright's accessibility snapshot (`browser_snapshot`) instead of screenshots for inspecting page state.
- Playwright can navigate pages, interact with elements, and verify content, but cannot capture visual output as images.
- Always ensure the backend is running before executing Playwright tests (`test:e2e`).
- Use console logs and DOM inspection methods for debugging instead of visual captures.

---

## 🧱 Generated Client Usage

- Import API hooks/functions from **`@client/generated`** (wrapper for `web/generated/`).
- *Never* edit any files inside `web/generated/`.
- On OpenAPI schema change, regenerate:

```bash
pnpm run codegen
```

---

## ✨ UI & Component Guidelines

- Use **shadcn/ui + Tailwind** for new components; shared primitives in `web/packages/ui`.
- Keep all props typed via `interface` or `type`.
- Follow accessible HTML semantics (aria, keyboard).
- Prefer functional components and React Server Components.
- For icons, use `lucide-react` or existing set—no ad-hoc SVG dumps.

---

## 📓 Task System

Junie‑Web follows the Markdown task flow:

1. Tasks live in `.junie/tasks/open/` as `TASK.<category>.<slug>.md`.
2. On completion, move to `.junie/tasks/closed/` **and** append:

   ```
   ## ✅ Task Completed
   **Changes made**
   - Detail changes...
   **Outcomes**
   - Describe results...
   ```

3. Do not close until **build + tests + lint** pass.
4. Use `safe-run.sh` for any long‑lived processes—never block with `tail -f` or interactive shells.

---

## ✔️ Lint & Format

- ESLint + Prettier enforced by Turborepo; run `pnpm lint` and fix issues.
- No unused variables, `any`, or `console.log`.
- Keep headers concise—no boilerplate/banner text.

---

## 🚦 Acceptance Bar

A task is done when all are true:

1. `pnpm build --filter controlpanel` succeeds.
2. `pnpm --filter controlpanel test` passes.
3. `pnpm lint` reports zero errors.
4. Task moved to `.junie/tasks/closed/` with completion summary.

---

## 🛑 Explicit Exclusions

- **No backend**: ignore `glyphd/`, `glyphsieve/`, SQLite, UV, ResourceContext.
- **No Docker** unless explicitly requested for frontend previews.
- Do not redefine backend ADRs or lint policies outside the frontend scope.

---

## 🛠 Happy shipping, Junie‑Web! Keep the UI crisp, the types tight, and the tests green.