import { useQuery } from '@tanstack/react-query';
import { getListings, GpuListing } from '@repo/client';
/**
 * Parameters for the useGpuListings hook
 */
export interface UseGpuListingsParams {
  /**
   * Number of items to return (pagination)
   */
  limit?: number;
  
  /**
   * Number of items to skip (pagination)
   */
  offset?: number;
  
  /**
   * Filter by Gpu model name
   */
  model?: string;
  
  /**
   * Filter by minimum price
   */
  minPrice?: number;
  
  /**
   * Filter by maximum price
   */
  maxPrice?: number;
  
  /**
   * Filter by listings from this date (ISO 8601 format: YYYY-MM-DD)
   */
  fromDate?: string;
  
  /**
   * Filter by listings until this date (ISO 8601 format: YYYY-MM-DD)
   */
  toDate?: string;
}

/**
 * Result returned by the useGpuListings hook
 */
export interface UseGpuListingsResult {
  /**
   * The listings data
   */
  data: GpuListing[] | undefined;
  
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
 * Hook to fetch Gpu listings with filtering and pagination
 * 
 * @param params - Parameters for filtering and pagination
 * @returns Object containing the listings data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useGpuListings({
 *   limit: 10,
 *   offset: 0,
 *   model: 'RTX 4090',
 *   minPrice: 1000,
 *   maxPrice: 2000,
 *   fromDate: '2023-01-01',
 *   toDate: '2023-12-31',
 * });
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * 
 * return (
 *   <ul>
 *     {data?.map(listing => (
 *       <li key={listing.id}>{listing.title} - ${listing.price}</li>
 *     ))}
 *   </ul>
 * );
 * ```
 */
export function useGpuListings({
  limit = 10,
  offset = 0,
  model,
  minPrice,
  maxPrice,
  fromDate,
  toDate,
}: UseGpuListingsParams = {}): UseGpuListingsResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<GpuListing[], Error>({
    queryKey: ['listings', limit, offset, model, minPrice, maxPrice, fromDate, toDate],
    queryFn: () => getListings({
      limit,
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

/**
 * Hook to fetch a single Gpu listing by ID
 * 
 * @param id - The ID of the listing to fetch
 * @returns Object containing the listing data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useGpuListingById('123');
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data) return <div>Listing not found</div>;
 * 
 * return (
 *   <div>
 *     <h1>{data.title}</h1>
 *     <p>Price: ${data.price}</p>
 *     <p>Model: {data.model}</p>
 *   </div>
 * );
 * ```
 */
export function useGpuListingById(id: string) {
  const result = useQuery<GpuListing[], Error>({
    queryKey: ['listing', id],
    queryFn: () => getListings({ id }),
    enabled: !!id, // Only run the query if an ID is provided
  });
  
  // Extract the first listing from the array if it exists
  const singleListing = result.data && result.data.length > 0 ? result.data[0] : undefined;
  
  return {
    ...result,
    data: singleListing,
  };
}

export default useGpuListings;