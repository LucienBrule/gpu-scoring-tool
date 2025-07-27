import { useState, useEffect } from 'react';
import { getHealth } from '@repo/client';

interface UseHealthResult {
  status: string | null;
  error: string | null;
  loading: boolean;
  refetch: () => Promise<void>;
}

/**
 * Custom hook to fetch health status from the API
 * @returns {UseHealthResult} Object containing status, error, loading state, and refetch function
 */
export function useHealth(): UseHealthResult {
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchHealth = async () => {
    try {
      setLoading(true);
      const response = await getHealth();
      setStatus(response.status);
      setError(null);
    } catch (err) {
      console.error('Error fetching health status:', err);
      setError('Failed to fetch health status');
      setStatus(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return {
    status,
    error,
    loading,
    refetch: fetchHealth,
  };
}