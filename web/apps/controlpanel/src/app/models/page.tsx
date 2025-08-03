'use client';

import React, { useState, useMemo } from 'react';
import { useGpuModels } from '@/hooks/useGpuModels';
import type { GPUModelDTO } from '@repo/client';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';
import { Input } from '@repo/ui/input';
import { Search, SortAsc, SortDesc } from 'lucide-react';

// Define the type for sort fields
type SortField = keyof GPUModelDTO;

export default function ModelsPage() {
  // State for search and filtering
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState<SortField>('model');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  
  // Fetch models data using the useGpuModels hook
  const { data, isLoading, isError, error } = useGpuModels();
  
  // Function to handle sorting
  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };
  
  // Function to handle search
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };
  
  // Filter and sort the data
  const filteredAndSortedData = useMemo(() => {
    if (!data) return [];
    
    return [...data]
      .filter(model => {
        if (!searchTerm) return true;
        
        const searchLower = searchTerm.toLowerCase();
        return (
          model.model.toLowerCase().includes(searchLower) ||
          (model.generation && model.generation.toLowerCase().includes(searchLower))
        );
      })
      .sort((a, b) => {
        const aValue = a[sortField];
        const bValue = b[sortField];
        
        if (aValue === undefined || bValue === undefined) return 0;
        
        let comparison = 0;
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          comparison = aValue.localeCompare(bValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          comparison = aValue - bValue;
        } else if (typeof aValue === 'boolean' && typeof bValue === 'boolean') {
          comparison = aValue === bValue ? 0 : aValue ? 1 : -1;
        }
        
        return sortDirection === 'asc' ? comparison : -comparison;
      });
  }, [data, searchTerm, sortField, sortDirection]);
  
  // Function to render sort indicator
  const renderSortIndicator = (field: SortField) => {
    if (field !== sortField) return null;
    return sortDirection === 'asc' ? <SortAsc className="inline h-4 w-4 ml-1" /> : <SortDesc className="inline h-4 w-4 ml-1" />;
  };
  
  // Function to format price
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price);
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">GPU Models</h1>
      </div>
      
      {/* Search and filter */}
      <div className="mb-6">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <Input
            type="text"
            placeholder="Search by model name or generation..."
            value={searchTerm}
            onChange={handleSearch}
            className="pl-10"
          />
        </div>
      </div>
      
      {/* Loading state */}
      {isLoading && (
        <div className="space-y-4">
          <Skeleton variant="rect" height={50} />
          <Skeleton variant="rect" height={400} />
        </div>
      )}
      
      {/* Error state */}
      {isError && (
        <ErrorBanner
          title="Error loading GPU models"
          message={error?.message || "There was a problem fetching the GPU models. Please try again later."}
          severity="error"
        />
      )}
      
      {/* Empty state */}
      {!isLoading && !isError && filteredAndSortedData.length === 0 && (
        <ErrorBanner
          title="No GPU models found"
          message={searchTerm ? `No models matching "${searchTerm}" were found.` : "No GPU models are available."}
          severity="warning"
        />
      )}
      
      {/* Table view */}
      {!isLoading && !isError && filteredAndSortedData.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-gray-500:35 border border-gray-200 shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-500:35">
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('model')}
                >
                  Model {renderSortIndicator('model')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('generation')}
                >
                  Generation {renderSortIndicator('generation')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('vramGb')}
                >
                  VRAM (GB) {renderSortIndicator('vramGb')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('tdpWatts')}
                >
                  TDP (W) {renderSortIndicator('tdpWatts')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('cudaCores')}
                >
                  CUDA Cores {renderSortIndicator('cudaCores')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('nvlink')}
                >
                  NVLink {renderSortIndicator('nvlink')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('medianPrice')}
                >
                  Median Price {renderSortIndicator('medianPrice')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('listingCount')}
                >
                  Listings {renderSortIndicator('listingCount')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-500">
              {filteredAndSortedData.map((model) => (
                <tr key={model.model} className="hover:bg-gray-600">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-300">
                    {model.model}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.generation || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.vramGb || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.tdpWatts || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.cudaCores || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.nvlink ? 'Yes' : 'No'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {formatPrice(model.medianPrice)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {model.listingCount}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}