import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useGpuModels } from './useGpuModels';
import { ApiClient, getModels } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import type { GPUModelDTO } from '@repo/client';

// Mock the ApiClient and standalone functions
vi.mock('@repo/client', () => ({
  ApiClient: {
    getModels: vi.fn(),
  },
  getModels: vi.fn(),
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
    data: [],
    isLoading: false,
    isError: false,
    error: null,
    refetch: vi.fn(),
    ...override,
  };
}

describe('useGpuModels', () => {
  const mockModelsData: GPUModelDTO[] = [
    {
      id: '1',
      model: 'NVIDIA RTX 4090',
      manufacturer: 'NVIDIA',
      memoryGB: 24,
      releaseDate: '2022-10-12',
    },
    {
      id: '2',
      model: 'NVIDIA RTX 4080',
      manufacturer: 'NVIDIA',
      memoryGB: 16,
      releaseDate: '2022-11-16',
    },
    {
      id: '3',
      model: 'AMD Radeon RX 7900 XTX',
      manufacturer: 'AMD',
      memoryGB: 24,
      releaseDate: '2022-12-13',
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockModelsData
    }));
  });

  it('should use correct query key', () => {
    // Call the hook
    useGpuModels();
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['models'],
    }));
  });

  it('should call getModels function', () => {
    // Call the hook
    useGpuModels();
    
    // Check that useQuery was called with a queryFn that calls getModels
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getModels).toHaveBeenCalled();
  });

  it('should return the expected structure', () => {
    // Set up the mock to return specific data
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue({
      data: mockModelsData,
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });
    
    // Call the hook
    const result = useGpuModels();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockModelsData);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch models';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useGpuModels();
    
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
    const result = useGpuModels();
    
    // Check that loading state is handled correctly
    expect(result.isLoading).toBe(true);
    expect(result.data).toBeUndefined();
  });
});