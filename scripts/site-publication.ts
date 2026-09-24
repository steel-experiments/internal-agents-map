// ABOUTME: Writes the routing manifest and checks the built artifacts after a build.
// ABOUTME: The manifest is the middleware input, so it must match the files in dist/.

import { existsSync } from 'node:fs';
import { readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import type { AstroIntegration } from 'astro';
import { RESERVED_APPROACH_IDS, type RouteInventory } from '../src/lib/routes.ts';

/** The file the middleware imports. It lives at the repository root, not in dist/. */
export const ROUTING_MANIFEST_FILE = 'routing-manifest.json';

/**
 * The route the build uses to serialize the inventory.
 * The inventory reads the lesson content, which only the build pipeline can load,
 * so the manifest is produced as a route and then moved out of the output.
 */
const MANIFEST_ROUTE = '/routing-manifest.json';

/**
 * Serialize the manifest.
 * The key order comes from the inventory, so two builds write the same bytes.
 */
export function serializeManifest(inventory: RouteInventory): string {
  return `${JSON.stringify(inventory, null, 2)}\n`;
}

/** Reject a manifest that is not the shape the middleware reads. */
export function parseManifest(text: string): RouteInventory {
  const value = JSON.parse(text) as RouteInventory;
  if (value.schema_version !== 1 || typeof value.routes !== 'object') {
    throw new Error(`${ROUTING_MANIFEST_FILE} is not a version 1 route inventory.`);
  }
  return value;
}

/** Reject a route whose last segment is a name that another file already uses. */
export function assertNoReservedRoutes(inventory: RouteInventory): void {
  for (const route of Object.keys(inventory.routes)) {
    const name = route.slice(route.lastIndexOf('/') + 1);
    if (RESERVED_APPROACH_IDS.has(name)) {
      throw new Error(`Route "${route}" uses the reserved name "${name}".`);
    }
  }
}

/** Fail the build when a declared route has no HTML or no Markdown file in dist/. */
export function assertArtifactsExist(inventory: RouteInventory, outDir: string): void {
  const missing: string[] = [];
  for (const [route, artifacts] of Object.entries(inventory.routes)) {
    for (const artifact of [artifacts.html, artifacts.markdown]) {
      if (!existsSync(path.join(outDir, artifact))) missing.push(`${route} -> ${artifact}`);
    }
  }
  if (missing.length > 0) {
    throw new Error(`The build did not write every declared artifact:\n  ${missing.join('\n  ')}`);
  }
}

/**
 * Write the routing manifest and check the build output against it.
 * The middleware bundles the manifest, so it reads the file that this hook writes.
 */
export function publicationIntegration(): AstroIntegration {
  let root = process.cwd();
  return {
    name: 'internal-agents-publication',
    hooks: {
      'astro:config:setup': ({ injectRoute }) => {
        injectRoute({
          pattern: MANIFEST_ROUTE,
          entrypoint: './scripts/routing-manifest-route.ts',
        });
      },
      'astro:config:done': ({ config }) => {
        root = fileURLToPath(config.root);
      },
      'astro:build:done': async ({ dir, logger }) => {
        const outDir = fileURLToPath(dir);
        const built = path.join(outDir, MANIFEST_ROUTE);
        const text = await readFile(built, 'utf8');
        const inventory = parseManifest(text);
        assertNoReservedRoutes(inventory);
        assertArtifactsExist(inventory, outDir);
        await writeFile(path.join(root, ROUTING_MANIFEST_FILE), text, 'utf8');
        // The manifest is a build input for the middleware, not published content.
        await rm(built);
        const count = Object.keys(inventory.routes).length;
        logger.info(`wrote ${ROUTING_MANIFEST_FILE} with ${count} routes`);
      },
    },
  };
}
