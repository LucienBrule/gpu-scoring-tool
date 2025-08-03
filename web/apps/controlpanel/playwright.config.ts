import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:3000';

/**
 * Playwright configuration for the controlpanel app
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',

  // Visual comparison settings
  expect: {
    // Configure snapshot comparison settings
    toHaveScreenshot: {
      // Maximum allowed difference in pixels between screenshots
      maxDiffPixels: 100,
      // Threshold for the difference between pixels to be considered different
      threshold: 0.2,
      // Snapshot style (can be 'css' or 'sha1')
      style: 'css',
    },
    toMatchSnapshot: {
      // Threshold for the difference between snapshots to be considered different
      threshold: 0.2,
    },
  },

  use: {
    baseURL,
    trace: 'on-first-retry',
    // Change to 'on' to capture screenshots for all test steps
    screenshot: 'only-on-failure',
  },

  projects: [
    // Desktop viewports
    {
      name: 'chromium-desktop',
      use: { 
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 800 },
      },
    },
    // Tablet viewport
    {
      name: 'chromium-tablet',
      use: { 
        ...devices['iPad Pro 11'],
      },
    },
    // Mobile viewport
    {
      name: 'chromium-mobile',
      use: { 
        ...devices['iPhone 13'],
      },
    },
  ],

  // Disable webServer since we're using the Docker Compose stack
  // webServer: {
  //   command: 'pnpm dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  //   stdout: 'pipe',
  //   stderr: 'pipe',
  // },
});
