## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useHealth` that queries the `/api/health` endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useHealth Hook

## Purpose
Provide a reusable, type-safe hook to fetch the API health status and expose loading, success, and error states for UI components to consume.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useHealth.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Use `react-query`'s `useQuery` function to call `ApiClient.getHealth()`.
4. Define and export the hook:
   ```ts
   export const useHealth = () =>
     useQuery(['health'], () => ApiClient.getHealth());
   ```
5. Ensure the hook returns `{ data, error, isLoading, isError }`.
6. Add appropriate typing for the return data.

## Constraints
- Import `ApiClient` from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Do not introduce custom fetch or retry logic beyond `useQuery` defaults.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useHealth.test.ts` using `@testing-library/react-hooks`:
  - Mock `ApiClient.getHealth` to return `{ status: 'ok' }` and assert `data.status === 'ok'`.
  - Mock failure and assert `isError === true` and `error` is an instance of `Error`.
- Verify the hook key is `['health']` and caching behaves correctly.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install --filter controlpanel
pnpm --filter controlpanel test src/hooks/useHealth.ts
# Run in Dev mode and open React Query Devtools to inspect key "health":
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useHealth.ts` exists and exports a working `useHealth` hook.
- UI components using `useHealth` display loading and error states correctly.
- Automated tests for `useHealth` pass with no errors.

## ✅ Task Completed
**Changes made**
- Updated the existing useHealth.ts file to use react-query's useQuery instead of useState/useEffect
- Implemented the hook to use ApiClient.getHealth() as specified
- Added proper TypeScript typing for the return data (HealthStatus)
- Created a comprehensive test file at apps/controlpanel/src/hooks/__tests__/useHealth.test.ts
- Added tests for query key, API call, return structure, error handling, and loading state

**Outcomes**
- The useHealth hook now provides a clean, type-safe interface for fetching API health status
- The hook returns the expected structure with data, isLoading, isError, and error properties
- All tests pass successfully, confirming the hook works as expected
- The hook follows the project's patterns and conventions
- UI components can now easily consume API health status with proper loading and error states