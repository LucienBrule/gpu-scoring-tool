import { useQuery } from '@tanstack/react-query';
import type { GpuReport } from '@repo/client';

/**
 * Hook to fetch data from /api/report
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function useReport() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<GpuReport, Error>({
    queryKey: ['usereport'],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching /api/report');
      return Promise.resolve({} as GpuReport);
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
