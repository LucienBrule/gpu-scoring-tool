// Custom client wrapper that provides a stable interface
// independent of the generated code structure
import { HealthApi, ListingsApi, Configuration } from '@repo/client-generated';
import type { GPUListingDTO } from '@repo/client-generated';

export class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;
  private healthApi: HealthApi;
  private listingsApi: ListingsApi;

  constructor(baseUrl: string, defaultHeaders: Record<string, string> = {}) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = defaultHeaders;

    const config = new Configuration({
      basePath: baseUrl,
      headers: defaultHeaders,
    });

    this.healthApi = new HealthApi(config);
    this.listingsApi = new ListingsApi(config);
  }

  // Add your custom client methods here
  // These will wrap the generated client to provide a stable API
  async getHealth() {
    return this.healthApi.healthCheckApiHealthGet();
  }

  // Get reports (using listings as a substitute)
  async getReports(filters?: {
    model?: string;
    minPrice?: number;
    maxPrice?: number;
    limit?: number;
    offset?: number;
  }) {
    return this.listingsApi.getListingsApiListingsGet({
      model: filters?.model,
      minPrice: filters?.minPrice,
      maxPrice: filters?.maxPrice,
      limit: filters?.limit,
      offset: filters?.offset,
    });
  }
}

// Re-export specific generated types/functions with aliases if needed
// This gives you control over what gets exposed and how
export const getHealth = async (baseUrl: string = '') => {
  const client = new ApiClient(baseUrl);
  return client.getHealth();
};

// Get reports (using listings as a substitute)
export const getReports = async (
  filters?: {
    model?: string;
    minPrice?: number;
    maxPrice?: number;
    limit?: number;
    offset?: number;
  },
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.getReports(filters);
};

// Re-export the GPUListingDTO type as GpuReportRow for consistency with the task
export type GpuReportRow = GPUListingDTO;
