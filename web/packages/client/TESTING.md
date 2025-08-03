# Testing the Client Package

## Current Status

The client package includes several hooks that wrap the auto-generated TanStack Query hooks to provide additional functionality. These hooks have been implemented and should work correctly in the application, but the tests are currently failing due to compatibility issues with the testing libraries.

## Issues Encountered

1. **React Hooks Testing**: React hooks can only be called inside React components, so testing them requires a library like `@testing-library/react-hooks` to render them in a React component context.

2. **Mocking TanStack Query**: The tests attempt to mock the `useQuery` hook from TanStack Query, but the mocking implementation is not correctly handling the way useQuery is being used in the hooks.

3. **Compatibility Issues**: There appears to be an incompatibility between the version of React being used (19.1.0) and the version of `@testing-library/react-hooks` (8.0.1). The error "ReactDOM.render is not a function" suggests that `@testing-library/react-hooks` is using an older API that's no longer available in React 19.

## Next Steps

1. **Update Testing Libraries**: Investigate if there's a newer version of `@testing-library/react-hooks` that's compatible with React 19, or if there's an alternative library that can be used.

2. **Simplify Mocking**: Simplify the mocking implementation to avoid complex interactions between mocks.

3. **Consider Integration Tests**: Instead of unit testing the hooks in isolation, consider writing integration tests that test the hooks in the context of a component that uses them.

4. **Manual Testing**: In the meantime, manually test the hooks in the application to ensure they're working correctly.

## Implemented Hooks

The following hooks have been implemented:

- `useHealthCheck`: Checks the health status of the backend API.
- `useListings`: Fetches GPU listings with pagination and date filtering.
- `useModels`: Fetches GPU models with filtering and sorting capabilities.

These hooks should work correctly in the application, but the tests are currently failing due to the issues described above.