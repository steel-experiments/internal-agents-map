// ABOUTME: The query model of the directory search: free text plus facet terms.
// ABOUTME: It resolves typed words to the catalog vocabulary and matches cards without the DOM.

import type { DirectoryCard } from './entry-view';

/** The facets the directory filters by. They are also the URL query parameters. */
export const FACET_KEYS = ['work', 'type', 'invocation', 'supervision'] as const;
export type FacetKey = (typeof FACET_KEYS)[number];

/** The name each facet shows next to a chip or a suggestion. */
export const FACET_LABELS: Record<FacetKey, string> = {
  work: 'Work domain',
  type: 'Approach',
  invocation: 'Work modes',
  supervision: 'Supervision',
};

/** One value a facet can take, with the other spellings a person can type for it. */
export interface FacetTerm {
  readonly key: FacetKey;
  readonly id: string;
  readonly label: string;
  readonly aliases: readonly string[];
}

/** The selected values of each facet. Values of one facet combine with OR, facets with AND. */
export type Selection = Readonly<Record<FacetKey, readonly string[]>>;

/** The facet values a card carries, read from its data attributes or its view. */
export type CardFacets = Readonly<Record<FacetKey, readonly string[]>>;

/** The most suggestions the search box lists at once. */
export const SUGGESTION_LIMIT = 8;

/** Lower case, single spaces, no edges. The same form the card search text uses. */
export function normalize(value: string): string {
  return value.toLowerCase().replace(/\s+/g, ' ').trim();
}

/** Every spelling a term answers to, normalized. */
function spellings(term: FacetTerm): string[] {
  return [term.id, term.label, ...term.aliases].flatMap((value) => [normalize(value), normalize(value.replace(/-/g, ' '))]);
}

/** Collect the facet vocabulary of the directory from its cards, sorted by label within each facet. */
export function facetVocabulary(cards: readonly DirectoryCard[]): FacetTerm[] {
  const terms = new Map<string, FacetTerm>();
  const add = (term: FacetTerm): void => {
    terms.set(`${term.key}:${term.id}`, term);
  };
  for (const card of cards) {
    for (const domain of card.domains) add({ key: 'work', id: domain.id, label: domain.label, aliases: [] });
    add({ key: 'type', id: card.approachType, label: card.approachTypeLabel, aliases: [] });
    for (const mode of card.invocation) {
      add({ key: 'invocation', id: mode.id, label: mode.label, aliases: mode.id === 'interactive' ? ['foreground'] : [] });
    }
    for (const boundary of card.boundaries) {
      add({
        key: 'supervision',
        id: boundary.id,
        label: boundary.level === null ? boundary.label : `${boundary.label} (level ${boundary.level})`,
        aliases: boundary.level === null ? [boundary.label] : [boundary.label, `level ${boundary.level}`],
      });
    }
  }
  return [...terms.values()].sort(
    (a, b) => FACET_KEYS.indexOf(a.key) - FACET_KEYS.indexOf(b.key) || a.label.localeCompare(b.label),
  );
}

/** The term that a typed text names exactly, by identifier, label, or alias. */
export function resolveTerm(text: string, vocabulary: readonly FacetTerm[]): FacetTerm | null {
  const wanted = normalize(text);
  if (!wanted) return null;
  return vocabulary.find((term) => spellings(term).includes(wanted)) ?? null;
}

/** The term of a facet with a given identifier, or null when the catalog does not use it. */
export function findTerm(key: FacetKey, id: string, vocabulary: readonly FacetTerm[]): FacetTerm | null {
  return vocabulary.find((term) => term.key === key && term.id === id) ?? null;
}

/**
 * The terms a typed text can mean, for the suggestion list.
 * A term qualifies when every word of the text occurs in one of its spellings.
 * Exact matches come first; already selected terms are left out.
 */
export function suggest(
  text: string,
  vocabulary: readonly FacetTerm[],
  selected: readonly FacetTerm[] = [],
  limit = SUGGESTION_LIMIT,
): FacetTerm[] {
  const wanted = normalize(text);
  if (!wanted) return [];
  const words = wanted.split(' ');
  const taken = new Set(selected.map((term) => `${term.key}:${term.id}`));
  const exact: FacetTerm[] = [];
  const partial: FacetTerm[] = [];
  for (const term of vocabulary) {
    if (taken.has(`${term.key}:${term.id}`)) continue;
    const forms = spellings(term);
    if (forms.includes(wanted)) exact.push(term);
    else if (forms.some((form) => words.every((word) => form.includes(word)))) partial.push(term);
  }
  return [...exact, ...partial].slice(0, limit);
}

/** Whether a card's search text carries every word of a free-text query. */
export function matchesText(search: string, query: string): boolean {
  const wanted = normalize(query);
  if (!wanted) return true;
  return wanted.split(' ').every((word) => search.includes(word));
}

/** Whether a card carries a selected value of every facet that has a selection. */
export function matchesFacets(card: CardFacets, selection: Selection): boolean {
  return FACET_KEYS.every((key) => {
    const wanted = selection[key];
    return wanted.length === 0 || wanted.some((value) => card[key].includes(value));
  });
}

/** Group selected terms by facet, in selection order. */
export function toSelection(selected: readonly FacetTerm[]): Selection {
  return {
    work: selected.filter((term) => term.key === 'work').map((term) => term.id),
    type: selected.filter((term) => term.key === 'type').map((term) => term.id),
    invocation: selected.filter((term) => term.key === 'invocation').map((term) => term.id),
    supervision: selected.filter((term) => term.key === 'supervision').map((term) => term.id),
  };
}
