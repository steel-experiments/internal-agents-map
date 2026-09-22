// ABOUTME: Checks the link preview cards: their derived content, their URLs, and one real render.
// ABOUTME: The tests read the real catalog, so a record that breaks a card fails here first.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { companyView } from '../../src/lib/companies';
import { directoryCards } from '../../src/lib/entry-view';
import {
  OG_EXCERPT_LIMIT,
  OG_HEIGHT,
  OG_TAG_LIMIT,
  OG_WIDTH,
  entryCard,
  isWide,
  ogAlt,
  ogImage,
  ogImagePath,
  ogVersion,
  organizationCard,
  organizationCount,
  sectionCard,
  titleSize,
} from '../../src/lib/og';
import { organizationPaths } from '../../src/lib/routes';
import { noteCard, SECTION_CARDS } from '../../src/lib/section-cards';
import { noteViews } from '../../src/lib/notes';
import { renderCard } from '../../src/og/render';

const catalog = loadCatalog();
const cards = directoryCards(catalog);

/** The pixel size in a PNG header. */
function pngSize(bytes: Uint8Array): [number, number] {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  expect(Array.from(bytes.slice(0, 8))).toEqual([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  return [view.getUint32(16), view.getUint32(20)];
}

describe('the entry card', () => {
  it('names every entry the way the directory does, within the card limits', () => {
    for (const card of cards) {
      const og = entryCard(card);
      expect(og.company, card.id).toBe(card.company);
      expect(og.name, card.id).toBe(card.agentName);
      expect(og.excerpt.length, card.id).toBeLessThanOrEqual(OG_EXCERPT_LIMIT + 1);
      expect(og.tags.length, card.id).toBeGreaterThan(0);
      expect(og.tags.length, card.id).toBeLessThanOrEqual(OG_TAG_LIMIT);
      expect(og.tags[0], card.id).toBe(card.approachTypeLabel);
      expect([80, 72, 64], card.id).toContain(og.titleSize);
    }
  });

  it('steps the title size down as the possessive title grows', () => {
    expect(titleSize("Ramp's Inspect")).toBe(72);
    expect(titleSize('Short name')).toBe(80);
    expect(titleSize("Brex's Collections response agent")).toBe(64);
  });

  it('treats a logo twice as wide as tall as a wordmark', () => {
    expect(isWide(122, 32)).toBe(true);
    expect(isWide(440, 440)).toBe(false);
    expect(isWide(858, 375)).toBe(true);
    const brex = cards.find((card) => card.companyView.id === 'brex')!;
    expect(entryCard(brex).logo?.wide).toBe(true);
  });
});

describe('the organization card', () => {
  it('counts the two collections in words', () => {
    expect(organizationCount(4, 1)).toBe('4 agents and 1 infrastructure entry in the catalog');
    expect(organizationCount(1, 0)).toBe('1 agent in the catalog');
    expect(organizationCount(0, 2)).toBe('2 infrastructure entries in the catalog');
  });

  it('lists every system of every published organization', () => {
    for (const path of organizationPaths(catalog)) {
      const id = path.split('/').pop()!;
      const members = cards.filter((card) => card.companyView.id === id);
      const og = organizationCard(companyView(catalog, id), members);
      expect(og.names, id).toEqual(members.map((card) => card.agentName));
      expect(og.count, id).toMatch(/ in the catalog$/);
    }
  });
});

describe('the card URL', () => {
  it('maps each canonical path to a file under /og, except the home page', () => {
    expect(ogImagePath('/')).toBe('/og.png');
    expect(ogImagePath('/agents/block-builderbot')).toBe('/og/agents/block-builderbot.png');
    expect(ogImagePath('/organizations/brex')).toBe('/og/organizations/brex.png');
    expect(ogImagePath('/infrastructure')).toBe('/og/infrastructure.png');
    expect(ogImagePath('/notes/stop-a-run')).toBe('/og/notes/stop-a-run.png');
  });

  it('changes its version with the card and keeps it otherwise', () => {
    const card = entryCard(cards[0]);
    expect(ogVersion(card)).toMatch(/^[0-9a-f]{8}$/);
    expect(ogVersion(card)).toBe(ogVersion({ ...card }));
    expect(ogVersion(card)).not.toBe(ogVersion({ ...card, excerpt: `${card.excerpt} ` }));
  });

  it('builds the head values on the production origin', () => {
    const card = entryCard(cards[0]);
    const image = ogImage(cards[0].path, card);
    expect(image.url).toBe(`https://internal-agents.com/og${cards[0].path}.png?v=${ogVersion(card)}`);
    expect(image.alt).toBe(ogAlt(card));
    expect(image.alt).toContain(card.name);
  });

  it('has a card for every section page and every note', () => {
    expect(Object.keys(SECTION_CARDS).sort()).toEqual(['definitions', 'infrastructure', 'methodology', 'notes']);
    for (const note of noteViews()) {
      const card = noteCard(note);
      expect(card.title).toBe(note.title);
      expect(card.date).toMatch(/\d{4}$/);
    }
    expect(sectionCard({ eyebrow: 'Notes', title: 'Notes', description: 'Short notes.' }).date).toBeNull();
  });
});

describe('the renderer', () => {
  it('draws a card at the preview size, and the same bytes twice', { timeout: 30_000 }, async () => {
    const card = entryCard(cards.find((item) => item.id === 'block-builderbot') ?? cards[0]);
    const first = await renderCard(card);
    const second = await renderCard(card);
    expect(pngSize(first)).toEqual([OG_WIDTH, OG_HEIGHT]);
    expect(first.length).toBeLessThan(300_000);
    expect(Buffer.compare(Buffer.from(first), Buffer.from(second))).toBe(0);
  });

  it('draws the organization and section cards', { timeout: 30_000 }, async () => {
    const brex = organizationCard(companyView(catalog, 'brex'), cards.filter((card) => card.companyView.id === 'brex'));
    expect(pngSize(await renderCard(brex))).toEqual([OG_WIDTH, OG_HEIGHT]);
    expect(pngSize(await renderCard(SECTION_CARDS.notes))).toEqual([OG_WIDTH, OG_HEIGHT]);
    expect(pngSize(await renderCard(noteCard(noteViews()[0])))).toEqual([OG_WIDTH, OG_HEIGHT]);
  });
});
