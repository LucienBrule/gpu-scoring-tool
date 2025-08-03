import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useForecastDeltas, useForecastDeltaById, calculatePercentChange, formatPercentChange, ForecastDelta } from '../useForecastDeltas';
import { getForecastDeltas, getForecastDeltaById } from '@repo/client';
import { useQuery } from '@tanstack/react-query';

// Mock the client module
vi.mock('@repo/client', () => ({
  getForecastDeltas: vi.fn(),
  getForecastDeltaById: vi.fn(),
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
    refetch: vi.fn(),
    ...override,
  };
}

describe('useForecastDeltas', () => {
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
    const testDate = new Date('2023-01-01');
    const params = {
      model: 'RTX 4090',
      minPriceChangePct: 5,
      after: testDate,
      region: 'US',
      limit: 10,
    };
    
    // Call the hook
    useForecastDeltas(params);
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['forecastDeltas', params.model, params.minPriceChangePct, testDate.toISOString(), params.region, params.limit],
    }));
  });

  it('should call getForecastDeltas with correct parameters', () => {
    const testDate = new Date('2023-01-01');
    const params = {
      model: 'RTX 4090',
      minPriceChangePct: 5,
      after: testDate,
      region: 'US',
      limit: 10,
    };
    
    // Call the hook
    useForecastDeltas(params);
    
    // Check that useQuery was called with a queryFn that calls getForecastDeltas
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getForecastDeltas).toHaveBeenCalledWith(params);
  });

  it('should use default values when parameters are not provided', () => {
    // Call the hook with no parameters
    useForecastDeltas();
    
    // Check that useQuery was called with default values in the queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['forecastDeltas', undefined, undefined, undefined, undefined, 10],
    }));
    
    // Check that getForecastDeltas is called with default values
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getForecastDeltas).toHaveBeenCalledWith({
      model: undefined,
      minPriceChangePct: undefined,
      after: undefined,
      region: undefined,
      limit: 10,
    });
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useForecastDeltas();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
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
    const result = useForecastDeltas();
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });
});

describe('useForecastDeltaById', () => {
  const mockForecastDelta: ForecastDelta = {
    id: 1,
    model: 'RTX 4090',
    oldPrice: 1599.99,
    newPrice: 1499.99,
    priceChangePct: -6.25,
    region: 'US',
    timestamp: '2023-08-01T12:00:00Z',
    listingId: '123',
    source: 'TestSource',
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock to return a single forecast delta
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockForecastDelta
    }));
  });

  it('should use correct query key with ID', () => {
    // Call the hook
    useForecastDeltaById(1);
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['forecastDelta', 1],
    }));
  });

  it('should call getForecastDeltaById with correct ID', () => {
    // Call the hook
    useForecastDeltaById(1);
    
    // Check that useQuery was called with a queryFn that calls getForecastDeltaById
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getForecastDeltaById).toHaveBeenCalledWith(1);
  });

  it('should not run the query if ID is not provided', () => {
    // Call the hook with an invalid ID (0)
    useForecastDeltaById(0);
    
    // Check that useQuery was called with enabled: false
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      enabled: false,
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useForecastDeltaById(1);
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    expect(result).toHaveProperty('calculatePercentChange');
    expect(result).toHaveProperty('formatPercentChange');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockForecastDelta);
  });
});

describe('calculatePercentChange', () => {
  it('should calculate positive percentage change correctly', () => {
    expect(calculatePercentChange(100, 110)).toBe(10);
    expect(calculatePercentChange(50, 75)).toBe(50);
  });

  it('should calculate negative percentage change correctly', () => {
    expect(calculatePercentChange(100, 90)).toBe(-10);
    expect(calculatePercentChange(50, 25)).toBe(-50);
  });

  it('should handle zero old value', () => {
    expect(calculatePercentChange(0, 100)).toBe(0);
  });

  it('should handle zero new value', () => {
    expect(calculatePercentChange(100, 0)).toBe(-100);
  });
});

describe('formatPercentChange', () => {
  it('should format positive percentage change correctly', () => {
    expect(formatPercentChange(10)).toBe('+10.00%');
    expect(formatPercentChange(50.5)).toBe('+50.50%');
  });

  it('should format negative percentage change correctly', () => {
    expect(formatPercentChange(-10)).toBe('-10.00%');
    expect(formatPercentChange(-50.5)).toBe('-50.50%');
  });

  it('should format zero percentage change correctly', () => {
    expect(formatPercentChange(0)).toBe('+0.00%');
  });
});