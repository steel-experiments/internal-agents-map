// ABOUTME: Decides whether a record is well documented, from the evidence the catalog holds for it.
// ABOUTME: The directory shows well-documented records first and marks them with a badge.

import type { Approach, Catalog } from './catalog';

/**
 * A record is well documented when all of these are true:
 * - its evidence strength is detailed primary evidence,
 * - no claim has low confidence,
 * - every claim has at least one source that supports it,
 * - every source has a saved copy,
 * - every scoped operating model has a known human attention boundary.
 * The rule measures the evidence. It does not say that the claims are true.
 */
export function isWellDocumented(catalog: Catalog, approach: Approach): boolean {
  if (approach.rubric.evidence_strength !== 'detailed-primary') return false;
  const claims = catalog.claims.filter((claim) => claim.approach_id === approach.id);
  if (claims.some((claim) => claim.confidence === 'low')) return false;
  if (claims.some((claim) => !claim.evidence.some((item) => item.relation === 'supports'))) return false;
  const sources = catalog.sources.filter((source) => source.approach_id === approach.id);
  if (sources.length === 0 || sources.some((source) => !source.capture)) return false;
  const models = approach.operating_models;
  return models.length > 0 && models.every((model) => model.attention_boundary !== 'unknown');
}

/** Put the well-documented items first. Each group keeps the order it was given. */
export function documentationOrder<T extends { readonly wellDocumented: boolean }>(items: readonly T[]): T[] {
  return [...items.filter((item) => item.wellDocumented), ...items.filter((item) => !item.wellDocumented)];
}
