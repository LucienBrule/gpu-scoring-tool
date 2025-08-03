## Persona
You are the Frontend UI Engineer. Your role is to create an ML Classifier Playground page that allows users to test the GPU classification model with text input and view live results using the `useGpuClassification` hook.

## Title
Create ML Classifier Playground with Live Results

## Purpose
Develop an interactive ML Classifier Playground that enables users to input text descriptions and receive real-time feedback on whether the text refers to a GPU. This feature will showcase the machine learning capabilities of the system, help users understand classification decisions, and provide a valuable tool for testing and improving the classification model.

## Requirements
1. Create a new ML Playground page component in `apps/controlpanel/src/app/ml-playground/page.tsx` (or equivalent path).
2. Import and implement the `useGpuClassification` hook created in TASK.web.v1.15.
3. Design an intuitive interface with:
   - A text input area for entering GPU descriptions
   - A prominent "Classify" button
   - Real-time classification results display
   - Confidence score visualization
   - Classification history section
4. Implement real-time or on-submit classification:
   - Display "Is GPU" or "Not GPU" result
   - Show confidence percentage
   - Highlight key terms that influenced the decision
5. Add options to adjust classification parameters:
   - Confidence threshold slider
   - Model version selector (if multiple versions exist)
6. Create a history section that saves recent classifications.
7. Implement proper loading states during classification.
8. Add error handling for failed API requests.
9. Add the ML Playground to the main navigation.
10. Ensure responsive design for all screen sizes.

## Constraints
- Maintain existing URL structure and routing.
- Ensure accessibility of all UI elements.
- Use the Catppuccin Mocha theme palette for styling.
- Optimize for quick response times and smooth user experience.
- Ensure dark mode compatibility.
- Follow established component patterns from TASK.web.v1.33.
- Limit classification requests to prevent API abuse (e.g., debounce inputs).

## Tests
- Verify the page correctly uses the `useGpuClassification` hook.
- Test with various text inputs (known GPUs, non-GPUs, ambiguous cases).
- Confirm confidence threshold adjustment works correctly.
- Test classification history functionality.
- Verify loading states display appropriately during classification.
- Confirm error states render correctly when API requests fail.
- Test responsive behavior on different screen sizes.
- Verify accessibility using browser dev tools.

## DX Runbook
```bash
# From project root:
pnpm --filter controlpanel install
# Start development server
pnpm --filter controlpanel dev
# Open browser to view the ML Playground
open http://localhost:3000/ml-playground
# Run tests if available
pnpm --filter controlpanel test src/app/ml-playground
```

## Completion Criteria
- The ML Playground successfully uses the `useGpuClassification` hook.
- Text input and classification works correctly.
- Classification results are displayed clearly with confidence scores.
- Parameter adjustments (threshold, model version) function properly.
- Classification history is maintained during the session.
- Loading and error states provide appropriate feedback to users.
- The page is responsive and accessible across devices.
- The ML Playground is accessible from the main navigation.
- All tests pass successfully.


## ✅ Task Completed
**Changes made**
- Created a new ML Playground page component in `apps/controlpanel/src/app/ml-playground/page.tsx`
- Implemented the page using the `useGpuClassification` hook
- Designed an intuitive interface with:
  - Text input area for entering GPU descriptions
  - Classification button and real-time classification option
  - Clear results display with confidence visualization
  - Confidence threshold slider
  - Classification history section that saves recent results
- Added proper loading states and error handling
- Implemented debounced real-time classification to prevent API abuse
- Added the ML Playground to the main navigation in the Navbar component
- Integrated the Sparkline component for visual trend representation
- Ensured responsive design with a grid layout that adapts to different screen sizes
- Fixed ESLint errors related to unescaped entities

**Outcomes**
- Users can now test the GPU classification model with any text input
- The interface provides clear feedback on classification results with confidence scores
- The confidence threshold can be adjusted to see how it affects classification decisions
- Classification history is maintained during the session for easy comparison
- The page is fully responsive and works well on all screen sizes
- The ML Playground is accessible from the main navigation
- The implementation follows the established component patterns and styling guidelines