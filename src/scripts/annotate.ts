// ABOUTME: Mounts the Agentation annotation toolbar into a host element of its own.
// ABOUTME: Explicitly opted-in development injects this; production never bundles it.

import { createElement } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { Agentation } from 'agentation';

/** The id of the element the toolbar renders into, so a reload reuses it. */
const HOST_ID = 'agentation-host';

/** The toolbar's root and the element it renders into, kept across page changes. */
let root: Root | null = null;
let host: HTMLElement | null = null;

/**
 * The toolbar's own styles, by id. Its modules put these in the head as they
 * are first needed, and a page change drops them; the toolbar does not put
 * them back, so they are kept here and restored on the page that arrives.
 */
const kept = new Map<string, string>();

/** Watches the head for the styles the toolbar injects as it goes. */
const watcher = new MutationObserver(() => remember());

/**
 * The style elements the toolbar's modules put in the head. They carry an id
 * and nothing else; the site's own styles are the ones the dev server marks.
 */
function toolbarStyles(): HTMLStyleElement[] {
  return [...document.querySelectorAll<HTMLStyleElement>('head > style[id]')].filter(
    (style) => style.dataset.viteDevId === undefined,
  );
}

/** Take a copy of whatever the toolbar has injected by now. */
function remember(): void {
  for (const style of toolbarStyles()) kept.set(style.id, style.textContent ?? '');
}

/** Put back every remembered style the current head is missing. */
function restore(): void {
  for (const [id, css] of kept) {
    if (document.getElementById(id)) continue;
    const style = document.createElement('style');
    style.id = id;
    style.textContent = css;
    document.head.append(style);
  }
}

/** Put the toolbar on the page, unless the one already there is still standing. */
function mount(): void {
  restore();
  if (host?.isConnected) return;
  root?.unmount();
  host = document.createElement('div');
  host.id = HOST_ID;
  document.body.append(host);
  root = createRoot(host);
  root.render(createElement(Agentation));
  // The head is swapped whole, so the watcher follows the one now in place.
  watcher.disconnect();
  watcher.observe(document.head, { childList: true });
}

/** Show the toolbar, and keep showing it as the reader moves between pages. */
export function startAnnotating(): void {
  mount();
  /*
   * A page change swaps the head the toolbar's styles were injected into and
   * the body it was mounted on. The styles go with the arriving document where
   * they can, are put back where they cannot, and the toolbar mounts again.
   */
  document.addEventListener('astro:before-swap', (event) => {
    remember();
    const { newDocument } = event as unknown as { newDocument: Document };
    for (const style of toolbarStyles()) newDocument.head.append(style.cloneNode(true));
  });
  document.addEventListener('astro:page-load', mount);
}
