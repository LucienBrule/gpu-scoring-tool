'use client';

import * as hooks from '@/hooks';
import { Skeleton } from '@/components/ui/skeleton';
import { ErrorBanner } from '@/components/ui/error-banner';

// This disables static generation for this page
export const dynamic = 'force-dynamic';
// This disables prerendering for this page
export const runtime = 'edge';

export default function IntegrationTestPage() {
  const { status, error, loading, refetch } = hooks.useHealthCheck();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Integration Test</h1>

      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-xl font-semibold">Health Check</h2>
          <button 
            onClick={() => refetch()} 
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            disabled={loading}
          >
            {loading ? 'Refreshing...' : 'Refresh Status'}
          </button>
        </div>

        {loading && (
          <Skeleton variant="text" count={2} className="w-full max-w-md" />
        )}

        {!loading && status && (
          <ErrorBanner
            title="Status"
            message={status}
            severity="success"
          />
        )}

        {!loading && error && (
          <ErrorBanner
            title="Error"
            message={error}
            severity="error"
            onRetry={() => refetch()}
          />
        )}
        
        {!loading && !status && !error && (
          <ErrorBanner
            title="Warning"
            message="No status information received from the server. The server might be running but returning an unexpected response."
            severity="warning"
          />
        )}
      </div>

      <div className="text-sm text-gray-500">
        <p>This page demonstrates integration with the backend API using the OpenAPI-generated client.</p>
        <p>The health check endpoint is called when the page loads, and the result is displayed above.</p>
      </div>
    </div>
  );
}
