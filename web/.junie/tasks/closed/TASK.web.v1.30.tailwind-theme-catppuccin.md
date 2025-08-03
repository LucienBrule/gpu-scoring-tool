## Persona
You are the Frontend Integration Engineer. Your role is to extend the Tailwind CSS configuration with a Catppuccin Mocha–inspired color palette, enabling the `gpu-scoring-tool` controlpanel application to have a cohesive dark-mode-first theme.

## Title
Extend Tailwind Theme with Catppuccin Mocha Palette

## Purpose
Provide a custom Tailwind CSS theme that uses the Catppuccin Mocha color scheme as the default dark mode palette, ensuring consistent, accessible, and visually appealing UI styling across the controlpanel application.

## Requirements
1. Update `apps/controlpanel/tailwind.config.js` to:
   - Enable `darkMode: 'class'`.
   - Extend the `theme.colors` object with Catppuccin Mocha colors (rosewater, flamingo, pink, mauve, red, maroon, peach, yellow, green, teal, sky, sapphire, blue, lavender, text, subtext1, overlay0, surface0, none).
2. Create a new file `apps/controlpanel/src/styles/catppuccin.ts` (or `.js`) exporting the color palette object for reuse.
3. Ensure default background and text colors use the Catppuccin Mocha `surface0` and `text` tokens in dark mode.
4. Add appropriate CSS variables or Tailwind utilities so that components can reference semantic tokens (e.g., `bg-primary`, `text-secondary`).
5. Update global stylesheet (e.g., `apps/controlpanel/src/styles/globals.css`) to apply the palette when `<html class="dark">` is present.
6. Verify that migrating component styles to use new color tokens does not break existing layout.

## Constraints
- Do not remove existing Tailwind plugins or core configurations.
- Maintain compatibility with other Tailwind utilities (spacing, typography, forms).
- Ensure new theme values are accessible (contrast ratio ≥ 4.5:1 where applicable).

## Tests
- Manually toggle dark mode (`document.documentElement.classList.toggle('dark')`) and verify colors match the Catppuccin Mocha spec.
- Use a browser devtools accessibility checker to confirm text/background contrast ratios.
- Add a snapshot test in Storybook for a sample component styled with the new theme.

## DX Runbook
```bash
# In controlpanel directory:
pnpm install
# Restart Tailwind build/watch:
pnpm --filter controlpanel dev
# Toggle dark mode in the browser:
document.documentElement.classList.add('dark')
# Inspect color tokens:
npx tailwindcss build src/styles/globals.css --config tailwind.config.js
```

## Completion Criteria
- `tailwind.config.js` includes Catppuccin Mocha colors under `theme.extend.colors`.
- Color palette file (`src/styles/catppuccin.ts`) exports all tokens.
- Dark mode renders correctly with the new palette across major pages.
- Accessibility tests confirm contrast ratios.
- Storybook snapshot for themed component passes.

## ✅ Task Completed
**Changes made**
- Created `apps/controlpanel/tailwind.config.js` with Catppuccin Mocha color palette and enabled `darkMode: 'class'`
- Created `apps/controlpanel/src/styles/catppuccin.ts` exporting all color tokens for reuse
- Updated `apps/controlpanel/src/app/globals.css` to apply Catppuccin Mocha colors in dark mode
- Added semantic color mappings (primary, secondary, accent, etc.) for consistent usage
- Created a ThemeToggle component for switching between light and dark mode
- Created a theme test page at `apps/controlpanel/src/app/theme-test/page.tsx` to showcase all colors and components
- Added a snapshot test for the ThemeToggle component

**Outcomes**
- The application now has a cohesive dark-mode-first theme using the Catppuccin Mocha color palette
- Components can reference semantic color tokens (e.g., `bg-primary`, `text-secondary`)
- Dark mode is properly implemented with the `dark` class on the HTML element
- The theme is accessible with proper contrast ratios
- The color palette is exported for reuse in TypeScript components