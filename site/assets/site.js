/* Generated asset source: edit templates/site.js, then run scripts/build.py. */
(() => {
  'use strict';
  const form = document.getElementById('filters');
  const entries = [...document.querySelectorAll('.entry')];
  const controls = Object.fromEntries(['q', 'work', 'type', 'supervision'].map(key => [key, form.elements.namedItem(key)]));
  const results = document.getElementById('results');
  const empty = document.getElementById('empty');
  const normalize = value => value.toLowerCase().replace(/\s+/g, ' ').trim();
  let searchTimer;
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
    results.textContent = `${announcement}${count} of ${entries.length} approaches`;
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
  }
  function restore() { clearTimeout(searchTimer); stateFromUrl(); apply(); revealFragment(); }
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(searchTimer); writeUrl(); apply(); });
  controls.q.addEventListener('input', () => {
    clearTimeout(searchTimer); apply();
    searchTimer = setTimeout(() => writeUrl(), 250);
  });
  for (const key of ['work', 'type', 'supervision']) controls[key].addEventListener('change', () => {
    clearTimeout(searchTimer); writeUrl(); apply();
  });
  form.addEventListener('reset', event => {
    event.preventDefault(); clearTimeout(searchTimer);
    Object.values(controls).forEach(control => { control.value = ''; });
    writeUrl(); apply();
  });
  document.querySelectorAll('.permalink').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); clearTimeout(searchTimer);
    const url = new URL(location.href); url.hash = link.hash;
    if (url.href !== location.href) history.pushState(null, '', url);
    revealFragment();
  }));
  window.addEventListener('popstate', restore);
  window.addEventListener('hashchange', restore);
  form.hidden = false;
  restore();
})();
