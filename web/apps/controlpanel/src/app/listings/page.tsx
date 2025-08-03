'use client';

import React, { useState, useEffect } from 'react';
import * as hooks from '@/hooks';
import type { GpuReportRow } from '@repo/client';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';

// // This disables static generation for this page
// export const dynamic = 'force-dynamic';
// // This disables prerendering for this page
// export const runtime = 'edge';

// Define the type for sort fields
type SortField = 'canonicalModel' | 'price' | 'score' | 'listing_age';

export default function ListingsPage() {
  // State for pagination
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  
  // State for sorting
  const [sortField, setSortField] = useState<SortField>('price');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  
  // State for search filtering
  const [searchTerm, setSearchTerm] = useState('');
  
  // Fetch listings data using the useListings hook
  const { data, isLoading, isError, error, refetch } = hooks.useListings({
    page,
    pageSize,
    // Additional filters can be added here when available
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
    setSearchTerm(e.target.value);
    setPage(1); // Reset to first page when searching
  };
  
  // Filter and sort the data
  const filteredAndSortedData = data ? [...data].filter(listing => {
    if (!searchTerm) return true;
    
    const searchTermLower = searchTerm.toLowerCase();
    
    // Search in canonicalModel (available)
    // Note: title and seller fields are not available in the current data model
    return listing.canonicalModel.toLowerCase().includes(searchTermLower);
  }).sort((a, b) => {
    // Handle sorting based on the selected field
    if (sortField === 'canonicalModel') {
      const comparison = a.canonicalModel.localeCompare(b.canonicalModel);
      return sortDirection === 'asc' ? comparison : -comparison;
    } else if (sortField === 'price') {
      const comparison = a.price - b.price;
      return sortDirection === 'asc' ? comparison : -comparison;
    } else if (sortField === 'score') {
      const comparison = a.score - b.score;
      return sortDirection === 'asc' ? comparison : -comparison;
    } else if (sortField === 'listing_age') {
      // Placeholder for listing_age sorting
      // This will be implemented when the backend adds support for it
      return 0;
    }
    
    return 0;
  }) : [];
  
  // Calculate pagination info
  const totalItems = filteredAndSortedData.length;
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
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">GPU Listings</h1>
        <button 
          onClick={() => refetch()} 
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          disabled={isLoading}
        >
          {isLoading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </div>
      
      {/* Search input */}
      <div className="mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="Search by model..."
            value={searchTerm}
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
          Search by model name. More search fields will be available in future updates.
        </p>
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
          title="Error loading listings"
          message={error || 'There was a problem fetching the listings data. Please try again later.'}
          severity="error"
          onRetry={() => refetch()}
          className="mb-4"
        />
      )}
      
      {/* Empty state */}
      {!isLoading && !isError && filteredAndSortedData.length === 0 && (
        <ErrorBanner
          title="No listings available"
          message="There are currently no GPU listings matching your criteria."
          severity="warning"
          className="mb-4"
        />
      )}
      
      {/* Table */}
      {!isLoading && !isError && filteredAndSortedData.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-50">
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('canonicalModel')}
                >
                  Model{renderSortIndicator('canonicalModel')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('price')}
                >
                  Price (USD){renderSortIndicator('price')}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('score')}
                >
                  Score{renderSortIndicator('score')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  VRAM (GB)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  TDP (Watts)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  NVLink
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredAndSortedData
                .slice((page - 1) * pageSize, page * pageSize)
                .map((listing, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {listing.canonicalModel}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    ${listing.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {listing.score.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {listing.vramGb}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {listing.tdpWatts}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {listing.nvlink ? 'Yes' : 'No'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {/* Pagination controls */}
      {!isLoading && !isError && filteredAndSortedData.length > 0 && (
        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center text-sm text-gray-500">
            <span className="text-sm text-gray-100">
              Showing <span className="font-medium text-gray-100">{Math.min(totalItems, (page - 1) * pageSize + 1)}</span> to{' '}
              <span className="font-medium">{Math.min(totalItems, page * pageSize)}</span> of{' '}
              <span className="font-medium">{totalItems}</span> results
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(page - 1)}
              disabled={page === 1}
              className={`px-3 py-1 rounded ${
                page === 1
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
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
                      ? 'bg-blue-500 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
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
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
              }`}
            >
              Next
            </button>
          </div>
        </div>
      )}
      
      <div className="mt-4 text-sm text-gray-500">
        <p>Note: This table displays GPU listings data with calculated utility scores.</p>
        <p>Click on column headers to sort the data.</p>
      </div>
    </div>
  );
}