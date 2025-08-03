import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { validateArtifact, ArtifactValidationResult } from '@repo/client';

/**
 * Artifact validation options
 */
export interface ArtifactValidationOptions {
  /**
   * Maximum file size in bytes (default: 10MB)
   */
  maxSize?: number;
  
  /**
   * Allowed file types (default: ['.csv', '.json', '.yaml', '.yml'])
   */
  allowedTypes?: string[];
  
  /**
   * Whether to save the artifact to disk for debugging (default: false)
   */
  saveToDisk?: boolean;
  
  /**
   * Callback function to execute when validation is successful
   */
  onSuccess?: (data: ArtifactValidationResult) => void;
  
  /**
   * Callback function to execute when validation fails
   */
  onError?: (error: Error) => void;
}

/**
 * Result returned by the useValidateArtifact hook
 */
export interface UseValidateArtifactResult {
  /**
   * Function to trigger the validation
   */
  validateFile: (file: File) => void;
  
  /**
   * The validation result
   */
  data: ArtifactValidationResult | undefined;
  
  /**
   * Whether the validation is in progress
   */
  isLoading: boolean;
  
  /**
   * Whether the validation failed
   */
  isError: boolean;
  
  /**
   * Error message if the validation failed
   */
  error: Error | null;
  
  /**
   * Whether the validation was successful
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
 * Validate a file for artifact validation
 * 
 * @param file - The file to validate
 * @param options - Validation options
 * @returns Error message if validation fails, null if validation passes
 */
export function validateFile(
  file: File,
  options: { maxSize?: number; allowedTypes?: string[] } = {}
): string | null {
  const { 
    maxSize = 10 * 1024 * 1024, 
    allowedTypes = ['.csv', '.json', '.yaml', '.yml'] 
  } = options;
  
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
 * Hook for validating data artifacts
 * 
 * @param options - Validation options
 * @returns Object containing the validation function, result, and utility functions
 * 
 * @example
 * ```tsx
 * const { validateFile, data, isLoading, isError, error, progress, validationError } = useValidateArtifact({
 *   maxSize: 5 * 1024 * 1024, // 5MB
 *   allowedTypes: ['.csv', '.json'],
 *   saveToDisk: true,
 *   onSuccess: (data) => {
 *     console.log(`Validation successful: ${data.valid ? 'Valid' : 'Invalid'} ${data.type}`);
 *   },
 * });
 * 
 * // In a form submit handler
 * const handleSubmit = (e) => {
 *   e.preventDefault();
 *   if (fileInputRef.current?.files?.[0]) {
 *     validateFile(fileInputRef.current.files[0]);
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
 *         <h2>Validation {data.valid ? 'Successful' : 'Failed'}</h2>
 *         <p>Type: {data.type}</p>
 *         <p>Schema Version: {data.schemaVersion}</p>
 *         {data.rows && <p>Rows: {data.rows}</p>}
 *         {data.warnings && data.warnings.length > 0 && (
 *           <div>
 *             <h3>Warnings:</h3>
 *             <ul>
 *               {data.warnings.map((warning, index) => (
 *                 <li key={index}>{warning}</li>
 *               ))}
 *             </ul>
 *           </div>
 *         )}
 *         {data.errors && data.errors.length > 0 && (
 *           <div>
 *             <h3>Errors:</h3>
 *             <ul>
 *               {data.errors.map((error, index) => (
 *                 <li key={index}>{error}</li>
 *               ))}
 *             </ul>
 *           </div>
 *         )}
 *       </div>
 *     )}
 *   </div>
 * );
 * ```
 */
export function useValidateArtifact(options: ArtifactValidationOptions = {}): UseValidateArtifactResult {
  const { maxSize, allowedTypes, saveToDisk = false, onSuccess, onError } = options;
  
  // State for tracking upload progress
  const [progress, setProgress] = useState<number>(0);
  
  // State for validation errors
  const [validationError, setValidationError] = useState<string | null>(null);
  
  // Reset validation error when starting a new upload
  const resetValidation = useCallback(() => {
    setValidationError(null);
  }, []);
  
  // Mutation for validating artifacts
  const mutation = useMutation<ArtifactValidationResult, Error, File>({
    mutationFn: async (file: File) => {
      // Reset validation and progress
      resetValidation();
      setProgress(0);
      
      // Validate the file
      const error = validateFile(file, { maxSize, allowedTypes });
      if (error) {
        setValidationError(error);
        throw new Error(error);
      }
      
      try {
        // Create a blob from the file
        const blob = new Blob([file], { type: file.type });
        
        // If XMLHttpRequest is available, use it to track progress
        if (typeof XMLHttpRequest !== 'undefined') {
          return new Promise<ArtifactValidationResult>((resolve, reject) => {
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
            xhr.open('POST', '/api/ingest/upload-artifact');
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('save_to_disk', saveToDisk.toString());
            
            xhr.send(formData);
          });
        } else {
          // Fallback to regular fetch if XMLHttpRequest is not available
          // This won't have progress tracking
          setProgress(50); // Set to 50% as a placeholder
          const result = await validateArtifact(blob, saveToDisk);
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
  
  // Function to trigger the validation
  const validateFileFunc = useCallback((file: File) => {
    mutation.mutate(file);
  }, [mutation]);
  
  return {
    validateFile: validateFileFunc,
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

export default useValidateArtifact;