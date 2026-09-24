// ABOUTME: Checks the discovery files, the routing manifest, and the structured data.
// ABOUTME: The inventory is the one source for sitemap, manifest, and canonical links.

import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { contentPaths } from '../../src/lib/content-routes';
import { lessonViews } from '../../src/lib/lessons';
import { entryView } from '../../src/lib/entry-view';
import {
  articleNode,
  breadcrumbNode,
  datasetNode,
  jsonLdScript,
  metaDescription,
  structuredData,
  webPageNode,
} from '../../src/lib/metadata';
import {
  ORIGIN,
  canonicalUrl,
  entryPath,
  htmlArtifactPath,
  markdownPath,
  lessonPath,
  routeInventory,
} from '../../src/lib/routes';
import { assertNoReservedRoutes, serializeManifest } from '../../scripts/site-publication';
import { publicationInventory } from '../../scripts/routing-manifest-route';
import { sitemapXml } from '../../src/pages/sitemap.xml';
import { ROBOTS_TXT } from '../../src/pages/robots.txt';
import { llmsTxt } from '../../src/pages/llms.txt';

const catalog = loadCatalog();
const paths = await contentPaths();
const inventory = routeInventory(catalog, paths);
const routes = Object.keys(inventory.routes);

describe('sitemap', () => {
  const xml = sitemapXml(routes);
  const locations = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]!);

  it('lists the canonical HTML pages of the build and nothing else', () => {
    expect(locations).toEqual(routes.map((path) => canonicalUrl(path)));
    expect(locations).toHaveLength(1 + catalog.approaches.length + new Set(catalog.approaches.map((entry) => entry.company_id)).size + paths.length);
  });

  it('holds no export, no 404, and no filtered directory URL', () => {
    for (const location of locations) {
      expect(location.startsWith(`${ORIGIN}/`)).toBe(true);
      expect(location).not.toMatch(/\.(md|json|xml|txt|html)$/);
      expect(location).not.toContain('404');
      expect(location).not.toContain('?');
      expect(location).not.toContain('#');
    }
  });

  it('states no modification date, because no page records one', () => {
    expect(xml).not.toContain('lastmod');
  });

  it('escapes the five XML characters in a location', () => {
    expect(sitemapXml(['/a&b'])).toContain(`<loc>${ORIGIN}/a&amp;b</loc>`);
  });
});

describe('robots.txt', () => {
  it('allows crawling and keeps the content signals', () => {
    expect(ROBOTS_TXT).toContain('User-agent: *\nAllow: /');
    expect(ROBOTS_TXT.match(/Content-Signal: search=yes, ai-input=yes, ai-train=yes/g)).toHaveLength(
      2,
    );
    expect(ROBOTS_TXT).toContain('User-agent: OAI-SearchBot');
    expect(ROBOTS_TXT).toContain('User-agent: Claude-SearchBot');
    expect(ROBOTS_TXT).toContain(`Sitemap: ${ORIGIN}/sitemap.xml`);
  });

  it('names the sitemap once and ends with a newline', () => {
    expect(ROBOTS_TXT.match(/^Sitemap: /gm)).toHaveLength(1);
    expect(ROBOTS_TXT.endsWith('\n')).toBe(true);
  });
});

describe('llms.txt', () => {
  const lessonTitles = new Map(lessonViews().map((lesson) => [lessonPath(lesson.slug), lesson.title]));
  const text = llmsTxt(paths, lessonTitles);

  it('keeps the data interfaces it has always named', () => {
    for (const target of ['/agents/index.json', '/data-guide.md', '/agents.json', '/index.md']) {
      expect(text).toContain(`](${ORIGIN}${target})`);
    }
  });

  it('links the Markdown of every guide and lesson', () => {
    for (const path of paths) expect(text).toContain(`](${ORIGIN}${markdownPath(path)})`);
    for (const lesson of lessonViews()) {
      expect(text).toContain(`- [${lesson.title}](${ORIGIN}${markdownPath(lessonPath(lesson.slug))})`);
    }
  });

  it('tells the reader to keep the qualifications with the claims', () => {
    expect(text).toContain('Preserve claim qualifications, dates, confidence');
    expect(text).toContain('company-reported metrics are not independent verification.');
  });
});

