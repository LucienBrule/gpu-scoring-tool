## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useGpuModels` that queries the `/api/models` endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useGpuModels Hook

## Purpose
Provide a reusable, type-safe hook to fetch GPU model metadata and expose loading, success, and error states for UI components to consume, enabling model-based filtering and display throughout the control panel.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useGpuModels.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Use `react-query`'s `useQuery` to call `ApiClient.getModels()`.
4. Define and export the hook:
   ```ts
   export const useGpuModels = () =>
     useQuery(['models'], () => ApiClient.getModels());
   ```
5. Ensure the hook returns `{ data, error, isLoading, isError }` with correct type inference.
6. Add appropriate typing for the return data.

## Constraints
- Import `ApiClient` from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Do not add additional retry or polling logic.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useGpuModels.test.ts` with `@testing-library/react-hooks`:
  - Mock `ApiClient.getModels` to return an array of model objects and assert `data.length` matches.
  - Mock failure and assert `isError === true`.
- Verify the hook key is `['models']` and caching behavior is correct.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install --filter controlpanel
pnpm --filter controlpanel test src/hooks/useGpuModels.ts
# Run Dev mode and inspect React Query Devtools for key "models":
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useGpuModels.ts` exists and exports a working `useGpuModels` hook.
- UI components using `useGpuModels` display model data, loading, and error states correctly.
- Automated tests for `useGpuModels` pass with no errors.

## ✅ Task Completed
**Changes made**
- Created `apps/controlpanel/src/hooks/useGpuModels.ts` with the required hook implementation
- Implemented the hook using `useQuery` from `@tanstack/react-query` to call `ApiClient.getModels()`
- Added proper TypeScript typing for the return data using `GPUModelDTO[]` from `@repo/client`
- Added JSDoc comments with description and example usage
- Created `apps/controlpanel/src/hooks/useGpuModels.test.ts` with comprehensive tests
- Verified that all tests pass successfully

**Outcomes**
- The `useGpuModels` hook provides a clean, type-safe interface for fetching GPU model data
- The hook returns the expected structure with `data`, `isLoading`, `isError`, and `error` properties
- All tests pass, confirming the hook works as expected
- The hook follows the project's patterns and conventions
- UI components can now easily consume GPU model data with proper loading and error states