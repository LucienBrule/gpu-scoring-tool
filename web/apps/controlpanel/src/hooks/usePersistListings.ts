import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { persistListings, GpuListing, ImportResult } from '@repo/client';

/**
 * Persistence mode options
 */
export enum PersistenceMode {
  /**
   * Create new records only
   */
  CREATE = 'create',
  
  /**
   * Update existing records only
   */
  UPDATE = 'update',
  
  /**
   * Create or update records as needed
   */
  UPSERT = 'upsert'
}

/**
 * Conflict resolution strategy
 */
export enum ConflictResolution {
  /**
   * Skip conflicting records
   */
  SKIP = 'skip',
  
  /**
   * Overwrite conflicting records
   */
  OVERWRITE = 'overwrite',
  
  /**
   * Merge conflicting records
   */
  MERGE = 'merge'
}

/**
 * Options for the usePersistListings hook
 */
export interface PersistListingsOptions {
  /**
   * Callback function to execute when persistence is successful
   */
  onSuccess?: (data: ImportResult) => void;
  
  /**
   * Callback function to execute when persistence fails
   */
  onError?: (error: Error) => void;
  
  /**
   * Default persistence mode
   * @default PersistenceMode.UPSERT
   */
  defaultMode?: PersistenceMode;
  
  /**
   * Default conflict resolution strategy
   * @default ConflictResolution.OVERWRITE
   */
  defaultConflictResolution?: ConflictResolution;
  
  /**
   * Default batch size for large operations
   * @default 100
   */
  defaultBatchSize?: number;
}

/**
 * Parameters for persisting listings
 */
export interface PersistListingsParams {
  /**
   * Array of GPU listings to persist
   */
  listings: GpuListing[];
  
  /**
   * Persistence mode (create, update, upsert)
   */
  mode?: PersistenceMode;
  
  /**
   * Conflict resolution strategy
   */
  conflictResolution?: ConflictResolution;
  
  /**
   * Batch size for large operations
   */
  batchSize?: number;
}

/**
 * Result returned by the usePersistListings hook
 */
export interface UsePersistListingsResult {
  /**
   * Function to trigger the persistence operation
   */
  persistListings: (params: PersistListingsParams) => void;
  
  /**
   * The persistence result
   */
  data: ImportResult | undefined;
  
  /**
   * Whether the persistence operation is in progress
   */
  isLoading: boolean;
  
  /**
   * Whether the persistence operation failed
   */
  isError: boolean;
  
  /**
   * Error message if the persistence operation failed
   */
  error: Error | null;
  
  /**
   * Whether the persistence operation was successful
   */
  isSuccess: boolean;
  
  /**
   * Validation error message
   */
  validationError: string | null;
  
  /**
   * Reset the mutation state
   */
  reset: () => void;
}

/**
 * Validate listings before persistence
 * 
 * @param params - The parameters to validate
 * @returns Error message if validation fails, null if validation passes
 */
export function validateListings(params: PersistListingsParams): string | null {
  // Check if listings array is provided
  if (!params.listings || !Array.isArray(params.listings)) {
    return 'Listings array is required';
  }
  
  // Check if listings array is empty
  if (params.listings.length === 0) {
    return 'Listings array cannot be empty';
  }
  
  // Check if all listings have required fields
  for (let i = 0; i < params.listings.length; i++) {
    const listing = params.listings[i];
    if (!listing.canonicalModel) {
      return `Listing at index ${i} is missing required field: canonicalModel`;
    }
    if (listing.price === undefined || listing.price === null) {
      return `Listing at index ${i} is missing required field: price`;
    }
  }
  
  return null;
}

/**
 * Hook for persisting GPU listings
 * 
 * @param options - Persistence options
 * @returns Object containing the persist function, result, and utility functions
 * 
 * @example
 * ```tsx
 * const { 
 *   persistListings, 
 *   data, 
 *   isLoading, 
 *   isError, 
 *   error, 
 *   validationError 
 * } = usePersistListings({
 *   onSuccess: (data) => {
 *     console.log(`Persistence successful: ${data.recordCount} records persisted`);
 *   },
 *   defaultMode: PersistenceMode.UPSERT,
 *   defaultConflictResolution: ConflictResolution.OVERWRITE,
 *   defaultBatchSize: 100
 * });
 * 
 * // In a form submit handler
 * const handleSubmit = (e) => {
 *   e.preventDefault();
 *   persistListings({
 *     listings: myListings,
 *     mode: PersistenceMode.CREATE,
 *     conflictResolution: ConflictResolution.SKIP,
 *     batchSize: 50
 *   });
 * };
 * 
 * // Display the result
 * return (
 *   <div>
 *     {validationError && <div className="error">{validationError}</div>}
 *     {isLoading && <div>Persisting listings...</div>}
 *     {isError && <div>Error: {error?.message}</div>}
 *     {data && (
 *       <div>
 *         <h2>Persistence Successful</h2>
 *         <p>Records persisted: {data.recordCount}</p>
 *         <p>First model: {data.firstModel}</p>
 *         <p>Last model: {data.lastModel}</p>
 *       </div>
 *     )}
 *   </div>
 * );
 * ```
 */
export function usePersistListings(options: PersistListingsOptions = {}): UsePersistListingsResult {
  const { 
    onSuccess, 
    onError, 
    defaultMode = PersistenceMode.UPSERT, 
    defaultConflictResolution = ConflictResolution.OVERWRITE, 
    defaultBatchSize = 100 
  } = options;
  
  // State for validation errors
  const [validationError, setValidationError] = useState<string | null>(null);
  
  // Reset validation error when starting a new persistence operation
  const resetValidation = useCallback(() => {
    setValidationError(null);
  }, []);
  
  // Mutation for persisting listings
  const mutation = useMutation<ImportResult, Error, PersistListingsParams>({
    mutationFn: async (params: PersistListingsParams) => {
      // Reset validation
      resetValidation();
      
      // Validate the parameters
      const error = validateListings(params);
      if (error) {
        setValidationError(error);
        throw new Error(error);
      }
      
      try {
        // Call the persistListings function
        return await persistListings(
          params.listings,
          {
            mode: params.mode || defaultMode,
            conflictResolution: params.conflictResolution || defaultConflictResolution,
            batchSize: params.batchSize || defaultBatchSize,
          }
        );
      } catch (error) {
        throw error;
      }
    },
    onSuccess,
    onError,
  });
  
  // Function to trigger the persistence operation
  const persist = useCallback((params: PersistListingsParams) => {
    mutation.mutate(params);
  }, [mutation]);
  
  return {
    persistListings: persist,
    data: mutation.data,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    isSuccess: mutation.isSuccess,
    validationError,
    reset: () => {
      mutation.reset();
      setValidationError(null);
    },
  };
}

export default usePersistListings;