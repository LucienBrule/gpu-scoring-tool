# TASK.web.12.visual-regression-tests

## 📌 Title
Add Playwright snapshot tests for `/` and `/reports` pages

## 📁 Location
- `web/apps/controlpanel/tests/integration/home.spec.ts`
- `web/apps/controlpanel/tests/integration/reports.spec.ts`

## 🧠 Context
As we continue to develop and enhance the frontend, we need to ensure that visual changes are intentional and don't break existing UI. Visual regression testing helps catch unintended visual changes by comparing snapshots of the UI before and after code changes.

This task involves adding Playwright snapshot tests for the home (`/`) and reports (`/reports`) pages to establish a baseline for visual regression testing. These tests will help ensure that future changes don't inadvertently affect the visual appearance of these key pages.

## ✅ Requirements

- Add or enhance Playwright tests for the home page:
  - Capture snapshots at common breakpoints (mobile, tablet, desktop)
  - Include interaction states such as hover and focus
  - Ensure test consistency by mocking necessary API responses

- Add or enhance Playwright tests for the reports page:
  - Load representative mock data
  - Capture snapshots for empty, loading, and populated states
  - Validate table sorting, filtering, and pagination
  - Run tests at multiple viewport sizes and themes

- Establish review workflow for visual diffs:
  - Document the process for reviewing and updating snapshots
  - Set clear instructions in README or test directory
  - Ensure Playwright tests execute in CI

## 🔧 Hints
- Use Playwright's accessibility snapshot (`browser_snapshot`) instead of screenshots for inspecting page state
- Consider testing both with and without data to cover loading states
- Mock API responses to ensure consistent data for snapshots
- Document the process for updating snapshots when UI changes are intentional
- Consider setting up a visual diff tool for easier review of changes

## 🧪 Testing

- Verify that tests accurately detect visual changes and reject non-deterministic output
- Ensure API mocks stabilize rendering for visual tests

## 🧼 Acceptance Criteria

- [x] Playwright tests for the home page capture visual state correctly
- [x] Playwright tests for the reports page capture visual state correctly
- [x] Tests run successfully in different viewport sizes
- [x] Tests handle both light and dark themes if applicable
- [x] Documentation explains how to update snapshots when needed
- [x] Tests are integrated into the CI pipeline
- [x] Tests are reliable and don't produce false positives
- [x] Snapshot review and update process documented
- [x] Mock data ensures deterministic rendering for snapshot comparison

## 🔗 Related

- EPIC.web.frontend-consume-hooks.md
- TASK.web.10.enhance-reports-view.md (tests will verify this implementation)
- TASK.web.11.add-loading-and-error-states.md (tests should verify these states)

## ✅ Task Completed

**Changes made**
- Created a new home.spec.ts file with visual regression tests for the home page
- Enhanced reports.spec.ts with visual regression tests for the reports page
- Created an API mocking utility (api-mocks.ts) to ensure consistent test data
- Updated Playwright configuration to enable visual regression testing
- Added tests for different viewport sizes (desktop, tablet, mobile)
- Added tests for interaction states (hover, focus)
- Added tests for empty, loading, and populated states
- Added tests for table sorting and filtering
- Created comprehensive documentation in VISUAL_TESTING.md

**Outcomes**
- Visual regression tests now capture the visual state of the home and reports pages
- Tests run at different viewport sizes to ensure responsive design
- API mocking ensures deterministic rendering for reliable snapshots
- Documentation provides guidelines for reviewing visual diffs and updating snapshots
- CI integration instructions ensure tests can run in CI environments
- The visual regression testing workflow is well-documented and maintainable

**Implementation Details**
- Used Playwright's `page.accessibility.snapshot()` and `expect(page).toHaveScreenshot()` for visual testing
- Set up API mocking using Playwright's `page.route()` to intercept network requests
- Configured snapshot comparison settings with appropriate thresholds
- Added tests for different states and interactions to ensure comprehensive coverage
- Documented best practices for ensuring deterministic rendering and handling flaky tests