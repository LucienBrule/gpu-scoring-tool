# Spacing and Typography Guide

This document outlines the standard spacing and typography patterns to be used across the GPU Scoring Tool Control Panel, based on the GPU Reports view baseline.

## Spacing

### Container and Layout Spacing

- **Main container**: `container mx-auto px-4 py-8`
  - Center-aligned with auto horizontal margins
  - Horizontal padding: 1rem (16px)
  - Vertical padding: 2rem (32px)

- **Section margins**:
  - Between sections: `mb-6` (margin-bottom: 1.5rem)
  - Small vertical spacing: `mt-4` (margin-top: 1rem)
  - Standard vertical spacing: `mt-6` (margin-top: 1.5rem)

- **Grid layouts**:
  - Responsive grid: `grid grid-cols-1 md:grid-cols-3 gap-4`
  - Grid gap: 1rem (16px)

- **Flex layouts**:
  - Centered with space between: `flex items-center justify-between`
  - Horizontal spacing: `flex space-x-2`
  - Vertical alignment: `flex items-center`

### Component Spacing

- **Buttons**:
  - Primary buttons: `px-4 py-2` (horizontal: 1rem, vertical: 0.5rem)
  - Small buttons: `px-3 py-1` (horizontal: 0.75rem, vertical: 0.25rem)
  - Form buttons: `px-3 py-2` (horizontal: 0.75rem, vertical: 0.5rem)

- **Inputs**:
  - Standard inputs: `px-4 py-2` (horizontal: 1rem, vertical: 0.5rem)
  - Form inputs: `px-3 py-2` (horizontal: 0.75rem, vertical: 0.5rem)

- **Tables**:
  - Header cells: `px-6 py-3` (horizontal: 1.5rem, vertical: 0.75rem)
  - Body cells: `px-6 py-4` (horizontal: 1.5rem, vertical: 1rem)

- **Form groups**:
  - Vertical spacing: `space-y-2` (0.5rem between elements)

- **Horizontal spacing**:
  - Small gap: `space-x-2` (0.5rem between elements)
  - Large gap: `space-x-8` (2rem between elements)

## Typography

### Text Sizes and Weights

- **Headings**:
  - Page titles: `text-2xl font-bold` (1.5rem, bold)
  - Section headings: `text-xl font-semibold` (1.25rem, semibold)
  - Subsection headings: `text-lg font-medium` (1.125rem, medium)

- **Table text**:
  - Headers: `text-xs font-medium uppercase tracking-wider` (0.75rem, medium, uppercase, letter-spacing)
  - Cell content: `text-sm` (0.875rem)
  - Emphasized cell content: `text-sm font-medium` (0.875rem, medium)

- **Form text**:
  - Labels: `text-sm font-medium` (0.875rem, medium)
  - Helper text: `text-sm text-gray-500` (0.875rem, gray)
  - Input text: `text-sm` (0.875rem)

- **Informational text**:
  - Standard text: `text-sm text-gray-700` (0.875rem, dark gray)
  - Secondary text: `text-sm text-gray-500` (0.875rem, medium gray)
  - Small text: `text-xs text-gray-400` (0.75rem, light gray)

## Borders and Dividers

- **Tables**:
  - Table border: `border border-gray-200`
  - Row dividers: `divide-y divide-gray-500`

- **Inputs and controls**:
  - Input borders: `border border-gray-300`

- **Rounded corners**:
  - Small radius: `rounded` (0.25rem)
  - Medium radius: `rounded-md` (0.375rem)
  - Large radius: `rounded-lg` (0.5rem)

## Interactive States

- **Focus states**:
  - Standard focus: `focus:outline-none focus:ring-2 focus:ring-blue-500`

- **Hover states**:
  - Button hover: `hover:bg-blue-700` (darker blue)
  - Table row hover: `hover:bg-gray-600` (darker gray)
  - Table header hover: `hover:bg-gray-500` (medium gray)

- **Disabled states**:
  - Disabled appearance: `bg-gray-700 text-gray-300 cursor-not-allowed`

## Responsive Patterns

- **Responsive visibility**:
  - Hide on mobile: `hidden md:table-cell` (hidden by default, table-cell on medium screens and up)
  - Show on mobile: `block md:hidden` (block by default, hidden on medium screens and up)

- **Responsive layout**:
  - Single column to multi-column: `grid-cols-1 md:grid-cols-3` (1 column by default, 3 columns on medium screens and up)

## Usage Guidelines

1. Use these spacing and typography patterns consistently across all pages and components.
2. Maintain the hierarchy of text sizes and weights to ensure proper visual hierarchy.
3. Ensure consistent spacing between related elements to create visual grouping.
4. Use responsive patterns to ensure good appearance on all screen sizes.
5. When creating new components, reference this guide to maintain consistency.