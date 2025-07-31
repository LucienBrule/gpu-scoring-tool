'use client';

import { hooks } from '@repo/client';

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
          <div className="text-gray-500">Loading health status...</div>
        )}

        {!loading && status && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            <p className="font-bold">Status: {status}</p>
          </div>
        )}

        {!loading && error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p className="font-bold">Error:</p>
            <p>{error}</p>
          </div>
        )}
        
        {!loading && !status && !error && (
          <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
            <p className="font-bold">Warning:</p>
            <p>No status information received from the server. The server might be running but returning an unexpected response.</p>
          </div>
        )}
      </div>

      <div className="text-sm text-gray-500">
        <p>This page demonstrates integration with the backend API using the OpenAPI-generated client.</p>
        <p>The health check endpoint is called when the page loads, and the result is displayed above.</p>
      </div>
    </div>
  );
}
