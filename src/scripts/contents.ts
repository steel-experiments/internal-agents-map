// ABOUTME: Builds the table of contents from the sections the page already has.
// ABOUTME: It marks the entries whose sections are in view, so the rail follows the reading.

/**
 * One entry of the rail. A page built from sections gives one element to watch;
 * a page built from headings gives the heading and the content under it, so the
 * entry stays lit for as long as any of it is on screen.
 */
interface Entry {
  readonly item: HTMLLIElement;
  readonly targets: readonly Element[];
}

/** The words a heading carries, trimmed to one line. */
function headingText(node: Element): string | null {
  const label = (node.textContent ?? '').replace(/\s+/g, ' ').trim();
  return label === '' ? null : label;
}

/** A heading and everything under it, up to the next heading of its rank. */
function region(node: Element): Element[] {
  const targets: Element[] = [node];
  let next = node.nextElementSibling;
  while (next && next.tagName !== 'H2') {
    targets.push(next);
    next = next.nextElementSibling;
  }
  return targets;
}

/** The heading that names a section, if it has one. */
function heading(section: Element): string | null {
  const labelled = section.getAttribute('aria-labelledby');
  const named = labelled ? document.getElementById(labelled) : null;
  const text = (named ?? section.querySelector('h2'))?.textContent ?? '';
  const label = text.replace(/\s+/g, ' ').trim();
  return label === '' ? null : label;
}

/** Build the rail, and keep it in step with what the reader can see. */
/** The observer of the page on show, stopped when the next page builds. */
let watching: IntersectionObserver | undefined;

export function startContents(): void {
  watching?.disconnect();
  watching = undefined;
  const rail = document.getElementById('contents');
  const main = document.getElementById('main');
  if (!(rail instanceof HTMLElement) || !main) return;

  rail.replaceChildren();
  rail.hidden = true;

  const list = document.createElement('ul');
  const entries: Entry[] = [];
  for (const node of main.querySelectorAll('section[id], h2[id]')) {
    // A heading inside a section is already spoken for by the section itself.
    if (node.tagName === 'H2' && node.closest('section[id]') !== null) continue;
    // A section that holds sections is their container: its own entries stand
    // in the rail, and it does not.
    if (node.tagName === 'SECTION' && node.querySelector('section[id]') !== null) continue;
    const label = node.tagName === 'H2' ? headingText(node) : heading(node);
    if (!label) continue;
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = `#${node.id}`;
    link.textContent = label;
    item.append(link);
    list.append(item);
    entries.push({ item, targets: node.tagName === 'H2' ? region(node) : [node] });
  }
  // A page with one section has nothing to navigate.
  if (entries.length < 2) return;

  const title = document.createElement('p');
  title.className = 'contents-title';
  title.textContent = 'Table of Contents';
  rail.append(title, list);
  rail.hidden = false;

  const seen = new Set<Element>();
  const observer = new IntersectionObserver(
    (records) => {
      for (const record of records) {
        if (record.isIntersecting) seen.add(record.target);
        else seen.delete(record.target);
      }
      for (const entry of entries) {
        const lit = entry.targets.some((target) => seen.has(target));
        entry.item.classList.toggle('is-visible', lit);
      }
    },
    // A sliver of a section counts, so the rail never goes blank between two.
    { rootMargin: '-8% 0px -8% 0px', threshold: 0 },
  );
  for (const entry of entries) for (const target of entry.targets) observer.observe(target);
  watching = observer;
}
