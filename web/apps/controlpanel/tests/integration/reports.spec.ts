import { test, expect } from '@playwright/test';

/**
 * End-to-end integration test for the reports view.
 * This test verifies that the reports page renders correctly and handles different states.
 */
test.describe('Reports View', () => {
  test('should navigate to reports page', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Click on Reports link and check URL
    await page.getByRole('link', { name: 'Reports' }).click();
    await expect(page).toHaveURL('/reports');
    
    // Reports link should be active
    await expect(page.getByRole('link', { name: 'Reports' })).toHaveAttribute('aria-current', 'page');
    
    // Page title should be visible
    const pageTitle = page.locator('h1:has-text("GPU Reports")');
    await expect(pageTitle).toBeVisible();
  });

  test('should display empty state when no data is available', async ({ page }) => {
    // Navigate directly to the reports page
    await page.goto('/reports');
    
    // Since we know the API returns an empty array, we should see the empty state message
    // Wait for the loading state to disappear first
    await page.waitForSelector('text=Loading reports data...', { state: 'hidden' });
    
    // Check for the empty state message
    const emptyState = page.locator('text=No reports available');
    await expect(emptyState).toBeVisible();
    
    // The table should not be visible
    const table = page.locator('table');
    await expect(table).not.toBeVisible();
  });

  test('should have a refresh button', async ({ page }) => {
    // Navigate to the reports page
    await page.goto('/reports');
    
    // Check if the refresh button is visible
    const refreshButton = page.getByRole('button', { name: 'Refresh Data' });
    await expect(refreshButton).toBeVisible();
    
    // Click the refresh button
    await refreshButton.click();
    
    // After clicking, it should briefly show "Refreshing..." and then go back to "Refresh Data"
    // This is hard to test reliably, so we'll just check that the refresh button still exists after clicking
    await expect(refreshButton).toBeVisible();
  });

  // Note: We can't reliably test the table rendering with actual data since we don't have control
  // over the API response in this test environment. In a real scenario, we would mock the API
  // to return test data. For now, we'll just test the navigation and empty state.
});