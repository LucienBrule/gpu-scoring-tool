# TASK.web.01.ui.01.add-navbar

## 📌 Title
Add a global navigation component (`Navbar`) to the frontend interface

## 📁 Location
`web/apps/controlpanel/src/components/Navbar.tsx`

## 🧠 Context
This task initiates the primary layout and navigation scaffold for the GPU Scoring Tool frontend. Right now, there is no top-level navigation between views (e.g. Reports, About). We want to add a persistent `<Navbar />` that links to core routes and can be styled with Tailwind + shadcn/ui.

Junie-Web will implement this component to:
- Establish visual and routing consistency
- Allow for page switching across views (`/`, `/reports`, `/about`)
- Be reused across layout.tsx or page boundaries

## ✅ Requirements

- Create a reusable `Navbar` React component
- Use Tailwind and/or `shadcn/ui` primitives for styling
- Include at least 3 links:
  - Home (`/`)
  - Reports (`/reports`)
  - About (`/about`)
- Render the component at the top of every page (use `layout.tsx`)
- The active page should be visually indicated (e.g. underline, color)
- Responsive design: collapse into a menu or stack vertically on mobile

## 🔧 Hints
- You may use `usePathname()` from `next/navigation` to determine the current route
- Consider whether this component should live in `@ui` and be promoted later
- Routes may not be implemented yet — use `href="#"` if needed, but leave TODO

## 🧪 Testing

- Add a Playwright integration test:
  - File: `web/apps/controlpanel/tests/integration/navbar.spec.ts`
  - Assert the nav renders and that clicking each link works
  - Test should pass under `pnpm test:e2e`

## 🧼 Acceptance Criteria

- [x] Navbar renders on all pages
- [x] Navigation is accessible and visually consistent
- [x] Component is isolated and reusable
- [x] Tests pass and linting is clean

## 🔗 Related

- EPIC.web.frontend-ui-ux.md
- TASK.ui.02.render-reports-view.md (depends on this)

## ✅ Task Completed
**Changes made**
- Created a new `Navbar.tsx` component in `apps/controlpanel/src/components/`
- Implemented responsive design with mobile hamburger menu
- Added links to Home, Reports, and About pages with active page indication
- Integrated the Navbar into the app layout.tsx
- Created Playwright integration tests to verify functionality
- Added lucide-react package for menu icons

**Outcomes**
- Navbar renders consistently across all pages
- Active page is visually indicated with styling
- Mobile view collapses into a hamburger menu
- All Navbar tests pass successfully
- Build and lint commands run without errors related to the Navbar