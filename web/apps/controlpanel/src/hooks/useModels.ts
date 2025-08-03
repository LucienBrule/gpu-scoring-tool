import { useQuery } from '@tanstack/react-query';
import { getModels } from '@repo/client';
import type { GpuModel } from '@repo/client';
import { useMemo } from 'react';

/**
 * Sorting direction for model attributes
 */
export type SortDirection = 'asc' | 'desc';

/**
 * Attributes that can be sorted
 */
export type SortableAttribute = keyof GpuModel | 'listingCount' | 'minPrice' | 'medianPrice' | 'maxPrice' | 'avgPrice';

/**
 * Match mode for string filters
 */
export type MatchMode = 'exact' | 'substring';

/**
 * Parameters for the useModels hook
 */
export interface UseModelsParams {
  /**
   * Filter by model name
   */
  modelName?: string;
  
  /**
   * Filter by manufacturer
   */
  manufacturer?: string;
  
  /**
   * Filter by generation
   */
  generation?: string;
  
  /**
   * Minimum VRAM in GB
   */
  minVramGb?: number;
  
  /**
   * Maximum VRAM in GB
   */
  maxVramGb?: number;
  
  /**
   * Minimum TDP in watts
   */
  minTdpWatts?: number;
  
  /**
   * Maximum TDP in watts
   */
  maxTdpWatts?: number;
  
  /**
   * Whether NVLink is supported
   */
  nvlink?: boolean;
  
  /**
   * Match mode for string filters (exact or substring)
   */
  matchMode?: MatchMode;
  
  /**
   * Attribute to sort by
   */
  sortBy?: SortableAttribute;
  
  /**
   * Sort direction
   */
  sortDirection?: SortDirection;
}

/**
 * Result returned by the useModels hook
 */
export interface UseModelsResult {
  /**
   * The filtered and sorted list of GPU models
   */
  data: GpuModel[] | undefined;
  
  /**
   * Whether the data is currently loading
   */
  isLoading: boolean;
  
  /**
   * Whether an error occurred
   */
  isError: boolean;
  
  /**
   * Error message if an error occurred
   */
  error: string | null;
  
  /**
   * Function to refetch the data
   */
  refetch: () => void;
  
  /**
   * Helper function to get models formatted for dropdown options
   */
  getDropdownOptions: () => { label: string; value: string }[];
  
  /**
   * Helper function to get a model by its name
   */
  getModelByName: (name: string) => GpuModel | undefined;
}

/**
 * Hook to fetch GPU models with filtering and sorting capabilities
 * 
 * @param params - Parameters for filtering and sorting
 * @returns Object containing the models data, loading state, error state, refetch function, and helper methods
 * 
 * @example
 * ```tsx
 * const { data, isLoading, isError, error, refetch, getDropdownOptions } = useModels({
 *   modelName: 'RTX',
 *   manufacturer: 'NVIDIA',
 *   generation: '40',
 *   minVramGb: 8,
 *   sortBy: 'vramGb',
 *   sortDirection: 'desc',
 *   matchMode: 'substring',
 * });
 * ```
 */
export function useModels({
  modelName,
  manufacturer,
  generation,
  minVramGb,
  maxVramGb,
  minTdpWatts,
  maxTdpWatts,
  nvlink,
  matchMode = 'substring',
  sortBy,
  sortDirection = 'asc',
}: UseModelsParams = {}): UseModelsResult {
  const {
    data: rawData,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<GpuModel[], Error>({
    queryKey: ['models'],
    queryFn: () => getModels(),
  });

  // Memoize the filtered and sorted data
  const data = useMemo(() => {
    if (!rawData) return undefined;

    // Start with all models
    let filteredData = [...rawData];

    // Apply filters
    if (modelName) {
      filteredData = filteredData.filter(model => {
        if (matchMode === 'exact') {
          return model.model === modelName;
        } else {
          return model.model.toLowerCase().includes(modelName.toLowerCase());
        }
      });
    }

    if (manufacturer) {
      filteredData = filteredData.filter(model => {
        // Extract manufacturer from model name (e.g., "NVIDIA RTX 4090" -> "NVIDIA")
        const modelManufacturer = model.model.split(' ')[0];
        if (!modelManufacturer) return false;
        
        if (matchMode === 'exact') {
          return modelManufacturer === manufacturer;
        } else {
          return modelManufacturer.toLowerCase().includes(manufacturer.toLowerCase());
        }
      });
    }

    if (generation) {
      filteredData = filteredData.filter(model => {
        if (!model.generation) return false;
        if (matchMode === 'exact') {
          return model.generation === generation;
        } else {
          return model.generation.toLowerCase().includes(generation.toLowerCase());
        }
      });
    }

    if (minVramGb !== undefined) {
      filteredData = filteredData.filter(model => 
        model.vramGb !== undefined && model.vramGb !== null && model.vramGb >= minVramGb
      );
    }

    if (maxVramGb !== undefined) {
      filteredData = filteredData.filter(model => 
        model.vramGb !== undefined && model.vramGb !== null && model.vramGb <= maxVramGb
      );
    }

    if (minTdpWatts !== undefined) {
      filteredData = filteredData.filter(model => 
        model.tdpWatts !== undefined && model.tdpWatts !== null && model.tdpWatts >= minTdpWatts
      );
    }

    if (maxTdpWatts !== undefined) {
      filteredData = filteredData.filter(model => 
        model.tdpWatts !== undefined && model.tdpWatts !== null && model.tdpWatts <= maxTdpWatts
      );
    }

    if (nvlink !== undefined) {
      filteredData = filteredData.filter(model => 
        model.nvlink === nvlink
      );
    }

    // Apply sorting
    if (sortBy) {
      filteredData.sort((a, b) => {
        // Use type assertion to tell TypeScript that these properties exist
        const aValue = a[sortBy as keyof typeof a];
        const bValue = b[sortBy as keyof typeof b];

        // Handle undefined or null values
        if (aValue === undefined || aValue === null) return sortDirection === 'asc' ? -1 : 1;
        if (bValue === undefined || bValue === null) return sortDirection === 'asc' ? 1 : -1;

        // Compare values
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortDirection === 'asc' 
            ? aValue.localeCompare(bValue) 
            : bValue.localeCompare(aValue);
        } else {
          return sortDirection === 'asc' 
            ? (aValue as number) - (bValue as number) 
            : (bValue as number) - (aValue as number);
        }
      });
    }

    return filteredData;
  }, [
    rawData, 
    modelName, 
    manufacturer, 
    generation, 
    minVramGb, 
    maxVramGb, 
    minTdpWatts, 
    maxTdpWatts, 
    nvlink, 
    matchMode, 
    sortBy, 
    sortDirection
  ]);

  // Helper function to get models formatted for dropdown options
  const getDropdownOptions = useMemo(() => {
    return () => {
      if (!data) return [];
      return data.map((model: GpuModel) => ({
        label: model.model,
        value: model.model,
      }));
    };
  }, [data]);

  // Helper function to get a model by its name
  const getModelByName = useMemo(() => {
    return (name: string) => {
      if (!data) return undefined;
      return data.find((model: GpuModel) => model.model === name);
    };
  }, [data]);

  return {
    data,
    isLoading,
    isError,
    error: error ? error.message : null,
    refetch: () => refetch(),
    getDropdownOptions,
    getModelByName,
  };
}
