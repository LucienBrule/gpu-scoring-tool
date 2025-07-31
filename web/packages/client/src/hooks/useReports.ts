import { useQuery } from '@tanstack/react-query';
import { getReports, GpuReportRow } from '../client.js';

export interface UseReportsFilters {
  model?: string;
  minPrice?: number;
  maxPrice?: number;
  limit?: number;
  offset?: number;
}

export interface UseReportsResult {
  data: GpuReportRow[] | undefined;
  isLoading: boolean;
  isError: boolean;
  refetch: () => void;
}

/**
 * Hook to fetch GPU reports (using listings as a substitute)
 * @param filters Optional filters to apply to the reports query
 * @returns Object containing the reports data, loading state, error state, and refetch function
 */
export function useReports(filters?: UseReportsFilters): UseReportsResult {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<GpuReportRow[], Error>({
    queryKey: ['reports', filters],
    queryFn: () => getReports(filters),
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}