# UI Standardization Plan

This document outlines the approach for standardizing UI components and styles across the GPU Scoring Tool Control Panel, based on the inconsistencies identified in the audit.

## Standardization Approach

After reviewing the different approaches used across the application, we've decided to standardize on the **shadcn/ui component approach** used in the Import Tools page for the following reasons:

1. Better component abstraction and reusability
2. Built-in dark mode support
3. Consistent styling across interactive elements
4. Easier maintenance and updates
5. Alignment with modern React best practices

## Implementation Plan

### Phase 1: Container and Typography Standardization

1. **Container Spacing**
   - Standardize on `container mx-auto px-4 py-8` for all page containers
   - Update Import Tools page to add the missing horizontal padding

2. **Typography**
   - Standardize on `text-2xl font-bold` for page titles (from Reports/Listings)
   - Use shadcn/ui Typography components where appropriate
   - Create consistent heading hierarchy:
     - Page titles: `text-2xl font-bold`
     - Section headings: `text-xl font-semibold`
     - Subsection headings: `text-lg font-medium`

### Phase 2: Component Migration

1. **Tables**
   - Create a reusable DataTable component using shadcn/ui Table
   - Migrate Reports and Listings tables to use this component
   - Ensure consistent styling for headers, rows, and hover states
   - Add dark mode support with appropriate dark: classes

2. **Forms and Inputs**
   - Migrate all direct HTML inputs to shadcn/ui Input components
   - Migrate all direct HTML selects to shadcn/ui Select components
   - Standardize on shadcn/ui Label component for form labels
   - Ensure consistent spacing and styling

3. **Buttons**
   - Migrate all direct HTML buttons to shadcn/ui Button components
   - Define standard button variants:
     - Primary: For main actions
     - Secondary/Outline: For secondary actions
     - Destructive: For delete/remove actions
     - Ghost: For low-emphasis actions

4. **Cards and Sections**
   - Use shadcn/ui Card components for content sections
   - Standardize on CardHeader, CardTitle, CardDescription, and CardContent structure

### Phase 3: Color Scheme Standardization

1. **Dark Mode Support**
   - Add explicit dark mode classes to all components
   - Ensure consistent color transitions between light and dark modes

2. **Table Colors**
   - Standardize on dark-friendly table styling:
     - Header: `bg-gray-500:35` (from Reports)
     - Header text: `text-white` (from Reports)
     - Row hover: `hover:bg-gray-600` (from Reports)
     - Dividers: `divide-y divide-gray-500` (from Reports)

3. **Button Colors**
   - Standardize on shadcn/ui button variants
   - Ensure consistent hover and focus states

### Phase 4: Feature Parity

1. **Error Handling**
   - Standardize on shadcn/ui Alert component for error messages
   - Migrate ErrorBanner usage to Alert component

2. **Loading States**
   - Standardize on Skeleton component for loading states
   - Add progress indicators where appropriate

3. **Data Visualization**
   - Add color coding for scores in Listings page
   - Add tooltips for column headers in Listings page

## Files to Update

### High Priority

1. **Listings Page**
   - `/apps/controlpanel/src/app/listings/page.tsx`
   - Migrate to shadcn/ui components
   - Update container spacing
   - Add color coding for scores

2. **Reports Page**
   - `/apps/controlpanel/src/app/reports/page.tsx`
   - Migrate to shadcn/ui components
   - Ensure dark mode compatibility

3. **Import Tools Page**
   - `/apps/controlpanel/src/app/import/page.tsx`
   - Update container spacing to match standard
   - Update page title size to match standard

### Medium Priority

1. **ReportsDataGrid Component**
   - `/apps/controlpanel/src/components/reports/ReportsDataGrid.tsx`
   - Refactor to use shadcn/ui Table component
   - Ensure dark mode compatibility

2. **Common Components**
   - Create reusable DataTable component
   - Create reusable FilterBar component
   - Create reusable PaginationControls component

### Low Priority

1. **Other Pages**
   - Apply standardization to any other pages in the application
   - Ensure consistent styling across all pages

## Testing Plan

1. **Visual Testing**
   - Compare before/after screenshots of each page
   - Verify consistent appearance across pages

2. **Responsive Testing**
   - Test at multiple breakpoints (mobile, tablet, desktop)
   - Ensure consistent responsive behavior

3. **Dark Mode Testing**
   - Test in both light and dark modes
   - Verify smooth transitions between modes

4. **Accessibility Testing**
   - Verify proper contrast ratios
   - Test keyboard navigation
   - Test screen reader compatibility

## Timeline

1. **Phase 1 (Container and Typography)**: 1 day
2. **Phase 2 (Component Migration)**: 2-3 days
3. **Phase 3 (Color Scheme)**: 1 day
4. **Phase 4 (Feature Parity)**: 1-2 days

Total estimated time: 5-7 days

## Success Criteria

1. All pages use consistent spacing and typography
2. All interactive elements use shadcn/ui components
3. Dark mode works consistently across all pages
4. No visual regressions in functionality
5. All tests pass successfully