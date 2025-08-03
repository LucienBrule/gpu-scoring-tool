import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useGpuReports, parseMarkdown } from '../useGpuReports';
import { ApiClient, getReports } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import type { ReportDTO } from '@repo/client';
import { renderHook } from '@testing-library/react';
import { createQueryClientWrapper } from '../../test-utils/queryClientWrapper';

// Mock the ApiClient and standalone functions
vi.mock('@repo/client', () => ({
  ApiClient: {
    getReports: vi.fn(),
  },
  getReports: vi.fn(),
}));

// Mock the react-query module
vi.mock('@tanstack/react-query', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useQuery: vi.fn(),
  };
});

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

describe('useGpuReports', () => {
  const mockReportsData: ReportDTO[] = [
    {
      id: '1',
      title: 'NVIDIA RTX 4090 Report',
      content: '# RTX 4090 Analysis\n\nThis is a markdown report for the RTX 4090.',
      model: 'RTX 4090',
      timestamp: '2023-08-01T12:00:00Z',
      author: 'GPU Analysis Team',
      stats: {
        averagePrice: 1599.99,
        minPrice: 1499.99,
        maxPrice: 1799.99,
        listingCount: 120,
      },
    },
    {
      id: '2',
      title: 'NVIDIA RTX 4080 Report',
      content: '# RTX 4080 Analysis\n\nThis is a markdown report for the RTX 4080.',
      model: 'RTX 4080',
      timestamp: '2023-08-01T12:00:00Z',
      author: 'GPU Analysis Team',
      stats: {
        averagePrice: 1199.99,
        minPrice: 1099.99,
        maxPrice: 1299.99,
        listingCount: 95,
      },
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockReportsData
    }));
    // Ensure ApiClient.getReports is properly mocked
    vi.mocked(ApiClient.getReports).mockResolvedValue(mockReportsData);
  });

  it('should use correct query key with all parameters', () => {
    const params = {
      model: 'RTX 4090',
      minPrice: 1000,
      maxPrice: 2000,
      limit: 10,
      offset: 0,
    };
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => useGpuReports(params), { wrapper });
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['reports', params.model, params.minPrice, params.maxPrice, params.limit, params.offset],
    }));
  });

  it('should call ApiClient.getReports with correct parameters', () => {
    const params = {
      model: 'RTX 4090',
      minPrice: 1000,
      maxPrice: 2000,
      limit: 10,
      offset: 0,
    };
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => useGpuReports(params), { wrapper });
    
    // Check that useQuery was called with a queryFn that calls getReports
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getReports).toHaveBeenCalledWith(params);
  });

  it('should use default values when parameters are not provided', () => {
    // Call the hook with no parameters using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => useGpuReports(), { wrapper });
    
    // Check that useQuery was called with default values in the queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['reports', undefined, undefined, undefined, 10, 0],
    }));
    
    // Check that getReports is called with default values
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getReports).toHaveBeenCalledWith({
      model: undefined,
      minPrice: undefined,
      maxPrice: undefined,
      limit: 10,
      offset: 0,
    });
  });

  it('should return the expected structure', () => {
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => useGpuReports(), { wrapper });
    
    // Check the structure of the returned object
    expect(result.current).toHaveProperty('data');
    expect(result.current).toHaveProperty('isLoading');
    expect(result.current).toHaveProperty('isError');
    expect(result.current).toHaveProperty('error');
    expect(result.current).toHaveProperty('refetch');
    expect(result.current).toHaveProperty('parseMarkdown');
    
    // Check that the data is passed through correctly
    expect(result.current.data).toEqual(mockReportsData);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch reports';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => useGpuReports(), { wrapper });
    
    // Check that error state is handled correctly
    expect(result.current.isError).toBe(true);
    expect(result.current.error).toBe(errorMessage);
    expect(result.current.data).toBeUndefined();
  });

  it('should configure retry behavior for 404 errors', () => {
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => useGpuReports(), { wrapper });
    
    // Get the retry function from the useQuery call
    const retryFn = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].retry;
    
    // Check that the retry function returns false for 404 errors
    expect(retryFn(1, new Error('404 Not Found'))).toBe(false);
    
    // Check that the retry function returns true for other errors (up to 3 retries)
    expect(retryFn(1, new Error('500 Internal Server Error'))).toBe(true);
    expect(retryFn(2, new Error('500 Internal Server Error'))).toBe(true);
    expect(retryFn(3, new Error('500 Internal Server Error'))).toBe(false);
  });
});

describe('parseMarkdown', () => {
  it('should return the input markdown string', () => {
    const markdown = '# Test Heading\n\nThis is a test paragraph.';
    expect(parseMarkdown(markdown)).toBe(markdown);
  });

  it('should handle empty strings', () => {
    expect(parseMarkdown('')).toBe('');
  });
});