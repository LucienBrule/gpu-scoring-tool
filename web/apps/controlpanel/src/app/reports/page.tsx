'use client';

import React, { useState } from 'react';
import { useGpuReports } from '@/hooks/useGpuReports';
import { MarkdownReport } from '@/components/reports/MarkdownReport';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';
import { Button } from '@repo/ui/button';
import { Input } from '@repo/ui/input';
import { Label } from '@repo/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@repo/ui/select';

// This disables static generation for this page
export const dynamic = 'force-dynamic';
// This disables prerendering for this page
export const runtime = 'edge';

export default function ReportsPage() {
  // State for filters
  const [modelFilter, setModelFilter] = useState<string | undefined>(undefined);
  const [limit, setLimit] = useState<number>(10);
  
  // Fetch reports using the useGpuReports hook
  const { 
    data, 
    isLoading, 
    isError, 
    error, 
    refetch 
  } = useGpuReports({
    model: modelFilter,
    limit,
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">GPU Market Reports</h1>
        <Button 
          onClick={() => refetch()} 
          disabled={isLoading}
          data-testid="refresh-button"
        >
          {isLoading ? 'Refreshing...' : 'Refresh Reports'}
        </Button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <div className="space-y-2">
          <Label htmlFor="modelFilter">Filter by Model</Label>
          <Input 
            id="modelFilter" 
            placeholder="e.g., RTX 3080" 
            value={modelFilter || ''}
            onChange={(e) => setModelFilter(e.target.value || undefined)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="limit">Number of Reports</Label>
          <Select 
            value={limit.toString()} 
            onValueChange={(value) => setLimit(parseInt(value))}
          >
            <SelectTrigger id="limit">
              <SelectValue placeholder="Select limit" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">1 Report</SelectItem>
              <SelectItem value="5">5 Reports</SelectItem>
              <SelectItem value="10">10 Reports</SelectItem>
              <SelectItem value="25">25 Reports</SelectItem>
              <SelectItem value="50">50 Reports</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Loading state */}
      {isLoading && (
        <div className="space-y-6">
          <Skeleton variant="card" height={400} />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Skeleton variant="card" height={150} />
            <Skeleton variant="card" height={150} />
            <Skeleton variant="card" height={150} />
          </div>
        </div>
      )}

      {/* Error state */}
      {isError && (
        <ErrorBanner
          title="Error loading reports"
          message={typeof error === 'string' ? error : error?.message || "There was a problem fetching the reports. Please try again later."}
          severity="error"
          onRetry={() => refetch()}
        />
      )}

      {/* Empty state */}
      {!isLoading && !isError && (!data || data.length === 0) && (
        <ErrorBanner
          title="No reports available"
          message="There are currently no GPU market reports matching your criteria."
          severity="warning"
        />
      )}

      {/* Reports */}
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="space-y-8">
          {data.map((report, index) => (
            <div key={index} className="border border-gray-700 rounded-lg p-6" data-testid="report-row">
              <MarkdownReport report={report} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}