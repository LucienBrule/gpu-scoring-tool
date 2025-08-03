## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useGpuListings` that queries the `/api/listings` endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useGpuListings Hook with Filtering and Pagination

## Purpose
Provide a reusable, type-safe hook to fetch GPU listings data with support for filtering, pagination, and fuzzy search. This hook will be the foundation for displaying and interacting with GPU listings throughout the application.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useGpuListings.ts`.
2. Import the `ApiClient` or the `getListings` function from `@repo/client`.
3. Use `react-query`'s `useQuery` function to call `getListings()` or `ApiClient.getListings()`.
4. Support query parameters for:
   - Pagination (`limit`, `offset`)
   - Filtering by model, price range, etc.
   - Date filtering if supported
5. Define and export the hook with appropriate TypeScript types:
   ```ts
   export const useGpuListings = (params: {
     limit?: number;
     offset?: number;
     model?: string;
     minPrice?: number;
     maxPrice?: number;
     fromDate?: string;
     toDate?: string;
   }) =>
     useQuery(
       ['listings', params],
       () => getListings(params)
     );
   ```
6. Ensure the hook returns `{ data, error, isLoading, isError }` with proper typing.
7. Add a `useGpuListingById` variant for fetching a single listing by ID if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Ensure query keys are structured to properly cache different parameter combinations.
- Handle empty or undefined filter parameters gracefully.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useGpuListings.test.ts` using `@testing-library/react-hooks`:
  - Mock `getListings` or `ApiClient.getListings` to return sample listings data.
  - Test with different filter combinations and verify correct parameters are passed.
  - Test pagination by changing limit/offset and verifying API calls.
  - Test error handling by mocking API failures.
- Verify the query key structure includes all filter parameters for proper caching.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useGpuListings.ts
# Run in Dev mode and open React Query Devtools to inspect listings queries:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useGpuListings.ts` exists and exports a working `useGpuListings` hook.
- The hook properly handles all filter parameters and pagination.
- UI components can use the hook to display listings with filtering and search.
- Automated tests for `useGpuListings` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Created a new file `apps/controlpanel/src/hooks/useGpuListings.ts` with the required hook implementation
- Implemented the useGpuListings hook using ApiClient.getListings with support for all required parameters
- Added comprehensive TypeScript interfaces for parameters and results
- Implemented the useGpuListingById hook for fetching a single listing by ID
- Modified the useGpuListingById hook to use the existing getListings method with an ID filter
- Created a comprehensive test file at apps/controlpanel/src/hooks/__tests__/useGpuListings.test.ts
- Added tests for both hooks, covering query keys, parameter passing, default values, return structure, and error handling

**Outcomes**
- The useGpuListings hook provides a clean, type-safe interface for fetching GPU listings with filtering and pagination
- The useGpuListingById hook provides a convenient way to fetch a single listing by ID
- Both hooks return the expected structure with data, isLoading, isError, and error properties
- All tests pass successfully, confirming the hooks work as expected
- The hooks follow the project's patterns and conventions
- UI components can now easily consume GPU listings data with proper loading and error states