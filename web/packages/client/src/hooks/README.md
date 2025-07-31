# Generated React Query Hooks

This directory contains React Query hooks that are automatically generated from the OpenAPI schema. These hooks provide a convenient way to fetch data from the backend API.

## Available Hooks

The following hooks are available:

### `useHealthCheck`

Fetches the health status of the backend API.

```tsx
import { hooks } from '@repo/client';

function HealthCheck() {
  const { status, loading, error, refetch } = hooks.useHealthCheck();
  
  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {status && <p>Status: {status}</p>}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### `useReports`

Fetches GPU reports data with optional filtering.

```tsx
import { hooks } from '@repo/client';

function Reports() {
  const { data, isLoading, isError, refetch } = hooks.useReports({
    model: 'RTX 3090',
    minPrice: 1000,
    maxPrice: 2000,
    limit: 10,
    offset: 0
  });
  
  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {isError && <p>Error loading reports</p>}
      {data && (
        <ul>
          {data.map((report, index) => (
            <li key={index}>{report.canonicalModel} - ${report.price}</li>
          ))}
        </ul>
      )}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### `useListingsLegacy`

Fetches GPU listings from the legacy endpoint with optional filtering.

```tsx
import { hooks } from '@repo/client';

function LegacyListings() {
  const { data, isLoading, isError, refetch } = hooks.useListingsLegacy({
    model: 'RTX 3090',
    quantized: true
  });
  
  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {isError && <p>Error loading listings</p>}
      {data && (
        <ul>
          {data.map((listing, index) => (
            <li key={index}>{listing.canonicalModel} - ${listing.price}</li>
          ))}
        </ul>
      )}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### `useModels`

Fetches all GPU model metadata.

```tsx
import { hooks } from '@repo/client';

function Models() {
  const { data, isLoading, isError, refetch } = hooks.useModels();
  
  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {isError && <p>Error loading models</p>}
      {data && (
        <ul>
          {data.map((model, index) => (
            <li key={index}>{model.model} - ${model.avgPrice}</li>
          ))}
        </ul>
      )}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### `useReport`

Fetches the latest GPU market insight report.

```tsx
import { hooks } from '@repo/client';

function Report() {
  const { data, isLoading, isError, refetch } = hooks.useReport();
  
  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {isError && <p>Error loading report</p>}
      {data && (
        <div>
          <h2>Market Insight Report</h2>
          <div dangerouslySetInnerHTML={{ __html: data.markdown }} />
          <h3>Top Ranked GPUs</h3>
          <ul>
            {data.topRanked.map((gpu, index) => (
              <li key={index}>{gpu}</li>
            ))}
          </ul>
        </div>
      )}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

## Generating Hooks

These hooks are generated from the OpenAPI schema using the `generate-hooks-simple.js` script. To generate new hooks or update existing ones, run:

```bash
cd packages/client
node scripts/generate-hooks-simple.js
```

Note that the generated hooks contain placeholder implementations. You will need to update the client.ts file to add the actual API calls.

## Implementation Notes

- All hooks use React Query for data fetching and caching
- Hooks return a consistent interface: `{ data, isLoading, isError, refetch }`
- Hooks with filters accept an optional filters object as a parameter
- The query key is based on the hook name and filters
- Error handling is built-in