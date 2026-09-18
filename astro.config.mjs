// ABOUTME: Configures the static build, the clean URL policy, and the site origin.
// ABOUTME: There is no server adapter: every page is a file in dist/.

import { defineConfig } from 'astro/config';
import { annotationIntegration, devFreshnessIntegration } from './scripts/site-annotation.ts';
import { publicationIntegration } from './scripts/site-publication.ts';

export default defineConfig({
  site: 'https://internal-agents.com',
  output: 'static',
  // The dev toolbar overlaps the floating search bar at the foot of the window.
  devToolbar: { enabled: false },
  trailingSlash: 'never',
  build: {
    // One file per page, so /agents/<id> is served from agents/<id>.html.
    format: 'file',
  },
  // ENABLE_ANNOTATIONS=1 opts the dev server into annotations; builds never include it.
  // Writes routing-manifest.json and checks dist/ against the declared routes.
  integrations: [devFreshnessIntegration(), annotationIntegration(), publicationIntegration()],
});
