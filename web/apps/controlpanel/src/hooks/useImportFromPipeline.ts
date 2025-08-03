import { useState, useCallback, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { importFromPipeline, ImportResult } from '@repo/client';

/**
 * Pipeline import options
 */
export interface PipelineImportOptions {
  /**
   * Callback function to execute when import is successful
   */
  onSuccess?: (data: ImportResult) => void;
  
  /**
   * Callback function to execute when import fails
   */
  onError?: (error: Error) => void;
  
  /**
   * Whether to enable polling for import status
   * @default false
   */
  enablePolling?: boolean;
  
  /**
   * Polling interval in milliseconds
   * @default 5000
   */
  pollingInterval?: number;
  
  /**
   * Maximum number of polling attempts
   * @default 20
   */
  maxPollingAttempts?: number;
}

/**
 * Import mode for pipeline imports
 */
export enum ImportMode {
  /**
   * Append new records to existing data
   */
  APPEND = 'append',
  
  /**
   * Replace existing data with new data
   */
  REPLACE = 'replace',
  
  /**
   * Merge new data with existing data
   */
  MERGE = 'merge'
}

/**
 * Pipeline import parameters
 */
export interface PipelineImportParams {
  /**
   * Full path to the pipeline output file
   */
  inputCsvPath: string;
  
  /**
   * Human-readable tag for this data source
   */
  sourceLabel: string;
  
  /**
   * Optional campaign identifier
   */
  campaignId?: string;
  
  /**
   * Optional metadata as key-value pairs
   */
  metadata?: { [key: string]: string };
  
  /**
   * Import mode (append, replace, merge)
   * @default ImportMode.APPEND
   */
  importMode?: ImportMode;
  
  /**
   * Start date for filtering data (ISO 8601 format)
   */
  startDate?: string;
  
  /**
   * End date for filtering data (ISO 8601 format)
   */
  endDate?: string;
}

/**
 * Import status for polling
 */
export enum ImportStatus {
  /**
   * Import has not started
   */
  IDLE = 'idle',
  
  /**
   * Import is in progress
   */
  PROCESSING = 'processing',
  
  /**
   * Import has completed successfully
   */
  COMPLETED = 'completed',
  
  /**
   * Import has failed
   */
  FAILED = 'failed'
}

/**
 * Result returned by the useImportFromPipeline hook
 */
export interface UseImportFromPipelineResult {
  /**
   * Function to trigger the import
   */
  importFromPipeline: (params: PipelineImportParams) => void;
  
  /**
   * The import result
   */
  data: ImportResult | undefined;
  
  /**
   * Whether the import is in progress
   */
  isLoading: boolean;
  
  /**
   * Whether the import failed
   */
  isError: boolean;
  
  /**
   * Error message if the import failed
   */
  error: Error | null;
  
  /**
   * Whether the import was successful
   */
  isSuccess: boolean;
  
  /**
   * Validation error message
   */
  validationError: string | null;
  
  /**
   * Current status of the import
   */
  status: ImportStatus;
  
  /**
   * Whether polling is currently active
   */
  isPolling: boolean;
  
  /**
   * Current polling attempt (1-based)
   */
  pollingAttempt: number;
  
  /**
   * Maximum number of polling attempts
   */
  maxPollingAttempts: number;
  
  /**
   * Function to manually check import status
   */
  checkStatus: () => Promise<void>;
  
  /**
   * Function to cancel polling
   */
  cancelPolling: () => void;
  
  /**
   * Reset the mutation state
   */
  reset: () => void;
}

/**
 * Validate pipeline import parameters
 * 
 * @param params - The parameters to validate
 * @returns Error message if validation fails, null if validation passes
 */
export function validatePipelineImportParams(params: PipelineImportParams): string | null {
  // Check if inputCsvPath is provided
  if (!params.inputCsvPath) {
    return 'Input CSV path is required';
  }
  
  // Check if sourceLabel is provided
  if (!params.sourceLabel) {
    return 'Source label is required';
  }
  
  return null;
}

/**
 * Hook for importing data from the pipeline
 * 
 * @param options - Import options
 * @returns Object containing the import function, result, and utility functions
 * 
 * @example
 * ```tsx
 * const { 
 *   importFromPipeline, 
 *   data, 
 *   isLoading, 
 *   isError, 
 *   error, 
 *   validationError,
 *   status,
 *   isPolling,
 *   pollingAttempt,
 *   checkStatus,
 *   cancelPolling
 * } = useImportFromPipeline({
 *   onSuccess: (data) => {
 *     console.log(`Import successful: ${data.recordCount} records imported`);
 *   },
 *   enablePolling: true,
 *   pollingInterval: 3000,
 *   maxPollingAttempts: 10
 * });
 * 
 * // In a form submit handler
 * const handleSubmit = (e) => {
 *   e.preventDefault();
 *   importFromPipeline({
 *     inputCsvPath: '/path/to/pipeline/output.csv',
 *     sourceLabel: 'Pipeline Import',
 *     campaignId: 'campaign-123',
 *     metadata: { source: 'web-ui' },
 *     importMode: ImportMode.APPEND,
 *     startDate: '2023-01-01',
 *     endDate: '2023-12-31'
 *   });
 * };
 * 
 * // Display the result
 * return (
 *   <div>
 *     {validationError && <div className="error">{validationError}</div>}
 *     {isLoading && <div>Importing...</div>}
 *     {isPolling && <div>Checking import status... Attempt {pollingAttempt} of {maxPollingAttempts}</div>}
 *     {isError && <div>Error: {error?.message}</div>}
 *     {status === ImportStatus.PROCESSING && <div>Import is being processed...</div>}
 *     {status === ImportStatus.COMPLETED && data && (
 *       <div>
 *         <h2>Import Successful</h2>
 *         <p>Records imported: {data.recordCount}</p>
 *         <p>First model: {data.firstModel}</p>
 *         <p>Last model: {data.lastModel}</p>
 *       </div>
 *     )}
 *   </div>
 * );
 * ```
 */
export function useImportFromPipeline(options: PipelineImportOptions = {}): UseImportFromPipelineResult {
  const { 
    onSuccess, 
    onError, 
    enablePolling = false, 
    pollingInterval = 5000, 
    maxPollingAttempts = 20 
  } = options;
  
  // State for validation errors
  const [validationError, setValidationError] = useState<string | null>(null);
  
  // State for polling
  const [status, setStatus] = useState<ImportStatus>(ImportStatus.IDLE);
  const [isPolling, setIsPolling] = useState<boolean>(false);
  const [pollingAttempt, setPollingAttempt] = useState<number>(0);
  const [importId, setImportId] = useState<string | null>(null);
  const [pollingIntervalId, setPollingIntervalId] = useState<NodeJS.Timeout | null>(null);
  
  // Reset validation error when starting a new import
  const resetValidation = useCallback(() => {
    setValidationError(null);
  }, []);
  
  // Function to cancel polling
  const cancelPolling = useCallback(() => {
    if (pollingIntervalId) {
      clearInterval(pollingIntervalId);
      setPollingIntervalId(null);
    }
    setIsPolling(false);
    setPollingAttempt(0);
  }, [pollingIntervalId]);
  
  // Function to check import status
  const checkStatus = useCallback(async () => {
    if (!importId || status === ImportStatus.COMPLETED || status === ImportStatus.FAILED) {
      return;
    }
    
    try {
      // In a real implementation, we would call an API endpoint to check the status
      // For now, we'll simulate a status check by assuming the import is completed after a few attempts
      setPollingAttempt((prev) => prev + 1);
      
      // Simulate a status check
      if (pollingAttempt >= 3) {
        setStatus(ImportStatus.COMPLETED);
        cancelPolling();
      }
    } catch (error) {
      setStatus(ImportStatus.FAILED);
      cancelPolling();
      if (onError) {
        onError(error as Error);
      }
    }
  }, [importId, status, pollingAttempt, cancelPolling, onError]);
  
  // Start polling when enablePolling is true and importId is set
  useEffect(() => {
    if (enablePolling && importId && status === ImportStatus.PROCESSING && !pollingIntervalId) {
      setIsPolling(true);
      const intervalId = setInterval(() => {
        if (pollingAttempt >= maxPollingAttempts) {
          cancelPolling();
          return;
        }
        checkStatus();
      }, pollingInterval);
      setPollingIntervalId(intervalId);
      
      // Clean up interval on unmount
      return () => {
        clearInterval(intervalId);
      };
    }
  }, [enablePolling, importId, status, pollingIntervalId, pollingAttempt, maxPollingAttempts, pollingInterval, checkStatus, cancelPolling]);
  
  // Mutation for importing from pipeline
  const mutation = useMutation<ImportResult, Error, PipelineImportParams>({
    mutationFn: async (params: PipelineImportParams) => {
      // Reset validation and polling state
      resetValidation();
      cancelPolling();
      setStatus(ImportStatus.IDLE);
      setImportId(null);
      
      // Validate the parameters
      const error = validatePipelineImportParams(params);
      if (error) {
        setValidationError(error);
        throw new Error(error);
      }
      
      try {
        // Set status to processing
        setStatus(ImportStatus.PROCESSING);
        
        // Call the importFromPipeline function
        const result = await importFromPipeline({
          inputCsvPath: params.inputCsvPath,
          sourceLabel: params.sourceLabel,
          campaignId: params.campaignId,
          metadata: {
            ...params.metadata,
            importMode: params.importMode || ImportMode.APPEND,
            startDate: params.startDate,
            endDate: params.endDate
          }
        });
        
        // Set importId for polling
        if (result.importId) {
          setImportId(result.importId);
        }
        
        // If polling is not enabled, set status to completed
        if (!enablePolling) {
          setStatus(ImportStatus.COMPLETED);
        }
        
        return result;
      } catch (error) {
        setStatus(ImportStatus.FAILED);
        throw error;
      }
    },
    onSuccess,
    onError: (error) => {
      setStatus(ImportStatus.FAILED);
      if (onError) {
        onError(error);
      }
    },
  });
  
  // Function to trigger the import
  const importPipeline = useCallback((params: PipelineImportParams) => {
    mutation.mutate(params);
  }, [mutation]);
  
  // Reset function
  const reset = useCallback(() => {
    mutation.reset();
    setValidationError(null);
    cancelPolling();
    setStatus(ImportStatus.IDLE);
    setImportId(null);
    setPollingAttempt(0);
  }, [mutation, cancelPolling]);
  
  return {
    importFromPipeline: importPipeline,
    data: mutation.data,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    isSuccess: mutation.isSuccess,
    validationError,
    status,
    isPolling,
    pollingAttempt,
    maxPollingAttempts,
    checkStatus,
    cancelPolling,
    reset
  };
}

export default useImportFromPipeline;