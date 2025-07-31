# Available API Endpoints

This document provides a summary of all consumable backend API endpoints that are available for the frontend. These endpoints can be used to fetch data for visualization or integration in the web UI.

## Criteria for Inclusion

Endpoints listed here meet the following criteria:
- Use `GET` method
- Provide a valid `response_model`
- Are reachable at `/api/`
- Have stable schema (DTO-backed responses)

## Endpoints Summary

| Path | Response DTO | Status | Suggested Hook |
|------|-------------|--------|----------------|
| `/api/health` | `HealthStatus` | ✅ Available | `useHealthCheck()` |
| `/api/listings` | `GPUListingDTO[]` | ✅ Available | `useListings()` |
| `/api/listings/legacy` | `GPUListingDTO[]` | ✅ Available | `useListingsLegacy()` |
| `/api/models` | `GPUModelDTO[]` | ✅ Available | `useModels()` |
| `/api/report` | `ReportDTO` | ✅ Available | `useReport()` |

## Endpoint Details

### `/api/health`

**Description:** Simple health check endpoint to verify API is running

**Response DTO:** `HealthStatus`
```typescript
interface HealthStatus {
  status: string;
}
```

**Parameters:** None

**Suggested Hook:** `useHealthCheck()`

---

### `/api/listings`

**Description:** Retrieve GPU listings from SQLite database with filtering, fuzzy matching, and pagination

**Response DTO:** Array of `GPUListingDTO`
```typescript
interface GPUListingDTO {
  canonicalModel: string;  // The canonical model name of the GPU
  vramGb: number;          // The amount of VRAM in GB
  migSupport: number;      // The MIG support level (0-7)
  nvlink: boolean;         // Whether the GPU supports NVLink
  tdpWatts: number;        // The TDP in watts
  price: number;           // The price in USD
  score: number;           // The calculated utility score
  importId?: string;       // The import batch ID
  importIndex?: number;    // The sequential index within the import batch
}
```

**Parameters:**
- `model` (optional): Filter by model name (supports fuzzy matching)
- `min_price` (optional): Minimum price filter
- `max_price` (optional): Maximum price filter
- `import_id` (optional): Filter by import batch ID
- `limit` (optional, default: 100): Maximum number of results (max: 1000)
- `offset` (optional, default: 0): Number of results to skip for pagination

**Suggested Hook:** `useListings()`

---

### `/api/listings/legacy`

**Description:** Retrieve all GPU listings with optional filtering by model and quantization capability (legacy endpoint)

**Response DTO:** Array of `GPUListingDTO` (same as above)

**Parameters:**
- `model` (optional): Filter by exact model name
- `quantized` (optional): Filter by quantization capability

**Suggested Hook:** `useListingsLegacy()`

---

### `/api/models`

**Description:** Retrieve all GPU model metadata including specifications and market data

**Response DTO:** Array of `GPUModelDTO`
```typescript
interface GPUModelDTO {
  model: string;           // The model name of the GPU
  listingCount: number;    // The number of listings for this model
  minPrice: number;        // The minimum price for this model
  medianPrice: number;     // The median price for this model
  maxPrice: number;        // The maximum price for this model
  avgPrice: number;        // The average price for this model
  vramGb?: number;         // The amount of VRAM in GB
  tdpWatts?: number;       // The TDP in watts
  migSupport?: number;     // The MIG support level (0-7)
  nvlink?: boolean;        // Whether the GPU supports NVLink
  generation?: string;     // The GPU generation (e.g., Ada, Ampere)
  cudaCores?: number;      // The number of CUDA cores
  slotWidth?: number;      // The slot width
  pcieGeneration?: number; // The PCIe generation
}
```

**Parameters:** None

**Suggested Hook:** `useModels()`

---

### `/api/report`

**Description:** Retrieve the latest GPU market insight report with summary statistics and scoring weights

**Response DTO:** `ReportDTO`
```typescript
interface ReportDTO {
  markdown: string;                    // The full markdown content of the report
  summaryStats: Record<string, string>; // Summary statistics from the report
  topRanked: string[];                 // List of top-ranked GPU models
  scoringWeights: Record<string, number>; // Weights used for scoring
}
```

**Parameters:** None

**Suggested Hook:** `useReport()`

## Implementation Status

All of the endpoints listed above are currently available and can be consumed by the frontend. The suggested hooks have been implemented for all endpoints and can be found in the `@repo/client` package.

## Usage Example

```tsx
import { hooks } from '@repo/client';

function ReportPage() {
  const { data, isLoading, isError, refetch } = hooks.useReport();
  
  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error loading report</div>;
  
  return (
    <div>
      <h1>GPU Market Insight Report</h1>
      <div dangerouslySetInnerHTML={{ __html: data.markdown }} />
      <h2>Top Ranked GPUs</h2>
      <ul>
        {data.topRanked.map((model, index) => (
          <li key={index}>{model}</li>
        ))}
      </ul>
    </div>
  );
}
```