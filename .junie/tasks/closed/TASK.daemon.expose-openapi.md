# TASK.daemon.expose-openapi.md

## 🧩 Task: Expose OpenAPI Metadata for `glyphd`

Junie, your task is to ensure that the FastAPI service `glyphd` exposes a complete and well-annotated OpenAPI schema that can be used by downstream consumers, SDK generators, and developer tools.

---

## 📌 Best Practices

- You **must use Pydantic v2 models** with `Field(...)` for all request and response schemas.
  - Avoid using `pydantic.v1` compatibility imports.
- In route decorators, set:
  ```python
  response_model_exclude_none=True
  ```
  to suppress optional fields that are unset in the output.
- Do **not** return ad-hoc `dict` values directly from routes.
  - Every route must return a validated, structured DTO.

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

---

## ✅ Task Completed

I've successfully implemented the OpenAPI metadata for the glyphd service. Here's what I did:

1. Verified that all routes have appropriate tags, summaries, descriptions, and response models.
2. Confirmed that all DTOs (GPUListingDTO, GPUModelDTO, ReportDTO) are using Pydantic v2 models with Field annotations.
3. Updated the FastAPI app metadata in router.py to match the requirements:
   - Set the title to "Glyphd: GPU Market API"
   - Updated the description to be more detailed
   - Added contact information
   - Added openapi_tags with descriptions for each tag
4. Verified that the OpenAPI endpoints (/docs and /openapi.json) are functional.

The glyphd service now exposes a complete and well-annotated OpenAPI schema that can be used by downstream consumers, SDK generators, and developer tools.