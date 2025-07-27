# Junie Guidelines (v0.1.1)

Welcome to Junie, the assistant task and tooling layer for `gpu-scoring-tool` and `glyphsieve`. This document outlines best practices, project norms, execution patterns, and guidance for maintaining and contributing to this evolving research system.

---

## 🧠 Project Overview

Junie supports the broader purpose of this repository: analyzing and interpreting real-world GPU market dynamics. She helps scaffold, extend, and maintain structured data pipelines and normalization tools across a multi-layered system.

---

## 📁 Repo Structure (High-Level)

- `glyphsieve/` — Python 3.12 project managed via `uv`; home of core normalization and scoring code.
- `sieveviz/` — Visualization layer (JS/HTML/CSS). Junie does not modify this without explicit instruction.
- `scrape/` — Raw CSV data scraped from sellers (organized by SKU).
- `recon/` — OSINT-style manual collection folders; Junie reads, but does not modify.
- `.junie/` — Junie's own memory and operational space.

---

## ⚙️ Tooling & Runtime

- This project uses [`uv`](https://github.com/astral-sh/uv) for Python environment and dependency management.
    - Add packages from within the relevant subproject:
      ```bash
      uv add <package>
      ```
    - Sync all environments:
      ```bash
      uv sync --all-packages
      ```
    - If the environment becomes stale (e.g. due to renames), reset with:
      ```bash
      rm uv.lock && uv sync --all-packages
      ```

### Scripting and Development Patterns

- Python 3.12 is the standard runtime for all `glyphsieve/` code
- Typer-based CLI tooling is planned for command-line interfaces
- When creating new scripts, follow these conventions:
  - Include docstrings with purpose and usage examples
  - Add type hints to function signatures
  - Implement proper error handling and logging
  - Create unit tests for core functionality

### Safe Execution Environment (`safe-run.sh`)

Junie must use `.junie/safe-run.sh` when running any long-lived or blocking process that could interfere with task concurrency (e.g., launching `pnpm dev`, running `uvicorn`, etc.).

This script safely runs foreground or background processes, manages logs, and records status and PID information.

#### Process Management with `safe-run.sh`

Junie can manage long-running processes with the following operations:

- **Starting processes**: Use the `-b` flag to run in background
  ```bash
  ./.junie/scripts/safe-run.sh -n process-name -b -- command args
  ```

- **Terminating processes**: Use the `-k` flag to kill a named process
  ```bash
  ./.junie/scripts/safe-run.sh -k process-name
  ```

- **Checking process status**: Inspect the status files in `.junie/status/`
  ```bash
  cat .junie/status/process-name.status
  ```

Example usage:

```bash
./.junie/safe-run.sh -n devserver -b pnpm dev --filter controlpanel
```

This runs the control panel frontend in the background and saves logs to `.junie/logs/`.

Junie must prefer `safe-run.sh` over raw `nohup` or foreground dev servers, especially when multiple services are running concurrently or during test-driven development.

#### Process Cleanup Guidelines

Always terminate background processes when they are no longer needed using the kill functionality. Include process cleanup in your task completion summary.

⚠️ **Important:** Junie must never use `tail -f` inside her tasks — it blocks her synchronous task execution and halts all downstream processing.

Instead, use log inspection tools that exit cleanly:

```bash
tail -n 20 .junie/logs/glyphd-server.log      # Show last 20 lines
grep 'ERROR' .junie/logs/glyphd-server.log    # Search for errors
```

Junie cannot observe logs in real time, but she can always inspect snapshots as part of post-task analysis.

### Language Interoperability

- Kotlin/TypeScript interop for DTO definitions and structured pipelines is planned
- When working with cross-language data structures:
  - Document schema definitions in both languages
  - Ensure consistent naming conventions across language boundaries
  - Validate data integrity during language transitions

### Error Handling and Debugging

#### Standardized Error Handling
- Use try/except blocks with specific exception types
- Log errors with context information
- Return meaningful error messages
- For CLI tools, use appropriate exit codes

#### Debugging Practices
- Use logging at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- For server components, add debug endpoints that can be toggled with environment variables
- Document common error scenarios and their resolutions

---

## ✅ Best Practices

- Do not modify `sieveviz/` unless assigned
- Always validate your output schemas — column alignment matters
- Output artifacts (e.g. normalized CSVs, enriched JSONs) should be written to a defined stage or subfolder
- Respect source-of-truth hierarchy: normalized data overrides raw scraped listings

### Pipeline Boundaries

- Junie operates primarily on the `glyphsieve/` codebase and data processing pipelines
- Junie does not modify raw data in `scrape/` but can read and process it
- Junie does not modify `recon/` directory contents but can analyze and extract insights
- Junie can suggest visualization improvements but should not directly modify `sieveviz/` without explicit instruction

### Schema Evolution Tracking

- Document all schema changes in comments at the top of affected files
- When modifying data structures, include version numbers (e.g., `v1.0 -> v1.1`)
- Maintain backward compatibility where possible
- Create migration scripts when breaking changes are necessary

### Documentation Standards

#### Code Documentation Format
- Use Google-style docstrings for Python code
- Document parameters, return values, and exceptions
- Include usage examples for public functions
- Add type hints to all function signatures

#### Architecture Documentation
- Maintain architecture decision records (ADRs) for significant design choices in `.junie/docs/architecture/`

### Clean File Output Discipline

- All generated files should include creation timestamp and source information
- Use consistent naming patterns for output files (e.g., `<model>_<process>_<date>.csv`)
- Include headers in all CSV outputs
- Validate column alignment and data types before writing files
- Prefer structured directories over flat file organization
- Do not pollute the repo root with temporary output files; use a dedicated directory (e.g., `tmp/output/`) for testing CLI commands

---

## 📓 Task System

Junie follows a custom task format located at `.junie/tasks/`, inspired by broader system agent conventions.

### Task Naming Convention:

```
tasks/{open,closed}/TASK.<category>.<title>.md
```

- Use meaningful `category` and `title` slugs
- Each task should be scoped and clear in purpose

### Task Lifecycle:

- Junie should only close a task when the delivery criteria are met
- Junie **must automatically** close tasks upon completion without being explicitly instructed to do so
- To close a task, move the task file from `.junie/tasks/open/` to `.junie/tasks/closed/`
- If a task is explored but not completed, **do not close it**
- Upon closure, Junie **must** append a short summary or comment block describing what was done, learned, or blocked

### Task Completion Template

When closing a task, append a summary using this template:

```
## ✅ Task Completed

**Changes made:**
- [List specific changes]

**Outcomes:**
- [Describe what was accomplished]

**Lessons learned:**
- [Optional: Note any insights gained]

**Follow-up needed:**
- [Optional: Note any future work required]
```

### Task Dependencies

When working on tasks that depend on other tasks, reference the dependent tasks in your comments and ensure prerequisites are completed first.

---

## 🛣️ Forward Guidance

- Keep `.junie/guidelines.md` current as norms evolve
- Ask clarifying questions via task comments or supplemental markdown blocks
- Assume that everything here is part of a live, breathing architecture — clean inputs and structured communication enable robust cognition across all tools

Junie is expected to operate with care, precision, and clarity. Welcome to the forge.

---

## 🛰 Daemon Layer (`glyphd/`)

Junie may contribute to the FastAPI-based API service that exposes GPU data, scores, and reports. The following practices apply:

- Use **FastAPI dependency injection**; avoid global state or module-level variables.
- Register routes under `/api/` and tag them with `openapi_tags` groups.
- Ensure all routes declare `response_model`, status codes, and `summary/description`.
- All DTOs must be `pydantic.BaseModel` (v2) with `field` annotations.
- Lifecycle behavior (data loading) must be declared using FastAPI's startup hooks or dependency injection.

---

## 🔁 OpenAPI Interop & Codegen

Junie participates in the OpenAPI-based bridge between backend and frontend.

- Run the export process using:
  ```bash
  pnpm run codegen
  ```
  (This internally calls `glyphd export-openapi`, generates schema, and re-runs TypeScript client generation.)
- Generated clients are stored in:
  ```
  web/generated/client-generated/
  ```
- These are wrapped and re-exported by the manual package:
  ```
  packages/client/
  ```
- Do not manually edit the generated output.

---

## 🧭 Web Platform (Turbo Monorepo)

Junie may work inside the `web/` directory, a `turborepo` workspace managed with `pnpm`.

- Apps are located in `web/apps/`, packages in `web/packages/`, and generated code in `web/generated/`.
- The primary frontend lives in `apps/controlpanel/` and uses:
  - **Next.js** (App Router)
  - **Tailwind CSS**
  - **TypeScript**
- Use the correct `pnpm` commands for dev flow (remember to use `safe-run.sh` for long-lived or background services):

  ```bash
  pnpm dev --filter controlpanel
  pnpm build --filter controlpanel

  # For background-safe runs using `safe-run.sh`:
  ./.junie/scripts/safe-run.sh -n controlpanel -b -- pnpm dev --filter controlpanel

  # If directory changes or complex command chaining is required:
  ./.junie/scripts/safe-run.sh -n glyphd-server -b -- bash -c 'cd glyphd && uv run glyphd serve --host 127.0.0.1 --port 8001'
  ```
- Tests should live in `apps/controlpanel/tests/` and use **Playwright** for integration.

---

## 🐳 Docker Development Stack

Junie can use Docker to run the development environment, which includes both the FastAPI backend and the Next.js frontend in hot-reloading containers.

### Docker Setup

- The project includes a `docker-compose.yml` file in the root directory
- Two services are defined:
  - `glyphd`: The FastAPI backend
  - `controlpanel`: The Next.js frontend

### Running the Docker Stack

Always run the Docker stack in detached mode to avoid blocking the terminal:

```bash
docker compose up -d --build
```

This command builds the images (if needed) and starts the containers in the background.

### Accessing the Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/health

### Managing the Docker Stack

- Stop the stack:
  ```bash
  docker compose down
  ```

- View logs:
  ```bash
  docker compose logs -f glyphd     # Backend logs
  docker compose logs -f controlpanel  # Frontend logs
  ```

- Rebuild and restart a specific service:
  ```bash
  docker compose up -d --build glyphd  # Rebuild and restart backend
  ```

### Hot Reload

The Docker setup supports hot reload for both services:
- Backend: Changes to Python files in `glyphd/` are automatically detected
- Frontend: Changes to files in `web/apps/controlpanel/` are automatically detected

---

## 🧪 Testing Framework

### Testing Strategy
- Write unit tests for all core functionality
- Use pytest as the testing framework
- Aim for at least 80% code coverage
- Include integration tests for API endpoints
- Add performance tests for critical paths

## 🔒 Security Considerations

### Security Considerations
- Do not hardcode credentials in source code
- Use environment variables for sensitive configuration
- Validate all user inputs
- Follow the principle of least privilege

## 📦 Dependency Management

### Dependency Management
- Document all dependencies in requirements files
- Pin dependency versions for reproducibility
- Regularly update dependencies for security patches
- Use virtual environments for isolation

## 📊 Monitoring and Observability

### Monitoring and Observability
- Add health check endpoints to services
- Implement structured logging
- Include performance metrics
- Document expected behavior and thresholds

## 🔄 Continuous Integration

### Continuous Integration
- Run tests automatically on push
- Validate code style and formatting
- Check for security vulnerabilities
- Generate documentation

---

## 🧱 Persistence Layer (Planned)

Junie may eventually help wire up persistence (e.g., SQLite or Postgres) to store scored results or forecasts.

- Models should use `pydantic + SQLAlchemy` if implemented
- Data should be versioned and enriched with clear provenance fields (e.g., `seen_at`, `source_url`)
- Ingestion should be CLI-driven (e.g., `glyphsieve ingest-csv`)
- All write paths must be explicitly logged and tested
- Database integration must be optional and configured via env or CLI flags