describe('routing manifest', () => {
  it('names the physical artifacts of every canonical route', async () => {
    const built = await publicationInventory();
    expect(built.schema_version).toBe(1);
    expect(Object.keys(built.routes)).toEqual(routes);
    for (const [path, artifacts] of Object.entries(built.routes)) {
      expect(artifacts.html).toBe(htmlArtifactPath(path));
      expect(artifacts.markdown).toBe(markdownPath(path));
    }
    expect(built.routes['/agents/block-builderbot']).toEqual({
      html: '/agents/block-builderbot.html',
      markdown: '/agents/block-builderbot.md',
    });
  });

  it('writes the same bytes on two builds', async () => {
    const first = serializeManifest(await publicationInventory());
    const second = serializeManifest(await publicationInventory());
    expect(first).toBe(second);
    expect(first.endsWith('}\n')).toBe(true);
  });

  it('matches the manifest the repository commits', async () => {
    const committed = readFileSync(new URL('../../routing-manifest.json', import.meta.url), 'utf8');
    expect(serializeManifest(await publicationInventory())).toBe(committed);
  });

  it('rejects a route that uses a reserved name', () => {
    expect(() =>
      assertNoReservedRoutes({
        schema_version: 1,
        routes: { '/agents/index': { html: '/agents/index.html', markdown: '/agents/index.md' } },
      }),
    ).toThrow(/reserved name/);
  });
});

describe('structured data', () => {
  const entry = entryView(catalog, 'block-builderbot');
  const url = canonicalUrl(entry.path);
  const graph = structuredData([
    webPageNode({ url, name: entry.title, description: metaDescription(entry.summaryText) }),
    breadcrumbNode(url, [
      { name: 'Catalog', path: '/' },
      { name: entry.title, path: entry.path },
    ]),
  ]);

  it('describes only real visible pages of this site', () => {
    const script = jsonLdScript(graph);
    const parsed = JSON.parse(script) as { '@graph': Array<Record<string, unknown>> };
    const crumbs = parsed['@graph'].find((node) => node['@type'] === 'BreadcrumbList');
    const items = (crumbs as { itemListElement: Array<{ item: string }> }).itemListElement;
    expect(items.map((item) => item.item)).toEqual([canonicalUrl('/'), url]);
    for (const item of items) {
      expect(routes).toContain(item.item.slice(ORIGIN.length));
    }
  });

  it('escapes a character that could close the script element', () => {
    const script = jsonLdScript(
      structuredData([webPageNode({ url, name: '</script><b>x', description: 'y' })]),
    );
    expect(script).not.toContain('<');
    expect(JSON.parse(script)).toEqual(
      structuredData([webPageNode({ url, name: '</script><b>x', description: 'y' })]),
    );
  });

  it('offers the catalog as one dataset with its real downloads', () => {
    const dataset = datasetNode({ description: 'x', dateModified: '2026-09-09' }) as {
      distribution: Array<{ contentUrl: string }>;
      dateModified: string;
    };
    expect(dataset.distribution.map((item) => item.contentUrl)).toEqual([
      `${ORIGIN}/agents.json`,
      `${ORIGIN}/agents/index.json`,
      `${ORIGIN}/data-guide.md`,
    ]);
    expect(dataset.dateModified).toBe('2026-09-09');
    expect(datasetNode({ description: 'x' })).not.toHaveProperty('dateModified');
  });

  it('describes a lesson as an article of this website', () => {
    const lesson = lessonViews()[0]!;
    const article = articleNode({
      url: canonicalUrl(lesson.path),
      name: lesson.title,
      headline: lesson.title,
      description: lesson.description,
      datePublished: lesson.publishedAt,
    }) as Record<string, unknown>;
    expect(article['@type']).toBe('Article');
    expect(article.headline).toBe(lesson.title);
    expect(article.datePublished).toBe(lesson.publishedAt);
    expect(article.inLanguage).toBe('en');
  });

  it('canonical links use the production origin and a clean path', () => {
    for (const approach of catalog.approaches) {
      expect(canonicalUrl(entryPath(approach.id))).toBe(
        `https://internal-agents.com/agents/${approach.id}`,
      );
    }
  });
});
