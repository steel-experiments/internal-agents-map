// ABOUTME: Opts the development server into Agentation with ENABLE_ANNOTATIONS=1.
// ABOUTME: It injects nothing for a build, so React and the toolbar stay out of dist/.

import type { AstroIntegration } from 'astro';

/** The module the injected script loads. Astro resolves it from the project root. */
const ENTRY = 'src/scripts/annotate.ts';

/**
 * Keep the development server from serving a page it prepared earlier.
 *
 * The dev server writes the site's styles into every page it renders, so a
 * page held in the prefetch cache carries the styles as they were when it was
 * fetched. Navigating to it then restores that older copy, and a change made
 * since appears to have been lost until the page is reloaded. The built site
 * links one stylesheet instead, so this belongs to development alone.
 */
export function devFreshnessIntegration(): AstroIntegration {
  return {
    name: 'internal-agents-dev-freshness',
    hooks: {
      'astro:config:setup': ({ command, updateConfig }) => {
        if (command !== 'dev') return;
        updateConfig({ prefetch: false });
      },
    },
  };
}

/**
 * Register the annotation toolbar only for explicitly opted-in `astro dev` runs.
 * Injecting only under the dev command keeps the toolbar out of the build graph,
 * so no orphan chunk of it reaches the output the publication check guards.
 */
export function annotationIntegration(): AstroIntegration {
  return {
    name: 'internal-agents-annotation',
    hooks: {
      'astro:config:setup': ({ command, injectScript }) => {
        if (command !== 'dev' || process.env.ENABLE_ANNOTATIONS !== '1') return;
        injectScript('page', `import { startAnnotating } from '/${ENTRY}';\nstartAnnotating();`);
      },
    },
  };
}
