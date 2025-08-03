import { useQuery } from '@tanstack/react-query';
import { getListings } from '@repo/client';
import type { GpuListing } from '@repo/client';

/**
 * Parameters for the useListings hook
 */
export interface UseListingsParams {
  page: number;
  pageSize: number;
  fromDate?: string; // ISO 8601 format (YYYY-MM-DD)
  toDate?: string; // ISO 8601 format (YYYY-MM-DD)
  model?: string;
  minPrice?: number;
  maxPrice?: number;
}

/**
 * Result returned by the useListings hook
 */
export interface UseListingsResult {
  data: GpuListing[] | undefined;
  isLoading: boolean;
  isError: boolean;
  error: string | null;
  refetch: () => void;
}

/**
 * Hook to fetch GPU listings with pagination and date filtering
 * 
 * @param params - Parameters for filtering and pagination
 * @param params.page - Page number (1-based)
 * @param params.pageSize - Number of items per page
 * @param params.fromDate - Optional start date filter (ISO 8601 format: YYYY-MM-DD)
 * @param params.toDate - Optional end date filter (ISO 8601 format: YYYY-MM-DD)
 * @param params.model - Optional model filter
 * @param params.minPrice - Optional minimum price filter
 * @param params.maxPrice - Optional maximum price filter
 * 
 * @returns Object containing the listings data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error, refetch } = useListings({
 *   page: 1,
 *   pageSize: 10,
 *   fromDate: '2023-01-01',
 *   toDate: '2023-12-31',
 *   model: 'RTX 4090',
 *   minPrice: 1000,
 *   maxPrice: 2000,
 * });
 * ```
 */
export function useListings({
  page = 1,
  pageSize = 10,
  fromDate,
  toDate,
  model,
  minPrice,
  maxPrice,
}: UseListingsParams): UseListingsResult {
  // Calculate offset based on page and pageSize
  const offset = (page - 1) * pageSize;
  
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<GpuListing[], Error>({
    queryKey: ['listings', page, pageSize, fromDate, toDate, model, minPrice, maxPrice],
    queryFn: () => getListings({
      limit: pageSize,
      offset,
      model,
      minPrice,
      maxPrice,
      fromDate,
      toDate,
    }),
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
  };
}