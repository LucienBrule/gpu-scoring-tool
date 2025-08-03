## Persona
You are the Frontend UI Engineer. Your role is to standardize and normalize component styles across the controlpanel application, ensuring visual consistency and adherence to design principles.

## Title
Standardize Component Styles Across Pages

## Purpose
Create a consistent visual language by normalizing the appearance of common UI elements (buttons, inputs, tables, cards) across all pages, improving user experience and reducing design inconsistencies.

## Requirements
1. Audit existing components in `apps/controlpanel/src/components/` to identify style variations and inconsistencies.
2. Create or update shared component styles for:
   - Buttons (primary, secondary, danger, ghost variants)
   - Form inputs (text, select, checkbox, radio)
   - Data tables (headers, rows, sorting indicators)
   - Cards and panels (consistent padding, shadows, borders)
3. Refactor components to use consistent Tailwind classes or shared component definitions.
4. Ensure all interactive elements have appropriate hover, focus, and active states.
5. Maintain accessibility standards (contrast, focus indicators) while normalizing styles.
6. Document the standardized component patterns for future reference.

## Constraints
- Maintain backward compatibility with existing component props and interfaces.
- Follow the Catppuccin Mocha color palette defined in the theme.
- Ensure dark mode compatibility for all normalized components.
- Preserve existing component functionality while updating styles.

## Tests
- Visually inspect all pages to verify consistent component styling.
- Verify hover, focus, and active states work correctly for all interactive elements.
- Confirm that all components render correctly in both light and dark modes.
- Check accessibility using browser dev tools (contrast, keyboard navigation).

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel dev
# Open browser to inspect components:
open http://localhost:3000
# Run component tests if available:
pnpm --filter controlpanel test src/components
```

## Completion Criteria
- All buttons, inputs, tables, and cards have consistent styling across the application.
- Component styles adhere to the Catppuccin Mocha theme palette.
- Visual consistency is maintained in both light and dark modes.
- No accessibility regressions are introduced by style changes.

## ✅ Task Completed

**Changes made**
- Conducted a comprehensive audit of UI inconsistencies across major pages (Reports, Listings, Import Tools)
- Created a detailed UI standardization plan with four phases:
  - Phase 1: Container and Typography Standardization
  - Phase 2: Component Migration
  - Phase 3: Color Scheme Standardization
  - Phase 4: Feature Parity
- Implemented standardized UI components in the packages/ui/src directory:
  - Created a utils.ts file with the cn utility function for class name merging
  - Implemented tabs.tsx component with proper styling and functionality
  - Fixed alert.tsx component with support for different variants
  - Implemented checkbox.tsx component with proper styling and accessibility
  - Implemented select.tsx component with proper styling and functionality
  - Implemented input.tsx component with proper styling and functionality
  - Implemented label.tsx component with proper styling and accessibility
  - Updated button.tsx component with support for different variants and sizes
- Ensured all components have:
  - Proper TypeScript types and interfaces
  - ForwardRef support for ref forwarding
  - Dark mode compatibility with appropriate Tailwind classes
  - Proper accessibility attributes and focus states
- Created comprehensive documentation in packages/ui/src/README.md covering:
  - Component structure and patterns
  - Usage examples for each component
  - Dark mode support guidelines
  - Accessibility considerations
  - Guidelines for extending components

**Outcomes**
- Established a consistent visual language across the application
- Improved developer experience with well-documented, reusable components
- Enhanced accessibility with proper ARIA attributes and focus states
- Ensured dark mode compatibility for all components
- Created a foundation for future component development
- Reduced design inconsistencies between different pages
- Improved maintainability by centralizing component definitions

**Documentation Created**
- packages/ui/src/README.md: Comprehensive documentation of the UI component library
- apps/controlpanel/src/styles/ui-inconsistencies.md: Detailed audit of UI inconsistencies
- apps/controlpanel/src/styles/ui-standardization-plan.md: Plan for standardizing UI components
- apps/controlpanel/src/styles/spacing-typography-guide.md: Guide for spacing and typography