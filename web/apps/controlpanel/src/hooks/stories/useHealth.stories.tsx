import React from 'react';
import type { Meta, StoryObj } from '@storybook/react-vite';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useHealth } from '../useHealth';
import { ApiClient } from '@repo/client';
import { Card, CardContent, CardHeader, CardTitle } from '@repo/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@repo/ui/alert';
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

// Mock the ApiClient.getHealth method
const originalGetHealth = ApiClient.getHealth;

// Component that uses the useHealth hook
const HealthStatus: React.FC = () => {
  const { data, isLoading, isError, error, refetch } = useHealth();

  return (
    <Card className="w-[400px]">
      <CardHeader>
        <CardTitle>API Health Status</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading && (
          <div className="flex items-center space-x-2">
            <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
            <span>Checking API health...</span>
          </div>
        )}

        {isError && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              {error?.message || 'Failed to fetch API health status'}
            </AlertDescription>
          </Alert>
        )}

        {data && (
          <>
            {data.status === 'ok' ? (
              <Alert className="bg-green-50 dark:bg-green-900/20 border-green-500">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <AlertTitle>API is Healthy</AlertTitle>
                <AlertDescription>
                  The API is responding normally.
                </AlertDescription>
              </Alert>
            ) : (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>API is Unhealthy</AlertTitle>
                <AlertDescription>
                  The API is experiencing issues.
                </AlertDescription>
              </Alert>
            )}
          </>
        )}

        <div className="mt-4">
          <button
            onClick={() => refetch()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Refresh Status
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

// Create a new QueryClient for each story
const createQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

// Wrapper component with QueryClientProvider
const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = React.useMemo(() => createQueryClient(), []);
  
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

const meta: Meta<typeof HealthStatus> = {
  title: 'Hooks/useHealth',
  component: HealthStatus,
  parameters: {
    layout: 'centered',
  },
  decorators: [
    (Story) => (
      <Wrapper>
        <Story />
      </Wrapper>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof HealthStatus>;

// Loading state
export const Loading: Story = {
  parameters: {
    mockData: [
      {
        url: '/api/health',
        method: 'GET',
        status: 200,
        response: { status: 'ok' },
        delay: 10000, // Long delay to simulate loading
      },
    ],
  },
  play: async () => {
    // Mock the API to return a pending promise
    ApiClient.getHealth = () => new Promise(() => {});
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getHealth = originalGetHealth;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Success state (Healthy)
export const Healthy: Story = {
  play: async () => {
    // Mock the API to return a healthy status
    ApiClient.getHealth = () => Promise.resolve({ status: 'ok' });
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getHealth = originalGetHealth;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Success state (Unhealthy)
export const Unhealthy: Story = {
  play: async () => {
    // Mock the API to return an unhealthy status
    ApiClient.getHealth = () => Promise.resolve({ status: 'error' });
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getHealth = originalGetHealth;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Error state
export const Error: Story = {
  play: async () => {
    // Mock the API to return an error
    ApiClient.getHealth = () => Promise.reject(new Error('Failed to connect to API'));
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getHealth = originalGetHealth;
        };
      }, []);
      
      return <Story />;
    },
  ],
};