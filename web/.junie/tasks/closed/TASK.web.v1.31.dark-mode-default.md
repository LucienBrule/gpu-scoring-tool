## Persona
You are the Frontend Integration Engineer. Your role is to configure the controlpanel application to use dark mode by default, ensuring a seamless and flash-free dark experience on first load.

## Title
Enable Default Dark Mode

## Purpose
Ensure that the controlpanel application applies the dark theme automatically on startup, providing users with a consistent dark-mode-first interface without manual toggling.

## Requirements
1. Confirm `apps/controlpanel/tailwind.config.js` has `darkMode: 'class'`.
2. Add logic in the application entrypoint (e.g., `apps/controlpanel/src/app/layout.tsx`) to add the `dark` class on the `<html>` element before the React app mounts.
3. Prevent flash of unstyled content (FOUC) by injecting the `dark` class via inline script or CSS hook before loading CSS.
4. Document the default behavior and how to override the theme via a CSS class or user toggle.

## Constraints
- Must not break server-side rendering or hydration.
- Avoid modifying core Tailwind CSS defaults beyond enabling the `class` strategy.
- Ensure compatibility with existing global styles and theme extensions.

## Tests
- On page load, confirm `<html>` element has `class="dark"`.
- Manually remove the `dark` class in DevTools and verify light-mode styles apply correctly.
- Write an end-to-end or unit test to assert `document.documentElement.classList.contains('dark')` on initialization.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install
pnpm --filter controlpanel dev
# Verify dark mode is applied:
sleep 2 && open http://localhost:3000 && \
  node -e "console.log(document.documentElement.classList.contains('dark'))"
```

## Completion Criteria
- The `dark` class is present on the `<html>` element by default.
- No flash of light mode occurs on initial load.
- The UI consistently renders using dark-mode styles.
- All dark-mode tests pass successfully.

## ✅ Task Completed

**Changes made**
- Confirmed that `darkMode: 'class'` was already set in the Tailwind configuration
- Modified `apps/controlpanel/src/app/layout.tsx` to add the `dark` class to the `<html>` element
- Added an inline script with `beforeInteractive` strategy to prevent flash of unstyled content (FOUC)
- Added `bg-background` and `text-foreground` classes to the body element for proper dark mode styling
- Created a test file in `apps/controlpanel/src/app/__tests__/layout.test.tsx` to verify dark mode implementation
- Created a comprehensive README in `apps/controlpanel/src/app/README.md` documenting the dark mode implementation and how to override it using the ThemeToggle component

**Outcomes**
- The application now uses dark mode by default with no flash of unstyled content
- The dark mode implementation is compatible with server-side rendering and hydration
- The existing ThemeToggle component still works correctly for users who want to switch to light mode
- The implementation follows best practices for Next.js and Tailwind CSS
- The dark mode implementation is thoroughly documented for future developers