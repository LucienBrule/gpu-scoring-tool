#!/usr/bin/env node

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Base directory of this script (i.e. packages/client/scripts/)
const SCRIPT_DIR = __dirname;

// Project root (go up from scripts/ → client/ → packages/ → web/)
const PROJECT_ROOT = path.resolve(SCRIPT_DIR, '../../../');

// Path to the OpenAPI schema output
const OPENAPI_FILE = path.resolve(SCRIPT_DIR, '../openapi.json');

console.log('🔄 Running glyphd export-openapi to generate OpenAPI schema...');

try {
  // Run glyphd to emit OpenAPI schema to the resolved location
  execSync(`cd ${PROJECT_ROOT} && uv run -m glyphd export-openapi ${OPENAPI_FILE}`, {
    stdio: 'inherit'
  });

  if (!existsSync(OPENAPI_FILE)) {
    console.error('❌ OpenAPI schema file was not created at expected location');
    process.exit(1);
  }

  console.log('✅ OpenAPI schema generated successfully!');

  console.log('🔄 Generating TypeScript client...');
  execSync('node scripts/generate-client.js', {
    stdio: 'inherit'
  });

  console.log('✅ Client generation completed successfully!');

} catch (error) {
  console.error('❌ Failed to generate client:', error.message);
  process.exit(1);
}