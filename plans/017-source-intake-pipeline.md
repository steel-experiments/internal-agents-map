# Plan 017: Turn a list of links into a reviewed catalog record

> Requested on 2026-09-22 as a plan after a brainstorm on a repeatable intake pipeline.
> The owner asked for a process that takes one link or a list of links, captures each
> page with Steel, classifies the evidence with Jev, writes the record prose with
> GPT-6 Sol, and produces the YAML record, so that people collect links and sources
> while scripts do the rest. Implementation is not authorized by this document; the
> STOP conditions below name what needs approval first.

## Status and baseline

- Priority P1; effort L. One branch per phase, one pull request per phase.
- Category: editorial tooling. Builds on [Plan 016](016-jev-investigation.md), which
  investigated Jev and reached no-go on automatic publication, and on the
  [schema simplification review](../docs/schema-simplification-review.md), which asks
  for generated bookkeeping, one observation per fact, and stable claim identities.
- Planned on 2026-09-22 on `main` at `9d2be29`, branch
  `claude/plan-017-source-intake-pipeline`.
- Baseline, counted from the working tree on 2026-09-22:

  | Measure | Count |
  | --- | ---: |
  | Records in `data/agents/` | 66 |
  | Source records | 138 |
  | Source records with a repository capture | 122 |
  | Evidence paths (claims with at least one link) | 1,172 |
  | Evidence paths with no locator on any link | 240 |
  | Evidence links without a locator | 292 |
  | Records that rest on one evidence source | about 41 |
  | Sources that are podcasts, talks, or transcripts | 11 |

- Intake today is the [add-agent-from-url skill](../.claude/skills/add-agent-from-url/SKILL.md):
  a coding agent reads the source, decides eligibility, writes the YAML by hand, runs
  the archiver, and runs `npm run verify`. The policy in that skill is good. The
  execution is prose instructions, so no two runs do the same work, nothing records
  which passage a claim came from unless the agent types it, and the agent reproduces
  by hand the evidence map, the claim metadata, and the page-content block that the
  schema review identifies as bookkeeping.
- The archiver, [scripts/archive_sources.py](../scripts/archive_sources.py), already
  captures a page with the Steel CLI to Markdown, writes a hashed manifest, rejects
  interstitial and error pages, respects `noarchive`, attempts a Wayback save, keeps
  bundles append-only, and verifies them offline in `npm run verify`. It keys bundles
  by source ID, which the pipeline does not know until identity is resolved.
- Jev, per Plan 016: typed questions over supplied state, no text generation, about
  $0.042 per million input tokens, 284 ms median for a five-question batch, coarse
  supported-versus-needs-review distinction held on 14 exploratory cases, finer
  verdicts flipped on identical repeats. The runnable harness with a budget cap is in
  [016-jev-eval](016-jev-eval/README.md).
- GPT-6 Sol was released on 2026-09-22 as `gpt-6-sol` in the OpenAI API. Published
  price at planning time: $2 per million input tokens, $10 per million output tokens,
  cached input at 10 percent. Structured output and reasoning effort settings are
  available through the Responses API. No dated snapshot exists yet; the pipeline
  records the model string the API returns on every call.
- Steel: the archiver shells out to the Steel CLI (`0.4.4` in the oldest manifests;
  `0.5.0-preview.6` is installed now). The Python SDK, package `steel-sdk`, exposes the
  same scrape action and returns the page metadata, including title, language, and
  published timestamp, which the CLI path discards today.

## Why this matters

- **Repeatability.** The catalog's value is that every sentence points to a passage.
  A pipeline that finds the passage by machine and refuses a claim without one makes
  that property cheap instead of heroic.
- **The schema review and this pipeline are one project.** If the writer model
  authors today's YAML, the pipeline automates the bookkeeping the review says to
  delete. If the writer model authors a small claim-centric extraction record and code
  renders the YAML, the pipeline becomes the first consumer of the simplified format,
  and the migration of the 66 existing records can follow the same renderer later.
- **The research gaps.** The owner's gap analysis names four: claim traceability
  (240 claims with no locator), evidential independence (single-source records, almost
  no `contradicts` links), currency and drift (no content-drift check), and coverage
  (domain, company-type, and geography skew). The same stages that draft a new record
  also backfill locators from existing captures, compare a second source's numbers
  against the first, and detect drift against a capture.

## Principles that bound every phase

1. **The pipeline drafts. A person decides.** Add, Update, Out of scope, silence, and
   merge are human decisions. Plan 016's no-go on automatic publication stands. No
   stage writes to `main`, opens a pull request, or marks a source reviewed.
2. **A quote, or nothing.** Every reported claim carries a verbatim quote that code has
   found in the immutable capture. A quote that is not found is a failed extraction,
   never a locator. Catalog inferences carry the quotes they reason from and are
   labelled `catalog-judgment`.
3. **Code owns numbers, dates, identities, and IDs.** Jev's own limitations page says
   it is weak on numbers, date comparison, and indirection. Numeric agreement between
   a claim and its quote, date arithmetic, URL normalisation, and claim identity are
   deterministic checks.
4. **Append only.** An Update adds sources, claims, and evidence links at the end of
   their lists. It never reorders, rewrites, or removes an existing claim, because
   public claim IDs are positional today.
5. **Silence needs a person.** The pipeline never writes `unreported`. When no passage
   answers a question, it writes `not-reviewed` with the note that the pipeline found
   no passage in the named sources. The reviewer flips it after reading.
6. **No network in verification.** `build.py --check`, the coverage check, and the
   archive check stay offline. Pipeline stages are separate commands with their own
   budgets, caches, and manifests.
7. **Reuse the validators.** The renderer produces YAML that today's build validates.
   The capture stage calls the archiver's page checks. No second implementation of a
   rule that already exists.
8. **Record every model call.** A run manifest holds the model strings the APIs
   returned, the prompt and question versions, the input hashes, token usage, and cost.
   Source text is untrusted input in every prompt.

## Product contract

- Input: a queue file with one entry per candidate. Each entry has one or more URLs and
  optional hints: company, system name, existing record ID, source role. Nothing else
  is required.
- Output per candidate: a draft record in today's schema under a drafts directory, the
  promoted capture bundles under `archive/sources/`, a company registry entry when the
  organization is new, one review sheet in Markdown, and one run manifest. The draft
  passes `build.py --check` and the coverage check before the pipeline reports success.
- The review sheet lists every claim with its quote, its line locator, its numeric
  check, its Jev verdicts with probabilities, its disposition, and the open questions.
  It names the decision the pipeline proposes and the decision a person must make.
- Existing records change only through the Update path, the locator backfill, and a
  reviewer's edits. Both machine paths are additive and are proposed in the review
  sheet before they are applied.
- The pipeline is reproducible, not deterministic. A rerun with a warm cache is
  byte-identical. A rerun with a cold cache can differ, because the writer model is
  not deterministic; the manifest records which happened.
- Cost is bounded per run. A run refuses to start if its worst-case reservation exceeds
  the budget passed on the command line, and it stops on the first API error. Default
  caps are conservative and are set in the skill configuration.

