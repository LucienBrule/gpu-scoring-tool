

# TASK.web.openapi-codegen-cli-export.md

## 🧩 Task: Generate and Import TypeScript OpenAPI Client

Junie, your task is to implement OpenAPI-driven code generation for the `glyphd` backend and connect the result to the Next.js frontend. This will complete the typed frontend-to-backend bridge.

---

## 🎯 Objectives

1. In `glyphd`, add a CLI subcommand:
   - `glyphd export-openapi`
   - This command should:
     - Start a FastAPI app instance **without serving**
     - Emit the OpenAPI schema to a target path as `openapi.json`

2. In `web/packages/client`, create a `pnpm run codegen` script that:
   - Runs `openapi-generator-cli`
   - Targets the `openapi.json` from the step above
   - Outputs generated code into `packages/client/src/`

3. In `apps/controlpanel`, import the generated SDK
   - Demonstrate by importing one method (e.g. `getHealth()`)
   - Use it in a sample layout or hook (`/app/page.tsx`)

---

## 🛠️ Instructions

### 📦 Backend CLI (`glyphd`)
- Implement `export-openapi` in the `click` CLI
- Should call `get_openapi()` and write to disk:
  ```python
  from fastapi.openapi.utils import get_openapi
  ```

### 📦 Frontend Client (`web/packages/client`)
- Create a `codegen.ts` wrapper script (Node or shell)
- Add `openapi-generator-cli` to `devDependencies`
- Configure codegen:
  - Generator: `typescript-fetch`
  - Input: `glyphd`'s OpenAPI file
  - Output: `./src/`

### 📦 Control Panel App (`web/apps/controlpanel`)
- Add this import to any test page:
  ```ts
  import { getHealth } from "@client";
  ```
- Use it inside `page.tsx` or a test `useEffect`

---

## ✅ Completion Criteria

- `pnpm run codegen` works and populates `client/src/`
- `apps/controlpanel` compiles and renders successfully
- At least one API function is imported and used
- `glyphd export-openapi` emits a valid OpenAPI schema to the correct directory

---

## 📎 Notes

This is your first interop bridge between the backend and frontend. Make sure it’s deterministic and reproducible. We'll build automated refresh and CI integration on top of this foundation.