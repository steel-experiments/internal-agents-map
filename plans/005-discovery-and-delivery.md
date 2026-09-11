# Discovery and delivery for internal-agents.com

Goal: publish crawlable canonical pages, source-preserving agent reading formats,
asset caching, and a custom 404 on Vercel without introducing an API service.

- [x] Canonical HTML metadata and www-to-apex redirect.
- [x] Build-generated robots.txt and sitemap (excluding 404).
- [x] Documented JSON, compact index, individual JSON/Markdown evidence records.
- [x] Markdown versions of content pages and llms.txt discovery links.
- [x] Link response headers and Accept-based Markdown negotiation.
- [x] Content-hashed CSS/JS/fonts with immutable caching; other files revalidate.
- [x] Custom accessible 404 with navigation and noindex.
- [x] Validate preview: 47 HTTP checks for formats, headers, evidence bytes, assets, and nested 404.
  Browser layout checked locally at desktop/mobile; production browser check follows.
- [x] Publish and validate production: 47 HTTP checks passed; www redirects with path/query preserved.
  Brotli compression and CDN HIT verified. Custom domain HTTPS checked against the
  publicly resolved Vercel IP because local DNS still cached the old delegation.
  Vercel confirms both nameservers; production browser checked via the public Vercel alias.

No OAuth, MCP, DNS-AID, ARD, or invented API metadata.
Follow-up: owner explicitly selected Content Signals `search=yes, ai-input=yes, ai-train=yes`.

Validation: 122 Python tests, 2 Node negotiation tests, archive/privacy/build/artifact/
lint/format/local-link checks passed. No Git commit or push performed.
