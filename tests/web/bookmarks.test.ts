// ABOUTME: Checks how the bookmarked records are read back from this browser's storage.
// ABOUTME: Text that is not a list of identifiers gives no bookmarks rather than an error.

import { describe, expect, it } from 'vitest';
import { parseBookmarks, toggled } from '../../src/scripts/bookmarks';

describe('the stored bookmarks', () => {
  it('reads a list of identifiers', () => {
    expect([...parseBookmarks('["a","b"]')]).toEqual(['a', 'b']);
  });

  it('gives no bookmarks for empty, broken, or foreign text', () => {
    expect(parseBookmarks(null).size).toBe(0);
    expect(parseBookmarks('{').size).toBe(0);
    expect(parseBookmarks('{"a":1}').size).toBe(0);
    expect([...parseBookmarks('["a",1,null]')]).toEqual(['a']);
  });

  it('adds an identifier that is absent and removes one that is present', () => {
    expect([...toggled(new Set(['a']), 'b')]).toEqual(['a', 'b']);
    expect([...toggled(new Set(['a', 'b']), 'a')]).toEqual(['b']);
  });
});
