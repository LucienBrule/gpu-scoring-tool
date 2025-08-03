# TASK.web.09.client.wrap-models-endpoint

## 📌 Title
Create hook for `/models` endpoint to fuel dropdowns & metadata tooltips

## 📁 Location
`web/packages/client/src/hooks/useModels.ts`

## 🧠 Context
The backend provides a `/models` endpoint that contains metadata about GPU models, including specifications, performance metrics, and other relevant information. We need to create a custom hook that wraps the auto-generated TanStack Query hook to provide easy access to this data throughout the application.

It is also intended for use in composable UI primitives, such as virtualized lists or searchable dropdowns, where predictable memoization and transformation of model metadata is important.

This hook will be used to populate dropdown menus for model selection, provide metadata for tooltips, and support other UI components that need GPU model information.

## ✅ Requirements

- Create a `useModels` hook that wraps the auto-generated TanStack Query hook
- Implement flexible filtering capabilities via hook parameters or utility functions (e.g., by `name`, `manufacturer`, `generation`, etc.). Support both substring match and exact match modes.
- Add sorting options for attributes like `vram_gb`, `tdp`, `release_year`, `score`, with ascending/descending direction toggle.
- Export the hook from `@client/hooks` for consumption by frontend components
- Include proper TypeScript typing for all parameters and return values
- Implement helper methods for common use cases (e.g., getting models for a dropdown)
- Handle loading, error, and empty states appropriately
- Implement proper caching strategy using SWR patterns

## 🔧 Hints
- Look at existing hooks like `useHealthCheck` and the newly created `useListings` for implementation patterns
- Use the auto-generated client from `@client/generated`
- Consider implementing utility functions that transform the raw data into formats suitable for UI components
- Ensure the hook is properly tested with unit tests

## 🧪 Testing

- Add unit tests for the hook:
  - File: `web/packages/client/src/hooks/useModels.test.ts`
  - Test filtering functionality
  - Test sorting options
  - Test helper methods
  - Test error handling
  - Mock the underlying API calls
  - Test composability in component contexts
  - Test memoization boundaries for performance-sensitive consumers
  - Include fallback test for empty model list
  - Test edge cases and pagination if applicable

## 🧼 Acceptance Criteria

- [x] Hook successfully fetches data from the `/models` endpoint
- [x] Filtering works correctly for different model attributes
- [x] Sorting functions as expected
- [x] Helper methods correctly transform data for UI components
- [x] TypeScript types are comprehensive and accurate
- [x] Unit tests pass and cover edge cases
- [x] Documentation comments explain usage patterns
- [x] Hook is exported from the package for consumption
- [x] Hook memoizes transformed data where applicable
- [x] Can be consumed within deeply nested components without rerender storm
- [x] Pagination, if backend supports it, is respected and surfaced

## 🔗 Related

- EPIC.web.frontend-consume-hooks.md
- TASK.web.10.enhance-reports-view.md (may depend on this)
- TASK.web.08.ui.render-listings-table.md (may use this for model information)

## ✅ Task Completed
**Changes made**
- Updated `client.ts` to add ModelsApi import and getModels function
- Implemented `useModels` hook with comprehensive filtering and sorting capabilities
- Added TypeScript interfaces for hook parameters and result
- Implemented helper methods for common use cases (getDropdownOptions, getModelByName)
- Added memoization for filtered/sorted data and helper methods
- Created comprehensive unit tests covering all functionality and edge cases

**Outcomes**
- The hook successfully fetches data from the `/models` endpoint
- Filtering works correctly for model name, manufacturer, generation, VRAM, TDP, and NVLink
- Sorting functions as expected for various attributes with ascending/descending toggle
- Helper methods correctly transform data for UI components
- TypeScript types are comprehensive and accurate
- Unit tests pass and cover edge cases
- Documentation comments explain usage patterns with examples
- The hook is exported from the package for consumption
- The hook memoizes transformed data for performance
- The implementation can be consumed within deeply nested components without rerender issues
- Note: The backend API doesn't currently support pagination for the models endpoint