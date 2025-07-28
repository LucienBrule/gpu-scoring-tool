> You are Junie — a daemon committed to excellence, precision, and clean Python code.
> You believe in strong types, explicit contracts, and tests that reflect *intent*, not just behavior.
> You detest brittle test scaffolds and loathe patching over structural rot.
>
> Your mission: bring `glyphd` into full architectural compliance.
> Not to silence the linter, but to refactor with understanding — and leave the system stronger than you found it.

# TASK.lint.glyphd.md

## Objective

Refactor `glyphd/src` to bring it into compliance with architectural linter rules GLS001 through GLS005. This task follows the same process and philosophy as the completed `glyphsieve` compliance task.

Please reference:
- `.junie/tasks/closed/TASK.lint.fix-violations.md`
- `.junie/status/lint_compliance_reflection.md`

for prior context, rationale, and expected patterns.

---

## Workflow

1. Run all linting tools from the project root:

   ```bash
   flake8 glyphd/src
   isort glyphd/src
   black glyphd/src
   ruff check glyphd/src
   ```

2. Triage violations. Address the following:

   - `GLS001`: Replace filesystem access or path composition with a resource loader.
   - `GLS002`: All `load_*` functions must return DTOs or typed containers of DTOs.
   - `GLS003`: Ensure any `BaseModel` subclass is defined inside a `models/` directory.
   - `GLS004`: Do not import from `glyphsieve.resources` directly — use the broker interface.
   - `GLS005`: Do not hardcode `Path("glyphsieve/resources/...")` — load resources with a loader abstraction.

3. After each change, test the system from the repo root:

   ```bash
   pytest
   ```

   All tests must pass. Do not skip or suppress failures.

4. Do **not** silence lint errors with `# noqa`. Do **not** move code just to bypass rules. All fixes must resolve the underlying structural issue.

5. If you're unsure how to resolve a rule, log your thoughts in:

   ```bash
   .junie/status/GLS_violations.md
   ```

6. Once the linter passes with no `GLS###` violations and all tests pass, the task is complete.

---

## Final Step

After finishing, return to your guidelines and reflect on anything new you learned, any confusing rules, or refinements you suggest to clarify future tasks. You may update `.junie/guidelines.md` or append to your compliance reflection.

## ✅ Task Completed

**Changes made:**
- Fixed GLS005 violations in `glyphd/src/glyphd/core/loader.py` by replacing hardcoded paths with the `YamlLoader` abstraction
- Added necessary imports for `YamlLoader`, `GPURegistry`, and `ScoringWeights`
- Replaced hardcoded path `Path("glyphsieve/src/glyphsieve/resources/gpu_specs.yaml")` with `YamlLoader().load(GPURegistry, "gpu_specs.yaml")`
- Replaced hardcoded path `Path("glyphsieve/resources/scoring_weights.yaml")` with `YamlLoader().load(ScoringWeights, "scoring_weights.yaml")`
- Simplified the code by directly accessing properties of the typed models instead of manually parsing YAML data
- Removed the unused `yaml` import after replacing direct YAML parsing with the `YamlLoader`
- Updated `.junie/status/lint_compliance_reflection.md` with reflections on GLS004 and GLS005 rules

**Outcomes:**
- All GLS005 violations in the `glyphd/src` codebase have been resolved
- All tests are passing (75 tests)
- The code now follows the architectural policies without suppressing any warnings
- The codebase is more maintainable, testable, and consistent

**Lessons learned:**
- Resource loading abstractions like `YamlLoader` provide a clean, type-safe way to access resources
- Using typed models (`GPURegistry` and `ScoringWeights`) instead of raw dictionaries improves code clarity and safety
- Architectural rules enforce good practices that make the system more robust and easier to understand
- The same architectural principles apply across different modules in the codebase

**Follow-up needed:**
- There are some other linting issues (E501, C901) that could be addressed in future tasks, but they're not related to the GLS rules