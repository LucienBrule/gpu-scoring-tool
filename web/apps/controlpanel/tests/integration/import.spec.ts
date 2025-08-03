import { test, expect } from '@playwright/test';

test.describe('Import Tools Page', () => {
  test('should navigate to Import Tools page from navbar', async ({ page }) => {
    // Start from the homepage
    await page.goto('/');
    
    // Click on the Import link in the navbar
    await page.click('nav a[href="/import"]');
    
    // Verify we're on the Import page
    await expect(page).toHaveURL('/import');
    
    // Check that the page title is displayed
    await expect(page.locator('h1')).toHaveText('Import Tools');
  });

  test('should display three tabs for different import methods', async ({ page }) => {
    // Go directly to the Import page
    await page.goto('/import');
    
    // Check that all three tabs are present
    await expect(page.locator('button[value="csv"]')).toBeVisible();
    await expect(page.locator('button[value="pipeline"]')).toBeVisible();
    await expect(page.locator('button[value="validate"]')).toBeVisible();
    
    // Verify the default tab is CSV Import
    await expect(page.locator('button[value="csv"][data-state="active"]')).toBeVisible();
  });

  test('should switch between tabs correctly', async ({ page }) => {
    // Go to the Import page
    await page.goto('/import');
    
    // Click on the Pipeline Import tab
    await page.click('button[value="pipeline"]');
    
    // Verify the Pipeline Import tab is active
    await expect(page.locator('button[value="pipeline"][data-state="active"]')).toBeVisible();
    
    // Verify the Pipeline Import content is visible
    await expect(page.locator('h2:has-text("Pipeline Import")')).toBeVisible();
    
    // Click on the Artifact Validation tab
    await page.click('button[value="validate"]');
    
    // Verify the Artifact Validation tab is active
    await expect(page.locator('button[value="validate"][data-state="active"]')).toBeVisible();
    
    // Verify the Artifact Validation content is visible
    await expect(page.locator('h2:has-text("Artifact Validation")')).toBeVisible();
    
    // Go back to the CSV Import tab
    await page.click('button[value="csv"]');
    
    // Verify the CSV Import tab is active
    await expect(page.locator('button[value="csv"][data-state="active"]')).toBeVisible();
    
    // Verify the CSV Import content is visible
    await expect(page.locator('h2:has-text("CSV Import")')).toBeVisible();
  });

  test('should show file upload area in CSV Import tab', async ({ page }) => {
    // Go to the Import page
    await page.goto('/import');
    
    // Verify the file upload area is visible
    await expect(page.locator('div:has-text("Drag and drop a CSV file here")')).toBeVisible();
    
    // Verify the column mapping section is present
    await expect(page.locator('h3:has-text("Column Mapping")')).toBeVisible();
    
    // Verify the import button is present but disabled (no file selected)
    const importButton = page.locator('button:has-text("Import CSV")');
    await expect(importButton).toBeVisible();
    await expect(importButton).toBeDisabled();
  });

  test('should show form fields in Pipeline Import tab', async ({ page }) => {
    // Go to the Import page
    await page.goto('/import');
    
    // Switch to Pipeline Import tab
    await page.click('button[value="pipeline"]');
    
    // Verify the input fields are present
    await expect(page.locator('input#inputCsvPath')).toBeVisible();
    await expect(page.locator('input#sourceLabel')).toBeVisible();
    await expect(page.locator('input#campaignId')).toBeVisible();
    
    // Verify the import button is present
    await expect(page.locator('button:has-text("Import from Pipeline")')).toBeVisible();
  });

  test('should show file upload and options in Artifact Validation tab', async ({ page }) => {
    // Go to the Import page
    await page.goto('/import');
    
    // Switch to Artifact Validation tab
    await page.click('button[value="validate"]');
    
    // Verify the file upload area is visible
    await expect(page.locator('div:has-text("Drag and drop a file here")')).toBeVisible();
    
    // Verify the schema version selector is present
    await expect(page.locator('label:has-text("Schema Version")')).toBeVisible();
    
    // Verify the validation level selector is present
    await expect(page.locator('label:has-text("Validation Level")')).toBeVisible();
    
    // Verify the save to disk checkbox is present
    await expect(page.locator('label:has-text("Save artifact to disk")')).toBeVisible();
    
    // Verify the validate button is present but disabled (no file selected)
    const validateButton = page.locator('button:has-text("Validate Artifact")');
    await expect(validateButton).toBeVisible();
    await expect(validateButton).toBeDisabled();
  });
});