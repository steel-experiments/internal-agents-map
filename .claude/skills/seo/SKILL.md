---
name: seo
description: Run the recurring (monthly) SEO pulse for internal-agents.com. Refreshes DataForSEO search-volume, cost-per-click, and trend data for the tracked terms, reads the Google position of the catalog for the terms it can own, audits the published routes by template family for head, structured-data, and thin-page defects, then writes a dated report against the previous month. Use this skill for a monthly or weekly SEO check, an SEO progress report, a ranking update, a search-health or regression audit, or questions such as "how is the catalog doing in search", "is anyone finding the map", "refresh the SEO data", or "SEO report". Use it also to add, remove, or change the tracked keywords, the route families, or the impression sinks.
---

# SEO pulse for internal-agents.com

A repeatable **monthly** check of one static site: the catalog at **internal-agents.com**. It
answers "is the map being found, and what moved since last month?" It joins DataForSEO keyword
and position data with an audit of every published route, then writes a dated report.

The site is generated: 103 routes come from six templates. A defect is normally a **template
defect on every page of a family**, and a win is normally a template win. The scripts therefore
report by family, not page by page.

## What it produces

- **Snapshots** in `.seo/snapshots/` (`perf-`, `queries-`, `volumes-`, `ranks-`, and
  `tech-YYYY-MM.json`). They are the state of this month; the next run compares against them.
  Git ignores them. The first run of each script has nothing to compare against and says so:
  it is the baseline.
- **`docs/seo/pulse-YYYY-MM.md`**, the report. It is the deliverable, and it is committed, next
  to the other dated reviews in `docs/`. `npm run verify` checks the links of committed Markdown,
  so every link in the report must resolve.

## Prerequisites

- **DataForSEO credentials** in a repository-root `.env`: `DATAFORSEO_AUTH=<base64 login:password>`,
  or `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`. Git ignores the file. If it is missing, ask for
  the credentials before Phase 1; do not invent numbers. The account must be verified and hold
  credit, because positions cost money. Keys stay in `.env`: never write one into a report, a
  snapshot, or a commit.
- **A build**, for the technical audit against `dist/`: run `npm run build` first. The audit reads
  `routing-manifest.json` and `dist/`, or the live site with `--live`.
- Run every script **from the repository root**.

## What this audit does not cover

`scripts/check_site.py` holds the structure of the build and `scripts/check_delivery.py` holds
the redirects, the headers, and the canonical `Link` header. Both run in `npm run verify`. This
skill does not repeat them. It holds what a search engine and a reader see: titles, descriptions,
canonical links, structured data, repeated head text, and pages with too little catalog text.

The Markdown twins (`/agents/<id>.md`) are not duplicate content: each one is served with a
`Link: rel="canonical"` header to its HTML page, and `check_delivery.py` proves it. Do not report
them as a defect. Watch them only as impression sinks.

## How to read the numbers

The keyword data comes from `keywords_data/google_ads/search_volume/live`:

- It is **Google Ads planner data**: United States, in buckets, and it under-reports the terms of
  a young subject. A volume of `10`, or `null`, means "below the reporting threshold", **not no
  demand**. Most of the catalog's own vocabulary lives there.
- `paid_competition` is **advertising competition, not the difficulty of ranking**. A term with
  low paid competition can still be held by vendors and news sites.
- `cpc` shows commercial intent. The catalog does not sell anything, so a high cost per click is
  a weak signal here: it usually marks a term that vendors will always outrank.
- `trend` holds the last 12 months. A rising term is worth more than a large flat one, because
  the catalog can arrive early on a subject that is still forming.

So weight **momentum and ownability**, and treat every number as a direction, not a measurement.

### What the catalog can own

Do not recommend competing for head terms. The catalog wins on questions its records answer:

- **Entry pages** (`/agents/<id>`) answer "what did this organization build?" Terms of the shape
  *organization plus system name* are the most ownable pages on the site.
- **Organization pages** (`/organizations/<id>`) answer "what has this organization published?"
  They are short by design, so their lever is more records for that organization, not more words.
- **Notes** (`/notes/<slug>`) answer a design question across records. They are the right home for
  a concept term that no single record owns.
- **Guides** (`/definitions`, `/methodology`, `/infrastructure`) answer "what counts as an internal
  agent, and how was this decided?" They are the home of definitional terms.

