/* Generated asset source: edit templates/site.js, then run scripts/build.py. */
(() => {
  'use strict';
  const form = document.getElementById('filters');
  const catalog = document.getElementById('catalog');
  const list = document.querySelector('.entries');
  const entries = [...document.querySelectorAll('.entry')];
  const controls = Object.fromEntries(['q', 'work', 'type', 'supervision'].map(key => [key, form.elements.namedItem(key)]));
  const results = document.getElementById('results');
  const empty = document.getElementById('empty');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const normalize = value => value.toLowerCase().replace(/\s+/g, ' ').trim();
  let searchTimer;
  // Restart a CSS animation on an element that may already carry the class.
  function replay(element, className) {
    element.classList.remove(className);
    void element.offsetWidth;
    element.classList.add(className);
  }
  // Animate the remaining entries into place when a whole filter changes.
  function reflow(update) {
    if (!document.startViewTransition || reducedMotion.matches) { update(); return; }
    list.classList.add('is-reflowing');
    document.startViewTransition(update).finished.finally(() => list.classList.remove('is-reflowing'));
  }
  function stateFromUrl() {
    const params = new URLSearchParams(location.search);
    for (const [key, control] of Object.entries(controls)) {
      const value = params.get(key) || '';
      control.value = key === 'q' || [...control.options].some(option => option.value === value) ? value : '';
    }
  }
  function matches(entry) {
    return entry.dataset.search.includes(normalize(controls.q.value)) &&
      (!controls.work.value || entry.dataset.work.split(' ').includes(controls.work.value)) &&
      (!controls.type.value || entry.dataset.type === controls.type.value) &&
      (!controls.supervision.value || entry.dataset.supervision.split(' ').includes(controls.supervision.value));
  }
  function apply(announcement = '') {
    let count = 0;
    entries.forEach(entry => { entry.hidden = !matches(entry); if (!entry.hidden) count++; });
    const text = `${announcement}${count} of ${entries.length} approaches`;
    if (results.textContent !== text) { results.textContent = text; replay(results, 'is-ticking'); }
    empty.hidden = count !== 0;
  }
  function writeUrl(method = 'pushState') {
    const url = new URL(location.href);
    if (method === 'pushState' && entries.some(entry => '#' + entry.id === url.hash)) url.hash = '';
    for (const [key, control] of Object.entries(controls)) {
      if (control.value) url.searchParams.set(key, control.value); else url.searchParams.delete(key);
    }
    if (url.href !== location.href) history[method](null, '', url);
  }
  function revealFragment() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const entry = entries.find(item => item.id === id);
    if (!entry) { apply(); return; }
    let changed = false;
    if (!entry.dataset.search.includes(normalize(controls.q.value))) { controls.q.value = ''; changed = true; }
    for (const key of ['work', 'type', 'supervision']) {
      if (controls[key].value && !entry.dataset[key].split(' ').includes(controls[key].value)) {
        controls[key].value = ''; changed = true;
      }
    }
    apply(changed ? 'Conflicting filters reset to show the linked approach. ' : '');
    if (changed) writeUrl('replaceState');
    entry.querySelector('details').open = true;
    entry.scrollIntoView({ block: 'start', behavior: 'instant' });
    replay(entry, 'is-targeted');
  }
  function restore() { clearTimeout(searchTimer); stateFromUrl(); apply(); revealFragment(); }
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(searchTimer); writeUrl(); apply(); });
  controls.q.addEventListener('input', () => {
    clearTimeout(searchTimer); apply();
    searchTimer = setTimeout(() => writeUrl(), 250);
  });
  for (const key of ['work', 'type', 'supervision']) controls[key].addEventListener('change', () => {
    clearTimeout(searchTimer); reflow(() => { writeUrl(); apply(); });
  });
  form.addEventListener('reset', event => {
    event.preventDefault(); clearTimeout(searchTimer);
    Object.values(controls).forEach(control => { control.value = ''; });
    reflow(() => { writeUrl(); apply(); });
  });
  // A work tag applies that Work filter and hands focus to the control that now shows it.
  list.addEventListener('click', event => {
    const tag = event.target.closest('.tag');
    if (!tag) return;
    clearTimeout(searchTimer);
    controls.work.value = tag.dataset.work;
    catalog.scrollIntoView({ block: 'start', behavior: 'instant' });
    reflow(() => { writeUrl(); apply(); });
    controls.work.focus({ preventScroll: true });
  });
  document.querySelectorAll('.permalink').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); clearTimeout(searchTimer);
    const url = new URL(location.href); url.hash = link.hash;
    if (url.href !== location.href) history.pushState(null, '', url);
    revealFragment();
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(url.href).then(() => {
      link.dataset.label ??= link.innerHTML;
      link.textContent = 'Link copied';
      clearTimeout(link.copyTimer);
      link.copyTimer = setTimeout(() => { link.innerHTML = link.dataset.label; }, 2000);
    }, () => {});
  }));
  window.addEventListener('popstate', restore);
  window.addEventListener('hashchange', restore);
  form.hidden = false;
  restore();
})();
