## Persona
You are the Frontend Integration Engineer. Your role is to implement a React hook `usePollingForecast` that polls the `/api/forecast/deltas` endpoint at a configurable interval, enabling live updates of market volatility data in the `gpu-scoring-tool` controlpanel application.

## Title
Implement usePollingForecast Hook for Live Forecast Updates

## Purpose
Provide a reusable, type-safe hook to fetch forecast deltas on a recurring schedule, keeping the UI updated with the latest price-change metrics without manual refresh.

## Requirements
1. Create a new file `apps/controlpanel/src/hooks/usePollingForecast.ts`.
2. Import `ApiClient` and the `GpuDelta` alias type (or `ForecastDeltaDTO`) from `@repo/client` and any necessary types.
3. Use `react-query`'s `useQuery` with:
   - Query key `['forecast-deltas', params]`.
   - Fetch function calling `ApiClient.getForecastDeltas(params)` or the standalone `getForecastDeltas(params)` function.
   - `refetchInterval` option, defaulting to 60_000 ms (1 minute), and overridable via hook arguments.
4. Accept optional hook parameters object for `model`, `region`, `limit`, and `intervalMs`.
5. Return `{ data, error, isLoading, isError, isFetching, refetch }` from the hook.
6. Document default interval and parameter usage in JSDoc comments above the hook.

## Constraints
- Use only React Query's built-in polling; do not add external timers.
- Default polling interval should balance freshness and API load (no less than 30 seconds).
- Import from `@repo/client`; do not import APIs directly from generated code.

## Tests
- Create `apps/controlpanel/src/hooks/__tests__/usePollingForecast.test.ts` with `@testing-library/react-hooks`:
  - Mock `getForecastDeltas` or `ApiClient.getForecastDeltas` to return sample delta data and assert `data` updates on each refetch.
  - Use `react-query` testing utilities to spoof timers (`jest.useFakeTimers()`) and advance time by `intervalMs` to verify automated polling.
  - Simulate error response and assert `isError === true`.
- Verify that the hook respects the `intervalMs` parameter when provided.

## DX Runbook
```bash
# In the controlpanel directory:
pnpm install --filter controlpanel
pnpm --filter controlpanel dev

# In a hook test environment:
# Run tests for polling behavior
pnpm --filter controlpanel test apps/controlpanel/src/hooks/usePollingForecast.ts
```

## Completion Criteria
- `apps/controlpanel/src/hooks/usePollingForecast.ts` exists and exports the `usePollingForecast` hook.
- Automated tests cover polling interval, data updates, and error handling.
- Hook returns expected properties (`data`, `isLoading`, `isError`, `isFetching`, `refetch`).

## ✅ Task Completed
**Changes made**
- Created `apps/controlpanel/src/hooks/usePollingForecast.ts` implementing the hook with React Query's polling capabilities
- Implemented the hook to accept parameters for model, region, limit, and intervalMs
- Set default polling interval to 60000ms (1 minute)
- Added comprehensive JSDoc comments with usage examples
- Created `apps/controlpanel/src/hooks/__tests__/usePollingForecast.test.ts` with tests for:
  - Query key formation
  - API function parameter passing
  - Default values
  - Custom and default refetchInterval
  - Return structure
  - Error handling
  - isFetching state

**Outcomes**
- All tests pass successfully
- The hook provides a reusable way to fetch forecast deltas with automatic polling
- The implementation follows the project's patterns and best practices
- The hook is ready to be used in components that need live updates of forecast data