# Plan 004: Generate and publish a searchable Internal Agents Map

> **Executor instructions:** Read this plan fully, implement in order, run the
> verification gates, and record results before updating the index. This is a
> plan for a future implementation; the planning task does not publish a site.
>
> **Drift check:** Run `git diff --stat e67e79b..HEAD -- scripts/build.py
> tests/test_build.py templates site scripts/check_site.py tests/test_site.py
> .github/workflows/validate.yml .github/pull_request_template.md README.md
> CONTRIBUTING.md docs/site.md plans` and `git status --short`. Compare the
> current-state excerpts below with the live files. The planning baseline
> deliberately includes the uncommitted, completed changes from Plans 002–003;
> a checkout of the recorded commit alone is insufficient.

## Status

- **Status:** DONE
- **Priority:** P2
- **Effort:** M (roughly one to two days including browser checks)
- **Risk:** MED — rendering must preserve evidence meaning and publication must follow validation.
- **Depends on:** Plans 002 and 003, both DONE in the current working tree.
- **Category:** direction
- **Planned at:** commit `e67e79b`, 2026-09-09, plus the current working-tree changes.

## Why this matters

The catalog is currently a long Markdown document. A small website will let
readers find relevant systems by company, work, approach type, and where human
review occurs. Generate the page from the same validated data as the Markdown
and JSON so contributors maintain one catalog and every accepted update reaches
the website through the existing CI workflow.

The user selected the local `steel-web-minimal/templates/starter.html` as visual
direction. Preserve its editorial typography, quiet sidebar, fine rules, and
restrained controls while making the catalog the main content.

## Current state

- Repository: `/Users/nikola/dev/steel/internal-agents-map`.
- Remote: `https://github.com/steel-experiments/internal-agents-map`; branch `main`.
- Python 3.12, uv, PyYAML, Ruff, and standard-library `unittest`; no frontend framework.
- `data/agents/*.yaml` is authored data. `scripts/build.py` validates it and
  generates Markdown plus schema-version-4 JSON. The working tree currently
  contains 39 approaches, 35 organizations, 555 claims, and 88 sources.
- `scripts/build.py:1088`, `normalize(records)`, returns separate `approaches`,
  `claims`, and `sources` arrays. Approach summaries, metrics, architecture,
  primitives, and lessons are moved into claims; they are not direct approach fields.
- `scripts/build.py:1179`, `rendered_outputs(records)`, currently ends with:

  ```python
  LANDSCAPE: render_landscape(records),
  DATA_JSON: json.dumps(normalize(records), indent=2, ensure_ascii=False) + "\n",
  ```

- `scripts/build.py:1206`, `write_outputs`, stages output in adjacent temporary
  files before replacing destinations. `main` compares every expected output
  in `--check` mode without writing. Extend this mechanism.
- `tests/test_build.py:18` imports the build script through
  `importlib.util.spec_from_file_location`. Preserve that import path and the CLI.
  Follow its `unittest.TestCase`, temporary-directory, and fixture conventions.
- `.github/workflows/validate.yml:20` runs all catalog checks on PRs and pushes
  to `main`. Actions use full commit pins with version comments; preserve that convention.
- `scripts/check_links.py:67` discovers Git-tracked Markdown only. It does not
  validate a website's HTML, assets, or HTML fragment targets.
- There is no existing site directory or Pages workflow. Remote Pages settings
  and domain configuration were not inspected; do not claim an address is live.
- Planning recon confirmed `scripts/build.py --check` and the local link checker
  pass. The preceding completed work passed 97 tests; rerun the baseline before implementation.

## Design direction

Reference files inspected during planning:

- `/Users/nikola/dev/steel/steel-web-minimal/templates/starter.html`
- Its `css/tokens.css`, `css/base.css`, `css/layout.css`, `css/components.css`,
  and `js/main.js` siblings in that repository.
- Its `assets/README.md` documents the reference assets. Use CSS and self-hosted Geist
  fonts for this page; reference logos, photographs, and trial fonts are unnecessary.

