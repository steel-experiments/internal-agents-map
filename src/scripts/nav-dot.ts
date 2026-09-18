// ABOUTME: Puts the sidebar's dot beside the link for the page being read.
// ABOUTME: Without this the sidebar still names the page; it simply has no dot.

/** Whether the width is already watched, so one listener serves every page. */
let watching = false;

/** Put the dot beside the current page's link, wherever that link is. */
function place(): void {
  const nav = document.querySelector<HTMLElement>('.nav-links');
  const dot = nav?.querySelector<HTMLElement>('.nav-dot');
  const current = nav?.querySelector<HTMLElement>('a[aria-current="page"]');
  if (!nav || !dot) return;
  if (!current) {
    dot.hidden = true;
    return;
  }

  dot.hidden = false;
  dot.style.top = `${current.offsetTop + current.offsetHeight / 2}px`;
}

/** Place the dot, and place it again when the column it measures returns. */
export function startNavDot(): void {
  place();
  if (watching) return;
  watching = true;
  // A narrow screen does not lay the column out, so it measures nothing to use.
  addEventListener('resize', place);
}
