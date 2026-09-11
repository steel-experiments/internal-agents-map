# Generated website

The mini page provides search, work/type/supervision filters, and expandable evidence
for the catalog. It is generated offline from the same normalized object as
[data/agents.json](../data/agents.json). Every claim remains reachable, with its
provenance, confidence, qualifications, evidence relations, and source locators.

## Editing and preview

- Edit `data/agents/*.yaml` for catalog content. Do not edit normalized JSON or generated HTML.
- Edit [the HTML shell](../templates/site.html), [CSS](../templates/site.css), and
  [JavaScript](../templates/site.js) for the website.
- Edit [the Definitions page](../templates/definitions.html) for the guide. Its quadrant
  compares workflow breadth and organizational adaptation. Three editorial placements
  link to scope, context, and tool claims; missing or unsupported claims remove a marker.
  Review placements when those claims change. Coordinates are illustrative, not scores.
  The guide shares navigation, footer, CSS, and Geist with the catalog.
- Edit [the Methodology page](../templates/methodology.html) for the evidence guide.
  It shares navigation, footer, CSS, and Geist with the catalog.
- Edit [the Notes index](../templates/notes.html) and the articles in `templates/notes/`
  for short observations. The build shares the catalog navigation and footer with these
  pages. Nested article links stay relative, so the site works from any base path.
  Follow [the notes writing guide](notes-writing.md) for language, quotes, and diagrams.
- Run `uv run --locked python scripts/build.py` to regenerate Markdown, JSON, and `site/`.
- Run `uv run --locked python scripts/check_site.py --root site` and the existing catalog checks.
- Serve the page locally with:

```sh
uv run --locked python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8000/`; stop the server with Ctrl-C when finished. Opening
`site/index.html` directly also provides the static catalog, but use HTTP for URL/history testing.
Commit all generated output with its authored changes. CI checks committed output without
rebuilding first, so stale HTML, CSS, JavaScript, JSON, or fonts fail validation.

`site/agents.json` is byte-identical to `data/agents.json`. Archive paths inside that
JSON remain repository-relative; resolve them against the repository checkout or
`https://github.com/steel-experiments/internal-agents-map/blob/main/`, not the website.
The page links preserved Markdown to GitHub; only website assets are deployed.

## Design and fonts

The visual direction comes from the local `steel-web-minimal/templates/starter.html`
reference: a quiet sidebar, bounded content column, fine dividers, white background,
dark ink, and restrained blue accents. The user requested Geist in place of serif
headings. All text uses self-hosted Geist Sans, with system sans-serif fallbacks and
`font-display: swap`. No runtime font CDN or build-time network access is required.

