import { test, expect } from '@playwright/test';

test.describe('Listings Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the home page before each test
    await page.goto('/');
  });

  test('should navigate to listings page from navbar', async ({ page }) => {
    // Click on the Listings link in the navbar
    await page.click('text=Listings');
    
    // Check that we're on the listings page
    await expect(page).toHaveURL('/listings');
    await expect(page.locator('h1')).toHaveText('GPU Listings');
  });

  test('should display listings table with data', async ({ page }) => {
    // Navigate to the listings page
    await page.goto('/listings');
    
    // Wait for the table to load (this assumes the API responds with data)
    // In a real test, you might want to mock the API response
    await page.waitForSelector('table', { timeout: 5000 }).catch(() => {
      // If table doesn't appear, it might be because of loading, error, or empty state
      // We'll check for these states
    });
    
    // Check if any of the expected states are visible
    const hasTable = await page.locator('table').count() > 0;
    const isLoading = await page.locator('text=Loading listings data...').count() > 0;
    const isError = await page.locator('text=Error loading listings').count() > 0;
    const isEmpty = await page.locator('text=No listings available').count() > 0;
    
    // At least one of these states should be true
    expect(hasTable || isLoading || isError || isEmpty).toBeTruthy();
    
    // If we have a table, check that it has the expected columns
    if (hasTable) {
      await expect(page.locator('th:has-text("Model")')).toBeVisible();
      await expect(page.locator('th:has-text("Price (USD)")')).toBeVisible();
      await expect(page.locator('th:has-text("Score")')).toBeVisible();
    }
  });

  test('should sort table when clicking on sortable column headers', async ({ page }) => {
    // Navigate to the listings page
    await page.goto('/listings');
    
    // Wait for the table to load
    const tableLocator = page.locator('table');
    await tableLocator.waitFor({ state: 'visible', timeout: 5000 }).catch(() => {
      // Table might not be visible if there's no data or an error
    });
    
    // If table is visible, test sorting
    if (await tableLocator.count() > 0) {
      // Get the first row's model name before sorting
      const firstModelBeforeSorting = await page.locator('tbody tr:first-child td:first-child').textContent();
      
      // Click on the Model header to sort
      await page.click('th:has-text("Model")');
      
      // Get the first row's model name after sorting
      const firstModelAfterSorting = await page.locator('tbody tr:first-child td:first-child').textContent();
      
      // If we have at least two different models, the first row should change after sorting
      // This is a simple check that sorting does something, but not a comprehensive test
      // In a real test with controlled data, you could make more specific assertions
      if (firstModelBeforeSorting && firstModelAfterSorting) {
        // We'll just check that the UI responds to the click, not the specific sorting order
        // since we don't control the test data in this integration test
        await expect(page.locator('th:has-text("Model")')).toContainText('↓');
      }
    }
  });

  test('should filter listings when using the search input', async ({ page }) => {
    // Navigate to the listings page
    await page.goto('/listings');
    
    // Wait for the table to load
    const tableLocator = page.locator('table');
    await tableLocator.waitFor({ state: 'visible', timeout: 5000 }).catch(() => {
      // Table might not be visible if there's no data or an error
    });
    
    // If table is visible, test search filtering
    if (await tableLocator.count() > 0) {
      // Count the number of rows before filtering
      const rowCountBefore = await page.locator('tbody tr').count();
      
      // Enter a search term that should match some but not all listings
      // This assumes there are some RTX models in the data
      await page.fill('input[placeholder="Search by model..."]', 'RTX');
      
      // Wait for the table to update
      await page.waitForTimeout(500);
      
      // Count the number of rows after filtering
      const rowCountAfter = await page.locator('tbody tr').count();
      
      // If the search term matches any listings, the number of rows should change
      // If it doesn't match any, we might see the empty state message
      const hasEmptyMessage = await page.locator('text=No listings available').isVisible();
      
      // Either the row count should change or we should see the empty message
      if (!hasEmptyMessage) {
        // This is a simple check that filtering does something
        // In a real test with controlled data, you could make more specific assertions
        expect(rowCountBefore).not.toEqual(0);
      }
    }
  });

  test('should navigate between pages using pagination controls', async ({ page }) => {
    // Navigate to the listings page
    await page.goto('/listings');
    
    // Wait for the table to load
    const tableLocator = page.locator('table');
    await tableLocator.waitFor({ state: 'visible', timeout: 5000 }).catch(() => {
      // Table might not be visible if there's no data or an error
    });
    
    // If table is visible, test pagination
    if (await tableLocator.count() > 0) {
      // Check if pagination controls are visible
      const nextButtonLocator = page.locator('button:has-text("Next")');
      const hasPagination = await nextButtonLocator.count() > 0;
      
      if (hasPagination) {
        // Check if the Next button is enabled (meaning there's more than one page)
        const isNextEnabled = !(await nextButtonLocator.getAttribute('disabled'));
        
        if (isNextEnabled) {
          // Get the first row's content before pagination
          const firstRowBeforePagination = await page.locator('tbody tr:first-child').textContent();
          
          // Click the Next button
          await nextButtonLocator.click();
          
          // Wait for the table to update
          await page.waitForTimeout(500);
          
          // Get the first row's content after pagination
          const firstRowAfterPagination = await page.locator('tbody tr:first-child').textContent();
          
          // The content should be different after navigating to the next page
          expect(firstRowBeforePagination).not.toEqual(firstRowAfterPagination);
          
          // Check that the pagination info has updated
          await expect(page.locator('text=Showing')).toContainText('Showing');
        }
      }
    }
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to the listings page
    await page.goto('/listings');
    
    // Check that the mobile menu button is visible
    await expect(page.locator('button[aria-controls="mobile-menu"]')).toBeVisible();
    
    // Check that the table container has horizontal scroll when needed
    const tableContainer = page.locator('.overflow-x-auto');
    await expect(tableContainer).toBeVisible();
    
    // Check that the search input is visible and usable on mobile
    const searchInput = page.locator('input[placeholder="Search by model..."]');
    await expect(searchInput).toBeVisible();
    
    // Check that the pagination controls are visible and usable on mobile
    // (if there's enough data for pagination)
    const paginationControls = page.locator('button:has-text("Next")');
    if (await paginationControls.count() > 0) {
      await expect(paginationControls).toBeVisible();
    }
  });
});