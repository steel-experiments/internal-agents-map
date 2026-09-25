// ABOUTME: Keeps the records a reader bookmarks, as a list of approach ids in this browser's storage.
// ABOUTME: When storage is absent or blocked, no record is bookmarked and nothing fails.

/** The storage key that holds the bookmarked approach ids as a JSON list. */
const STORAGE_KEY = 'bookmarks';

/** The identifiers in stored text. Text that is not a list of strings gives none. */
export function parseBookmarks(text: string | null): Set<string> {
  try {
    const value: unknown = JSON.parse(text ?? '[]');
    if (!Array.isArray(value)) return new Set();
    return new Set(value.filter((id): id is string => typeof id === 'string'));
  } catch {
    return new Set();
  }
}

/** The set with the identifier added when absent, or removed when present. */
export function toggled(ids: ReadonlySet<string>, id: string): Set<string> {
  const next = new Set(ids);
  if (!next.delete(id)) next.add(id);
  return next;
}

export function readBookmarks(): Set<string> {
  try {
    return parseBookmarks(localStorage.getItem(STORAGE_KEY));
  } catch {
    return new Set();
  }
}

export function writeBookmarks(ids: ReadonlySet<string>): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...ids]));
  } catch {
    // Storage is blocked: the bookmark holds for this page only.
  }
}
