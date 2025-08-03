import React, { useState } from 'react';
import type { Meta, StoryObj } from '@storybook/react-vite';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useGpuListings } from '../useGpuListings';
import { ApiClient } from '@repo/client';
import type { GPUListingDTO } from '@repo/client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@repo/ui/card';
import { Input } from '@repo/ui/input';
import { Label } from '@repo/ui/label';
import { Button } from '@repo/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@repo/ui/alert';
import { AlertCircle, Loader2 } from 'lucide-react';

// Mock the ApiClient.getListings method
const originalGetListings = ApiClient.getListings;

// Sample GPU listings data
const sampleListings: GPUListingDTO[] = [
  {
    canonicalModel: 'RTX 3080',
    vramGb: 10,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 320,
    price: 699.99,
    score: 0.85,
    importId: 'import-123',
    importIndex: 1
  },
  {
    canonicalModel: 'RTX 3090',
    vramGb: 24,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 350,
    price: 1499.99,
    score: 0.92,
    importId: 'import-123',
    importIndex: 2
  },
  {
    canonicalModel: 'RTX 4080',
    vramGb: 16,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 320,
    price: 1199.99,
    score: 0.88,
    importId: 'import-123',
    importIndex: 3
  },
  {
    canonicalModel: 'RTX 4090',
    vramGb: 24,
    migSupport: 0,
    nvlink: true,
    tdpWatts: 450,
    price: 1599.99,
    score: 0.95,
    importId: 'import-123',
    importIndex: 4
  },
  {
    canonicalModel: 'A100',
    vramGb: 80,
    migSupport: 7,
    nvlink: true,
    tdpWatts: 400,
    price: 10999.99,
    score: 0.98,
    importId: 'import-123',
    importIndex: 5
  }
];

// Component that uses the useGpuListings hook
const GpuListingsComponent: React.FC = () => {
  const [filters, setFilters] = useState({
    model: '',
    minPrice: '',
    maxPrice: '',
  });
  
  const [appliedFilters, setAppliedFilters] = useState({
    model: '',
    minPrice: undefined as number | undefined,
    maxPrice: undefined as number | undefined,
  });
  
  const { data, isLoading, isError, error, refetch } = useGpuListings({
    model: appliedFilters.model || undefined,
    minPrice: appliedFilters.minPrice,
    maxPrice: appliedFilters.maxPrice,
    limit: 10,
    offset: 0,
  });
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };
  
  const handleApplyFilters = () => {
    setAppliedFilters({
      model: filters.model,
      minPrice: filters.minPrice ? parseFloat(filters.minPrice) : undefined,
      maxPrice: filters.maxPrice ? parseFloat(filters.maxPrice) : undefined,
    });
  };
  
  const handleReset = () => {
    setFilters({
      model: '',
      minPrice: '',
      maxPrice: '',
    });
    setAppliedFilters({
      model: '',
      minPrice: undefined,
      maxPrice: undefined,
    });
  };
  
  return (
    <Card className="w-[600px]">
      <CardHeader>
        <CardTitle>GPU Listings</CardTitle>
        <CardDescription>
          Browse and filter GPU listings
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Filters */}
          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="model">Model</Label>
              <Input
                id="model"
                name="model"
                value={filters.model}
                onChange={handleInputChange}
                placeholder="e.g. RTX 3080"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="minPrice">Min Price ($)</Label>
              <Input
                id="minPrice"
                name="minPrice"
                type="number"
                value={filters.minPrice}
                onChange={handleInputChange}
                placeholder="e.g. 500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxPrice">Max Price ($)</Label>
              <Input
                id="maxPrice"
                name="maxPrice"
                type="number"
                value={filters.maxPrice}
                onChange={handleInputChange}
                placeholder="e.g. 2000"
              />
            </div>
          </div>
          
          <div className="flex space-x-2">
            <Button onClick={handleApplyFilters}>Apply Filters</Button>
            <Button variant="outline" onClick={handleReset}>Reset</Button>
          </div>
          
          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center space-x-2 py-4">
              <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
              <span>Loading GPU listings...</span>
            </div>
          )}
          
          {/* Error State */}
          {isError && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                {error || 'Failed to fetch GPU listings'}
              </AlertDescription>
            </Alert>
          )}
          
          {/* Data Display */}
          {data && !isLoading && (
            <div className="mt-4">
              {data.length === 0 ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  No GPU listings found matching your criteria.
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Showing {data.length} results
                  </div>
                  <div className="border rounded-md overflow-hidden">
                    <table className="w-full">
                      <thead className="bg-gray-100 dark:bg-gray-800">
                        <tr>
                          <th className="px-4 py-2 text-left">Model</th>
                          <th className="px-4 py-2 text-left">VRAM (GB)</th>
                          <th className="px-4 py-2 text-left">Price ($)</th>
                          <th className="px-4 py-2 text-left">Score</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.map((listing, index) => (
                          <tr 
                            key={`${listing.canonicalModel}-${index}`}
                            className="border-t dark:border-gray-700"
                          >
                            <td className="px-4 py-2">{listing.canonicalModel}</td>
                            <td className="px-4 py-2">{listing.vramGb}</td>
                            <td className="px-4 py-2">${listing.price.toFixed(2)}</td>
                            <td className="px-4 py-2">{(listing.score * 100).toFixed(0)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </CardContent>
      <CardFooter>
        <Button variant="outline" onClick={() => refetch()}>Refresh Data</Button>
      </CardFooter>
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

const meta: Meta<typeof GpuListingsComponent> = {
  title: 'Hooks/useGpuListings',
  component: GpuListingsComponent,
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
type Story = StoryObj<typeof GpuListingsComponent>;

// Loading state
export const Loading: Story = {
  play: async () => {
    // Mock the API to return a pending promise
    ApiClient.getListings = () => new Promise(() => {});
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getListings = originalGetListings;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Success state with data
export const WithData: Story = {
  play: async () => {
    // Mock the API to return sample data
    ApiClient.getListings = () => Promise.resolve(sampleListings);
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getListings = originalGetListings;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Success state with filtered data
export const FilteredData: Story = {
  play: async () => {
    // Mock the API to return filtered data based on parameters
    ApiClient.getListings = (params) => {
      let filteredData = [...sampleListings];
      
      if (params?.model) {
        filteredData = filteredData.filter(listing => 
          listing.canonicalModel.toLowerCase().includes(params.model.toLowerCase())
        );
      }
      
      if (params?.minPrice !== undefined) {
        filteredData = filteredData.filter(listing => listing.price >= params.minPrice!);
      }
      
      if (params?.maxPrice !== undefined) {
        filteredData = filteredData.filter(listing => listing.price <= params.maxPrice!);
      }
      
      return Promise.resolve(filteredData);
    };
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getListings = originalGetListings;
        };
      }, []);
      
      return <Story />;
    },
  ],
};

// Success state with empty data
export const EmptyData: Story = {
  play: async () => {
    // Mock the API to return empty data
    ApiClient.getListings = () => Promise.resolve([]);
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getListings = originalGetListings;
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
    ApiClient.getListings = () => Promise.reject(new Error('Failed to fetch GPU listings'));
  },
  decorators: [
    (Story) => {
      // Reset the mock after the story
      React.useEffect(() => {
        return () => {
          ApiClient.getListings = originalGetListings;
        };
      }, []);
      
      return <Story />;
    },
  ],
};