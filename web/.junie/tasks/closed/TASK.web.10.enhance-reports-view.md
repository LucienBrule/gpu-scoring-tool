# TASK.web.10.enhance-reports-view

## 📌 Title
Replace placeholder alert with real data grid in reports view

## 📁 Location
`web/apps/controlpanel/src/app/reports/page.tsx`

## 🧠 Context
Currently, the reports page contains only a placeholder alert instead of actual data. Now that we have the necessary hooks available, we need to enhance the reports view to display real data in a comprehensive grid format. This grid should show utility scores, price/GB, and other relevant metrics to help users analyze GPU performance and value.

The enhanced reports view will be a central feature of the application, providing users with valuable insights into GPU metrics and helping them make informed decisions. To ensure maintainability and scalability, the data grid should be isolated into a reusable, composable component with encapsulated logic for data fetching, sorting, and filtering. This approach will improve testability and allow easy integration in other parts of the app if needed.

## ✅ Requirements

- Replace the placeholder alert with a data grid component
- Isolate the data grid into a reusable, composable component
- Use the existing hooks to fetch and display real data
- Include columns for utility score, price/GB, and other relevant metrics
- Implement client-side sorting and filtering with clear architectural separation (e.g., use custom hooks or utility functions)
- Add filtering capabilities (by model, score range, price range, etc.)
- Ensure the grid is responsive and works well on mobile devices
- Implement pagination if the dataset is large
- Add visual indicators for high/low scores (e.g., color coding)
- Include tooltips for explaining metrics and calculations
- Encapsulate sorting and filtering logic within the data grid component or related hooks/utilities to keep the page component clean
- Write unit tests covering rendering, sorting, filtering, visual indicators, and composability aspects

## 🔧 Hints
- Use shadcn/ui Table component as the foundation
- Consider using a library like TanStack Table for advanced features
- Implement client-side filtering and sorting for better UX, possibly via custom hooks or utility functions to keep logic modular
- Use Tailwind's color utilities for visual indicators
- Look at the listings table implementation for patterns and reusable components
- Consider creating utility functions for filtering and sorting logic to promote reuse
- Utilize existing hooks for data fetching and state management to keep components declarative and testable

## 🧪 Testing

- Add unit tests for the component:
  - File: `web/apps/controlpanel/src/app/reports/__tests__/page.test.tsx`
  - Test rendering with mock data
  - Test sorting functionality
  - Test filtering capabilities
  - Test visual indicators
  - Test composability and isolated logic (e.g., test custom hooks or utilities separately)
- Update or add Playwright integration test:
  - File: `web/apps/controlpanel/tests/integration/reports.spec.ts`
  - Test navigation to the page
  - Test basic interaction with the grid
  - Test sorting and filtering

## 🧼 Acceptance Criteria

- [x] Reports page renders real data in a grid format
- [x] Grid is isolated as a reusable, composable component with encapsulated logic
- [x] Grid includes columns for utility score, price/GB, and other relevant metrics
- [x] Client-side sorting and filtering logic is cleanly separated and testable
- [x] Sorting works for all columns
- [x] Filtering narrows down results as expected
- [x] Visual indicators clearly show high/low scores
- [x] Tooltips provide helpful explanations
- [x] Grid is responsive and usable on mobile devices
- [x] Unit and integration tests pass and cover composability and logic encapsulation

## 🔗 Related

- EPIC.web.frontend-consume-hooks.md
- TASK.web.09.client.wrap-models-endpoint.md (may be a dependency)
- TASK.web.11.add-loading-and-error-states.md (will enhance this component)

## ✅ Task Completed

**Changes made**
- Created a reusable `ReportsDataGrid` component in `components/reports/ReportsDataGrid.tsx`
- Implemented the reports page to use the new component and fetch data with the useReports hook
- Added comprehensive filtering capabilities:
  - Text search for model name
  - Price range filtering (min/max)
  - Score range filtering (min/max)
  - Model selection filtering
- Implemented sorting for all columns
- Added visual indicators for scores and price/GB using color coding
- Added tooltips for all column headers to explain metrics
- Implemented responsive design with mobile-friendly layout
- Added pagination for large datasets
- Implemented proper loading, error, and empty states
- Added comprehensive unit tests for the component
- Fixed test issues by adding QueryClientProvider to test files

**Outcomes**
- The reports page now displays real data in a comprehensive grid format
- Users can sort and filter the data to find the information they need
- Visual indicators help users quickly identify high-performing GPUs
- The component is reusable and can be integrated into other parts of the app
- All tests are passing, confirming the functionality works as expected
- The implementation meets all acceptance criteria

**Challenges and Solutions**
- Fixed test failures due to missing QueryClientProvider by adding a wrapper component to all test files
- Ensured proper typing for all component props and state to maintain type safety
- Implemented responsive design to ensure the grid works well on mobile devices by hiding less important columns
- Used useMemo for data processing to optimize performance with large datasets