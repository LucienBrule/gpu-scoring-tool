import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useGpuListings, useGpuListingById } from '../useGpuListings';
import { ApiClient, getListings } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import type { GPUListingDTO } from '@repo/client';

// Mock the ApiClient and standalone functions
vi.mock('@repo/client', () => ({
  ApiClient: {
    getListings: vi.fn(),
  },
  getListings: vi.fn(),
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

describe('useGpuListings', () => {
  const mockListingsData: GPUListingDTO[] = [
    {
      id: '1',
      title: 'NVIDIA RTX 4090 24GB',
      price: 1599.99,
      model: 'RTX 4090',
      url: 'https://example.com/gpu/1',
      source: 'TestSource',
      timestamp: '2023-08-01T12:00:00Z',
    },
    {
      id: '2',
      title: 'NVIDIA RTX 4080 16GB',
      price: 1199.99,
      model: 'RTX 4080',
      url: 'https://example.com/gpu/2',
      source: 'TestSource',
      timestamp: '2023-08-01T12:00:00Z',
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockListingsData
    }));
  });

  it('should use correct query key with all parameters', () => {
    const params = {
      limit: 20,
      offset: 20,
      fromDate: '2023-01-01',
      toDate: '2023-12-31',
      model: 'RTX 4090',
      minPrice: 1000,
      maxPrice: 2000,
    };
    
    // Call the hook
    useGpuListings(params);
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['listings', params.limit, params.offset, params.model, params.minPrice, params.maxPrice, params.fromDate, params.toDate],
    }));
  });

  it('should call getListings function with correct parameters', () => {
    const params = {
      limit: 20,
      offset: 20,
      fromDate: '2023-01-01',
      toDate: '2023-12-31',
      model: 'RTX 4090',
      minPrice: 1000,
      maxPrice: 2000,
    };
    
    // Call the hook
    useGpuListings(params);
    
    // Check that useQuery was called with a queryFn that calls getListings
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getListings).toHaveBeenCalledWith(params);
  });

  it('should use default values when parameters are not provided', () => {
    // Call the hook with no parameters
    useGpuListings();
    
    // Check that useQuery was called with default values in the queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['listings', 10, 0, undefined, undefined, undefined, undefined, undefined],
    }));
    
    // Check that getListings is called with default values
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getListings).toHaveBeenCalledWith({
      limit: 10,
      offset: 0,
      model: undefined,
      minPrice: undefined,
      maxPrice: undefined,
      fromDate: undefined,
      toDate: undefined,
    });
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useGpuListings();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockListingsData);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch listings';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useGpuListings();
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });
});

describe('useGpuListingById', () => {
  const mockListingsData: GPUListingDTO[] = [
    {
      id: '123',
      title: 'NVIDIA RTX 4090 24GB',
      price: 1599.99,
      model: 'RTX 4090',
      url: 'https://example.com/gpu/123',
      source: 'TestSource',
      timestamp: '2023-08-01T12:00:00Z',
    }
  ];

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('should use correct query key with ID', () => {
    // Set up the useQuery mock to return a single listing
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockListingsData
    }));
    
    // Call the hook
    useGpuListingById('123');
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['listing', '123'],
    }));
  });

  it('should call getListings function with ID parameter', () => {
    // Set up the useQuery mock to return a single listing
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockListingsData
    }));
    
    // Call the hook
    useGpuListingById('123');
    
    // Check that useQuery was called with a queryFn that calls getListings
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getListings).toHaveBeenCalledWith({ id: '123' });
  });

  it('should extract the first listing from the result array', () => {
    // Set up the useQuery mock to return an array with a single listing
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockListingsData
    }));
    
    // Call the hook
    const result = useGpuListingById('123');
    
    // Check that the data is the first listing from the array
    expect(result.data).toEqual(mockListingsData[0]);
  });

  it('should return undefined data when the result array is empty', () => {
    // Set up the useQuery mock to return an empty array
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: []
    }));
    
    // Call the hook
    const result = useGpuListingById('123');
    
    // Check that the data is undefined
    expect(result.data).toBeUndefined();
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch listing';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useGpuListingById('123');
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBeInstanceOf(Error);
    expect(result.error?.message).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });

  it('should not run the query if ID is not provided', () => {
    // Set up the useQuery mock
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn());
    
    // Call the hook with an empty ID
    useGpuListingById('');
    
    // Check that useQuery was called with enabled: false
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      enabled: false,
    }));
  });
});