#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Base directory of this script (i.e. packages/client/scripts/)
const SCRIPT_DIR = __dirname;

// Path to the OpenAPI schema
const OPENAPI_FILE = path.join(SCRIPT_DIR, '..', 'openapi.json');

// Path to the hooks directory
const HOOKS_DIR = path.join(SCRIPT_DIR, '..', 'src', 'hooks');

// Path to the client.ts file
const CLIENT_FILE = path.join(SCRIPT_DIR, '..', 'src', 'client.ts');

// Path to the hooks/index.ts file
const HOOKS_INDEX_FILE = path.join(HOOKS_DIR, 'index.ts');

console.log('🔄 Generating hooks from OpenAPI schema...');

try {
  // Read the OpenAPI schema
  const openApiSchema = JSON.parse(fs.readFileSync(OPENAPI_FILE, 'utf8'));
  
  // Read the current client.ts file
  const clientContent = fs.readFileSync(CLIENT_FILE, 'utf8');
  
  // Read the current hooks/index.ts file
  const hooksIndexContent = fs.readFileSync(HOOKS_INDEX_FILE, 'utf8');
  
  // Track new hooks to add to index.ts
  const newHooks = [];
  
  // Track new client imports to add to client.ts
  const newImports = [];
  
  // Track new client methods to add to client.ts
  const newClientMethods = [];
  
  // Track new standalone functions to add to client.ts
  const newFunctions = [];
  
  // Identify GET endpoints with response models
  const paths = openApiSchema.paths;
  for (const [path, methods] of Object.entries(paths)) {
    if (methods.get) {
      const getMethod = methods.get;
      const operationId = getMethod.operationId;
      const responses = getMethod.responses;
      
      // Check if the endpoint has a 200 response with a schema
      if (responses['200'] && 
          responses['200'].content && 
          responses['200'].content['application/json'] && 
          responses['200'].content['application/json'].schema) {
        
        const schema = responses['200'].content['application/json'].schema;
        let responseType;
        let isArray = false;
        
        // Determine the response type
        if (schema.$ref) {
          // Direct reference to a schema
          responseType = schema.$ref.split('/').pop();
        } else if (schema.type === 'array' && schema.items && schema.items.$ref) {
          // Array of references
          responseType = schema.items.$ref.split('/').pop();
          isArray = true;
        } else if (schema.items && schema.items.$ref) {
          // Items with reference
          responseType = schema.items.$ref.split('/').pop();
          isArray = true;
        }
        
        if (responseType) {
          // Skip endpoints we already have hooks for
          if (operationId === 'health_check_api_health_get' || 
              operationId === 'get_listings_api_listings_get') {
            continue;
          }
          
          // Generate hook name based on the path
          const pathParts = path.split('/').filter(p => p && p !== 'api');
          const hookName = `use${pathParts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('')}`;
          
          // Generate client method name based on the operationId
          const methodName = operationId.replace(/_/g, '');
          
          // Determine the API class name based on the path
          const apiTag = getMethod.tags ? getMethod.tags[0] : pathParts[0];
          const apiClassName = `${apiTag.charAt(0).toUpperCase() + apiTag.slice(1)}Api`;
          
          // Add import if not already in client.ts
          if (!clientContent.includes(`import { ${apiClassName}`)) {
            newImports.push(apiClassName);
          }
          
          // Check if the endpoint has parameters
          const parameters = getMethod.parameters || [];
          const hasParams = parameters.length > 0;
          
          // Generate client method
          let clientMethod = '';
          if (hasParams) {
            // Extract parameter names and types
            const paramNames = parameters.map(p => p.name.replace(/-/g, '_'));
            
            // Create filters interface
            const filtersInterface = `export interface ${hookName}Filters {
${parameters.map(p => `  ${p.name.replace(/-/g, '_')}?: ${p.schema.type === 'integer' ? 'number' : p.schema.type};`).join('\n')}
}`;
            
            // Create client method
            clientMethod = `
  // ${getMethod.summary || `Get ${pathParts.join(' ')}`}
  async ${methodName}(filters?: ${hookName}Filters) {
    return this.${apiTag.toLowerCase()}Api.${operationId}({
${parameters.map(p => `      ${p.name.replace(/-/g, '_')}: filters?.${p.name.replace(/-/g, '_')},`).join('\n')}
    });
  }`;
            
            // Create standalone function
            const standaloneFunction = `
// ${getMethod.summary || `Get ${pathParts.join(' ')}`}
export const ${methodName} = async (
  filters?: ${hookName}Filters,
  baseUrl: string = ''
) => {
  const client = new ApiClient(baseUrl);
  return client.${methodName}(filters);
};`;
            
            newFunctions.push(filtersInterface);
            newFunctions.push(standaloneFunction);
            
            // Generate hook
            const hookContent = `import { useQuery } from '@tanstack/react-query';
import { ${methodName}, ${hookName}Filters } from '../client.js';
import type { ${responseType} } from '@repo/client-generated';

export interface ${hookName}Result {
  data: ${isArray ? `${responseType}[]` : responseType} | undefined;
  isLoading: boolean;
  isError: boolean;
  refetch: () => void;
}

/**
 * Hook to fetch ${getMethod.summary || pathParts.join(' ')}
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
    queryKey: ['${pathParts.join('-')}', filters],
    queryFn: () => ${methodName}(filters),
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
`;
            
            // Write hook file
            const hookFilePath = path.join(HOOKS_DIR, `${hookName}.ts`);
            fs.writeFileSync(hookFilePath, hookContent);
            console.log(`✅ Generated hook: ${hookName}`);
            
            // Add to new hooks list
            newHooks.push(hookName);
            
          } else {
            // Simple endpoint without parameters
            clientMethod = `
  // ${getMethod.summary || `Get ${pathParts.join(' ')}`}
  async ${methodName}() {
    return this.${apiTag.toLowerCase()}Api.${operationId}();
  }`;
            
            // Create standalone function
            const standaloneFunction = `
// ${getMethod.summary || `Get ${pathParts.join(' ')}`}
export const ${methodName} = async (baseUrl: string = '') => {
  const client = new ApiClient(baseUrl);
  return client.${methodName}();
};`;
            
            newFunctions.push(standaloneFunction);
            
            // Generate hook
            const hookContent = `import { useQuery } from '@tanstack/react-query';
import { ${methodName} } from '../client.js';
import type { ${responseType} } from '@repo/client-generated';

/**
 * Hook to fetch ${getMethod.summary || pathParts.join(' ')}
 * @returns Object containing the data, loading state, error state, and refetch function
 */
export function ${hookName}() {
  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery<${isArray ? `${responseType}[]` : responseType}, Error>({
    queryKey: ['${pathParts.join('-')}'],
    queryFn: () => ${methodName}(),
  });

  return {
    data,
    isLoading,
    isError,
    refetch: () => refetch(),
  };
}
`;
            
            // Write hook file
            const hookFilePath = path.join(HOOKS_DIR, `${hookName}.ts`);
            fs.writeFileSync(hookFilePath, hookContent);
            console.log(`✅ Generated hook: ${hookName}`);
            
            // Add to new hooks list
            newHooks.push(hookName);
          }
          
          // Add client method to list
          newClientMethods.push(clientMethod);
        }
      }
    }
  }
  
  // Update client.ts with new imports
  if (newImports.length > 0) {
    const importRegex = /import \{ (.*?) \} from '@repo\/client-generated';/;
    const importMatch = clientContent.match(importRegex);
    if (importMatch) {
      const currentImports = importMatch[1];
      const updatedImports = [...new Set([...currentImports.split(', '), ...newImports])].join(', ');
      const updatedClientContent = clientContent.replace(
        importRegex,
        `import { ${updatedImports} } from '@repo/client-generated';`
      );
      
      // Update ApiClient class with new API instances
      const apiInstancesRegex = /private healthApi: HealthApi;([^}]*)/;
      const apiInstancesMatch = updatedClientContent.match(apiInstancesRegex);
      if (apiInstancesMatch) {
        const currentApiInstances = apiInstancesMatch[1];
        const newApiInstances = newImports
          .filter(api => !currentApiInstances.includes(api.replace('Api', '').toLowerCase() + 'Api'))
          .map(api => `\n  private ${api.replace('Api', '').toLowerCase()}Api: ${api};`).join('');
        
        const updatedApiInstances = currentApiInstances + newApiInstances;
        const updatedWithApiInstances = updatedClientContent.replace(
          apiInstancesRegex,
          `private healthApi: HealthApi;${updatedApiInstances}`
        );
        
        // Update constructor with new API initializations
        const constructorRegex = /this\.healthApi = new HealthApi\(config\);([^}]*)/;
        const constructorMatch = updatedWithApiInstances.match(constructorRegex);
        if (constructorMatch) {
          const currentInitializations = constructorMatch[1];
          const newInitializations = newImports
            .filter(api => !currentInitializations.includes(`this.${api.replace('Api', '').toLowerCase()}Api = new ${api}`))
            .map(api => `\n    this.${api.replace('Api', '').toLowerCase()}Api = new ${api}(config);`).join('');
          
          const updatedInitializations = currentInitializations + newInitializations;
          const updatedWithInitializations = updatedWithApiInstances.replace(
            constructorRegex,
            `this.healthApi = new HealthApi(config);${updatedInitializations}`
          );
          
          // Add new client methods
          const clientMethodsRegex = /\/\/ Add your custom client methods here([^}]*)/;
          const clientMethodsMatch = updatedWithInitializations.match(clientMethodsRegex);
          if (clientMethodsMatch) {
            const updatedWithMethods = updatedWithInitializations.replace(
              clientMethodsRegex,
              `// Add your custom client methods here${clientMethodsMatch[1]}${newClientMethods.join('')}`
            );
            
            // Add new standalone functions
            const functionsRegex = /\/\/ Re-export the GPUListingDTO type as GpuReportRow for consistency with the task/;
            const updatedWithFunctions = updatedWithMethods.replace(
              functionsRegex,
              `${newFunctions.join('')}\n\n// Re-export the GPUListingDTO type as GpuReportRow for consistency with the task`
            );
            
            fs.writeFileSync(CLIENT_FILE, updatedWithFunctions);
            console.log('✅ Updated client.ts with new methods');
          }
        }
      }
    }
  }
  
  // Update hooks/index.ts with new hooks
  if (newHooks.length > 0) {
    const updatedHooksIndex = hooksIndexContent.trim() + '\n' + 
      newHooks.map(hook => `export * from './${hook}.js';`).join('\n');
    fs.writeFileSync(HOOKS_INDEX_FILE, updatedHooksIndex);
    console.log('✅ Updated hooks/index.ts with new hooks');
  }
  
  console.log('✅ Hook generation completed successfully!');
  
} catch (error) {
  console.error('❌ Failed to generate hooks:', error);
  process.exit(1);
}