## Architecture

```text
queue.yaml
  -> 1 capture      Steel        .intake/captures/<url-hash>/  (staging; promoted later)
  -> 2 segment      code         paragraphs with IDs and line ranges
  -> 3 resolve      code + Jev   Add / Update / ambiguous, matched record ID
  -> 4 extract      writer model extraction record: claims + verbatim quotes
  -> 5 verify       code         quote found, line locator, or claim flagged
  -> 6 judge        Jev          relation, actor, temporal status, approval, basis
  -> 7 numbers      code         claim numbers and dates agree with the quote
  -> 8 write        writer model summary, primitives, lessons, confidence reasons
  -> 9 preflight    Jev          each written sentence against its claims
  -> 10 render      code         YAML in today's schema, company entry, captures promoted
  -> 11 validate    build, coverage, archive checks
  -> 12 review      code         review sheet and run manifest
                                 -> a person edits, approves, opens the pull request
```

Two more modes reuse stages without adding new ones:

- **Backfill** (Gap 1): input is an existing record. For each claim without a locator,
  stage 4 proposes the supporting quote from the record's own captures, stage 5 verifies
  it, stage 6 grades it. Output is a proposed evidence link per claim, in the review
  sheet, applied only to `locator` fields after approval.
- **Drift** (Gap 3): input is every source with a capture. Stage 1 rescrapes without
  saving, normalises, and hashes against the capture text. On change it diffs, maps the
  changed paragraphs to claims through their line locators, runs stage 6 on those
  claims against the new text, and proposes a new capture under a new source ID.

### Stage contracts

| Stage | Input | Output | Fails when |
| --- | --- | --- | --- |
| 1 Capture | URL | staging bundle: `content.md`, `metadata.json` with the page metadata, optional `page.pdf` | interstitial, error page, `noarchive`, short body, non-HTTPS final URL. A failure is a collection blocker, reported as such, never worked around. |
| 2 Segment | staging `content.md` | `paragraphs.json`: id, heading path, line start and end, text | never; an empty result is a stage 1 failure |
| 3 Resolve | paragraphs, hints, `data/agents/*.yaml`, `data/companies.yaml` | `identity.json`: company match, system-name matches, shortlisted records with a same-system probability, proposed decision | no company name in text or hints: stops with Needs evidence |
| 4 Extract | paragraphs, field definitions, inclusion rules, prompt version | `extraction.json` (schema below) | schema violation after one retry, or budget cap |
| 5 Verify | extraction, `content.md` | each quote marked `exact`, `fuzzy`, or `missing`, with lines | never; missing quotes set the claim to `review` |
| 6 Judge | claims with verified quotes, paragraph clusters | per-claim verdicts and probabilities, model and question version | API error, or budget cap |
| 7 Numbers | claims, quotes | per-claim numeric and date agreement | never; disagreement sets the claim to `review` |
| 8 Write | accepted claims only, style rules, prompt version | prose fields, each sentence tagged with claim IDs | a sentence without a claim ID, after one retry |
| 9 Preflight | prose, claims, quotes | per-sentence verdicts | API error, or budget cap |
| 10 Render | extraction, identity, prose | draft YAML, company entry, promoted captures, compatibility map | render output fails schema validation |
| 11 Validate | draft on disk | pass or the failing check's message | any check fails |
| 12 Review | everything above | `review.md`, `run.json` | never |

### The extraction record

Version 1. The writer model produces the `claims` list. Every other block is filled by
code. IDs are content addressed: the claim ID is a hash of the source content hash, the
quote span, and the field path, so two runs over the same capture give the same IDs and
no ID depends on list position.

```yaml
schema_version: 1
run_id: "2026-09-22T19:40:11Z-3f9a"
candidate:
  company: Airbnb
  system_name: Datako
  record_id: airbnb-datako          # proposed for Add, existing for Update
  decision: add                     # add | update | needs-evidence | out-of-scope; proposed
  matched_records:
    - id: airbnb-airchat
      same_system: 0.08
      reason: same company, different system name
sources:
  - local_id: s1                    # becomes <record-id>-source-<n> at render
    url: https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/
    canonical_url: https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/
    kind: podcast
    provenance_class: direct-participant
    published_at: "2026-06-22"       # from page metadata, confirmed by a quote when possible
    staging_path: .intake/captures/8c1e2f0a4b7d9e33/
    content_sha256: "sha256:..."
claims:
  - id: c-7d3b19e2
    field: key_metrics[]             # field path family; the renderer assigns the index
    text: Airbnb reports high hundreds of daily active users.
    kind: metric
    provenance: reported
    quotes:
      - source: s1
        text: "we have high hundreds of daily active users on Datako"
        paragraph_id: p41
        lines: [212, 214]            # stage 5
        match: exact                 # exact | fuzzy | missing
    numbers:                         # stage 7
      - claim: "high hundreds"
        in_quote: true
    judgments:                       # stage 6, advisory
      relation: {label: stated, p: 0.91}
      actor_mismatch: 0.04
      temporal: {label: current, p: 0.88}
      approval_removed: 0.02
      basis: {label: reported-measurement, p: 0.71}
      model: jev-1.13.0
      question_version: 1
    disposition: accept              # accept | review | drop; code applies the policy
    review_note: null
questions:                           # stage 10 derives page_content from this block
  human_involvement:
    state: not-reviewed
    note: The pipeline found no passage in s1. Confirm silence or record the next action.
```

Rendering rules, field by field:

| Extraction | Today's YAML |
| --- | --- |
| `claims[].field` and order of acceptance | list index in `summary`, `primitives`, `key_metrics`, `lessons_learned`, `architecture.*`, `operating_models[]` |
| `claims[].quotes[]` with `match: exact` | `evidence.<path>[]` with `relation: supports` and locator `Preserved content.md, lines a–b` |
| `claims[].kind`, `provenance`, `numbers`, judgments | `claim_metadata.<path>`: kind, provenance, confidence, `confidence_reason` from stage 8, `metric_scope`, `denominator`, `measurement_method` when the quote states them, `valid_at` from a dated quote or `published_at` |
| the best metric by basis and specificity | `headline_metric`; the rest become `key_metrics`; no metric appears twice |
| `questions` | `page_content.questions` and `implementation_fields`; `reported` when accepted claims exist, else `not-reviewed` with the note |
| `sources[]` | `sources[]` with `canonical_url` normalised by code, `accessed_at` and `last_verified_at` set to the capture date, `capture.manifest_path` after promotion |
| `candidate.company` when new | a `data/companies.yaml` entry with `logo: none` and a `logo_note` asking for editorial logo collection |
| claim IDs to rendered paths | `compatibility.json` in the run manifest: the explicit mapping the schema review asks for |

### Division of labour

- **Steel** acquires. The scrape response's page metadata travels into the staging
  bundle and the extraction record. It does not enter the committed manifest in this
  plan; that would be a manifest schema change and is listed under open decisions.
- **The writer model** extracts and writes. It is the only component that produces
  text. It receives paragraphs with IDs, the field definitions, and the inclusion rules.
  It returns JSON that matches the extraction schema. Prompts are versioned files.
