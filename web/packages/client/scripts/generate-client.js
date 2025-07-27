#!/usr/bin/env node

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define where to output the client
const GENERATED_OUTPUT_PATH = path.resolve(__dirname, '../../../generated/client-generated');

const OPENAPI_FILE = process.argv[2] || 'openapi.json';
const OPENAPI_YAML = process.argv[2] || 'openapi.yaml';

// Check if OpenAPI spec exists
const hasJson = existsSync(OPENAPI_FILE);
const hasYaml = existsSync(OPENAPI_YAML);

if (!hasJson && !hasYaml) {
    console.error('❌ No OpenAPI spec found. Please provide openapi.json or openapi.yaml');
    process.exit(1);
}

const specFile = hasJson ? OPENAPI_FILE : OPENAPI_YAML;

console.log('🔄 Generating TypeScript client from', specFile);

try {
    // Clean previous generated code
    execSync(`rm -rf ${GENERATED_OUTPUT_PATH}`, { stdio: 'inherit' });

    // Generate the client
    execSync(`npx openapi-generator-cli generate -i ${specFile} -g typescript-fetch -o ${GENERATED_OUTPUT_PATH} --additional-properties=typescriptThreePlus=true,supportsES6=true,npmName=@repo/client-generated`, {
        stdio: 'inherit'
    });

    console.log('✅ Client generated successfully!');
} catch (error) {
    console.error('❌ Failed to generate client:', error.message);
    process.exit(1);
}