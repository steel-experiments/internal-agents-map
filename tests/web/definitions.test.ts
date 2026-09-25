// ABOUTME: Checks that a chart placement depends on the evidence the catalog holds.
// ABOUTME: A claim that is removed, emptied, or unsupported removes its placement.

import { describe, expect, it } from 'vitest';
import { loadCatalog, type Catalog, type Claim } from '../../src/lib/catalog';
import {
  PLACEMENT_CANDIDATES,
  UPGRADE_PATHS,
  markerAnchor,
  placements,
  placementsByCell,
  referenceMarkers,
  regionOf,
  upgradePaths,
} from '../../src/lib/definitions';
import { REFERENCE_PLACEMENTS } from '../../src/lib/guide-content';
import { entryPath } from '../../src/lib/routes';

const catalog = loadCatalog();
const SAMPLE = 'stripe-minions';

/** Copy the catalog with one claim of one implementation changed or removed. */
function withClaim(field: string, change: ((claim: Claim) => Claim) | null): Catalog {
  const target = catalog.claims.find(
    (claim) => claim.approach_id === SAMPLE && claim.field === field,
  )!;
  if (change === null) {
    return {
      ...catalog,
      approaches: catalog.approaches.map((item) =>
        item.id === SAMPLE
          ? { ...item, claim_ids: item.claim_ids.filter((id) => id !== target.id) }
          : item,
      ),
      claims: catalog.claims.filter((claim) => claim.id !== target.id),
    };
  }
  return {
    ...catalog,
    claims: catalog.claims.map((claim) => (claim.id === target.id ? change(claim) : claim)),
  };
}

describe('the chart placements', () => {
  it('places every selected implementation the catalog still supports', () => {
    const placed = placements(catalog);
    expect(placed.map((item) => item.id).sort()).toEqual(
      PLACEMENT_CANDIDATES.map((item) => item.id).sort(),
    );
  });

  it('links a placement to the entry page and to the claim it names', () => {
    const minions = placements(catalog).find((item) => item.id === SAMPLE)!;
    expect(minions.path).toBe(entryPath(SAMPLE));
    expect(minions.evidence.map((item) => item.label)).toEqual(['Scope', 'Context', 'Tools']);
    for (const link of minions.evidence) {
      expect(link.href.startsWith(`${entryPath(SAMPLE)}#claim-${SAMPLE}--`)).toBe(true);
    }
  });

  it('groups the placements by the region that holds them', () => {
    const cells = placementsByCell(catalog);
    expect(cells.specialized.map((item) => item.id)).toContain(SAMPLE);
    expect(cells.shared.map((item) => item.id)).toContain('sentry-junior');
    expect(cells.ready.map((item) => item.id)).toContain('cursor-support-workflow');
    expect(cells.ready.map((item) => item.id)).not.toContain('retool-retoolgpt');
  });

  it('derives the region from the coordinates, so the two cannot disagree', () => {
    expect(regionOf(20, 80)).toBe('specialized');
    expect(regionOf(80, 80)).toBe('shared');
    expect(regionOf(20, 20)).toBe('ready');
    expect(regionOf(80, 20)).toBe('assistants');
    for (const item of placements(catalog)) expect(item.cell).toBe(regionOf(item.x, item.y));
    for (const item of referenceMarkers()) expect(item.cell).toBe(regionOf(item.x, item.y));
  });

  it('keeps every marker inside the plot and clear of the two axes', () => {
    for (const item of [...PLACEMENT_CANDIDATES, ...REFERENCE_PLACEMENTS]) {
      for (const value of [item.x, item.y]) {
        expect(value, item.id).toBeGreaterThan(0);
        expect(value, item.id).toBeLessThan(100);
        expect(Math.abs(value - 50), item.id).toBeGreaterThanOrEqual(5);
      }
    }
  });

  it('gives every marker its own note anchor', () => {
    const anchors = [...PLACEMENT_CANDIDATES, ...REFERENCE_PLACEMENTS].map((item) => markerAnchor(item.id));
    expect(new Set(anchors).size).toBe(anchors.length);
  });
});

describe('the upgrade arrows', () => {
  it('draws each arrow upward, from a reference product to a catalog entry built on it', () => {
    const arrows = upgradePaths(catalog);
    expect(arrows.map((arrow) => arrow.to.id).sort()).toEqual(['github-qubot', 'spotify-honk-xirp']);
    const references = new Map(referenceMarkers().map((item) => [item.id, item]));
    const placed = new Map(placements(catalog).map((item) => [item.id, item]));
    for (const arrow of arrows) {
      expect(arrow.from).toMatchObject({ x: references.get(arrow.from.id)!.x, y: references.get(arrow.from.id)!.y });
      expect(arrow.to).toMatchObject({ x: placed.get(arrow.to.id)!.x, y: placed.get(arrow.to.id)!.y });
      expect(arrow.to.y).toBeGreaterThan(arrow.from.y);
    }
  });

  it('drops an arrow when its catalog entry loses its placement', () => {
    const target = UPGRADE_PATHS[0].to;
    const fixture: Catalog = {
      ...catalog,
      approaches: catalog.approaches.map((item) =>
        item.id === target
          ? { ...item, claim_ids: item.claim_ids.filter((id) => !id.endsWith('--summary')) }
          : item,
      ),
    };
    expect(upgradePaths(fixture).map((arrow) => arrow.to.id)).not.toContain(target);
  });

  it('drops a placement when a required claim is removed', () => {
    const fixture = withClaim('architecture.tool_access', null);
    expect(placements(fixture).map((item) => item.id)).not.toContain(SAMPLE);
    expect(placements(fixture).map((item) => item.id)).toContain('sentry-junior');
  });

  it('drops a placement when a required claim says nothing', () => {
    const fixture = withClaim('architecture.knowledge', (claim) => ({ ...claim, text: 'Unknown' }));
    expect(placements(fixture).map((item) => item.id)).not.toContain(SAMPLE);
  });

  it('drops a placement when no source supports the required claim', () => {
    const fixture = withClaim('summary', (claim) => ({
      ...claim,
      evidence: claim.evidence.map((item) => ({ ...item, relation: 'contextualizes' as const })),
    }));
    expect(placements(fixture).map((item) => item.id)).not.toContain(SAMPLE);
  });
});
