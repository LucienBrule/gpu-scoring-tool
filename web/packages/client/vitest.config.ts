import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        environment: 'jsdom',
        globals: true,
        include: ['src/**/*.{test,spec}.{ts,tsx}'], // Include all test files in the src directory
        exclude: ['node_modules', 'dist'],
    },
});