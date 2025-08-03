# GPU Scoring Tool Control Panel

This directory contains the main application code for the GPU Scoring Tool Control Panel.

## Dark Mode Implementation

The application uses Tailwind CSS with the `darkMode: 'class'` strategy and is configured to use dark mode by default.

### How Dark Mode is Applied

1. The `dark` class is added to the `<html>` element in the `layout.tsx` file:
   ```tsx
   <html lang="en" className="dark">
   ```

2. An inline script is added to prevent flash of unstyled content (FOUC):
   ```tsx
   <Script id="set-dark-mode" strategy="beforeInteractive">
     {`
       // This script ensures dark mode is applied before the page renders
       // to prevent flash of unstyled content (FOUC)
       (function() {
         document.documentElement.classList.add('dark');
       })();
     `}
   </Script>
   ```

3. The body element uses Tailwind's dark mode utility classes:
   ```tsx
   <body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}>
   ```

### Overriding Dark Mode

The application includes a `ThemeToggle` component that allows users to switch between light and dark mode:

1. Import the ThemeToggle component:
   ```tsx
   import ThemeToggle from "@/components/ThemeToggle";
   ```

2. Add it to your component:
   ```tsx
   <ThemeToggle />
   ```

The ThemeToggle component:
- Initializes the theme based on localStorage or system preference
- Updates the document class and localStorage when the theme changes
- Provides a button to toggle between light and dark mode

### How ThemeToggle Works

The ThemeToggle component manages theme state using React's useState and useEffect hooks:

1. It checks localStorage for a saved theme preference
2. If no preference is found, it checks the system preference using `window.matchMedia('(prefers-color-scheme: dark)')`
3. It updates the document classes and localStorage when the theme changes
4. It provides a button to toggle between light and dark mode

### Testing Dark Mode

Tests for the dark mode implementation can be found in `__tests__/layout.test.tsx`. These tests verify:

1. The `<html>` element has the `dark` class
2. The script to prevent FOUC is included with the correct attributes
3. The body has the proper background and text color classes

## Color Palette

The application uses the Catppuccin Mocha color palette, which is defined in the Tailwind configuration file (`tailwind.config.js`). This provides a consistent dark-mode-first color scheme across the application.

The main colors are:
- `background`: Base color for backgrounds (`#1e1e2e`)
- `foreground`: Base color for text (`#cdd6f4`)
- `primary`: Primary accent color (`#cba6f7`)
- `secondary`: Secondary accent color (`#89b4fa`)

For more details on the color palette, see the Tailwind configuration file.