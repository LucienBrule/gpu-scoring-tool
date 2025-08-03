'use client';

import React, { useState, useMemo } from 'react';
import { useForecastDeltas, ForecastDelta } from '@/hooks/useForecastDeltas';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';
import { Button } from '@repo/ui/button';
import { Input } from '@repo/ui/input';
import { Label } from '@repo/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@repo/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@repo/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@repo/ui/select';
import { Badge } from '@repo/ui/badge';
import { ArrowDown, ArrowUp, Download, Calendar, Filter } from 'lucide-react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, Cell 
} from 'recharts';

// This disables static generation for this page
export const dynamic = 'force-dynamic';
// This disables prerendering for this page
export const runtime = 'edge';

// Define regions for the filter
const REGIONS = [
  { value: 'all', label: 'All Regions' },
  { value: 'us', label: 'United States' },
  { value: 'eu', label: 'Europe' },
  { value: 'asia', label: 'Asia' },
  { value: 'other', label: 'Other Regions' },
];

// Define time ranges for the filter
const TIME_RANGES = [
  { value: '7d', label: 'Last 7 Days' },
  { value: '30d', label: 'Last 30 Days' },
  { value: '90d', label: 'Last Quarter' },
  { value: '365d', label: 'Last Year' },
];

export default function ForecastPage() {
  // State for filters
  const [modelFilter, setModelFilter] = useState<string>('');
  const [regionFilter, setRegionFilter] = useState<string>('all');
  const [timeRange, setTimeRange] = useState<string>('30d');
  const [minPriceChangePct, setMinPriceChangePct] = useState<number>(5);
  const [limit, setLimit] = useState<number>(50);
  const [viewMode, setViewMode] = useState<'chart' | 'table'>('chart');
  const [chartType, setChartType] = useState<'line' | 'bar'>('bar');
  
  // Calculate the date for the selected time range
  const afterDate = useMemo(() => {
    const date = new Date();
    switch (timeRange) {
      case '7d':
        date.setDate(date.getDate() - 7);
        break;
      case '30d':
        date.setDate(date.getDate() - 30);
        break;
      case '90d':
        date.setDate(date.getDate() - 90);
        break;
      case '365d':
        date.setDate(date.getDate() - 365);
        break;
      default:
        date.setDate(date.getDate() - 30);
    }
    return date;
  }, [timeRange]);
  
  // Fetch forecast deltas using the useForecastDeltas hook
  const { 
    data, 
    isLoading, 
    isError, 
    error, 
    refetch,
    formatPercentChange 
  } = useForecastDeltas({
    model: modelFilter || undefined,
    minPriceChangePct,
    after: afterDate,
    region: regionFilter === 'all' ? undefined : regionFilter,
    limit,
  });
  
  // Prepare data for charts
  const chartData = useMemo(() => {
    if (!data) return [];
    
    // Sort by timestamp
    return [...data].sort((a, b) => 
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );
  }, [data]);
  
  // Group data by model for aggregated view
  const modelAggregatedData = useMemo(() => {
    if (!data) return [];
    
    const modelMap = new Map<string, { 
      model: string, 
      avgPriceChangePct: number, 
      count: number,
      totalOldPrice: number,
      totalNewPrice: number
    }>();
    
    data.forEach(delta => {
      if (!modelMap.has(delta.model)) {
        modelMap.set(delta.model, { 
          model: delta.model, 
          avgPriceChangePct: 0, 
          count: 0,
          totalOldPrice: 0,
          totalNewPrice: 0
        });
      }
      
      const entry = modelMap.get(delta.model)!;
      entry.totalOldPrice += delta.oldPrice;
      entry.totalNewPrice += delta.newPrice;
      entry.count += 1;
    });
    
    // Calculate averages and convert to array
    return Array.from(modelMap.values()).map(entry => ({
      ...entry,
      avgPriceChangePct: entry.count > 0 
        ? ((entry.totalNewPrice - entry.totalOldPrice) / entry.totalOldPrice) * 100
        : 0
    })).sort((a, b) => Math.abs(b.avgPriceChangePct) - Math.abs(a.avgPriceChangePct));
  }, [data]);
  
  // Function to export data as CSV
  const exportData = () => {
    if (!data) return;
    
    // Create CSV content
    const headers = ['Model', 'Old Price', 'New Price', 'Price Change %', 'Region', 'Timestamp', 'Listing ID', 'Source'];
    const csvContent = [
      headers.join(','),
      ...data.map(delta => [
        delta.model,
        delta.oldPrice,
        delta.newPrice,
        delta.priceChangePct,
        delta.region || 'N/A',
        delta.timestamp,
        delta.listingId,
        delta.source || 'N/A'
      ].join(','))
    ].join('\n');
    
    // Create and download the file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `forecast-deltas-${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  // Function to format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Price Forecast Deltas</h1>
        <div className="flex items-center space-x-2">
          <Button 
            variant={viewMode === 'chart' ? 'default' : 'outline'}
            onClick={() => setViewMode('chart')}
          >
            Chart
          </Button>
          <Button 
            variant={viewMode === 'table' ? 'default' : 'outline'}
            onClick={() => setViewMode('table')}
          >
            Table
          </Button>
          <Button 
            variant="outline" 
            onClick={exportData}
            disabled={!data || data.length === 0}
          >
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
        </div>
      </div>
      
      {/* Filters */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center">
            <Filter className="h-5 w-5 mr-2" />
            Filters
          </CardTitle>
          <CardDescription>
            Adjust filters to refine the forecast data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="modelFilter">GPU Model</Label>
              <Input 
                id="modelFilter" 
                placeholder="e.g., RTX 3080" 
                value={modelFilter}
                onChange={(e) => setModelFilter(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="regionFilter">Region</Label>
              <Select 
                value={regionFilter} 
                onValueChange={setRegionFilter}
              >
                <SelectTrigger id="regionFilter">
                  <SelectValue placeholder="Select region" />
                </SelectTrigger>
                <SelectContent>
                  {REGIONS.map((region) => (
                    <SelectItem key={region.value} value={region.value}>
                      {region.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="timeRange">Time Range</Label>
              <Select 
                value={timeRange} 
                onValueChange={setTimeRange}
              >
                <SelectTrigger id="timeRange">
                  <SelectValue placeholder="Select time range" />
                </SelectTrigger>
                <SelectContent>
                  {TIME_RANGES.map((range) => (
                    <SelectItem key={range.value} value={range.value}>
                      {range.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="minPriceChangePct">Min Price Change %</Label>
              <div className="flex items-center space-x-2">
                <Input 
                  id="minPriceChangePct" 
                  type="number" 
                  value={minPriceChangePct}
                  onChange={(e) => setMinPriceChangePct(Number(e.target.value))}
                  min={0}
                  max={100}
                  step={1}
                />
                <Button 
                  variant="outline" 
                  onClick={() => refetch()}
                  disabled={isLoading}
                >
                  Apply
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Loading state */}
      {isLoading && (
        <div className="space-y-6">
          <Skeleton variant="rect" height={400} />
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
          title="Error loading forecast data"
          message={error || "There was a problem fetching the forecast data. Please try again later."}
          severity="error"
          onRetry={() => refetch()}
        />
      )}
      
      {/* Empty state */}
      {!isLoading && !isError && (!data || data.length === 0) && (
        <ErrorBanner
          title="No forecast data available"
          message="There are currently no price forecast deltas matching your criteria. Try adjusting your filters."
          severity="warning"
        />
      )}
      
      {/* Chart View */}
      {!isLoading && !isError && data && data.length > 0 && viewMode === 'chart' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Price Change by Model</CardTitle>
                <div className="flex items-center space-x-2">
                  <Button 
                    variant={chartType === 'bar' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setChartType('bar')}
                  >
                    Bar
                  </Button>
                  <Button 
                    variant={chartType === 'line' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setChartType('line')}
                  >
                    Line
                  </Button>
                </div>
              </div>
              <CardDescription>
                Average price change percentage by GPU model
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  {chartType === 'bar' ? (
                    <BarChart
                      data={modelAggregatedData}
                      margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="model" 
                        angle={-45} 
                        textAnchor="end" 
                        height={70} 
                        tick={{ fontSize: 12 }}
                      />
                      <YAxis 
                        label={{ 
                          value: 'Price Change %', 
                          angle: -90, 
                          position: 'insideLeft',
                          style: { textAnchor: 'middle' }
                        }} 
                      />
                      <Tooltip 
                        formatter={(value: number) => [`${value.toFixed(2)}%`, 'Price Change']}
                        labelFormatter={(label) => `Model: ${label}`}
                      />
                      <Legend />
                      <Bar dataKey="avgPriceChangePct" name="Price Change %" fill="#8884d8">
                        {modelAggregatedData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={entry.avgPriceChangePct >= 0 ? '#4ade80' : '#f87171'} 
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  ) : (
                    <LineChart
                      data={chartData}
                      margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="timestamp" 
                        angle={-45} 
                        textAnchor="end" 
                        height={70} 
                        tick={{ fontSize: 12 }}
                        tickFormatter={formatDate}
                      />
                      <YAxis 
                        label={{ 
                          value: 'Price Change %', 
                          angle: -90, 
                          position: 'insideLeft',
                          style: { textAnchor: 'middle' }
                        }} 
                      />
                      <Tooltip 
                        formatter={(value: number) => [`${value.toFixed(2)}%`, 'Price Change']}
                        labelFormatter={(label) => formatDate(label)}
                      />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="priceChangePct" 
                        name="Price Change %" 
                        stroke="#8884d8" 
                        activeDot={{ r: 8 }} 
                      />
                    </LineChart>
                  )}
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Average Change</CardTitle>
                <CardDescription>
                  Average price change across all models
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  {data && data.length > 0 ? (
                    <>
                      <div className="text-4xl font-bold mb-2">
                        {formatPercentChange(
                          data.reduce((sum, delta) => sum + delta.priceChangePct, 0) / data.length
                        )}
                      </div>
                      <div className="text-sm text-gray-500">
                        Based on {data.length} price changes
                      </div>
                    </>
                  ) : (
                    <div className="text-gray-500">No data available</div>
                  )}
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Largest Increase</CardTitle>
                <CardDescription>
                  Model with the largest price increase
                </CardDescription>
              </CardHeader>
              <CardContent>
                {data && data.length > 0 ? (
                  (() => {
                    const maxIncrease = data.reduce((max, delta) => 
                      delta.priceChangePct > max.priceChangePct ? delta : max, data[0]);
                    return (
                      <div className="text-center">
                        <div className="text-xl font-bold mb-2">{maxIncrease.model}</div>
                        <div className="text-3xl font-bold text-green-500 flex items-center justify-center">
                          <ArrowUp className="h-6 w-6 mr-1" />
                          {formatPercentChange(maxIncrease.priceChangePct)}
                        </div>
                        <div className="text-sm text-gray-500 mt-2">
                          {formatDate(maxIncrease.timestamp)}
                        </div>
                      </div>
                    );
                  })()
                ) : (
                  <div className="text-center text-gray-500">No data available</div>
                )}
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Largest Decrease</CardTitle>
                <CardDescription>
                  Model with the largest price decrease
                </CardDescription>
              </CardHeader>
              <CardContent>
                {data && data.length > 0 ? (
                  (() => {
                    const maxDecrease = data.reduce((min, delta) => 
                      delta.priceChangePct < min.priceChangePct ? delta : min, data[0]);
                    return (
                      <div className="text-center">
                        <div className="text-xl font-bold mb-2">{maxDecrease.model}</div>
                        <div className="text-3xl font-bold text-red-500 flex items-center justify-center">
                          <ArrowDown className="h-6 w-6 mr-1" />
                          {formatPercentChange(maxDecrease.priceChangePct)}
                        </div>
                        <div className="text-sm text-gray-500 mt-2">
                          {formatDate(maxDecrease.timestamp)}
                        </div>
                      </div>
                    );
                  })()
                ) : (
                  <div className="text-center text-gray-500">No data available</div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      )}
      
      {/* Table View */}
      {!isLoading && !isError && data && data.length > 0 && viewMode === 'table' && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-gray-500:35 border border-gray-200 shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-500:35">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Old Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  New Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Change %
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Region
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">
                  Source
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-500">
              {data.map((delta, index) => (
                <tr key={index} className="hover:bg-gray-600">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-300">
                    {delta.model}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    ${delta.oldPrice.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    ${delta.newPrice.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <Badge variant={delta.priceChangePct >= 0 ? "default" : "destructive"}>
                      {delta.priceChangePct >= 0 ? (
                        <ArrowUp className="h-3 w-3 mr-1" />
                      ) : (
                        <ArrowDown className="h-3 w-3 mr-1" />
                      )}
                      {formatPercentChange(delta.priceChangePct)}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {delta.region || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {formatDate(delta.timestamp)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {delta.source || 'N/A'}
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