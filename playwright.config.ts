// ABOUTME: Runs browser acceptance against the built site served by astro preview.
// ABOUTME: One project disables JavaScript, so pages must read without it.

import { defineConfig, devices } from '@playwright/test';
import { PREVIEW_URL } from './tests/e2e/preview';

export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: '**/*.spec.ts',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  reporter: process.env.CI ? 'line' : 'list',
  globalTimeout: 5 * 60_000,
  webServer: {
    command: 'node tests/e2e/serve.ts',
    url: PREVIEW_URL,
    reuseExistingServer: false,
    timeout: 30_000,
    gracefulShutdown: { signal: 'SIGTERM', timeout: 5_000 },
  },
  use: { baseURL: PREVIEW_URL },
  projects: [
    {
      name: 'desktop',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 900 } },
    },
    {
      name: 'mobile',
      use: { ...devices['Pixel 7'] },
    },
    {
      name: 'no-javascript',
      use: { ...devices['Desktop Chrome'], javaScriptEnabled: false },
    },
  ],
});