The reference HTML and CSS were read directly during planning. During execution,
the reference was also rendered and inspected in Chromium at 1440px width; compare
the generated page at desktop and mobile widths before final validation.
The following specification is sufficient if the sibling repository is unavailable.

| Element | Direction for the map |
| --- | --- |
| Palette | White `#ffffff`; ink `#2c2b31`; muted text around `#666666`; rules `#ededee`; pale surfaces `#f3f3f3`; blue `#386bff` for links and focus |
| Typography | Geist Sans for headings and body, with sans-serif fallbacks; optional Geist Mono for numeric metadata. Self-host licensed WOFF2 assets with font-display: swap. |
| Scale | Body 15–16px with 1.5 line height; heading about 28–34px; metadata at least 12px |
| Desktop shell | Centered shell up to 1248px; approximately 224px sticky sidebar and 800px main column, 32px insets |
| Spacing | Mostly 8/16/24/32/48px; shorten the reference's 128px top space so the catalog begins within the first desktop screen |
| Components | Small section labels, lightly bordered controls, thin row dividers, native disclosure rows, modest 4px control radii |
| Mobile | Below about 800px, one column with 20–24px insets, wrapping filters, and a simple visible navigation row |

Keep the first version light themed, text led, and usable without external
fonts, images, or a JavaScript CDN. Give useful text sufficient contrast; the
reference's faint decorative text is not a requirement. Avoid importing its
product sales copy, pricing, illustration slots, or six-column footer.

### Page structure and behavior

1. **Navigation:** Internal Agents Map wordmark as text; links to Catalog,
   Methodology, source repository, and JSON download. A simple mobile navigation
   row avoids adding a full-screen menu solely to reproduce the reference.
2. **Introduction:** Title "Internal Agents Map", the existing definition in
   plain language, and generated counts for approaches, organizations, and
   sources. Label dates precisely: "Latest entry review" is the maximum
   `last_reviewed_at`, not a claim that every source was rechecked that day.
3. **Catalog controls:** Labeled search input; work, approach-type, and human
   supervision selects; reset button; live result count. Filter values are
   generated from the data, with readable labels and explicit Unknown values.
4. **Catalog rows:** Company, agent name, summary, approach type, work tags,
   and supervision description. Use a vertical list with fine dividers; longer
   content wraps. Default order is company then agent name, with ID as tie-breaker.
5. **Expanded entry:** Scoped operating models, architecture, reported metrics,
   lessons/interpretation, supporting and conflicting evidence, sources, review
   date, and permalink. Use native `details`/`summary`; no essential content
   requires JavaScript or a fetch. All catalog claims must remain reachable here.
6. **Methodology/footer:** Brief distinction between reports and catalog
   interpretation, explanation that levels describe workflows, and links to the
   existing schema, patterns, adoption observations, evidence review, and contribution guide.

Search matches company, agent name, summary, domains, and approach type using
case-insensitive substring matching over normalized whitespace. Filters combine
with AND; any matching domain or scoped attention boundary qualifies within its
filter. Use `operating_models[].attention_boundary` for human supervision and
retain each model's scope. Never average levels or treat them as company rankings.

Use query parameters `q`, `work`, `type`, and `supervision`; use the approach ID
as the fragment. Restore controls on load, support browser history, and ignore
invalid filter values gracefully. A permalink opens and reveals its entry; if
filters exclude the requested entry, reset the conflicting filters and announce
the change. Provide a clear zero-results message and working reset button.
With JavaScript disabled, show the full ordered catalog and disclosures, hide
inactive filter controls, and keep navigation and source links usable.

## Data and generation contract

- Compute `catalog = normalize(records)` once in `rendered_outputs`; serialize
  that same object for JSON and pass it to a pure `render_site(catalog)` renderer.
  Add the renderer and small HTML helpers to `scripts/build.py`; a broader build
  refactor is outside this feature.
- Join `approach.claim_ids` to claims by ID, then evidence links to sources by
  `source_id`. Group claims by `field` for presentation, but identify numerical
  metrics by `claim.kind == "metric"`. Five former metric fields now contain
  other kinds of claims; a field named `key_metrics.*` alone is not sufficient.
