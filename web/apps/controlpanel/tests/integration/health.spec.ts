import { test, expect } from '@playwright/test';

/**
 * End-to-end integration test for health check rendering.
 * This test verifies that the frontend correctly calls the generated client and renders the response.
 */
test.describe('Health Check Integration', () => {
  test('should render health status from API client', async ({ page }) => {
    await page.goto('http://localhost:3000/integration-test');

    const statusBox = await page.locator('text=Status: ok');
    await expect(statusBox).toBeVisible();
  });
});
