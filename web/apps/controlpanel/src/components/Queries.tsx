import {QueryClient} from "@tanstack/react-query";

let queryClientSingleton: QueryClient | undefined = undefined;
export const getQueryClient = () => {
    console.log('getQueryClient');
    if (typeof window === 'undefined') {
        // Server-side - always create a new QueryClient
        return new QueryClient({
            defaultOptions: {
                queries: {
                    // Don't retry on the server
                    retry: false,
                    // Don't refetch on the server
                    refetchOnWindowFocus: false,
                    // Don't refetch on mount
                    refetchOnMount: false,
                    // Important for SSR
                    staleTime: Infinity,
                },
            },
        });
    }

    // Client-side - create a singleton QueryClient
    if (!queryClientSingleton) {
        queryClientSingleton = new QueryClient({
            defaultOptions: {
                queries: {
                    // Default stale time to reduce unnecessary refetches
                    staleTime: 60 * 1000, // 1 minute
                    // Default cache time
                    gcTime: 5 * 60 * 1000, // 5 minutes
                },
            },
        });
    }

    return queryClientSingleton;
};