The variable font is the official [Geist 1.5.1](https://github.com/vercel/geist-font/releases/tag/1.5.1)
asset from commit `3c80bfcc1ba4988ece0eda46a282e15d29e61bbf`, path
`fonts/Geist/webfonts/Geist[wght].woff2`, copied without modification to
[templates/fonts/Geist.woff2](../templates/fonts/Geist.woff2).
The accompanying [SIL Open Font License](../templates/fonts/OFL.txt) is retained
and copied with the font to `site/assets/fonts/`. The font's license applies to that
asset; repository licenses continue to govern other content.

## Reading and sharing

Search matches company, agent name, summary, work tags, and approach type. Filters
combine with AND; any matching scoped attention boundary qualifies for supervision.
Levels describe workflows, not company rankings. Select options come from the catalog,
including Unknown when present. Missing claim metadata stays unknown.

The URL uses `q`, `work`, `type`, and `supervision` query parameters. Permalinks use
approach IDs as fragments, open the requested entry, and clear conflicting filters
with a brief announcement. Deliberately changing filters clears a prior approach
fragment so reload restores the visible search. Browser back/forward restores URL
state. Without JavaScript, the complete catalog, native disclosures, sources, and
navigation remain available; inactive filter controls stay hidden.

## Validation and publication

`scripts/check_site.py` validates the explicit artifact allowlist, required landmarks,
unique IDs, local asset and fragment links, CSS font references, source/claim/approach
coverage, JSON parity, and privacy. It rejects extra files, symlinks, escaping paths,
and executable URL schemes. External source URLs are not fetched by this checker;
the existing external-link scheduler handles those checks.

The `validate` workflow runs archive, build, site, privacy, lint, format, test, and
local-link gates on pull requests and on pushes to `main`. It does not deploy. Workflow
concurrency is scoped to workflow and Git ref; a newer `main` run cancels an older run.

GitHub Pages is disabled for this repository. The site has one public host,
`https://internal-agents.com/`, served by Vercel (see below). A second host would split
search authority and duplicate every page.

Rollback: revert the faulty change on `main` to restore a previously validated website
revision, including its templates and generated outputs, then redeploy to Vercel.
Do not upload an unchecked folder manually.

## Browser acceptance record

Browser results are recorded below after running the implementation matrix.

Executed on 2026-09-09 with Playwright and Chromium 151.0.7922.34. Desktop
1440×1000, tablet 800×1100, mobile 390×844, and 200% CSS layout zoom at 1440×1000
were rendered; screenshots were visually inspected. The 200% check used CSS layout
zoom rather than the browser's toolbar zoom. The reference template was also rendered
and reviewed. Test scripts/screenshots are local review artifacts, not published assets.

| Check | Expected | Actual |
| --- | --- | --- |
| Initial load | All catalog entries; no missing assets/errors | 39 entries; Geist loaded; no page errors or failed asset responses |
| Search and clear | Case/whitespace tolerant Stripe match, then all entries | One Stripe result, then 39 |
| AND filters | Match every active filter, any matching scope | Coding + background agent + work-product review returned Ramp and Stripe; reload preserved both |
| Zero results and reset | Empty message, then defaults | Absent search showed empty state; reset restored 39 |
| Evidence disclosure | Full text, qualifications, citations, relations | Uber low-confidence weekly/monthly conflict and contradicting source link remained readable |
| Permalink and URL state | Open/reveal entry; restore history | Stripe fragment cleared conflicting finance filter with announcement; later Uber search cleared old fragment; reload/back/forward agreed |
| JavaScript disabled | Full readable catalog and native disclosures | All 39 entries, working evidence disclosures/citations; controls hidden |
| Keyboard | Skip link, controls, disclosures, sources, visible focus | Traversal reached each control and native disclosure, Enter expanded them, source links received visible focus; no trap |
| Responsive and zoom | No horizontal overflow or overlapping controls | Desktop, tablet, mobile, and 200% layout zoom passed; mobile filters wrapped and labels stayed legible |
| Project subdirectory | Relative assets and JSON work | Served under `/internal-agents-map/`; search, font, CSS, JS, and JSON succeeded |

Final local verification passed: 116 unit tests; archive, generated-output, artifact,
privacy, Ruff lint/format, Markdown-link, and whitespace checks. Repeated generation
produced identical bytes. Data and archive files were unchanged relative to the
transferred Plans 002–003 baseline; only the authored README navigation changed
among existing generated documentation.

Live publication acceptance on 2026-09-09 also passed in Chromium: all 39 entries
were visible, Geist loaded, and search, evidence disclosures, permalinks, and reload
worked without page errors.

## Vercel delivery and agent-readable formats

The canonical site is now **https://internal-agents.com/** on Vercel, in the Steel
team (`nen-labs/internal-agents-map`). `www` permanently redirects to the apex while
retaining paths and query strings. Automatic Vercel Git integration was
not connected during setup; CLI deployment works independently.

The build generates `robots.txt`, `sitemap.xml`, `llms.txt`, Markdown for every
published content page, `agents/index.json`, and `agents/<id>.json` and `.md`.
The sitemap excludes the custom 404 and does not invent modification dates. The
compact index links to individual records containing all associated claims and
sources. `agents.json` remains byte-identical to the normalized source catalog.
`data-guide.md` combines reading instructions with the repository schema reference.
Robots allows public crawling, including explicit search/retrieval bot groups.
The owner selected `search=yes, ai-input=yes, ai-train=yes`; Content Signals
declare these preferences in both the wildcard and search/retrieval groups.
These preferences do not change the rights of cited publishers.

Edit `templates/vercel.json` for delivery configuration; the build produces root
`vercel.json` with per-page discovery headers and exact hashed asset cache rules.
Edit `templates/data-guide.md` for reading instructions and `templates/404.html`
for the missing-page experience. The error page is excluded from indexing, uses
root-relative navigation/assets to work for missing nested URLs, and is served
with HTTP 404 by Vercel. Its root-relative links target Vercel hosting.

The Python build creates content-hashed CSS, JavaScript, and font files and updates
HTML/preload/CSS references together. Vercel gives only these exact hashed paths
one-year immutable browser caching. Unhashed compatibility copies remain available
with revalidation; HTML, JSON, Markdown, and discovery files also revalidate.
Obsolete generated hashes and individual records are removed on rebuild.

`middleware.ts` uses the generated `routing-manifest.json` to rewrite explicit
Markdown requests to static `.md` files. Browser requests and wildcard Accept
headers stay HTML. Quality preferences and `q=0` are respected; HTML wins an
explicit equal-quality tie. Both representations use `Vary: Accept`. The CDN sees
distinct rewrite targets; direct Markdown URLs also work without middleware.
Filters do not change exported content. There is no
runtime HTML conversion, model call, authenticated API, or registration service.

Before publishing, regenerate and validate locally, then deploy a preview:

```sh
uv sync --locked
npm ci
uv run --locked python scripts/build.py
uv run --locked python scripts/check_site.py --root site
uv run --locked python -m unittest discover -s tests
npm test
vercel deploy --yes --scope nen-labs
```

Vercel also builds and checks the artifact on every deployment. Generate locally
first because Vercel reads routing configuration before executing the build.
Check the preview's content types, negotiated representations, cache headers, and
missing nested URL before `vercel deploy --prod --yes --scope nen-labs`. Protected
previews can be checked with `vercel curl --deployment <preview-url>`. Production
must remain publicly readable without bypass credentials.

Repeatable deployed verification:

```sh
uv run --locked python scripts/check_delivery.py https://your-preview.vercel.app --preview
uv run --locked python scripts/check_delivery.py https://internal-agents.com
```

The verifier checks response bytes against generated files, content types, discovery
headers, immutable asset caching, quality-weighted negotiation, missing nested URLs,
and alternating HTML/Markdown requests to detect cache contamination. It removes
only Vercel's appended feedback-toolbar script when comparing protected preview HTML.

Delivery acceptance on 2026-09-11: 122 Python tests and 2 Node tests passed;
47 preview and 47 production HTTP checks passed. Vercel serves Brotli-compressed
HTML with CDN cache hits. `www` returns 308 and preserves path/query. Both Vercel
nameservers are verified. Local DNS still held the previous delegation, so custom
domain HTTPS checks used `--resolve-ip` with a public DNS answer; no TLS checks
were bypassed. Browser acceptance used the public production Vercel alias.
