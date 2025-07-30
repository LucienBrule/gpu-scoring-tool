# Lint Compliance Reflection

## What Each Rule Taught Me About the System's Architecture

### GLS001 — No Path-Based Resource Access

This rule enforces a clean abstraction for resource loading. By prohibiting direct path-based access like `Path(__file__)` or `os.path.dirname(__file__)`, the system ensures:

1. **Resource location independence**: Resources can be moved or reorganized without breaking code that depends on them.
2. **Packaging compatibility**: The code works correctly when packaged (e.g., as a wheel) where file paths may differ from development.
3. **Testability**: Resources can be mocked or substituted during testing without modifying file paths.

The `YamlLoader` abstraction provides a clean interface for loading resources, making the code more maintainable and flexible.

### GLS002 — Typed Model Returns for `load_*` Functions

This rule enforces type safety and data validation by requiring all `load_*` functions to return Pydantic models rather than raw dictionaries. This ensures:

1. **Data validation**: All loaded data is validated against a schema.
2. **Type safety**: Consumers of the loaded data know exactly what structure to expect.
3. **Documentation**: The data structure is self-documenting through the model definition.
4. **Consistency**: All resource loading follows the same pattern.

This was particularly evident when refactoring `load_gpu_specs()` to return a `GPURegistry` model instead of a dictionary, which required updating the consuming code to handle the model properly.

### GLS003 — Models Must Live in `/models/`

This rule enforces a clear separation between data models and business logic. By requiring all Pydantic models to be defined in files within the `/models/` directory, the system ensures:

1. **Separation of concerns**: Data models are separate from the code that uses them.
2. **Discoverability**: Models are easy to find and understand.
3. **Reusability**: Models can be reused across different parts of the codebase.
4. **Consistency**: All models follow the same organizational pattern.

Moving the `HeuristicConfig` and `QuantizationHeuristicConfig` classes from `heuristics.py` to `models/heuristic.py` made the code more organized and maintainable.

## Questions or Confusion Encountered

1. **Balancing backward compatibility with architectural rules**: When refactoring `load_gpu_specs()` to return a Pydantic model instead of a dictionary, I had to carefully update the consuming code to maintain backward compatibility. This required understanding how the function was used throughout the codebase.

2. **Test dependencies on implementation details**: The tests in `test_enrichment.py` were tightly coupled to the implementation details of `load_gpu_specs()`, expecting it to return a dictionary. This made the refactoring more challenging and required updating the tests to work with the new approach.

3. **Resource loading abstraction**: The `YamlLoader` class provides a good abstraction for loading YAML resources, but it's not immediately clear how to handle other resource types or how to mock resources during testing.

## Suggestions for Improving the Guidelines

1. **Add examples of proper resource loading**: Include concrete examples of how to use the `YamlLoader` and other resource loaders correctly, especially for common use cases like loading YAML, JSON, or CSV files.

2. **Clarify backward compatibility expectations**: Provide guidance on how to handle backward compatibility when refactoring code to comply with architectural rules, especially when the changes affect public APIs or interfaces used by other parts of the codebase.

3. **Document testing strategies**: Include recommendations for testing code that uses resource loaders, such as how to mock resources or set up test fixtures.

4. **Explain the rationale behind each rule**: While the rules themselves are clear, it would be helpful to understand the specific problems they're designed to solve and the benefits they provide.

5. **Provide migration paths**: For existing code that violates the rules, suggest step-by-step approaches for refactoring it to comply with the architectural guidelines.

6. **Clarify model organization**: Provide more guidance on how models should be organized within the `/models/` directory, such as whether they should be grouped by domain, functionality, or some other criteria.

By following these architectural rules, the codebase becomes more maintainable, testable, and consistent. The rules enforce good practices that make the system more robust and easier to understand for new developers.

## Additional Reflections on GLS004 and GLS005

### GLS004 — Import Discipline

This rule enforces proper abstraction for resource imports by prohibiting direct imports from `glyphsieve.resources`. By requiring the use of a loader or broker function to access resource files, the system ensures:

1. **Abstraction integrity**: Resources are accessed through a well-defined interface rather than directly.
2. **Version control**: Changes to resource formats or locations can be managed in a single place.
3. **Type safety**: Resources are loaded with appropriate validation and typing.

### GLS005 — Filesystem Resource Path Violations

This rule prohibits hardcoding paths like `Path("glyphsieve/resources/...")` and requires using the `YamlLoader().load(...)` method with the appropriate model and filename. This ensures:

1. **Path independence**: Code doesn't rely on specific filesystem paths that might change.
2. **Resource abstraction**: Resources are accessed through a typed interface rather than as raw files.
3. **Cross-module consistency**: Resources are accessed the same way throughout the codebase.
4. **Packaging compatibility**: Resources can be accessed correctly regardless of how the package is installed or deployed.

When fixing GLS005 violations in `glyphd/src/glyphd/core/loader.py`, I replaced hardcoded paths with the `YamlLoader` abstraction, which not only fixed the linter violations but also made the code more robust and maintainable. The changes also simplified the code by leveraging the typed models (`GPURegistry` and `ScoringWeights`) instead of manually parsing YAML data.