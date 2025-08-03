# UI Inconsistencies Audit

This document outlines the inconsistencies found between different pages in the GPU Scoring Tool Control Panel. The goal is to identify areas that need standardization to ensure a consistent user experience across the application.

## Pages Audited

1. **Reports Page** (`/app/reports/page.tsx` and `/components/reports/ReportsDataGrid.tsx`)
2. **Listings Page** (`/app/listings/page.tsx`)
3. **Import Tools Page** (`/app/import/page.tsx`)

## Component Approach Inconsistencies

### Reports & Listings Pages
- Use direct Tailwind classes for styling
- Build UI elements from scratch with HTML elements
- No explicit component abstractions

### Import Tools Page
- Uses shadcn/ui components from `@repo/ui/*` (Card, Button, Input, etc.)
- Component-based approach with proper abstractions
- Better dark mode support with explicit dark mode classes

## Spacing Inconsistencies

### Container Spacing
- **Reports/Listings**: `container mx-auto px-4 py-8`
- **Import Tools**: `container mx-auto py-6` (missing horizontal padding)

### Section Margins
- **Reports/Listings**: `mb-6` for section spacing
- **Import Tools**: Various spacing classes (`mb-6`, `mb-4`, `space-y-4`)

### Form Element Spacing
- **Reports/Listings**: `px-4 py-2` for inputs
- **Import Tools**: Uses shadcn/ui components with their own spacing

## Typography Inconsistencies

### Page Titles
- **Reports/Listings**: `text-2xl font-bold`
- **Import Tools**: `text-3xl font-bold`

### Section Headings
- **Reports/Listings**: No consistent pattern
- **Import Tools**: Uses CardTitle component

### Form Labels
- **Reports/Listings**: `text-sm font-medium text-gray-500`
- **Import Tools**: Uses Label component

## Color Inconsistencies

### Table Styling
- **Reports**:
  - Header: `bg-gray-500:35`
  - Header text: `text-white`
  - Row hover: `hover:bg-gray-600`
  - Dividers: `divide-y divide-gray-500`

- **Listings**:
  - Header: `bg-gray-50`
  - Header text: `text-gray-500`
  - Row hover: `hover:bg-gray-50`
  - Dividers: `divide-y divide-gray-200`

### Button Styling
- **Reports**:
  - Primary: `bg-blue-500 text-white rounded hover:bg-blue-700`
  - Pagination: `bg-gray-400 text-white hover:bg-blue-500`
  - Disabled: `bg-gray-700 text-gray-300 cursor-not-allowed`

- **Listings**:
  - Primary: `bg-blue-500 text-white rounded hover:bg-blue-600`
  - Pagination: `bg-white text-gray-700 hover:bg-gray-50 border border-gray-300`
  - Disabled: `bg-gray-100 text-gray-400 cursor-not-allowed`

- **Import Tools**:
  - Uses shadcn/ui Button component with variants

### Dark Mode Support
- **Reports/Listings**: Limited dark mode classes
- **Import Tools**: Extensive dark mode support with `dark:` prefixed classes

## Interactive Elements Inconsistencies

### Buttons
- **Reports/Listings**: Direct HTML buttons with Tailwind classes
- **Import Tools**: shadcn/ui Button component with variants

### Inputs
- **Reports/Listings**: Direct HTML inputs with Tailwind classes
- **Import Tools**: shadcn/ui Input component

### Dropdowns/Selects
- **Reports/Listings**: Direct HTML selects with Tailwind classes
- **Import Tools**: shadcn/ui Select component

## Feature Inconsistencies

### Error Handling
- **Reports/Listings**: Uses ErrorBanner component
- **Import Tools**: Uses shadcn/ui Alert component

### Loading States
- **Reports/Listings**: Uses Skeleton component
- **Import Tools**: Text-based loading indicators and progress bars

### Data Visualization
- **Reports**: Color-coded scores based on value
- **Listings**: No color coding for scores

## Recommendations

Based on the audit, we recommend the following approach to standardize the UI:

1. **Component Approach**: Adopt the shadcn/ui component approach used in the Import Tools page, as it provides better abstraction, reusability, and dark mode support.

2. **Container Spacing**: Standardize on `container mx-auto px-4 py-8` for main container spacing.

3. **Typography**: 
   - Page titles: `text-2xl font-bold` (Reports/Listings) or `text-3xl font-bold` (Import Tools)
   - Standardize on one approach

4. **Color Scheme**:
   - Adopt dark mode compatible colors throughout
   - Standardize table styling (headers, rows, hover states)
   - Standardize button styling with consistent variants

5. **Interactive Elements**:
   - Use shadcn/ui components for all interactive elements
   - Ensure consistent focus, hover, and active states

6. **Feature Parity**:
   - Add color coding for scores in Listings page
   - Standardize error handling and loading states
   - Add tooltips for column headers in Listings page

## Implementation Priority

1. Update container spacing and typography first (easiest wins)
2. Migrate to shadcn/ui components where direct Tailwind is used
3. Standardize color scheme and interactive states
4. Add missing features for feature parity