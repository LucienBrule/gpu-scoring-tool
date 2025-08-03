# Epic: Glyphd Integration & Control Panel v1 Polish

## Scope & Intent
This epic encompasses the end-to-end integration of the newly generated OpenAPI client into our manual API client, the creation of React hooks for all backend endpoints, wiring those hooks into the control panel UI, and a comprehensive design polish with a dark-mode-first, Catppuccin Mocha–inspired theme. It aims to deliver a polished v1 experience of the GPU Scoring Tool’s control panel, ensuring full API coverage, developer ergonomics, and visual coherence.

## Tasks

### Phase 1 – Codegen & Manual Client Integration
- **TASK.web.v1.00.codegen-import-openapi.md**  
  Ingest the latest OpenAPI Generator output into `generated/client-generated/src`, ensuring files are up-to-date.

- **TASK.web.v1.01.api-client-reexports.md**  
  Extend the manual `ApiClient` to re-export all newly generated API classes under a unified interface.

- **TASK.web.v1.02.domain-type-aliases.md**  
  Create domain-aligned TypeScript type aliases (e.g., `GpuListing`, `GpuModelStats`) to simplify DTO usage.

- **TASK.web.v1.03.tree-shaking-verification.md**  
  Verify that unused API methods are tree-shaken in production builds; adjust exports if necessary.

- **TASK.web.v1.04.type-coverage-validation.md**  
  Write a script or test to confirm that all public API methods have correct TypeScript types and documentation.

### Phase 2 – Hook Surface Definition
- **TASK.web.v1.10.define-useHealth-hook.md**  
  Implement `useHealth` hook for the `/api/health` endpoint.

- **TASK.web.v1.11.define-useGpuModels-hook.md**  
  Implement `useGpuModels` hook for the `/api/models` endpoint.

- **TASK.web.v1.12.define-useGpuListings-hook.md**  
  Implement `useGpuListings` hook for the `/api/listings` endpoint, supporting filters, pagination, and fuzzy search.

- **TASK.web.v1.13.define-useGpuReports-hook.md**  
  Implement `useGpuReports` hook for the `/api/report` endpoint.

- **TASK.web.v1.14.define-useForecastDeltas-hook.md**  
  Implement `useForecastDeltas` hook for the `/api/forecast/deltas` endpoint with query parameters.

- **TASK.web.v1.15.define-useGpuClassification-hook.md**  
  Implement `useGpuClassification` hook for the `/api/ml/is-gpu` endpoint.

- **TASK.web.v1.16.define-useSchemaInfo-hook.md**  
  Implement `useSchemaInfo` hook for `/api/schema/versions` and `/api/schema/versions/{version}`.

- **TASK.web.v1.17.define-useImportCsv-hook.md**  
  Implement `useImportCsv` hook for the `/api/import/csv` endpoint.

- **TASK.web.v1.18.define-useImportFromPipeline-hook.md**  
  Implement `useImportFromPipeline` hook for the `/api/imports/from-pipeline` endpoint.

- **TASK.web.v1.19.define-usePersistListings-hook.md**  
  Implement `usePersistListings` hook for the `/api/persist/listings` endpoint.

- **TASK.web.v1.1A.define-useValidateArtifact-hook.md**  
  Implement `useValidateArtifact` hook for the `/api/ingest/upload-artifact` endpoint.

### Phase 3 – Hook Usage & Page Wiring
- **TASK.web.v1.20.page-wire-gpu-reports.md**  
  Refactor the GPU Reports page to use `useGpuReports` and render markdown plus structured stats.

- **TASK.web.v1.21.page-wire-gpu-models.md**  
  Implement or refine the GPU Models page using `useGpuModels`.

- **TASK.web.v1.22.page-wire-forecast.md**  
  Create a Forecast tab to display deltas via `useForecastDeltas` with optional model and region filters.

- **TASK.web.v1.23.page-wire-ml-playground.md**  
  Add an ML Classifier Playground page with text input and live results from `useGpuClassification`.

- **TASK.web.v1.24.page-wire-import-tools.md**  
  Build an Import Tools page combining `useImportCsv`, `useImportFromPipeline`, and `useValidateArtifact` with upload forms.

### Phase 4 – Design Polish & Theming
- **TASK.web.v1.30.tailwind-theme-catppuccin.md**  
  Extend Tailwind config with a Catppuccin Mocha–inspired color palette.

- **TASK.web.v1.31.dark-mode-default.md**  
  Configure `darkMode: 'class'`, default to dark mode, and update `<html>` classes.

- **TASK.web.v1.32.ui-spacing-and-typography.md**  
  Align spacing, typography, and component density to match the GPU Reports baseline.

- **TASK.web.v1.33.component-style-normalization.md**  
  Standardize button, input, table, and card styles across all pages.

### Phase 5 – Developer DX & Utilities
- **TASK.web.v1.40.dev-harness-page.md**  
  Create a Developer Harness page to exercise all hooks and endpoints in isolation.

- **TASK.web.v1.41.loading-and-empty-states.md**  
  Add consistent loading spinners and empty-state placeholders for each data view.

- **TASK.web.v1.42.storybook-setup.md**  
  Initialize Storybook or similar component explorer for UI and hook snapshots.

- **TASK.web.v1.43.type-test-scripts.md**  
  Add automated tests or scripts to verify hook return types and error handling.

- **TASK.web.v1.44.polling-refresh-hook.md**  
  Optional: Build `usePollingForecast` hook to auto-refresh deltas on a set interval.

- **TASK.web.v1.45.sparkline-trendline-component.md**  
  Optional: Develop a lightweight Sparkline component for inline trend visualization in listings.
