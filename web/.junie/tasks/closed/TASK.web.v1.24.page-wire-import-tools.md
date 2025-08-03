## Persona
You are the Frontend UI Engineer. Your role is to build a comprehensive Import Tools page that combines multiple data import hooks (`useImportCsv`, `useImportFromPipeline`, and `useValidateArtifact`) with intuitive upload forms and import controls.

## Title
Build Import Tools Page with Multiple Import Methods

## Purpose
Create a unified Import Tools page that provides administrators and data managers with multiple methods to import, validate, and process GPU data. This centralized interface will streamline data management workflows, ensure data quality through validation, and provide clear feedback on import operations.

## Requirements
1. Create a new Import Tools page component in `apps/controlpanel/src/app/import/page.tsx` (or equivalent path).
2. Import and implement the following hooks:
   - `useImportCsv` from TASK.web.v1.17
   - `useImportFromPipeline` from TASK.web.v1.18
   - `useValidateArtifact` from TASK.web.v1.1A
3. Design a tabbed or sectioned interface with:
   - CSV Import section with file upload
   - Pipeline Import section with source selection
   - Artifact Validation section with file upload
4. Implement file upload components with:
   - Drag-and-drop support
   - File type validation
   - Size limit indicators
   - Progress tracking
5. Create configuration forms for each import method:
   - CSV import options (column mapping, validation rules)
   - Pipeline import options (sources, date ranges)
   - Artifact validation options (schema version, validation level)
6. Display import results with:
   - Success/error summaries
   - Detailed logs or messages
   - Record counts and statistics
7. Implement proper loading states during import operations.
8. Add error handling for failed imports or validations.
9. Add the Import Tools to the main navigation (admin section).
10. Ensure responsive design for all screen sizes.

## Constraints
- Maintain existing URL structure and routing.
- Ensure accessibility of all UI elements and forms.
- Use the Catppuccin Mocha theme palette for styling.
- Optimize for handling large file uploads.
- Ensure dark mode compatibility.
- Follow established component patterns from TASK.web.v1.33.
- Implement proper security measures for file uploads.
- Handle potentially long-running operations gracefully.

## Tests
- Verify each import method correctly uses its respective hook.
- Test file uploads with various file types and sizes.
- Confirm configuration options work correctly for each import method.
- Test validation feedback and error handling.
- Verify import results display correctly.
- Test with mock successful and failed imports.
- Test responsive behavior on different screen sizes.
- Verify accessibility using browser dev tools.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
# Install file upload component if needed
pnpm --filter controlpanel add react-dropzone
# Start development server
pnpm --filter controlpanel dev
# Open browser to view the import tools page
open http://localhost:3000/import
# Run tests if available
pnpm --filter controlpanel test src/app/import
```

## Completion Criteria
- The Import Tools page successfully implements all three import hooks.
- File upload components work correctly with proper validation.
- Configuration options for each import method function properly.
- Import results are displayed clearly with appropriate feedback.
- Loading and error states provide appropriate user feedback.
- Long-running operations are handled gracefully.
- The page is responsive and accessible across devices.
- The Import Tools page is accessible from the main navigation.
- All tests pass successfully.

## ✅ Task Completed

**Changes made**
- Enhanced the existing Import Tools page to fully utilize all features of the import hooks
- Added support for import mode selection (append, replace, merge) in the Pipeline Import section
- Added date range filtering options to the Pipeline Import section
- Added a checkbox to enable/disable polling for long-running imports
- Added UI elements to display polling status with attempt count
- Updated the form to disable buttons during polling
- Added processing status indicators for better user feedback
- Ensured all form fields are properly reset when the Reset button is clicked
- Fixed ESLint errors by properly using the ImportMode enum

**Outcomes**
- The Import Tools page now provides a comprehensive interface for all import methods
- Users have more control over how imports are processed with additional configuration options
- Long-running operations are handled gracefully with status updates and polling
- The UI provides clear feedback during all stages of the import process
- The page follows established design patterns and is responsive across all screen sizes
- All three import methods (CSV, Pipeline, Artifact Validation) are fully functional
- The implementation is type-safe and follows best practices