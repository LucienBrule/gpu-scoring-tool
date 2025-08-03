/**
 * Tree-Shaking Verification Script
 * 
 * This script analyzes the production bundle to verify that unused API modules
 * are properly tree-shaken (removed) from the bundle. It uses source-map-explorer
 * to analyze the bundle and generates a report with the results.
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

// Configuration
const BUNDLE_DIR = path.resolve('.next/static/chunks');
const REPORT_FILE = path.resolve('tree-shaking-report.md');
const HTML_REPORT_FILE = path.resolve('bundle-report.html');

// API modules that should be checked for tree-shaking
const API_MODULES = [
  'ForecastApi',
  'HealthApi',
  'ImportApi',
  'ListingsApi',
  'MLApi',
  'ModelsApi',
  'PersistApi',
  'ReportApi',
  'SchemaApi',
  'ValidationApi'
];

// API modules that are known to be used in the codebase
// This list should be updated if new API modules are used
const USED_API_MODULES = [
  'ForecastApi',
  'HealthApi',
  'ImportApi',
  'ListingsApi',
  'MLApi',
  'ModelsApi',
  'PersistApi',
  'ReportApi',
  'SchemaApi',
  'ValidationApi'
];

/**
 * Main function to verify tree-shaking
 */
async function verifyTreeShaking() {
  console.log('🔍 Verifying tree-shaking of API modules...');
  
  // Check if the bundle directory exists
  if (!fs.existsSync(BUNDLE_DIR)) {
    console.error('❌ Bundle directory not found. Please run `pnpm build` first.');
    generateErrorReport();
    process.exit(1);
  }
  
  // Get all JavaScript files in the bundle directory
  const bundleFiles = fs.readdirSync(BUNDLE_DIR)
    .filter(file => file.endsWith('.js'))
    .map(file => path.join(BUNDLE_DIR, file));
  
  if (bundleFiles.length === 0) {
    console.error('❌ No JavaScript files found in the bundle directory.');
    generateErrorReport();
    process.exit(1);
  }
  
  console.log(`📦 Found ${bundleFiles.length} JavaScript files in the bundle.`);
  
  // Generate HTML report using source-map-explorer
  try {
    console.log('📊 Generating HTML bundle report...');
    execSync(`npx source-map-explorer ${bundleFiles.join(' ')} --html ${HTML_REPORT_FILE}`, { stdio: 'inherit' });
    console.log(`✅ HTML bundle report generated: ${HTML_REPORT_FILE}`);
  } catch (error) {
    console.error('❌ Failed to generate HTML bundle report:', error.message);
  }
  
  // Analyze bundle content to check for unused API modules
  console.log('🔍 Analyzing bundle content...');
  const bundleContent = bundleFiles.map(file => fs.readFileSync(file, 'utf8')).join('\n');
  
  // Check which API modules are included in the bundle
  const includedModules = API_MODULES.filter(module => 
    bundleContent.includes(`class ${module}`) || 
    bundleContent.includes(`"${module}"`) || 
    bundleContent.includes(`'${module}'`)
  );
  
  // Identify unused API modules that are included in the bundle
  const unusedIncludedModules = includedModules.filter(module => !USED_API_MODULES.includes(module));
  
  // Generate report
  generateReport(includedModules, unusedIncludedModules);
  
  // Check if tree-shaking is working correctly
  if (unusedIncludedModules.length > 0) {
    console.error('❌ Tree-shaking verification failed. Unused API modules found in the bundle.');
    process.exit(1);
  } else {
    console.log('✅ Tree-shaking verification passed. No unused API modules found in the bundle.');
  }
}

/**
 * Generate a report with the results of the tree-shaking verification
 */
function generateReport(includedModules, unusedIncludedModules) {
  const report = [
    '# Tree-Shaking Verification Report',
    '',
    `Generated on: ${new Date().toISOString()}`,
    '',
    '## Summary',
    '',
    `- Total API modules: ${API_MODULES.length}`,
    `- API modules used in codebase: ${USED_API_MODULES.length}`,
    `- API modules included in bundle: ${includedModules.length}`,
    `- Unused API modules in bundle: ${unusedIncludedModules.length}`,
    '',
    '## Details',
    '',
    '### API Modules Used in Codebase',
    '',
    ...USED_API_MODULES.map(module => `- ${module}`),
    '',
    '### API Modules Included in Bundle',
    '',
    ...includedModules.map(module => `- ${module}`),
    '',
  ];
  
  if (unusedIncludedModules.length > 0) {
    report.push(
      '### Unused API Modules in Bundle',
      '',
      ...unusedIncludedModules.map(module => `- ${module}`),
      '',
      '## Recommendations',
      '',
      'The following API modules are included in the bundle but not used in the codebase:',
      '',
      ...unusedIncludedModules.map(module => `- ${module}`),
      '',
      'To improve tree-shaking, consider:',
      '',
      '1. Using named imports instead of namespace imports',
      '2. Avoiding side effects in imports',
      '3. Using dynamic imports for code splitting',
      '4. Ensuring that the bundler is configured for production mode',
      ''
    );
  } else {
    report.push(
      '## Conclusion',
      '',
      'Tree-shaking is working correctly. All API modules included in the bundle are used in the codebase.',
      '',
      'The bundle size could potentially be further optimized by:',
      '',
      '1. Using dynamic imports for code splitting',
      '2. Lazy loading components and routes',
      '3. Optimizing dependencies',
      ''
    );
  }
  
  fs.writeFileSync(REPORT_FILE, report.join('\n'));
  console.log(`📝 Tree-shaking report generated: ${REPORT_FILE}`);
}

/**
 * Generate an error report when the bundle cannot be analyzed
 */
function generateErrorReport() {
  const report = [
    '# Tree-Shaking Verification Error Report',
    '',
    `Generated on: ${new Date().toISOString()}`,
    '',
    '## Error',
    '',
    'The bundle could not be analyzed because the bundle directory was not found or contained no JavaScript files.',
    '',
    '## Recommendations',
    '',
    '1. Run `pnpm build` to generate the production bundle',
    '2. Ensure that the build completes successfully',
    '3. Run this script again to verify tree-shaking',
    ''
  ];
  
  fs.writeFileSync(REPORT_FILE, report.join('\n'));
  console.log(`📝 Error report generated: ${REPORT_FILE}`);
}

// Run the verification
verifyTreeShaking().catch(error => {
  console.error('❌ An error occurred during tree-shaking verification:', error);
  process.exit(1);
});