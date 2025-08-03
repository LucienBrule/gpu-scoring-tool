## Persona
You are the Frontend UI Engineer. Your role is to create a new Forecast tab that displays price forecast deltas using the `useForecastDeltas` hook with filtering capabilities.

## Title
Create Forecast Tab with Delta Visualization

## Purpose
Develop a new Forecast tab that leverages the `useForecastDeltas` hook to display price trend forecasts and comparative analysis. This feature will enable users to visualize price changes over time, filter by model and region, and make data-driven decisions based on predicted market trends.

## Requirements
1. Create a new Forecast page component in `apps/controlpanel/src/app/forecast/page.tsx` (or equivalent path).
2. Import and implement the `useForecastDeltas` hook created in TASK.web.v1.14.
3. Design an intuitive interface with:
   - Filter controls for model selection
   - Region/market selection dropdown
   - Time range selector (week, month, quarter)
   - Comparison period options
4. Implement visualizations for delta data:
   - Price trend charts (line or bar)
   - Percentage change indicators
   - Color-coded positive/negative changes
5. Add a tabular view for detailed delta information.
6. Implement proper loading states during data fetching.
7. Add error handling for failed API requests.
8. Create an export function for data (CSV or JSON).
9. Ensure responsive design for all screen sizes.
10. Add the Forecast tab to the main navigation.

## Constraints
- Maintain existing URL structure and routing.
- Ensure accessibility of all UI elements and visualizations.
- Use the Catppuccin Mocha theme palette for styling.
- Optimize rendering performance for complex visualizations.
- Ensure dark mode compatibility.
- Follow established component patterns from TASK.web.v1.33.
- Use lightweight charting libraries to minimize bundle size.

## Tests
- Verify the page correctly fetches data using `useForecastDeltas`.
- Test filtering functionality with various model and region combinations.
- Confirm time range and comparison period selectors work correctly.
- Test chart rendering with different data sets.
- Verify loading states display appropriately during data fetching.
- Confirm error states render correctly when API requests fail.
- Test data export functionality.
- Test responsive behavior on different screen sizes.
- Verify accessibility using browser dev tools.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
# Install charting library if needed (example)
pnpm --filter controlpanel add recharts
# Start development server
pnpm --filter controlpanel dev
# Open browser to view the forecast page
open http://localhost:3000/forecast
# Run tests if available
pnpm --filter controlpanel test src/app/forecast
```

## Completion Criteria
- The Forecast tab successfully uses the `useForecastDeltas` hook for data fetching.
- Filtering by model and region works correctly.
- Time range and comparison period selection functions properly.
- Visualizations accurately represent delta data.
- Tabular view provides detailed information.
- Data export functionality works as expected.
- Loading and error states provide appropriate feedback to users.
- The page is responsive and accessible across devices.
- The Forecast tab is accessible from the main navigation.
- All tests pass successfully.

## ✅ Task Completed
**Changes made**
- Created a new Forecast page component in `apps/controlpanel/src/app/forecast/page.tsx`
- Implemented the `useForecastDeltas` hook for data fetching
- Designed an intuitive interface with comprehensive filtering capabilities:
  - Model filter input
  - Region selection dropdown
  - Time range selector (7 days, 30 days, quarter, year)
  - Minimum price change percentage filter
- Implemented visualizations for delta data:
  - Bar chart showing price changes by model
  - Line chart showing price changes over time
  - Toggle between chart types
  - Color-coded positive/negative changes
- Added summary cards showing average change, largest increase, and largest decrease
- Created a tabular view with detailed delta information
- Implemented a CSV export function for data
- Added proper loading states with skeleton components
- Implemented error handling with error banners and retry functionality
- Ensured responsive design using Tailwind's grid system
- Added the Forecast tab to the main navigation

**Outcomes**
- Users can now visualize price forecast deltas with comprehensive filtering options
- The interface provides both high-level visualizations and detailed tabular data
- Users can export data for further analysis
- The page provides appropriate feedback during loading and error states
- The interface is responsive and works well on different screen sizes
- The implementation follows the Catppuccin Mocha theme palette for styling
- The page is accessible with proper ARIA attributes and semantic HTML


