## Persona
You are the Frontend Integration Engineer. Your role is to develop a lightweight Sparkline/Trendline component that renders inline data visualizations for market volatility and price trends in the `gpu-scoring-tool` controlpanel application.

## Title
Develop Sparkline Trendline Component

## Purpose
Enable compact, high-density visualization of time-series or array-based metrics (e.g., price deltas over time) directly within tables or list items, providing users with at-a-glance trend insights without navigating to detailed charts.

## Requirements
1. Create a new file `apps/controlpanel/src/components/ui/Sparkline.tsx`.
2. Implement the component using SVG or a minimal library (e.g., `d3-shape`) with a small footprint.
3. Accept props:
   - `data: number[]` (required): array of numeric values to plot.
   - `width?: number`, `height?: number` (defaults to 100×24).
   - `color?: string` (defaults to a theme token or CSS variable).
   - `strokeWidth?: number` (defaults to 2).
   - `gradientFill?: boolean` (optional): whether to fill the area under the curve.
4. Render a single `<path>` in SVG scaled to the viewBox, handling edge cases:
   - If `data` is empty or has a single value, render a flat line at mid-height.
5. Integrate theme tokens (Catppuccin Mocha) via CSS variables or props for color styling.
6. Ensure accessibility: include `role="img"` and an `aria-label` describing the data.

## Constraints
- Do not introduce large charting libraries; keep bundle size minimal.
- Use only existing dependencies or minimal utility packages.
- Ensure the component is responsive and performant.

## Tests
1. Write Storybook stories in `apps/controlpanel/src/components/ui/Sparkline.stories.tsx` showcasing:
   - Standard line sparkline.
   - Sparkline with gradient fill.
   - Handling of empty and single-value data arrays.
2. Add unit tests in `apps/controlpanel/src/components/ui/__tests__/Sparkline.test.tsx` using React Testing Library:
   - Verify correct SVG path generation for a sample data array.
   - Assert that `aria-label` contains data summary (e.g., "Sparkline with 5 points").
   - Test that `gradientFill` prop renders an additional `<linearGradient>` element.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install --filter controlpanel
pnpm --filter controlpanel storybook
# View Sparkline stories in Storybook:
# - Sparkline/Standard
# - Sparkline/WithGradient
# - Sparkline/EmptyData
```

## Completion Criteria
- `apps/controlpanel/src/components/ui/Sparkline.tsx` implements the Sparkline component correctly.
- Storybook stories demonstrate all required variations.
- Unit tests pass with full coverage for path generation and accessibility.

## ✅ Task Completed
**Changes made**
- Created `apps/controlpanel/src/components/ui/Sparkline.tsx` implementing a lightweight SVG-based sparkline component
- Implemented the component with all required props:
  - `data: number[]` for the values to plot
  - `width` and `height` with defaults of 100×24
  - `color` with default of "currentColor"
  - `strokeWidth` with default of 2
  - `gradientFill` for optional area fill under the curve
- Added proper handling of edge cases (empty data, single value, same values)
- Ensured accessibility with `role="img"` and descriptive `aria-label`
- Created comprehensive Storybook stories in `apps/controlpanel/src/components/ui/stories/Sparkline.stories.tsx`
- Added unit tests in `apps/controlpanel/src/components/ui/__tests__/Sparkline.test.tsx`

**Outcomes**
- All tests pass successfully
- The component renders different trend types (upward, downward, volatile, flat)
- Edge cases are handled correctly
- Accessibility is properly implemented
- The component is lightweight and performant, using only SVG without external dependencies
- The component can be easily integrated into tables or list items for inline visualization