// ABOUTME: Opens the command palette and narrows its items by text and by facet.
// ABOUTME: Every item is already a link, so without this script the page still reaches them all.

import { animate } from 'motion';

/** How long the palette takes to arrive, and to leave. */
const OPEN_SECONDS = 0.26;
const SHUT_SECONDS = 0.14;
/** The page's own ease-out. */
const EASE = [0.22, 1, 0.36, 1] as const;

/** The facets the pills filter by, in the order the palette lists them. */
const FACETS = ['group', 'work', 'type', 'invocation', 'supervision'] as const;
type Facet = (typeof FACETS)[number];

/** How many of each kind the palette shows before the reader has asked for anything. */
const RESTING_LIMIT = 6;

/** Readers who ask for less motion get the palette without the arrival. */
function reducedMotion(): boolean {
  return typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Blur the bar out of the way, or back into it.
 * The bar is centred by a transform of its own, so only its opacity and its
 * focus move: touching the transform would slide it sideways as it went.
 */
const fading = new WeakMap<HTMLElement, { stop: () => void }>();

const fadeVersions = new WeakMap<HTMLElement, object>();

function fadeBar(bar: HTMLElement, show: boolean, delay = 0): void {
  const version = {};
  fadeVersions.set(bar, version);
  fading.get(bar)?.stop();
  const rest = (): void => {
    if (fadeVersions.get(bar) !== version) return;
    bar.style.opacity = show ? '' : '0';
    bar.style.removeProperty('filter');
    bar.style.pointerEvents = show ? '' : 'none';
  };
  if (reducedMotion()) {
    rest();
    return;
  }
  if (show) bar.style.pointerEvents = '';
  const run = animate(
    bar,
    show
      ? { opacity: [0, 1], filter: ['blur(6px)', 'blur(0px)'] }
      : { opacity: [1, 0], filter: ['blur(0px)', 'blur(6px)'] },
    { duration: OPEN_SECONDS, ease: EASE, delay },
  );
  fading.set(bar, run);
  run.finished.then(rest, rest);
  setTimeout(rest, (OPEN_SECONDS + delay) * 1000 + 80);
}

/**
 * Bring one block in: out of focus and slightly low, to sharp and in place.
 * The blur is on the contents, never on the panel, whose own backdrop filter
 * would stop working the moment it became a containing block.
 */
function bringIn(element: Element, delay = 0): void {
  if (reducedMotion()) return;
  const done = (): void => {
    (element as HTMLElement).style.removeProperty('filter');
    (element as HTMLElement).style.removeProperty('transform');
    (element as HTMLElement).style.removeProperty('opacity');
  };
  const run = animate(
    element,
    { opacity: [0, 1], filter: ['blur(6px)', 'blur(0px)'], transform: ['translateY(6px)', 'translateY(0px)'] },
    { duration: OPEN_SECONDS, ease: EASE, delay },
  );
  run.finished.then(done, done);
  setTimeout(done, (OPEN_SECONDS + delay) * 1000 + 80);
}

/** Lower case, single spaces, no edges: the form the items were indexed in. */
function normalize(value: string): string {
  return value.toLowerCase().replace(/\s+/g, ' ').trim();
}

/**
 * The palette of the page on show. The document keeps its listeners across a
 * swap, so the shortcut is claimed once and always acts on the current one.
 */
let live: { open: () => void; close: () => void; isOpen: () => boolean } | null = null;
let shortcutClaimed = false;
const initialized = new WeakSet<HTMLElement>();

/** Start the palette. Without it the shortcut does nothing and the items stay reachable. */
export function startPalette(): void {
  const palette = document.getElementById('palette');
  const input = document.getElementById('palette-input');
  if (!palette || !(input instanceof HTMLInputElement) || initialized.has(palette)) return;
  initialized.add(palette);

  const shortcut = document.getElementById('search-shortcut');
  // The badge reads ⌘ K in the HTML, so only a platform without one changes it.
  if (shortcut && !/Mac|iPhone|iPad|iPod/.test(navigator.platform)) shortcut.textContent = 'Ctrl K';
  const items = [...palette.querySelectorAll<HTMLAnchorElement>('.palette-item')];
  const groups = [...palette.querySelectorAll<HTMLElement>('.palette-group')];
  const empty = palette.querySelector<HTMLElement>('.palette-empty');
  /** The values chosen in each pill. A facet with none chosen filters nothing. */
  const chosen: Record<Facet, Set<string>> = {
    group: new Set(),
    work: new Set(),
    type: new Set(),
    invocation: new Set(),
    supervision: new Set(),
  };
  /** Where focus was before the palette opened, so closing gives it back. */
  let opener: Element | null = null;
  let active = -1;

  /** The items still on show, in document order. */
  const shown = (): HTMLAnchorElement[] => items.filter((item) => !item.hidden);

  const point = (next: number): void => {
    const list = shown();
    for (const item of list) item.setAttribute('aria-selected', 'false');
    active = list.length === 0 ? -1 : (next + list.length) % list.length;
    const item = list[active];
    if (!item) return;
    item.setAttribute('aria-selected', 'true');
    item.scrollIntoView({ block: 'nearest' });
  };

  /** An item shows when the text matches and every chosen facet is satisfied. */
  const matches = (item: HTMLAnchorElement, query: string): boolean => {
    if (query && !(item.dataset.search ?? '').includes(query)) return false;
    for (const facet of FACETS) {
      const wanted = chosen[facet];
      if (wanted.size === 0) continue;
      const carried = (item.dataset[facet] ?? '').split(' ').filter(Boolean);
      if (!carried.some((value) => wanted.has(value))) return false;
    }
    return true;
  };

  /** True once the reader has narrowed the palette, by typing or by a pill. */
  const narrowed = (query: string): boolean =>
    query.length > 0 || FACETS.some((facet) => chosen[facet].size > 0);

  const apply = (settle = false): void => {
    const query = normalize(input.value);
    const asked = narrowed(query);
    const before = results ? results.getBoundingClientRect().height : 0;
    let total = 0;
    for (const group of groups) {
      // At rest each kind shows a handful; asking for something lifts the cap.
      let kept = 0;
      for (const item of group.querySelectorAll<HTMLAnchorElement>('.palette-item')) {
        const fits = matches(item, query) && (asked || kept < RESTING_LIMIT);
        item.hidden = !fits;
        if (fits) kept += 1;
      }
      // A group with nothing left says nothing, rather than leaving a bare heading.
      group.hidden = kept === 0;
      total += kept;
    }
    if (empty) empty.hidden = total > 0;
    point(0);
    if (settle && results && !reducedMotion()) {
      const after = results.getBoundingClientRect().height;
      if (Math.abs(after - before) > 1) {
        const clear = (): void => { results.style.removeProperty('height'); };
        const run = animate(
          results,
          { height: [`${before}px`, `${after}px`] },
          { duration: OPEN_SECONDS, ease: EASE },
        );
        run.finished.then(clear, clear);
        setTimeout(clear, OPEN_SECONDS * 1000 + 80);
      }
    }
  };

  /** The bars that open the palette: the directory's own box, or the launcher. */
  const bars = [...document.querySelectorAll<HTMLElement>('#filters, .search-launcher')];
  const panel = palette.querySelector<HTMLElement>('.palette-panel');
  const scrim = palette.querySelector<HTMLElement>('.palette-scrim');
  const search = palette.querySelector<HTMLElement>('.palette-search');
  const filters = palette.querySelector<HTMLElement>('.palette-filters');
  const results = palette.querySelector<HTMLElement>('.palette-results');

  const settle = (): void => {
    palette.hidden = true;
    // Back in the place it left, never shifted by a transform of its own.
    for (const bar of bars) fadeBar(bar, true);
    if (opener instanceof HTMLElement) opener.focus();
  };

  /** The closing animation, stopped if the palette opens again before its fill is gone. */
  let leaving: { stop: () => void; finished: Promise<unknown> } | undefined;

  let transition = 0;
  /** True while a close is still running, when the palette is neither open nor shut. */
  let closing = false;
  const close = (): void => {
    if (palette.hidden || closing) return;
    const version = ++transition;
    closing = true;
    closeMenus();
    // Going is not applying: a sheet left open takes its staged choices with it.
    dropSheet();
    if (reducedMotion() || !panel) {
      closing = false;
      settle();
      return;
    }
    leaving = animate(
      palette,
      { opacity: [1, 0] },
      { duration: SHUT_SECONDS, ease: EASE },
    );
    let ended = false;
    const done = (): void => {
      if (ended || version !== transition) return;
      ended = true;
      closing = false;
      leaving?.stop();
      palette.style.removeProperty('opacity');
      settle();
    };
    leaving.finished.then(done, done);
    setTimeout(done, SHUT_SECONDS * 1000 + 60);
  };

  const open = (): void => {
    // A palette still closing is on its way out, not open: it reopens from there.
    if (!palette.hidden && !closing) return;
    transition += 1;
    closing = false;
    // A finished close keeps its fill on the palette and would hide this open.
    leaving?.stop();
    palette.style.removeProperty('opacity');
    opener = document.activeElement;
    palette.hidden = false;
    sheet(false);
    apply();
    input.focus();
    input.select();
    // The bar goes as the palette comes: one exchange, not two steps.
    for (const bar of bars) fadeBar(bar, false);
    if (scrim) bringIn(scrim);
    if (panel) bringIn(panel);
    if (search) bringIn(search, 0.04);
    if (filters) bringIn(filters, 0.07);
    if (results) bringIn(results, 0.1);
  };

  /** Close whichever pill is open, optionally leaving one alone. */
  const closeMenus = (except?: Element): void => {
    for (const facet of palette.querySelectorAll<HTMLElement>('.palette-facet')) {
      if (facet === except) continue;
      facet.querySelector('.palette-pill')?.setAttribute('aria-expanded', 'false');
      const menu = facet.querySelector<HTMLElement>('.palette-menu');
      if (menu) menu.hidden = true;
    }
  };

  for (const facet of palette.querySelectorAll<HTMLElement>('.palette-facet')) {
    const key = facet.dataset.facet as Facet | undefined;
    const pill = facet.querySelector<HTMLButtonElement>('.palette-pill');
    const menu = facet.querySelector<HTMLElement>('.palette-menu');
    const count = facet.querySelector<HTMLElement>('.palette-pill-count');
    if (!key || !pill || !menu) continue;

    pill.addEventListener('click', () => {
      const opening = menu.hidden;
      closeMenus(facet);
      menu.hidden = !opening;
      pill.setAttribute('aria-expanded', String(opening));
      if (opening) {
        // A menu near the right edge hangs from that edge rather than past it.
        menu.style.removeProperty('right');
        menu.style.removeProperty('left');
        const room = palette.querySelector('.palette-panel')?.getBoundingClientRect();
        if (room && menu.getBoundingClientRect().right > room.right) {
          menu.style.left = 'auto';
          menu.style.right = '0';
        }
        bringIn(menu);
      }
    });

    for (const option of menu.querySelectorAll<HTMLButtonElement>('.palette-option')) {
      option.addEventListener('click', () => {
        const value = option.dataset.value ?? '';
        // A second press clears the value, so a facet can always return to none.
        if (chosen[key].has(value)) chosen[key].delete(value);
        else chosen[key].add(value);
        option.setAttribute('aria-pressed', String(chosen[key].has(value)));
        pill.classList.toggle('is-on', chosen[key].size > 0);
        if (count) {
          count.textContent = String(chosen[key].size);
          count.hidden = chosen[key].size === 0;
        }
        // Behind the sheet the choices are only staged, so the list waits.
        if (!staged) apply(true);
        settleApply();
      });
    }
  }

  /*
   * On a phone the filters are a sheet: what is chosen there is staged against
   * the values the sheet opened with, applied by its Apply and dropped by its
   * Go back. Elsewhere there is no sheet, so a choice still lands at once.
   */
  const apply_ = palette.querySelector<HTMLButtonElement>('.palette-apply');
  let staged: Record<Facet, string[]> | null = null;

  /** Whether the staged choices differ from the ones the sheet opened with. */
  const edited = (): boolean => {
    const opened = staged;
    if (!opened) return false;
    return FACETS.some(
      (facet) =>
        chosen[facet].size !== opened[facet].length ||
        opened[facet].some((value) => !chosen[facet].has(value)),
    );
  };

  /** Apply commits: it waits for something to commit. */
  const settleApply = (): void => {
    if (apply_) apply_.disabled = !(FACETS.some((facet) => chosen[facet].size > 0) || edited());
  };

  /** Draw every pill and option from the values now chosen. */
  const drawFacets = (): void => {
    for (const facet of palette.querySelectorAll<HTMLElement>('.palette-facet')) {
      const key = facet.dataset.facet as Facet | undefined;
      if (!key) continue;
      const count = facet.querySelector<HTMLElement>('.palette-pill-count');
      facet.querySelector('.palette-pill')?.classList.toggle('is-on', chosen[key].size > 0);
      if (count) {
        count.textContent = String(chosen[key].size);
        count.hidden = chosen[key].size === 0;
      }
      for (const option of facet.querySelectorAll<HTMLButtonElement>('.palette-option')) {
        option.setAttribute('aria-pressed', String(chosen[key].has(option.dataset.value ?? '')));
      }
    }
    settleApply();
  };

  const sheet = (open: boolean): void => {
    filters?.classList.toggle('is-open', open);
    staged = open
      ? (Object.fromEntries(FACETS.map((facet) => [facet, [...chosen[facet]]])) as Record<Facet, string[]>)
      : null;
    if (!open) closeMenus();
    settleApply();
  };
  palette.querySelector('.palette-filter-open')?.addEventListener('click', () => sheet(true));
  apply_?.addEventListener('click', () => {
    sheet(false);
    apply(true);
  });
  /** Leave the sheet as it was found: its choices never reached the list. */
  function dropSheet(): void {
    if (!staged) return;
    for (const facet of FACETS) chosen[facet] = new Set(staged[facet]);
    sheet(false);
    drawFacets();
  }
  palette.querySelector('.palette-back')?.addEventListener('click', dropSheet);

  input.addEventListener('input', () => apply());
  input.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowDown') { event.preventDefault(); point(active + 1); }
    else if (event.key === 'ArrowUp') { event.preventDefault(); point(active - 1); }
    else if (event.key === 'Enter') {
      const item = shown()[active];
      if (item) { event.preventDefault(); item.click(); }
    }
  });

  for (const dismiss of palette.querySelectorAll('[data-palette-dismiss]')) {
    dismiss.addEventListener('click', close);
    // The page behind holds still without hiding its overflow, which would drop
    // every sticky element back to where it would sit on an unscrolled page.
    dismiss.addEventListener('wheel', (event) => event.preventDefault(), { passive: false });
    dismiss.addEventListener('touchmove', (event) => event.preventDefault(), { passive: false });
  }
  palette.addEventListener('click', (event) => {
    if (event.target instanceof Element && !event.target.closest('.palette-facet')) closeMenus();
  });

  live = { open, close, isOpen: () => !palette.hidden };
  if (!shortcutClaimed) {
    shortcutClaimed = true;
    document.addEventListener('keydown', (event) => {
      if (!live) return;
      if (event.key === 'Escape' && live.isOpen()) { event.preventDefault(); live.close(); return; }
      if (
        event.defaultPrevented || event.isComposing || event.repeat ||
        event.altKey || event.shiftKey || event.metaKey === event.ctrlKey ||
        event.key.toLowerCase() !== 'k'
      ) return;
      event.preventDefault();
      live.open();
    });
  }

  // A phone has no shortcut key, so the whole box is the door, not its hint.
  const narrow = (): boolean =>
    typeof matchMedia === 'function' && matchMedia('(max-width: 800px)').matches;
  for (const box of document.querySelectorAll<HTMLElement>('.search-box')) {
    // Taking the press keeps the field from focusing and the keyboard from rising.
    box.addEventListener('pointerdown', (event) => { if (narrow()) event.preventDefault(); });
    box.addEventListener('click', (event) => {
      if (!narrow()) return;
      event.preventDefault();
      open();
    });
  }

  // The directory's own search box is the palette's other door.
  for (const trigger of document.querySelectorAll<HTMLElement>('[data-palette-open]')) {
    // Open after the full click so a touch cannot land on the arriving scrim.
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      open();
    });
  }
  apply();
}
