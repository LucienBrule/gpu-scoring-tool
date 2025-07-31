#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define paths
const OPENAPI_PATH = path.join(__dirname, '..', 'openapi.json');
const HOOKS_DIR = path.join(__dirname, '..', 'src', 'hooks');

console.log('🔄 Generating hooks from OpenAPI schema...');

// Read the OpenAPI schema
const openApiSchema = JSON.parse(fs.readFileSync(OPENAPI_PATH, 'utf8'));

// Create hooks for specific endpoints
const endpoints = [
  {
    path: '/api/listings/legacy',
    operationId: 'get_listings_legacy_api_listings_legacy_get',
    responseType: 'GPUListingDTO',
    isArray: true,
    hookName: 'useListingsLegacy',
    methodName: 'getListingsLegacyApiListingsLegacyGet',
    parameters: [
      { name: 'model', type: 'string' },
      { name: 'quantized', type: 'boolean' }
    ]
  },
  {
    path: '/api/models',
    operationId: 'get_models_api_models_get',
    responseType: 'GPUModelDTO',
    isArray: true,
    hookName: 'useModels',
    methodName: 'getModelsApiModelsGet',
    parameters: []
  },
  {
    path: '/api/report',
    operationId: 'get_report_api_report_get',
    responseType: 'ReportDTO',
    isArray: false,
    hookName: 'useReport',
    methodName: 'getReportApiReportGet',
    parameters: []
  }
];

// Generate hooks for each endpoint
for (const endpoint of endpoints) {
  const { hookName, methodName, responseType, isArray, parameters } = endpoint;
  
  let hookContent;
  
  if (parameters.length > 0) {
    // Hook with parameters
    hookContent = `import { useQuery } from '@tanstack/react-query';
import type { ${responseType} } from '@repo/client-generated';

export interface ${hookName}Filters {
${parameters.map(p => `  ${p.name}?: ${p.type};`).join('\n')}
}

export interface ${hookName}Result {
  data: ${isArray ? `${responseType}[]` : responseType} | undefined;
  isLoading: boolean;
  isError: boolean;
  refetch: () => void;
}

/**
 * Hook to fetch data from ${endpoint.path}
 * @param filters Optional filters to apply to the query
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function ${hookName}(filters?: ${hookName}Filters): ${hookName}Result {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<${isArray ? `${responseType}[]` : responseType}, Error>({
    queryKey: ['${hookName.toLowerCase()}', filters],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching ${endpoint.path} with filters:', filters);
      return Promise.resolve(${isArray ? '[]' : '{}'} as ${isArray ? `${responseType}[]` : responseType});
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
`;
  } else {
    // Hook without parameters
    hookContent = `import { useQuery } from '@tanstack/react-query';
import type { ${responseType} } from '@repo/client-generated';

/**
 * Hook to fetch data from ${endpoint.path}
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function ${hookName}() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<${isArray ? `${responseType}[]` : responseType}, Error>({
    queryKey: ['${hookName.toLowerCase()}'],
    queryFn: () => {
      // TODO: Replace this with actual API call
      console.log('Fetching ${endpoint.path}');
      return Promise.resolve(${isArray ? '[]' : '{}'} as ${isArray ? `${responseType}[]` : responseType});
    },
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
`;
  }
  
  // Write hook file
  const hookFilePath = path.join(HOOKS_DIR, `${hookName}.ts`);
  fs.writeFileSync(hookFilePath, hookContent);
  console.log(`✅ Generated hook: ${hookName}`);
}

// Update hooks/index.ts
const indexPath = path.join(HOOKS_DIR, 'index.ts');
const indexContent = fs.readFileSync(indexPath, 'utf8');
const newExports = endpoints.map(e => `export * from './${e.hookName}.js';`).join('\n');
const updatedIndexContent = indexContent.trim() + '\n' + newExports;
fs.writeFileSync(indexPath, updatedIndexContent);
console.log('✅ Updated hooks/index.ts');

console.log('✅ Hook generation completed successfully!');
console.log('NOTE: The generated hooks contain placeholder implementations.');
console.log('You will need to update client.ts to add the actual API calls.');