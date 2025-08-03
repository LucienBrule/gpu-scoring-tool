# Visual Regression Testing Guide

This document provides guidelines for working with visual regression tests in the GPU Scoring Tool frontend.

## Overview

Visual regression testing helps catch unintended visual changes by comparing snapshots of the UI before and after code changes. We use Playwright's snapshot testing capabilities to capture and compare visual states of our application.

## Types of Visual Tests

We use two main types of visual tests:

1. **Screenshot Comparisons** - Using `expect(page).toHaveScreenshot()` to capture and compare full-page or element screenshots.
2. **Accessibility Snapshots** - Using `page.accessibility.snapshot()` and `expect(snapshot).toMatchSnapshot()` to capture and compare the accessibility tree of the page.

## Test Organization

Visual tests are organized in the following structure:

- `tests/integration/home.spec.ts` - Visual tests for the home page
- `tests/integration/reports.spec.ts` - Visual tests for the reports page
- `tests/utils/api-mocks.ts` - Utilities for mocking API responses to ensure consistent test data

Each test file contains multiple test suites:
- Basic functional tests
- Visual tests for different states (empty, loading, populated)
- Responsive visual tests for different viewport sizes

## Running Visual Tests

To run the visual tests:

```bash
# Run all tests
pnpm test:e2e --filter controlpanel

# Run only visual tests for a specific page
pnpm test:e2e --filter controlpanel -g "Home Page Visual Tests"
pnpm test:e2e --filter controlpanel -g "Reports Page Visual Tests"

# Run only responsive visual tests
pnpm test:e2e --filter controlpanel -g "Responsive Visual Tests"
```

## Reviewing Visual Diffs

When a visual test fails, Playwright will generate a diff image showing the differences between the expected and actual screenshots. These diffs are stored in the `test-results` directory.

To review visual diffs:

1. Run the tests and note any failures
2. Open the test report: `npx playwright show-report`
3. Click on the failed test to see the diff image
4. Review the diff to determine if the changes are intentional or not

## Updating Snapshots

When you make intentional changes to the UI, you'll need to update the snapshots to reflect the new expected state.

To update snapshots:

```bash
# Update all snapshots
pnpm test:e2e --filter controlpanel --update-snapshots

# Update snapshots for a specific test
pnpm test:e2e --filter controlpanel -g "Home Page Visual Tests" --update-snapshots
```

## Best Practices

### 1. Ensure Deterministic Rendering

For reliable visual testing, ensure that the rendering is deterministic:

- Use API mocking to provide consistent data
- Disable animations or wait for them to complete
- Set fixed viewport sizes
- Wait for the page to stabilize before capturing snapshots

Example:
```typescript
// Set up API mocking
await setupApiMocks(page);

// Navigate to the page
await page.goto('/reports');

// Wait for the page to stabilize
await page.waitForLoadState('networkidle');
await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });

// Capture visual snapshot
await expect(page).toHaveScreenshot('reports-page-with-data.png');
```

### 2. Test Different States

Test different states of your components:

- Empty state (no data)
- Loading state
- Error state
- Populated state (with data)
- Interactive states (hover, focus, etc.)

### 3. Test Responsive Design

Test your components at different viewport sizes:

- Desktop (e.g., 1280x800)
- Tablet (e.g., 768x1024)
- Mobile (e.g., 375x667)

### 4. Name Snapshots Clearly

Use descriptive names for your snapshots to make it easier to identify them:

```typescript
await expect(page).toHaveScreenshot('home-page-desktop.png');
await expect(page).toHaveScreenshot('home-page-mobile.png');
await expect(page).toHaveScreenshot('home-page-hover-reports.png');
```

## Troubleshooting

### Flaky Tests

If you encounter flaky tests (tests that sometimes pass and sometimes fail), try the following:

1. Increase the `maxDiffPixels` or `threshold` in the Playwright configuration
2. Add more wait statements to ensure the page is fully rendered
3. Disable animations or transitions that might cause inconsistencies
4. Use more specific selectors to capture smaller parts of the UI

### CI Integration

Visual regression tests can be integrated into your CI pipeline to catch visual regressions automatically. The Playwright configuration already includes CI-specific settings:

```typescript
// playwright.config.ts
export default defineConfig({
  // ...
  forbidOnly: !!process.env.CI,  // Prevents tests marked with .only from running in CI
  retries: process.env.CI ? 2 : 0,  // Retries failed tests twice in CI
  workers: process.env.CI ? 1 : undefined,  // Uses a single worker in CI
  // ...
});
```

#### Setting Up CI Pipeline

To integrate visual regression tests into your CI pipeline:

1. **Install Dependencies**: Ensure your CI environment installs all required dependencies and browsers:

   ```yaml
   # Example GitHub Actions workflow step
   - name: Install dependencies
     run: |
       pnpm install
       npx playwright install --with-deps chromium
   ```

2. **Run Visual Tests**: Execute the visual tests as part of your CI pipeline:

   ```yaml
   # Example GitHub Actions workflow step
   - name: Run visual tests
     run: pnpm test:e2e --filter controlpanel
   ```

3. **Upload Test Results**: Store the test results and snapshots as artifacts:

   ```yaml
   # Example GitHub Actions workflow step
   - name: Upload test results
     if: always()
     uses: actions/upload-artifact@v3
     with:
       name: playwright-report
       path: |
         web/apps/controlpanel/playwright-report/
         web/apps/controlpanel/test-results/
   ```

4. **Update Baseline Snapshots**: When intentional UI changes are made, update the baseline snapshots and commit them to the repository:

   ```bash
   pnpm test:e2e --filter controlpanel --update-snapshots
   git add web/apps/controlpanel/tests/integration/__snapshots__/
   git commit -m "Update visual test snapshots"
   ```

#### Handling Visual Differences in CI

In CI environments, visual tests might behave differently due to different rendering engines or system fonts. To address this:

1. Use the same browser and version in CI as in development
2. Consider using a containerized environment for consistent rendering
3. Adjust thresholds for CI environments if needed:

   ```typescript
   // playwright.config.ts
   export default defineConfig({
     // ...
     expect: {
       toHaveScreenshot: {
         // Increase threshold for CI environments
         maxDiffPixels: process.env.CI ? 200 : 100,
         threshold: process.env.CI ? 0.3 : 0.2,
       },
     },
     // ...
   });
   ```

4. For flaky tests, consider using more specific selectors or capturing smaller parts of the UI

## Further Reading

- [Playwright Visual Comparisons Documentation](https://playwright.dev/docs/test-snapshots)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)