// ABOUTME: Opens the navigation over the page on a screen too narrow for a column.
// ABOUTME: Without this the links are still in the page; they simply always show.

import { animate } from 'motion';

/** How long the menu takes to arrive, and to leave. */
const OPEN_SECONDS = 0.24;
const EASE = [0.22, 1, 0.36, 1] as const;

/** Readers who ask for less motion get the menu without the arrival. */
function reducedMotion(): boolean {
  return typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Whichever menu is on the page now, so one listener can serve every page. */
let live: { close: () => void } | null = null;
let claimed = false;

/** Wire the menu of the page on show. */
export function startNavMenu(): void {
  const toggle = document.querySelector<HTMLButtonElement>('.nav-toggle');
  const menu = document.getElementById('mobile-nav');
  if (!toggle || !menu) return;

  let moving: { stop: () => void } | undefined;

  const set = (open: boolean, animated = true): void => {
    toggle.setAttribute('aria-expanded', String(open));
    /*
     * A wide screen has no menu to shut: the element this moves is the sidebar
     * itself, standing in its column. Closing what is already closed would
     * still fade it, so the menu answers only for the menu that is open.
     */
    if (!open && !menu.classList.contains('is-open')) return;
    moving?.stop();
    if (!animated || reducedMotion()) {
      menu.classList.toggle('is-open', open);
      menu.style.removeProperty('opacity');
      menu.style.removeProperty('filter');
      return;
    }
    // Opening shows the menu first so it has something to come into focus from.
    if (open) menu.classList.add('is-open');
    const run = animate(
      menu,
      open
        ? { opacity: [0, 1], filter: ['blur(8px)', 'blur(0px)'] }
        : { opacity: [1, 0], filter: ['blur(0px)', 'blur(8px)'] },
      { duration: OPEN_SECONDS, ease: EASE },
    );
    moving = run;
    const rest = (): void => {
      menu.classList.toggle('is-open', open);
      menu.style.removeProperty('opacity');
      menu.style.removeProperty('filter');
    };
    run.finished.then(rest, rest);
    setTimeout(rest, OPEN_SECONDS * 1000 + 80);
  };
  // A new page arrives closed, whatever the last one was doing.
  set(false, false);

  toggle.addEventListener('click', () => {
    set(toggle.getAttribute('aria-expanded') !== 'true');
  });
  // Following a link is an answer, so the menu that offered it stands down.
  menu.addEventListener('click', (event) => {
    if (event.target instanceof Element && event.target.closest('a')) set(false);
  });

  live = { close: () => set(false) };
  if (claimed) return;
  claimed = true;
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') live?.close();
  });
}