- **Jev** judges. Choice and yes/no questions over a short passage cluster, batched per
  cluster, with the question set from Plan 016 Design 1 and the identity question from
  Design 2. Its outputs are advisory columns and a coarse gate, never an authority.
- **Code** segments, resolves names, verifies quotes, checks numbers and dates,
  renders, validates, caches, and writes the review sheet.
- **A person** reads the review sheet, edits the draft, decides, and opens the pull
  request.

### Decision policy

- Identity: a deterministic match on company and on system name or alias shortlists
  existing records. Jev answers "same system and version?" per shortlisted record. A
  probability at or above the calibrated threshold proposes Update; none proposes Add;
  a value between proposes review. The reviewer confirms every identity decision.
- Claim disposition: `accept` when the quote is exact, numbers agree, and the relation
  verdict is `stated` at or above the coarse threshold with no other flag above its
  threshold. `review` for anything else. `drop` only for a missing quote on a claim the
  writer model marked as reported. Thresholds live in the skill configuration, are set
  in Phase 3 from calibration, and start conservative.
- Eligibility: the pipeline applies the contributing guide's categorical questions to
  what the accepted claims establish and proposes Add, Update, Needs evidence, or Out
  of scope with the reason. No numerical score.
- Contradiction: in Update and in the cross-source hunt, a restated number that
  disagrees with an existing metric becomes a proposed evidence link with
  `relation: contradicts` on the existing claim. The reviewer decides whether the
  numbers describe the same observation.

## Scope

In scope: the twelve stages, the backfill and drift modes, the extraction schema and
renderer, staging captures and promotion, a Python package under uv with tests, the
adapters for Steel, the writer model, and Jev, the review sheet, the run manifest, a
thin skill, an operator document, the backtest harness, and the Jev evaluation Plan 016
specified.

Out of scope: automatic commits, pull requests, or publication; changing the public
schema of `data/agents/*.yaml` or `agents.json`; migrating the 66 existing records to a
new authoring format; audio transcription; a discovery crawler that finds candidate
URLs; embeddings or semantic search for readers; a hosted service; a database.

## Implementation steps

Execute the phases in order. Each phase ends with `npm run verify` green, the phase's
own checks, and a status update in this file. Stop at every STOP line and report; do
not continue into the next phase on the same authorization.

### Phase 0. Extraction record, renderer, backtest scaffold (M, no network, no model calls)

1. Add the package `intake/` at the repository root with the modules listed under
   repository layout. Add `pydantic` to the runtime dependencies in `pyproject.toml`
   and refresh `uv.lock`. Keep `scripts/build.py` untouched; the package imports its
   validators through one small import shim, the same way the coverage script does.
2. Write the extraction record models and their JSON schema export. Write the renderer
   from an extraction record to today's YAML and to a company entry. Write the
   compatibility map.
3. Golden tests: hand-written extraction records for three existing entries, one per
   collection shape (an agent with metrics, a platform, an agent with lessons), render
   to YAML, and assert the build's validators accept the output and that every
   evidence link has a locator.
4. Backtest scaffold: a command that loads an existing record and its captures and
   produces the comparison report shape (claim recall, claim precision, locator
   agreement, unverified-quote count) from a supplied extraction record. No model call
   yet.
5. Add `.intake/` to `.gitignore`, next to `.seo/`.

STOP: report the package layout, the dependency addition, and the golden-test output.
Approval needed for the run-manifest location (open decision 1) before Phase 1.

### Phase 1. Capture staging, segmentation, identity (M, Steel only)

1. Capture: a function that scrapes a URL with the Steel Python SDK, runs the archiver's
   page checks on the result, and writes a staging bundle keyed by the hash of the
   canonical URL, with the page metadata saved beside the Markdown. A promotion
   function copies a staging bundle into `archive/sources/<source-id>/` through the
   archiver's own manifest writer, so the append-only rule and the manifest format
   stay in one place. Refuse to promote onto an existing bundle.
2. Segment: split the capture into paragraphs with stable IDs, heading paths, and line
   ranges. Tables and code blocks are single paragraphs. Transcript timestamps, when
   present, are kept in the paragraph text so a locator can name them.
3. Resolve: normalise company and system names, search records and aliases and the
   company registry, shortlist, and write the identity file. Jev's same-system question
   is added in Phase 3; until then the shortlist is the output.
4. Tests with the 122 existing captures as fixtures: segmentation is stable across
   runs, promotion refuses an existing bundle, the page checks reject the archiver's
   own interstitial fixtures, name resolution finds each existing record from its own
   summary.
5. Add `STEEL_API_KEY` to the `.env` conventions in the operator document. Never print
   it.

STOP: report which of the 138 sources the SDK path captures identically to the CLI path
on a sample of ten, and any difference in Markdown fidelity. Approval needed to use the
SDK beside the CLI in the archiver path (open decision 2).

### Phase 2. Extraction, quote verification, numbers, backtest (L, writer model)

1. Extract: the writer-model adapter with structured output, the versioned prompt, one
   retry on schema violation, and the budget cap copied from the Plan 016 runner:
   reserve the worst case per call, refuse a run above the cap, stop on the first
   error, never overwrite a run directory.
2. Verify quotes: normalise whitespace, Unicode compatibility forms, quotation marks,
   and dashes on both sides; find the quote in the capture; record the line range.
   A near match at or above a fixed similarity within the named paragraph is `fuzzy`
   and sends the claim to review. Anything else is `missing`.
3. Numbers and dates: extract numbers with units, percentages, counts, durations,
   spelled quantities such as "high hundreds", and dates from claim and quote. Every
   number in the claim must appear in the quote. A date in the claim must appear in the
   quote or equal the source's published date, and the latter is flagged.
4. Backtest: run stages 2, 4, 5, and 7 over the 66 records' captures with the
   existing claim text withheld, then compare to the human YAML. Report claim recall
   by kind, precision, the number of pipeline quotes that were `missing`, and locator
   agreement with the 1,007 existing locators. Record the model string, token usage,
   and cost per record.
5. Backfill mode, dry run only: for the 240 claims without a locator, propose a quote
   and a locator, verify it, and write the proposals to a review sheet. Apply nothing.

STOP: approval of the writer-model budget before step 4 (planning estimate: at most
$20 for the full backtest at published prices, most sources far below the worst case).
Go/no-go on the backtest: at least 90 percent recall of reported facts and metrics,
at least 80 percent claim precision, and zero `missing` quotes with `accept`. If a kind
fails, restrict the pipeline to the kinds that pass and report.

### Phase 3. Jev judgments and the adjudicated evaluation (M, Jev)

1. Judge: the Jev adapter with direct HTTP, a persistent connection, a timeout, no
   automatic retry, and the same budget-cap pattern. Questions per claim from Plan 016
   Design 1: relation, actor mismatch, temporal status, approval condition removed,
   observation basis. The identity question from Design 2 joins stage 3. Batch all
   claims that share a paragraph cluster. Cache by claim text hash, capture hash, span,
   question version, and model version.
