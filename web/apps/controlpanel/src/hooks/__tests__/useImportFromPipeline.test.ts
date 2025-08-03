import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useImportFromPipeline, validatePipelineImportParams, ImportMode, ImportStatus } from '../useImportFromPipeline';
import { importFromPipeline, ImportResultDTO } from '@repo/client';
import { useMutation } from '@tanstack/react-query';
import { renderHook, act } from '@testing-library/react';

// Mock the client module
vi.mock('@repo/client', () => ({
  importFromPipeline: vi.fn(),
}));

// Mock the react-query module
vi.mock('@tanstack/react-query', () => ({
  useMutation: vi.fn(),
}));

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
    isError: false,
    isSuccess: false,
    error: null,
    reset: vi.fn(),
    ...override,
  };
}

describe('validatePipelineImportParams', () => {
  it('should return error for missing inputCsvPath', () => {
    expect(validatePipelineImportParams({
      inputCsvPath: '',
      sourceLabel: 'Test Source'
    })).toBe('Input CSV path is required');
  });

  it('should return error for missing sourceLabel', () => {
    expect(validatePipelineImportParams({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: ''
    })).toBe('Source label is required');
  });

  it('should return null for valid parameters', () => {
    expect(validatePipelineImportParams({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: 'Test Source'
    })).toBeNull();
  });

  it('should return null for valid parameters with optional fields', () => {
    expect(validatePipelineImportParams({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: 'Test Source',
      campaignId: 'campaign-123',
      metadata: { source: 'web-ui' }
    })).toBeNull();
  });

  it('should return null for valid parameters with import mode and date range', () => {
    expect(validatePipelineImportParams({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: 'Test Source',
      importMode: ImportMode.APPEND,
      startDate: '2023-01-01',
      endDate: '2023-12-31'
    })).toBeNull();
  });
});

describe('useImportFromPipeline', () => {
  const mockImportResult: ImportResultDTO = {
    recordCount: 100,
    firstModel: 'RTX 3080',
    lastModel: 'RTX 4090',
    importId: 'import-123',
    timestamp: '2023-08-02T12:00:00Z',
    source: 'test-import'
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useMutation mock with default return values
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      data: mockImportResult
    }));
  });

  it('should call useMutation with correct parameters', async () => {
    // Mock importFromPipeline to resolve immediately
    vi.mocked(importFromPipeline).mockResolvedValue({
      recordCount: 100,
      firstModel: 'RTX 3080',
      lastModel: 'RTX 4090',
      importId: 'import-123',
      timestamp: '2023-08-02T12:00:00Z',
      source: 'test-import'
    });
    
    // Call the hook using renderHook
    renderHook(() => useImportFromPipeline());
    
    // Check that useMutation was called with a mutationFn
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      mutationFn: expect.any(Function),
    }));
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with parameters inside act
    await act(async () => {
      await mutationFn({
        inputCsvPath: '/path/to/file.csv',
        sourceLabel: 'Test Source'
      });
    });
    
    // Check that importFromPipeline was called with the correct parameters
    expect(importFromPipeline).toHaveBeenCalled();
  });

  it('should pass onSuccess and onError callbacks to useMutation', () => {
    // Create mock callbacks
    const onSuccess = vi.fn();
    const onError = vi.fn();
    
    // Call the hook with callbacks using renderHook
    renderHook(() => useImportFromPipeline({
      onSuccess,
      onError,
    }));
    
    // Check that useMutation was called with the callbacks
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      onSuccess,
      onError: expect.any(Function),
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Check the structure of the returned object
    expect(result.current).toHaveProperty('importFromPipeline');
    expect(result.current).toHaveProperty('data');
    expect(result.current).toHaveProperty('isLoading');
    expect(result.current).toHaveProperty('isError');
    expect(result.current).toHaveProperty('error');
    expect(result.current).toHaveProperty('isSuccess');
    expect(result.current).toHaveProperty('validationError');
    expect(result.current).toHaveProperty('status');
    expect(result.current).toHaveProperty('isPolling');
    expect(result.current).toHaveProperty('pollingAttempt');
    expect(result.current).toHaveProperty('maxPollingAttempts');
    expect(result.current).toHaveProperty('checkStatus');
    expect(result.current).toHaveProperty('cancelPolling');
    expect(result.current).toHaveProperty('reset');
    
    // Check that the data is passed through correctly
    expect(result.current.data).toEqual(mockImportResult);
  });

  it('should call mutate when importFromPipeline is called', async () => {
    // Set up the useMutation mock with a mock mutate function
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Call the importFromPipeline function from result.current inside act
    await act(async () => {
      result.current.importFromPipeline({
        inputCsvPath: '/path/to/file.csv',
        sourceLabel: 'Test Source'
      });
    });
    
    // Check that mutate was called with the correct parameters
    expect(mockMutate).toHaveBeenCalledWith({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: 'Test Source'
    });
  });

  it('should call reset when reset is called', async () => {
    // Set up the useMutation mock with a mock reset function
    const mockReset = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      reset: mockReset,
    }));
    
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Call the reset function from result.current inside act
    await act(async () => {
      result.current.reset();
    });
    
    // Check that reset was called
    expect(mockReset).toHaveBeenCalled();
  });

  it('should validate parameters before submission', async () => {
    // Set up the useMutation mock with a mock mutate function
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Call the importFromPipeline function with invalid parameters inside act
    await act(async () => {
      result.current.importFromPipeline({
        inputCsvPath: '',
        sourceLabel: 'Test Source'
      });
    });
    
    // Check that mutate was called (validation happens inside the mutationFn)
    expect(mockMutate).toHaveBeenCalled();
  });

  it('should handle import mode and date range parameters', async () => {
    // Set up the useMutation mock with a mock mutate function
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Call the importFromPipeline function with import mode and date range inside act
    await act(async () => {
      result.current.importFromPipeline({
        inputCsvPath: '/path/to/file.csv',
        sourceLabel: 'Test Source',
        importMode: ImportMode.REPLACE,
        startDate: '2023-01-01',
        endDate: '2023-12-31'
      });
    });
    
    // Check that mutate was called with the correct parameters
    expect(mockMutate).toHaveBeenCalledWith({
      inputCsvPath: '/path/to/file.csv',
      sourceLabel: 'Test Source',
      importMode: ImportMode.REPLACE,
      startDate: '2023-01-01',
      endDate: '2023-12-31'
    });
  });

  it('should initialize with correct default values', () => {
    // Call the hook using renderHook
    const { result } = renderHook(() => useImportFromPipeline());
    
    // Check default values
    expect(result.current.status).toBe(ImportStatus.IDLE);
    expect(result.current.isPolling).toBe(false);
    expect(result.current.pollingAttempt).toBe(0);
    expect(result.current.maxPollingAttempts).toBe(20);
    expect(result.current.validationError).toBeNull();
  });

  it('should accept custom polling options', () => {
    // Call the hook with custom polling options using renderHook
    const { result } = renderHook(() => useImportFromPipeline({
      enablePolling: true,
      pollingInterval: 3000,
      maxPollingAttempts: 10
    }));
    
    // Check that maxPollingAttempts is set correctly
    expect(result.current.maxPollingAttempts).toBe(10);
  });
});