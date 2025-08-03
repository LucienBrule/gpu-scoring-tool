import { useQuery } from '@tanstack/react-query';
import { getReports, GpuReport} from '@repo/client';

/**
 * Parameters for the useGpuReports hook
 */
export interface UseGpuReportsParams {
  /**
   * Filter by GPU model name
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
   * Number of items to return (pagination)
   */
  limit?: number;
  
  /**
   * Number of items to skip (pagination)
   */
  offset?: number;
}

/**
 * Result returned by the useGpuReports hook
 */
export interface UseGpuReportsResult {
  /**
   * The reports data
   */
  data: GpuReport[] | undefined;
  
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
   * Parse markdown content from a report
   */
  parseMarkdown: (markdown: string) => string;
}

/**
 * Simple utility function to parse markdown content
 * This is a placeholder - in a real application, you might use a library like marked or remark
 * 
 * @param markdown - The markdown content to parse
 * @returns The parsed markdown content
 */
export function parseMarkdown(markdown: string): string {
  // This is a simple implementation that just returns the original markdown
  // In a real application, you would use a proper markdown parser
  return markdown;
}

/**
 * Hook to fetch GPU reports with filtering and pagination
 * 
 * @param params - Parameters for filtering and pagination
 * @returns Object containing the reports data, loading state, error state, refetch function, and markdown parser
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error, parseMarkdown } = useGpuReports({
 *   model: 'RTX 4090',
 *   minPrice: 1000,
 *   maxPrice: 2000,
 *   limit: 10,
 *   offset: 0,
 * });
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * if (!data || data.length === 0) return <div>No reports found</div>;
 * 
 * return (
 *   <div>
 *     {data.map(report => (
 *       <div key={report.id}>
 *         <h2>{report.title}</h2>
 *         <div dangerouslySetInnerHTML={{ __html: parseMarkdown(report.content) }} />
 *       </div>
 *     ))}
 *   </div>
 * );
 * ```
 */
export function useGpuReports({
  model,
  minPrice,
  maxPrice,
  limit = 10,
  offset = 0,
}: UseGpuReportsParams = {}): UseGpuReportsResult {
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<GpuReport[], Error>({
    queryKey: ['reports', model, minPrice, maxPrice, limit, offset],
    queryFn: () => getReports({
      model,
      minPrice,
      maxPrice,
      limit,
      offset,
    }),
    // Handle missing reports gracefully
    retry: (failureCount, error) => {
      // Don't retry if we get a 404 (not found)
      if (error.message.includes('404')) {
        return false;
      }
      // Retry up to 3 times for other errors
      return failureCount < 3;
    },
  });

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
    parseMarkdown,
  };
}

export default useGpuReports;