2. Review sheet columns for every verdict and probability. Coarse gate only:
   `stated` at or above the threshold and no flag above its threshold means `accept`;
   everything else means `review`.
3. Run the evaluation Plan 016 specified: about 120 independently adjudicated
   claim-and-passage items, grouped splits, two human labellers, oracle passages and
   retrieval tracks, permutation and repeat stress, calibration per question. Budget as
   in that plan, at most $1 of Jev usage.
4. Set the thresholds from the calibration split and record them in the skill
   configuration with the model version they belong to.

STOP: go/no-go per Plan 016's advisory-checker criteria: at least 90 percent
material-defect recall and 80 percent alert precision on the held-out groups. If the
criteria fail, Jev stays as advisory columns with no gate, and the pipeline sends every
claim to review. Report either outcome.

### Phase 4. Writing, preflight, render, verify, skill (L, writer model and Jev)

1. Write: the writer model receives accepted claims with their quotes and the catalog's
   style rules, and returns the summary, the primitive descriptions, the lesson wording
   with its scope, the metric scope wording, and one confidence reason per claim. Every
   sentence carries the claim IDs it rests on. A sentence without an ID fails the stage
   after one retry.
2. Preflight: Jev checks each sentence against the quotes of its claims with the
   relation question. A `conflicts` or low `stated` verdict sends the sentence to review.
3. Render, validate, and review sheet as specified. Promote captures only when the
   draft validates. Write the run manifest with the compatibility map.
4. The skill `.claude/skills/intake/` in the shape of the SEO skill: `SKILL.md`,
   `config.json` with budgets, thresholds, model strings, and prompt versions, and an
   `evals/` folder with the golden cases. The add-agent-from-url skill keeps the policy
   and the assessment path and points to this skill for execution.
5. Operator document `docs/intake-pipeline.md`: commands, the review sheet, what the
   pipeline never does, how to read a run manifest, how to rerun one stage.
6. Acceptance run: three leads from the 2026-09-11 policy-review table in
   [the coverage backlog](../docs/coverage-backlog.md), end to end. The owner reviews
   the three drafts and their sheets before the remaining five run.

STOP: after the three drafts. Approval needed for each pull request that adds a
drafted record, as today.

### Phase 5. Backfill, drift, schedule (M)

1. Backfill: apply approved locator proposals to existing records, touching only
   `locator` fields, worst records first. One pull request per batch of records with
   the review sheet attached.
2. Drift: the rescrape-and-compare mode with a report of changed sources, affected
   claims, and proposed new captures. Run it once by hand and record the result.
3. Schedule: a weekly GitHub Actions job beside `links.yml` that runs the drift report
   and the link check and opens an issue on change. It needs the Steel key in Actions
   secrets, which is open decision 4.

STOP: approval to modify existing records (locators only) before step 1; approval for
the scheduled job and its secret before step 3.

## Repository layout

```text
intake/
  __init__.py  __main__.py         # uv run python -m intake <command>
  models.py                        # extraction record, run manifest, review rows
  capture.py  segment.py  resolve.py  extract.py  verify_quotes.py
  judge.py  numbers.py  write.py  render.py  review.py  cache.py  budget.py
  run.py  stage.py  preflight.py   # queue runs, stage reruns, sheet flags
  backtest.py  backfill.py  evals.py  apply.py  drift.py
  adapters/steel.py  adapters/writer.py  adapters/jev.py
  prompts/extract.v1.md  prompts/write.v1.md  questions/judge.v1.json
tests/test_intake_*.py             # one module per stage; fixtures from archive/sources/
.intake/                           # gitignored: staging captures, stage outputs, cache, runs
drafts/                            # gitignored: draft records awaiting review
.claude/skills/intake/             # SKILL.md, config.json, evals/
docs/intake-pipeline.md
```

Commands, all from the repository root:

```sh
uv run python -m intake run queue.yaml --budget-usd 2.00        # all stages, one candidate or many
uv run python -m intake stage <name> --run <run-id>              # rerun one stage from cache
uv run python -m intake backtest --records all --budget-usd 20   # Phase 2 gate
uv run python -m intake backfill data/agents/<id>.yaml --dry-run # locator proposals
uv run python -m intake drift --report                           # Gap 3
uv run python -m intake review <run-id>                          # print the review sheet
npm run verify
```

## Configuration and secrets

- `.env` at the repository root, git-ignored, beside the DataForSEO keys:
  `STEEL_API_KEY`, `OPENAI_API_KEY`, `TYPESAFE_API_KEY`. The adapters read them from
  the environment only. No value is ever written to a manifest, a sheet, a log, or a
  commit. The private-data check runs in `npm run verify` and stays as the last guard.
- `config.json` in the skill holds model strings, prompt and question versions,
  thresholds with the model version they were calibrated for, default budgets, and the
  similarity bound for fuzzy quotes. A threshold without a model version is invalid.
- Every run directory holds `run.json`: run ID, queue entry, model strings returned by
  each API, prompt and question versions, capture hashes, per-stage token usage and
  cost, cache hits, and the compatibility map.

## Cost, planning estimates only

| Item | Assumption | Estimate |
| --- | --- | ---: |
| Writer model per source | 10,000 to 40,000 input tokens across extract and write, 4,000 to 8,000 output | $0.06 to $0.16 |
| Jev per source | 10 clusters, 4,000 tokens each, all questions | under $0.01 |
| Steel per source | one scrape, one optional PDF | per the Steel plan |
| Backtest over 66 records | 122 captures, worst case per source | at most $20 |
| Backfill over 240 claims | one extract call per record with the claim list | at most $10 |

Measure `usage` on every call. The estimates exclude reviewer time, which is the cost
that matters: one percent false alerts at two minutes each across the catalog is more
than the whole model bill.

## Evaluation

- **Backtest** (Phase 2): the 66 human-written records and their captures are the
  labelled set. Metrics: claim recall by kind, claim precision, `missing` quote count,
  locator agreement. The gate is stated at the Phase 2 STOP line.
- **Adjudicated Jev evaluation** (Phase 3): as specified in Plan 016, with its
  leakage controls, baselines, stress tests, and go/no-go criteria.
- **Acceptance** (Phase 4): eight backlog leads end to end. Success is a draft the
  owner can approve with edits to wording only, no missing quotes, and no invented
  facts. Any invented fact is a stop.
- **Ongoing**: the skill's `evals/` folder keeps the golden cases; a change to a prompt
  or question version reruns them before it ships.

## Done criteria

1. Phase 0: the renderer produces YAML that the build validates for three golden cases.
2. Phase 1: staging capture, promotion, segmentation, and name resolution pass their
   tests on the existing captures; the SDK path matches the CLI path on the sample.
3. Phase 2: the backtest meets its gate; the backfill dry run lists a verified quote for
   at least 80 percent of the 240 unlocated claims.
4. Phase 3: thresholds are calibrated and recorded, or Jev is demoted to advisory
   columns with the evaluation report attached.
5. Phase 4: eight backlog leads drafted; three reviewed by the owner first; the skill
   and the operator document exist; `npm run verify` green with the new tests.
