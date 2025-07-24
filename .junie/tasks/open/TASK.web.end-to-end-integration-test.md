# TASK.web.end-to-end-integration-test.md

## 🧩 Task: End-to-End Integration Test Between Frontend and Backend

Junie, your task is to wire up the end-to-end interaction between the controlpanel frontend and the glyphd backend. This will validate full-stack integration using the OpenAPI-generated client.

---

## 🎯 Objectives

- Add a page to the Next.js app (`controlpanel`) that:
  - Uses the OpenAPI SDK (`@client`) to call `GET /api/health`
  - Displays the result in the rendered output

- Set up a frontend test suite:
  - Use **Playwright** or **Vitest + jsdom** to validate this interaction

---

## 🧪 Required Checks

- Render a page at `/health` or `/integration-test`
  - Must call `getHealth()` using the generated SDK
  - Must display `"status: ok"` or error fallback in the UI

- Add a test in `apps/controlpanel/tests/` that:
  - Launches the app (or mocks fetch)
  - Confirms that the API returns the correct result
  - Verifies that the UI renders the fetched response

### 🧪 Required Test Environment

- You must use **Playwright** to perform an actual browser test of the integration.
- This test must:
  - Boot the frontend in dev mode (if not already running)
  - Visit the live page (`/integration-test`)
  - Wait for the OpenAPI SDK call to resolve
  - Assert that the correct status appears in the UI (e.g. `"status: ok"`)

- This ensures the end-to-end system is validated from the browser down to the backend.
- Backend tests may use `curl`, but **UI integration must be validated with Playwright or equivalent**.

---

## 📦 File Locations

- Page: `apps/controlpanel/app/integration-test/page.tsx`
- Hook (optional): `apps/controlpanel/src/hooks/useHealth.ts`
- Test: `apps/controlpanel/tests/integration/health.spec.ts`

---

## 🧑‍💻 Dev Environment Assumptions

- The backend is running at `http://localhost:8000`
- The frontend is running at `http://localhost:3000`
- You are using `docker compose up -d` to run both services

---

## ✅ Completion Criteria

- Visiting `http://localhost:3000/integration-test` renders API data
- Tests pass via:
  ```bash
  pnpm test --filter controlpanel
  ```
- Uses `@client` OpenAPI SDK directly (no hand-written fetch)
- Results are typed and error states are handled

---

## ✍️ Notes

This proves that the stack is wired up and working with type safety and runtime correctness. It also gives you a baseline for validating future routes like `/listings`, `/report`, or filtered queries.