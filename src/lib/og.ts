// ABOUTME: Derives the content of each link preview card from the catalog views.
// ABOUTME: Pure data: the renderer under src/og/ draws these inputs, the pages link to them.

import { createHash } from 'node:crypto';
import type { Catalog, CompanyLogo } from './catalog';
import type { CompanyView } from './companies';
import type { DirectoryCard } from './entry-view';
import { canonicalUrl } from './routes';
import { shorten } from './text';

/** Bump when the drawing changes, so link caches drop the old card. */
export const OG_TEMPLATE_VERSION = 2;
export const OG_WIDTH = 1200;
export const OG_HEIGHT = 630;
/** The summary length the card holds in four lines at its type size. */
export const OG_EXCERPT_LIMIT = 140;
/** The approach type and up to three work domains fit one row. */
export const OG_TAG_LIMIT = 4;
/** The home page card sits at the site root, where the site-wide preview tag points. */
export const OG_DEFAULT_PATH = '/og.png';

/** The vendored logo as the card draws it. `wide` marks a wordmark-shaped file. */
export interface OgLogo {
  readonly path: string;
  readonly width: number;
  readonly height: number;
  readonly sha256: string;
  readonly wide: boolean;
}

export interface OgEntryCard {
  readonly kind: 'entry';
  readonly company: string;
  readonly name: string;
  /** The company and the name as one line of text, such as `Stripe · Minions`. */
  readonly title: string;
  readonly excerpt: string;
  readonly tags: readonly string[];
  readonly logo: OgLogo | null;
  readonly monogram: string;
  readonly titleSize: number;
}

export interface OgOrganizationCard {
  readonly kind: 'organization';
  readonly company: string;
  readonly count: string;
  readonly names: readonly string[];
  readonly logo: OgLogo | null;
  readonly monogram: string;
  readonly titleSize: number;
}

export interface OgSectionCard {
  readonly kind: 'section';
  /** The kind of page, shown as the blue tag. The home page has none. */
  readonly eyebrow: string | null;
  readonly title: string;
  readonly description: string;
  /** The description cut to the length the card holds. */
  readonly excerpt: string;
  /** The publication date a lesson shows below its description. */
  readonly date: string | null;
  readonly titleSize: number;
  /** The company logos the front card shows, in the order the card places them. */
  readonly logos: readonly OgLogo[];
}

export type OgCard = OgEntryCard | OgOrganizationCard | OgSectionCard;

/** What a page puts in its head. */
export interface OgImage {
  readonly url: string;
  readonly alt: string;
}

/** A logo twice as wide as it is tall spells the name, so the card does not repeat it. */
export function isWide(width: number, height: number): boolean {
  return width / height >= 2;
}

export function ogLogo(logo: CompanyLogo | null): OgLogo | null {
  if (!logo) return null;
  return {
    path: logo.path,
    width: logo.width,
    height: logo.height,
    sha256: logo.sha256,
    wide: isWide(logo.width, logo.height),
  };
}

/** The title steps down as the company and the name grow. */
export function titleSize(text: string): number {
  if (text.length <= 30) return 64;
  if (text.length <= 44) return 56;
  return 48;
}

/** The card of one implementation, as the directory names it. */
export function entryCard(card: DirectoryCard): OgEntryCard {
  const tags = [card.approachTypeLabel, ...card.domains.map((domain) => domain.label)];
  return {
    kind: 'entry',
    company: card.company,
    name: card.agentName,
    title: card.title,
    excerpt: shorten(card.summary, OG_EXCERPT_LIMIT),
    tags: tags.slice(0, OG_TAG_LIMIT),
    logo: ogLogo(card.companyView.logo),
    monogram: card.companyView.monogram,
    titleSize: titleSize(card.title),
  };
}

/** "4 agents and 1 infrastructure entry in the catalog", from the two collections. */
export function organizationCount(agents: number, infrastructure: number): string {
  const parts: string[] = [];
  if (agents > 0) parts.push(`${agents} ${agents === 1 ? 'agent' : 'agents'}`);
  if (infrastructure > 0) {
    parts.push(`${infrastructure} infrastructure ${infrastructure === 1 ? 'entry' : 'entries'}`);
  }
  return `${parts.join(' and ')} in the catalog`;
}

/** The card of one organization: its mark, its count, and the names of its systems. */
export function organizationCard(
  company: CompanyView,
  cards: readonly DirectoryCard[],
): OgOrganizationCard {
  const agents = cards.filter((card) => card.catalogSection === 'agents').length;
  return {
    kind: 'organization',
    company: company.name,
    count: organizationCount(agents, cards.length - agents),
    names: cards.map((card) => card.agentName),
    logo: ogLogo(company.logo),
    monogram: company.monogram,
    titleSize: titleSize(company.name),
  };
}

/** A 32-bit seed from a text, so the same text always gives the same order. */
function seedOf(text: string): number {
  return createHash('sha256').update(text).digest().readUInt32BE(0);
}

/** A small seeded random number generator (mulberry32). */
function seededRandom(seed: number): () => number {
  let state = seed;
  return () => {
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Every company logo in the catalog, in an order that the seed text sets. */
export function mosaicLogos(catalog: Catalog, seed: string): OgLogo[] {
  const logos = catalog.companies.flatMap((company) => {
    const logo = ogLogo(company.logo);
    return logo ? [logo] : [];
  });
  const random = seededRandom(seedOf(seed));
  for (let index = logos.length - 1; index > 0; index -= 1) {
    const other = Math.floor(random() * (index + 1));
    [logos[index], logos[other]] = [logos[other], logos[index]];
  }
  return logos;
}

/** The card of the home page, a section, a guide, or a lesson. */
export function sectionCard(options: {
  eyebrow: string | null;
  title: string;
  description: string;
  date?: string | null;
  logos?: readonly OgLogo[];
}): OgSectionCard {
  return {
    kind: 'section',
    eyebrow: options.eyebrow,
    title: options.title,
    description: options.description,
    excerpt: shorten(options.description, OG_EXCERPT_LIMIT),
    date: options.date ?? null,
    titleSize: titleSize(options.title),
    logos: options.logos ?? [],
  };
}

/** The image file behind a canonical path: `/agents/x` becomes `/og/agents/x.png`. */
export function ogImagePath(path: string): string {
  if (path === '/') return OG_DEFAULT_PATH;
  return `/og${path}.png`;
}

/** Eight hex digits of the drawing input, so a changed card gets a new URL. */
export function ogVersion(card: OgCard): string {
  const hash = createHash('sha256');
  hash.update(String(OG_TEMPLATE_VERSION));
  hash.update(JSON.stringify(card));
  return hash.digest('hex').slice(0, 8);
}

/** The words a reader hears in place of the card. */
export function ogAlt(card: OgCard): string {
  switch (card.kind) {
    case 'entry':
      return `${card.company} · ${card.name}: ${card.excerpt}`;
    case 'organization':
      return `${card.company}: ${card.count}`;
    case 'section':
      return `${card.title}: ${card.description}`;
  }
}

/** The head tags of the page at `path`, whose card is `card`. */
export function ogImage(path: string, card: OgCard): OgImage {
  return {
    url: `${canonicalUrl(ogImagePath(path))}?v=${ogVersion(card)}`,
    alt: ogAlt(card),
  };
}
