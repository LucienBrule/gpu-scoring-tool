import { useQuery } from '@tanstack/react-query';
import type { GPUListingDTO } from '@repo/client-generated';

export interface useListingsLegacyFilters {
  model?: string;
  quantized?: boolean;
}

export interface useListingsLegacyResult {
  data: GPUListingDTO[] | undefined;
  isLoading: boolean;
  isError: boolean;
  refetch: () => void;
}

/**
 * Hook to fetch data from /api/listings/legacy
 * @param filters Optional filters to apply to the query
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function useListingsLegacy(filters?: useListingsLegacyFilters): useListingsLegacyResult {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<GPUListingDTO[], Error>({
    queryKey: ['uselistingslegacy', filters],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching /api/listings/legacy with filters:', filters);
      return Promise.resolve([] as GPUListingDTO[]);
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
