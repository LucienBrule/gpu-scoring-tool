

## TASK.ingest.05.api.schema-versioning-support

## ✍️ Planning Commentary

**Current State:** The glyphd service uses Pydantic models for validation but doesn't have explicit schema versioning. The existing `ImportResultDTO` and `GPUListingDTO` are implicitly "v1" schemas.

**Strategic Value:** This task enables API evolution without breaking existing clients. It's foundational for long-term API stability as the ingestion system grows.

**Implementation Approach:** Should leverage Pydantic's discriminated unions or enum-based validation to handle multiple schema versions gracefully.

---

### 🎯 Goal

Introduce support for API schema versioning within the ingestion system, enabling explicit control over format changes, backward compatibility, and validation against known schema versions.

---

### 🧩 Motivation

As the GPU listing ingestion API evolves, breaking changes in input or output formats could destabilize dependent systems. Schema versioning allows the pipeline to reason about payload compatibility, validate against expected structures, and introduce new fields or behaviors in a controlled fashion.

---

### 📐 Requirements

- Add a `schema_version` field to `ImportRequestDTO` and `ImportResultDTO`
- Accept version strings such as `"v1"`, `"v1.1"`, `"v2-beta"`
- Default to `"v1"` if not specified
- Extend Pydantic validators to enforce version support
- Implement runtime validation logic (e.g., reject unsupported versions with 4xx errors)
- Expose supported versions as a static list in code and docs

---

### 🛠 Implementation Notes

- Use an Enum or Literal type in Pydantic to define allowed schema versions
- Consider reading supported versions from a static resource (e.g. `resources/schemas/supported_versions.yaml`)
- Update `glyphd` API route and DTO logic accordingly
- Extend OpenAPI doc annotations to reflect schema version usage

---

### ✅ Completion Criteria

- `ImportRequestDTO` and `ImportResultDTO` include a `schema_version` field
- `schema_version` is validated at request time
- Unsupported schema versions return a structured 400 error
- Unit tests exist for accepted and rejected versions
- OpenAPI documentation reflects schema versioning
- Static list of supported schema versions is defined in code and resource

---

### 🧠 Background

This task lays groundwork for long-term API stability and future evolution of the ingestion pipeline. It also supports future CLI and agent use where schema negotiation may be required.