## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `useGpuClassification` that queries the ML classification endpoint through the unified `ApiClient` from the `@repo/client` package in the `gpu-scoring-tool` controlpanel application.

## Title
Implement useGpuClassification Hook for ML Classification

## Purpose
Provide a reusable, type-safe hook to interact with the machine learning classification endpoint that determines whether a text description refers to a GPU. This hook will enable the application to offer real-time classification feedback and power the ML Playground feature.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/useGpuClassification.ts`.
2. Import the `ApiClient` from `@repo/client`.
3. Note that you may need to extend the client package with a new method for GPU classification, following the pattern of existing methods.
4. Implement a new method in the client package for GPU classification if not already present.
5. Use `react-query`'s `useMutation` function to call this new method, passing parameters for:
   - Text description to classify
   - Optional confidence threshold
   - Optional classification mode or model version
6. Ensure the hook returns `{ mutate, data, error, isLoading, isError }` with proper typing.
7. Add helper functions to format confidence scores or interpret classification results if needed.

## Constraints
- Import from `@repo/client`; do not import APIs directly from generated code.
- Use `useMutation` instead of `useQuery` since this is a POST endpoint with variable input.
- Handle empty or malformed text input gracefully.
- Avoid excessive re-renders when classification is triggered repeatedly.
- Follow the pattern established in the client package for other API methods.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/useGpuClassification.test.ts` using `@testing-library/react-hooks`:
  - Mock the classification function to return sample classification results.
  - Test with various text inputs and verify correct parameters are passed.
  - Test error handling by mocking API failures.
  - Verify the hook correctly handles edge cases like empty strings or very long inputs.
- Test integration with form inputs in a component context.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
pnpm --filter controlpanel test src/hooks/useGpuClassification.ts
# Run in Dev mode and test classification in the browser:
pnpm --filter controlpanel dev
```

## Completion Criteria
- `apps/controlpanel/src/hooks/useGpuClassification.ts` exists and exports a working `useGpuClassification` hook.
- The hook properly handles text input and returns classification results.
- UI components can use the hook to provide real-time classification feedback.
- Automated tests for `useGpuClassification` pass with no errors.
- The hook is documented with JSDoc comments explaining parameters and return values.

## ✅ Task Completed
**Changes made**
- Extended the client package with a `classifyGpu` method in the ApiClient class
- Added a standalone `classifyGpu` function to the client package
- Updated exports in the client package's index.ts file to include the new function
- Created `apps/controlpanel/src/hooks/useGpuClassification.ts` with the required hook implementation
- Implemented the useGpuClassification hook using useMutation from react-query
- Added utility functions for formatting confidence scores and checking thresholds
- Created a comprehensive test file at apps/controlpanel/src/hooks/__tests__/useGpuClassification.test.ts
- Added tests for the hook and utility functions

**Outcomes**
- The useGpuClassification hook provides a clean, type-safe interface for classifying GPU descriptions
- The hook returns a comprehensive result object with the classification result and utility functions
- The utility functions make it easy to format confidence scores and check thresholds
- All tests pass successfully, confirming the hook works as expected
- The hook follows the project's patterns and conventions
- UI components can now easily classify GPU descriptions with proper loading and error states
- The hook is well-documented with JSDoc comments explaining parameters and return values