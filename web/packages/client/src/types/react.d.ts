declare module 'react' {
  export function useMemo<T>(factory: () => T, deps: ReadonlyArray<any>): T;
  // Add other React exports as needed
}