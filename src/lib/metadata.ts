// ABOUTME: Holds the shared publisher identity, social tags, and structured data.
// ABOUTME: Every page describes itself through these helpers, so the identity matches.

import { ORIGIN, canonicalUrl } from './routes';
import { shorten } from './text';

export const SITE_NAME = 'Internal Agents Map';
export const SITE_DESCRIPTION =
  'A source-backed catalog of AI systems organizations build for their own teams.';
export const CONTENT_LICENSE = 'https://creativecommons.org/licenses/by-sa/4.0/';
export const OG_IMAGE = `${ORIGIN}/og.png`;
export const OG_IMAGE_ALT = `${SITE_NAME}: a source-backed catalog of internal AI agents`;
/** Where a reader suggests an addition or a correction to the catalog. */
export const CONTRIBUTE_URL =
  'https://github.com/steel-experiments/internal-agents-map/issues/new?title=Catalog+suggestion';

/** The organization that publishes the catalog. */
export const PUBLISHER = {
  '@type': 'Organization',
  '@id': 'https://steel.dev/#organization',
  name: 'Steel',
  url: 'https://steel.dev/',
  description: 'Open-source browser infrastructure for AI agents.',
  sameAs: ['https://github.com/steel-dev', 'https://x.com/steeldotdev'],
} as const;

export const WEBSITE_ID = `${ORIGIN}/#website`;

export type JsonLdNode = Record<string, unknown>;

/** The website node that every page belongs to. */
export function websiteNode(): JsonLdNode {
  return {
    '@type': 'WebSite',
    '@id': WEBSITE_ID,
    name: SITE_NAME,
    url: `${ORIGIN}/`,
    description: SITE_DESCRIPTION,
    publisher: { '@id': PUBLISHER['@id'] },
    license: CONTENT_LICENSE,
  };
}

/** Describe one page of the website. */
export function webPageNode(options: {
  url: string;
  name: string;
  description: string;
  dateModified?: string | null;
}): JsonLdNode {
  const node: JsonLdNode = {
    '@type': 'WebPage',
    '@id': options.url,
    url: options.url,
    name: options.name,
    description: options.description,
    isPartOf: { '@id': WEBSITE_ID },
    publisher: { '@id': PUBLISHER['@id'] },
  };
  if (options.dateModified) node.dateModified = options.dateModified;
  return node;
}

/**
 * Describe the whole catalog as one dataset with its two downloads.
 * Only the directory page carries this node: there is one dataset.
 */
export function datasetNode(options: { description: string; dateModified?: string | null }): JsonLdNode {
  const node: JsonLdNode = {
    '@type': 'Dataset',
    '@id': `${ORIGIN}/#dataset`,
    name: SITE_NAME,
    description: options.description,
    url: `${ORIGIN}/`,
    license: CONTENT_LICENSE,
    isAccessibleForFree: true,
    creator: { '@id': PUBLISHER['@id'] },
    publisher: { '@id': PUBLISHER['@id'] },
    distribution: [
      {
        '@type': 'DataDownload',
        name: 'Complete dataset',
        encodingFormat: 'application/json',
        contentUrl: `${ORIGIN}/agents.json`,
      },
      {
        '@type': 'DataDownload',
        name: 'Compact catalog index',
        encodingFormat: 'application/json',
        contentUrl: `${ORIGIN}/agents/index.json`,
      },
      {
        '@type': 'DataDownload',
        name: 'Data and evidence guide',
        encodingFormat: 'text/markdown',
        contentUrl: `${ORIGIN}/data-guide.md`,
      },
    ],
  };
  if (options.dateModified) node.dateModified = options.dateModified;
  return node;
}

/** Describe one lesson as an article of this website. */
export function articleNode(options: {
  url: string;
  name: string;
  headline: string;
  description: string;
  datePublished?: string | null;
  dateModified?: string | null;
}): JsonLdNode {
  const node = webPageNode({
    url: options.url,
    name: options.name,
    description: options.description,
    dateModified: options.dateModified,
  });
  node['@type'] = 'Article';
  node.headline = options.headline;
  node.mainEntityOfPage = options.url;
  node.author = { '@id': PUBLISHER['@id'] };
  node.inLanguage = 'en';
  if (options.datePublished) node.datePublished = options.datePublished;
  return node;
}

/** Describe the path a reader follows from the directory to this page. */
export function breadcrumbNode(url: string, items: ReadonlyArray<{ name: string; path: string }>): JsonLdNode {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${url}#breadcrumb`,
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: canonicalUrl(item.path),
    })),
  };
}

/** Wrap page nodes in the graph that carries the shared publisher identity. */
export function structuredData(nodes: readonly JsonLdNode[]): JsonLdNode {
  return { '@context': 'https://schema.org', '@graph': [PUBLISHER, websiteNode(), ...nodes] };
}

/**
 * Serialize structured data for a script element.
 * `<` becomes an escape sequence, so catalog text can never close the element.
 */
export function jsonLdScript(data: unknown): string {
  return JSON.stringify(data).replace(/</g, '\\u003c');
}

/** Shorten catalog prose into a page description. */
export function metaDescription(text: string, limit = 155): string {
  return shorten(text, limit);
}
