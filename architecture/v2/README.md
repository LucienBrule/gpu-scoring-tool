# v2 Architecture – Modular Plugin Runtime

This document outlines the future direction of the GPU Scoring Tool as it evolves into a **plugin-based,
category-agnostic signal processing runtime**. The v2 architecture focuses on modularity, composability, and horizontal
scalability across categories such as GPUs, DPUs, and Servers.

---

## 🧠 Architectural Vision

Unlike the monolithic v1 stack, v2 will adopt a **plugin-oriented monolith** model:

- A shared core defines pipeline interfaces, models, and lifecycle coordination.
- Category-specific logic (e.g. GPU, DPU, Server) is implemented as plugins.
- The FastAPI daemon (`glyphd`) loads these plugins dynamically at runtime.
- CLI and API commands are routed by category.

---

## 🧱 Core Components

### 1. `sieve-core/` (new package)

- Contains:
    - `BaseListingDTO` (shared Pydantic base)
    - `BasePipeline`, `BaseScoringStrategy`, `BaseHeuristic` (ABC interfaces)
    - Plugin loader (e.g. via `importlib.metadata` or custom registry)
- Responsible for orchestrating:
    - Pipeline composition
    - CLI command routing
    - FastAPI dependency injection

### 2. `glyphd/` (updated)

- Becomes a **universal signal daemon**
- Loads category pipelines at startup (via plugin interface)
- Serves OpenAPI for:
    - `/categories`
    - `/listings?category=...`
    - `/score`, `/report`, etc.
- Supports emitting OpenAPI spec per category (namespaced or merged)

### 3. Category Plugins (separate UV packages)

- Example: `gpu-sieve/`, `dpu-sieve/`, `server-sieve/`
- Each plugin implements:
    - `ListingDTO` for its domain
    - `normalize()`, `enrich()`, `score()`, etc.
    - Heuristic and scoring strategies
    - YAML-backed metadata/spec

### 4. `glyphsieve` CLI (wrapper)

- Unified CLI that delegates to category-specific pipelines
- Supports:
  ```bash
  glyphsieve pipeline run --category=gpu
  glyphsieve pipeline score --category=dpu
  glyphsieve normalize --category=server
  ```

### 5. Web Client (unchanged)

- Still uses TurboRepo / Next.js
- TS client is generated via OpenAPI from `glyphd`
- UI adapts based on category introspection (`GET /categories`)

---

## 🔄 Data Flow

```
CSV scrape →
normalize(category) →
enrich(category) →
score(category) →
store →
serve →
visualize
```

All operations route through the category-aware plugin runtime.

---

## 🛠️ Benefits

- ✨ Add new hardware domains with minimal boilerplate
- 🧪 Reuse tests, DTOs, heuristics across domains
- 🧱 Run scoped containers (e.g., only GPU plugins in one, DPU in another)
- 🧠 Extendable for LLMs, NICs, ARM inference chips, etc.

---

## 🧭 Migration Plan

1. Complete v1 GPU stack
2. Refactor `glyphsieve/` into `gpu-sieve/`
3. Create `sieve-core/` with abstract pipeline & DTOs
4. Rewrite `glyphd` to use plugin loader
5. Move CLI to dynamic registry-based entrypoints
6. Test category routing end-to-end (CLI + API + Web)

---

## 🧬 Symbolic Summary

> **v1** taught us to see.  
> **v2** teaches us to *see across*.  
> We go from *pipeline* to *platform*.  
> From *one lens* to *a lattice of insight*.  