# Architecture Overview

This directory contains versioned architecture documentation for the GPU Scoring and Signal Platform. We are currently
operating under the `v1` architecture, with a planned transition to `v2` that introduces plugin-based modularity across
multiple signal domains.

## Current Architecture: v1

The current system (v1) consists of:

- A monolithic Python pipeline (`glyphsieve`) built with Click
- A FastAPI service (`glyphd`) that loads scored listing data from CSV
- A web frontend (Next.js + Tailwind) consuming OpenAPI-generated clients
- GPU listings only, with CLI-first workflows and an emphasis on CSV normalization, scoring, and insight generation

See: [v1/README.md](v1/README.md)

## Planned Architecture: v2

The upcoming architecture (v2) will:

- Introduce `sieve-core` with abstract pipeline interfaces and shared DTOs
- Modularize domain-specific logic into plugins (e.g. `gpu-sieve`, `dpu-sieve`)
- Allow category-specific heuristics, scoring, enrichment, and persistence
- Keep a unified FastAPI daemon (`glyphd`) that loads plugin pipelines at runtime
- Retain the same frontend + OpenAPI flow with support for multiple signal domains

See: [v2/README.md](v2/README.md)
