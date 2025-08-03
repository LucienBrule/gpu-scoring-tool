import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useSchemaVersions, useSchemaVersionDetails, formatVersion, isDefaultVersion } from '../useSchemaInfo';
import { getSchemaVersions, getSchemaVersionDetails } from '@repo/client';
import { useQuery } from '@tanstack/react-query';
import type { SchemaVersionInfo, SchemaVersion } from '@repo/client';

// Mock the client module
vi.mock('@repo/client', () => ({
  getSchemaVersions: vi.fn(),
  getSchemaVersionDetails: vi.fn(),
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

describe('useSchemaVersions', () => {
  const mockSchemaVersionsData: SchemaVersionInfo = {
    defaultVersion: '1.0',
    supportedVersions: ['0.9', '1.0', '1.1-beta'],
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockSchemaVersionsData
    }));
  });

  it('should use correct query key', () => {
    // Call the hook
    useSchemaVersions();
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['schemaVersions'],
    }));
  });

  it('should call getSchemaVersions', () => {
    // Call the hook
    useSchemaVersions();
    
    // Check that useQuery was called with a queryFn that calls getSchemaVersions
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getSchemaVersions).toHaveBeenCalled();
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useSchemaVersions();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    expect(result).toHaveProperty('isDefaultVersion');
    expect(result).toHaveProperty('formatVersion');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockSchemaVersionsData);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch schema versions';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useSchemaVersions();
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });

  it('should correctly identify default version', () => {
    // Call the hook
    const result = useSchemaVersions();
    
    // Check that isDefaultVersion works correctly
    expect(result.isDefaultVersion('1.0')).toBe(true);
    expect(result.isDefaultVersion('0.9')).toBe(false);
  });

  it('should format version strings correctly', () => {
    // Call the hook
    const result = useSchemaVersions();
    
    // Check that formatVersion works correctly
    expect(result.formatVersion('1.0')).toBe('v1.0');
    expect(result.formatVersion('v1.0')).toBe('v1.0');
  });
});

describe('useSchemaVersionDetails', () => {
  const mockSchemaVersionData: SchemaVersion = {
    version: '1.0',
    releaseDate: '2023-01-01T00:00:00Z',
    schema: {
      type: 'object',
      properties: {
        id: { type: 'string' },
        name: { type: 'string' },
      },
      required: ['id', 'name'],
    },
  };

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockSchemaVersionData
    }));
  });

  it('should use correct query key with version', () => {
    // Call the hook
    useSchemaVersionDetails('1.0');
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['schemaVersion', '1.0'],
    }));
  });

  it('should call getSchemaVersionDetails with correct version', () => {
    // Call the hook
    useSchemaVersionDetails('1.0');
    
    // Check that useQuery was called with a queryFn that calls getSchemaVersionDetails
    const queryFnArg = (useQuery as ReturnType<typeof vi.fn>).mock.calls[0][0].queryFn;
    queryFnArg();
    expect(getSchemaVersionDetails).toHaveBeenCalledWith('1.0');
  });

  it('should not run the query if version is not provided', () => {
    // Call the hook with an empty version
    useSchemaVersionDetails('');
    
    // Check that useQuery was called with enabled: false
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      enabled: false,
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useSchemaVersionDetails('1.0');
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockSchemaVersionData);
  });

  it('should handle error state', () => {
    // Set up the mock to return an error state
    const errorMessage = 'Failed to fetch schema version details';
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error(errorMessage),
    }));
    
    // Call the hook
    const result = useSchemaVersionDetails('1.0');
    
    // Check that error state is handled correctly
    expect(result.isError).toBe(true);
    expect(result.error).toBe(errorMessage);
    expect(result.data).toBeUndefined();
  });
});

describe('formatVersion', () => {
  it('should add v prefix if not present', () => {
    expect(formatVersion('1.0')).toBe('v1.0');
    expect(formatVersion('1.1-beta')).toBe('v1.1-beta');
  });

  it('should not modify version if v prefix is already present', () => {
    expect(formatVersion('v1.0')).toBe('v1.0');
    expect(formatVersion('v1.1-beta')).toBe('v1.1-beta');
  });
});

describe('isDefaultVersion', () => {
  it('should return true if version matches default version', () => {
    expect(isDefaultVersion('1.0', '1.0')).toBe(true);
  });

  it('should return false if version does not match default version', () => {
    expect(isDefaultVersion('1.1', '1.0')).toBe(false);
  });

  it('should return false if default version is undefined', () => {
    expect(isDefaultVersion('1.0', undefined)).toBe(false);
  });
});