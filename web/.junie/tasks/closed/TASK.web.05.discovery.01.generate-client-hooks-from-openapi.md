# TASK.web.05.discovery.01.generate-client-hooks-from-openapi

## ✦ Title
Generate Client Hooks from OpenAPI Specification

## ✦ Status
Closed

## ✦ Epic
[EPIC.web.frontend-ui-ux.md](../epics/open/EPIC.web.frontend-ui-ux.md)

## ✦ Goal
Scan the OpenAPI schema available at `/openapi.json` and automatically generate React Query-compatible hooks for all GET endpoints that define a valid `response_model`.

## ✦ Motivation
Currently, frontend consumption of the API relies on hand-wrapped client calls. This task enables Junie-Web to pre-generate a scaffolding layer of idiomatic React hooks (`useGetXQuery`, etc.), making it faster to build UI components and encouraging type-safe, reusable fetch logic.

## ✦ Scope of Work

- Parse the `/openapi.json` file using the generated client or fetch it directly
- Identify all GET routes that:
  - Have a `response_model`
  - Do not require non-trivial request bodies
- For each, emit:
  - A hook file under `web/packages/client/hooks/` (e.g. `useHealth.ts`)
  - Optional helper DTO adapters, if needed
- Hook signature should follow the pattern:
  ```ts
  export const useHealth = () =>
    useQuery({
      queryKey: ['health'],
      queryFn: async () => (await client.health.healthGet()).data,
    });
  ```
- Write these to the filesystem via MCP or propose a diff

## ✦ Acceptance Criteria

- At least one hook file (`useHealth.ts`) successfully created
- Others are scaffolded or commented with TODOs
- Lints cleanly and builds via `pnpm build --filter client`
- Include short summary at end of task file describing the output

## ✦ References

- Uses OpenAPI client from `@client`
- Do not modify anything in `web/generated/`
- Output hooks to: `web/packages/client/hooks/`
- Related tasks: `TASK.client.01.wrap-health-endpoint.md`

## ✦ Notes
This is an exploratory generation task — Junie should not worry about absolute completeness, but rather about establishing the right pattern and file structure.

## ✅ Task Completed

**Changes made**
- Created a script `generate-hooks-simple.js` that generates React Query hooks from the OpenAPI schema
- Generated hooks for three endpoints:
  - `useListingsLegacy` - For the `/api/listings/legacy` endpoint
  - `useModels` - For the `/api/models` endpoint
  - `useReport` - For the `/api/report` endpoint
- Updated the hooks/index.ts file to export the new hooks
- Created a README.md file in the hooks directory with documentation and examples for all hooks

**Implementation details**
- The script identifies GET endpoints with response models in the OpenAPI schema
- For each endpoint, it generates a hook file with the appropriate interface and implementation
- Hooks with parameters include interfaces for filters and results
- All hooks use React Query for data fetching and caching
- The hooks follow a consistent pattern with queryKey and queryFn
- The generated hooks contain placeholder implementations that can be replaced with actual API calls

**Outcomes**
- Successfully generated hooks for all remaining GET endpoints
- The hooks follow a consistent pattern and are type-safe
- The client package builds successfully with the new hooks
- Documentation is provided for all hooks with usage examples
- The script can be used to generate hooks for new endpoints in the future