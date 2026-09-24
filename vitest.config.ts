// ABOUTME: Runs the TypeScript contract tests for the catalog, routes, and views.
// ABOUTME: Browser acceptance lives in tests/e2e and runs through Playwright.

import { getViteConfig } from 'astro/config';
import type { ViteUserConfig } from 'vitest/config';

// The Astro Vite configuration lets the tests read the authored Markdown lessons.
// Vitest 5 does not add its `test` field to the Vite config type, so the cast is needed.
export default getViteConfig({
  test: {
    include: ['tests/web/**/*.test.ts'],
    environment: 'node',
  },
} as ViteUserConfig);
