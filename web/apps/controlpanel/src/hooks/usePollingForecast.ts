import { useQuery } from '@tanstack/react-query';
import { getForecastDeltas } from '@repo/client';
import { ForecastDelta, calculatePercentChange, formatPercentChange } from './useForecastDeltas';

/**
 * Parameters for the usePollingForecast hook
 */
export interface UsePollingForecastParams {
  /**
   * Filter by GPU model name
   */
  model?: string;
  
  /**
   * Filter by region
   */
  region?: string;
  
  /**
   * Number of items to return
   */
  limit?: number;

  /**
   * Polling interval in milliseconds (defaults to 60000ms / 1 minute)
   */
  intervalMs?: number;
}

/**
 * Result returned by the usePollingForecast hook
 */
export interface UsePollingForecastResult {
  /**
   * The forecast deltas data
   */
  data: ForecastDelta[] | undefined;
  
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
   * Whether the data is currently being fetched (initial or background)
   */
  isFetching: boolean;
  
  /**
   * Function to manually refetch the data
   */
  refetch: () => void;
  
  /**
   * Calculate percentage change between two values
   */
  calculatePercentChange: (oldValue: number, newValue: number) => number;
  
  /**
   * Format percentage change for display
   */
  formatPercentChange: (percentChange: number) => string;
}

/**
 * Hook to fetch GPU price forecast deltas with automatic polling at a configurable interval
 * 
 * @param params - Parameters for filtering and polling configuration
 * @returns Object containing the forecast deltas data, loading states, error state, refetch function, and utility functions
 * 
 * @example
 * ```tsx
 * // Basic usage with default 1-minute polling interval
 * const { data, isLoading, isError, error } = usePollingForecast();
 * 
 * // With filters and custom 30-second polling interval
 * const { data, isLoading, isError, isFetching } = usePollingForecast({
 *   model: 'RTX 4090',
 *   region: 'US',
 *   limit: 10,
 *   intervalMs: 30000, // 30 seconds
 * });
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data || data.length === 0) return <div>No forecast deltas found</div>;
 * 
 * return (
 *   <div>
 *     {isFetching && <div>Refreshing...</div>}
 *     {data.map(delta => (
 *       <div key={delta.id}>
 *         <h2>{delta.model}</h2>
 *         <p>Price Change: {formatPercentChange(delta.priceChangePct)}</p>
 *       </div>
 *     ))}
 *   </div>
 * );
 * ```
 */
export function usePollingForecast({
  model,
  region,
  limit = 10,
  intervalMs = 60000, // Default to 1 minute polling
}: UsePollingForecastParams = {}): UsePollingForecastResult {
  const {
    data,
    isLoading,
    isError,
    error,
    isFetching,
    refetch,
  } = useQuery<ForecastDelta[], Error>({
    queryKey: ['forecast-deltas', { model, region, limit }],
    queryFn: () => getForecastDeltas({
      model,
      region,
      limit,
    }),
    refetchInterval: intervalMs, // Enable polling with the specified interval
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    isFetching,
    refetch,
    calculatePercentChange,
    formatPercentChange,
  };
}

export default usePollingForecast;