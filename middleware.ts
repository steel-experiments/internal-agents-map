import { next, rewrite } from '@vercel/functions';
import routes from './routing-manifest.json' with { type: 'json' };
import { canonicalRedirect, wantsMarkdown } from './scripts/negotiation.mjs';

export const config = { matcher: ['/', '/:path*.html'] };

export default function middleware(request: Request) {
  const url = new URL(request.url);
  // Middleware answers before vercel.json redirects, so alias hosts are redirected here.
  const canonical = canonicalRedirect(url);
  if (canonical) return Response.redirect(canonical, 308);
  const markdown = routes[url.pathname as keyof typeof routes];
  if (!markdown || !['GET', 'HEAD'].includes(request.method)) return next();
  const headers = { Vary: 'Accept', 'Cache-Control': 'public, max-age=0, must-revalidate' };
  if (wantsMarkdown(request.headers.get('accept') ?? '')) {
    url.pathname = markdown;
    // Query filters affect the browser UI, not the complete reading representation.
    url.search = '';
    return rewrite(url, { headers: { ...headers, 'Content-Type': 'text/markdown; charset=utf-8' } });
  }
  return next({ headers });
}
