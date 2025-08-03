## Persona
You are the Frontend UI Engineer. Your role is to refactor the GPU Reports page to use the newly created `useGpuReports` hook and implement proper rendering of markdown content and structured statistics.

## Title
Refactor GPU Reports Page to Use useGpuReports Hook

## Purpose
Enhance the GPU Reports page by integrating the type-safe `useGpuReports` hook, enabling the display of rich markdown content and structured statistics. This refactoring will improve data fetching, error handling, and loading states while providing users with more detailed and formatted GPU analysis reports.

## Requirements
1. Refactor the existing GPU Reports page component in `apps/controlpanel/src/app/reports/page.tsx` (or equivalent path).
2. Import and implement the `useGpuReports` hook created in TASK.web.v1.13.
3. Add proper loading states during data fetching.
4. Implement error handling for failed API requests.
5. Render markdown content using a suitable markdown renderer (e.g., `react-markdown`).
6. Display structured statistics in an organized, visually appealing format.
7. Add filtering capabilities to select different reports by model or type.
8. Ensure responsive design for all screen sizes.

## Constraints
- Maintain existing URL structure and routing.
- Ensure accessibility of all rendered content, including proper heading hierarchy in markdown.
- Use the Catppuccin Mocha theme palette for styling.
- Optimize rendering performance, especially for large markdown documents.
- Ensure dark mode compatibility.

## Tests
- Verify the page correctly fetches data using `useGpuReports`.
- Test with various report types and content lengths.
- Confirm loading states display appropriately during data fetching.
- Verify error states render correctly when API requests fail.
- Test markdown rendering with complex content (tables, code blocks, images).
- Ensure responsive behavior on different screen sizes.
- Verify accessibility using browser dev tools.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
# Install markdown renderer if not already present
pnpm --filter controlpanel add react-markdown
# Start development server
pnpm --filter controlpanel dev
# Open browser to view the reports page
open http://localhost:3000/reports
# Run tests if available
pnpm --filter controlpanel test src/app/reports
```

## Completion Criteria
- The GPU Reports page successfully uses the `useGpuReports` hook for data fetching.
- Markdown content renders correctly with proper formatting.
- Structured statistics are displayed in a clear, organized manner.
- Loading and error states provide appropriate feedback to users.
- The page is responsive and accessible across devices.
- All tests pass successfully.

## ✅ Task Completed
**Changes made**
- Created a new `MarkdownReport` component for displaying markdown content and structured statistics
- Refactored the Reports page to use the `useGpuReports` hook instead of `useReports`
- Implemented proper rendering of markdown content using `react-markdown`
- Added tabbed interface to display report content, summary statistics, and scoring weights
- Displayed structured statistics in an organized, visually appealing format
- Added filtering capabilities (model filter and limit)
- Implemented proper loading states with skeleton components
- Added error handling with error banners and retry functionality
- Ensured responsive design using Tailwind's grid system
- Maintained accessibility with proper ARIA attributes and semantic HTML

**Outcomes**
- The GPU Reports page now displays rich markdown content and structured statistics
- Users can filter reports by model and limit the number of reports displayed
- The page provides appropriate feedback during loading and error states
- The interface is responsive and works well on different screen sizes
- The implementation follows the Catppuccin Mocha theme palette for styling
- The page is accessible with proper heading hierarchy and ARIA attributes


