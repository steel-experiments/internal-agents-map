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