- Preserve full claim text and qualifications. Display provenance and confidence
  with the claim, including its reason when expanded. Show `reported_by`, scope,
  denominator, method, and `valid_at` when supplied; missing values stay unknown.
  Label `valid_at` as the claim's observation date, not automatically its measurement window.
- Do not turn the Uber weekly/monthly conflict into a single unqualified number.
  Render `supports`, `contradicts`, and `contextualizes` as distinct relations,
  with their source titles and locators. Community commentary is not independent verification.
- Evidence strength describes source detail, and first-party confidence is not
  independent verification. Avoid ratings or "verified" badges that imply otherwise.
- Keep original source URLs visible as primary citations. Offer preserved Markdown
  and optional Wayback links separately. Repository archive paths become GitHub
  blob links under `https://github.com/steel-experiments/internal-agents-map/blob/main/`;
  a free-text locator is displayed as text, not converted into a guessed fragment.
  Normalized `source.capture` is the expanded manifest; the Markdown path is
  `source.capture.artifacts.markdown.path`, not the YAML capture pointer.
- Use the same repository base for documentation and contribution links. Website
  assets use relative paths such as `assets/site.css`, never root-absolute paths,
  so the page works at both `/` and `/internal-agents-map/`.
- Generate and track these website outputs (plus self-hosted Geist font/license assets): `site/index.html`,
  `site/agents.json`, `site/assets/site.css`, `site/assets/site.js`.
  The downloaded JSON must be byte-identical to `data/agents.json`; its schema and
  repository-relative archive paths remain unchanged. Explain those paths in `docs/site.md`.
- Author the shell and assets in `templates/site.html`, `templates/site.css`,
  and `templates/site.js`. Copy assets through the same output map so `--check`
  detects stale CSS/JS too. Put an appropriate generated-file comment in outputs
  where syntax allows it. Do not manually edit generated website files.
- Escape catalog text and attribute values with `html.escape(..., quote=True)`.
  Treat source prose as text. Do not render untrusted Markdown/HTML, inject
  catalog values with `innerHTML`, or interpolate them into executable JavaScript.
  Small escaped `data-*` attributes are enough for filtering; avoid embedding a
  second full JSON payload inside the page.
- Builds remain deterministic, offline, and independent of the sibling reference
  repository. No current-time stamps, scraping, browser rendering, or remote fonts at build time.

## Scope

**In scope:**

- `scripts/build.py`, `tests/test_build.py`
- `templates/site.html`, `templates/site.css`, `templates/site.js` (new)
- The four generated `site/` files specified above plus Geist WOFF2/license assets (new)
- `templates/fonts/` — official Geist assets and license, copied into site assets (new)
- `scripts/check_site.py`, `tests/test_site.py` (new)
- `.github/workflows/validate.yml`, `.github/pull_request_template.md`
- `README.md`, `CONTRIBUTING.md`, `docs/site.md` (new documentation)
- This plan and its row in `plans/README.md`

**Out of scope:** Authored agent data or schema changes, archive capture changes,
changes to existing evidence conclusions, the external-link scheduler, edits to
`steel-web-minimal`, a frontend framework/package manager, an API/database,
analytics, accounts, a custom domain, visual graph layouts, comparison tools,
and independently hosted detail pages. Existing generated Markdown/JSON should
remain byte-identical except for explicitly authored README navigation edits.

## Git workflow

Preserve all existing changes. If dispatched into an isolated worktree, transfer
the reviewed Plans 002–003 baseline first, including `docs/evidence-review.md`.
Use a branch such as `feat/generated-mini-page`; compare your result against the
transferred baseline rather than claiming existing modifications as your own.
If commits are authorized, follow the repository's Conventional Commit style,
for example `feat(site): generate searchable catalog page`. This plan does not
itself authorize a push or live publication.

## Steps

### Step 1: Establish the baseline and record the output boundary

Read the current files and capture the working-tree baseline. Run the existing
verification gates below. Confirm the normalized joins and data counts from
the current data, treating the recorded counts as drift indicators, not fixtures
to hard-code in the renderer. Record the reference style and generation layout in
`docs/site.md`, including which files contributors edit and the local preview command.

