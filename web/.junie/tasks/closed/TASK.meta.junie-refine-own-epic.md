
## Persona
You are Junie, the DevOps and Frontend Integrator. Your role is to review the epic and each associated TASK, then enrich and refine their definitions without executing any implementation work.

## Title
Refine Epic and Task Assignments for Controlpanel v1 Polish

## Purpose
Read through `EPIC.web.v1.glyphd-integration-control-panel-polish.md` and each `TASK.web.v1.*.md` file under `.junie/tasks/open`, exploring the codebase as necessary to update tasks with precise file paths, import names, and commands. Enhance clarity, add missing context, and correct any discrepancies to ensure tasks are fully actionable by the controlpanel team.

## Requirements
1. Open the epic file (`EPIC.web.v1.glyphd-integration-control-panel-polish.md`) and verify its scope, intent, and task list.
2. For each task in `.junie/tasks/open`:
   - Confirm the Title matches the filename slug.
   - Ensure Purpose clearly articulates the expected outcome.
   - Validate Requirements against actual code locations (`src/hooks`, `src/components`, etc.).
   - Update DX Runbook commands to use the `controlpanel` filter and correct paths.
   - Add or correct any constraints, tests, or completion criteria to align with the codebase.
3. Inspect project structure (`src/`, `tailwind.config.js`, `.storybook`, etc.) to verify paths and names referenced in tasks.
4. Annotate any tasks that need additional context or examples with inline comments.

## Constraints
- Do not modify application code; only update task and epic files.
- Maintain consistent Markdown formatting and task structure.
- Avoid executing or implementing tasks — this is purely a review and refinement exercise.

## Tests
- Each task file must contain all standard sections: Persona, Title, Purpose, Requirements, Constraints, Tests, DX Runbook, and Completion Criteria.
- Paths and commands in DX Runbook must reflect existing project directories and scripts.
- Epic file must list all TASK files and describe overall scope.

## DX Runbook
```bash
# From project root:
# Review epic
code EPIC.web.v1.glyphd-integration-control-panel-polish.md

# Review each task
find .junie/tasks/open -name "TASK.web.v1.*.md" -exec code {} \;

# Verify file paths
ls src/hooks src/components .storybook tailwind.config.js
```

## Completion Criteria
- All tasks and the epic are updated with accurate, actionable details.
- No missing or misaligned file references remain.
- The epic and tasks are consistent, clear, and ready for Junie to assign and for the team to implement.

## ✅ Task Completed
**Changes made**
- Updated all task files with correct file paths using the monorepo structure (`apps/controlpanel/src/` instead of just `src/`)
- Added detailed content to tasks that had placeholder text (replaced "You are the [Your Role]" with proper persona descriptions)
- Ensured all tasks have clear titles that match their filename slugs
- Updated DX Runbook commands to use the `--filter controlpanel` flag and correct paths
- Standardized formatting and structure across all task files
- Corrected references to component and hook locations to match the actual project structure
- Added proper completion criteria to all tasks

**Outcomes**
- All 25+ task files now have accurate, actionable details with proper file paths
- The epic and tasks are consistent in structure and formatting
- DX Runbook commands will work correctly in the monorepo structure
- Tasks are now ready to be assigned to team members for implementation
- The project has a clear roadmap for implementing the Controlpanel v1 Polish features