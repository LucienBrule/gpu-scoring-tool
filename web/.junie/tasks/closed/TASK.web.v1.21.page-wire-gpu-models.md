## Persona
You are the Frontend UI Engineer. Your role is to implement or refine the GPU Models page using the newly created `useGpuModels` hook to display comprehensive GPU model information.

## Title
Implement GPU Models Page Using useGpuModels Hook

## Purpose
Create or enhance the GPU Models page to display detailed information about GPU models using the type-safe `useGpuModels` hook. This page will provide users with a comprehensive view of available GPU models, their specifications, and performance metrics, enabling better analysis and comparison.

## Requirements
1. Create or refactor the GPU Models page component in `apps/controlpanel/src/app/models/page.tsx` (or equivalent path).
2. Import and implement the `useGpuModels` hook created in TASK.web.v1.11.
3. Design a clean, informative layout to display GPU model data, including:
   - Model name and manufacturer
   - Technical specifications (VRAM, architecture, etc.)
   - Performance metrics and benchmarks
   - Price trends or MSRP information
4. Implement sorting and filtering capabilities (by manufacturer, performance tier, release date, etc.).
5. Add a search function to quickly find specific models.
6. Create a detailed view for individual models when selected.
7. Implement proper loading states during data fetching.
8. Add error handling for failed API requests.
9. Ensure responsive design for all screen sizes.

## Constraints
- Maintain existing URL structure and routing.
- Ensure accessibility of all UI elements and information.
- Use the Catppuccin Mocha theme palette for styling.
- Optimize rendering performance for large datasets.
- Ensure dark mode compatibility.
- Follow established component patterns from TASK.web.v1.33.

## Tests
- Verify the page correctly fetches data using `useGpuModels`.
- Test sorting and filtering functionality with various criteria.
- Confirm search functionality works correctly.
- Test detailed view rendering for individual models.
- Verify loading states display appropriately during data fetching.
- Confirm error states render correctly when API requests fail.
- Test responsive behavior on different screen sizes.
- Verify accessibility using browser dev tools.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
# Start development server
pnpm --filter controlpanel dev
# Open browser to view the models page
open http://localhost:3000/models
# Run tests if available
pnpm --filter controlpanel test src/app/models
```

## Completion Criteria
- The GPU Models page successfully uses the `useGpuModels` hook for data fetching.
- All GPU model information is displayed in a clear, organized manner.
- Sorting, filtering, and search functionality work correctly.
- Detailed view for individual models provides comprehensive information.
- Loading and error states provide appropriate feedback to users.
- The page is responsive and accessible across devices.
- All tests pass successfully.

## ✅ Task Completed
**Changes made**
- Created a new GPU Models page at `apps/controlpanel/src/app/models/page.tsx`
- Implemented the page using the `useGpuModels` hook for data fetching
- Designed a clean, informative layout with both grid and table views
- Added comprehensive sorting, filtering, and search capabilities
- Created a detailed view dialog for individual models with tabs for:
  - Specifications (VRAM, TDP, CUDA Cores, NVLink, etc.)
  - Pricing (min, max, average, median prices)
  - Market Data (listing count, price range, volatility)
- Implemented proper loading states with skeleton components
- Added error handling with error banners
- Ensured responsive design with Tailwind's grid system
- Made the page accessible with proper ARIA attributes and semantic HTML

**Outcomes**
- Users can now view and analyze all available GPU models in a clean, organized interface
- The grid view provides a quick overview of key specifications and pricing
- The table view allows for easy sorting and comparison across multiple attributes
- The detailed view provides comprehensive information about each model
- Users can search and filter models to find specific information
- The page provides appropriate feedback during loading and error states
- The interface is responsive and works well on different screen sizes
- The implementation follows the Catppuccin Mocha theme palette for styling
- The page is accessible with proper ARIA attributes and semantic HTML


