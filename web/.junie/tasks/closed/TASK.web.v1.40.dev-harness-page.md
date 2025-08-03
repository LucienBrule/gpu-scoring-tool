## Persona
You are the Frontend Integration Engineer. Your role is to build and maintain a Developer Harness page that exposes all API hooks and endpoints, facilitating manual testing and debugging in the `gpu-scoring-tool` controlpanel application.

## Title
Create Developer Harness Page for API and Hook Testing

## Purpose
Provide developers with an isolated interface to exercise every React hook, API endpoint, and component state, streamlining debugging, validation, and QA without navigating through full application flows.

## Requirements
1. Create a new page at `apps/controlpanel/src/app/dev-harness/page.tsx`.
2. Import and render each hook (`useHealth`, `useGpuModels`, `useGpuListings`, `useGpuReports`, `useForecastDeltas`, `useGpuClassification`, etc.) with UI controls to trigger queries (buttons, inputs).
3. Display raw JSON responses, loading states, and error messages for each hook invocation.
4. Add simple form controls for endpoints requiring parameters (e.g., deltas filter, classification input).
5. Include a section to test file uploads (`useImportCsv`, `useImportFromPipeline`, `useValidateArtifact`) with file pickers and response display.
6. Style the page minimally using existing component styles and Tailwind utilities; prioritize functionality over polish.
7. Add a navigation link or route (`/dev-harness`) accessible only in development mode.

## Constraints
- Do not bundle heavy dependencies; use only already installed packages.
- Feature-flag the page so it is not available in production builds (e.g., based on `NODE_ENV`).
- Maintain existing routing and layout patterns.

## Tests
- Manually navigate to `/dev-harness` in development and verify each hook triggers the correct network request.
- Confirm loading and error states render as expected.
- Upload a sample CSV to validate import hooks and view responses.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install
pnpm --filter controlpanel dev
# Open Developer Harness:
open http://localhost:3000/dev-harness
```

## Completion Criteria
- `apps/controlpanel/src/app/dev-harness/page.tsx` exists and implements all hook testing interfaces.
- The page is only accessible in development mode.
- All hooks can be exercised and display correct data, errors, and loading states.

## ✅ Task Completed
**Changes made**
- Created a comprehensive dev-harness page at `apps/controlpanel/src/app/dev-harness/page.tsx`
- Implemented testing interfaces for all hooks:
  - Health: useHealth
  - Data: useGpuListings, useGpuModels, useGpuReports, useSchemaInfo
  - Forecast: useForecastDeltas
  - Import: useImportCsv, useImportFromPipeline, useValidateArtifact
  - ML: useGpuClassification
- Added UI controls for triggering queries with appropriate parameters
- Implemented display of raw JSON responses, loading states, and error messages
- Added file upload testing for import hooks with file pickers and response display
- Feature-flagged the page to only be accessible in development mode
- Added a navigation link in the Navbar that only appears in development mode
- Used existing component styles and Tailwind utilities for consistent styling

**Outcomes**
- Developers now have an isolated interface to test all hooks and endpoints
- The page streamlines debugging, validation, and QA without navigating through full application flows
- All hooks can be exercised with appropriate parameters and display correct data, errors, and loading states
- The page is only accessible in development mode, ensuring it doesn't appear in production builds
