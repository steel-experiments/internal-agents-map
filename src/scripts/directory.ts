// ABOUTME: Resolves the old homepage fragment links to the entry pages they name.
// ABOUTME: Every card and every entry link is already in the HTML; nothing here hides one.

import { entryPath } from '../lib/routes';

/** A claim anchor: `claim-<approach-id>--<field-path>`. */
const CLAIM_FRAGMENT = /^claim-([a-z0-9-]+)--([a-z0-9-]+)$/;
/** A source anchor: `source-<source-id>`. The card of its entry lists the source id. */
const SOURCE_FRAGMENT = /^source-([a-z0-9-]+)$/;
/** An approach identifier on its own. */
const APPROACH_FRAGMENT = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/** The resolver of the page on show, rebuilt whenever the router swaps one in. */
let live: (() => void) | null = null;
/** Whether the listener is in place, so the one listener serves every page. */
let claimed = false;

/** The identifiers of the implementations this page carries, one per card. */
function approachIds(cards: readonly HTMLElement[]): ReadonlySet<string> {
  return new Set(cards.map((card) => card.dataset.approachId ?? ''));
}

/** The entry of every source identifier the cards list. */
function sourceOwners(cards: readonly HTMLElement[]): ReadonlyMap<string, string> {
  const owners = new Map<string, string>();
  for (const card of cards) {
    const approach = card.dataset.approachId ?? '';
    for (const id of (card.dataset.sourceIds ?? '').split(' ')) if (id) owners.set(id, approach);
  }
  return owners;
}

/**
 * Find the entry page an old homepage fragment belongs to.
 * The path comes from the route helper and a known identifier. The anchor is
 * rebuilt from the matched parts, so no text of the fragment reaches the URL raw.
 */
export function legacyTarget(
  hash: string,
  ids: ReadonlySet<string>,
  sources: ReadonlyMap<string, string>,
): string | null {
  let fragment: string;
  try {
    fragment = decodeURIComponent(hash.replace(/^#/, ''));
  } catch {
    return null;
  }
  if (!fragment) return null;
  const claim = CLAIM_FRAGMENT.exec(fragment);
  if (claim && ids.has(claim[1]!)) {
    return `${entryPath(claim[1]!)}#claim-${claim[1]!}--${claim[2]!}`;
  }
  const source = SOURCE_FRAGMENT.exec(fragment);
  const owner = source ? sources.get(source[1]!) : undefined;
  if (source && owner && ids.has(owner)) {
    return `${entryPath(owner)}#source-${source[1]!}`;
  }
  if (APPROACH_FRAGMENT.test(fragment) && ids.has(fragment)) return entryPath(fragment);
  return null;
}

/**
 * Send an old fragment link on to the page that now holds what it named, on
 * arrival and whenever one is followed from within the page. The search that
 * once lived here is the command palette's; the cards below are all of them.
 */
export function startDirectory(): void {
  const cards = [...document.querySelectorAll<HTMLElement>('.entry[data-approach-id]')];
  if (cards.length === 0) return;
  const ids = approachIds(cards);
  const sources = sourceOwners(cards);

  live = (): void => {
    const target = legacyTarget(location.hash, ids, sources);
    if (target) location.replace(target);
  };
  live();
  if (claimed) return;
  claimed = true;
  // The listener outlives the page that added it, so it asks for the live one.
  addEventListener('hashchange', () => live?.());
}
