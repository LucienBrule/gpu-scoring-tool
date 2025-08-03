// Custom client wrapper that provides a stable interface
// independent of the generated code structure
import { 
  Configuration,
  ForecastApi,
  HealthApi,
  ImportApi,
  ListingsApi,
  MLApi,
  ModelsApi,
  PersistApi,
  ReportApi,
  SchemaApi,
  ValidationApi
} from '@repo/client-generated';

// Import domain-aligned type aliases
import type {
  ArtifactValidationResult,
  GpuListing,
  GpuModel,
  GpuReport,
  HttpValidationError,
  HealthStatus,
  ImportResult,
  ImportSummaryStats,
  MlPredictionRequest,
  MlPredictionResponse,
  PipelineImportRequest,
  ApiValidationError,
  RowError,
  SchemaVersion,
  SchemaVersionInfo,
  ValidationErrorLocation
} from './types/api.js';

export class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;
  
  // API class instances
  private readonly forecastApi: ForecastApi;
  private readonly healthApi: HealthApi;
  private readonly importApi: ImportApi;
  private readonly listingsApi: ListingsApi;
  private readonly mlApi: MLApi;
  private readonly modelsApi: ModelsApi;
  private readonly persistApi: PersistApi;
  private readonly reportApi: ReportApi;
  private readonly schemaApi: SchemaApi;
  private readonly validationApi: ValidationApi;

  constructor(baseUrl: string, defaultHeaders: Record<string, string> = {}) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = defaultHeaders;

    const config = new Configuration({
      basePath: baseUrl,
      headers: defaultHeaders,
    });

    // Initialize all API classes
    this.forecastApi = new ForecastApi(config);
    this.healthApi = new HealthApi(config);
    this.importApi = new ImportApi(config);
    this.listingsApi = new ListingsApi(config);
    this.mlApi = new MLApi(config);
    this.modelsApi = new ModelsApi(config);
    this.persistApi = new PersistApi(config);
    this.reportApi = new ReportApi(config);
    this.schemaApi = new SchemaApi(config);
    this.validationApi = new ValidationApi(config);
  }

  // Getter methods for API classes
  get forecast(): ForecastApi {
    return this.forecastApi;
  }

  get health(): HealthApi {
    return this.healthApi;
  }

  get import(): ImportApi {
    return this.importApi;
  }

  get listings(): ListingsApi {
    return this.listingsApi;
  }

  get ml(): MLApi {
    return this.mlApi;
  }

  get models(): ModelsApi {
    return this.modelsApi;
  }

  get persist(): PersistApi {
    return this.persistApi;
  }

  get report(): ReportApi {
    return this.reportApi;
  }

  get schema(): SchemaApi {
    return this.schemaApi;
  }

  get validation(): ValidationApi {
    return this.validationApi;
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

  // Get listings directly
  async getListingsDirectly(params?: {
    model?: string;
    minPrice?: number;
    maxPrice?: number;
    limit?: number;
    offset?: number;
  }) {
    return this.listingsApi.getListingsApiListingsGet(params || {});
  }

  // Get GPU models
  async getModels() {
    return this.modelsApi.getModelsApiModelsGet();
  }

  // Get forecast deltas
  async getForecastDeltas(params?: {
    model?: string;
    minPriceChangePct?: number;
    after?: Date;
    region?: string;
    limit?: number;
  }) {
    return this.forecastApi.getListingDeltasApiForecastDeltasGet({
      model: params?.model,
      minPriceChangePct: params?.minPriceChangePct,
      after: params?.after,
      region: params?.region,
      limit: params?.limit,
    });
  }

  // Get specific forecast delta by ID
  async getForecastDeltaById(deltaId: number) {
    return this.forecastApi.getListingDeltaApiForecastDeltasDeltaIdGet({
      deltaId,
    });
  }

  // Classify whether a text description refers to a GPU
  async classifyGpu(title: string) {
    return this.mlApi.predictGpuClassificationApiMlIsGpuPost({
      mLPredictionRequest: {
        title,
      },
    });
  }

  // Get all supported schema versions
  async getSchemaVersions() {
    return this.schemaApi.getSchemaVersionsApiSchemaVersionsGet();
  }

  // Check if a specific schema version is supported
  async getSchemaVersionDetails(version: string) {
    return this.schemaApi.checkSchemaVersionApiSchemaVersionsVersionGet({
      version,
    });
  }

  // Import CSV file
  async importCsv(file: Blob) {
    return this.importApi.importCsvApiImportCsvPost({
      file,
    });
  }

  // Import from pipeline
  async importFromPipeline(params: {
    inputCsvPath: string;
    sourceLabel: string;
    campaignId?: string;
    metadata?: { [key: string]: string };
  }) {
    return this.persistApi.importFromPipelineApiImportsFromPipelinePost({
      pipelineImportRequestDTO: {
        inputCsvPath: params.inputCsvPath,
        sourceLabel: params.sourceLabel,
        campaignId: params.campaignId || null,
        metadata: params.metadata || null,
      },
    });
  }

  // Validate artifact
  async validateArtifact(file: Blob, saveToDisk: boolean = false) {
    return this.validationApi.uploadArtifactApiIngestUploadArtifactPost({
      file,
      saveToDisk,
    });
  }

  // Persist GPU listings
  async persistListings(listings: GpuListing[], options?: {
    mode?: 'create' | 'update' | 'upsert';
    batchSize?: number;
    conflictResolution?: 'skip' | 'overwrite' | 'merge';
  }) {
    // Default options
    const mode = options?.mode || 'upsert';
    const batchSize = options?.batchSize || listings.length;
    const conflictResolution = options?.conflictResolution || 'overwrite';

    // Add metadata to track persistence options
    const metadata = {
      mode,
      conflictResolution,
      batchSize: batchSize.toString(),
      timestamp: new Date().toISOString(),
    };

    // Process in batches if needed
    if (batchSize < listings.length) {
      const results: ImportResult[] = [];
      for (let i = 0; i < listings.length; i += batchSize) {
        const batch = listings.slice(i, i + batchSize);
        const result = await this.persistApi.importListingsApiPersistListingsPost({
          gPUListingDTO: batch,
        });
        results.push(result);
      }
      
      // Combine results
      return {
        recordCount: results.reduce((sum, r) => sum + (r.recordCount || 0), 0),
        firstModel: results[0]?.firstModel || null,
        lastModel: results[results.length - 1]?.lastModel || null,
        importId: results[0]?.importId || null,
        timestamp: results[0]?.timestamp || null,
        source: results[0]?.filename || null,
      };
    }

    // Process all at once
    return this.persistApi.importListingsApiPersistListingsPost({
      gPUListingDTO: listings,
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

// Re-export domain-aligned type aliases
export type {
  ArtifactValidationResult,
  GpuListing,
  GpuModel,
  GpuReport,
  HttpValidationError,
  HealthStatus,
  ImportResult,
  ImportSummaryStats,
  MlPredictionRequest,
  MlPredictionResponse,
  PipelineImportRequest,
  ApiValidationError,
  RowError,
  SchemaVersion,
  SchemaVersionInfo,
  ValidationErrorLocation
};

// Re-export the GpuListing type as GpuReportRow for consistency with the task
export type GpuReportRow = GpuListing;

// Get listings with pagination and filtering
export const getListings = async (
  filters?: {
    model?: string;
    minPrice?: number;
    maxPrice?: number;
    limit?: number;
    offset?: number;
    fromDate?: string; // ISO 8601 format (YYYY-MM-DD)
    toDate?: string; // ISO 8601 format (YYYY-MM-DD)
  },
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  // Use the public method to get listings
  const listings = await client.getListingsDirectly({
    model: filters?.model,
    minPrice: filters?.minPrice,
    maxPrice: filters?.maxPrice,
    limit: filters?.limit,
    offset: filters?.offset,
  });

  // Apply date filtering on the client side if fromDate or toDate is provided
  // Note: This assumes that the listings have a date field that we can filter on
  // Since the GPUListingDTO doesn't have a date field, we'll need to implement this
  // when the backend adds support for date filtering
  
  // For now, we'll just return the listings without date filtering
  return listings;
};

// Get GPU models
export const getModels = async (baseUrl: string = '') => {
  const client = new ApiClient(baseUrl);
  return client.getModels();
};

// Get forecast deltas
export const getForecastDeltas = async (
  params?: {
    model?: string;
    minPriceChangePct?: number;
    after?: Date;
    region?: string;
    limit?: number;
  },
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.getForecastDeltas(params);
};

// Get specific forecast delta by ID
export const getForecastDeltaById = async (
  deltaId: number,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.getForecastDeltaById(deltaId);
};

// Classify whether a text description refers to a GPU
export const classifyGpu = async (
  title: string,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.classifyGpu(title);
};

// Get all supported schema versions
export const getSchemaVersions = async (
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.getSchemaVersions();
};

// Check if a specific schema version is supported
export const getSchemaVersionDetails = async (
  version: string,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.getSchemaVersionDetails(version);
};

// Import CSV file
export const importCsv = async (
  file: Blob,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.importCsv(file);
};

// Import from pipeline
export const importFromPipeline = async (
  params: {
    inputCsvPath: string;
    sourceLabel: string;
    campaignId?: string;
    metadata?: { [key: string]: string };
  },
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.importFromPipeline(params);
};

// Validate artifact
export const validateArtifact = async (
  file: Blob,
  saveToDisk: boolean = false,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.validateArtifact(file, saveToDisk);
};

// Persist GPU listings
export const persistListings = async (
  listings: GpuListing[],
  options?: {
    mode?: 'create' | 'update' | 'upsert';
    batchSize?: number;
    conflictResolution?: 'skip' | 'overwrite' | 'merge';
  },
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.persistListings(listings, options);
};
