// ABOUTME: Checks how the catalog order is read from the URL, written back, and compared.
// ABOUTME: Bookmarked records come first; then featured, then well-documented ones, then A–Z within each group.

import { describe, expect, it } from 'vitest';
import { compareOrder, orderFromSearch, searchWithOrder } from '../../src/scripts/catalog-order';

describe('the catalog order in the URL', () => {
  it('reads A–Z only from sort=az', () => {
    expect(orderFromSearch('?sort=az')).toBe('az');
    expect(orderFromSearch('')).toBe('documented');
    expect(orderFromSearch('?sort=documented')).toBe('documented');
    expect(orderFromSearch('?sort=<script>')).toBe('documented');
  });

  it('writes only the choice that is not the default, and keeps other parameters', () => {
    expect(searchWithOrder('', 'az')).toBe('?sort=az');
    expect(searchWithOrder('?sort=az', 'documented')).toBe('');
    expect(searchWithOrder('?ref=x&sort=az', 'documented')).toBe('?ref=x');
    expect(searchWithOrder('?ref=x', 'az')).toBe('?ref=x&sort=az');
  });
});

describe('the catalog order comparison', () => {
  const items = [
    { id: 'a', bookmarked: false, featured: false, wellDocumented: false, alphabeticalRank: 0 },
    { id: 'b', bookmarked: false, featured: false, wellDocumented: true, alphabeticalRank: 1 },
    { id: 'c', bookmarked: false, featured: false, wellDocumented: false, alphabeticalRank: 2 },
    { id: 'd', bookmarked: false, featured: false, wellDocumented: true, alphabeticalRank: 3 },
  ];
  /** The same items with `c` bookmarked. */
  const marked = items.map((item) => ({ ...item, bookmarked: item.id === 'c' }));

  it('puts well-documented items first, then A–Z', () => {
    const sorted = [...items].sort((x, y) => compareOrder('documented', x, y));
    expect(sorted.map((item) => item.id)).toEqual(['b', 'd', 'a', 'c']);
  });

  it('sorts by the alphabetical rank alone for A–Z', () => {
    const sorted = [...items].reverse().sort((x, y) => compareOrder('az', x, y));
    expect(sorted.map((item) => item.id)).toEqual(['a', 'b', 'c', 'd']);
  });

  it('puts featured items before well-documented ones in the default order only', () => {
    const picked = items.map((item) => ({ ...item, featured: item.id === 'd' }));
    expect([...picked].sort((x, y) => compareOrder('documented', x, y)).map((item) => item.id)).toEqual(['d', 'b', 'a', 'c']);
    expect([...picked].sort((x, y) => compareOrder('az', x, y)).map((item) => item.id)).toEqual(['a', 'b', 'c', 'd']);
  });

  it('puts bookmarked items first in either order', () => {
    expect([...marked].sort((x, y) => compareOrder('documented', x, y)).map((item) => item.id)).toEqual(['c', 'b', 'd', 'a']);
    expect([...marked].sort((x, y) => compareOrder('az', x, y)).map((item) => item.id)).toEqual(['c', 'a', 'b', 'd']);
  });
});
