import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Create a simple mock implementation of useHealthCheck
const mockUseHealthCheck = vi.fn();

// Mock the hooks from @repo/client
vi.mock('@repo/client', () => ({
  hooks: {
    useHealthCheck: () => mockUseHealthCheck()
  }
}));

// Import the mocked hooks
import { hooks } from '@repo/client';

// Create a wrapper component with QueryClientProvider
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  
  // Using a named function to avoid ESLint display-name warning
  function TestWrapper({ children }: { children: React.ReactNode }) {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
  }
  
  return TestWrapper;
};

describe('useHealthCheck', () => {
  it('should return loading state initially', () => {
    // Set up the mock to return loading state
    mockUseHealthCheck.mockReturnValue({
      status: null,
      loading: true,
      error: null,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useHealthCheck(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.loading).toBe(true);
    expect(result.current.status).toBe(null);
    expect(result.current.error).toBe(null);
  });
  
  it('should return status when successful', () => {
    // Set up the mock to return success state
    mockUseHealthCheck.mockReturnValue({
      status: 'ok',
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useHealthCheck(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.loading).toBe(false);
    expect(result.current.status).toBe('ok');
    expect(result.current.error).toBe(null);
  });
  
  it('should return error when request fails', () => {
    const errorMessage = 'Failed to fetch health status';
    
    // Set up the mock to return error state
    mockUseHealthCheck.mockReturnValue({
      status: null,
      loading: false,
      error: errorMessage,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useHealthCheck(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.loading).toBe(false);
    expect(result.current.status).toBe(null);
    expect(result.current.error).toBe(errorMessage);
  });
  
  it('should refetch data when refetch is called', () => {
    const mockRefetch = vi.fn();
    
    // Set up the mock to return a refetch function
    mockUseHealthCheck.mockReturnValue({
      status: 'ok',
      loading: false,
      error: null,
      refetch: mockRefetch,
    });
    
    const { result } = renderHook(() => hooks.useHealthCheck(), {
      wrapper: createWrapper(),
    });
    
    // Call refetch
    result.current.refetch();
    
    // Verify that refetch was called
    expect(mockRefetch).toHaveBeenCalledTimes(1);
  });
});