**Verify:** `uv run --locked python scripts/build.py --check` and
`uv run --locked python -m unittest discover -s tests` → exit 0, all baseline tests pass.

### Step 2: Generate the complete static page

Add the template, source assets, renderer, four base outputs, and Geist assets. Start with complete
HTML and readable no-JavaScript content; then apply the design direction.
Keep every claim connected to its evidence. Build all IDs deterministically;
use distinct entry, claim, and source ID namespaces where necessary to prevent
duplicates when a summary is also repeated in expanded content.

**Verify:** `uv run --locked python scripts/build.py`, followed by
`uv run --locked python scripts/build.py --check` → exit 0, all outputs current.
`cmp data/agents.json site/agents.json` → exit 0.
`uv run --locked python -m unittest discover -s tests -p 'test_site.py'` → renderer tests pass.

### Step 3: Add filtering and shareable entry links

Implement progressive enhancement in `templates/site.js`, using DOM properties,
native controls, and `hidden` to filter pre-rendered entries. Keep focus on the
control being used. Announce result counts through a polite live region, without
announcing the entire catalog. Make permalink navigation, direct loading, query
restoration, and back/forward navigation agree. Preserve reduced-motion behavior.

**Verify:** rebuild and run `--check`; both exit 0. Execute the browser acceptance
matrix below and record expected/actual results in `docs/site.md`. Failures are
implementation work to resolve, not items to silently leave for the user.

### Step 4: Validate the deployable artifact

Add `scripts/check_site.py --root site` (default root `site`) using standard-library
HTML parsing and filesystem inspection. Validate the explicit output allowlist, including Geist font/license assets,
nonempty output, required landmarks, duplicate IDs, local `href`/`src` targets,
fragment targets, and relative-asset behavior. Reject unexpected files, symlinks,
paths escaping the output root, or executable URL schemes. Check the generated
HTML and JSON against the source catalog for entry/claim/source coverage.
External citations are not fetched by this checker; the existing scheduler owns that job.

Include output text in the existing privacy-check function's coverage during
tests or an explicit artifact scan, so new untracked files are checked before
staging. Keep the existing tracked-file privacy gate intact.

**Verify:** `uv run --locked python scripts/check_site.py --root site` → exit 0,
with a concise successful validation message. The checker must also pass for a
temporary copy nested under `internal-agents-map/` and fail on fixtures containing
a missing asset, bad fragment, duplicate ID, or escaping path.

### Step 5: Connect validated output to GitHub Pages

Extend `.github/workflows/validate.yml` rather than creating an independent
deployment path that could race or bypass validation:

1. Keep all existing checks and the `validate` job name. Add the site checker
   after the generated-file check. Do not rebuild before `--check` in CI; that
   would hide stale committed output.
2. Keep PRs validation-only. For pushes to `main` and optional manually triggered
   runs on `main`, upload **only `site/`** after every validation step passes.
   Never publish the repository root or archive tree as the Pages artifact.
3. Add a deployment job with `needs: validate`, a main-branch and event guard,
   the `github-pages` environment, and the deployed URL as its environment URL.
   Restrict `pages: write` and `id-token: write` to deployment-related jobs;
   retain `contents: read` for validation.
4. Use GitHub's maintained Pages actions and full verified commit pins, with
   readable version comments. Serialize Pages deployments with a concurrency
   group so older runs cannot finish after newer deployments. Ensure PR runs
   cannot cancel publication through the same concurrency group.
5. Document the initial repository setting (Pages source: GitHub Actions), the
   prospective project-path URL, and rollback by deploying a previously validated
   revision. Record the actual URL only after a successful authorized deployment.

The deployment contract follows [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages),
checked on 2026-09-09. Verify current action pins when implementing.

**Verify:** tests in `tests/test_site.py` parse the workflow and assert deployment
depends on validation, PRs cannot upload/deploy, and the artifact path is `site/`.
Use a YAML loader that preserves `on` as a key; PyYAML's default YAML 1.1 rules
otherwise interpret it as a boolean. Remote acceptance, when publication is
authorized, requires a successful Actions run plus HTTP 200 for the page, CSS,
JavaScript, and JSON at the actual project URL.

