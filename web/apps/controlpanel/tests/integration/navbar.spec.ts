import { test, expect } from '@playwright/test';

test.describe('Navbar', () => {
  test('should render navbar with all links', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Check if navbar is rendered
    const navbar = await page.locator('nav');
    await expect(navbar).toBeVisible();
    
    // Check if all links are present
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Reports' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'About' })).toBeVisible();
  });

  test('should indicate active page', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Check if Home link is marked as active
    const homeLink = page.getByRole('link', { name: 'Home' });
    await expect(homeLink).toHaveAttribute('aria-current', 'page');
    
    // Other links should not be marked as active
    const reportsLink = page.getByRole('link', { name: 'Reports' });
    const aboutLink = page.getByRole('link', { name: 'About' });
    
    await expect(reportsLink).not.toHaveAttribute('aria-current', 'page');
    await expect(aboutLink).not.toHaveAttribute('aria-current', 'page');
  });

  test('should navigate to different pages when links are clicked', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');
    
    // Click on Reports link and check URL
    await page.getByRole('link', { name: 'Reports' }).click();
    await expect(page).toHaveURL('/reports');
    
    // Reports link should now be active
    await expect(page.getByRole('link', { name: 'Reports' })).toHaveAttribute('aria-current', 'page');
    
    // Click on About link and check URL
    await page.getByRole('link', { name: 'About' }).click();
    await expect(page).toHaveURL('/about');
    
    // About link should now be active
    await expect(page.getByRole('link', { name: 'About' })).toHaveAttribute('aria-current', 'page');
    
    // Click on Home link and check URL
    await page.getByRole('link', { name: 'Home' }).click();
    await expect(page).toHaveURL('/');
    
    // Home link should now be active
    await expect(page.getByRole('link', { name: 'Home' })).toHaveAttribute('aria-current', 'page');
  });

  test('should display mobile menu when hamburger icon is clicked', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to the home page
    await page.goto('/');
    
    // Mobile menu should be hidden initially
    const mobileMenu = page.locator('#mobile-menu');
    await expect(mobileMenu).not.toBeVisible();
    
    // Click hamburger icon
    await page.getByRole('button', { name: 'Open main menu' }).click();
    
    // Mobile menu should now be visible
    await expect(mobileMenu).toBeVisible();
    
    // All links should be visible in the mobile menu
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Reports' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'About' })).toBeVisible();
  });
});