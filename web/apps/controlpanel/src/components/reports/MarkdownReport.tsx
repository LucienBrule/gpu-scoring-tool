'use client';

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ReportDTO, GpuReportRow } from '@repo/client';
import { Card, CardContent, CardHeader, CardTitle } from '@repo/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@repo/ui/tabs';
import { Badge } from '@repo/ui/badge';
import { ReportsDataGrid } from './ReportsDataGrid';

interface MarkdownReportProps {
  report: ReportDTO | GpuReportRow;
}

export function MarkdownReport({ report }: MarkdownReportProps) {
  const [activeTab, setActiveTab] = useState('report');
  
  // Check if the report has the properties expected by a ReportDTO
  const hasMarkdown = 'markdown' in report;
  const hasSummaryStats = 'summaryStats' in report;
  const hasTopRanked = 'topRanked' in report;
  const hasScoringWeights = 'scoringWeights' in report;

  // Determine which tabs to show based on the report type
  const availableTabs = ['report'];
  if (hasSummaryStats || hasTopRanked) availableTabs.push('stats');
  if (hasScoringWeights) availableTabs.push('weights');

  // If the active tab is not available, default to the first available tab
  if (!availableTabs.includes(activeTab)) {
    setActiveTab(availableTabs[0]);
  }

  // For GpuReportRow, use the ReportsDataGrid component
  if (!hasMarkdown) {
    // Cast the report to GpuReportRow
    const gpuReport = report as GpuReportRow;
    
    // Create an array with the single report for ReportsDataGrid
    const reportData = [gpuReport];
    
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>GPU Model: {gpuReport.canonicalModel}</CardTitle>
          </CardHeader>
          <CardContent>
            <ReportsDataGrid 
              data={reportData}
              isLoading={false}
              isError={false}
            />
          </CardContent>
        </Card>
      </div>
    );
  }

  // For ReportDTO, show the full report with tabs
  return (
    <div className="space-y-6">
      <Tabs defaultValue="report" value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className={availableTabs.length === 1 ? "grid grid-cols-1 mb-6" : 
                  availableTabs.length === 2 ? "grid grid-cols-2 mb-6" : 
                  "grid grid-cols-3 mb-6"}>
          {availableTabs.includes('report') && <TabsTrigger value="report">Report</TabsTrigger>}
          {availableTabs.includes('stats') && <TabsTrigger value="stats">Statistics</TabsTrigger>}
          {availableTabs.includes('weights') && <TabsTrigger value="weights">Scoring Weights</TabsTrigger>}
        </TabsList>
        
        {/* Report Tab - Markdown Content */}
        {hasMarkdown && (
          <TabsContent value="report" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>GPU Market Report</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown>{(report as ReportDTO).markdown || ''}</ReactMarkdown>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        )}
        
        {/* Stats Tab - Summary Statistics */}
        {(hasSummaryStats || hasTopRanked) && (
          <TabsContent value="stats" className="space-y-6">
            {hasSummaryStats && (
              <Card>
                <CardHeader>
                  <CardTitle>Summary Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries((report as ReportDTO).summaryStats ?? {}).map(([key, value]) => (
                      <div key={key} className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-sm font-medium text-gray-400 mb-1">{formatKey(key)}</h3>
                        <p className="text-xl font-semibold">{value}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
            
            {hasTopRanked && (
              <Card>
                <CardHeader>
                  <CardTitle>Top Ranked GPUs</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {((report as ReportDTO).topRanked ?? []).map((model, index) => (
                      <Badge key={model} variant={getBadgeVariant(index)}>
                        {index + 1}. {model}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        )}
        
        {/* Weights Tab - Scoring Weights */}
        {hasScoringWeights && (
          <TabsContent value="weights" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Scoring Weights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries((report as ReportDTO).scoringWeights ?? {}).map(([key, value]) => (
                    <div key={key} className="space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">{formatKey(key)}</span>
                        <span className="text-sm text-gray-400">{(value * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2.5">
                        <div 
                          className="bg-blue-600 h-2.5 rounded-full" 
                          style={{ width: `${value * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}

// Helper function to format keys for display
function formatKey(key: string): string {
  return key
    .split(/(?=[A-Z])|_/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

// Helper function to get badge variant based on ranking
function getBadgeVariant(index: number): "default" | "secondary" | "destructive" | "outline" {
  if (index === 0) return "default"; // First place - primary color
  if (index === 1) return "secondary"; // Second place - secondary color
  if (index === 2) return "outline"; // Third place - outline
  return "destructive"; // Others - destructive color
}

export default MarkdownReport;