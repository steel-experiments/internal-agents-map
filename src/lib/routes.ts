// ABOUTME: Holds the canonical paths of the website and the publication inventory.
// ABOUTME: Page links, exports, and the routing manifest all read these helpers.

import { sortedApproaches, type Catalog } from './catalog';

/** The production origin. Canonical links and structured data use it. */
export const ORIGIN = 'https://internal-agents.com';

/** The version of the inventory shape that later build steps write to disk. */
export const ROUTE_INVENTORY_SCHEMA_VERSION = 1;

/**
 * Names that an approach identifier must not take.
 * `index` would collide with the compact index export at `/agents/index.json`.
 */
export const RESERVED_APPROACH_IDS: ReadonlySet<string> = new Set(['index']);

const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export interface PublicationRoute {
  /** The canonical clean URL path. */
  readonly path: string;
  /** The physical HTML file the host serves for that path. */
  readonly html: string;
  /** The Markdown representation of the same page. */
  readonly markdown: string;
}

export interface RouteInventory {
  readonly schema_version: number;
  readonly routes: Record<string, { readonly html: string; readonly markdown: string }>;
}

/** The directory page. */
export function homePath(): string {
  return '/';
}

/** The page of one catalog implementation. */
export function entryPath(id: string): string {
  return `/agents/${id}`;
}

/** The stable page of one organization. */
export function organizationPath(id: string): string {
  if (!SLUG_PATTERN.test(id)) throw new Error(`Company id "${id}" is not a lower-case slug.`);
  return `/organizations/${id}`;
}

/** Publish only registry companies with catalog records. */
export function organizationPaths(catalog: Catalog): string[] {
  const ids = new Set(catalog.approaches.map((entry) => entry.company_id));
  for (const id of ids) {
    if (!catalog.companies.some((company) => company.id === id)) throw new Error(`Unknown company "${id}".`);
  }
  return catalog.companies.filter((company) => ids.has(company.id)).map((company) => organizationPath(company.id));
}

/** The lessons index. */
export function lessonsIndexPath(): string {
  return '/lessons';
}

/** One lesson. */
export function lessonPath(slug: string): string {
  return `/lessons/${slug}`;
}

/** One guide page, such as `definitions` or `methodology`. */
export function guidePath(name: string): string {
  return `/${name}`;
}

/** The physical HTML file behind a canonical path. */
export function htmlArtifactPath(path: string): string {
  return path === '/' ? '/index.html' : `${path}.html`;
}

/** The Markdown representation of a canonical path. */
export function markdownPath(path: string): string {
  return path === '/' ? '/index.md' : `${path}.md`;
}

/** The JSON record export of one implementation. */
export function entryJsonPath(id: string): string {
  return `/agents/${id}.json`;
}

/** The absolute URL of a canonical path. */
export function canonicalUrl(path: string): string {
  return ORIGIN + path;
}

/** Reject an identifier that cannot become a safe, unique entry path. */
export function assertPublishableId(id: string): void {
  if (!SLUG_PATTERN.test(id)) {
    throw new Error(`Approach id "${id}" is not a lower-case slug and cannot become a path.`);
  }
  if (RESERVED_APPROACH_IDS.has(id)) {
    throw new Error(`Approach id "${id}" is a reserved route name under /agents.`);
  }
}

/** Reject a publication set that would write two pages to one path. */
export function assertUniquePaths(paths: readonly string[]): void {
  const seen = new Set<string>();
  for (const path of paths) {
    if (seen.has(path)) throw new Error(`Route "${path}" is claimed by more than one page.`);
    seen.add(path);
  }
}

/** Describe one publishable page by its canonical path. */
export function publicationRoute(path: string): PublicationRoute {
  return { path, html: htmlArtifactPath(path), markdown: markdownPath(path) };
}

/**
 * List every publishable page of this build.
 * `extraPaths` carries the guides and lessons as later steps add them.
 */
export function publicationRoutes(catalog: Catalog, extraPaths: readonly string[] = []) {
  const entries = sortedApproaches(catalog).map((approach) => {
    assertPublishableId(approach.id);
    return entryPath(approach.id);
  });
  const paths = [homePath(), ...entries, ...organizationPaths(catalog), ...extraPaths];
  assertUniquePaths(paths);
  return paths.map(publicationRoute);
}

/** Build the inventory that the routing manifest and discovery files read. */
export function routeInventory(catalog: Catalog, extraPaths: readonly string[] = []): RouteInventory {
  const routes: Record<string, { html: string; markdown: string }> = {};
  for (const route of publicationRoutes(catalog, extraPaths)) {
    routes[route.path] = { html: route.html, markdown: route.markdown };
  }
  return { schema_version: ROUTE_INVENTORY_SCHEMA_VERSION, routes };
}
