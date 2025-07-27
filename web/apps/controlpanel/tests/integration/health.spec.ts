import { test, expect } from '@playwright/test';

/**
 * End-to-end integration test for the health check endpoint
 * This test verifies that the backend API is accessible and returns the expected response.
 */
test.describe('Health Check Integration', () => {
  test('should get health status directly from API', async () => {
    // Make a direct request to the backend API
    const response = await fetch('http://127.0.0.1:8002/api/health');

    // Verify the response status
    expect(response.status).toBe(200);

    // Verify the response body
    const data = await response.json();
    expect(data).toHaveProperty('status', 'ok');

    console.log('[DEBUG_LOG] Health check API response:', data);
  });

  test('should handle API errors gracefully with direct fetch', async () => {
    // Make a request to a non-existent endpoint to simulate an error
    const response = await fetch('http://127.0.0.1:8002/api/non-existent');

    // Verify the response status is an error
    expect(response.status).toBe(404);

    console.log('[DEBUG_LOG] Error response status:', response.status);
  });
});
