// ABOUTME: Draws one link preview card as a PNG with satori and resvg at build time.
// ABOUTME: Reads the licensed ABC Areal desktop files and the vendored logos from disk.

import { readFileSync } from 'node:fs';
import path from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import satori, { type Font } from 'satori';
import { OG_HEIGHT, OG_WIDTH, type OgCard, type OgEntryCard, type OgLogo, type OgOrganizationCard, type OgSectionCard } from '../lib/og';

// The build runs from the repository root, as the publication integration assumes.
const ROOT = process.cwd();
const FONT_DIR = path.join(ROOT, 'src/og/fonts');
const PUBLIC_DIR = path.join(ROOT, 'public');

const INK = '#21201c';
const MUTED = '#82827c';
const SOFT = '#63635e';
const SAND3 = '#f1f0ef';
const WHITE = '#ffffff';
const BLUE = '#0090ff';
const BLUE3 = '#e6f4fe';
const FAMILY = 'ABC Areal';
const SITE = 'internal-agents.com';

/** A satori element. Every element with more than one child needs `display: flex`. */
type Node = { type: string; props: Record<string, unknown> };
type Style = Record<string, string | number>;

function h(type: string, style: Style, children?: unknown, extra: Record<string, unknown> = {}): Node {
  return { type, props: { style, children, ...extra } };
}

const column = (style: Style, children: unknown[]): Node =>
  h('div', { display: 'flex', flexDirection: 'column', ...style }, children);
const row = (style: Style, children: unknown[]): Node =>
  h('div', { display: 'flex', flexDirection: 'row', ...style }, children);

let fonts: Font[] | undefined;

/** The two weights DESIGN.md allows. Missing files stop the build; there is no fallback face. */
function loadFonts(): Font[] {
  fonts ??= [
    { name: FAMILY, weight: 400, style: 'normal', data: readFileSync(path.join(FONT_DIR, 'ABCAreal-Regular.ttf')) },
    { name: FAMILY, weight: 500, style: 'normal', data: readFileSync(path.join(FONT_DIR, 'ABCAreal-Medium.ttf')) },
  ];
  return fonts;
}

function logoDataUri(logo: OgLogo): string {
  const mime = logo.path.endsWith('.svg') ? 'image/svg+xml' : 'image/png';
  const bytes = readFileSync(path.join(PUBLIC_DIR, logo.path));
  return `data:${mime};base64,${bytes.toString('base64')}`;
}

/** Fit a logo to a box height, keeping its ratio. A raster file never grows past its own pixels. */
function logoImage(logo: OgLogo, boxHeight: number): Node {
  const raster = !logo.path.endsWith('.svg');
  const height = raster ? Math.min(boxHeight, logo.height) : boxHeight;
  const width = Math.round((height * logo.width) / logo.height);
  return h('img', { width, height }, undefined, { src: logoDataUri(logo), width, height });
}

/** The letters the site shows when it holds no logo. */
function monogramBox(letters: string, size: number): Node {
  return row(
    { width: size, height: size, borderRadius: Math.round(size / 5), background: SAND3, alignItems: 'center', justifyContent: 'center', fontSize: Math.round(size * 0.4), fontWeight: 500, color: INK },
    [letters],
  );
}

/** The mark of an organization with its name, unless the mark already spells it. */
function mark(logo: OgLogo | null, monogram: string, company: string, markHeight: number, wideHeight: number, nameSize: number): Node[] {
  if (!logo) return [monogramBox(monogram, markHeight), h('div', { fontSize: nameSize, fontWeight: 500, marginTop: 26 }, company)];
  if (logo.wide) return [logoImage(logo, wideHeight)];
  return [logoImage(logo, markHeight), h('div', { fontSize: nameSize, fontWeight: 500, marginTop: 26 }, company)];
}

function tag(label: string, first: boolean): Node {
  return h(
    'div',
    { fontSize: 28, lineHeight: 1, padding: '12px 20px', borderRadius: 28, background: first ? BLUE3 : WHITE, color: first ? BLUE : SOFT, marginRight: 16, marginBottom: 16 },
    label,
  );
}

const footer = (text: string): Node => h('div', { marginTop: 'auto', fontSize: 26, fontWeight: 500, color: INK }, text);

