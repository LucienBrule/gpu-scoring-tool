import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { importCsv, ImportResultDTO } from '@repo/client';

/**
 * CSV import options
 */
export interface CsvImportOptions {
  /**
   * Maximum file size in bytes (default: 10MB)
   */
  maxSize?: number;
  
  /**
   * Allowed file types (default: ['.csv'])
   */
  allowedTypes?: string[];
  
  /**
   * Callback function to execute when import is successful
   */
  onSuccess?: (data: ImportResultDTO) => void;
  
  /**
   * Callback function to execute when import fails
   */
  onError?: (error: Error) => void;
}

/**
 * Result returned by the useImportCsv hook
 */
export interface UseImportCsvResult {
  /**
   * Function to trigger the import
   */
  importFile: (file: File) => void;
  
  /**
   * The import result
   */
  data: ImportResultDTO | undefined;
  
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
   * Upload progress (0-100)
   */
  progress: number;
  
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
 * Validate a file for CSV import
 * 
 * @param file - The file to validate
 * @param options - Validation options
 * @returns Error message if validation fails, null if validation passes
 */
export function validateCsvFile(
  file: File,
  options: { maxSize?: number; allowedTypes?: string[] } = {}
): string | null {
  const { maxSize = 10 * 1024 * 1024, allowedTypes = ['.csv'] } = options;
  
  // Check if file is provided
  if (!file) {
    return 'No file selected';
  }
  
  // Check file size
  if (file.size > maxSize) {
    return `File size exceeds the maximum allowed size (${Math.round(maxSize / 1024 / 1024)}MB)`;
  }
  
  // Check file type
  const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
  if (!allowedTypes.includes(fileExtension)) {
    return `File type not supported. Allowed types: ${allowedTypes.join(', ')}`;
  }
  
  return null;
}

/**
 * Hook for importing CSV files
 * 
 * @param options - Import options
 * @returns Object containing the import function, result, and utility functions
 * 
 * @example
 * ```tsx
 * const { importFile, data, isLoading, isError, error, progress, validationError } = useImportCsv({
 *   maxSize: 5 * 1024 * 1024, // 5MB
 *   allowedTypes: ['.csv'],
 *   onSuccess: (data) => {
 *     console.log(`Import successful: ${data.recordCount} records imported`);
 *   },
 * });
 * 
 * // In a form submit handler
 * const handleSubmit = (e) => {
 *   e.preventDefault();
 *   if (fileInputRef.current?.files?.[0]) {
 *     importFile(fileInputRef.current.files[0]);
 *   }
 * };
 * 
 * // Display the result
 * return (
 *   <div>
 *     {validationError && <div className="error">{validationError}</div>}
 *     {isLoading && <div>Uploading... {progress}%</div>}
 *     {isError && <div>Error: {error?.message}</div>}
 *     {data && (
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
export function useImportCsv(options: CsvImportOptions = {}): UseImportCsvResult {
  const { maxSize, allowedTypes, onSuccess, onError } = options;
  
  // State for tracking upload progress
  const [progress, setProgress] = useState<number>(0);
  
  // State for validation errors
  const [validationError, setValidationError] = useState<string | null>(null);
  
  // Reset validation error when starting a new upload
  const resetValidation = useCallback(() => {
    setValidationError(null);
  }, []);
  
  // Mutation for importing CSV files
  const mutation = useMutation<ImportResultDTO, Error, File>({
    mutationFn: async (file: File) => {
      // Reset validation and progress
      resetValidation();
      setProgress(0);
      
      // Validate the file
      const error = validateCsvFile(file, { maxSize, allowedTypes });
      if (error) {
        setValidationError(error);
        throw new Error(error);
      }
      
      try {
        // Create a blob from the file
        const blob = new Blob([file], { type: file.type });
        
        // If XMLHttpRequest is available, use it to track progress
        if (typeof XMLHttpRequest !== 'undefined') {
          return new Promise<ImportResultDTO>((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            // Track upload progress
            xhr.upload.addEventListener('progress', (event) => {
              if (event.lengthComputable) {
                const progressPercent = Math.round((event.loaded / event.total) * 100);
                setProgress(progressPercent);
              }
            });
            
            // Handle completion
            xhr.addEventListener('load', () => {
              if (xhr.status >= 200 && xhr.status < 300) {
                try {
                  const result = JSON.parse(xhr.responseText);
                  resolve(result);
                } catch (error) {
                  reject(new Error('Failed to parse response'));
                }
              } else {
                reject(new Error(`HTTP error ${xhr.status}: ${xhr.statusText}`));
              }
            });
            
            // Handle errors
            xhr.addEventListener('error', () => {
              reject(new Error('Network error occurred'));
            });
            
            xhr.addEventListener('abort', () => {
              reject(new Error('Upload aborted'));
            });
            
            // Prepare and send the request
            xhr.open('POST', '/api/import/csv');
            
            const formData = new FormData();
            formData.append('file', file);
            
            xhr.send(formData);
          });
        } else {
          // Fallback to regular fetch if XMLHttpRequest is not available
          // This won't have progress tracking
          setProgress(50); // Set to 50% as a placeholder
          const result = await importCsv(blob);
          setProgress(100);
          return result;
        }
      } catch (error) {
        // Reset progress on error
        setProgress(0);
        throw error;
      }
    },
    onSuccess,
    onError,
  });
  
  // Function to trigger the import
  const importFile = useCallback((file: File) => {
    mutation.mutate(file);
  }, [mutation]);
  
  return {
    importFile,
    data: mutation.data,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    isSuccess: mutation.isSuccess,
    progress,
    validationError,
    reset: () => {
      mutation.reset();
      setProgress(0);
      setValidationError(null);
    },
  };
}

export default useImportCsv;