### Step 6: Document and finish verification

Add the page/local preview entry point to README and explain automatic updates
in CONTRIBUTING and `docs/site.md`. Extend the PR checklist with the site and
privacy checks. Run every gate below, record browser checks and any deployment
result, then update this plan and the index. If only local implementation was
authorized, report publication as pending rather than claiming a live site.

**Verify:** all final gates exit 0; a baseline comparison shows no unrelated
data/archive changes. Rebuilding twice produces identical website bytes.

## Commands and final gates

Run from the repository root. Setup may be skipped if the locked environment is current.

| Purpose | Command | Expected result |
| --- | --- | --- |
| Setup | `uv sync --locked` | Exit 0 |
| Generate | `uv run --locked python scripts/build.py` | Writes current outputs |
| Archives | `uv run --locked python scripts/archive_sources.py --check` | Declared captures validate |
| Generated output | `uv run --locked python scripts/build.py --check` | All outputs current |
| Privacy | `uv run --locked python scripts/check_private_data.py` | No prohibited contact data |
| Lint | `uv run --locked ruff check .` | All checks pass |
| Formatting | `uv run --locked ruff format --check .` | No changes needed |
| Tests | `uv run --locked python -m unittest discover -s tests` | Existing and new tests pass |
| Markdown links | `uv run --locked python scripts/check_links.py --local` | Local links pass |
| Site artifact (new) | `uv run --locked python scripts/check_site.py --root site` | Site validates |
| Data parity | `cmp data/agents.json site/agents.json` | Exit 0 |
| Patch whitespace | `git diff --check` | Exit 0 |
| Preview | `uv run --locked python -m http.server 8000 --bind 127.0.0.1 --directory site` | Local page served; stop after review |

Existing tracked-file checks do not include new untracked documentation.
Validate new files explicitly before staging, then run the standard checks again
once those files are tracked as part of the authorized Git workflow.

## Test plan

Use `tests/test_site.py` for focused renderer, artifact, and workflow tests;
extend `tests/test_build.py` only for build integration. Follow its existing
importlib loading and `unittest` conventions. Meaningful coverage includes:

- Every approach and claim in the normalized fixture is reachable in HTML;
  counts and filter options reflect the fixture, including empty and unknown values.
- Kind overrides, low-confidence metrics, missing optional metric fields,
  multiple scoped operating models, and contradictory/contextual evidence retain
  their meaning. Include the Uber conflict as a regression fixture.
- Quotes, ampersands, markup-like prose, and non-ASCII text survive as text;
  generated catalog values cannot become HTML elements or executable attributes.
- Original and archive citations are distinct; missing Wayback/PDF values produce
  no fabricated links. The downloaded JSON is unchanged.
- Repeated generation is byte-identical, and missing or stale HTML/CSS/JS/JSON
  makes build `--check` fail. Test in temporary fixtures, not by corrupting checked-in output.
- The artifact checker detects broken paths, fragments, duplicate IDs, escaping
  paths, symlinks, and extra files; root and nested output directories pass.
- CI upload/deploy conditions, artifact boundary, and dependency on successful validation.

### Browser acceptance matrix

Use an available browser tool at desktop (approximately 1440px), tablet (800px),
and mobile (390px), plus 200% zoom. Record the tool/browser and results; source
inspection alone is not a substitute for these implementation checks.

| Action | Expected behavior |
| --- | --- |
| Initial load | Catalog is visible, counts agree with data, no console errors or missing assets |
| Search `Stripe`, then clear | Matching Stripe entry, then full result set |
| Combine work/type/supervision filters | Results satisfy all active filters; multiple scopes match by any boundary |
| Search for an absent term, then reset | Clear empty state, then full catalog with defaults restored |
| Expand metrics/evidence | Full caveats, provenance, source titles, and locator text remain readable |
| Open a permalink, reload, back/forward | Requested entry is open and visible; controls and URL stay consistent |
| Disable JavaScript | Full catalog, disclosures, citations, and navigation still work; inactive controls are hidden |
| Keyboard only | Skip link, filters, disclosures, permalinks, and sources reachable; visible focus; no trap |
| Mobile and zoom | No page-wide horizontal overflow, clipped labels, or overlapping controls |
| Serve under project subdirectory | CSS, JavaScript, JSON, fragments, and navigation work without root-path assumptions |

