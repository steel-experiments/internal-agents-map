// ABOUTME: Puts the sidebar's dot beside the link for the page being read.
// ABOUTME: Without this the sidebar still names the page; it simply has no dot.

/** Whether the width is already watched, so one listener serves every page. */
let watching = false;

/*
 * The dot is the one part of the navigation that stands somewhere else on the
 * next page. Under a single name the page change pairs it with itself and
 * holds both halves on screen for as long as the change takes: the dot of the
 * page being left, and the dot of the page arriving. So the two are named
 * apart. Each is then captured on its own, and the stylesheet takes one out
 * before it brings the other in.
 */
const LEAVING = 'nav-dot-out';
const ARRIVING = 'nav-dot-in';

/** Put the dot beside the current page's link, wherever that link is. */
function place(): HTMLElement | null {
  const nav = document.querySelector<HTMLElement>('.nav-links');
  const dot = nav?.querySelector<HTMLElement>('.nav-dot');
  const current = nav?.querySelector<HTMLElement>('a[aria-current="page"]');
  if (!nav || !dot) return null;
  if (!current) {
    dot.hidden = true;
    return dot;
  }

  dot.hidden = false;
  dot.style.top = `${current.offsetTop + current.offsetHeight / 2}px`;
  return dot;
}

/** Place the dot, and place it again when the column it measures returns. */
export function startNavDot(): void {
  place();
  if (watching) return;
  watching = true;
  // A narrow screen does not lay the column out, so it measures nothing to use.
  addEventListener('resize', place);
  /*
   * Each name is given while the page it belongs to is still the page on
   * screen: the one being left is captured after the first of these events,
   * the one arriving after the second. A name set any later is too late to be
   * the name it is captured under.
   */
  document.addEventListener('astro:before-preparation', () => {
    const dot = document.querySelector<HTMLElement>('.nav-links .nav-dot');
    if (dot) dot.style.viewTransitionName = LEAVING;
  });
  document.addEventListener('astro:after-swap', () => {
    const dot = place();
    if (dot) dot.style.viewTransitionName = ARRIVING;
  });
}
