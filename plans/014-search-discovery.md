# Plan 014: Make the catalog findable through search

> Requested on 2026-09-21 as a plan. Implementation is not authorized by this
> document. Each phase names its own approval gate; template changes that touch
> every page and any new page type need explicit approval before work starts.

## Status and baseline

- Priority P1; effort L across five phases, each phase S to M on its own.
- Category: discovery, metadata, and derived content.
- Planned on 2026-09-21 on `main` at `46267d5`, with the SEO pulse skill and its
  first report staged and uncommitted (`.claude/skills/seo/`,
  `docs/seo/pulse-2026-09.md`).
- Baseline, from the [first SEO pulse](../docs/seo/pulse-2026-09.md): 103 routes,
  56 records, 35 organizations, 7 notes. One term in Google's top 20, the site's own
  name at position 10 under the legacy `/definitions.html` name. Every subject term and
  every *organization plus system* term is held by the primary source and news sites.
  No critical or high technical defect; the medium defects are all template-level.
- Search Console has never been read for this site. The Google Ads planner returns
  `null` or `10` for the catalog's own vocabulary, so the planner cannot measure this
  subject. Search Console can.
- Other agents edit this checkout. Stage explicit paths only; never `git add -A`.

## Why this matters

The catalog answers questions nobody else answers with sources: what did this
organization build, how much does a person supervise it, and where is the evidence.
Today those answers reach readers through the GitHub repository and direct links.
Search does not send anyone, because the pages do not yet say, in the places a search
engine reads, which question they answer. The pages are sound. They are anonymous.

The competing results are lists that sell something (MagmaLabs, TechRev, tkxel), a
paywalled Substack deep dive with the same organization list and no sources, and, on
each system's name, the organization's own post followed by LinkedIn, YouTube, and one
or two secondary write-ups. The catalog's entry pages are the natural third result on
every *organization plus system* term and hold none of them. The argument for that
position is provenance. This plan makes the provenance visible to machines and readers
who arrive from a search, without adding one unsourced sentence.

## Principles that bound every phase

