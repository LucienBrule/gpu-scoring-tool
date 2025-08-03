## 🐛 TASK.web.09a — Bug‑fix / Refactor TanStack Query Hooks  
*Unify hook location so that every invocation sits inside a `QueryClientProvider`.*

---

### 🧠 Why this matters  
`TanStack Query` hooks **must** be executed within the React subtree that owns the `QueryClientProvider`.  
Placing hooks in **`packages/client`** means they can be imported (and therefore evaluated) by *any* consumer ― including server‑side code or separate apps ― without a provider in scope.  
At runtime this raises the dreaded ✖ **"No QueryClient set"** error and breaks pages such as **`/listings`**.

---

### 🔨 Required Changes  

1. **Migrate hooks**  
   - Move every file under  
     ```
     packages/client/src/hooks/
     ```  
     → **`apps/controlpanel/src/hooks/`**

2. **Update imports** inside *only* the controlpanel app:  
   - Search for `from "@client/hooks"` or similar path aliases.  
   - Replace with relative imports:  
     ```ts
     import { useListings } from "@/hooks/useListings";
     ```

3. **Remove hook code‑gen**  
   - Delete the following *and* their references:  
     ```
     packages/client/scripts/generate-hooks*.js
     packages/client/src/hooks/**
     ```
   - Ensure `pnpm run codegen` in `packages/client` now produces only the OpenAPI client (no hooks).

4. **Tidy package exports**  
   - `packages/client` should re‑export **only**:  
     - Generated API runtime  
     - DTO types  
     - Top‑level API classes  
   - No React code remains.

5. **Configuration / TS paths**  
   - If `tsconfig.json` previously mapped `@client/hooks`, remove that alias.  
   - Verify that `apps/controlpanel/tsconfig.json` resolves `@/hooks/*`.

6. **Lint & tests**  
   ```bash
   pnpm lint --filter controlpanel
   pnpm test:unit --filter controlpanel
   pnpm test:e2e  --filter controlpanel   # requires docker‑stack up
   ```

---

### ✅ Completion Criteria  

| # | Requirement |
|---|-------------|
| 1 | All hooks live under `apps/controlpanel/src/hooks/` |
| 2 | `pnpm dev --filter controlpanel` renders **/listings** without QueryClient errors |
| 3 | Unit tests in `src/hooks/tests/` pass and cover the migrated hooks |
| 4 | Playwright integration suite passes end‑to‑end |
| 5 | `packages/client` no longer contains **any** `.tsx?` files or React imports |
| 6 | Task file moved to `.junie/tasks/closed/` with a short completion summary |

---

### 💡 Hints  
- After moving files, run `pnpm changeset status` (if enabled) to ensure package versions stay consistent.  
- Running `grep -R "useListings" web/ | cut -c1-120` can help spot stale import paths quickly.  
- Remember to restart **safe‑run** `dockerstack` if you change API port mappings.

---

Happy refactoring — this unblocks every future page that relies on data‑fetching hooks! 🚀

## ✅ Task Completed
**Changes made**
- Moved all hook files from `packages/client/src/hooks/` to `apps/controlpanel/src/hooks/`
- Updated imports in the moved hook files to use `@repo/client` instead of relative paths
- Updated the hooks index.ts file to export all hooks correctly
- Updated client package's index.ts to remove hooks export and add exports for getListings and getModels
- Updated all import references to the hooks in the controlpanel app to use `@/hooks` instead of `@repo/client`
- Removed hook code-gen scripts and their references
- Removed the hooks directory from the client package
- Fixed ESLint errors in useModels.test.ts by replacing `any` with `unknown` and `GPUModelDTO`
- Rebuilt the client package to ensure the changes take effect
- Verified that the /listings page renders without QueryClient errors

**Outcomes**
- All hooks now live under `apps/controlpanel/src/hooks/`
- The /listings page renders without QueryClient errors
- The hook tests pass and cover the migrated hooks
- The client package no longer contains any React code
- The project structure is now more maintainable with hooks properly scoped to the app that uses them
- This change unblocks all future pages that rely on data-fetching hooks