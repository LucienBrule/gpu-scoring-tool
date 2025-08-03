import { Page } from '@playwright/test';

/**
 * Mock data for health check endpoint
 */
export const mockHealthCheck = {
  status: 'ok',
};

/**
 * Mock data for GPU models
 */
export const mockModels = [
  {
    model: 'NVIDIA RTX 4090',
    listingCount: 120,
    minPrice: 1499.99,
    medianPrice: 1599.99,
    maxPrice: 1799.99,
    avgPrice: 1649.99,
    vramGb: 24,
    tdpWatts: 450,
    migSupport: 0,
    nvlink: true,
    generation: '40 Series',
    cudaCores: 16384,
    slotWidth: 3,
    pcieGeneration: 4,
  },
  {
    model: 'NVIDIA RTX 4080',
    listingCount: 95,
    minPrice: 1099.99,
    medianPrice: 1199.99,
    maxPrice: 1299.99,
    avgPrice: 1189.99,
    vramGb: 16,
    tdpWatts: 320,
    migSupport: 0,
    nvlink: true,
    generation: '40 Series',
    cudaCores: 9728,
    slotWidth: 3,
    pcieGeneration: 4,
  },
  {
    model: 'AMD Radeon RX 7900 XTX',
    listingCount: 80,
    minPrice: 999.99,
    medianPrice: 1049.99,
    maxPrice: 1149.99,
    avgPrice: 1059.99,
    vramGb: 24,
    tdpWatts: 355,
    migSupport: null,
    nvlink: false,
    generation: 'RDNA 3',
    cudaCores: null,
    slotWidth: 2.5,
    pcieGeneration: 4,
  },
];

/**
 * Mock data for GPU listings/reports
 */
export const mockListings = [
  {
    canonicalModel: 'NVIDIA RTX 4090',
    vramGb: 24,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 450,
    price: 1599.99,
    score: 9.2,
    importId: null,
    importIndex: null,
  },
  {
    canonicalModel: 'NVIDIA RTX 3080',
    vramGb: 10,
    migSupport: 0,
    nvlink: false,
    tdpWatts: 320,
    price: 699.99,
    score: 8.5,
    importId: null,
    importIndex: null,
  },
  {
    canonicalModel: 'AMD Radeon RX 6900 XT',
    vramGb: 16,
    migSupport: 0,
    nvlink: false,
    tdpWatts: 300,
    price: 999.99,
    score: 7.8,
    importId: null,
    importIndex: null,
  },
  {
    canonicalModel: 'NVIDIA RTX A6000',
    vramGb: 48,
    migSupport: 7,
    nvlink: true,
    tdpWatts: 300,
    price: 4999.99,
    score: 6.5,
    importId: null,
    importIndex: null,
  },
  {
    canonicalModel: 'NVIDIA RTX 3060',
    vramGb: 12,
    migSupport: 0,
    nvlink: false,
    tdpWatts: 170,
    price: 329.99,
    score: 7.2,
    importId: null,
    importIndex: null,
  },
];

/**
 * Mock data for empty listings/reports
 */
export const mockEmptyListings: typeof mockListings = [];

/**
 * Sets up API mocking for health check endpoint
 * @param page - Playwright Page object
 */
export async function mockHealthCheckEndpoint(page: Page): Promise<void> {
  await page.route('**/api/health**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockHealthCheck),
    });
  });
}

/**
 * Sets up API mocking for models endpoint
 * @param page - Playwright Page object
 */
export async function mockModelsEndpoint(page: Page): Promise<void> {
  await page.route('**/api/models**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockModels),
    });
  });
}

/**
 * Sets up API mocking for listings/reports endpoint
 * @param page - Playwright Page object
 * @param isEmpty - Whether to return empty data
 */
export async function mockListingsEndpoint(page: Page, isEmpty = false): Promise<void> {
  await page.route('**/api/listings**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(isEmpty ? mockEmptyListings : mockListings),
    });
  });
}

/**
 * Sets up API mocking for all endpoints
 * @param page - Playwright Page object
 * @param options - Configuration options
 */
export async function setupApiMocks(
  page: Page,
  options: {
    mockHealth?: boolean;
    mockModels?: boolean;
    mockListings?: boolean;
    emptyListings?: boolean;
  } = {}
): Promise<void> {
  const { mockHealth = true, mockModels = true, mockListings = true, emptyListings = false } = options;

  if (mockHealth) {
    await mockHealthCheckEndpoint(page);
  }

  if (mockModels) {
    await mockModelsEndpoint(page);
  }

  if (mockListings) {
    await mockListingsEndpoint(page, emptyListings);
  }
}