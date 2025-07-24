# TASK.daemon.bootstrap-fastapi-service.md

## 🧩 Task: Bootstrap `glyphd` FastAPI Service

Junie, your task is to scaffold a new FastAPI-based service project named `glyphd` within the `gpu-scoring-tool` repository. This daemon will eventually expose pipeline outputs via a live API. You are building the operational and runtime entrypoint for the scoring backend.

---

## 🎯 Objectives

- Create a new `uv`-managed Python project named `glyphd`
- Register it as a workspace member in the existing uv workspace
- Add `FastAPI`, `Uvicorn`, `Click`, and `pydantic` as dependencies
- Scaffold the basic app structure and CLI interface

---

## 🧱 Project Structure

```
glyphd/
├── pyproject.toml
└── src/
    └── glyphd/
        ├── __main__.py              # Entry point via `uv run glyphd`
        ├── cli.py                   # Click CLI definition
        └── api/
            └── router.py           # FastAPI router w/ health check
```

---

## ⚙️ CLI Behavior

- Use `click` to implement a CLI under `glyphd.cli`
- Subcommand: `serve` — runs the FastAPI app with `uvicorn`
- CLI must support additional subcommands in the future
- Example usage:
  ```bash
  uv run glyphd serve --host 0.0.0.0 --port 8080
  ```

---

## 🌐 FastAPI Router (MVP)

- Mount at `/api`
- Define at least one route:
  - `GET /api/health` → `{ "status": "ok" }`

---

## 📦 Dependencies to Install

Run from inside the `glyphd/` directory:
```bash
uv add fastapi uvicorn click pydantic
```

---

## 🧪 Completion Criteria

- `uv run glyphd serve` starts the dev server
- `GET /api/health` returns 200 with `{"status": "ok"}`
- CLI subcommand interface is wired correctly
- Project is cleanly isolated but ready to import `glyphsieve` as a dependency later

---

## ✍️ Notes

This scaffolding will become the core of the GPU market API. Make sure it's cleanly bootstrapped and structured for CLI and API extensibility.

---

## ✅ Task Completed

This task has been completed. The following was done:

1. Created a new `uv`-managed Python project named `glyphd`
2. Registered it as a workspace member in the existing uv workspace
3. Added `FastAPI`, `Uvicorn`, `Click`, and `pydantic` as dependencies
4. Scaffolded the basic app structure and CLI interface:
   - Created `__main__.py` as the entry point
   - Created `cli.py` with the Click CLI definition
   - Created `api/router.py` with the FastAPI router and health check endpoint

The implementation meets all the completion criteria:
- The CLI subcommand interface is wired correctly with a `serve` command that runs the FastAPI app with uvicorn
- The FastAPI router is mounted at `/api` and includes a health check endpoint that returns `{"status": "ok"}`
- The project is cleanly isolated but ready to import `glyphsieve` as a dependency later

Additionally, a comprehensive test suite was created to verify the implementation:
- Tests for the API endpoints using FastAPI's TestClient
- Tests for the CLI functionality using Click's CliRunner
- All tests pass, confirming that the implementation meets the requirements