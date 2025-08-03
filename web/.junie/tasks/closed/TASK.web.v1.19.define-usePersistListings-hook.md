## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `usePersistListings` that saves GPU listings data through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement usePersistListings Hook for Data Persistence

## Purpose
Provide a reusable, type-safe hook to save and persist GPU listings data to the database. This hook will enable the application to commit changes, save edited listings, and ensure data durability after modifications or imports.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/usePersistListings.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with a new method for persisting listings, following the pattern of existing methods.
4. Use `react-query`'s `useMutation` function to call this new method.
5. Support persisting single or multiple listings with options for:
   - Persistence mode (create, update, upsert)
   - Validation options
   - Conflict resolution strategy
   - Batch size for large operations
6. Ensure the hook returns `{ mutate, data, error, isLoading, isError }` with proper typing.
7. Add helper functions for common persistence operations if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `useMutation` since this is a POST endpoint that modifies data.
- Handle validation of listings data before submission.
- Provide appropriate error handling for network issues, validation errors, and conflicts.
- Consider implementing optimistic updates for better UX.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/usePersistListings.test.ts` using `@testing-library/react-hooks`:
  - Mock the persist listings function to simulate successful and failed persistence.
  - Test with different data payloads and verify correct parameters are passed.
  - Test error handling for various scenarios (network error, validation error, conflict error).
  - If implementing optimistic updates, test the rollback mechanism on failure.
- Test integration with UI components that save or update listings.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/usePersistListings.ts
# Run in Dev mode and test persistence in the browser:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/usePersistListings.ts` exists and exports a working `usePersistListings` hook.
- The hook properly handles different persistence operations and returns results.
- UI components can use the hook to save and update listings with appropriate feedback.
- The hook handles errors gracefully and provides meaningful error messages.
- Automated tests for `usePersistListings` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Implemented `usePersistListings` hook in `apps/controlpanel/src/hooks/usePersistListings.ts`
- Created enums for persistence modes (CREATE, UPDATE, UPSERT) and conflict resolution strategies (SKIP, OVERWRITE, MERGE)
- Added comprehensive validation for listings data before submission
- Implemented detailed error handling and validation error reporting
- Added extensive JSDoc documentation with usage examples
- Created comprehensive tests covering various scenarios

**Outcomes**
- The hook provides a complete solution for persisting GPU listings data
- It supports different persistence modes and conflict resolution strategies
- The implementation includes validation and detailed error messages
- The hook is well-documented with JSDoc comments and usage examples
- Comprehensive tests are in place covering various use cases and edge cases