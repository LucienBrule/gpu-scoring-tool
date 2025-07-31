import { useQuery } from '@tanstack/react-query';
import type { GPUModelDTO } from '@repo/client-generated';

/**
 * Hook to fetch data from /api/models
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function useModels() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<GPUModelDTO[], Error>({
    queryKey: ['usemodels'],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching /api/models');
      return Promise.resolve([] as GPUModelDTO[]);
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
