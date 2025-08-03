import { useQuery } from '@tanstack/react-query';
import { getSchemaVersions, getSchemaVersionDetails } from '@repo/client';
import type { SchemaVersionInfo, SchemaVersion } from '@repo/client';

/**
 * Result returned by the useSchemaVersions hook
 */
export interface UseSchemaVersionsResult {
  /**
   * The schema versions information
   */
  data: SchemaVersionInfo | undefined;
  
  /**
   * Whether the data is currently loading
   */
  isLoading: boolean;
  
  /**
   * Whether an error occurred
   */
  isError: boolean;
  
  /**
   * Error message if an error occurred
   */
  error: string | null;
  
  /**
   * Function to refetch the data
   */
  refetch: () => void;
  
  /**
   * Check if a version is the current default
   */
  isDefaultVersion: (version: string) => boolean;
  
  /**
   * Format a version string for display
   */
  formatVersion: (version: string) => string;
}

/**
 * Result returned by the useSchemaVersionDetails hook
 */
export interface UseSchemaVersionDetailsResult {
  /**
   * The schema version details
   */
  data: SchemaVersion | undefined;
  
  /**
   * Whether the data is currently loading
   */
  isLoading: boolean;
  
  /**
   * Whether an error occurred
   */
  isError: boolean;
  
  /**
   * Error message if an error occurred
   */
  error: string | null;
  
  /**
   * Function to refetch the data
   */
  refetch: () => void;
}

/**
 * Format a version string for display
 * 
 * @param version - The version string to format
 * @returns The formatted version string
 */
export function formatVersion(version: string): string {
  // Add 'v' prefix if not present
  if (!version.startsWith('v')) {
    return `v${version}`;
  }
  return version;
}

/**
 * Check if a version is the current default
 * 
 * @param version - The version to check
 * @param defaultVersion - The default version
 * @returns Whether the version is the default
 */
export function isDefaultVersion(version: string, defaultVersion?: string): boolean {
  if (!defaultVersion) return false;
  return version === defaultVersion;
}

/**
 * Hook to fetch all supported schema versions
 * 
 * @returns Object containing the schema versions data, loading state, error state, and utility functions
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error, isDefaultVersion, formatVersion } = useSchemaVersions();
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data) return <div>No schema versions found</div>;
 * 
 * return (
 *   <div>
 *     <h2>Default Version: {formatVersion(data.defaultVersion)}</h2>
 *     <h3>Supported Versions:</h3>
 *     <ul>
 *       {data.supportedVersions.map(version => (
 *         <li key={version}>
 *           {formatVersion(version)}
 *           {isDefaultVersion(version, data.defaultVersion) && ' (Default)'}
 *         </li>
 *       ))}
 *     </ul>
 *   </div>
 * );
 * ```
 */
export function useSchemaVersions(): UseSchemaVersionsResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<SchemaVersionInfo, Error>({
    queryKey: ['schemaVersions'],
    queryFn: () => getSchemaVersions(),
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
    isDefaultVersion: (version: string) => isDefaultVersion(version, data?.defaultVersion),
    formatVersion,
  };
}

/**
 * Hook to fetch details for a specific schema version
 * 
 * @param version - The version to fetch details for
 * @returns Object containing the schema version details, loading state, and error state
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useSchemaVersionDetails('1.0');
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data) return <div>Version details not found</div>;
 * 
 * return (
 *   <div>
 *     <h2>Version: {data.version}</h2>
 *     <p>Released: {new Date(data.releaseDate).toLocaleDateString()}</p>
 *     <h3>Schema:</h3>
 *     <pre>{JSON.stringify(data.schema, null, 2)}</pre>
 *   </div>
 * );
 * ```
 */
export function useSchemaVersionDetails(version: string): UseSchemaVersionDetailsResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<SchemaVersion, Error>({
    queryKey: ['schemaVersion', version],
    queryFn: () => getSchemaVersionDetails(version),
    enabled: !!version, // Only run the query if a version is provided
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
  };
}

/**
 * Result returned by the useSchemaInfo hook
 */
export interface UseSchemaInfoResult {
  /**
   * The schema versions information
   */
  data: SchemaVersionInfo | undefined;
  
  /**
   * Whether the data is currently loading
   */
  isLoading: boolean;
  
  /**
   * Whether an error occurred
   */
  isError: boolean;
  
  /**
   * Error message if an error occurred
   */
  error: string | null;
  
  /**
   * Function to refetch the data
   */
  refetch: () => void;
}

/**
 * Hook to fetch schema information
 * 
 * This is a convenience hook that wraps useSchemaVersions for use in the dev-harness page.
 * 
 * @returns Object containing the schema versions data, loading state, error state, and refetch function
 */
export function useSchemaInfo(): UseSchemaInfoResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useSchemaVersions();

  return {
    data,
    isLoading,
    isError,
    error,
    refetch,
  };
}
