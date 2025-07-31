
## TASK.web.06.discovery.02.list-consumable-endpoints

### 📌 Goal

Generate a human-readable summary of all currently consumable backend API endpoints for the frontend. This task helps identify what data is available and how it can be visualized or integrated in the web UI.

---

### 🧠 Background

The backend exposes a growing number of REST endpoints defined via FastAPI. Each route is defined with OpenAPI metadata, including response models and summaries.

Junie-Web should inspect the OpenAPI spec and list all routes that:
- Use `GET` method
- Provide a valid `response_model`
- Are reachable at `/api/`
- Have stable schema (i.e., DTO-backed responses)

This list will form the foundation for planning new frontend components.

---

### 🧩 What to Output

- A Markdown table or bullet list showing:
  - `Path`: `/api/health`, `/api/reports`, etc.
  - `Response DTO`: The expected model returned
  - `Status`: ✅ Available | ⚠️ Missing Model | 🚧 Experimental
  - `Suggested Hook`: Name of hook that could wrap it (e.g. `useHealthStatus()`)

Save this summary under:

```
web/docs/api/available-endpoints.md
```

Junie should ensure this file is clear, well-formatted, and does not duplicate content from other sources.

---

### 📦 Implementation Steps

1. Fetch the current OpenAPI schema from:
   ```
   http://localhost:8000/openapi.json
   ```
   (Ensure `docker-stack.sh up` is running.)

2. Parse the schema and extract all `GET` routes.

3. For each route:
   - Confirm it returns a structured response (not `Any`, `str`, or `Dict`).
   - Extract the `summary`, `tags`, and `response_model` (if present).
   - Generate a proposed name for a React hook that would wrap it.

4. Write a summary file to `web/docs/api/available-endpoints.md`.

---

### ✅ Acceptance Criteria

- File `web/docs/api/available-endpoints.md` exists and is properly formatted.
- At least 3 confirmed consumable endpoints are listed.
- Each entry includes a hook suggestion and response type.
- File is git tracked and pushed in same commit.

---

### 🔗 Related Tasks

- [`TASK.web.05.discovery.01.generate-client-hooks-from-openapi`](./TASK.web.05.discovery.01.generate-client-hooks-from-openapi.md)
- [`TASK.client.01.wrap-health-endpoint`](./TASK.client.01.wrap-health-endpoint.md)
- [`TASK.client.02.wrap-reports-endpoint`](./TASK.client.02.wrap-reports-endpoint.md)

---

### 🛰 EPIC Reference

This task is part of the following epic:

[`EPIC.web.frontend-ui-ux`](../epics/open/EPIC.web.frontend-ui-ux.md)

## ✅ Task Completed

**Changes made**
- Created a comprehensive Markdown document at `web/docs/api/available-endpoints.md` that lists all consumable backend API endpoints
- Identified 5 GET endpoints with valid response models:
  - `/api/health` - Returns a HealthStatus object
  - `/api/listings` - Returns an array of GPUListingDTO objects
  - `/api/listings/legacy` - Returns an array of GPUListingDTO objects
  - `/api/models` - Returns an array of GPUModelDTO objects
  - `/api/report` - Returns a ReportDTO object
- For each endpoint, documented:
  - Path
  - Response DTO with TypeScript interface
  - Status (all are ✅ Available)
  - Suggested hook name
  - Description
  - Parameters (if any)
- Added an implementation status section and a usage example

**Outcomes**
- The documentation provides a clear overview of all available endpoints that can be consumed by the frontend
- The suggested hook names align with the hooks that have already been implemented
- The documentation includes detailed information about the response DTOs, making it easier to understand the data structure
- The file is properly formatted and meets all acceptance criteria