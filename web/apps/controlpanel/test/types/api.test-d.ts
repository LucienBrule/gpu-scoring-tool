/**
 * Type tests for API client methods and DTOs
 * 
 * This file contains type assertions to ensure that API client methods and DTOs
 * are correctly typed. It uses tsd to verify that the types are correct at compile time.
 */

import { expectType, expectAssignable, expectNotAssignable } from 'tsd';
import { 
  ApiClient, 
  getHealth, 
  getListings, 
  getModels,
  getForecastDeltas,
  classifyGpu,
  importCsv,
  importFromPipeline,
  validateArtifact,
  GpuListing,
  GpuModel,
  GpuReport,
  HealthStatus,
  ImportResult,
  MlPredictionResponse,
  ArtifactValidationResult
} from '@repo/client';

// Test ApiClient class methods
{
  const client = new ApiClient('http://localhost:8000');
  
  // Test getHealth method
  expectType<Promise<HealthStatus>>(client.getHealth());
  
  // Test getListings method
  expectType<Promise<GpuListing[]>>(
    client.getListingsDirectly({
      model: 'RTX 3080',
      minPrice: 500,
      maxPrice: 1000,
      limit: 10,
      offset: 0
    })
  );
  
  // Test getModels method
  expectType<Promise<GpuModel[]>>(client.getModels());
  
  // Test getForecastDeltas method
  expectType<Promise<Array<Record<string, unknown>>>>(
    client.getForecastDeltas({
      model: 'RTX 3080',
      minPriceChangePct: 5,
      after: new Date(),
      region: 'US',
      limit: 10
    })
  );
  
  // Test classifyGpu method
  expectType<Promise<MlPredictionResponse>>(
    client.classifyGpu('NVIDIA GeForce RTX 3080 10GB GDDR6X')
  );
  
  // Test importCsv method
  expectType<Promise<ImportResult>>(
    client.importCsv(new Blob(['csv data'], { type: 'text/csv' }))
  );
  
  // Test importFromPipeline method
  expectType<Promise<ImportResult>>(
    client.importFromPipeline({
      inputCsvPath: '/path/to/csv',
      sourceLabel: 'test-source',
      campaignId: 'test-campaign',
      metadata: { key: 'value' }
    })
  );
  
  // Test validateArtifact method
  expectType<Promise<ArtifactValidationResult>>(
    client.validateArtifact(new Blob(['artifact data']), true)
  );
}

// Test standalone utility functions
{
  // Test getHealth function
  expectType<Promise<HealthStatus>>(getHealth());
  
  // Test getListings function
  expectType<Promise<GpuListing[]>>(
    getListings({
      model: 'RTX 3080',
      minPrice: 500,
      maxPrice: 1000,
      limit: 10,
      offset: 0
    })
  );
  
  // Test getModels function
  expectType<Promise<GpuModel[]>>(getModels());
}

// Test DTO type aliases
{
  // Test GpuListing type
  const listing: GpuListing = {
    canonicalModel: 'RTX 3080',
    vramGb: 10,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 320,
    price: 699.99,
    score: 0.85,
    importId: 'import-123',
    importIndex: 1
  };
  expectType<GpuListing>(listing);
  
  // Test GpuModel type
  const model: GpuModel = {
    model: 'RTX 3080',
    listingCount: 100,
    minPrice: 599.99,
    medianPrice: 699.99,
    maxPrice: 799.99,
    avgPrice: 699.99,
    vramGb: 10,
    tdpWatts: 320,
    migSupport: 0,
    nvlink: true,
    generation: 'Ampere',
    cudaCores: 8704,
    slotWidth: 2,
    pcieGeneration: 4
  };
  expectType<GpuModel>(model);
  
  // Test GpuReport type
  const report: GpuReport = {
    markdown: '# GPU Market Report\n\nThis is a report about the GPU market.',
    summaryStats: {
      'totalListings': '1000',
      'averagePrice': '$699.99',
      'priceRange': '$599.99 - $799.99'
    },
    topRanked: ['RTX 3080', 'RTX 3090', 'RTX 3070'],
    scoringWeights: {
      'performance': 0.5,
      'efficiency': 0.3,
      'value': 0.2
    }
  };
  expectType<GpuReport>(report);
  
  // Test HealthStatus type
  const health: HealthStatus = {
    status: 'ok'
  };
  expectType<HealthStatus>(health);
}

// Test type compatibility and constraints
{
  // Test that a string is not assignable to GpuListing
  expectNotAssignable<GpuListing>('not a listing');
  
  // Test that a partial GpuListing is not assignable to GpuListing
  expectNotAssignable<GpuListing>({ canonicalModel: 'RTX 3080', price: 699.99 });
  
  // Test that a GpuListing is assignable to a type with a subset of its properties
  type PartialGpuListing = Pick<GpuListing, 'canonicalModel' | 'price' | 'score'>;
  const fullListing: GpuListing = {
    canonicalModel: 'RTX 3080',
    vramGb: 10,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 320,
    price: 699.99,
    score: 0.85
  };
  expectAssignable<PartialGpuListing>(fullListing);
}