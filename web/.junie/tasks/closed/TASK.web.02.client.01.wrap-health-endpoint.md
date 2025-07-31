# TASK.web.02.client.01.wrap-health-endpoint

## Title

Wrap Health Check Endpoint with React Hook

## Status

Closed

## Epic

[EPIC.web.frontend-ui-ux.md](../epics/open/EPIC.web.frontend-ui-ux.md)

## Purpose

The backend provides a `/api/health` endpoint that returns the system health status. This task is to create a typed client hook in the frontend project that wraps this endpoint using the existing OpenAPI client.

This hook will be used by components to check backend connectivity and status.

## Requirements

- Create a hook `useHealthCheck()` in `web/packages/client/src/hooks/useHealthCheck.ts`.
- The hook should use the generated OpenAPI client to call the `/health` endpoint.
- It should return:
  - `status`: the parsed status response (e.g., `{ status: "ok" }`)
  - `isLoading`: boolean
  - `error`: any error from the request
- Use React Query (or the client wrapper if already configured) for internal fetch state management.
- Do **not** use raw `fetch()` or Axios — must use the generated OpenAPI client under `@client/generated`.
- Ensure type safety and infer the correct return type from the OpenAPI schema.
- Do **not** modify files inside `web/generated/`.

## Output

- `web/packages/client/src/hooks/useHealthCheck.ts`
- Optional: `web/apps/controlpanel/src/app/integration-test/page.tsx` can be updated to use this hook if desired for quick smoke test.

## Dev & Test

- Run backend via `.junie/scripts/docker-stack.sh up`
- Run dev server:
  ```bash
  ./.junie/scripts/safe-run.sh -n controlpanel -b -- pnpm dev --filter controlpanel
  ```
- Run tests:
  ```bash
  pnpm run test:unit --filter controlpanel
  pnpm run test:e2e --filter controlpanel
  ```

## Acceptance Criteria

- Hook is created and type-safe
- Hook successfully calls the backend and returns health status
- Hook is used somewhere in the codebase (optional but preferred)
- Tests pass
- Task file moved to `.junie/tasks/closed/` with a summary block

## ✅ Task Completed

**Changes made**
- Created a new hook `useHealthCheck()` in `web/packages/client/src/hooks/useHealthCheck.ts` that uses React Query to fetch health status from the backend API
- Added an export for the hook in `web/packages/client/src/hooks/index.ts`
- Updated the client package's exports in `web/packages/client/src/index.ts` to include the hooks
- Updated the integration test page to use the new hook instead of the old `useHealth` hook
- Added React Query as a dependency to both the client and controlpanel packages
- Created a Providers component in the controlpanel app to set up the React Query provider
- Modified the layout component to wrap the app with the Providers component

**Outcomes**
- The hook is type-safe and correctly infers the return type from the OpenAPI schema
- The hook successfully calls the backend API and returns the health status
- The hook is used in the integration test page to display the health status
- All integration tests are now passing, including the health check test
- The unit tests are also passing