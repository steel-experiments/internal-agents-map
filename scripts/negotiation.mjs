/** Hosts that alias the canonical origin. Requests on them redirect to it. */
export const CANONICAL_ORIGIN = 'https://internal-agents.com';
const ALIAS_HOSTS = new Set(['www.internal-agents.com', 'internal-agents-map.vercel.app']);

/** Return the canonical URL for a request on an alias host, or null when the host is canonical. */
export function canonicalRedirect(url) {
  if (!ALIAS_HOSTS.has(url.hostname)) return null;
  return CANONICAL_ORIGIN + url.pathname + url.search;
}

/** Prefer HTML unless the client explicitly requests an acceptable Markdown type. */
export function wantsMarkdown(accept = '') {
  const ranges = accept.toLowerCase().split(',').map(part => {
    const [type, ...params] = part.trim().split(';').map(value => value.trim());
    const qParam = params.find(value => value.startsWith('q='));
    const q = qParam ? Number(qParam.slice(2)) : 1;
    return { type, q: Number.isFinite(q) && q >= 0 && q <= 1 ? q : 0 };
  });
  const explicit = ranges.find(range => range.type === 'text/markdown');
  if (!explicit || explicit.q === 0) return false;
  const html = ranges.find(range => range.type === 'text/html');
  const fallback = ranges.find(range => range.type === 'text/*')
    ?? ranges.find(range => range.type === '*/*');
  const htmlQ = (html ?? fallback)?.q ?? 0;
  return explicit.q > htmlQ || (explicit.q === htmlQ && !html);
}
