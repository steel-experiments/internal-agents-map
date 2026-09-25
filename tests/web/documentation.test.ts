// ABOUTME: Checks the rule that marks a record as well documented, and the order it gives the directory.
// ABOUTME: Each condition of the rule is proven by a record that fails it alone.

import { describe, expect, it } from 'vitest';
import { loadCatalog, type Approach, type Catalog } from '../../src/lib/catalog';
import { documentationOrder, isWellDocumented } from '../../src/lib/documentation';

const catalog = loadCatalog();
const approach = (id: string): Approach => catalog.approaches.find((item) => item.id === id)!;
const stripe = approach('stripe-minions');

/** The catalog with one approach, its claims, or its sources changed. */
function edited(change: {
  approach?: Partial<Approach>;
  claim?: (claim: Catalog['claims'][number]) => Catalog['claims'][number];
  source?: (source: Catalog['sources'][number]) => Catalog['sources'][number];
}): { catalog: Catalog; approach: Approach } {
  const changed = { ...stripe, ...change.approach } as Approach;
  const firstClaim = catalog.claims.find((claim) => claim.approach_id === stripe.id)!;
  const firstSource = catalog.sources.find((source) => source.approach_id === stripe.id)!;
  return {
    approach: changed,
    catalog: {
      ...catalog,
      approaches: catalog.approaches.map((item) => (item.id === stripe.id ? changed : item)),
      claims: catalog.claims.map((claim) => (claim === firstClaim && change.claim ? change.claim(claim) : claim)),
      sources: catalog.sources.map((source) => (source === firstSource && change.source ? change.source(source) : source)),
    },
  };
}

describe('the well-documented rule', () => {
  it('marks records with detailed, archived, fully supported evidence', () => {
    for (const id of ['stripe-minions', 'linear-agent', 'posthog-stamphog', 'sierra-pinecone']) {
      expect(isWellDocumented(catalog, approach(id)), id).toBe(true);
    }
  });

  it('does not mark records with thin or unarchived evidence', () => {
    for (const id of ['airbnb-datako', 'airbnb-pascal', 'brex-disputes', 'uber-coding-agent']) {
      expect(isWellDocumented(catalog, approach(id)), id).toBe(false);
    }
  });

  it('requires detailed primary evidence', () => {
    const { catalog: changed, approach: record } = edited({
      approach: { rubric: { ...stripe.rubric, evidence_strength: 'mixed' } },
    });
    expect(isWellDocumented(changed, record)).toBe(false);
  });

  it('rejects a record with a low-confidence claim', () => {
    const { catalog: changed, approach: record } = edited({ claim: (claim) => ({ ...claim, confidence: 'low' }) });
    expect(isWellDocumented(changed, record)).toBe(false);
  });

  it('rejects a record with a claim that no source supports', () => {
    const { catalog: changed, approach: record } = edited({
      claim: (claim) => ({
        ...claim,
        evidence: claim.evidence.map((item) => ({ ...item, relation: 'contextualizes' as const })),
      }),
    });
    expect(isWellDocumented(changed, record)).toBe(false);
  });

  it('rejects a record with a source that has no saved copy', () => {
    const { catalog: changed, approach: record } = edited({ source: (source) => ({ ...source, capture: null }) });
    expect(isWellDocumented(changed, record)).toBe(false);
  });

  it('rejects a record whose human attention boundary is unknown', () => {
    const { catalog: changed, approach: record } = edited({
      approach: { operating_models: [...stripe.operating_models, { scope: 'x', attention_boundary: 'unknown', level: null }] },
    });
    expect(isWellDocumented(changed, record)).toBe(false);
  });

  it('rejects a record with no operating model', () => {
    const { catalog: changed, approach: record } = edited({ approach: { operating_models: [] } });
    expect(isWellDocumented(changed, record)).toBe(false);
  });
});

describe('the documentation order', () => {
  it('puts well-documented records first and keeps the given order within each group', () => {
    const cards = [
      { id: 'a', featured: false, wellDocumented: false },
      { id: 'b', featured: false, wellDocumented: true },
      { id: 'c', featured: false, wellDocumented: false },
      { id: 'd', featured: false, wellDocumented: true },
    ];
    expect(documentationOrder(cards).map((card) => card.id)).toEqual(['b', 'd', 'a', 'c']);
  });

  it('puts featured records before all others', () => {
    const cards = [
      { id: 'a', featured: false, wellDocumented: true },
      { id: 'b', featured: true, wellDocumented: true },
      { id: 'c', featured: false, wellDocumented: false },
      { id: 'd', featured: true, wellDocumented: true },
    ];
    expect(documentationOrder(cards).map((card) => card.id)).toEqual(['b', 'd', 'a', 'c']);
  });
});

describe('the featured records', () => {
  const featured = catalog.approaches.filter((item) => item.featured);

  it('are the records the catalog shows first', () => {
    expect(featured.map((item) => item.id).sort()).toEqual(['linear-agent', 'sierra-pinecone', 'stripe-minions']);
  });

  it('are all well documented', () => {
    for (const item of featured) expect(isWellDocumented(catalog, item), item.id).toBe(true);
  });
});
