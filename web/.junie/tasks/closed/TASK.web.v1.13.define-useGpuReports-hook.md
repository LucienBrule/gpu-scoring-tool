## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useGpuReports` that queries the reports endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useGpuReports Hook for Markdown Reports

## Purpose
Provide a reusable, type-safe hook to fetch GPU reports data, including markdown content and structured statistics. This hook will enable the application to display detailed GPU analysis reports with rich formatting.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useGpuReports.ts`.
2. Import the `ApiClient` or the `getReports` function from `@repo/client`.
3. Use `react-query`'s `useQuery` function to call `getReports()` or `ApiClient.getReports()`.
4. Support query parameters for:
   - Model name
   - Price range filters
   - Limit and offset for pagination
5. Define and export the hook with appropriate TypeScript types:
   ```ts
   export const useGpuReports = (params: {
     model?: string;
     minPrice?: number;
     maxPrice?: number;
     limit?: number;
     offset?: number;
   }) =>
     useQuery(
       ['reports', params],
       () => getReports(params)
     );
   ```
6. Ensure the hook returns `{ data, error, isLoading, isError }` with proper typing.
7. Add a utility function to parse markdown content if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Do not attempt to render markdown within the hook; return raw content for components to render.
- Handle missing reports gracefully with appropriate error states.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useGpuReports.test.ts` using `@testing-library/react-hooks`:
  - Mock `getReports` or `ApiClient.getReports` to return sample report data.
  - Test with different parameter combinations and verify correct parameters are passed.
  - Test error handling by mocking API failures.
  - Verify the hook correctly handles empty or malformed responses.
- Verify the query key structure includes all parameters for proper caching.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useGpuReports.ts
# Run in Dev mode and open React Query Devtools to inspect report queries:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useGpuReports.ts` exists and exports a working `useGpuReports` hook.
- The hook properly handles all query parameters.
- UI components can use the hook to display formatted reports with markdown content.
- Automated tests for `useGpuReports` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Created a new file `apps/controlpanel/src/hooks/useGpuReports.ts` with the required hook implementation
- Implemented the useGpuReports hook using ApiClient.getReports with support for all required parameters
- Added comprehensive TypeScript interfaces for parameters and results
- Added a parseMarkdown utility function for parsing markdown content
- Implemented improved error handling with a custom retry strategy for 404 errors
- Created a comprehensive test file at apps/controlpanel/src/hooks/__tests__/useGpuReports.test.ts
- Added tests for both the hook and the parseMarkdown utility function

**Outcomes**
- The useGpuReports hook provides a clean, type-safe interface for fetching GPU reports with filtering and pagination
- The hook returns the expected structure with data, isLoading, isError, error, and parseMarkdown properties
- The parseMarkdown utility function provides a way to parse markdown content from reports
- The hook handles missing reports gracefully with appropriate error states
- All tests pass successfully, confirming the hook works as expected
- The hook follows the project's patterns and conventions
- UI components can now easily consume GPU reports data with proper loading and error states