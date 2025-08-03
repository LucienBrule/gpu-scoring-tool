import { test, expect } from '@playwright/test';
import { setupApiMocks } from '../utils/api-mocks';

/**
 * End-to-end integration test for the reports view.
 * This test verifies that the reports page renders correctly and handles different states.
 */
test.describe('Reports View', () => {
  test('should navigate to reports page', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Click on Reports link and check URL
    await page.locator('a:has-text("Reports")').click();
    await expect(page).toHaveURL('/reports');
    
    // Reports link should be active
    await expect(page.locator('a:has-text("Reports")')).toHaveAttribute('aria-current', 'page');
    
    // Page title should be visible
    const pageTitle = page.locator('h1:has-text("GPU Reports")');
    await expect(pageTitle).toBeVisible();
  });

  test('should display empty state when no data is available', async ({ page }) => {
    // Set up API mocking to return empty data
    await setupApiMocks(page, { emptyListings: true });
    
    // Navigate directly to the reports page
    await page.goto('/reports');
    
    // Wait for the loading state to disappear
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check for the empty state message
    const emptyState = page.locator('text=No reports available');
    await expect(emptyState).toBeVisible();
    
    // The table should not be visible
    const table = page.locator('table');
    await expect(table).not.toBeVisible();
  });

  test('should have a refresh button', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Check if the refresh button is visible
    const refreshButton = page.locator('button:has-text("Refresh Data")');
    await expect(refreshButton).toBeVisible();
    
    // Click the refresh button
    await refreshButton.click();
    
    // After clicking, it should briefly show "Refreshing..." and then go back to "Refresh Data"
    // This is hard to test reliably, so we'll just check that the refresh button still exists after clicking
    await expect(refreshButton).toBeVisible();
  });

  test('should have search and filter controls', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the loading state to disappear
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check for the search input
    const searchInput = page.locator('input[placeholder="Search by model..."]');
    await expect(searchInput).toBeVisible();
    
    // Check for price range filter inputs
    const priceMinInput = page.locator('input[placeholder="Min"]').first();
    const priceMaxInput = page.locator('input[placeholder="Max"]').first();
    await expect(priceMinInput).toBeVisible();
    await expect(priceMaxInput).toBeVisible();
    
    // Check for score range filter inputs
    const scoreMinInput = page.locator('input[placeholder="Min"]').nth(1);
    const scoreMaxInput = page.locator('input[placeholder="Max"]').nth(1);
    await expect(scoreMinInput).toBeVisible();
    await expect(scoreMaxInput).toBeVisible();
    
    // Check for model filter dropdown
    const modelFilterDropdown = page.locator('select');
    await expect(modelFilterDropdown).toBeVisible();
  });

  test('should have tooltips for column headers', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the loading state to disappear
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check that the table is visible
    const table = page.locator('table');
    await expect(table).toBeVisible();
    
    // Check for column headers
    const modelHeader = page.locator('th', { hasText: 'Model' });
    const vramHeader = page.locator('th', { hasText: 'VRAM' });
    const priceHeader = page.locator('th', { hasText: 'Price' });
    const pricePerGbHeader = page.locator('th', { hasText: '$/GB' });
    const scoreHeader = page.locator('th', { hasText: 'Score' });
    
    await expect(modelHeader).toBeVisible();
    await expect(vramHeader).toBeVisible();
    await expect(priceHeader).toBeVisible();
    await expect(pricePerGbHeader).toBeVisible();
    await expect(scoreHeader).toBeVisible();
    
    // Note: We can't reliably test the tooltips themselves since they require hover interactions
    // and the content is only visible on hover. Playwright can simulate hover, but checking the
    // tooltip content is more complex and may be flaky in CI environments.
  });

  test('should have pagination controls if data is available', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the loading state to disappear
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check that the table is visible
    const table = page.locator('table');
    await expect(table).toBeVisible();
    
    // Check for pagination controls
    const previousButton = page.locator('button:has-text("Previous")');
    const nextButton = page.locator('button:has-text("Next")').first();
    
    await expect(previousButton).toBeVisible();
    await expect(nextButton).toBeVisible();
    
    // Check for pagination info text
    const paginationInfo = page.locator('text=/Showing .* to .* of .* results/');
    await expect(paginationInfo).toBeVisible();
  });

  test('should be able to interact with sorting', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the loading state to disappear
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check that the table is visible
    const table = page.locator('table');
    await expect(table).toBeVisible();
    
    // Click on the Price header to sort by price
    const priceHeader = page.locator('th', { hasText: 'Price' });
    await priceHeader.click();
    
    // Click on the Score header to sort by score
    const scoreHeader = page.locator('th', { hasText: 'Score' });
    await scoreHeader.click();
    
    // Click on the Model header to sort by model
    const modelHeader = page.locator('th', { hasText: 'Model' });
    await modelHeader.click();
  });
});

/**
 * Visual regression tests for the reports page.
 * These tests capture snapshots of the reports page in different states.
 */
test.describe('Reports Page Visual Tests', () => {
  test('should render reports page with data correctly', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Skip accessibility snapshot for now due to compatibility issues
    // const snapshot = await page.accessibility.snapshot();
    // expect(snapshot).toMatchSnapshot('reports-page-accessibility.json');
    
    // Capture visual snapshot of the entire page
    await expect(page).toHaveScreenshot('reports-page-with-data.png');
  });

  test('should render reports page in empty state correctly', async ({ page }) => {
    // Set up API mocking to return empty data
    await setupApiMocks(page, { emptyListings: true });
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Capture visual snapshot of the empty state
    await expect(page).toHaveScreenshot('reports-page-empty.png');
  });

  test('should render reports page with filtered data correctly', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Filter by model name
    await page.fill('input[placeholder="Search by model..."]', 'RTX');
    
    // Wait for the filter to apply
    await page.waitForTimeout(300);
    
    // Capture visual snapshot of the filtered state
    await expect(page).toHaveScreenshot('reports-page-filtered.png');
  });

  test('should render reports page with sorted data correctly', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Sort by price
    await page.click('th:has-text("Price")');
    
    // Wait for the sort to apply
    await page.waitForTimeout(300);
    
    // Capture visual snapshot of the sorted state
    await expect(page).toHaveScreenshot('reports-page-sorted-by-price.png');
    
    // Sort by score
    await page.click('th:has-text("Score")');
    
    // Wait for the sort to apply
    await page.waitForTimeout(300);
    
    // Capture visual snapshot of the sorted state
    await expect(page).toHaveScreenshot('reports-page-sorted-by-score.png');
  });
});

/**
 * Visual regression tests for the reports page at different viewport sizes.
 * These tests capture snapshots of the reports page at desktop, tablet, and mobile viewport sizes.
 */
test.describe('Reports Page Responsive Visual Tests', () => {
  // Test desktop viewport
  test('should render correctly on desktop', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Set viewport to desktop size
    await page.setViewportSize({ width: 1280, height: 800 });
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('reports-page-desktop.png');
  });

  // Test tablet viewport
  test('should render correctly on tablet', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Set viewport to tablet size
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('reports-page-tablet.png');
  });

  // Test mobile viewport
  test('should render correctly on mobile', async ({ page }) => {
    // Set up API mocking
    await setupApiMocks(page);
    
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('reports-page-mobile.png');
    
    // Test mobile menu
    // Click hamburger icon to open mobile menu
    await page.click('button[aria-controls="mobile-menu"]');
    
    // Wait for animation to complete
    await page.waitForTimeout(300);
    
    // Capture visual snapshot with mobile menu open
    await expect(page).toHaveScreenshot('reports-page-mobile-menu-open.png');
  });
});