6. Phase 5: locators applied to the worst five records at least; a drift report exists;
   the schedule runs or its rejection is recorded.

## STOP conditions

- Any stage produces a claim with a `missing` quote and disposition `accept`. Stop the
  phase; this is a correctness bug, not a tuning matter.
- The writer model returns a person's name, e-mail address, or contact detail outside a
  source's `authors` field. Stop and report; the private companion repository holds
  people data, the public catalog does not.
- A capture fails the archiver's page checks. Report a collection blocker for that URL
  and continue with the other URLs; never reconstruct a source from snippets, a search
  result, or memory.
- A run would exceed its budget reservation. Refuse to start; report the reservation.
- The backtest or the Jev evaluation misses its gate. Report; restrict scope; do not
  lower the gate to pass.
- The extraction schema needs a field that today's YAML cannot carry. Record it in the
  compatibility map and in this file; do not add a key to the public schema in this
  plan.
- Any request to let the pipeline commit, open a pull request, or publish.

## Risks and rejected ideas

- **The writer model authors the YAML directly.** Rejected: it reproduces the
  bookkeeping the schema review asks to delete, and the evidence map would be prose,
  not a rendering of verified quotes.
- **Jev as the extractor.** Rejected: Jev answers typed questions and cannot produce
  text or find a passage it was not given. Its role is judgement over supplied state.
- **Automatic publication or merge.** Rejected by Plan 016 and by this plan.
- **Raw HTML as evidence.** Already rejected in the plans index; the staging bundle
  keeps only the Markdown, the page metadata, and the optional PDF.
- **Rewriting the archiver around the SDK.** Rejected: the archiver's checks, manifest,
  and append-only rule are correct and tested. The pipeline calls them.
- **Embeddings or vector search.** Out of scope; Plan 016 Design 3 remains deferred.
- **Determinism claims.** The pipeline is reproducible with a warm cache. Docs must not
  call it deterministic.
- **Risk: a brand-new writer model.** GPT-6 Sol shipped on the planning date. The
  adapter pins the model string, records what the API returns, and is swappable behind
  one interface. If a dated snapshot appears, switch to it and rerun the golden cases.
- **Risk: transcript sources.** A scrape of a podcast or talk page captures the page,
  not the words, unless the page carries a transcript. In this plan such a source goes
  to review with "Needs evidence: transcript" unless the capture holds the words.
  YouTube captions and audio transcription are a follow-up with their own terms review.
- **Risk: capture fidelity.** Steel captures have dropped standfirsts and datelines
  before. The page metadata's published timestamp reduces the date problem; a
  reviewer still confirms `published_at` when no quote states it.
- **Risk: review load.** If the sheet costs more minutes than it saves, the coarse gate
  is too loose or the extractor too eager. Measure reviewer minutes per record in the
  acceptance run and record them in this file.

## Open decisions for the owner

1. **Run manifest location.** Commit one `run.json` per drafted record, under
   `archive/intake/<record-id>/`, so a reader can see that a record was machine-drafted
   and by which model, or keep manifests local and note the model in the pull request
   only. Recommendation: commit them; they are small and they carry the compatibility
   map the schema migration will need.
2. **Steel SDK beside the CLI.** The archiver keeps the CLI; the pipeline uses the SDK
   for staging and hands the result to the archiver's writer. Manifests record the tool
   name and version that produced them, so both are honest. Recommendation: yes.
3. **Page metadata in the committed manifest.** Adding `published_at` and `language`
   to the manifest is a schema change with a version bump. Recommendation: not in this
   plan; carry them into the source record instead.
4. **Scheduled drift check with API secrets in GitHub Actions.** Recommendation: run
   the drift report by hand for two months first, then decide.
5. **Writer-model effort level and budget defaults.** Recommendation: medium effort,
   $2 per run, $20 for the backtest, all in `config.json`.

## Completion record

Planned on 2026-09-22. Execution of each phase requires its own approval as stated at
the phase's STOP line.

## Execution log

Executed under the owner's Ralph-loop instruction of 2026-09-22 ("continue until the
full plan is implemented and done"), which serves as the standing authorization the
STOP lines ask for. Each phase still reports at its STOP line before the next begins.
One deviation: the loop names one branch for the whole plan
(`claude/plan-017-source-intake-pipeline`), so phases land as commits on that branch
instead of one branch per phase.

### Phase 0 — extraction record, renderer, backtest scaffold (2026-09-22)

STOP-line report:

- Package layout: `intake/` with `__init__.py`, `__main__.py` (commands: `schema`,
  `render`, `backtest`), `models.py` (pydantic extraction record and run manifest,
  content-addressed claim IDs, `finalize`), `catalog.py` (import shim that loads
  `scripts/build.py` the way the coverage script and the tests do), `render.py`
  (renderer, compatibility map, company entry), `backtest.py` (comparison scaffold),
  and the committed JSON schema export `intake/schemas/extraction-record.v1.json`.
  Tests: `tests/test_intake_models.py`, `tests/test_intake_render.py`,
  `tests/test_intake_backtest.py`; fixtures under `tests/fixtures/intake/`.
  `.intake/` and `drafts/` are gitignored.
- Dependency addition: `pydantic==2.13.5` pinned like the existing `PyYAML` pin;
  `uv.lock` refreshed. `scripts/build.py` is untouched; the package reaches its
  validators only through `intake.catalog`.
- Golden tests: three hand-written extraction records (plaid-ai-annotator — agent with
  metrics; zup-codegen — agent with lessons; duolingo-agentic-workflows — platform)
  render to YAML that `build.validate_record` accepts; every evidence link carries a
  locator; every exact quote is verified verbatim inside its named capture lines;
  rendering is deterministic; pipeline silence renders as `not-reviewed`, never
  `unreported`. Backtest scaffold: the zup fixture against its human record scores
  10/10 recall, precision 1.0, locator agreement 1.0, zero unverified quotes; the
  plaid fixture exercises the partial-report path (6 of 7 human claims).
- Open decision 1 (run-manifest location): not yet live — no run manifest has been
  committed because no record has been drafted end to end. The recommendation
  (commit under `archive/intake/<record-id>/`) stands and Phase 1 keeps staging
  manifests under gitignored `.intake/` until then.

`npm run verify` green with the new tests (full gate, dist rebuilt).

### Phase 1 — capture staging, segmentation, identity (2026-09-22)

STOP-line report:

- Capture (stage 1): `intake/adapters/steel.py` scrapes through the Steel Python
  SDK (`steel-sdk==0.19.0`, pinned) and runs the archiver's own page checks on
  the response, so interstitial titles, error statuses, `noarchive`, short
  bodies, and non-HTTPS final URLs fail exactly as in the CLI path. The page
  metadata the CLI discards (published time, language, canonical URL,
  description) travels into the staging bundle's `page.json`.
