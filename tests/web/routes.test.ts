// ABOUTME: Checks the canonical paths, the reserved names, and the publication inventory.
// ABOUTME: The inventory shape is the contract that later steps write to disk.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import {
  assertPublishableId,
  assertUniquePaths,
  canonicalUrl,
  entryJsonPath,
  entryPath,
  guidePath,
  homePath,
  htmlArtifactPath,
  markdownPath,
  lessonPath,
  lessonsIndexPath,
  routeInventory,
} from '../../src/lib/routes';

describe('canonical paths', () => {
  it('builds the paths of the published pages', () => {
    expect(homePath()).toBe('/');
    expect(entryPath('block-builderbot')).toBe('/agents/block-builderbot');
    expect(lessonsIndexPath()).toBe('/lessons');
    expect(lessonPath('stop-a-run')).toBe('/lessons/stop-a-run');
    expect(guidePath('definitions')).toBe('/definitions');
  });

  it('maps a canonical path to its artifacts', () => {
    expect(htmlArtifactPath('/')).toBe('/index.html');
    expect(markdownPath('/')).toBe('/index.md');
    expect(htmlArtifactPath('/agents/block-builderbot')).toBe('/agents/block-builderbot.html');
    expect(markdownPath('/agents/block-builderbot')).toBe('/agents/block-builderbot.md');
    expect(entryJsonPath('block-builderbot')).toBe('/agents/block-builderbot.json');
  });

  it('builds absolute URLs on the production origin', () => {
    expect(canonicalUrl('/')).toBe('https://internal-agents.com/');
    expect(canonicalUrl('/agents/uber-ureview')).toBe('https://internal-agents.com/agents/uber-ureview');
  });
});

describe('route guards', () => {
  it('refuses a reserved name as an approach identifier', () => {
    expect(() => assertPublishableId('index')).toThrow(/reserved route name/);
  });

  it('refuses an identifier that is not a slug', () => {
    expect(() => assertPublishableId('Block Builderbot')).toThrow(/not a lower-case slug/);
    expect(() => assertPublishableId('../secrets')).toThrow(/not a lower-case slug/);
  });

  it('refuses two pages that claim one path', () => {
    expect(() => assertUniquePaths(['/a', '/b', '/a'])).toThrow(/Route "\/a" is claimed by more than one page/);
  });

  it('accepts every identifier in the catalog', () => {
    for (const approach of loadCatalog().approaches) {
      expect(() => assertPublishableId(approach.id)).not.toThrow();
    }
  });
});

describe('the publication inventory', () => {
  const catalog = loadCatalog();
  const inventory = routeInventory(catalog);

  it('uses the inventory shape the routing manifest reads', () => {
    expect(inventory.schema_version).toBe(1);
    expect(inventory.routes['/']).toEqual({ html: '/index.html', markdown: '/index.md' });
    expect(inventory.routes['/agents/block-builderbot']).toEqual({
      html: '/agents/block-builderbot.html',
      markdown: '/agents/block-builderbot.md',
    });
  });

  it('holds the directory and one route for every approach', () => {
    const paths = Object.keys(inventory.routes);
    expect(paths.length).toBe(catalog.approaches.length + new Set(catalog.approaches.map((entry) => entry.company_id)).size + 1);
    for (const approach of catalog.approaches) {
      expect(paths).toContain(entryPath(approach.id));
    }
  });

  it('adds the pages that later steps publish', () => {
    const extended = routeInventory(catalog, [guidePath('definitions'), lessonPath('stop-a-run')]);
    expect(Object.keys(extended.routes).length).toBe(catalog.approaches.length + new Set(catalog.approaches.map((entry) => entry.company_id)).size + 3);
    expect(extended.routes['/lessons/stop-a-run']).toEqual({
      html: '/lessons/stop-a-run.html',
      markdown: '/lessons/stop-a-run.md',
    });
  });

  it('refuses an extra page that repeats an entry path', () => {
    expect(() => routeInventory(catalog, [entryPath('block-builderbot')])).toThrow(
      /claimed by more than one page/,
    );
  });
});