1. **Evidence decides what gets built, never demand.** No page, title, or description
   contains a claim the records do not carry. A term with demand and no source is out of
   scope ([inclusion rules](../CONTRIBUTING.md#inclusion-rules)).
2. **Template before page.** A change in one template moves 35 or 56 pages at once. Do
   not hand-edit generated text on individual pages.
3. **Derive, do not author.** Every new page and every new head text is a function of
   record fields (`company`, `agent_name`, `domains`, `approach_type`, counts,
   `last_reviewed_at`). The precedent is Plan 013: organization pages are a derived
   index, not a profile.
4. **Design is unchanged.** `DESIGN.md` and the Plan 013 constraints apply: `SiteLayout`,
   `AgentCard`, Sand tokens, 684px column, no new navigation, no hero, no stats strip.
5. **Measure before and after.** The SEO pulse skill runs before the first phase and
   after each phase's release. Snapshots are the record of what moved.

## Product contract

- Every canonical HTML page carries: a title of at most 70 characters that names the
  subject and the work, a description of 110 to 160 characters derived from the record,
  the canonical link to its clean path, one `h1`, and structured data with the nodes
  of its family. The `tech-audit.mjs` families and `page_rules` in
  `.claude/skills/seo/config.json` are the contract; the audit is the test.
- The subject organization of an entry or organization page is an `Organization` node
  in the page's structured data, with the registry `homepage` as `url`, so the page is
  machine-readably *about* that organization. No claim about the organization beyond
  its name and website.
- A derived index exists for each work domain at `/work/<domain>` (14 today), built
  exactly as Plan 013 built organizations: `AgentCard` previews, agents and
  infrastructure listed separately, no authored text beyond the domain label and a
  derived count sentence. It appears in the sitemap, `llms.txt`, and the routing
  manifest, with Markdown parity. Approval gate: this is a new page type.
- Every entry page has a social preview image that shows the organization logo, the
  system name, and the site name, generated at build time from the same registry
  assets; pages without a permitted logo (HubSpot, Microsoft, Sierra) use the
  wordless variant. Approval gate: adds a build step and 56 images.
- Search Console and Bing Webmaster Tools hold verified properties for
  `internal-agents.com`, with the sitemap submitted. The monthly pulse reads their
  exports.
- URLs, exports, redirects, and the delivery contract of `check_delivery.py` do not
  change. The sitemap still carries no `lastmod`: the review date describes a review,
  not a content change, and that decision stands.

## Scope

In scope: head metadata templates, structured data, derived domain pages, social
preview images, internal links between derived pages, Search Console setup, an outreach
list, notes chosen against measured queries, the pulse as the measurement gate.

Out of scope: any authored profile text, ratings, or aggregate metrics; paid search;
link purchases or directory submissions; a blog; changes to the notes' voice or the
`notes-writing.md` guide; `lastmod` in the sitemap; new navigation items; redesign.

## Implementation steps

Execute the phases in order. Each phase ends with `npm run verify`, a pulse
(`tech-audit.mjs` against `dist/`, then `--live` after release), and a status update in
this file. Stop at every STOP line and report; do not continue into the next phase on
the same authorization.

### Phase 0. Measure, and open the door (S, no code, no approval needed)

1. Verify `internal-agents.com` in Google Search Console (DNS record, since the site is
   static and the publisher owns the domain) and in Bing Webmaster Tools. Submit
   `https://internal-agents.com/sitemap.xml` in both. **Done on 2026-09-21** by the
   owner. Data starts at verification; the first usable exports are two to four weeks
   out.
2. Request indexing of `/definitions`, `/`, `/infrastructure`, `/methodology`, and
   `/notes` so the index moves from the legacy `.html` names to the clean paths. The
   redirects already exist; this only asks for the recrawl.
3. Export **Pages** and **Queries**, last 3 months, CSV, and run
   `gsc-perf.mjs` and `gsc-queries.mjs` from the pulse skill. Record the baseline in
   `docs/seo/pulse-2026-09.md` under Search performance and Queries (replace the two
   "Skipped" sections; keep the rest).
4. Publish the catalog's existence where the publisher already speaks: a link from
   `steel.dev` and `docs.steel.dev` (the publisher's own domains, the one backlink fully
   under our control), the `steel-dev` GitHub organization profile, and the repository
   description. Record where each link lives.

STOP: report the baseline numbers and the striking-distance queries. They decide the
order of notes in Phase 4.

### Phase 1. Fix what the first pulse found (S, template edits, approval to touch `src/`)

Files: `src/pages/organizations/[id].astro`, `src/lib/organization-view.ts`,
`src/pages/infrastructure.astro`, `src/content/notes/*.md` (three `description:`
lines and one `title:`), and their Markdown twins through the shared view.

1. Organization description, derived: `"<n> agents and <m> infrastructure records
   documented at <Company>: <domain labels, comma-separated>."` Omit the empty count.
   Check the result lands in 110 to 160 characters for every organization in the test.
2. Organization `BreadcrumbList`: Directory → Company, the same shape entry pages use.
3. `/infrastructure` title to at most 70 characters: drop the trailing
   "How companies build internal AI agents" segment or the middle site-name repeat, and
   lengthen its description with a second derived sentence (count of platform and
   supporting-pattern records).
4. Notes `work-can-continue` (title 73), `steps-without-a-model`, `test-on-your-work`,
   `work-can-continue` (descriptions 46 to 51): a second sentence in `description:` that
   names the question the note examines, in the note's own voice. The title of
   `work-can-continue` is authored; shorten the " · Notes" segment in the notes template
   only if the author declines to shorten the title.
5. Entry pages `airbnb-pascal` and `dropbox-deflaker`: the description is the record
   `summary`, which is short. Lengthen only with sourced text, or leave it. Do not pad.

Gate: `tech-audit.mjs` reports zero medium defects in the organization and guide
families; `tests/web/organizations.test.ts` asserts the description shape and the
breadcrumb node; `npm run verify` passes.

STOP: request release approval.

### Phase 2. Titles and structured data that name the subject (M, every page, explicit approval)

The entry title formula is `"<System> at <Company> · Internal Agents Map"`. It names the
subject and never the work. A person searching "notion security agent" or "stripe
coding agents" does not see a match. Derive the work from `domains`.

1. Entry title: `"<System>, <Company>'s <domain label> agent · Internal Agents Map"`
   for one domain; `"<System> at <Company>: <domain 1> and <domain 2> agent"` for two;
   the current formula plus the first domain for three or more. Platforms and
   supporting patterns use `platform` or `component` in place of `agent` (the labels in
   `src/lib/labels.ts`). Compute the length in the unit test for all 56 records; any
   result over 70 characters falls back to the current formula. Files:
   `src/pages/agents/[id].astro`, `src/lib/entry-view.ts`, `tests/web/entry-view.test.ts`.
2. Entry description: keep `"<Company> — <System>. <summary>"`, and when the summary
   leaves the total under 110 characters, append the supervision level sentence the
   page already renders (`levelLabel`) so the description is derived, not padded.
3. `about` node: on entry and organization pages add
   `{ "@type": "Organization", "name": <company>, "url": <homepage> }` to the page's
   graph and reference it from `WebPage.about`. On entry pages add
   `WebPage.mainEntity` as a `Thing` with the system name only. No `SoftwareApplication`,
   no ratings, no `offers`.
4. Extend `route_families` in `.claude/skills/seo/config.json` with the `Organization`
   node expectation for entry and organization pages, so the audit holds the new
   contract.

Gate: `tech-audit.mjs` shows no title over 70 and no repeated title;
`exports.test.ts` proves the Markdown twins and JSON exports carry the same title; the
`og:title` follows. Position tracking in the next pulse is the measurement: the
*organization plus system* terms are where this phase must show.

STOP: this changes the title of every page and the social preview text. Request
explicit approval with the full list of 56 new titles from the test output.

### Phase 3. Derived work-domain pages (M, new page type, explicit approval)

The queries "ai code review agents at companies" and "companies using ai agents for
X" have no page on the site that answers them. The home directory answers them only
through a client-side filter, which is not indexable by design (the sitemap excludes
filter URLs).

1. Routes: `/work/<domain>` for each domain in `data/agents.json`, from a new
   `workPaths(catalog)` in `src/lib/routes.ts` next to `organizationPaths`. Reserved
   names and slug rules as for organizations. Add to `publicationRoutes`, the routing
   manifest, `sitemap.xml`, `llms.txt`, and `check_site.py` coverage.
2. View: `src/lib/work-view.ts`, a sibling of `organization-view.ts`: label from
   `termLabel`, agents and infrastructure grouped separately, `AgentCard` previews sorted
   as the directory sorts them, and one derived sentence:
   `"<n> agents and <m> infrastructure records do <domain label> work at <k>
   organizations."` No further prose.
3. Page: `src/pages/work/[id].astro` and `[id].md.ts`, `SiteLayout` with `current`
   omitted, title `"<Domain label> agents · Internal Agents Map"`, `WebPage` +
   `BreadcrumbList` + `ItemList` of the records. Reuse `organization-page` styles; add
   none.
4. Links: each entry page's work tags become links to the domain page (the tag stays a
   14px rounded tag; only its target changes). The home directory's domain filter
   chips do not change. Each domain page links back to the directory in its breadcrumb.
5. Tests: `tests/web/work.test.ts` mirroring `organizations.test.ts` (route set equals
   the domain set, empty sections omitted, Markdown parity), plus the E2E path list.

Gate: `check_site.py`, `check_delivery.py --preview`, and the full `verify`. The audit's
new `work` family (add it to `config.json` with `WebPage`, `BreadcrumbList`, `ItemList`,
floor 60 words) reports clean.

STOP: new page type and 14 new routes. Request approval before implementation, then
again before release, with a desktop and mobile review as Plan 013 required.

### Phase 4. Notes against measured queries (M, content, per-note approval)

Notes are the home of concept terms. Choose the next notes from the Phase 0 query
data and the pulse, not from taste. Today's candidates, in order:

1. Levels of human oversight. `ai agent autonomy levels` is held by arXiv and CSA; the
   catalog has the only public scale with 56 assessed records behind it
   (`/definitions`). A note that reports how three records sit on the scale and why, with
   sources, is the strongest concept page the site can write.
2. Agent evaluation in practice. `agent evals` rose 40% over six months. The catalog
   records that report evaluation (Stripe, Dropbox, DoorDash) carry the evidence.
3. What a code review agent reviews. Twenty-four records carry `code-review`; the
   domain page from Phase 3 lists them, and a note can compare what they look at.

Each note follows `docs/notes-writing.md` (200 to 350 words, ASD-STE100, sources
first, `relatedAgentIds`), and its `description:` carries the query term in plain
words. No note is written for a term the records cannot support.

STOP: each note is authored work and needs its own review.

### Phase 5. Social previews, and the second month (M, build step, approval)

1. Per-entry `og:image`, now specified in [Plan 015](015-social-preview-cards.md)
   with the chosen design and its checks; the description below stands as the
   original intent. A build-time renderer (Astro endpoint or a `scripts/` step)
   that composes the organization logo from `public/logos/` (registry-governed; the
   three monogram organizations use the wordless variant), the system name, and the
   site name on the Sand background, 1200 × 630, into `dist/og/<id>.png`. `SiteLayout`
   takes an optional `ogImage` and entry pages pass theirs. Organization and domain
   pages follow with the logo or label alone. The default `og.png` remains for guides
   and notes.
2. Outreach list, not outreach: `docs/seo/outreach.md` with the organizations whose
   systems are cataloged, the secondary writers on each system's SERP (ByteByteGo,
   InfoQ, Lenny's Newsletter, ZenML, MindStudio), and Department of Product. One line
   each: what they published, what the catalog adds (provenance, the supervision
   assessment, the corrections channel). The message is "we documented your system
   with sources; corrections welcome", never a link request. Sending is a separate
   decision.
3. Run the second pulse. Compare against the September snapshots. Move queries that
   appeared two months running into `tracked_keywords`; add the *organization plus
   system* terms from `catalog-terms.mjs --untracked` to `rank_keywords`.

STOP: the build step adds a dependency (an image renderer). Request approval with the
dependency named and the build time measured.

## Commands

```sh
npm run build
node .claude/skills/seo/scripts/tech-audit.mjs
node .claude/skills/seo/scripts/tech-audit.mjs --live
node .claude/skills/seo/scripts/gsc-perf.mjs <pages.csv>
node .claude/skills/seo/scripts/gsc-queries.mjs <queries.csv>
node .claude/skills/seo/scripts/dfs-rank.mjs
node .claude/skills/seo/scripts/catalog-terms.mjs --untracked
npm run verify
uv run --locked python scripts/check_delivery.py --preview
```

## Done criteria and review order

1. Phase 0: both webmaster properties verified, the sitemap submitted, the baseline
   report holds Search performance and Queries, and the publisher's domains link to the
   catalog.
2. Phase 1: `tech-audit.mjs --live` reports no medium defect in the organization and
   guide families.
3. Phase 2: no title over 70 characters, no repeated title, every entry and
   organization page carries an `Organization` node; the next pulse shows the
   *organization plus system* terms moving from "not in the top 20" to a position.
4. Phase 3: 14 `/work/<domain>` routes in the manifest, sitemap, `llms.txt`, and
   delivery checks; entry tags link to them; design review passed.
5. Phase 4: three notes published against measured queries, each with sources.
6. Phase 5: entry pages carry their own preview image; the outreach list exists; the
   second pulse is written.
7. Overall: three consecutive pulses show rising impressions on the entry family, at
   least five *organization plus system* terms in the top 10, and brand share of
   queries falling as subject searches rise.

## Git, stop conditions and maintenance

- One branch per phase (`plan-014-phase-<n>`), one pull request per phase, `npm run
  verify` green before each request. Stage explicit paths only.
- Stop and report if: a derived description cannot reach 110 characters for some
  organization without authored text (leave it short; report which); a title cannot
  fit 70 characters under any derivation (fall back; report which); the pulse shows a
  position lost after a release (do not revert on one reading; read again next month
  unless the loss is on a brand term); the renderer adds more than 30 seconds to the
  build.
- Never add `lastmod`, a filter URL, or a `noindex` to a canonical page as part of this
  plan. Never write a sentence a record does not support.
- The pulse skill's `config.json` is the living contract: extend its families and
  rules with every phase, so the audit tests what this plan promised.

## Completion record

Planned on 2026-09-21. Execution of each phase requires its own approval as stated at
the phase's STOP line.

- 2026-09-21: Phase 0 step 1 done by the owner. Google Search Console and Bing
  Webmaster Tools verified for `internal-agents.com`; the sitemap is submitted in both.
  Steps 2 and 3 open. Step 4: the GitHub repository has the homepage set, and topics
  `ai-agents`, `astro`, `catalog`, `dataset`, and `internal-tools` were added on
  2026-09-21. The `docs.steel.dev` link is proposed in
  [steel-dev/docs#129](https://github.com/steel-dev/docs/pull/129), from the
  human-in-the-loop guide's "What's Next" list to `/definitions`; it awaits review.
