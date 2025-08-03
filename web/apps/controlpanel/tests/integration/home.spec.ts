import { test, expect } from '@playwright/test';
import { setupApiMocks } from '../utils/api-mocks';

/**
 * Visual regression tests for the home page.
 * These tests capture snapshots of the home page in different states and viewport sizes.
 */
test.describe('Home Page Visual Tests', () => {
  // Set up API mocking before each test
  test.beforeEach(async ({ page }) => {
    await setupApiMocks(page);
  });

  test('should render home page correctly', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Skip accessibility snapshot for now due to compatibility issues
    // const snapshot = await page.accessibility.snapshot();
    // expect(snapshot).toMatchSnapshot('home-page-accessibility.json');
    
    // Capture visual snapshot of the entire page
    await expect(page).toHaveScreenshot('home-page.png');
  });

  test('should render home page with hover states', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Hover over the Reports link in the navbar
    await page.hover('a:has-text("Reports")');
    
    // Capture visual snapshot with hover state
    await expect(page).toHaveScreenshot('home-page-hover-reports.png');
    
    // Hover over the About link in the navbar
    await page.hover('a:has-text("About")');
    
    // Capture visual snapshot with hover state
    await expect(page).toHaveScreenshot('home-page-hover-about.png');
  });

  test('should render home page with focus states', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Focus on the Reports link in the navbar
    await page.focus('a:has-text("Reports")');
    
    // Capture visual snapshot with focus state
    await expect(page).toHaveScreenshot('home-page-focus-reports.png');
    
    // Focus on the About link in the navbar
    await page.focus('a:has-text("About")');
    
    // Capture visual snapshot with focus state
    await expect(page).toHaveScreenshot('home-page-focus-about.png');
  });
});

/**
 * Visual regression tests for the home page at different viewport sizes.
 * These tests capture snapshots of the home page at desktop, tablet, and mobile viewport sizes.
 */
test.describe('Home Page Responsive Visual Tests', () => {
  // Set up API mocking before each test
  test.beforeEach(async ({ page }) => {
    await setupApiMocks(page);
  });

  // Test desktop viewport
  test('should render correctly on desktop', async ({ page }) => {
    // Set viewport to desktop size
    await page.setViewportSize({ width: 1280, height: 800 });
    
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('home-page-desktop.png');
  });

  // Test tablet viewport
  test('should render correctly on tablet', async ({ page }) => {
    // Set viewport to tablet size
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('home-page-tablet.png');
  });

  // Test mobile viewport
  test('should render correctly on mobile', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to the home page
    await page.goto('/');
    
    // Wait for the page to stabilize
    await page.waitForLoadState('networkidle');
    
    // Capture visual snapshot
    await expect(page).toHaveScreenshot('home-page-mobile.png');
    
    // Test mobile menu
    // Click hamburger icon to open mobile menu
    await page.click('button[aria-controls="mobile-menu"]');
    
    // Wait for animation to complete
    await page.waitForTimeout(300);
    
    // Capture visual snapshot with mobile menu open
    await expect(page).toHaveScreenshot('home-page-mobile-menu-open.png');
  });
});