**Evidence decides what gets built, never demand.** A term with demand and no source behind it is
not an opportunity: it is out of scope. Recommendations that need a new record must go through
[CONTRIBUTING.md](../../../CONTRIBUTING.md#inclusion-rules) and the `add-agent-from-url` skill.
Never propose a page that the catalog cannot support with sources.

### Impression sinks

`/llms.txt`, `/agents.json`, and the Markdown twins answer machines. If one of them collects
impressions that no person clicks, it moves every site-level number away from what the catalog
pages do. `config.json` holds `impression_sinks` for exactly those pages, and the performance
report always prints the site **with and without** them. The list starts empty. **When you report
a site-level clicks, impressions, or click-through number, report the figure without the sinks
next to it** and name what was excluded. Never remove the exported figure: a change in the sinks
themselves must stay visible.

## The monthly workflow

The scripts hold the mechanical part and write the snapshots. You hold the synthesis and the
judgment. Run them in order from the repository root.

### Phase 0: Search performance (needs an export)

```bash
node .claude/skills/seo/scripts/gsc-perf.mjs <search-console-pages-export.csv>
```

Ask for two Search Console exports for internal-agents.com, last 3 months, CSV: **Pages** and
**Queries**. The pages script prints the site with and without the sinks, the totals of each route
family, the pages with the most clicks, and the count of pages that collect impressions and no
clicks.

```bash
node .claude/skills/seo/scripts/gsc-queries.mjs <search-console-queries-export.csv>
```

The queries script separates brand searches (`query_rules.brand_pattern`) from searches for the
subject, lists the **striking-distance** queries (the catalog appears at position 5 to 20 with
real impressions), and lists the queries with demand that `config.json` does not track. For a
young site this is the best discovery source there is: Search Console shows what Google already
tries the catalog for, where the planner data shows `null`. A striking-distance query names the
page to work on and the term its title should carry.

Without the exports, skip the phase and say so in the report. Do not quote a click-through rate
from memory.

### Phase 1: Demand

```bash
node .claude/skills/seo/scripts/dfs-volumes.mjs            # every tracked keyword
node .claude/skills/seo/scripts/dfs-volumes.mjs --limit 10 # a cheap check that it works, writes no snapshot
```

Reads volume, cost per click, and the 12-month trend of `tracked_keywords`, writes
`volumes-YYYY-MM.json` and `movers-YYYY-MM.json`, and prints the movers (a volume change of 50 or
more, or a trend change of 25% or more). A run that reads nothing, and a run with `--limit`, write
no snapshot: neither can become next month's baseline and hide the keywords it did not read.

### Phase 2: Positions (this phase spends credit)

```bash
node .claude/skills/seo/scripts/dfs-rank.mjs
node .claude/skills/seo/scripts/dfs-rank.mjs --limit 8     # when the balance is low
```

Reads the Google position of internal-agents.com for `rank_keywords`, records the page that ranks
and **which family it belongs to**, keeps the top three results for each term, and prints the
changes. Which family earns the positions is the useful signal: it says which template to invest
in. A run with `--limit`, or a run that lost keywords to an empty balance, marks its snapshot
`partial`. On `40200` the balance is empty: stop, ask for credit, and write in the report that
position tracking is incomplete.

### Phase 3: Technical audit (free)

```bash
npm run build
node .claude/skills/seo/scripts/tech-audit.mjs                 # reads dist/
node .claude/skills/seo/scripts/tech-audit.mjs --live          # reads the production site
node .claude/skills/seo/scripts/tech-audit.mjs --family entry  # one family, writes no snapshot
```

Reads every route of `routing-manifest.json` and checks the status, the title, the description,
the canonical link, `noindex`, the structured-data nodes each family must carry, the count of h1
elements, the Markdown alternate link, and the words of the `main` element against the family
floor. Across pages it finds **repeated titles and descriptions**, which is the defect a generated
catalog produces most easily, and it compares the sitemap with the published routes. It prints a
defect once for each family with the number of pages it affects, then the changes since the last
snapshot: new defects, resolved defects, changed titles, and pages added or removed.

Use `dist/` before a release and `--live` to confirm what is published. A run limited to one
family writes no snapshot, so it cannot replace the baseline of the month.

### Phase 4: Drift and discovery (your judgment)

The scripts cannot see a subject forming or a competitor moving.

- Start with the striking-distance and untracked queries from Phase 0. They are demand the site
  already receives; each one is a title or description change, or a term to add to tracking.
- Read the movers from Phase 1. In this subject a rising term usually means an organization has
  just published something. That is a lead for the catalog, not only for a page.
- For 3 to 5 ownable terms, use `WebSearch` and record what changed: a new list of agent case
  studies, a vendor page that now answers the question, or a catalog page that started ranking.
- Compare the catalog against the demand: which organizations or kinds of work appear in the
  movers and have no record? Add them to `docs/coverage-backlog.md` as leads, with the source.
- Propose keywords to add to `config.json` next month.

### Phase 5: The report

Write `docs/seo/pulse-YYYY-MM.md` (create the directory if it is missing) from the three script
summaries and your Phase 4 notes:

```markdown
# SEO pulse, YYYY-MM

Against: YYYY-MM. Written: YYYY-MM-DD.

## Summary
Two to four sentences: is the catalog found, what moved, what is the largest defect, what is the
largest opportunity.

## Search performance
| View | Clicks | Impressions | Click-through |
| --- | --- | --- | --- |
| Site as exported | | | |
| Site without the sinks | | | |

Name the excluded pages with their impressions. Compare against last month on the second row.
Follow with the family table: which templates earn the impressions and the clicks.

## Demand
- Rising: term, previous to now, why it matters, what it suggests.
- Falling: term, previous to now.
- Terms with demand and no record: leads for the catalog, with the source.

## Queries
Brand share, then the striking-distance queries with the page each one names, then the untracked
queries worth adding. Compare brand share against last month: a falling share means the subject
is finding the site.

## Positions
The terms that hold a position, the page and family that holds it, and the change since last
month. State when position tracking was incomplete and why.

## Technical health
Defects by family with the number of pages affected, repeated titles or descriptions, the sitemap
result, and the changes since last month. Say which are template fixes in `src/` and which are
record fixes in `data/agents/`.

## Drift and discovery
What changed in the results, and which keywords to track next month.

## Actions
Three to six items in priority order, each named as a template change, a record change, or a
research lead. Every item that needs new catalog text must name the source that supports it.
```

Keep it short. Lead with what changed.

## How to prioritize

- **Template before page.** A fix in `src/layouts/SiteLayout.astro` or a page template moves every
  page of the family at once. A description that is too short on 35 organization pages is one
  change in `src/pages/organizations/[id].astro`.
- **Evidence before demand.** More sources on an existing record beats a new page for a term.
- **Position before volume.** A striking-distance query, where the catalog already sits at 5 to
  20, is worth more than a larger term where it does not appear. The fix is on one page and is
  usually its title.
- **Ownability.** Entry and note pages can win; head terms belong to vendors.
- Say which files an action touches: `src/` for templates, `data/agents/*.yaml` for records,
  `src/content/notes/` for notes, `config.json` for tracking.

## Configuration and maintenance

Everything tracked lives in `.claude/skills/seo/config.json`.

- The catalog is the keyword list. Run `node .claude/skills/seo/scripts/catalog-terms.mjs
  --untracked` to list the *organization plus system name* terms of records nobody tracks yet,
  and add the ones with a searchable name to `rank_keywords`. A generic name such as "internal
  coding agent" is not a term anyone types: skip it.
- Add terms to `tracked_keywords` as the subject grows, and to `rank_keywords` only when the
  catalog can realistically hold a position. Move a query from the untracked list of Phase 0 into
  `tracked_keywords` once it appears two months in a row.
- Review `query_rules` when the site gets a new name or alias, so brand searches stay separate.
- Add a `route_families` entry when the site publishes a new kind of page, with the structured-data
  nodes it must carry and a word floor below what the family holds today, so the floor reports a
  loss of content and not the normal size of the page.
- Add a page to `impression_sinks` when it collects impressions that nobody clicks, and remove it
  when it stops.
- Review `page_rules` when the title formula changes in `src/lib/metadata.ts`.

## Cost

- Volumes: about $0.02 for each run, in batches of 25 keywords. Run it freely.
- Positions: about $0.05 to $0.10 for each keyword, so about $1.50 for the full set. This is the
  phase that spends money. Use `--limit` when the balance is low, and stop on `40200`.
- Technical audit: free. It reads local files, or fetches the live pages.
- Search performance and queries: free. They parse the exports.
- Catalog terms: free. It reads `data/agents.json`.

Without DataForSEO you can still run Phase 0, Phase 3, and a qualitative Phase 4 with `WebSearch`.
Record the gap in the report; do not skip the pulse.
