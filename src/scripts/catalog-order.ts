// ABOUTME: Sorts the directory cards and the palette items, bookmarked first, then well documented or A–Z.
// ABOUTME: The HTML already holds the default order; the URL keeps the A–Z choice as ?sort=az.

import { readBookmarks, toggled, writeBookmarks } from './bookmarks';

export type CatalogOrder = 'documented' | 'az';

/** The query parameter that holds a choice other than the default. */
export const ORDER_PARAM = 'sort';

/** The order a URL asks for. Anything but `sort=az` gives the default. */
export function orderFromSearch(search: string): CatalogOrder {
  return new URLSearchParams(search).get(ORDER_PARAM) === 'az' ? 'az' : 'documented';
}

/** The query string of a URL with the order written in, keeping its other parameters. */
export function searchWithOrder(search: string, order: CatalogOrder): string {
  const params = new URLSearchParams(search);
  if (order === 'az') params.set(ORDER_PARAM, 'az');
  else params.delete(ORDER_PARAM);
  const text = params.toString();
  return text ? `?${text}` : '';
}

export interface OrderKey {
  readonly bookmarked: boolean;
  readonly wellDocumented: boolean;
  readonly alphabeticalRank: number;
}

/**
 * Compare two items in the given order. Bookmarked items come first in either
 * order. The default then puts well-documented items first, then A–Z.
 */
export function compareOrder(order: CatalogOrder, a: OrderKey, b: OrderKey): number {
  if (a.bookmarked !== b.bookmarked) return a.bookmarked ? -1 : 1;
  if (order === 'documented' && a.wellDocumented !== b.wellDocumented) return a.wellDocumented ? -1 : 1;
  return a.alphabeticalRank - b.alphabeticalRank;
}

function orderKey(element: HTMLElement, bookmarks: ReadonlySet<string>): OrderKey {
  return {
    // A card names its record by its approach id. A palette item cannot, as
    // that attribute marks the one card of each record, so it has its own.
    bookmarked: bookmarks.has(element.dataset.approachId ?? element.dataset.bookmarkId ?? ''),
    wellDocumented: element.dataset.wellDocumented === 'true',
    alphabeticalRank: Number(element.dataset.alphabeticalRank),
  };
}

/** Move the sortable children of a container into the order. Other children stay in front. */
function sortChildren(container: Element, order: CatalogOrder, bookmarks: ReadonlySet<string>): void {
  const items = [...container.children].filter(
    (child): child is HTMLElement => child instanceof HTMLElement && child.dataset.alphabeticalRank !== undefined,
  );
  items.sort((a, b) => compareOrder(order, orderKey(a, bookmarks), orderKey(b, bookmarks)));
  for (const item of items) container.append(item);
}

/** The lists whose items carry an order, on the page on show. */
function sortedLists(): Element[] {
  return [
    ...document.querySelectorAll('.entries'),
    ...document.querySelectorAll('.palette-group[data-group="catalog"] ul, .palette-group[data-group="infrastructure"] ul'),
  ];
}

function show(order: CatalogOrder): void {
  const bookmarks = readBookmarks();
  for (const list of sortedLists()) sortChildren(list, order, bookmarks);
  for (const ribbon of document.querySelectorAll<HTMLButtonElement>('[data-bookmark]')) {
    ribbon.setAttribute('aria-pressed', String(bookmarks.has(ribbon.dataset.bookmark ?? '')));
  }
  for (const option of document.querySelectorAll<HTMLButtonElement>('[data-sort-option]')) {
    option.setAttribute('aria-pressed', String(option.dataset.sortOption === order));
  }
  document.getElementById('palette')?.dispatchEvent(new CustomEvent('catalog-order'));
}

/**
 * Wire the sort controls of the page on show. A page with a directory keeps
 * the choice in its URL, so a link opens the same order. Without this script
 * the controls and the bookmark ribbons stay hidden and the default order stands.
 */
export function startCatalogOrder(): void {
  const directory = document.querySelector('.entries');
  let order = orderFromSearch(location.search);
  show(order);
  for (const ribbon of document.querySelectorAll<HTMLButtonElement>('[data-bookmark]')) {
    ribbon.hidden = false;
    ribbon.addEventListener('click', () => {
      writeBookmarks(toggled(readBookmarks(), ribbon.dataset.bookmark ?? ''));
      show(order);
    });
  }
  for (const option of document.querySelectorAll<HTMLButtonElement>('[data-sort-option]')) {
    option.addEventListener('click', () => {
      order = option.dataset.sortOption === 'az' ? 'az' : 'documented';
      if (directory) {
        history.replaceState(history.state, '', `${location.pathname}${searchWithOrder(location.search, order)}${location.hash}`);
      }
      show(order);
    });
  }
}
