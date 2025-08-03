## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useImportFromPipeline` that triggers data imports from the existing pipeline through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useImportFromPipeline Hook for Automated Data Import

## Purpose
Provide a reusable, type-safe hook to trigger and monitor imports from the established data pipeline. This hook will enable the application to refresh its dataset from upstream sources, ensuring the GPU listings database stays current with minimal manual intervention.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useImportFromPipeline.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with a new method for pipeline imports, following the pattern of existing methods.
4. Use `react-query`'s `useMutation` function to call this new method.
5. Support configuration parameters for the pipeline import, such as:
   - Source selection (which upstream sources to import from)
   - Import mode (append, replace, merge)
   - Date range filters
   - Validation options
6. Ensure the hook returns `{ mutate, data, error, isLoading, isError }` with proper typing.
7. Add a polling mechanism to check import status if the operation is asynchronous.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `useMutation` since this is a POST endpoint that triggers an action.
- Handle potential long-running operations gracefully.
- Provide appropriate error handling for network issues and server errors.
- Consider implementing a status check mechanism if imports run asynchronously.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useImportFromPipeline.test.ts` using `@testing-library/react-hooks`:
  - Mock the pipeline import function to simulate successful and failed imports.
  - Test with different configuration parameters and verify correct parameters are passed.
  - Test error handling for various scenarios (network error, validation error, server error).
  - If implementing polling, test the polling mechanism with mock responses.
- Test integration with UI components that trigger pipeline imports.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useImportFromPipeline.ts
# Run in Dev mode and test pipeline import in the browser:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useImportFromPipeline.ts` exists and exports a working `useImportFromPipeline` hook.
- The hook properly handles configuration parameters and returns import results.
- UI components can use the hook to trigger pipeline imports with appropriate feedback.
- If the import is asynchronous, the hook provides a way to monitor progress or completion.
- Automated tests for `useImportFromPipeline` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed

**Changes made**
- Enhanced the existing useImportFromPipeline hook with additional features:
  - Added support for import mode (append, replace, merge)
  - Added support for date range filtering
  - Implemented a polling mechanism to check import status
  - Added status tracking for long-running operations
  - Improved error handling and validation
- Expanded the hook's interface to include:
  - Status reporting (idle, processing, completed, failed)
  - Polling controls (start, stop, check status)
  - Configuration options for polling behavior
- Enhanced the tests to be more comprehensive:
  - Added tests for the new features (import mode, date range, polling)
  - Verified correct initialization with default values
  - Tested custom polling options
  - Ensured proper parameter validation

**Outcomes**
- The useImportFromPipeline hook now provides a complete solution for pipeline imports
- Long-running operations are handled gracefully with status updates and polling
- UI components can provide rich feedback during the import process
- The hook is well-documented with JSDoc comments and includes comprehensive examples
- All tests pass successfully, verifying the hook's functionality
- The implementation follows the pattern established in the client package