- Staging and promotion: `intake/capture.py` stages under
  `.intake/captures/<canonical-url-hash>/` with a placeholder snapshot header of
  the same 9-line shape the archive uses, so line locators are stable. Promotion
  rebuilds the snapshot with the final source ID through a new
  `write_capture_bundle` extracted from the archiver's `capture_source` — the
  manifest format and the append-only rule stay in one place, and the archiver's
  own tests still pass. The manifest validator now accepts the tool name
  `steel-python-sdk` beside `steel` (open decision 2, per its recommendation).
- Segment (stage 2): `intake/segment.py` — paragraphs with IDs `p1..pn`, heading
  paths, and 1-based line ranges; fenced code blocks stay single paragraphs;
  headings are their own paragraphs. Tested over all 122 existing captures:
  segmentation is stable, IDs are sequential, ranges cover every non-blank line
  exactly once.
- Resolve (stage 3): `intake/resolve.py` — deterministic company match against
  the registry (hint or text), system-name scoring against `agent_name` and
  aliases (exact 1.0, containment 0.85, token overlap), a shortlist of at most
  five, and a proposed decision (update / review / add / needs-evidence; no
  company evidence proposes needs-evidence per the stage contract). Tested: all
  66 records are found from their own company, name, and summary, top-ranked,
  decision `update`.
- Operator document: `docs/intake-pipeline.md` created with the commands and the
  `.env` conventions (`STEEL_API_KEY`, `OPENAI_API_KEY`, `TYPESAFE_API_KEY`).
- SDK-versus-CLI sample comparison (the STOP line's ask): **not run — blocked**.
  No `STEEL_API_KEY` exists on this machine (no `.env`). The comparison needs
  ten live scrapes through both paths; it stays open until the key is provided.
  Everything testable offline is tested: the adapter reuses the archiver's
  checks on fixture payloads, and promotion round-trips through the archiver's
  own validator.

`npm run verify` green with the new tests.

### Phase 2 — extraction, quote verification, numbers, backtest (2026-09-22)

STOP-line report:

- Extract (stage 4): `intake/adapters/writer.py` pins `gpt-6-sol` through the
  OpenAI Responses API with structured output (the payload's JSON schema made
  strict: every key required, no extras), records the model string the API
  returns, and reports token usage to the budget ledger. `intake/extract.py`
  composes the untrusted input (paragraphs with IDs, source facts, hints), runs
  the versioned prompt `intake/prompts/extract.v1.md`, retries once on a schema
  violation, and fails the stage on the second. The writer refers to its own
  claims positionally (`#0`, `#1`); `resolve_references` rewrites those into
  the content-addressed IDs after `finalize`. Dependency: `openai==3.18.0`,
  pinned.
- Budget: `intake/budget.py` follows the Plan 016 runner — worst-case
  reservation per attempted call (64k input + 16k output at the published
  $2/$10 per million prices, about $0.288 per call), refusal above the passed
  budget, usage recorded per call, run directories under `.intake/runs/` never
  overwritten, and a `run.json` manifest per run.
- Verify quotes (stage 5): `intake/verify_quotes.py` normalises Unicode
  compatibility forms, curly quotes, dashes, and whitespace on both sides, then
  finds the smallest line window that contains the quote (`exact` with lines).
  Near matches at or above the 0.7 word-window similarity inside the named
  paragraph are `fuzzy`; anything else is `missing`. Both fuzzy and missing send
  the claim to review, so the bound is deliberately loose on the safe side. The
  golden fixtures' quotes all verify `exact` in their real captures; a
  hyphenation variant verifies `exact`, a paraphrase is `fuzzy`, an absent quote
  is `missing`.
- Numbers (stage 7): `intake/numbers.py` extracts percentages, counts with
  separators, multipliers, durations with abbreviations, spelled quantities
  ("high hundreds"), fractions ("one in eight"), and ISO and month-name dates.
  Every claim number must appear in the quote; a claim date must appear in the
  quote or equal the source's published date, and the fallback carries a note.
- Backtest: the Phase 0 scaffold plus the renderer compatibility map is the
  comparison; the live backtest over the 66 records (**the phase gate**) is
  **blocked — no `OPENAI_API_KEY`**. The gate (at least 90 percent recall of
  reported facts and metrics, at least 80 percent precision, zero
  `missing`-with-`accept`) cannot be evaluated until the key exists; nothing
  was faked.
- Backfill dry run: `intake/backfill.py` proposes a quote per unlocated claim
  through the writer adapter, verifies it with stage 5, checks the numbers, and
  writes a Markdown review sheet. Applies nothing. The live run over the 240
  unlocated claims is blocked on the same key; tested offline with a fake
  writer over the real zup capture.

`npm run verify` green with the new tests (full gate, exit 0).

### Phase 3 — Jev judgments and the adjudicated evaluation (2026-09-22)

STOP-line report:

- Judge (stage 6): `intake/adapters/jev.py` calls `jev-1.13.0` over direct
  HTTPS with a persistent connection, a 20-second timeout, no automatic retry,
  and the Plan 016 budget pattern (the 65,536-token maximum input charge
  reserved per attempted request, about $0.0028). Every answer's shape is
  validated before use. `intake/judge.py` asks the five Design 1 questions per
  claim (relation, actor mismatch, temporal status, approval condition,
  observation basis), batches the claims of one paragraph cluster into one
  request with only that cluster as state, and caches by claim text, field,
  capture hash, quote span, question version, and model version
  (`intake/cache.py`, under `.intake/cache/`). A warm-cache rerun makes zero
  requests.
- Review-sheet columns: every verdict and probability lands on the claim rows
  (the sheet assembly is stage 12, Phase 4; the judgment blocks carry the
  columns). The coarse gate lives in `apply_dispositions`: `accept` only with
  an exact quote, agreeing numbers and dates, a `stated` relation at or above
  0.8, no actor-mismatch or approval-removal flag above 0.3; a `missing` quote
  on a reported claim is `drop`.
- Identity (Design 2) joins stage 3: `resolve.refine_with_jev` adds the
  same-system probability to every shortlist entry as an advisory column; the
  deterministic scores stay.
- The adjudicated evaluation (**the phase gate**): the harness exists —
  `intake/evals.py` samples claim-and-passage items from the authored records
  with exact line locators (reproducible for a fixed seed), holds two labeller
  columns plus an adjudicated label per item, never overwrites an item file,
  and scores material-defect recall and alert precision against the Plan 016
  criteria (0.9 / 0.8). **The run itself is blocked twice over**: the live Jev
  pass needs `TYPESAFE_API_KEY`, and the labels need two humans labelling
  about 120 items from the original evidence. Neither happened; no thresholds
  were calibrated and nothing was faked.
- Thresholds: `GATE` in `intake/judge.py` records the provisional values with
  the model and question version they belong to, and states why they are
  provisional. Calibration replaces them only after the evaluation runs; per
  the STOP rule, if the criteria fail, Jev stays advisory with no gate and
  every claim goes to review.

`npm run verify` green with the new tests.

### Phase 4 — writing, preflight, render, verify, skill (2026-09-22)

STOP-line report:

- Write (stage 8): `intake/write.py` with the versioned prompt
  `intake/prompts/write.v1.md`. The claim prose comes from stage 4, so stage 8
  writes the one piece stage 4 may leave blank: the per-claim confidence
  reason. The writer receives the claims with their computed IDs and quotes;
  an unknown claim ID, an empty reason, or a number the claim and quotes do
  not carry fails the stage after one retry. The "every sentence carries its
  claim IDs" rule holds structurally: every rendered field maps to claims
  through the compatibility map, and the renderer refuses a field without one.
- Preflight (stage 9): `intake/preflight.py` flags conflicts and low-stated
  verdicts onto the sheet. It consumes the stage 6 relation verdicts instead
  of asking the same question twice on the same passage — the plan's separate
  sentence pass assumed stage 8 writes new prose; here the prose is the claims
  and was already judged. Stage 8's output is confidence reasons, whose
  numbers were checked at write time.
- Render, validate, review: `intake/run.py` orchestrates all twelve stages
  from a queue file (`uv run python -m intake run queue.yaml --budget-usd 2.00`),
  saves every stage's artifact under `.intake/runs/<run-id>/` (never
  overwritten), writes the draft under `drafts/` (never overwritten), and
  `intake/review.py` produces the sheet (claims, quotes, locators, verdicts,
  dispositions, model usage, the decision a person makes) and the `run.json`
  manifest with the compatibility map. Stage 11 runs `build.validate_record`
  on the draft. Offline stages rerun with `intake stage <name> --run <run-id>`
  into `<artifact>.rerun` files.
