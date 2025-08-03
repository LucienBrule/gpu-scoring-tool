import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useGpuClassification, formatConfidence, meetsThreshold } from '../useGpuClassification';
import { classifyGpu } from '@repo/client';
import { useMutation } from '@tanstack/react-query';

// Mock the client module
vi.mock('@repo/client', () => ({
  classifyGpu: vi.fn(),
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

describe('useGpuClassification', () => {
  const mockClassificationData = {
    mlIsGpu: true,
    mlScore: 0.95,
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useMutation mock with default return values
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      data: mockClassificationData
    }));
  });

  it('should call useMutation with correct parameters', () => {
    // Call the hook
    useGpuClassification();
    
    // Check that useMutation was called with a mutationFn
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      mutationFn: expect.any(Function),
    }));
    
    // Get the mutationFn from the useMutation call
    const mutationFn = (useMutation as ReturnType<typeof vi.fn>).mock.calls[0][0].mutationFn;
    
    // Call the mutationFn with a title
    mutationFn('NVIDIA RTX 4090');
    
    // Check that classifyGpu was called with the title
    expect(classifyGpu).toHaveBeenCalledWith('NVIDIA RTX 4090');
  });

  it('should pass onSuccess and onError callbacks to useMutation', () => {
    // Create mock callbacks
    const onSuccess = vi.fn();
    const onError = vi.fn();
    
    // Call the hook with callbacks
    useGpuClassification({
      onSuccess,
      onError,
    });
    
    // Check that useMutation was called with the callbacks
    expect(useMutation).toHaveBeenCalledWith(expect.objectContaining({
      onSuccess,
      onError,
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useGpuClassification();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('classify');
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('isSuccess');
    expect(result).toHaveProperty('reset');
    expect(result).toHaveProperty('formatConfidence');
    expect(result).toHaveProperty('meetsThreshold');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockClassificationData);
  });

  it('should call mutate when classify is called', () => {
    // Set up the useMutation mock with a mock mutate function
    const mockMutate = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      mutate: mockMutate,
    }));
    
    // Call the hook
    const { classify } = useGpuClassification();
    
    // Call the classify function
    classify('NVIDIA RTX 4090');
    
    // Check that mutate was called with the title
    expect(mockMutate).toHaveBeenCalledWith('NVIDIA RTX 4090');
  });

  it('should call reset when reset is called', () => {
    // Set up the useMutation mock with a mock reset function
    const mockReset = vi.fn();
    (useMutation as ReturnType<typeof vi.fn>).mockReturnValue(mockUseMutationReturn({
      reset: mockReset,
    }));
    
    // Call the hook
    const { reset } = useGpuClassification();
    
    // Call the reset function
    reset();
    
    // Check that reset was called
    expect(mockReset).toHaveBeenCalled();
  });

  it('should use the provided confidence threshold for meetsThreshold', () => {
    // Call the hook with a custom confidence threshold
    const { meetsThreshold } = useGpuClassification({
      confidenceThreshold: 0.8,
    });
    
    // Check that meetsThreshold uses the custom threshold
    expect(meetsThreshold(0.7)).toBe(false);
    expect(meetsThreshold(0.8)).toBe(true);
    expect(meetsThreshold(0.9)).toBe(true);
  });
});

describe('formatConfidence', () => {
  it('should format confidence score as percentage with one decimal place', () => {
    expect(formatConfidence(0)).toBe('0.0%');
    expect(formatConfidence(0.5)).toBe('50.0%');
    expect(formatConfidence(0.75)).toBe('75.0%');
    expect(formatConfidence(1)).toBe('100.0%');
  });

  it('should handle undefined score', () => {
    expect(formatConfidence(undefined)).toBe('N/A');
  });
});

describe('meetsThreshold', () => {
  it('should return true if score meets or exceeds threshold', () => {
    expect(meetsThreshold(0.5, 0.5)).toBe(true);
    expect(meetsThreshold(0.6, 0.5)).toBe(true);
    expect(meetsThreshold(1, 0.5)).toBe(true);
  });

  it('should return false if score is below threshold', () => {
    expect(meetsThreshold(0.4, 0.5)).toBe(false);
    expect(meetsThreshold(0, 0.5)).toBe(false);
  });

  it('should use default threshold of 0.5 if not provided', () => {
    expect(meetsThreshold(0.4)).toBe(false);
    expect(meetsThreshold(0.5)).toBe(true);
    expect(meetsThreshold(0.6)).toBe(true);
  });

  it('should handle undefined score', () => {
    expect(meetsThreshold(undefined, 0.5)).toBe(false);
  });
});