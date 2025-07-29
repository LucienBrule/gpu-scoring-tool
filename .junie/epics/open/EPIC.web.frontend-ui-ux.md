## EPIC: Frontend UI/UX for GPU Scoring Tool

### Overview
This Epic aims to implement a full-featured, operator-facing web frontend for the GPU Scoring Tool system. The frontend enables visualization, filtering, historical tracking, and actionable intelligence based on scored GPU market data.

The application is built using Next.js, TailwindCSS, and TypeScript, and communicates with the backend via a code-generated TypeScript client (OpenAPI-based).

### Goals
- Visualize scored GPU listings and insight metrics
- Provide sorting, filtering, and heuristic overlays (e.g. quantization support, scoring tier, VRAM)
- Enable historical views via import metadata (`import_id`, timestamps)
- Ensure full integration with backend service (`glyphd`)
- Run Playwright-based integration tests for all interactive features

### Scope
This Epic includes:
- UI/UX implementation of the reports page
- GPU listing visualizations with dynamic filters and tags
- Historical import timeline or navigation
- Client-side logic for interfacing with `glyphd` API via generated SDK
- Snapshot testing and test automation with Playwright
- OpenAPI codegen pipeline integration

### Tasks
- `TASK.web.reports-view`
- `TASK.web.interactive-filtering`
- `TASK.web.import-history-tracker`
- `TASK.web.integration-test-suite`
- `TASK.web.openapi-codegen-cli-export`
- `TASK.web.gpu-tag-badges` (optional enhancement)

### Constraints
- All components must use the generated TypeScript client (no direct fetch)
- Components must support dark mode and mobile responsiveness
- No mocking; tests must execute against live Docker Compose backend

### Success Criteria
- End-to-end tests validate functional integration
- GPU reports load from the API and reflect current scored dataset
- Operators can filter, inspect, and compare listings effectively
- DX is stable and repeatable via codegen and workspace conventions
