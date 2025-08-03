## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useForecastDeltas` that queries the forecast deltas endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useForecastDeltas Hook with Query Parameters

## Purpose
Provide a reusable, type-safe hook to fetch GPU price forecast deltas with support for model and region filtering. This hook will enable the application to display price trend forecasts and comparative analysis between different time periods.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useForecastDeltas.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with a new method for forecast deltas, following the pattern of existing methods like `getHealth`, `getListings`, etc.
4. Implement a new method in the client package for forecast deltas if not already present.
5. Use `react-query`'s `useQuery` function to call this new method, passing parameters for model, region, date ranges, and comparison periods.
6. Ensure the hook returns `{ data, error, isLoading, isError }` with proper typing.
7. Add utility functions to calculate percentage changes or format delta values if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `react-query` for caching and deduplication.
- Handle date formatting consistently (ISO 8601 format for API requests).
- Ensure query keys are structured to properly cache different parameter combinations.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useForecastDeltas.test.ts` using `@testing-library/react-hooks`:
  - Mock the forecast deltas function to return sample forecast data.
  - Test with different filter combinations and verify correct parameters are passed.
  - Test date range parameters and comparison period options.
  - Test error handling by mocking API failures.
- Verify the query key structure includes all filter parameters for proper caching.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useForecastDeltas.ts
# Run in Dev mode and open React Query Devtools to inspect forecast queries:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useForecastDeltas.ts` exists and exports a working `useForecastDeltas` hook.
- The hook properly handles all filter parameters and date ranges.
- UI components can use the hook to display forecast deltas with filtering options.
- Automated tests for `useForecastDeltas` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Extended the client package with methods for forecast deltas (getForecastDeltas and getForecastDeltaById)
- Created `apps/controlpanel/src/hooks/useForecastDeltas.ts` with the required hook implementation
- Implemented the useForecastDeltas hook using getForecastDeltas with support for all required parameters
- Implemented the useForecastDeltaById hook for fetching a specific delta by ID
- Added utility functions for calculating and formatting percentage changes
- Created a ForecastDelta interface to provide proper typing for the hook
- Created a comprehensive test file at apps/controlpanel/src/hooks/__tests__/useForecastDeltas.test.ts
- Added tests for both hooks and utility functions

**Outcomes**
- The useForecastDeltas hook provides a clean, type-safe interface for fetching forecast deltas with filtering
- The useForecastDeltaById hook provides a way to fetch a specific forecast delta by ID
- The utility functions make it easy to calculate and format percentage changes
- All tests pass successfully, confirming the hooks work as expected
- The hooks follow the project's patterns and conventions
- UI components can now easily consume forecast delta data with proper loading and error states
- The hooks are well-documented with JSDoc comments explaining parameters and return values