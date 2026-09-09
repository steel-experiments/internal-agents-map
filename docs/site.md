# Generated website

The mini page provides search, work/type/supervision filters, and expandable evidence
for the catalog. It is generated offline from the same normalized object as
[data/agents.json](../data/agents.json). Every claim remains reachable, with its
provenance, confidence, qualifications, evidence relations, and source locators.

## Editing and preview

- Edit `data/agents/*.yaml` for catalog content. Do not edit normalized JSON or generated HTML.
- Edit [the HTML shell](../templates/site.html), [CSS](../templates/site.css), and
  [JavaScript](../templates/site.js) for the website.
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

The existing `validate` workflow runs archive, build, site, privacy, lint, format,
test, and local-link gates before uploading **only `site/`**. Pull requests validate
without uploading or deploying. Pushes to `main`, or manual runs on `main`, may deploy
through a separate job that depends on successful validation. Workflow concurrency
is scoped to workflow and Git ref; a newer `main` run cancels an older run, while
PR runs cannot cancel publication. Deployment is additionally serialized in the Pages group.

Initial setup: in repository Settings → Pages, set **Source: GitHub Actions**. No custom
domain is configured by this feature. The configured project URL is
`https://steel-experiments.github.io/internal-agents-map/`.

Publication status: **Live at [Internal Agents Map](https://steel-experiments.github.io/internal-agents-map/).**
The first publication from commit `abf9887` passed validation and deployment in
[Actions run 34336076085](https://github.com/steel-experiments/internal-agents-map/actions/runs/34336076085)
on 2026-09-09. Public HTML, CSS, JavaScript, JSON, Geist, and its license all returned
HTTP 200 and matched the local artifact bytes.

Rollback: revert the faulty change on `main` to restore a previously validated website
revision, including its templates and generated outputs. The same validation and Pages
workflow republishes it. Do not upload an unchecked folder manually.

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
