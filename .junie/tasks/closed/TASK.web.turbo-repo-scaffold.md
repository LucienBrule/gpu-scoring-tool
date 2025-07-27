

# TASK.web.turbo-repo-scaffold.md

## 🧩 Task: Scaffold a Turborepo-based PNPM Workspace for the Web Layer

Junie, your task is to create the baseline monorepo structure under the `web/` directory using [Turborepo](https://turbo.build/) and [pnpm workspaces](https://pnpm.io/workspaces). This will support our frontend (Next.js) and shared client packages for TypeScript interop.

---

## 🎯 Objectives

- Create a `web/` directory at the repo root
- Initialize a Turborepo layout with:
  - `apps/controlpanel/` → a Next.js 14+ app using TypeScript and Tailwind
  - `packages/client/` → placeholder package to hold OpenAPI-generated TypeScript SDK code

---

## 📦 Directory Layout

```
web/
├── apps/
│   └── controlpanel/
├── packages/
│   └── client/
├── pnpm-workspace.yaml
├── turbo.json
└── README.md
```

---

## 🧪 Requirements

- Use the **App Router** (not Pages) in the Next.js app
- The control panel should:
  - Build and run using `pnpm dev --filter controlpanel`
  - Render a home page at `/`
  - Use Tailwind CSS and TypeScript
- The client package must compile cleanly (even if empty)

---

## 📦 Steps

1. Initialize the Turborepo from the `web/` directory:
   ```bash
   pnpm init
   pnpm add -D turbo
   ```

2. Scaffold the Next.js control panel using:
   ```bash
   pnpm create next-app apps/controlpanel --ts --app --tailwind --eslint
   ```

3. Create an empty TypeScript package at `packages/client`:
   - Add a `package.json`
   - Include `"private": true` and `"type": "module"`

4. Create `pnpm-workspace.yaml`:
   ```yaml
   packages:
     - 'apps/*'
     - 'packages/*'
   ```

5. Create `turbo.json`:
   ```json
   {
     "$schema": "https://turbo.build/schema.json",
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": [".next/**", "dist/**"]
       },
       "dev": {
         "cache": false
       }
     }
   }
   ```

---

## ✅ Completion Criteria

- Running `pnpm install` at the `web/` root bootstraps both packages
- `pnpm dev --filter controlpanel` starts the Next.js app
- `packages/client/` exists, compiles, and is ready for OpenAPI codegen

---

## ✍️ Notes

This repo will grow over time. Structure matters. Your work here sets the foundation for the full web UI, API client interop, and test automation. Make it clean, conventional, and forward-looking.


Note: done manually since pnpm create command hangs in Junie