const frame = (children: unknown[], direction: 'row' | 'column'): Node =>
  h('div', { display: 'flex', flexDirection: direction, width: OG_WIDTH, height: OG_HEIGHT, background: SAND3, padding: '72px 84px 60px', fontFamily: FAMILY, color: INK }, children);

/** The directory card at poster scale: the possessive title, the summary, the tags, the mark on a panel. */
function entryTree(card: OgEntryCard): Node {
  return frame([
    column({ flex: 1, marginRight: 56, minWidth: 0 }, [
      row({ flexWrap: 'wrap', fontSize: card.titleSize, fontWeight: 500, letterSpacing: '-0.03em', lineHeight: 1.02 }, [
        h('span', { color: MUTED, marginRight: '0.22em' }, `${card.company}'s`),
        h('span', {}, card.name),
      ]),
      h('div', { fontSize: 32, lineHeight: 1.38, color: MUTED, marginTop: 24, letterSpacing: '-0.01em' }, card.excerpt),
      row({ marginTop: 30, marginBottom: -16 }, card.tags.map((label, index) => tag(label, index === 0))),
      footer(SITE),
    ]),
    column({ width: 340, background: WHITE, borderRadius: 32, alignItems: 'center', justifyContent: 'center' }, mark(card.logo, card.monogram, card.company, 120, 64, 32)),
  ], 'row');
}

/** The organization card: mark, name, count, and the names of its systems as tags. */
function organizationTree(card: OgOrganizationCard): Node {
  const head = card.logo?.wide
    ? [logoImage(card.logo, 56)]
    : [
        card.logo ? logoImage(card.logo, 64) : monogramBox(card.monogram, 64),
        h('div', { fontSize: 32, fontWeight: 500, marginLeft: 24 }, card.company),
      ];
  return frame([
    row({ alignItems: 'center' }, head),
    h('div', { fontSize: 80, fontWeight: 500, letterSpacing: '-0.03em', lineHeight: 1.02, marginTop: 30 }, card.company),
    h('div', { fontSize: 32, lineHeight: 1.38, color: MUTED, marginTop: 22, letterSpacing: '-0.01em' }, card.count),
    row({ flexWrap: 'wrap', marginTop: 26 }, card.names.map((name) => tag(name, false))),
    footer(SITE),
  ], 'column');
}

/** A section, guide, or note: a blue dot, the eyebrow, the title, the description. */
function sectionTree(card: OgSectionCard): Node {
  const eyebrow: unknown[] = [
    h('div', { width: 14, height: 14, borderRadius: 7, background: BLUE, marginRight: 18 }),
    h('div', { fontSize: 26, letterSpacing: '0.12em', textTransform: 'uppercase', color: MUTED }, card.eyebrow),
  ];
  if (card.date) {
    eyebrow.push(h('div', { width: 6, height: 6, borderRadius: 3, background: '#dad9d6', margin: '0 18px' }));
    eyebrow.push(h('div', { fontSize: 26, color: MUTED }, card.date));
  }
  return frame([
    row({ alignItems: 'center' }, eyebrow),
    h('div', { fontSize: 72, fontWeight: 500, letterSpacing: '-0.03em', lineHeight: 1.05, marginTop: 30 }, card.title),
    h('div', { fontSize: 32, lineHeight: 1.38, color: MUTED, marginTop: 22, letterSpacing: '-0.01em', maxWidth: 900 }, card.description),
    footer(SITE),
  ], 'column');
}

function tree(card: OgCard): Node {
  switch (card.kind) {
    case 'entry':
      return entryTree(card);
    case 'organization':
      return organizationTree(card);
    case 'section':
      return sectionTree(card);
  }
}

/** Render one card to PNG bytes. The same input gives the same bytes. */
export async function renderCard(card: OgCard): Promise<Uint8Array> {
  const svg = await satori(tree(card) as never, { width: OG_WIDTH, height: OG_HEIGHT, fonts: loadFonts() });
  return new Resvg(svg, { fitTo: { mode: 'width', value: OG_WIDTH } }).render().asPng();
}

/** The HTTP response of a card endpoint. */
export function pngResponse(bytes: Uint8Array): Response {
  // The body type wants a plain ArrayBuffer view; a Buffer is one, so copy its bytes over.
  return new Response(new Uint8Array(bytes), { headers: { 'Content-Type': 'image/png' } });
}
