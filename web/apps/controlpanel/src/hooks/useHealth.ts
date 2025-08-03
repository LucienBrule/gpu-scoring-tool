import { useQuery } from '@tanstack/react-query';
import { getHealth} from '@repo/client';
import type { HealthStatus } from '@repo/client';

/**
 * Hook to fetch API health status
 * 
 * @returns Object containing the health status data, loading state, error state, and refetch function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error } = useHealth();
 * 
 * if (isLoading) return <div>Loading...</div>;
 * if (isError) return <div>Error: {error}</div>;
 * 
 * return (
 *   <div>
 *     API Status: {data?.status === 'ok' ? 'Healthy' : 'Unhealthy'}
 *   </div>
 * );
 * ```
 */
export const useHealth = () =>
  useQuery<HealthStatus, Error>({
    queryKey: ['health'],
    queryFn: () => getHealth()
  });

export default useHealth;