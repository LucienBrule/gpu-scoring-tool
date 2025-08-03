import { describe, it, expect, vi, beforeEach } from 'vitest';
import { usePersistListings, validateListings, PersistenceMode, ConflictResolution } from '../usePersistListings';
import { persistListings, ImportResult } from '@repo/client';
import { useMutation } from '@tanstack/react-query';
import { renderHook, act } from '@testing-library/react';
import { createQueryClientWrapper } from '../../test-utils/queryClientWrapper';

// We're not mocking React hooks anymore, as it was causing issues with the useState function
// Instead, we'll let the test use the real useState, useCallback, and useEffect functions

// Mock the client module
vi.mock('@repo/client', () => ({
  persistListings: vi.fn(),
}));

// Mock the react-query module
vi.mock('@tanstack/react-query', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useMutation: vi.fn(),
  };
});

/**
 * Helper function to create mock return values for useMutation
 * @param override - Override specific properties of the default mock return value
 * @returns A mock return value for useMutation
 */
function mockUseMutationReturn(override = {}) {
  return {
    mutate: vi.fn(),
    data: undefined,
    isPending: false,
    isLoading: false, // Add isLoading for backward compatibility
    isError: false,
    isSuccess: false,
    error: null,
    reset: vi.fn(),
    ...override,
  };
}

describe('validateListings', () => {
  it('should return error for missing listings array', () => {
    expect(validateListings({} as Partial<{ listings: GpuListing[] }>)).toBe('Listings array is required');
  });

  it('should return error for empty listings array', () => {
    expect(validateListings({ listings: [] })).toBe('Listings array cannot be empty');
  });

  it('should return error for listings missing required fields', () => {
    expect(validateListings({
      listings: [{ price: 100 } as Partial<GpuListing>]
    })).toContain('missing required field: canonicalModel');

    expect(validateListings({
      listings: [{ canonicalModel: 'RTX 3080' } as Partial<GpuListing>]
    })).toContain('missing required field: price');
  });

  it('should return null for valid listings', () => {
    expect(validateListings({
      listings: [{
        canonicalModel: 'RTX 3080',
        vramGb: 10,
        migSupport: 0,
        nvlink: true,
        tdpWatts: 320,
        price: 699.99,
        score: 0.85
      }]
    })).toBeNull();
  });
});

describe('usePersistListings', () => {
  const mockImportResult: ImportResult = {
    recordCount: 100,
    firstModel: 'RTX 3080',
    lastModel: 'RTX 4090',
    importId: 'import-123',
    timestamp: '2023-08-02T12:00:00Z',
    source: 'test-import'
  };

  const mockListings = [
    {
      canonicalModel: 'RTX 3080',
      vramGb: 10,
      migSupport: 0,
      nvlink: true,
      tdpWatts: 320,
      price: 699.99,
      score: 0.85
    },
    {
      canonicalModel: 'RTX 4090',
      vramGb: 24,
      migSupport: 0,
      nvlink: true,
      tdpWatts: 450,
      price: 1599.99,
      score: 0.95
    }
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useMutation mock with default return values
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      data: mockImportResult
    }));
  });

  it('should call useMutation with correct parameters', () => {
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => usePersistListings(), { wrapper });
    
    // Check that useMutation was called with a mutationFn
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      mutationFn: expect.any(Function),
    }));
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with listings
    mutationFn({ listings: mockListings });
    
    // Check that persistListings was called with the correct parameters
    expect(persistListings).toHaveBeenCalled();
  });

  it('should pass onSuccess and onError callbacks to useMutation', () => {
    // Create mock callbacks
    const onSuccess = vi.fn();
    const onError = vi.fn();
    
    // Call the hook with callbacks using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    renderHook(() => usePersistListings({
      onSuccess,
      onError,
    }), { wrapper });
    
    // Check that useMutation was called with the callbacks
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      onSuccess,
      onError,
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => usePersistListings(), { wrapper });
    
    // Check the structure of the returned object
    expect(result.current).toHaveProperty('persistListings');
    expect(result.current).toHaveProperty('data');
    expect(result.current).toHaveProperty('isLoading');
    expect(result.current).toHaveProperty('isError');
    expect(result.current).toHaveProperty('error');
    expect(result.current).toHaveProperty('isSuccess');
    expect(result.current).toHaveProperty('validationError');
    expect(result.current).toHaveProperty('reset');
    
    // Check that the data is passed through correctly
    expect(result.current.data).toEqual(mockImportResult);
  });

  it('should call mutate when persistListings is called', () => {
    // Set up the useMutation mock with a mock mutate function
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => usePersistListings(), { wrapper });
    
    // Call the persistListings function from result.current
    result.current.persistListings({ listings: mockListings });
    
    // Check that mutate was called with the listings
    expect(mockMutate).toHaveBeenCalledWith({ listings: mockListings });
  });

  it('should call reset when reset is called', () => {
    // Set up the useMutation mock with a mock reset function
    const mockReset = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      reset: mockReset,
    }));
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => usePersistListings(), { wrapper });
    
    // Call the reset function from result.current
    result.current.reset();
    
    // Check that reset was called
    expect(mockReset).toHaveBeenCalled();
  });

  it('should use default options when not provided', () => {
    // Set up the useMutation mock
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => usePersistListings(), { wrapper });
    
    // Call the persistListings function without options
    result.current.persistListings({ listings: mockListings });
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with listings
    mutationFn({ listings: mockListings });
    
    // Check that persistListings was called with default options
    expect(persistListings).toHaveBeenCalledWith(
      mockListings,
      expect.objectContaining({
        mode: PersistenceMode.UPSERT,
        conflictResolution: ConflictResolution.OVERWRITE,
        batchSize: 100,
      })
    );
  });

  it('should use provided options instead of defaults', () => {
    // Set up the useMutation mock
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook with custom defaults using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    const { result } = renderHook(() => usePersistListings({
      defaultMode: PersistenceMode.CREATE,
      defaultConflictResolution: ConflictResolution.SKIP,
      defaultBatchSize: 50,
    }), { wrapper });
    
    // Call the persistListings function with custom options
    result.current.persistListings({
      listings: mockListings,
      mode: PersistenceMode.UPDATE,
      conflictResolution: ConflictResolution.MERGE,
      batchSize: 25,
    });
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with listings and options
    mutationFn({
      listings: mockListings,
      mode: PersistenceMode.UPDATE,
      conflictResolution: ConflictResolution.MERGE,
      batchSize: 25,
    });
    
    // Check that persistListings was called with the provided options
    expect(persistListings).toHaveBeenCalledWith(
      mockListings,
      expect.objectContaining({
        mode: PersistenceMode.UPDATE,
        conflictResolution: ConflictResolution.MERGE,
        batchSize: 25,
      })
    );
  });

  it('should validate listings before submission', async () => {
    // Set up the useMutation mock
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook with QueryClientProvider wrapper
    const wrapper = createQueryClientWrapper();
    let result;
    
    await act(async () => {
      // Wrap the renderHook call in act to handle state updates
      const hookResult = renderHook(() => usePersistListings(), { wrapper });
      result = hookResult.result;
    });
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with invalid listings, wrapped in act
    await act(async () => {
      await expect(mutationFn({ listings: [] })).rejects.toThrow('Listings array cannot be empty');
    });
    
    // Check that persistListings was not called
    expect(mockMutate).not.toHaveBeenCalled();
  });
});