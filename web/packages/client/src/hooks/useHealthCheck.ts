import { useQuery } from '@tanstack/react-query';
import { getHealth } from '../client.js';
import { HealthStatus } from '@repo/client-generated';

/**
 * Hook to check the health status of the backend API
 * @returns Object containing the health status, loading state, error, and refetch function
 */
export function useHealthCheck() {
  const {
    data,
    isLoading,
    error,
    refetch,
  } = useQuery<HealthStatus, Error>({
    queryKey: ['health'],
    queryFn: () => getHealth(),
  });

  return {
    status: data?.status || null, // Extract the status string from the HealthStatus object
    loading: isLoading, // Renamed to match existing interface
    error: error ? error.message : null, // Convert Error to string message or null
    refetch: () => refetch(), // Provide refetch function
  };
}