# TASK.web.07.client.wrap-listings-endpoint

## 📌 Title
Export `useListings` hook with pagination and date filters

## 📁 Location
`web/packages/client/src/hooks/useListings.ts`

## 🧠 Context
The backend now exposes a `/listings` endpoint that provides GPU listing data. We need to create a custom hook that wraps the auto-generated TanStack Query hook to provide a more ergonomic API for consuming this data in the frontend. This hook will be used in the listings table view and potentially other components that need access to GPU listing data.

The hook should support pagination and date filtering to allow users to navigate through large datasets efficiently and filter listings by date ranges.

## ✅ Requirements

- Create a `useListings` hook that wraps the auto-generated TanStack Query hook
- Implement pagination support with configurable page size and page number
- Add date filtering capabilities (from/to dates)
- Export the hook from `@client/hooks` for consumption by frontend components
- Include proper TypeScript typing for all parameters and return values
- Handle loading, error, and empty states appropriately
- Implement proper caching strategy using SWR patterns

- Look at existing hooks like `useHealthCheck` for implementation patterns
- Use the auto-generated client from `@client/generated`
- Consider implementing a custom hook factory pattern if there are common patterns across multiple endpoints
- Define a typed parameter interface to improve clarity:
  ```ts
  interface UseListingsParams {
    page: number;
    pageSize: number;
    fromDate?: string;
    toDate?: string;
  }
  ```
- Use ISO 8601 format (`YYYY-MM-DD`) for `fromDate` and `toDate` when passing to the API.
- Ensure the hook is properly tested with unit tests
- Include all filter parameters in the query key for proper SWR caching:
  ```ts
  const queryKey = ['listings', page, pageSize, fromDate, toDate];
  ```

## 🧪 Testing

- Add unit tests for the hook:
  - File: `web/packages/client/src/hooks/useListings.test.ts`
  - Test pagination functionality
  - Test date filtering
  - Test error handling
  - Mock the underlying API calls

## 🧼 Acceptance Criteria

- [x] Hook successfully fetches data from the `/listings` endpoint
- [x] Pagination works correctly (page size and page number)
- [x] Date filtering functions as expected
- [x] TypeScript types are comprehensive and accurate
- [x] Unit tests pass and cover edge cases
- [x] Documentation comments explain usage patterns
- [x] Hook is exported from the package for consumption

## 🔗 Related

- EPIC.web.frontend-consume-hooks.md
- TASK.web.08.ui.render-listings-table.md (depends on this)

## ✅ Task Completed

**Changes made**
- Created a new `getListings` function in `client.ts` that wraps the auto-generated API client
- Implemented the `useListings` hook in `packages/client/src/hooks/useListings.ts` with pagination and date filtering support
- Added comprehensive TypeScript interfaces for parameters and return values
- Implemented proper caching with query keys that include all filter parameters
- Added detailed JSDoc comments with usage examples
- Created unit tests in `packages/client/src/hooks/useListings.test.ts` that verify pagination, filtering, and error handling
- Exported the hook from `@client/hooks` via the index.ts file

**Outcomes**
- The `useListings` hook provides a clean, ergonomic API for consuming GPU listing data
- Pagination is implemented with configurable page size and page number
- Date filtering is supported with fromDate and toDate parameters
- The hook handles loading, error, and empty states appropriately
- The hook is properly typed and documented
- Unit tests verify the hook's functionality
- The hook is ready for use in the listings table view (TASK.web.08)