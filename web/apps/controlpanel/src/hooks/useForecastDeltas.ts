import { useQuery } from '@tanstack/react-query';
import { getForecastDeltas, getForecastDeltaById } from '@repo/client';

/**
 * Interface representing a forecast delta item
 */
export interface ForecastDelta {
  id: number;
  model: string;
  oldPrice: number;
  newPrice: number;
  priceChangePct: number;
  region?: string;
  timestamp: string;
  listingId: string;
  source?: string;
}

/**
 * Parameters for the useForecastDeltas hook
 */
export interface UseForecastDeltasParams {
  /**
   * Filter by GPU model name
   */
  model?: string;
  
  /**
   * Filter by minimum price change percentage
   */
  minPriceChangePct?: number;
  
  /**
   * Filter by changes after this date
   */
  after?: Date;
  
  /**
   * Filter by region
   */
  region?: string;
  
  /**
   * Number of items to return
   */
  limit?: number;
}

/**
 * Result returned by the useForecastDeltas hook
 */
export interface UseForecastDeltasResult {
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
   * Function to refetch the data
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
 * Calculate percentage change between two values
 * 
 * @param oldValue - The original value
 * @param newValue - The new value
 * @returns The percentage change (positive for increase, negative for decrease)
 */
export function calculatePercentChange(oldValue: number, newValue: number): number {
  if (oldValue === 0) return 0; // Avoid division by zero
  return ((newValue - oldValue) / Math.abs(oldValue)) * 100;
}

/**
 * Format percentage change for display
 * 
 * @param percentChange - The percentage change value
 * @returns Formatted string with + or - sign and 2 decimal places
 */
export function formatPercentChange(percentChange: number): string {
  const sign = percentChange >= 0 ? '+' : '';
  return `${sign}${percentChange.toFixed(2)}%`;
}

/**
 * Hook to fetch GPU price forecast deltas with filtering
 * 
 * @param params - Parameters for filtering
 * @returns Object containing the forecast deltas data, loading state, error state, refetch function, and utility functions
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error, formatPercentChange } = useForecastDeltas({
 *   model: 'RTX 4090',
 *   minPriceChangePct: 5,
 *   after: new Date('2023-01-01'),
 *   region: 'US',
 *   limit: 10,
 * });
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data || data.length === 0) return <div>No forecast deltas found</div>;
 * 
 * return (
 *   <div>
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
export function useForecastDeltas({
  model,
  minPriceChangePct,
  after,
  region,
  limit = 10,
}: UseForecastDeltasParams = {}): UseForecastDeltasResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<ForecastDelta[], Error>({
    queryKey: ['forecastDeltas', model, minPriceChangePct, after?.toISOString(), region, limit],
    queryFn: () => getForecastDeltas({
      model,
      minPriceChangePct,
      after,
      region,
      limit,
    }),
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
    calculatePercentChange,
    formatPercentChange,
  };
}

/**
 * Hook to fetch a specific forecast delta by ID
 * 
 * @param deltaId - The ID of the forecast delta to fetch
 * @returns Object containing the forecast delta data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useForecastDeltaById(123);
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data) return <div>Forecast delta not found</div>;
 * 
 * return (
 *   <div>
 *     <h1>{data.model}</h1>
 *     <p>Price Change: {formatPercentChange(data.priceChangePct)}</p>
 *     <p>Region: {data.region}</p>
 *   </div>
 * );
 * ```
 */
export function useForecastDeltaById(deltaId: number) {
  const result = useQuery<ForecastDelta, Error>({
    queryKey: ['forecastDelta', deltaId],
    queryFn: () => getForecastDeltaById(deltaId),
    enabled: !!deltaId, // Only run the query if a deltaId is provided
  });
  
  return {
    ...result,
    error: result.error ? result.error.message : null,
    calculatePercentChange,
    formatPercentChange,
  };
}

export default useForecastDeltas;