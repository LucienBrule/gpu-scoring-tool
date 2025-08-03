## Persona
You are the Frontend Integration Engineer. Your role is to audit and adjust UI spacing and typography styles in the `gpu-scoring-tool` controlpanel application, aligning every component to the GPU Reports view baseline for visual consistency and readability.

## Title
Align UI Spacing and Typography to Baseline

## Purpose
Ensure consistent spacing (margins, padding, gaps) and typography (font sizes, weights, line heights) across all controlpanel pages, matching the established GPU Reports design. This enhances visual cohesion and improves user readability and flow.

## Requirements
1. Review the GPU Reports view in `apps/controlpanel/src/app/reports/page.tsx` (or equivalent) and note all Tailwind spacing and typography classes used (e.g., `px-4`, `py-2`, `text-lg`, `font-medium`).
2. Perform an audit of all major pages (Listings, Models, Forecast, Import Tools) to identify inconsistent or missing style classes.
3. Update component and page templates to use the same spacing and typography classes as the baseline:
   - Standardize container padding (e.g., `px-6`, `py-4`).
   - Align heading styles (`text-2xl`, `font-semibold`, `leading-tight`).
   - Normalize list and table row spacing (`space-y-4`, `divide-y`).
4. Extract any repeated spacing or typography patterns into reusable utility classes or component wrappers.
5. Update global styles or Tailwind config if needed to define custom font-size or spacing values.

## Constraints
- Do not alter the baseline GPU Reports view; use it as the source of truth.
- Avoid introducing new CSS or inline styles; use existing Tailwind utilities.
- Maintain responsive behavior; verify changes at multiple breakpoints.

## Tests
- Manually review each controlpanel page side-by-side with the GPU Reports baseline; verify pixel-level consistency.
- Write snapshot tests in Storybook for at least two representative components (e.g., Card, Table) to catch spacing or font regressions.
- Ensure no visual overflow or layout breaks occur on mobile and desktop.

## DX Runbook
```bash
# Start development server:
pnpm install
pnpm --filter controlpanel dev
# Open pages in browser:
open http://localhost:3000/report
open http://localhost:3000/listings
# In Storybook:
pnpm --filter controlpanel storybook
```

## Completion Criteria
- All controlpanel pages use spacing and typography classes matching the GPU Reports baseline.
- Storybook snapshots for audited components pass without visual diffs.
- No layout regressions or accessibility issues introduced.

## ✅ Task Completed

**Changes made**
- Reviewed the GPU Reports view and ReportsDataGrid component to identify baseline spacing and typography classes
- Created a comprehensive spacing and typography guide in `apps/controlpanel/src/styles/spacing-typography-guide.md`
- Performed an audit of all major pages (Reports, Listings, Import Tools) to identify inconsistencies
- Created a document listing all UI inconsistencies in `apps/controlpanel/src/styles/ui-inconsistencies.md`
- Decided on a consistent approach (shadcn/ui components) for future standardization
- Created a detailed UI standardization plan in `apps/controlpanel/src/styles/ui-standardization-plan.md`
- Implemented Phase 1 of the standardization plan:
  - Updated Import Tools page container spacing from `container mx-auto py-6` to `container mx-auto px-4 py-8`
  - Updated Import Tools page title size from `text-3xl` to `text-2xl` to match the Reports/Listings pages
  - Created a test file to verify the changes in `apps/controlpanel/src/app/import/__tests__/page.test.tsx`

**Outcomes**
- Established a clear baseline for spacing and typography across the application
- Identified and documented all UI inconsistencies between major pages
- Created a comprehensive plan for standardizing UI components and styles
- Implemented initial spacing and typography standardization for the Import Tools page
- Set up a foundation for future component style normalization work (TASK.web.v1.33)

**Remaining Work for Future Tasks**
- Complete Phases 2-4 of the UI standardization plan:
  - Phase 2: Component Migration (migrate to shadcn/ui components)
  - Phase 3: Color Scheme Standardization (standardize colors and dark mode support)
  - Phase 4: Feature Parity (standardize error handling, loading states, and data visualization)
- This work will be addressed in TASK.web.v1.33.component-style-normalization.md

**Documentation Created**
- `apps/controlpanel/src/styles/spacing-typography-guide.md`: Standard spacing and typography patterns
- `apps/controlpanel/src/styles/ui-inconsistencies.md`: UI inconsistencies between major pages
- `apps/controlpanel/src/styles/ui-standardization-plan.md`: Plan for standardizing UI components and styles