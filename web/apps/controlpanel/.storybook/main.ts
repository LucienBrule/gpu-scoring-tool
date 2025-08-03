import type { StorybookConfig } from '@storybook/react-vite';
import path from 'path';

const config: StorybookConfig = {
  "stories": [
    "../src/components/**/*.stories.@(js|jsx|ts|tsx)",
    "../src/hooks/**/*.stories.@(js|jsx|ts|tsx)"
  ],
  "addons": [
    '@storybook/addon-essentials',
    '@storybook/addon-docs'
  ],
  "framework": {
    "name": '@storybook/react-vite',
    "options": {}
  },
  "viteFinal": async (config) => {
    // Add support for Turborepo workspace packages
    if (config.resolve) {
      config.resolve.alias = {
        ...config.resolve.alias,
        '@repo/ui': path.resolve(__dirname, '../../../packages/ui/src'),
        '@repo/client': path.resolve(__dirname, '../../../packages/client/src'),
        '@repo/client-generated': path.resolve(__dirname, '../../../generated/client-generated/src'),
        '@': path.resolve(__dirname, '../src')
      };
    }
    return config;
  }
};
export default config;