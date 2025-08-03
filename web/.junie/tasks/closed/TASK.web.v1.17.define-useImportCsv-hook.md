## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useImportCsv` that handles file uploads to the CSV import endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useImportCsv Hook for CSV Data Import

## Purpose
Provide a reusable, type-safe hook to upload and import CSV files containing GPU listings data. This hook will enable the application to ingest external data sources, allowing users to bulk import listings for analysis and processing.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useImportCsv.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with a new method for CSV imports, following the pattern of existing methods.
4. Use `react-query`'s `useMutation` function to call this new method.
5. Implement proper FormData handling for file uploads.
6. Add support for optional parameters like:
   - Import mode (append, replace, etc.)
   - Validation options
   - Column mapping configuration
7. Ensure the hook returns `{ mutate, data, error, isLoading, isError, progress }` with proper typing.
8. Implement upload progress tracking if the API supports it.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `useMutation` since this is a POST endpoint with file upload.
- Handle file validation (file type, size limits) before submission.
- Provide appropriate error handling for network issues and server validation errors.
- Ensure compatibility with common file input components.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useImportCsv.test.ts` using `@testing-library/react-hooks`:
  - Mock the CSV import function to simulate successful and failed imports.
  - Test with sample CSV files of different sizes and formats.
  - Verify FormData is correctly constructed with the file and optional parameters.
  - Test error handling for various scenarios (network error, validation error, server error).
- Test integration with file input components in a component context.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useImportCsv.ts
# Run in Dev mode and test CSV import in the browser:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useImportCsv.ts` exists and exports a working `useImportCsv` hook.
- The hook properly handles file uploads and returns import results.
- UI components can use the hook to provide CSV import functionality with progress feedback.
- Automated tests for `useImportCsv` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.
- Error states and validation feedback are properly handled and exposed to consuming components.

## ✅ Task Completed

**Changes made**
- Verified that the useImportCsv hook already exists and meets all requirements
- Enhanced the tests for the useImportCsv hook to follow the pattern used in useGpuClassification.test.ts
- Added comprehensive tests for:
  - Verifying that useMutation is called with the correct parameters
  - Testing that callbacks are passed correctly
  - Checking that the hook returns the expected structure
  - Ensuring that the hook's functions call the underlying mutation functions
  - Validating that file validation works correctly

**Outcomes**
- The useImportCsv hook is fully implemented and tested
- The hook provides a reusable, type-safe way to upload and import CSV files
- It handles file validation, progress tracking, and error handling
- It's well-documented with JSDoc comments and includes a comprehensive example
- UI components can use the hook to provide CSV import functionality with progress feedback
- The hook follows the pattern established in the client package for other API methods