- Skill: `.claude/skills/intake/` with `SKILL.md`, `config.json` (model
  strings, prompt and question versions, provisional gate thresholds with
  their model version, budgets, similarity bound), and `evals/` holding the
  three golden extraction records. The add-agent-from-url skill keeps the
  policy and now points to the intake skill for execution.
- Operator document: `docs/intake-pipeline.md` completed — commands, reading a
  run, rerunning one stage, secrets, and what the pipeline never does.
- Acceptance run (**the phase gate**): **blocked — no `STEEL_API_KEY` and no
  `OPENAI_API_KEY`**. The three 2026-09-11 policy-review leads (Snowflake,
  Databricks Omnigent, and Amazon Q Developer are ready candidates) cannot be
  captured or drafted live. Instead, the whole pipeline is proven end to end
  offline: a queue run over the real zup capture with fake services passes all
  twelve stages, produces a draft that `build.validate_record` accepts with
  locators on every evidence link, writes the sheet and manifest, and reruns
  its offline stages. The eight-lead acceptance and the reviewer-minutes
  measurement stay open until the keys exist.
- One deviation recorded: the run stages every source conservatively as
  `kind: other`, `provenance_class: independent-secondary`; the sheet tells the
  reviewer to correct both. The writer prompt asks for the real values but the
  queue defaults stay honest rather than guessed.

`npm run verify` green with the new tests (full gate, exit 0).

### Phase 5 — backfill apply, drift, schedule (2026-09-22)

STOP-line report:

- Apply (step 1): `intake/apply.py` plus `backfill-apply` in the CLI. The input
  is the dry run's proposal list, each entry carrying an `approved: true` flag
  a person added. The applier touches only `locator` fields on existing
  evidence links. It refuses entries without the flag, unknown evidence paths,
  links that name no such source, and links that already carry a different
  locator. It never reorders, rewrites, or removes anything; the person
  regenerates the outputs and opens the pull request. The STOP line's approval
  to modify existing records covers the machinery only: no record was edited,
  because the live dry run that produces proposals needs `OPENAI_API_KEY` and
  has not run. The done criterion "locators applied to the worst five records"
  stays open with it.
- Drift (step 2): `intake/drift.py` plus `drift` in the CLI. Every captured
  source is rescraped without saving; the page is compared with the preserved
  capture after the nine-line capture header is stripped, marks and whitespace
  normalised through the quote-verifier's normaliser, and the changed line
  spans shifted back so they number lines the way locators do. Changed sources
  list their spans and the claims whose locators fall inside them; blocked
  rescrapes are listed, never hidden; the report lands in
  `.intake/drift/report.json` and never edits a record. One detail the plan did
  not spell out: locators number lines in the preserved file with its header,
  so the header is stripped only for the comparison and the spans are offset
  back. "Run it once by hand and record the result" — **blocked, no
  `STEEL_API_KEY`**. Instead the mode is proven offline over the real zup
  capture with a fake Steel adapter: a changed abstract line reports line 18
  and the claims citing it; an unchanged page reports no drift; a blocked
  rescrape lands on the blocked list.
- Schedule (step 3): **rejected, recorded here**. Open decision 4 recommends
  running the drift report by hand for two months before any scheduled job;
  the plan's own step 3 defers to that decision. No GitHub Actions job, no
  Actions secret. Revisit after the two months of hand runs.
- Gate repair, found this phase: `ruff format` in this repository now formats
  Python code blocks inside Markdown, and `plans/016-jev-investigation.md`
  failed `ruff format --check` — verified at HEAD in a clean worktree, so the
  break predates this phase. The file was reformatted (code blocks only, no
  prose change) and a papercut was logged.
- Tests: eleven new tests in `tests/test_intake_modes.py` (apply refusals and
  the locator-only guarantee; span, drift, and blocked paths). The intake
  suite holds 106 tests. One Phase 4 leftover rides along:
  `tests/test_intake_stages.py` still called `run_extract(paragraphs=...)`
  against the committed `paragraphs_by_source` signature; the rename is part
  of this commit so the tree is self-consistent.
- Gate honesty: the working tree carries an unrelated, in-progress record edit
  (Shopify) whose YAML and generated outputs fail eight web tests on their
  own. The gate was therefore run with those five files stashed — `npm run
  verify` exit 0, 177 web tests and the full Python suite green — and the
  files were restored byte-identical afterwards.
- Tip verification (added after the phase commit): a second run in a clean
  worktree at the branch tip, fresh installs, no working-tree files —
  `npm run verify` exit 0. The committed schema file also matches a fresh
  `intake schema` export byte for byte.
- Seam repair (found on re-read): the Phase 2 dry run and the Phase 5 applier
  did not compose — the report carried no per-entry record ID, the sheet hid
  the quote a reviewer must read, and no machine-readable proposal file
  existed. `backfill --proposals <path>` now writes the applier-shaped list
  (one entry per verified quote, every entry `approved: false` so the file
  refuses until a person approves it), and the sheet carries the quote beside
  the locator. A new test drives the whole seam offline: fake writer, dry run,
  unapproved refusal, approval, apply, locator landed. The intake suite holds
  108 tests.
- Gate-command repair (found on the same re-read): the plan's Phase 2 gate
  command (`backtest --records all --budget-usd 20`) did not exist — only the
  single-pair comparison did. `run_batch` now walks every record under
  `data/agents/`, maps each captured source to the `s1, s2, ...` local keys a
  run uses, extracts with the writer, verifies quotes, and compares against
  the human record, under one budget reservation; records without captures
  are skipped and listed, a budget refusal or writer failure stops the batch
  with the reason on the sheet. Tested offline with a fake writer over the
  real zup capture plus a capture-less record (skip, budget stop, writer
  stop). The intake suite holds 111 tests. The live run stays blocked on
  `OPENAI_API_KEY`; when the key arrives, the gate is one command.
