# useReports Hook Example

This document demonstrates how to use the `useReports` hook to fetch GPU reports data.

## Basic Usage

```tsx
import { hooks } from '@repo/client';

function ReportsPage() {
  const { data, isLoading, isError, refetch } = hooks.useReports();

  if (isLoading) {
    return <div>Loading reports...</div>;
  }

  if (isError) {
    return <div>Error loading reports</div>;
  }

  return (
    <div>
      <h1>GPU Reports</h1>
      <button onClick={() => refetch()}>Refresh</button>
      
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>VRAM (GB)</th>
            <th>Price</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((report, index) => (
            <tr key={index}>
              <td>{report.canonical_model}</td>
              <td>{report.vram_gb}</td>
              <td>${report.price.toFixed(2)}</td>
              <td>{report.score.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## With Filters

The hook accepts optional filters to narrow down the results:

```tsx
import { hooks } from '@repo/client';
import { useState } from 'react';

function FilteredReportsPage() {
  const [filters, setFilters] = useState({
    model: '',
    minPrice: undefined,
    maxPrice: undefined,
    limit: 10,
    offset: 0
  });
  
  const { data, isLoading, isError, refetch } = hooks.useReports(filters);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: name === 'minPrice' || name === 'maxPrice' ? 
        value ? Number(value) : undefined : 
        value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    refetch();
  };

  return (
    <div>
      <h1>Filtered GPU Reports</h1>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Model:
            <input 
              type="text" 
              name="model" 
              value={filters.model} 
              onChange={handleFilterChange} 
            />
          </label>
        </div>
        
        <div>
          <label>
            Min Price:
            <input 
              type="number" 
              name="minPrice" 
              value={filters.minPrice || ''} 
              onChange={handleFilterChange} 
            />
          </label>
        </div>
        
        <div>
          <label>
            Max Price:
            <input 
              type="number" 
              name="maxPrice" 
              value={filters.maxPrice || ''} 
              onChange={handleFilterChange} 
            />
          </label>
        </div>
        
        <div>
          <label>
            Limit:
            <input 
              type="number" 
              name="limit" 
              value={filters.limit} 
              onChange={handleFilterChange} 
            />
          </label>
        </div>
        
        <div>
          <label>
            Offset:
            <input 
              type="number" 
              name="offset" 
              value={filters.offset} 
              onChange={handleFilterChange} 
            />
          </label>
        </div>
        
        <button type="submit">Apply Filters</button>
      </form>
      
      {isLoading && <div>Loading reports...</div>}
      {isError && <div>Error loading reports</div>}
      
      {data && (
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>VRAM (GB)</th>
              <th>Price</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {data.map((report, index) => (
              <tr key={index}>
                <td>{report.canonical_model}</td>
                <td>{report.vram_gb}</td>
                <td>${report.price.toFixed(2)}</td>
                <td>{report.score.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      
      <div>
        <button 
          onClick={() => setFilters(prev => ({...prev, offset: Math.max(0, prev.offset - prev.limit)}))}
          disabled={filters.offset === 0}
        >
          Previous Page
        </button>
        <button 
          onClick={() => setFilters(prev => ({...prev, offset: prev.offset + prev.limit}))}
          disabled={!data || data.length < filters.limit}
        >
          Next Page
        </button>
      </div>
    </div>
  );
}
```

## TypeScript Types

The hook provides TypeScript types for both the filters and the result:

```tsx
import { hooks } from '@repo/client';

// Filter type
type Filters = hooks.UseReportsFilters;

// Result type
type Result = hooks.UseReportsResult;

// Report row type
type ReportRow = import('@repo/client').GpuReportRow;
```

These types can be used to ensure type safety when working with the hook.