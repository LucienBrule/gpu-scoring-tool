'use client';

import React, { useState, useMemo } from 'react';
import type { GpuReportRow } from '@repo/client';
import { Tooltip } from '../ui/Tooltip';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';

// Define the type for sort fields
type SortField = keyof GpuReportRow | 'pricePerGb';

// Define the type for filter options
interface FilterOptions {
  searchTerm: string;
  minPrice?: number;
  maxPrice?: number;
  minScore?: number;
  maxScore?: number;
  modelFilter?: string;
}

// Define the props for the ReportsDataGrid component
interface ReportsDataGridProps {
  data: GpuReportRow[];
  isLoading: boolean;
  isError: boolean;
}

export function ReportsDataGrid({
  data,
  isLoading,
  isError,
}: ReportsDataGridProps) {
  // State for pagination
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10); // Using fixed pageSize for now
  
  // State for sorting
  const [sortField, setSortField] = useState<SortField>('score');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  
  // State for filtering
  const [filters, setFilters] = useState<FilterOptions>({
    searchTerm: '',
    minPrice: undefined,
    maxPrice: undefined,
    minScore: undefined,
    maxScore: undefined,
    modelFilter: undefined,
  });
  
  // Function to handle sorting
  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc'); // Default to descending for new sort field
    }
  };
  
  // Function to handle search
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({
      ...filters,
      searchTerm: e.target.value,
    });
    setPage(1); // Reset to first page when searching
  };
  
  // Function to handle price range filtering
  const handlePriceRangeChange = (min?: number, max?: number) => {
    setFilters({
      ...filters,
      minPrice: min,
      maxPrice: max,
    });
    setPage(1); // Reset to first page when filtering
  };
  
  // Function to handle score range filtering
  const handleScoreRangeChange = (min?: number, max?: number) => {
    setFilters({
      ...filters,
      minScore: min,
      maxScore: max,
    });
    setPage(1); // Reset to first page when filtering
  };
  
  // Function to handle model filtering
  const handleModelFilterChange = (model?: string) => {
    setFilters({
      ...filters,
      modelFilter: model,
    });
    setPage(1); // Reset to first page when filtering
  };
  
  // Calculate derived data with price per GB and apply filters and sorting
  const processedData = useMemo(() => {
    if (!data) return [];
    
    return data
      .map(report => ({
        ...report,
        pricePerGb: report.price / report.vramGb,
      }))
      .filter(report => {
        // Apply search term filter
        if (filters.searchTerm && !report.canonicalModel.toLowerCase().includes(filters.searchTerm.toLowerCase())) {
          return false;
        }
        
        // Apply price range filter
        if (filters.minPrice !== undefined && report.price < filters.minPrice) {
          return false;
        }
        if (filters.maxPrice !== undefined && report.price > filters.maxPrice) {
          return false;
        }
        
        // Apply score range filter
        if (filters.minScore !== undefined && report.score < filters.minScore) {
          return false;
        }
        if (filters.maxScore !== undefined && report.score > filters.maxScore) {
          return false;
        }
        
        // Apply model filter
        if (filters.modelFilter && !report.canonicalModel.includes(filters.modelFilter)) {
          return false;
        }
        
        return true;
      })
      .sort((a, b) => {
        // Handle sorting based on the selected field
        if (sortField === 'canonicalModel') {
          const comparison = a.canonicalModel.localeCompare(b.canonicalModel);
          return sortDirection === 'asc' ? comparison : -comparison;
        } else if (sortField === 'pricePerGb') {
          const aValue = a.price / a.vramGb;
          const bValue = b.price / b.vramGb;
          const comparison = aValue - bValue;
          return sortDirection === 'asc' ? comparison : -comparison;
        } else {
          const aValue = a[sortField];
          const bValue = b[sortField];
          
          if (aValue === undefined || bValue === undefined || aValue === null || bValue === null) return 0;
          
          // Both values are now guaranteed to be non-null and non-undefined
          const comparison = aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
          return sortDirection === 'asc' ? comparison : -comparison;
        }
      });
  }, [data, filters, sortField, sortDirection]);
  
  // Calculate pagination info
  const totalItems = processedData.length;
  const totalPages = Math.ceil(totalItems / pageSize);
  
  // Handle page change
  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setPage(newPage);
    }
  };
  
  // Render sort indicator
  const renderSortIndicator = (field: SortField) => {
    if (field !== sortField) return null;
    return sortDirection === 'asc' ? ' ↑' : ' ↓';
  };
  
  // Function to determine score color based on value
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-300 font-semibold';
    if (score >= 6) return 'text-blue-300';
    if (score >= 4) return 'text-yellow-300';
    return 'text-red-300';
  };
  
  // Function to determine price/GB color based on value
  const getPricePerGbColor = (pricePerGb: number) => {
    if (pricePerGb <= 50) return 'text-green-300 font-semibold';
    if (pricePerGb <= 100) return 'text-blue-300';
    if (pricePerGb <= 150) return 'text-yellow-300';
    return 'text-red-300';
  };
  
  return (
    <div>
      {/* Search and filter controls */}
      <div className="mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="Search by model..."
            value={filters.searchTerm}
            onChange={handleSearch}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Search by model name. Use filters below for more specific results.
        </p>
      </div>
      
      {/* Advanced filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Price range filter */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-400">Price Range (USD)</label>
          <div className="flex space-x-2">
            <input
              type="number"
              placeholder="Min"
              value={filters.minPrice || ''}
              onChange={(e) => handlePriceRangeChange(
                e.target.value ? Number(e.target.value) : undefined,
                filters.maxPrice
              )}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.maxPrice || ''}
              onChange={(e) => handlePriceRangeChange(
                filters.minPrice,
                e.target.value ? Number(e.target.value) : undefined
              )}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        {/* Score range filter */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-400">Score Range</label>
          <div className="flex space-x-2">
            <input
              type="number"
              placeholder="Min"
              value={filters.minScore || ''}
              onChange={(e) => handleScoreRangeChange(
                e.target.value ? Number(e.target.value) : undefined,
                filters.maxScore
              )}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.maxScore || ''}
              onChange={(e) => handleScoreRangeChange(
                filters.minScore,
                e.target.value ? Number(e.target.value) : undefined
              )}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        {/* Model filter */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-400">Model Filter</label>
          <select
            value={filters.modelFilter || ''}
            onChange={(e) => handleModelFilterChange(e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Models</option>
            {/* Get unique models from data */}
            {Array.from(new Set(data?.map(report => report.canonicalModel) || [])).map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>
      </div>
      
      {/* Loading state */}
      {isLoading && (
        <div className="py-8">
          <Skeleton variant="table" count={5} className="mb-4" />
        </div>
      )}
      
      {/* Error state */}
      {isError && (
        <ErrorBanner
          title="Error loading reports"
          message="There was a problem fetching the reports data. Please try again later."
          severity="error"
          className="mb-4"
        />
      )}
      
      {/* Empty state */}
      {!isLoading && !isError && processedData.length === 0 && (
        <ErrorBanner
          title="No reports available"
          message="There are currently no GPU reports matching your criteria."
          severity="warning"
          className="mb-4"
        />
      )}
      
      {/* Table */}
      {!isLoading && !isError && processedData.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-gray-500:35 border border-gray-200 shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-500:35">
              <tr>
                {/* Always show Model column */}
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('canonicalModel')}
                >
                  <Tooltip content="GPU model name">
                    <span>Model{renderSortIndicator('canonicalModel')}</span>
                  </Tooltip>
                </th>
                
                {/* Always show VRAM column */}
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('vramGb')}
                >
                  <Tooltip content="Amount of video memory in gigabytes">
                    <span>VRAM{renderSortIndicator('vramGb')}</span>
                  </Tooltip>
                </th>
                
                {/* Always show Price column */}
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('price')}
                >
                  <Tooltip content="Current market price in USD">
                    <span>Price{renderSortIndicator('price')}</span>
                  </Tooltip>
                </th>
                
                {/* Always show Price/GB column */}
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('pricePerGb')}
                >
                  <Tooltip content="Price per GB of VRAM (lower is better)">
                    <span>$/GB{renderSortIndicator('pricePerGb')}</span>
                  </Tooltip>
                </th>
                
                {/* Always show Score column */}
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('score')}
                >
                  <Tooltip content="Utility score based on performance and value (higher is better)">
                    <span>Score{renderSortIndicator('score')}</span>
                  </Tooltip>
                </th>
                
                {/* Hide TDP, MIG, and NVLink columns on small screens */}
                <th 
                  className="hidden md:table-cell px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('tdpWatts')}
                >
                  <Tooltip content="Thermal Design Power in watts">
                    <span>TDP{renderSortIndicator('tdpWatts')}</span>
                  </Tooltip>
                </th>
                
                <th 
                  className="hidden md:table-cell px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('migSupport')}
                >
                  <Tooltip content="Multi-Instance GPU support level (0-7)">
                    <span>MIG{renderSortIndicator('migSupport')}</span>
                  </Tooltip>
                </th>
                
                <th 
                  className="hidden md:table-cell px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                  onClick={() => handleSort('nvlink')}
                >
                  <Tooltip content="Whether the GPU supports NVLink for multi-GPU connectivity">
                    <span>NVLink{renderSortIndicator('nvlink')}</span>
                  </Tooltip>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-500">
              {processedData
                .slice((page - 1) * pageSize, page * pageSize)
                .map((report, index) => {
                  const pricePerGb = report.price / report.vramGb;
                  
                  return (
                    <tr key={index} className="hover:bg-gray-600">
                      {/* Always show Model column */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-300" data-testid="gpu-model">
                        {report.canonicalModel}
                      </td>
                      
                      {/* Always show VRAM column */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {report.vramGb}
                      </td>
                      
                      {/* Always show Price column */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        ${report.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </td>
                      
                      {/* Always show Price/GB column */}
                      <td className={`px-6 py-4 whitespace-nowrap text-sm ${getPricePerGbColor(pricePerGb)}`}>
                        ${pricePerGb.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </td>
                      
                      {/* Always show Score column */}
                      <td className={`px-6 py-4 whitespace-nowrap text-sm ${getScoreColor(report.score)}`}>
                        {report.score.toFixed(2)}
                      </td>
                      
                      {/* Hide TDP, MIG, and NVLink columns on small screens */}
                      <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {report.tdpWatts}
                      </td>
                      
                      <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {report.migSupport}
                      </td>
                      
                      <td className="hidden md:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {report.nvlink ? 'Yes' : 'No'}
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      )}
      
      {/* Pagination controls */}
      {!isLoading && !isError && processedData.length > 0 && (
        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center">
            <span className="text-sm text-gray-700">
              Showing <span className="font-medium">{Math.min(totalItems, (page - 1) * pageSize + 1)}</span> to{' '}
              <span className="font-medium">{Math.min(totalItems, page * pageSize)}</span> of{' '}
              <span className="font-medium">{totalItems}</span> results
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(page - 1)}
              disabled={page === 1}
              className={`px-3 py-1 rounded  ${
                page === 1
                  ? 'bg-gray-700 text-gray-300 cursor-not-allowed'
                    : 'bg-gray-400 text-white hover:bg-gray-50 hover:text-blue-400 cursor-pointer'
              }`}
            >
              Previous
            </button>
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              // Show pages around the current page
              let pageNum;
              if (totalPages <= 5) {
                pageNum = i + 1;
              } else if (page <= 3) {
                pageNum = i + 1;
              } else if (page >= totalPages - 2) {
                pageNum = totalPages - 4 + i;
              } else {
                pageNum = page - 2 + i;
              }
              
              return (
                <button
                  key={pageNum}
                  onClick={() => handlePageChange(pageNum)}
                  className={`px-3 py-1 rounded ${
                    page === pageNum
                      ? 'bg-blue-400 text-white'
                      : 'bg-gray-400 text-white hover:bg-blue-500 hover:text-gray-300 cursor-pointer'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              onClick={() => handlePageChange(page + 1)}
              disabled={page === totalPages}
              className={`px-3 py-1 rounded ${
                page === totalPages
                  ? 'bg-gray-700 text-gray-300 cursor-not-allowed'
                    : 'bg-gray-400 text-white hover:bg-gray-50 hover:text-blue-400 cursor-pointer'
              }`}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}