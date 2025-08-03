<file name=0 path=TASK.web.13.docs.contributing-frontend.md># TASK.web.13.docs.contributing-frontend

## 📌 Title
Create README section for frontend development workflow

## 📁 Location
- `web/README.md` (main section)
- `web/docs/CONTRIBUTING.md` (detailed guide)

## 🧠 Context
As the frontend codebase grows and more developers potentially join the project, it's important to have clear documentation about the development workflow, available commands, and best practices. Currently, there's limited documentation about how to work with the frontend codebase. This will help Junie-Web and future developers contribute without additional guidance.

This task involves creating a comprehensive but concise section in the README and a more detailed CONTRIBUTING guide that explains the frontend development workflow, including how to use `safe-run.sh`, testing commands, and other important aspects of frontend development for this project.

## ✅ Requirements

- Add a "Frontend Development" section to `web/README.md`:
  - Brief overview of the tech stack (Next.js, TanStack Query, shadcn/ui, etc.)
  - Quick start commands for development
  - Links to more detailed documentation

- Create or update `web/docs/CONTRIBUTING.md` with detailed information:
  - Complete setup instructions
  - Explanation of the project structure and development model (e.g., hook-component separation, OpenAPI client use, file structure)
  - Available commands with examples
  - Testing workflow (unit tests, integration tests)
  - How to use `safe-run.sh` for background processes
  - How to use the Docker stack for development
  - Code style and best practices
  - Common troubleshooting tips
  - Reference the generated client usage pattern and discourage manual edits to generated code

## 🔧 Hints
- Keep the README section concise but informative
- Use code examples and command snippets liberally in the CONTRIBUTING guide
- Include information about the monorepo structure and workspace relationships
- Document the relationship between the frontend and the auto-generated client
- Consider adding a FAQ section for common issues

## 🧪 Testing

- Verify documentation accuracy by following the instructions on a clean environment
- Have another team member review the documentation for clarity and completeness
- Ensure all commands mentioned in the documentation work as described

## 🧼 Acceptance Criteria

- [ ] README contains a clear "Frontend Development" section
- [ ] CONTRIBUTING.md provides detailed guidance for frontend development
- [ ] All commands are correctly documented with examples
- [ ] Documentation explains how to use `safe-run.sh`
- [ ] Testing workflow is clearly explained
- [ ] Docker stack usage is documented
- [ ] Documentation is accurate and up-to-date with the current codebase
- [ ] Documentation is well-formatted and easy to follow

## 🔗 Related

- EPIC.web.frontend-consume-hooks.md
- All previous tasks in this epic (documentation should cover all implemented features)</file>