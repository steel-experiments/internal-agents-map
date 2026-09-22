# Website

The website is an [Astro](https://astro.build/) project in `src/`. It builds static HTML,
Markdown, and JSON files from the same normalized catalog as
[data/agents.json](../data/agents.json). Python validates the research data and writes that
catalog; the website build does not change evidence. Every claim stays reachable with its
provenance, confidence, qualifications, evidence relations, and source locators.

Vercel serves the result at `https://internal-agents.com/`.

## Editing and preview

- Edit `data/agents/*.yaml` for catalog content. Do not edit the normalized JSON.
- Edit `src/content/notes/*.md` for the notes. Each note declares its title, description,
  publication date, reading order, sources, and `relatedAgentIds`. The entry pages read that
  metadata for their related reading. Follow [the notes writing guide](notes-writing.md) for
  language, quotes, and diagrams.
- Edit `src/lib/guide-content.ts` for the text of the Definitions and Methodology guides. The
  page and its Markdown export read the same values, so the two stay together.
- Edit the pages in `src/pages/`, the shared layouts in `src/layouts/`, the components in
  `src/components/`, and the styles in `src/styles/` for the presentation.
- The Definitions quadrant compares workflow breadth and organizational adaptation. Its catalog
  markers come from claims in `src/lib/definitions.ts`; a missing or unsupported claim removes a
  marker. Review the placements when those claims change. Coordinates are illustrative, not scores.

Run the local preview with:

```sh
npm run dev
```

The command first regenerates `data/agents.json` with the Python data build, then starts Astro.
It watches `data/agents/`, so a record edit produces a new catalog and the page reloads. A
validation failure stays visible in the terminal; the server does not serve older data silently.

Run `npm run build` for the complete static build and `npm run preview -- --host 127.0.0.1
--port 4180` to serve the built files. The build writes `dist/`, which Git ignores. Do not commit
website output. Astro caches in `.astro/`, and the browser tests write `playwright-report/` and
`test-results/`; Git ignores these too.

Run `npm run verify` before a pull request. It checks the committed data and archives first, then
runs the type, unit, build, artifact, Python test, lint, format, privacy, local-link, browser,
and whitespace gates in one sequence.

The browser tests use Playwright's managed `webServer` to start the built Astro site,
wait up to 30 seconds for readiness, and stop it after the run. The server uses Astro's
JavaScript API so it stays in the foreground in both agent environments and CI.
The suite has a five-minute limit, and the complete validation job has a fifteen-minute
limit. Tests require a free port: set `PREVIEW_PORT` to use a port other than 4180.

## Routes and formats

Astro uses `output: 'static'`, `build.format: 'file'`, and `trailingSlash: 'never'`. Each page
becomes one file, such as `dist/agents/stripe-minions.html`, and Vercel `cleanUrls` serves it at
`/agents/stripe-minions`. Vercel answers a request for the `.html` name before the middleware
runs, so on an alias host that request takes two permanent redirects. A trailing slash gets a
permanent redirect to the clean path.

The build generates the directory, one page for each implementation, the two guides, the notes
index, the notes, and the 404 page. It also generates `robots.txt`, `sitemap.xml`, `llms.txt`,
Markdown for every published page, `agents/index.json`, `agents/<id>.json`, `agents/<id>.md`, and
`agents.json`. `agents.json` remains byte-identical to the normalized source catalog.
`data-guide.md` combines reading instructions with the repository schema reference. The sitemap
holds the canonical HTML pages only. It excludes the 404 page, redirects, exports, and filter
states, and it does not invent modification dates.

Archive paths inside the JSON remain repository-relative; resolve them against the repository
checkout or `https://github.com/steel-experiments/internal-agents-map/blob/main/`, not the
website. The pages link preserved Markdown to GitHub; only website assets are deployed.

Robots allows public crawling, including the search and retrieval bot groups. The owner selected
`search=yes, ai-input=yes, ai-train=yes`; Content Signals declare these preferences in the
wildcard group and in those groups. These preferences do not change the rights of cited
publishers.

`routing-manifest.json` is generated. The publication integration writes it during `npm run
build` from the declared routes, and it records the physical HTML and Markdown file behind each
clean path. `middleware.ts` imports the manifest and answers a request for Markdown with the
static `.md` file. Browser requests and wildcard `Accept` headers stay HTML. Quality preferences
and `q=0` are respected, and HTML wins an explicit equal-quality tie. Both representations send
`Vary: Accept`. The middleware also redirects the alias hosts itself, because it answers HTML
requests before the `vercel.json` redirects run. Direct Markdown URLs work without the
middleware, and an unknown route reaches the real 404 page.

## Design and fonts

The visual direction comes from the local `steel-web-minimal/templates/starter.html`
reference: a quiet sidebar, bounded content column, fine dividers, white background,
dark ink, and restrained accents. All text uses self-hosted ABC Areal, with system
sans-serif fallbacks and `font-display: swap`. No runtime font CDN or build-time
network access is required.

The variable font is `ABCArealVariable.woff2` from the licensed ABC Areal package by
[Dinamo](https://abcdinamo.com), copied without modification to
[public/fonts/Areal.woff2](../public/fonts/Areal.woff2). Its weight axis runs 400-700,
so the `font-weight: 550` rules in the stylesheets resolve to a real intermediate
weight rather than a synthesized one. The face also carries `slnt` and `DRKM` axes,
which the site does not currently use.

ABC Areal is a commercially licensed typeface. Unlike the openly licensed face it
replaced, no font license file is published beside the asset; the foundry's terms
govern its use, including self-hosting on this domain. Repository licenses continue
to govern other content.

## Reading and sharing

The directory holds one compact card for each implementation. Every card is in the initial HTML
and links to the entry page, so the entries stay crawlable and work without JavaScript. One search
box carries the whole query. A word that names a work area, an approach type, or a supervision
level becomes a chip, either from the suggestion list under the box or on Enter when the word is
an exact match. The chip label of a supervision level shows the boundary and its derived level,
and the level alone, such as `level 4`, also names it. Every other word searches the text of the
cards, which holds the company, agent name, summary, work tags, approach type, attention
boundaries with their levels, and autonomy. All words of the free text must match.

Chips of one facet combine with OR, facets combine with AND, and the free text applies on top.
Any matching scoped attention boundary qualifies for supervision. Levels describe workflows, not
company rankings. The suggestion vocabulary comes from the catalog, including Unknown when present,
and the page carries it as JSON so the script and the cards agree.

The URL uses `q`, `work`, `type`, and `supervision` query parameters, and repeats a facet
parameter for each selected value. Browser back and forward restore that state. Filter states keep
the homepage canonical and stay out of the sitemap.

An old homepage fragment still reaches its content. A known approach, claim, or source fragment
sends the browser to the entry page and the same anchor there. The script rebuilds the target
path from the route helper and the matched identifier, so an unknown fragment keeps ordinary
homepage behavior and cannot become a redirect target. Without JavaScript, the card links remain
the path to each entry.

Every page except the home page carries its own link preview. The build draws one 1200 by 630 PNG
per route under `dist/og/` with satori and resvg, from `src/og/render.ts`, on the ground and type
of the directory: the possessive title the homepage uses, the summary shortened to three lines, the
approach type and work tags, the address, and the organization mark on a white panel. An
organization card lists its systems; a section, guide, or note card shows its heading and
description under a blue dot eyebrow. `src/lib/og.ts` derives every value from the same views the
pages read, and `src/lib/section-cards.ts` holds the section inputs. The `og:image` URL carries a
short hash of the card input, so a changed card gets a new URL and the link caches of Slack,
LinkedIn, and X drop the old one. The renderer reads `ABCAreal-Regular.ttf` and
`ABCAreal-Medium.ttf` from `src/og/fonts/`; a missing file stops the build, because no other face
may stand in. The home page keeps `public/og.png`. `scripts/check_site.py` requires every page to
name a card that exists at the card size, and the SEO pulse reports a page that fell back to the
shared card.

## Validation and publication

`scripts/check_site.py --root dist` validates the built artifact: the expected route inventory,
required landmarks, unique identifiers, local asset and fragment links, CSS font references,
per-entry claim and source coverage, JSON parity, and privacy. It rejects extra files, symlinks,
escaping paths, and executable URL schemes. External source URLs are not fetched by this checker;
the scheduled external-link workflow handles those.

The `validate` workflow installs uv, Node, and the pinned Chromium browser, then runs
`npm run verify` on pull requests and on pushes to `main`. It does not deploy. Workflow
concurrency is scoped to workflow and Git ref; a newer `main` run cancels an older run.

GitHub Pages is disabled for this repository. The site has one public host. A second host would
split search authority and duplicate every page.

## Vercel delivery

The canonical site is **https://internal-agents.com/** on Vercel, in the Steel team
(`nen-labs/internal-agents-map`). The project is connected to the GitHub repository; every push
to `main` deploys to production.

`vercel.json` is authored, not generated. Vercel reads it before the build command runs, so it
must not depend on the build. It holds fixed rules only, and a new entry or note needs no change
to it:

- `installCommand` is `npm ci`. `buildCommand` checks the committed research outputs, builds the
  website, and checks `dist/`. `outputDirectory` is `dist`.
- `cleanUrls` is true and `trailingSlash` is false.
- `www.internal-agents.com` and the bare `internal-agents-map.vercel.app` alias redirect
  permanently to the apex origin, with the path and query string.
- Headers set `nosniff`, revalidation for pages and exports, one-year immutable caching for the
  hashed assets under `/_astro/`, the Markdown and JSON content types, CORS for the exports, and
  the `describedby` link to `data-guide.md`.
- `X-Robots-Tag: noindex` covers the raw JSON records, the compact JSON index, and the 404 page
  only. No HTML entry page carries it. The Markdown representations use an HTTP canonical link to
  their HTML page instead of a noindex directive.

Before you publish, verify locally and then deploy a preview:

```sh
uv sync --locked
npm ci
npm run verify
vercel deploy --yes --scope nen-labs
```

Check the preview with the delivery checker, then promote the same revision:

```sh
uv run --locked python scripts/check_delivery.py <preview-url> --preview --root dist
uv run --locked python scripts/check_delivery.py https://internal-agents.com --root dist
```

The checker compares response bytes with the built files in `--root`, and it checks content
types, discovery headers, immutable asset caching, quality-weighted negotiation, clean and legacy
paths, missing nested URLs, and alternating HTML and Markdown requests that would show cache
contamination. It removes only Vercel's appended feedback-toolbar script when it compares
protected preview HTML. A protected preview can also be read with
`vercel curl --deployment <preview-url>`. Production must stay publicly readable without bypass
credentials. A local Astro preview cannot prove the middleware, the redirects, or the headers.

Rollback: deploy or promote an earlier Vercel deployment that already contains the entry pages,
their assets, and the clean-URL policy. A deployment from before those pages existed would turn
published entry URLs into 404s, so it is not a rollback target. Record the chosen deployment
identifier before a release. For a faulty content change, revert the commit on `main` and let the
connected project deploy the corrected revision. Do not upload an unchecked folder by hand.

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
Delivery acceptance on 2026-09-11: 122 Python tests and 2 Node tests passed;
47 preview and 47 production HTTP checks passed. Vercel serves Brotli-compressed
HTML with CDN cache hits. `www` returns 308 and preserves path/query. Both Vercel
nameservers are verified. Local DNS still held the previous delegation, so custom
domain HTTPS checks used `--resolve-ip` with a public DNS answer; no TLS checks
were bypassed. Browser acceptance used the public production Vercel alias.

## Company pages

Each referenced company has a generated `/organizations/<company.id>` page and matching `.md` representation. Record Company fields link to it. Membership and connections derive from existing catalog records; registry-only companies have no page. Agents and Infrastructure remain separate nonempty groups, and connections retain authored direction and relation type. There is no Organizations menu item or index. Shared page furniture, catalog cards, and floating search remain unchanged. Routes are included in the publication inventory, sitemap, and llms.txt; no catalog schema or JSON export changes are required.
