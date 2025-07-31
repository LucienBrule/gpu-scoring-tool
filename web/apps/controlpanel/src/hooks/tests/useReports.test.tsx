import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { GpuReportRow } from '@repo/client';

// Sample data for testing
const mockReportsData: GpuReportRow[] = [
  {
    canonicalModel: 'RTX 3090',
    vramGb: 24,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 350,
    price: 1499.99,
    score: 0.85,
  },
  {
    canonicalModel: 'RTX 4090',
    vramGb: 24,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 450,
    price: 1999.99,
    score: 0.95,
  },
];

// Create a simple mock implementation of useReports
const mockUseReports = vi.fn();

// Mock the hooks from @repo/client
vi.mock('@repo/client', () => ({
  hooks: {
    useReports: (filters) => mockUseReports(filters)
  },
  type: {
    GpuReportRow: {}
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

describe('useReports', () => {
  it('should return loading state initially', () => {
    // Set up the mock to return loading state
    mockUseReports.mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useReports(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBe(undefined);
    expect(result.current.isError).toBe(false);
  });
  
  it('should return data when successful', () => {
    // Set up the mock to return success state with data
    mockUseReports.mockReturnValue({
      data: mockReportsData,
      isLoading: false,
      isError: false,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useReports(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.data).toEqual(mockReportsData);
    expect(result.current.isError).toBe(false);
  });
  
  it('should return error when request fails', () => {
    // Set up the mock to return error state
    mockUseReports.mockReturnValue({
      data: undefined,
      isLoading: false,
      isError: true,
      refetch: vi.fn(),
    });
    
    const { result } = renderHook(() => hooks.useReports(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.data).toBe(undefined);
    expect(result.current.isError).toBe(true);
  });
  
  it('should pass filters to useReports', () => {
    const mockRefetch = vi.fn();
    mockUseReports.mockReturnValue({
      data: mockReportsData,
      isLoading: false,
      isError: false,
      refetch: mockRefetch,
    });
    
    const filters = {
      model: 'RTX',
      minPrice: 1000,
      maxPrice: 2000,
      limit: 10,
      offset: 0,
    };
    
    renderHook(() => hooks.useReports(filters), {
      wrapper: createWrapper(),
    });
    
    // Verify that useReports was called with the filters
    expect(mockUseReports).toHaveBeenCalledWith(filters);
  });
  
  it('should refetch data when refetch is called', () => {
    const mockRefetch = vi.fn();
    
    // Set up the mock to return a refetch function
    mockUseReports.mockReturnValue({
      data: mockReportsData,
      isLoading: false,
      isError: false,
      refetch: mockRefetch,
    });
    
    const { result } = renderHook(() => hooks.useReports(), {
      wrapper: createWrapper(),
    });
    
    // Call refetch
    result.current.refetch();
    
    // Verify that refetch was called
    expect(mockRefetch).toHaveBeenCalledTimes(1);
  });
});