import { describe, it, expect, vi, beforeEach } from 'vitest';
import { usePollingForecast } from '../usePollingForecast';
import { getForecastDeltas } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import { ForecastDelta } from '../useForecastDeltas';

// Mock the client module
vi.mock('@repo/client', () => ({
  getForecastDeltas: vi.fn(),
}));

// Mock the react-query module
vi.mock('@tanstack/react-query', () => ({
  useQuery: vi.fn(),
}));

/**
 * Helper function to create mock return values for useQuery
 * @param override - Override specific properties of the default mock return value
 * @returns A mock return value for useQuery
 */
function mockUseQueryReturn(override = {}) {
  return {
    data: undefined,
    isLoading: false,
    isError: false,
    error: null,
    isFetching: false,
    refetch: vi.fn(),
    ...override,
  };
}

describe('usePollingForecast', () => {
  const mockForecastDeltas: ForecastDelta[] = [
    {
      id: 1,
      model: 'RTX 4090',
      oldPrice: 1599.99,
      newPrice: 1499.99,
      priceChangePct: -6.25,
      region: 'US',
      timestamp: '2023-08-01T12:00:00Z',
      listingId: '123',
      source: 'TestSource',
    },
    {
      id: 2,
      model: 'RTX 4080',
      oldPrice: 1199.99,
      newPrice: 1099.99,
      priceChangePct: -8.33,
      region: 'US',
      timestamp: '2023-08-01T12:00:00Z',
      listingId: '456',
      source: 'TestSource',
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockForecastDeltas
    }));
  });

  it('should use correct query key with all parameters', () => {
    const params = {
      model: 'RTX 4090',
      region: 'US',
      limit: 10,
      intervalMs: 30000,
    };
    
    // Call the hook
    usePollingForecast(params);
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['forecast-deltas', { model: params.model, region: params.region, limit: params.limit }],
    }));
  });

  it('should call getForecastDeltas with correct parameters', () => {
    const params = {
      model: 'RTX 4090',
      region: 'US',
      limit: 10,
      intervalMs: 30000,
    };
    
    // Call the hook
    usePollingForecast(params);
    
    // Check that useQuery was called with a queryFn that calls getForecastDeltas
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    
    // Verify getForecastDeltas is called with the correct parameters (excluding intervalMs)
    expect(getForecastDeltas).toHaveBeenCalledWith({
      model: params.model,
      region: params.region,
      limit: params.limit,
    });
  });

  it('should use default values when parameters are not provided', () => {
    // Call the hook with no parameters
    usePollingForecast();
    
    // Check that useQuery was called with default values in the queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['forecast-deltas', { model: undefined, region: undefined, limit: 10 }],
    }));
    
    // Check that getForecastDeltas is called with default values
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getForecastDeltas).toHaveBeenCalledWith({
      model: undefined,
      region: undefined,
      limit: 10,
    });
  });

  it('should set the refetchInterval to the provided intervalMs', () => {
    const params = {
      intervalMs: 30000, // 30 seconds
    };
    
    // Call the hook
    usePollingForecast(params);
    
    // Check that useQuery was called with the correct refetchInterval
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      refetchInterval: 30000,
    }));
  });

  it('should use default refetchInterval of 60000ms when not provided', () => {
    // Call the hook without intervalMs
    usePollingForecast();
    
    // Check that useQuery was called with the default refetchInterval
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      refetchInterval: 60000, // 1 minute
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = usePollingForecast();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('isFetching');
    expect(result).toHaveProperty('refetch');
    expect(result).toHaveProperty('calculatePercentChange');
    expect(result).toHaveProperty('formatPercentChange');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockForecastDeltas);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch forecast deltas';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = usePollingForecast();
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });

  it('should handle isFetching state', () => {
    // Set up the mock to return a fetching state
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockForecastDeltas,
      isLoading: false,
      isFetching: true,
    }));
    
    // Call the hook
    const result = usePollingForecast();
    
    // Check that fetching state is handled correctly
    expect(result.isFetching).toBe(true);
    expect(result.data).toEqual(mockForecastDeltas);
  });
});