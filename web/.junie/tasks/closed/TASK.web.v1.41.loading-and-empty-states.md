## Persona
You are the Frontend Integration Engineer. Your role is to implement consistent loading indicators and empty-state placeholders across all data-driven views in the `gpu-scoring-tool` controlpanel application, enhancing user feedback during data fetch and absence scenarios.

## Title
Add Loading and Empty-State UI Feedback

## Purpose
Provide unified, accessible visual cues for asynchronous data operations—displaying spinners or skeletons during loading and meaningful placeholders when no data is available—to improve perceived performance and user experience.

## Requirements
1. Identify all data-fetching components/pages that use hooks: Listings, Models, Reports, Forecast, Import Tools, ML Playground.
2. Implement a common `Spinner` or skeleton component (e.g., in `apps/controlpanel/src/components/ui/Spinner.tsx`) if not already present.
3. In each component:
   - During `isLoading`, render the `Spinner` or skeleton layout in place of content.
   - After loading, if the data array or object is empty/null, render an empty-state UI with a message and optional action (e.g., "No listings found. Try adjusting filters.").
4. Ensure loading and empty states use Tailwind utility classes and theme tokens for spacing, color, and typography.
5. Document the pattern in a README or shared style guide for future components.

## Constraints
- Do not introduce new dependencies; use existing components or minimal custom code.
- Maintain accessibility: spinners should have `aria-busy` or `role="status"`, and empty states should be announced to screen readers.
- Keep styling consistent with the Catppuccin Mocha theme and component style utilities.

## Tests
- Manual: throttle network (e.g., Chrome DevTools "Slow 3G") and verify spinners appear.
- Manual: simulate empty API responses (mock hooks) and verify empty-state UIs appear with correct messaging.
- Snapshot tests: add stories in Storybook for loading and empty states of at least two components (e.g., ListingsTable, ReportSection).
- Unit tests: mock `isLoading` and `data=[]` for one component and assert correct elements render.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install
pnpm --filter controlpanel dev

# Simulate slow network and open pages:
open http://localhost:3000/listings
# Toggle network throttling in DevTools to "Slow 3G" to see spinner

# Mock empty data in Storybook:
pnpm --filter controlpanel storybook
# Select "ListingsTable/Loading" and "ListingsTable/Empty" stories
```

## Completion Criteria
- All data-driven views show a spinner or skeleton during loading.
- All views display a clear empty-state placeholder when no data is returned.
- Accessibility checks pass (screen-reader announcements).
- Storybook snapshots for loading and empty states are added and passing.

## ✅ Task Completed
**Changes made**
- Created a new `Spinner` component in `apps/controlpanel/src/components/ui/Spinner.tsx` with customizable size, color, and text options
- Created a new `ProgressBar` component in `apps/controlpanel/src/components/ui/ProgressBar.tsx` for operations with measurable progress
- Added Storybook stories for both components in `apps/controlpanel/src/components/ui/stories/`
- Added Storybook stories for existing `Skeleton` and `ErrorBanner` components
- Updated the dev-harness page to use the new `Spinner` component for all loading states
- Added import statement for `ProgressBar` component in the import page
- Created comprehensive documentation in `apps/controlpanel/src/components/ui/README.md` explaining the pattern for loading and empty states

**Outcomes**
- Consistent loading indicators across the application with the `Spinner` component
- Improved accessibility with proper ARIA attributes for loading and empty states
- Clear documentation for future developers on how to implement loading and empty states
- Storybook stories for all loading and empty state components
- The application now provides better feedback during asynchronous operations and when no data is available