## Done criteria

- [x] Authored templates/assets generate the complete page through the existing build.
- [x] Counts, summaries, metrics, and evidence derive from the validated normalized catalog.
- [x] Search, filters, disclosures, URL state, and no-JavaScript reading pass the browser matrix.
- [x] Design follows the supplied reference and passes desktop/mobile/keyboard review.
- [x] All final command gates pass, including explicit checks of new files.
- [x] CI validates PRs and permits publication only from validated `main` runs.
- [x] Documentation explains editing, regeneration, preview, initial Pages setup, and rollback.
- [x] Actual publication status is recorded accurately; the deployed page and all assets return HTTP 200.
- [x] Only in-scope changes are introduced relative to the preserved starting baseline.
- [x] This plan and the index reflect the result; no publication prerequisite remains.

## STOP conditions

- The normalized schema or evidence model has changed incompatibly: reconcile the
  plan before adapting fields or silently dropping evidence.
- The completed Plans 002–003 baseline is absent from an isolated checkout:
  obtain the reviewed baseline instead of rebuilding from the older commit.
- Implementation requires editing agent claims, captured evidence, the sibling
  design project, or introducing a backend: report the mismatch in scope.
- Pages is unavailable or a pre-existing domain/deployment conflicts with the
  proposed target: finish the local artifact and report the concrete deployment
  constraint before changing unrelated hosting settings.
- A verification repeatedly fails after two reasonable fix attempts: record the
  exact failure and remaining work; do not mark the plan DONE.

## Maintenance notes

When fields or claim kinds change, review the renderer and its unknown-value
behavior alongside the schema. Keep generation free of network dependencies and
source-fetching side effects. Add new website files to the explicit artifact
allowlist and generated-output check. Keep Pages dependent on every required
validation gate, and update repository documentation links if the repository moves.
Revisit pagination or separate entry pages only when catalog size makes the
single-page document measurably inconvenient.

## Execution amendment — 2026-09-09

The user requested execution and a goal, replacing serif typography with Geist.
Use self-hosted official Geist fonts and retain their license; font assets are now
in scope. Preserve the template’s layout, spacing, and restrained palette.

Execution research verified official Geist 1.5.1 commit
`3c80bfcc1ba4988ece0eda46a282e15d29e61bbf` and its OFL license.
GitHub Pages was absent at preflight; the repository is public and the current
account can administer it. Publish only after the completed artifact passes review.

## Execution review — 2026-09-09

Implementation approved after isolated execution against baseline `58ec948`,
which preserved the completed Plans 002–003 work. The page covers all 39 approaches,
555 claims, and 88 sources. All 116 tests and required command gates passed in
independent review. Browser checks passed at desktop, tablet, and mobile widths,
including search/filter combinations, history and permalink restoration, keyboard
access, no-JavaScript reading, and a project subdirectory. The 200% check used
CSS layout zoom, not browser-toolbar zoom; the method is recorded in `docs/site.md`.

The renderer supports binary font outputs, the artifact checker checks font URLs
and untracked output, and publication follows successful validation. Font bytes
match the pinned official Geist asset. OFL wording is unchanged; trailing whitespace
was normalized to satisfy the repository patch check. The reviewed implementation
introduces no changes to catalog evidence or preserved sources.

GitHub Pages is now configured for workflow publication with HTTPS at
`https://steel-experiments.github.io/internal-agents-map/`. Publication completed successfully from commit `abf98875f107c70bd929d2030839be33c5d1b3a0`.
Both validation and deployment jobs passed in Actions run `34336076085`.
The public HTML, CSS, JavaScript, JSON, Geist font, and license return HTTP 200
and exactly match the validated artifact. A live Chromium check confirmed all
39 entries, loaded Geist, search, evidence disclosures, and permalink reload
without console or request errors. The goal and plan are fulfilled.
