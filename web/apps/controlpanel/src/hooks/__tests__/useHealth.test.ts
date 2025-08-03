import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useHealth } from '../useHealth';
import { ApiClient, getHealth } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import type { HealthStatus } from '@repo/client';

// Mock the ApiClient and standalone functions
vi.mock('@repo/client', () => ({
  ApiClient: {
    getHealth: vi.fn(),
  },
  getHealth: vi.fn(),
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

describe('useHealth', () => {
  const mockHealthData: HealthStatus = {
    status: 'ok',
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockHealthData
    }));
  });

  it('should use correct query key', () => {
    // Call the hook
    useHealth();
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['health'],
    }));
  });

  it('should call getHealth function', () => {
    // Call the hook
    useHealth();
    
    // Check that useQuery was called with a queryFn that calls getHealth
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(vi.mocked(getHealth)).toHaveBeenCalled();
  });

  it('should return the expected structure', () => {
    // Set up the mock to return specific data
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue({
      data: mockHealthData,
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });
    
    // Call the hook
    const result = useHealth();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockHealthData);
    expect(result.data?.status).toBe('ok');
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch health status';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useHealth();
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBeInstanceOf(Error);
    expect(result.error?.message).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });

  it('should handle loading state', () => {
    // Set up the mock to return a loading state
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: true,
      isError: false,
      error: null,
    }));
    
    // Call the hook
    const result = useHealth();
    
    // Check that loading state is handled correctly
    expect(result.isLoading).toBe(true);
    expect(result.data).toBeUndefined();
  });
});