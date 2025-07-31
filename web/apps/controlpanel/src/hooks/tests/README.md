# Testing React Hooks

This directory contains tests for React hooks used in the application. The tests are written using Vitest and React Testing Library.

## Testing Approach

When testing hooks, we follow these principles:

1. **Isolation**: Test each hook in isolation from the components that use it.
2. **Mocking**: Mock external dependencies (like API calls) to control the test environment.
3. **State Transitions**: Test all possible states of the hook (loading, success, error).
4. **Edge Cases**: Test edge cases like empty responses or unexpected errors.

## Test Structure

Each test file follows this structure:

1. **Setup**: Create a wrapper component with necessary providers (e.g., QueryClientProvider).
2. **Mocking**: Mock external dependencies using Vitest's mocking capabilities.
3. **Test Cases**: Write test cases for different scenarios.
4. **Assertions**: Verify that the hook behaves as expected in each scenario.

## Example: Testing a Query Hook

Here's an example of how to test a hook that uses React Query:

```tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { hooks } from '@repo/client';
import * as clientModule from '@repo/client';

// Create a wrapper component with QueryClientProvider
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  
  function TestWrapper({ children }: { children: React.ReactNode }) {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
  }
  
  return TestWrapper;
};

describe('useMyHook', () => {
  // Mock the API function
  const mockApiFunction = vi.fn();
  
  beforeEach(() => {
    vi.resetAllMocks();
    // Mock the API function in the client module
    vi.spyOn(clientModule, 'apiFunction').mockImplementation(mockApiFunction);
  });
  
  it('should return loading state initially', () => {
    mockApiFunction.mockResolvedValue({ data: 'test' });
    
    const { result } = renderHook(() => hooks.useMyHook(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBe(undefined);
    expect(result.current.isError).toBe(false);
  });
  
  it('should return data when successful', async () => {
    const mockData = { data: 'test' };
    mockApiFunction.mockResolvedValue(mockData);
    
    const { result } = renderHook(() => hooks.useMyHook(), {
      wrapper: createWrapper(),
    });
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.data).toEqual(mockData);
    expect(result.current.isError).toBe(false);
  });
  
  it('should return error when request fails', async () => {
    mockApiFunction.mockRejectedValue(new Error('Failed to fetch data'));
    
    const { result } = renderHook(() => hooks.useMyHook(), {
      wrapper: createWrapper(),
    });
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.data).toBe(undefined);
    expect(result.current.isError).toBe(true);
  });
});
```

## Best Practices

1. **Test Initial State**: Always test the initial state of the hook.
2. **Test Loading State**: Verify that the hook shows a loading state while fetching data.
3. **Test Success State**: Verify that the hook returns the expected data on success.
4. **Test Error State**: Verify that the hook handles errors correctly.
5. **Test Refetching**: If the hook provides a refetch function, test that it works as expected.
6. **Test with Different Parameters**: If the hook accepts parameters, test it with different parameter values.

## Running Tests

To run the tests for hooks, use the following command:

```bash
pnpm run test:unit
```

This will run all unit tests, including the hook tests in this directory.