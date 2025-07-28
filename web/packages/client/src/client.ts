// Custom client wrapper that provides a stable interface
// independent of the generated code structure
import { HealthApi, Configuration } from '@repo/client-generated';

export class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;
  private healthApi: HealthApi;

  constructor(baseUrl: string, defaultHeaders: Record<string, string> = {}) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = defaultHeaders;

    const config = new Configuration({
      basePath: baseUrl,
      headers: defaultHeaders,
    });

    this.healthApi = new HealthApi(config);
  }

  // Add your custom client methods here
  // These will wrap the generated client to provide a stable API
  async getHealth() {
    return this.healthApi.healthCheckApiHealthGet();
  }
}

// Re-export specific generated types/functions with aliases if needed
// This gives you control over what gets exposed and how
export const getHealth = async (baseUrl: string = '') => {
  const client = new ApiClient(baseUrl);
  return client.getHealth();
};
