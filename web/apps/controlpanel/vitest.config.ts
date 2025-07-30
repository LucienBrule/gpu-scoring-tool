import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        environment: 'jsdom',
        globals: true,
        setupFiles: ['./vitest.setup.ts'],
        include: ['src/**/*.{test,spec}.{ts,tsx}'], // or wherever your unit tests live
        exclude: ['tests/integration/**', 'node_modules', 'dist'],
    },
});