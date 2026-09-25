// ABOUTME: Opens the closed disclosure that holds the target of an in-page link.
// ABOUTME: A chart marker links to its note, and the note must be visible when the page arrives.

/** Open every closed disclosure around the element with this fragment. */
function reveal(hash: string): void {
  if (hash.length < 2) return;
  let node = document.getElementById(decodeURIComponent(hash.slice(1)))?.parentElement ?? null;
  while (node) {
    if (node instanceof HTMLDetailsElement && !node.open) node.open = true;
    node = node.parentElement;
  }
}

let started = false;

/** Reveal the target of the current address and of each in-page link a reader follows. */
export function startOpenTargets(): void {
  reveal(location.hash);
  if (started) return;
  started = true;
  // A second click on the same link changes no fragment, so the click opens the note too.
  document.addEventListener('click', (event) => {
    const link = (event.target as Element | null)?.closest?.('a[href^="#"]');
    if (link) reveal(link.getAttribute('href') ?? '');
  });
  addEventListener('hashchange', () => reveal(location.hash));
}
