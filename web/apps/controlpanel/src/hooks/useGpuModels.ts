import { useQuery } from '@tanstack/react-query';
import { getModels} from '@repo/client';
import type { GpuModel } from '@repo/client';

/**
 * Hook to fetch GPU model metadata
 * 
 * @returns Object containing the models data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useGpuModels();
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * 
 * return (
 *   <ul>
 *     {data?.map(model => (
 *       <li key={model.id}>{model.model}</li>
 *     ))}
 *   </ul>
 * );
 * ```
 */
export const useGpuModels = () =>
  useQuery<GpuModel[], Error>({
    queryKey: ['models'],
    queryFn: () => getModels()
  });

export default useGpuModels;