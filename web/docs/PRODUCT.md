# Web UI – Product Overview

The `web/` directory contains the frontend interface for the GPU Scoring Tool. It serves as the primary user-facing application for browsing scored GPU listings, tracking price trends, and interpreting market insights derived from the glyphsieve pipeline.

## Purpose

The web interface provides a clean, responsive, and filterable view into the enriched GPU dataset. It is built with TypeScript, Next.js (App Router), Tailwind CSS, and is structured as a Turbo monorepo for scalable component reuse.

## Features

- 🔍 **Listings & Reports**: Interactive reports filtered by model, price range, score range, and other criteria.
- 📊 **Score Visualizations**: Tables with color-coded price/GB, score, and metadata indicators (TDP, MIG, NVLink, etc.).
- 🧪 **End-to-End Tested**: Verified via Playwright integration tests inside Docker Compose.
- 📦 **Stable API Client**: Uses a wrapped client architecture that consumes the OpenAPI-generated SDK from `client-generated`.
- 📱 **Responsive Design**: Mobile-friendly layout tested across viewports.
- 🔁 **Live Integration**: Communicates with the `glyphd` FastAPI backend running via Docker Compose.

## Usage

The app is served via Docker Compose (`http://localhost:3000`) and connects to the `glyphd` service on port `8080`. All API requests use the generated client with typed interfaces.

## Architecture

- `apps/controlpanel`: Main Next.js application.
- `packages/client`: Wrapper SDK for generated API.
- `generated/client-generated`: OpenAPI codegen target.
- `apps/controlpanel/src/tests`: Playwright integration tests.

## Future Extensions

- 🛎 Additional views for historical pricing, quantization support, and comparison
- 🧠 Filter presets powered by model metadata
- 📬 Integration with alerting/report generation pipelines
- 🔒 Auth and dashboarding for private listings or sourcing tools

## Development Notes

- Run `pnpm codegen` to regenerate the API client.
- Do not run the dev server directly — use `docker compose up -d --build`.
- Update tests and adhere to internal lint/style guidelines.

---
This UI is a key presentation layer for glyphsieve's insights and marks the completion of the V1 milestone.
