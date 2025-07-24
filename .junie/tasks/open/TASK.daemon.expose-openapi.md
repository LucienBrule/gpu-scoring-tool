

# TASK.daemon.expose-openapi.md

## 🧩 Task: Expose OpenAPI Metadata for `glyphd`

Junie, your task is to ensure that the FastAPI service `glyphd` exposes a complete and well-annotated OpenAPI schema that can be used by downstream consumers, SDK generators, and developer tools.

---

## 🎯 Objectives

- Provide OpenAPI metadata and tags on all routes.
- Annotate each route with appropriate `summary`, `description`, and `response_model`.
- Define reusable response models for all endpoints using Pydantic v2.
- Make sure FastAPI's built-in `/docs` and `/openapi.json` routes are functional and reflect the current schema.

---

## 🧩 OpenAPI Metadata

In `main.py` or `app.py`, ensure the FastAPI app has:

```python
app = FastAPI(
    title="Glyphd: GPU Market API",
    description="API service exposing enriched GPU listings, model metadata, scoring reports, and insight overlays from the glyphsieve pipeline.",
    version="0.1.0",
    contact={
        "name": "Glyphsieve Research",
        "url": "https://github.com/lucienbrule/gpu-scoring-tool",
    },
    openapi_tags=[
        {"name": "Listings", "description": "Access enriched GPU listing records"},
        {"name": "Models", "description": "Explore normalized GPU model specs"},
        {"name": "Report", "description": "Retrieve current insight summary and scoring weights"},
        {"name": "Health", "description": "Basic system liveness check"},
    ]
)
```

---

## 📦 Requirements

- Add `tags=["Listings"]`, `tags=["Models"]`, etc. to each router.
- Define proper HTTP status codes (200, 404, etc.).
- Ensure that `/openapi.json` and `/docs` render cleanly with no schema warnings.

---

## 🧪 Completion Criteria

- Navigating to `/docs` shows a human-usable API UI with model schemas.
- Navigating to `/openapi.json` returns the valid OpenAPI schema.
- Routes include tag groupings and descriptions.
- DTOs are referenced properly and not inlined as anonymous objects.

---

## 💡 Notes

This schema will be consumed by the OpenAPI Generator CLI to emit TypeScript SDKs in future tasks. Correct structure and tagging is essential.

Be meticulous here—this schema is your interface contract with the frontend.