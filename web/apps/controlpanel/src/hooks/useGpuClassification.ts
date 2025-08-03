import { useMutation } from '@tanstack/react-query';
import { classifyGpu, MlPredictionResponse } from '@repo/client';

/**
 * Options for the useGpuClassification hook
 */
export interface UseGpuClassificationOptions {
  /**
   * Minimum confidence score (0.0-1.0) to consider a prediction valid
   */
  confidenceThreshold?: number;
  
  /**
   * Callback function to execute when classification is successful
   */
  onSuccess?: (data: MlPredictionResponse) => void;
  
  /**
   * Callback function to execute when classification fails
   */
  onError?: (error: Error) => void;
}

/**
 * Result returned by the useGpuClassification hook
 */
export interface UseGpuClassificationResult {
  /**
   * Function to trigger the classification
   */
  classify: (title: string) => void;
  
  /**
   * The classification result
   */
  data: MlPredictionResponse | undefined;
  
  /**
   * Whether the classification is in progress
   */
  isLoading: boolean;
  
  /**
   * Whether the classification failed
   */
  isError: boolean;
  
  /**
   * Error message if the classification failed
   */
  error: Error | null;
  
  /**
   * Whether the classification was successful
   */
  isSuccess: boolean;
  
  /**
   * Reset the mutation state
   */
  reset: () => void;
  
  /**
   * Format the confidence score as a percentage
   */
  formatConfidence: (score?: number) => string;
  
  /**
   * Check if the confidence score meets the threshold
   */
  meetsThreshold: (score?: number) => boolean;
}

/**
 * Format a confidence score as a percentage
 * 
 * @param score - The confidence score (0.0-1.0)
 * @returns The formatted percentage string
 */
export function formatConfidence(score?: number): string {
  if (score === undefined) return 'N/A';
  return `${(score * 100).toFixed(1)}%`;
}

/**
 * Check if a confidence score meets the threshold
 * 
 * @param score - The confidence score (0.0-1.0)
 * @param threshold - The threshold to check against (0.0-1.0)
 * @returns Whether the score meets the threshold
 */
export function meetsThreshold(score?: number, threshold = 0.5): boolean {
  if (score === undefined) return false;
  return score >= threshold;
}

/**
 * Hook for classifying whether a text description refers to a GPU
 * 
 * @param options - Options for the hook
 * @returns Object containing the classification function, result, and utility functions
 * 
 * @example
 * ```tsx
 * const { classify, data, isLoading, isError, error, formatConfidence, meetsThreshold } = useGpuClassification({
 *   confidenceThreshold: 0.7,
 *   onSuccess: (data) => console.log(`Classification result: ${data.mlIsGpu ? 'GPU' : 'Not GPU'}`),
 * });
 * 
 * // In a form submit handler
 * const handleSubmit = (e) => {
 *   e.preventDefault();
 *   classify(inputText);
 * };
 * 
 * // Display the result
 * return (
 *   <div>
 *     {isLoading && <div>Classifying...</div>}
 *     {isError && <div>Error: {error?.message}</div>}
 *     {data && (
 *       <div>
 *         <div>Is GPU: {data.mlIsGpu ? 'Yes' : 'No'}</div>
 *         <div>Confidence: {formatConfidence(data.mlScore)}</div>
 *         <div>Meets threshold: {meetsThreshold(data.mlScore, confidenceThreshold) ? 'Yes' : 'No'}</div>
 *       </div>
 *     )}
 *   </div>
 * );
 * ```
 */
export function useGpuClassification({
  confidenceThreshold = 0.5,
  onSuccess,
  onError,
}: UseGpuClassificationOptions = {}): UseGpuClassificationResult {
  const mutation = useMutation<MlPredictionResponse, Error, string>({
    mutationFn: (title: string) => classifyGpu(title),
    onSuccess,
    onError,
  });

  return {
    classify: (title: string) => mutation.mutate(title),
    data: mutation.data,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    isSuccess: mutation.isSuccess,
    reset: () => mutation.reset(),
    formatConfidence: (score?: number) => formatConfidence(score),
    meetsThreshold: (score?: number) => meetsThreshold(score, confidenceThreshold),
  };
}

export default useGpuClassification;