- Evaluation-command repair (same re-read): the Phase 3 gate had no operator
  entry either — `evals.py` could build, agree, and score, but nothing asked
  Jev the items or printed a report. The judgment half of the coarse gate is
  extracted from `apply_dispositions` into `judge.gates_pass` (one threshold
  table, two callers), and `evals run_verdicts` judges each item's passage
  verbatim through the same five questions, caching by item, passage, question
  version, and model. The CLI gained `evals --items` (build, append-only) and
  `evals --items --score` (judge, score, labeller agreement). Thirteen new
  tests cover the extracted gate, item building, verdicts (accept, review,
  warm cache), and scoring (recall, precision, gate pass and fail). The intake
  suite holds 124 tests. The live pass still needs `TYPESAFE_API_KEY` and the
  two human labellers.
- Acceptance queue (same re-read): the Phase 4 acceptance run now has its
  input committed — `queue/acceptance-2026-09-11.yaml` holds the three
  policy-review leads (Snowflake Cortex Code, Databricks Omnigent, Amazon Q
  Developer) with every source URL from `docs/coverage-backlog.md`, HTTPS
  only, hints only. A test loads the queue through `load_queue` and holds it
  to three entries with at least one first-party source each, so the file
  cannot silently rot. When both keys exist the gate is one command:
  `uv run python -m intake run queue/acceptance-2026-09-11.yaml
  --budget-usd 2.00`. The run itself stays blocked; the LinkedIn social post
  in the Omnigent entry's backlog row was left out deliberately — social
  platforms make poor captures and the reviewer can add it by hand.
- Identity-column repair (same re-read): the stage 3 contract — "shortlisted
  records with a same-system probability" — was not met by the run.
  `resolve.refine_with_jev` existed and was tested, but `run_candidate` never
  called it, so a live run wrote identity files with no Jev column. The run
  now refines every non-empty shortlist (passage capped at 8,000 characters),
  caches by candidate, passage, shortlist, and question version, and reports
  model, tokens, cost, and cache hits on the resolve stage line. `resolve
  --jev` exposes the same step offline from the CLI. Two side repairs: the
  run's Jev cache is now injectable, and the end-to-end tests pass a
  temporary cache so fake answers never reach the shared `.intake` cache.
  The intake suite holds 127 tests.
- Identity on the sheet (follow-on, same re-read): the sheet rendered the
  writer's candidate echo, which carries no shortlist, so the Identity section
  was empty in real runs. The run now merges the identity stage's shortlist
  into the record's candidate before rendering, `MatchedRecord` gained the
  `same_system_jev` field, and the sheet shows "Jev same-system" beside the
  deterministic score. The committed schema file was regenerated to match.
  The end-to-end test asserts the section, both columns, and the resolve
  stage's model and call count in the manifest.
- Drift contract repair (same re-read): the drift specification says stage 6
  runs on the affected claims against the new text, but the mode stopped at
  listing them. `judge_drifted` now re-judges each affected claim over the
  rescraped passage — the changed span shifted back past the capture header
  and widened to its paragraph — through the same five questions, caching by
  claim, passage, question version, and model. The verdicts are advisory
  columns on the drift sheet; without a Jev adapter the report lists the
  claims and says so. The `drift` command judges by default under its own
  budget. Tested offline with a fake adapter: a changed abstract line
  re-judges the claims citing it, a warm cache judges nothing anew, and a
  report without Jev carries no verdicts and no error. The intake suite holds
  129 tests.
- STOP-line guard (same re-read): the plan's stop condition — "the writer
  model returns a person's name, e-mail address, or contact detail outside a
  source's `authors` field. Stop and report" — had no in-run detector; a
  writer reply carrying an e-mail would have reached the draft and failed
  only the repository-level verify, after the run. `intake/privacy.py` walks
  the whole extraction record after stages 4 and 8 with the repository
  scan's own e-mail pattern (authors lists exempt) and stops the run with
  the offending paths. Names are not mechanically detectable; that half of
  the STOP line is now an explicit step on the sheet's decision list. Eight
  new tests cover the walker, the exemption, the golden fixtures' cleanliness,
  and a poisoned writer reply stopping stage 4 of a real run. The intake
  suite holds 137 tests.
- Reproducibility repair (same re-read): the product contract — "a rerun with
  a warm cache is byte-identical" — could not hold, because stages 4 and 8
  had no writer cache at all. The writer adapter now caches structured
  replies keyed by instructions, input, schema, model, and effort (a hit
  replays the payload at zero tokens and cost, and the stage line reports
  zero calls with a cache hit), `run_candidate` threads a writer cache beside
  the Jev cache, and both are injectable so tests stay hermetic. One input
  repair made the keys stable: the staging header, which carries the capture
  timestamp, no longer reaches the writer's input; paragraph IDs and line
  ranges still number the full file, so locators are unchanged. A new
  end-to-end test runs the zup candidate twice over the same warm caches and
  asserts the two drafts are byte-identical with zero calls on the extract,
  judge, and write stages. The intake suite holds 138 tests.
- Evidential-independence repair (same re-read): the gap analysis says the
  same stages "compare a second source's numbers against the first", but an
  Update run never looked at the record it proposed to update. Two repairs
  in `intake/crosscheck.py`: the run now passes the existing record's source
  count to the renderer, so an update's new source is numbered
  `<record>-source-<n+1>` instead of colliding with `-source-1`; and the new
  claims are matched against the existing record's claims with digits
  masked, so a restated metric with a new value still aligns — a matched
  pair whose numbers disagree, or that drops a recorded number, lands on the
  sheet under "Cross-source checks". Seven unit tests cover the masked
  matcher's agree, differ, dropped, and unmatched paths, and an end-to-end
  test asserts the source numbering on a real update run. The intake suite
  holds 146 tests.
- Update merge (follow-on, same re-read): principle 4 — "an Update adds
  sources, claims, and evidence links at the end of their lists" — had no
  machine embodiment; an update's draft carried only the new claims and a
  person merged by hand. `intake/merge.py` now merges the rendered draft
  onto the record the update names: sources, list items, evidence links,
  and metadata entries append at the end when absent; single-valued fields
  keep the recorded text and a difference becomes a renderer note; the
  page-content block keeps its recorded answers and upgrades only the
  questions the new run reviewed (never downgrading). The end-to-end update
  test asserts the merged draft: the existing source stays first, the new
  source appends, the recorded summary and lessons are untouched, evidence
  for both old and new paths is present, and the sheet carries the
  single-valued note. Unit tests cover the additive guarantees and the
  page-content upgrade path. The intake suite holds 148 tests.
- Rerun repair (follow-on, same re-read): `intake stage render` re-rendered
  from the run directory without the existing record and with today's date,
  so an update run's `draft.yaml.rerun` silently differed from its own
  draft. The rerun now takes the review date from the draft's
  `last_reviewed_at` and merges onto the record the manifest names; the
  end-to-end update test asserts the rerun equals the run's draft byte for
  byte.

