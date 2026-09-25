// ABOUTME: Draws one link preview card as a PNG with satori and resvg at build time.
// ABOUTME: Reads the licensed ABC Areal desktop files and the vendored logos, and keeps drawn cards in a disk cache.

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, utimesSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import satori, { type Font } from 'satori';
import { OG_HEIGHT, OG_WIDTH, type OgCard, type OgEntryCard, type OgLogo, type OgOrganizationCard, type OgSectionCard } from '../lib/og';

// The build runs from the repository root, as the publication integration assumes.
const ROOT = process.cwd();
const FONT_DIR = path.join(ROOT, 'src/og/fonts');
const PUBLIC_DIR = path.join(ROOT, 'public');
// Drawing one card takes about half a second, so the build keeps each PNG under the hash of its input.
// CI restores this directory between runs and removes the files that a run did not use.
const CACHE_DIR = path.join(ROOT, 'node_modules/.cache/og-cards');

const INK = '#21201c';
const SAND1 = '#fdfdfc';
const SAND3 = '#f1f0ef';
const SAND5 = '#e2e1de';
const SAND6 = '#dad9d6';
const SAND9 = '#8d8d86';
const WHITE = '#ffffff';
const BLUE = '#0090ff';
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

/** Fit a logo to a box, keeping its ratio. A raster file never grows past its own pixels. */
function logoImage(logo: OgLogo, boxHeight: number, boxWidth = Infinity): Node {
  const raster = !logo.path.endsWith('.svg');
  const fitted = Math.min(boxHeight, (boxWidth * logo.height) / logo.width);
  const height = Math.round(raster ? Math.min(fitted, logo.height) : fitted);
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

/** A pill: the first tag of an entry is solid blue, the others are Sand. */
function tag(label: string, first: boolean): Node {
  return h(
    'div',
    { fontSize: 20, fontWeight: 500, lineHeight: '28px', letterSpacing: '-0.02em', padding: '6px 14px', borderRadius: 100, background: first ? BLUE : SAND5, color: first ? SAND1 : INK, marginRight: 12, marginBottom: 12 },
    label,
  );
}

/** "internal-agents.com by steel.dev", with the "by" in Sand 9. */
const footer = (): Node =>
  row({ position: 'absolute', left: 72, bottom: 72, fontSize: 24, fontWeight: 500, lineHeight: '32px', letterSpacing: '-0.02em', color: INK }, [
    h('span', {}, SITE),
    h('span', { color: SAND9, margin: '0 0.2em' }, 'by'),
    h('span', {}, 'steel.dev'),
  ]);

const CARD_WIDTH = 407;
const CARD_HEIGHT = 511;
const CARD_LEFT = 719;
const CARD_TOP = 59;
const CARD_SHADOW = '0px 22px 13px rgba(0,0,0,0.01), 0px 10px 10px rgba(0,0,0,0.02), 0px 2px 5px rgba(0,0,0,0.03)';

/** One white card of the stack. All three turn around the same center. */
function stackCard(rotate: number, children: unknown[] = []): Node {
  return column(
    { position: 'absolute', left: CARD_LEFT, top: CARD_TOP, width: CARD_WIDTH, height: CARD_HEIGHT, background: WHITE, border: `0.5px solid ${SAND6}`, borderRadius: 32, boxShadow: CARD_SHADOW, alignItems: 'center', justifyContent: 'center', transform: `rotate(${rotate}deg)` },
    children,
  );
}

/** The mark on the front card: the logo in a 183px box, or the monogram. */
function frontMark(logo: OgLogo | null, monogram: string): Node {
  if (!logo) return monogramBox(monogram, 183);
  return logo.wide ? logoImage(logo, 96, 300) : logoImage(logo, 183, 183);
}

/** Every card: the title, the text below it and the tags on the left, and a stack of cards on the right. */
function poster(title: string, size: number, text: string, tags: readonly Node[], front: Node): Node {
  const left: Node[] = [
    h('div', { fontSize: size, fontWeight: 500, lineHeight: 1.125, letterSpacing: '-0.02em', color: '#000000' }, title),
    h('div', { fontSize: 26, fontWeight: 500, lineHeight: '38px', letterSpacing: '-0.02em', color: SAND9, marginTop: 16 }, text),
  ];
  if (tags.length > 0) left.push(row({ flexWrap: 'wrap', marginTop: 20, marginBottom: -12 }, [...tags]));
  return h('div', { display: 'flex', position: 'relative', width: OG_WIDTH, height: OG_HEIGHT, background: SAND3, fontFamily: FAMILY, color: INK }, [
    column({ position: 'absolute', left: 72, top: 72, width: 511 }, left),
    footer(),
    stackCard(-14.15),
    stackCard(-6.26),
    stackCard(0, [front]),
  ]);
}

/** The directory card at poster scale: the title, the summary, the tags, and the mark on the cards. */
function entryTree(card: OgEntryCard): Node {
  const tags = card.tags.map((label, index) => tag(label, index === 0));
  return poster(card.title, card.titleSize, card.excerpt, tags, frontMark(card.logo, card.monogram));
}

/** An organization shows this many names of its systems, and counts the rest in one more tag. */
const ORGANIZATION_NAME_LIMIT = 3;

/** The organization card: the name, the count, the names of its systems as tags, and the mark on the cards. */
function organizationTree(card: OgOrganizationCard): Node {
  const labels = card.names.slice(0, ORGANIZATION_NAME_LIMIT);
  const rest = card.names.length - labels.length;
  if (rest > 0) labels.push(`+${rest} more`);
  const tags = labels.map((label) => tag(label, false));
  return poster(card.company, card.titleSize, card.count, tags, frontMark(card.logo, card.monogram));
}

const MOSAIC_PITCH = 92;
const MOSAIC_SIZE = 104;
const MOSAIC_INSET = 30;
/** How much a logo shrinks from the center of the card to its edge. */
const MOSAIC_FALLOFF = 0.7;

/**
 * The logos on a honeycomb, largest at the center of the card, each one fully inside it.
 * Each logo covers about the same area, so a wordmark and a square mark read at one weight.
 */
function mosaic(logos: readonly OgLogo[]): Node {
  const rowHeight = MOSAIC_PITCH * 0.866;
  const centerX = CARD_WIDTH / 2;
  const centerY = CARD_HEIGHT / 2;
  const cells: Node[] = [];
  for (let line = -6; line <= 6; line += 1) {
    for (let step = -6; step <= 6; step += 1) {
      if (cells.length >= logos.length) break;
      const x = centerX + step * MOSAIC_PITCH + (Math.abs(line) % 2 ? MOSAIC_PITCH / 2 : 0);
      const y = centerY + line * rowHeight;
      const distance = Math.hypot((x - centerX) / centerX, (y - centerY) / centerY);
      const size = MOSAIC_SIZE * Math.max(0.35, 1 - MOSAIC_FALLOFF * distance * distance);
      const half = size / 2;
      if (x - half < MOSAIC_INSET || x + half > CARD_WIDTH - MOSAIC_INSET) continue;
      if (y - half < MOSAIC_INSET || y + half > CARD_HEIGHT - MOSAIC_INSET) continue;
      const logo = logos[cells.length];
      const root = Math.sqrt(logo.width / logo.height);
      const side = size * 0.58;
      cells.push(
        row(
          { position: 'absolute', left: Math.round(x - half), top: Math.round(y - half), width: Math.round(size), height: Math.round(size), alignItems: 'center', justifyContent: 'center' },
          [logoImage(logo, side / root, Math.min(size, side * root))],
        ),
      );
    }
  }
  return h('div', { display: 'flex', position: 'relative', width: CARD_WIDTH, height: CARD_HEIGHT }, cells);
}

/** The home page, a section, guide, problem, or lesson: the title, the description, the kind and date as tags, and the logos on the cards. */
function sectionTree(card: OgSectionCard): Node {
  const tags: Node[] = [];
  if (card.eyebrow) tags.push(tag(card.eyebrow, true));
  if (card.date) tags.push(tag(card.date, false));
  return poster(card.title, card.titleSize, card.excerpt, tags, mosaic(card.logos));
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

function packageVersion(name: string): string {
  return JSON.parse(readFileSync(path.join(ROOT, 'node_modules', name, 'package.json'), 'utf8')).version;
}

/**
 * The hash of all that decides the PNG bytes. The element tree holds every style and each logo as a
 * data URI, so a change to the layout, the content, or a logo gives a new key.
 */
function cacheKey(element: Node): string {
  const hash = createHash('sha256');
  hash.update(JSON.stringify(element));
  for (const font of loadFonts()) hash.update(font.data as Buffer);
  hash.update(`${OG_WIDTH}x${OG_HEIGHT} satori@${packageVersion('satori')} resvg@${packageVersion('@resvg/resvg-js')}`);
  return hash.digest('hex');
}

async function draw(element: Node): Promise<Uint8Array> {
  const svg = await satori(element as never, { width: OG_WIDTH, height: OG_HEIGHT, fonts: loadFonts() });
  return new Resvg(svg, { fitTo: { mode: 'width', value: OG_WIDTH } }).render().asPng();
}

/**
 * Render one card to PNG bytes. The same input gives the same bytes.
 * With a cache directory, a card drawn before is read from disk; `null` always draws.
 */
export async function renderCard(card: OgCard, cacheDir: string | null = CACHE_DIR): Promise<Uint8Array> {
  const element = tree(card);
  if (cacheDir === null) return draw(element);
  const file = path.join(cacheDir, `${cacheKey(element)}.png`);
  try {
    const bytes = readFileSync(file);
    // A fresh time marks the file as in use, so CI keeps it.
    const now = new Date();
    utimesSync(file, now, now);
    return bytes;
  } catch {
    const bytes = await draw(element);
    mkdirSync(cacheDir, { recursive: true });
    writeFileSync(file, bytes);
    return bytes;
  }
}

/** The HTTP response of a card endpoint. */
export function pngResponse(bytes: Uint8Array): Response {
  // The body type wants a plain ArrayBuffer view; a Buffer is one, so copy its bytes over.
  return new Response(new Uint8Array(bytes), { headers: { 'Content-Type': 'image/png' } });
}
