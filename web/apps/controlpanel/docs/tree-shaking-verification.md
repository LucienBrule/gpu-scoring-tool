# Tree-Shaking Verification Guide

This document explains how to verify that unused API modules are properly tree-shaken (removed) from the production bundle of the controlpanel application.

## What is Tree-Shaking?

Tree-shaking is a term commonly used in the JavaScript context for dead-code elimination. It relies on the static structure of ES2015 module syntax (`import` and `export`). When bundling your application for production, the bundler analyzes your code and removes any code that isn't actually used, reducing the final bundle size.

## Why Verify Tree-Shaking?

Verifying that tree-shaking is working correctly is important for several reasons:

1. **Reduced Bundle Size**: Smaller bundles lead to faster load times and better user experience.
2. **Improved Performance**: Less code means less parsing and execution time.
3. **Better Caching**: Smaller bundles are more cache-friendly.
4. **Reduced Network Usage**: Smaller bundles use less bandwidth.

## How to Verify Tree-Shaking

We've added two scripts to the controlpanel application to help verify tree-shaking:

1. `analyze-bundle`: Generates an HTML report of the bundle contents using source-map-explorer.
2. `verify-tree-shaking`: Analyzes the bundle to check if unused API modules are included.

### Prerequisites

Before running these scripts, you need to:

1. Build the application for production:

```bash
pnpm --filter controlpanel build
```

> Note: If the build fails due to ESLint errors, you can skip linting with:
> ```bash
> cd apps/controlpanel && npx next build --no-lint
> ```

### Analyzing the Bundle

To generate an HTML report of the bundle contents:

```bash
pnpm --filter controlpanel analyze-bundle
```

This will create a file called `bundle-report.html` in the controlpanel directory. Open this file in a browser to see a visual representation of the bundle contents.

### Verifying Tree-Shaking

To verify that unused API modules are properly tree-shaken:

```bash
pnpm --filter controlpanel verify-tree-shaking
```

This will analyze the bundle and generate a report called `tree-shaking-report.md` in the controlpanel directory. The report will include:

- A summary of the API modules used in the codebase and included in the bundle
- Details about which API modules are included in the bundle
- Recommendations for improving tree-shaking if unused modules are found

## Interpreting the Results

### HTML Bundle Report

The HTML bundle report shows a visual representation of the bundle contents. Each rectangle represents a module, and the size of the rectangle is proportional to the size of the module. This can help identify large modules that might be candidates for optimization.

### Tree-Shaking Report

The tree-shaking report provides a more focused analysis of API modules. It checks if any unused API modules are included in the bundle. If all API modules included in the bundle are used in the codebase, tree-shaking is working correctly.

## Improving Tree-Shaking

If the tree-shaking report identifies unused API modules in the bundle, consider the following strategies to improve tree-shaking:

1. **Use Named Imports**: Instead of importing entire modules, import only the specific functions or classes you need.
   ```javascript
   // Instead of this:
   import * as api from './api';
   
   // Do this:
   import { specificFunction } from './api';
   ```

2. **Avoid Side Effects**: Ensure that your modules don't have side effects that prevent tree-shaking.

3. **Use Dynamic Imports**: Consider using dynamic imports for code splitting.
   ```javascript
   // Instead of this:
   import { heavyModule } from './heavy-module';
   
   // Do this:
   const heavyModule = () => import('./heavy-module');
   ```

4. **Configure Bundler for Production**: Ensure that your bundler is configured for production mode, which typically enables more aggressive optimizations.

## CI Integration

The `verify-tree-shaking` script is designed to be run in CI environments. It will exit with a non-zero status code if unused API modules are found in the bundle, causing the CI build to fail.

To integrate with CI, add the following step to your CI workflow:

```yaml
- name: Verify Tree-Shaking
  run: pnpm --filter controlpanel verify-tree-shaking
```

## Conclusion

By regularly verifying tree-shaking, we can ensure that our application remains optimized and performant. The scripts provided make it easy to check if tree-shaking is working correctly and identify opportunities for improvement.