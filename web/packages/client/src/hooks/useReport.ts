import { useQuery } from '@tanstack/react-query';
import type { ReportDTO } from '@repo/client-generated';

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
  } = useQuery<ReportDTO, Error>({
    queryKey: ['usereport'],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching /api/report');
      return Promise.resolve({} as ReportDTO);
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
