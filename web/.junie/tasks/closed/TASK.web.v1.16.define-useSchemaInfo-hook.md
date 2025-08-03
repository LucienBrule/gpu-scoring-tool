## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useSchemaInfo` that queries the schema version endpoints through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useSchemaInfo Hook for Schema Versioning

## Purpose
Provide a reusable, type-safe hook to fetch database schema version information and details. This hook will enable the application to display schema version history, track migrations, and ensure data compatibility across different versions.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useSchemaInfo.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with new methods for schema version information, following the pattern of existing methods.
4. Implement two related hooks:
   - `useSchemaVersions`: Fetches all available schema versions
   - `useSchemaVersionDetails`: Fetches details for a specific version
5. Use `react-query`'s `useQuery` function to call the appropriate methods.
6. Ensure the version-specific hook doesn't fetch if no version is provided (use the `enabled` option).
7. Ensure both hooks return `{ data, error, isLoading, isError }` with proper typing.
8. Add utility functions to compare versions or format schema changes if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Ensure the version-specific hook doesn't fetch if no version is provided.
- Handle version format validation before making API calls.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useSchemaInfo.test.ts` using `@testing-library/react-hooks`:
  - Mock the schema version functions to return sample version data.
  - Test with valid and invalid version parameters.
  - Test error handling by mocking API failures.
  - Verify the hooks correctly handle edge cases like non-existent versions.
- Test the conditional fetching behavior of `useSchemaVersionDetails`.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useSchemaInfo.ts
# Run in Dev mode and inspect schema version data:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useSchemaInfo.ts` exists and exports both schema-related hooks.
- The hooks properly handle version parameters and return appropriate data.
- UI components can use the hooks to display schema version information.
- Automated tests for both hooks pass with no errors.
- The hooks are documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Extended the client package with methods for schema version information:
  - Added wrapper methods to the ApiClient class
  - Added standalone functions for these methods
  - Updated exports in index.ts to include the new functions
- Created `apps/controlpanel/src/hooks/useSchemaInfo.ts` with two hooks:
  - `useSchemaVersions`: Fetches all available schema versions
  - `useSchemaVersionDetails`: Fetches details for a specific version
- Added utility functions:
  - `formatVersion`: Formats a version string for display (adds 'v' prefix if not present)
  - `isDefaultVersion`: Checks if a version is the current default
- Created comprehensive tests in `apps/controlpanel/src/hooks/__tests__/useSchemaInfo.test.ts`
- Verified that all tests pass successfully

**Outcomes**
- The useSchemaInfo hooks provide a clean, type-safe interface for fetching schema version information
- The hooks return the expected structure with data, isLoading, isError, and error properties
- The utility functions make it easy to format version strings and check if a version is the default
- The useSchemaVersionDetails hook only runs the query if a version is provided
- All tests pass successfully, confirming the hooks work as expected
- The hooks follow the project's patterns and conventions
- UI components can now easily consume schema version information with proper loading and error states
- The hooks are well-documented with JSDoc comments explaining parameters and return values