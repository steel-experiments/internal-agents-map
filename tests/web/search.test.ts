// ABOUTME: Checks the directory search model: vocabulary, term resolution, suggestions, and matching.
// ABOUTME: The browser script only wires these functions to the DOM, so the rules live here.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { directoryCards } from '../../src/lib/entry-view';
import {
  FACET_KEYS,
  facetVocabulary,
  findTerm,
  matchesFacets,
  matchesText,
  resolveTerm,
  suggest,
  toSelection,
} from '../../src/lib/search';

const catalog = loadCatalog();
const cards = directoryCards(catalog);
const vocabulary = facetVocabulary(cards);

describe('the facet vocabulary', () => {
  it('holds every work, approach type, invocation, and supervision value once', () => {
    const seen = new Set(vocabulary.map((term) => `${term.key}:${term.id}`));
    expect(seen.size).toBe(vocabulary.length);
    for (const card of cards) {
      for (const domain of card.domains) expect(seen.has(`work:${domain.id}`)).toBe(true);
      expect(seen.has(`type:${card.approachType}`)).toBe(true);
      for (const mode of card.invocation) expect(seen.has(`invocation:${mode.id}`)).toBe(true);
      for (const boundary of card.boundaries) expect(seen.has(`supervision:${boundary.id}`)).toBe(true);
    }
  });

  it('orders the terms by facet, then by label', () => {
    const keys = vocabulary.map((term) => FACET_KEYS.indexOf(term.key));
    expect(keys).toEqual([...keys].sort((a, b) => a - b));
    for (const key of FACET_KEYS) {
      const labels = vocabulary.filter((term) => term.key === key).map((term) => term.label);
      expect(labels).toEqual([...labels].sort((a, b) => a.localeCompare(b)));
    }
  });

  it('names a supervision boundary with its level and answers to the level alone', () => {
    const term = findTerm('supervision', 'exception-only', vocabulary)!;
    expect(term.label).toBe('Exception-only (level 5)');
    expect(term.aliases).toEqual(['Exception-only', 'level 5']);
    const unknown = findTerm('supervision', 'unknown', vocabulary)!;
    expect(unknown.label).toBe('Unknown');
    expect(unknown.aliases).toEqual(['Unknown']);
  });
});

describe('term resolution', () => {
  it('resolves an identifier, a label, or an alias regardless of case and spacing', () => {
    expect(resolveTerm('coding', vocabulary)?.id).toBe('coding');
    expect(resolveTerm('  Code Review ', vocabulary)?.id).toBe('code-review');
    expect(resolveTerm('BACKGROUND', vocabulary)?.id).toBe('background');
    expect(resolveTerm('foreground', vocabulary)?.id).toBe('interactive');
    expect(resolveTerm('level 5', vocabulary)?.id).toBe('exception-only');
    expect(resolveTerm('work product review', vocabulary)?.key).toBe('supervision');
  });

  it('leaves free text alone', () => {
    expect(resolveTerm('uber', vocabulary)).toBeNull();
    expect(resolveTerm('coding assistant', vocabulary)).toBeNull();
    expect(resolveTerm('', vocabulary)).toBeNull();
  });

  it('finds a facet value by identifier and rejects one the catalog does not use', () => {
    expect(findTerm('work', 'security', vocabulary)?.label).toBe('Security');
    expect(findTerm('work', 'not-a-real-value', vocabulary)).toBeNull();
    expect(findTerm('type', 'security', vocabulary)).toBeNull();
  });
});

describe('suggestions', () => {
  it('lists nothing for an empty text', () => {
    expect(suggest('', vocabulary)).toEqual([]);
    expect(suggest('   ', vocabulary)).toEqual([]);
  });

  it('lists the terms whose spellings carry every typed word, exact matches first', () => {
    const forCod = suggest('cod', vocabulary);
    expect(forCod.map((term) => term.id)).toEqual(['code-review', 'coding']);
    expect(suggest('coding', vocabulary)[0]?.id).toBe('coding');
    expect(suggest('level 5', vocabulary).map((term) => term.id)).toEqual(['exception-only']);
    expect(suggest('review level', vocabulary).map((term) => term.id)).toEqual([
      'outcome-review',
      'work-product-review',
    ]);
  });

  it('leaves out the terms already selected and respects the limit', () => {
    const coding = findTerm('work', 'coding', vocabulary)!;
    expect(suggest('cod', vocabulary, [coding]).map((term) => term.id)).toEqual(['code-review']);
    expect(suggest('e', vocabulary, [], 3)).toHaveLength(3);
  });
});

describe('card matching', () => {
  it('needs every word of a free text somewhere in the search text', () => {
    expect(matchesText('uber ureview code review coding', 'uber')).toBe(true);
    expect(matchesText('uber ureview code review coding', 'coding uber')).toBe(true);
    expect(matchesText('uber ureview code review coding', 'uber stripe')).toBe(false);
    expect(matchesText('anything', '')).toBe(true);
    expect(matchesText('Uber', 'UBER')).toBe(false);
  });

  it('combines the values of one facet with OR and the facets with AND', () => {
    const card = {
      work: ['coding', 'security'],
      type: ['agent'],
      invocation: ['interactive', 'background'],
      supervision: ['outcome-review'],
    };
    const none = toSelection([]);
    expect(matchesFacets(card, none)).toBe(true);
    expect(matchesFacets(card, { ...none, work: ['security'] })).toBe(true);
    expect(matchesFacets(card, { ...none, work: ['support', 'security'] })).toBe(true);
    expect(matchesFacets(card, { ...none, work: ['support'] })).toBe(false);
    expect(matchesFacets(card, { ...none, work: ['coding'], type: ['platform'] })).toBe(false);
    expect(matchesFacets(card, { ...none, type: ['agent'], invocation: ['background'] })).toBe(true);
    expect(matchesFacets(card, { ...none, type: ['agent'], invocation: ['scheduled'] })).toBe(false);
    expect(matchesFacets(card, { ...none, work: ['coding'], supervision: ['outcome-review'] })).toBe(true);
  });

  it('groups selected terms by facet in selection order', () => {
    const selected = [
      findTerm('supervision', 'exception-only', vocabulary)!,
      findTerm('work', 'security', vocabulary)!,
      findTerm('work', 'coding', vocabulary)!,
    ];
    expect(toSelection(selected)).toEqual({
      work: ['security', 'coding'],
      type: [],
      invocation: [],
      supervision: ['exception-only'],
    });
  });

  it('finds every card of the catalog through its own facet values', () => {
    for (const card of cards) {
      const facets = {
        work: card.domains.map((domain) => domain.id),
        type: [card.approachType],
        invocation: card.invocation.map((mode) => mode.id),
        supervision: card.boundaries.map((boundary) => boundary.id),
      };
      const selection = toSelection([
        findTerm('type', card.approachType, vocabulary)!,
        ...(card.boundaries.length ? [findTerm('supervision', card.boundaries[0]!.id, vocabulary)!] : []),
      ]);
      expect(matchesFacets(facets, selection)).toBe(true);
    }
  });
});
