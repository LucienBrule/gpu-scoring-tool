import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useModels } from './useModels.js';
import * as client from '../client.js';
import { useQuery } from '@tanstack/react-query';
import type { GPUModelDTO } from '@repo/client-generated';

// Mock the client module
vi.mock('../client', () => ({
  getModels: vi.fn(),
}));

// Mock the react-query module
vi.mock('@tanstack/react-query', () => ({
  useQuery: vi.fn(),
}));

// Mock React hooks
vi.mock('react', () => ({
  useMemo: (fn: () => unknown) => fn(),
}));

/**
 * Helper function to create mock return values for useQuery
 * @param override - Override specific properties of the default mock return value
 * @returns A mock return value for useQuery
 */
function mockUseQueryReturn(override = {}) {
  return {
    data: [],
    isLoading: false,
    isError: false,
    error: null,
    refetch: vi.fn(),
    ...override,
  };
}

describe('useModels', () => {
  const mockModelsData = [
    {
      model: 'NVIDIA RTX 4090',
      listingCount: 120,
      minPrice: 1499.99,
      medianPrice: 1599.99,
      maxPrice: 1799.99,
      avgPrice: 1649.99,
      vramGb: 24,
      tdpWatts: 450,
      migSupport: 0,
      nvlink: true,
      generation: '40 Series',
      cudaCores: 16384,
      slotWidth: 3,
      pcieGeneration: 4,
    },
    {
      model: 'NVIDIA RTX 4080',
      listingCount: 95,
      minPrice: 1099.99,
      medianPrice: 1199.99,
      maxPrice: 1299.99,
      avgPrice: 1189.99,
      vramGb: 16,
      tdpWatts: 320,
      migSupport: 0,
      nvlink: true,
      generation: '40 Series',
      cudaCores: 9728,
      slotWidth: 3,
      pcieGeneration: 4,
    },
    {
      model: 'AMD Radeon RX 7900 XTX',
      listingCount: 80,
      minPrice: 999.99,
      medianPrice: 1049.99,
      maxPrice: 1149.99,
      avgPrice: 1059.99,
      vramGb: 24,
      tdpWatts: 355,
      migSupport: null,
      nvlink: false,
      generation: 'RDNA 3',
      cudaCores: null,
      slotWidth: 2.5,
      pcieGeneration: 4,
    },
    {
      model: 'NVIDIA RTX 3090',
      listingCount: 150,
      minPrice: 899.99,
      medianPrice: 949.99,
      maxPrice: 1099.99,
      avgPrice: 979.99,
      vramGb: 24,
      tdpWatts: 350,
      migSupport: 0,
      nvlink: true,
      generation: '30 Series',
      cudaCores: 10496,
      slotWidth: 3,
      pcieGeneration: 4,
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    // Set up the useQuery mock with default return values
    (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
      data: mockModelsData
    }));
  });

  it('should use correct query key', () => {
    // Call the hook
    useModels();
    
    // Check that useQuery was called with the correct queryKey
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['models'],
    }));
  });

  it('should reset query cache when parameters change', () => {
    // Reset the mock to clear previous calls
    (useQuery as ReturnType<typeof vi.fn>).mockClear();
    
    // Call the hook with default parameters
    useModels();
    
    // Check that useQuery was called
    expect(useQuery).toHaveBeenCalled();
    
    // Reset the mock again
    (useQuery as ReturnType<typeof vi.fn>).mockClear();
    
    // Call the hook with different parameters
    useModels({ modelName: 'RTX' });
    
    // Check that useQuery was called again with different parameters
    expect(useQuery).toHaveBeenCalledWith(expect.objectContaining({
      queryKey: ['models'],
    }));
  });

  it('should return the expected structure', () => {
    // Call the hook
    const result = useModels();
    
    // Check the structure of the returned object
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('isLoading');
    expect(result).toHaveProperty('isError');
    expect(result).toHaveProperty('error');
    expect(result).toHaveProperty('refetch');
    expect(result).toHaveProperty('getDropdownOptions');
    expect(result).toHaveProperty('getModelByName');
    
    // Check that the data is passed through correctly
    expect(result.data).toEqual(mockModelsData);
  });

  describe('filtering', () => {
    it('should filter by model name with substring match', () => {
      // Call the hook with a model name filter
      const result = useModels({ modelName: 'RTX' });
      
      // Check that only models with "RTX" in the name are returned
      expect(result.data?.length).toBe(3);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.model).toContain('RTX');
      });
    });

    it('should filter by model name with exact match', () => {
      // Call the hook with a model name filter and exact match
      const result = useModels({ 
        modelName: 'NVIDIA RTX 4090', 
        matchMode: 'exact' 
      });
      
      // Check that only the exact model is returned
      expect(result.data?.length).toBe(1);
      expect(result.data?.[0].model).toBe('NVIDIA RTX 4090');
    });

    it('should filter by manufacturer', () => {
      // Call the hook with a manufacturer filter
      const result = useModels({ manufacturer: 'NVIDIA' });
      
      // Check that only NVIDIA models are returned
      expect(result.data?.length).toBe(3);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.model).toContain('NVIDIA');
      });
    });

    it('should filter by generation', () => {
      // Call the hook with a generation filter
      const result = useModels({ generation: '40' });
      
      // Check that only 40 Series models are returned
      expect(result.data?.length).toBe(2);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.generation).toContain('40');
      });
    });

    it('should filter by minimum VRAM', () => {
      // Call the hook with a minimum VRAM filter
      const result = useModels({ minVramGb: 24 });
      
      // Check that only models with 24GB or more VRAM are returned
      expect(result.data?.length).toBe(3);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.vramGb).toBeGreaterThanOrEqual(24);
      });
    });

    it('should filter by maximum VRAM', () => {
      // Call the hook with a maximum VRAM filter
      const result = useModels({ maxVramGb: 16 });
      
      // Check that only models with 16GB or less VRAM are returned
      expect(result.data?.length).toBe(1);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.vramGb).toBeLessThanOrEqual(16);
      });
    });

    it('should filter by minimum TDP', () => {
      // Call the hook with a minimum TDP filter
      const result = useModels({ minTdpWatts: 400 });
      
      // Check that only models with 400W or more TDP are returned
      expect(result.data?.length).toBe(1);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.tdpWatts).toBeGreaterThanOrEqual(400);
      });
    });

    it('should filter by maximum TDP', () => {
      // Call the hook with a maximum TDP filter
      const result = useModels({ maxTdpWatts: 350 });
      
      // Check that only models with 350W or less TDP are returned
      expect(result.data?.length).toBe(2);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.tdpWatts).toBeLessThanOrEqual(350);
      });
    });

    it('should filter by NVLink support', () => {
      // Call the hook with an NVLink filter
      const result = useModels({ nvlink: true });
      
      // Check that only models with NVLink support are returned
      expect(result.data?.length).toBe(3);
      result.data?.forEach((model: GPUModelDTO) => {
        expect(model.nvlink).toBe(true);
      });
    });

    it('should combine multiple filters', () => {
      // Call the hook with multiple filters
      const result = useModels({
        manufacturer: 'NVIDIA',
        generation: '40',
        minVramGb: 20,
      });
      
      // Check that only models matching all filters are returned
      expect(result.data?.length).toBe(1);
      expect(result.data?.[0].model).toBe('NVIDIA RTX 4090');
    });
  });

  describe('sorting', () => {
    it('should sort by VRAM in ascending order', () => {
      // Call the hook with sorting by VRAM
      const result = useModels({
        sortBy: 'vramGb',
        sortDirection: 'asc',
      });
      
      // Check that models are sorted by VRAM in ascending order
      expect(result.data?.[0].vramGb).toBe(16);
      expect(result.data?.[1].vramGb).toBe(24);
      expect(result.data?.[2].vramGb).toBe(24);
      expect(result.data?.[3].vramGb).toBe(24);
    });

    it('should sort by VRAM in descending order', () => {
      // Call the hook with sorting by VRAM
      const result = useModels({
        sortBy: 'vramGb',
        sortDirection: 'desc',
      });
      
      // Check that models are sorted by VRAM in descending order
      expect(result.data?.[0].vramGb).toBe(24);
      expect(result.data?.[1].vramGb).toBe(24);
      expect(result.data?.[2].vramGb).toBe(24);
      expect(result.data?.[3].vramGb).toBe(16);
    });

    it('should sort by TDP in ascending order', () => {
      // Call the hook with sorting by TDP
      const result = useModels({
        sortBy: 'tdpWatts',
        sortDirection: 'asc',
      });
      
      // Check that models are sorted by TDP in ascending order
      expect(result.data?.[0].tdpWatts).toBe(320);
      expect(result.data?.[1].tdpWatts).toBe(350);
      expect(result.data?.[2].tdpWatts).toBe(355);
      expect(result.data?.[3].tdpWatts).toBe(450);
    });

    it('should sort by model name in ascending order', () => {
      // Call the hook with sorting by model name
      const result = useModels({
        sortBy: 'model',
        sortDirection: 'asc',
      });
      
      // Check that models are sorted by name in ascending order
      expect(result.data?.[0].model).toBe('AMD Radeon RX 7900 XTX');
      expect(result.data?.[1].model).toBe('NVIDIA RTX 3090');
      expect(result.data?.[2].model).toBe('NVIDIA RTX 4080');
      expect(result.data?.[3].model).toBe('NVIDIA RTX 4090');
    });

    it('should sort by price in descending order', () => {
      // Call the hook with sorting by price
      const result = useModels({
        sortBy: 'avgPrice',
        sortDirection: 'desc',
      });
      
      // Check that models are sorted by price in descending order
      expect(result.data?.[0].avgPrice).toBe(1649.99);
      expect(result.data?.[1].avgPrice).toBe(1189.99);
      expect(result.data?.[2].avgPrice).toBe(1059.99);
      expect(result.data?.[3].avgPrice).toBe(979.99);
    });
  });

  describe('helper methods', () => {
    it('should return dropdown options', () => {
      // Call the hook
      const result = useModels();
      
      // Get dropdown options
      const options = result.getDropdownOptions();
      
      // Check that options are formatted correctly
      expect(options.length).toBe(4);
      expect(options[0]).toEqual({
        label: 'NVIDIA RTX 4090',
        value: 'NVIDIA RTX 4090',
      });
    });

    it('should get a model by name', () => {
      // Call the hook
      const result = useModels();
      
      // Get a model by name
      const model = result.getModelByName('NVIDIA RTX 4090');
      
      // Check that the correct model is returned
      expect(model).toEqual(mockModelsData[0]);
    });

    it('should return undefined for a non-existent model', () => {
      // Call the hook
      const result = useModels();
      
      // Get a non-existent model
      const model = result.getModelByName('Non-existent Model');
      
      // Check that undefined is returned
      expect(model).toBeUndefined();
    });
  });

  describe('error handling', () => {
    it('should handle API errors', () => {
      // Set up the mock to return an error state
      const errorMessage = 'Failed to fetch models';
      (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
        data: undefined,
        isLoading: false,
        isError: true,
        error: new Error(errorMessage),
      }));
      
      // Call the hook
      const result = useModels();
      
      // Check that error state is handled correctly
      expect(result.isError).toBe(true);
      expect(result.error).toBe(errorMessage);
      expect(result.data).toBeUndefined();
    });
  });

  describe('edge cases', () => {
    it('should handle empty data', () => {
      // Set up the mock to return empty data
      (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
        data: []
      }));
      
      // Call the hook
      const result = useModels();
      
      // Check that empty data is handled correctly
      expect(result.data).toEqual([]);
      expect(result.getDropdownOptions()).toEqual([]);
      expect(result.getModelByName('Any Model')).toBeUndefined();
    });

    it('should handle null or undefined values in sorting', () => {
      // Create mock data with null values
      const mockDataWithNulls = [
        ...mockModelsData,
        {
          model: 'Unknown GPU',
          listingCount: 10,
          minPrice: 499.99,
          medianPrice: 549.99,
          maxPrice: 599.99,
          avgPrice: 549.99,
          vramGb: null,
          tdpWatts: null,
          migSupport: null,
          nvlink: null,
          generation: null,
          cudaCores: null,
          slotWidth: null,
          pcieGeneration: null,
        },
      ];
      
      // Set up the mock to return data with nulls
      (useQuery as ReturnType<typeof vi.fn>).mockReturnValue(mockUseQueryReturn({
        data: mockDataWithNulls
      }));
      
      // Call the hook with sorting by a field that has null values
      const result = useModels({
        sortBy: 'vramGb',
        sortDirection: 'asc',
      });
      
      // Check that null values are handled correctly in sorting
      // Null values should be sorted first in ascending order
      expect(result.data?.[0].vramGb).toBeNull();
    });
  });
});