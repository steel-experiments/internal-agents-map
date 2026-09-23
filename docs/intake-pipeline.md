# The source intake pipeline

The intake pipeline turns a list of links into a reviewed catalog record draft.
It is specified in [Plan 017](../plans/017-source-intake-pipeline.md); this page
is the operator document. The pipeline drafts; a person decides. No stage writes
to `main`, opens a pull request, or marks a source reviewed.

## Commands

Run every command from the repository root:

```sh
uv run python -m intake run queue.yaml --budget-usd 2.00   # all twelve stages
uv run python -m intake run queue/acceptance-2026-09-11.yaml --budget-usd 2.00  # the Phase 4 gate
uv run python -m intake review <run-id>                     # print a run's review sheet
uv run python -m intake stage render --run <run-id>         # rerun one offline stage
uv run python -m intake capture <url>                       # stage 1 alone
uv run python -m intake capture <url> --pdf                 # also keep the page PDF
uv run python -m intake promote <dir> --source-id ID        # promote into archive/sources/
uv run python -m intake segment --input <content.md> --output <paragraphs.json>  # stage 2
uv run python -m intake resolve --company X --system Y [--text-file f] [--jev]   # stage 3
uv run python -m intake render --extraction <file> --output <draft.yaml> --reviewed-at YYYY-MM-DD
uv run python -m intake backfill --rank                                # worst records first
uv run python -m intake backfill data/agents/<id>.yaml --budget-usd 10 --proposals p.json  # dry run
uv run python -m intake backfill-apply <proposals.json>                         # apply approved locators
uv run python -m intake drift                                                   # rescrape and report drift
uv run python -m intake evals --items <items.json>                              # sample evaluation items
uv run python -m intake evals --items <items.json> --score --budget-usd 20       # judge and score
uv run python -m intake backtest --records all --budget-usd 20          # the Phase 2 gate
uv run python -m intake backtest --record <yaml> --extraction <file> [--compatibility <json>]
uv run python -m intake schema                               # refresh the committed schema file
npm run verify                                               # the phase gate
```

A queue file is a YAML list; each entry holds `urls` (HTTPS) and optional
`company`, `system_name`, `record_id`, `source_role`, and `homepage` hints.
The queue's `company`, `system_name`, `homepage`, and `record_id` hints are
authoritative over the writer model's echo: queue input is input data the
writer cannot verify. `source_role` names a provenance class from the
catalog's own set
(`first-party`, `direct-participant`, `independent-secondary`, `community`,
`aggregator`) and sets every source of the entry; an unknown value stops the
queue before any capture or spend:

```yaml
- urls: [https://example.com/posts/agents]
  company: Example
  system_name: Example agent
  source_role: first-party
```

Every run bounds its cost before it spends. Each model call reserves its
documented worst case first, and a run refuses to start when even its
writer floor — one extract and one write call, $0.576 at the planning
prices — cannot fit the budget. The judge's request count is unknowable
before extraction, so those reservations happen per request; a run stops
at the first refusal or API error.

## Reading a run

Each run lives under `.intake/runs/<run-id>/` and is never overwritten:
`review.md` (the sheet), `run.json` (the manifest), `identity.json`,
`paragraphs-s*.json`, `extraction.yaml`, `extraction-gated.yaml`, and
`draft.yaml` (the run's archival copy of the draft). Drafts also land under
`drafts/`. Staging captures live under `.intake/captures/` and the Jev cache
under `.intake/cache/`; all three are gitignored and regenerable.

When the draft validates, the run promotes its staging captures into
`archive/sources/<source-id>/` through the archiver's append-only writer,
and the draft's sources carry the manifest paths. A rerun that meets its own
identical bundle reuses it; a bundle with different content stops the run
with the conflict named. The pull request carries the promoted bundles and
the run manifest, archived at `archive/intake/<record-id>/run.json` (open
decision 1's recommendation): a reader sees the record was machine-drafted,
by which model, and which claim IDs map to which rendered paths. The
archived copy records the latest run that drafted the record; the per-run
history stays under `.intake/runs/<run-id>/`.

A URL that fails the page checks is a **collection blocker**: the run
reports it, keeps the URLs that captured, and continues. Blockers land in
`blockers.json` in the run directory, in the run notes, and in a
"Collection blockers" section on the sheet. When every URL of an entry
fails, that entry reports `blocked` with no draft and no sheet, and the
queue continues with the next entry. Nothing is ever reconstructed from
snippets, a search result, or memory.

When the queue entry carries a `homepage` hint and the organization is not
yet in `data/companies.yaml`, the run also writes a `company-entry.yaml`
(one registry entry with `logo: none` and a `logo_note` asking for editorial
logo collection) into the run directory and beside the archived manifest;
append it to `data/companies.yaml`, keeping the list sorted by id. A known
organization gets no entry file and a note saying so.

The review sheet lists every claim with its quote, its line locator, its
numeric check, its Jev verdicts with probabilities, its disposition, and the
open questions. It names the decision the pipeline proposes and the decision a
person must make. An **Eligibility** section carries the categorical proposal
over the accepted claims — the contribution guide's three inclusion questions,
each answered or named as open, the writer's own proposal beside it, and no
numerical score. When the identity shortlist is non-empty, stage 3 also asks
Jev the same-system question per shortlisted record and writes the
`same_system_jev` advisory column into `identity.json`; the deterministic
scores stay. The proposed decision then follows the decision policy's bands
over the top entry's probability: at or above the update bound
(provisionally 0.8) proposes Update, below the add bound (provisionally
0.3) proposes Add, and a value between proposes review. The bands are
provisional until the Phase 3 calibration runs — `identity.json` records
the applied rule and bounds in `decision_basis` — and a person confirms
every identity decision either way. A queue entry whose text and hints
name no company at all stops after stage 3 with `needs-evidence` — no
writer spend, no draft — and names what a person must add; the queue
continues with the next entry. A company the registry does not know,
named by the hint, is the Add path for a new organization, not a stop.
When the run proposes an Update against a record that exists,
the new source is numbered after the existing ones, the new claims are
matched against the existing record with digits masked — a matched pair whose
numbers disagree, or that drops a recorded number, lands on the sheet under
"Cross-source checks" — and the draft is the **merged** record: the existing
record with the update's sources, list items, evidence links, and metadata
appended at the end of their lists, single-valued fields kept as recorded
(differences become renderer notes for a person), and the page-content block
keeping its recorded answers except where the new run reviewed a question.
Nothing is reordered, rewritten, or removed. The
run manifest records the model strings the APIs
returned, the prompt and question versions, per-stage token usage and cost,
cache hits, the claim-ID-to-path compatibility map, and — for every model
stage — the sha256 digests of the exact request inputs each call read
(`input_hashes`). A warm rerun that replays a stage lists the same digests
with `calls: 0`, so an auditor can confirm the rerun read the same inputs
without re-deriving them. The page metadata the SDK returns travels into
the extraction record (`published_at`, `language`, `description`); when
today's source schema has no field for a value — language and description
today — the manifest's `not_carried` map names where it went and the sheet
says so.

## Secrets and `.env`

The adapters read keys from the environment only. Put them in a git-ignored
`.env` at the repository root, beside the DataForSEO keys of the SEO pulse;
the CLI seeds the environment from that file at startup, and an exported
variable always wins over the file:

- `STEEL_API_KEY` — the Steel API key for capture staging (stage 1).
- `OPENAI_API_KEY` — the writer model (stages 4 and 8).
- `TYPESAFE_API_KEY` — Jev (stages 3, 6, and 9).

No key value is ever written to a manifest, a review sheet, a log, or a commit.
The private-data check in `npm run verify` stays the last guard.

## How to rerun one stage

Offline stages (`segment`, `resolve`, `verify`, `render`, `review`) rerun from
a run directory's artifacts; the new output lands beside the original as
`<artifact>.rerun`. Model-driven stages come from their caches — Jev under
`.intake/cache/jev.json`, the writer under `.intake/cache/writer.json` — so a
warm-cache rerun of the whole run makes no new model calls and reproduces the
draft byte for byte (drafts are never overwritten; the rerun writes its own
directory). The writer's input never includes the staging header, whose
capture timestamp would otherwise change the cache key on every run. A cold
rerun can differ, because the writer model is not deterministic; the manifest
records which happened, with per-stage cache hits.

## What the pipeline never does

- It never commits, opens a pull request, or publishes.
- It never writes `unreported`; silence renders as `not-reviewed` with a note.
- It never accepts a claim whose quote code has not found in the capture.
- It never reconstructs a source from snippets, a search result, or memory.
- It never carries an e-mail address the writer produced past the stage that
  produced it: stages 4 and 8 stop with a report (`intake/privacy.py`, the
  same pattern the repository-level scan uses). A person's name is not
  mechanically detectable; that check stays on the sheet's decision list.

## The batch backtest

`backtest --records all` is the Phase 2 gate. It walks every record under
`data/agents/`, skips the records without captures (they are listed), and for
each captured record extracts claims with the writer over that record's own
captures, verifies the quotes, and compares the result with the human record.
One budget reservation covers the whole batch; when it refuses, the batch
stops and the sheet says so. A writer failure stops the batch the way it
stops a run. The sheet pools recall, precision, locator agreement, and
unverified quotes, and lists each record's row. A measurement only; nothing
is applied.

## The adjudicated evaluation

The Phase 3 calibration runs in two steps. `evals --items <path>` samples
claim-and-passage pairs from the authored records (deterministic seed,
append-only file) and writes the item set for two human labellers. They fill
`labels.labeller_a` and `labels.labeller_b` on every item from the original
evidence; a person then fills `labels.adjudicated`. `evals --items <path>
--score` asks Jev the same items — the item's passage becomes the judged state
verbatim, through the same five questions and the same coarse gate the
pipeline uses — and scores material-defect recall and alert precision against
the adjudicated labels. Verdicts are cached, so a warm rerun makes no new
calls.

Three mechanics from the Plan 016 design ride along. `--track retrieval`
builds the items by lexical search over each capture instead of the recorded
locator, so the evaluation also measures the judge on searched passages
(`--track oracle` is the default). `--split-dir <dir>` writes grouped
`calibration.json` and `test.json` files — whole records stay on one side, so
near-duplicate claims cannot leak across the split. `--repeats N` repeats
every item with permuted order for the permutation-and-repeat stress, and
`--score` then reports the fraction of repeated groups that got identical
verdicts. Once labels exist, the scored report also carries the calibration
Plan 016 asks for, per question and never averaged: the relation question's
Brier score, reliability bins over the chosen answer's confidence, and a
threshold sweep — at each candidate `stated` bound, how many items the gate
would accept and how many of those were material defects. The labellers and
the live pass are the blocked part: the pass needs `TYPESAFE_API_KEY`, the
labels need two people.

## Backfill apply and drift

`backfill` (above) writes a dry-run report of locator proposals. Start with
`backfill --rank`: it lists the records by unlocated evidence paths, worst
first — the order Phase 5's batching follows — and makes no model call. Pass
`--proposals <path>` to also write the JSON list `backfill-apply` consumes:
one entry per verified quote, each carrying `approved: false`. The writer
sees the whole claim list in one call per record (the cost table's operating
point), and each found quote is verified, number-checked, and graded on its
own. The review
sheet shows every proposal's quote beside its locator. Each exactly verified
proposal is also graded with the five judge questions over its paragraph
cluster; the relation verdict and the actor score ride on the sheet as
advisory columns, cached by claim and passage. Without `TYPESAFE_API_KEY`
the sheet says `not judged` and nothing fails. A person reads each
quote against its capture, sets `approved: true` on the entries that hold,
and hands the file to `backfill-apply`. It then edits only the
`locator` fields named by the approved proposals. It refuses unapproved
entries, unknown evidence paths, and links that already carry a different
locator. It never reorders, rewrites, or removes anything. After it runs,
regenerate the data outputs and open the pull request yourself.

`drift` rescrapes every captured source without saving, compares the page with
its preserved capture (the capture header stripped, marks and whitespace
normalised), and writes `.intake/drift/report.json` plus a Markdown sheet to
standard output. Changed sources list their changed line spans and the claims
whose locators fall inside them. Each affected claim is then re-judged
against the rescraped text through the same five judge questions; the
verdicts are advisory columns on the sheet, cached by claim, passage, and
question version. Blocked rescrapes are listed, never hidden. Without
`TYPESAFE_API_KEY` the command still reports changed sources and affected
claims, without verdicts — it does not die at the first changed source
after spending its rescrapes. The pipeline
proposes a new capture under a new source ID; a person captures and reviews.
There is no schedule yet — run it by hand (see the plan's open decision 4).

## Status

- Phase 0 (models, renderer, backtest scaffold): done.
- Phase 1 (capture staging, segmentation, identity): implemented; the live
  SDK-versus-CLI comparison of the STOP line needs `STEEL_API_KEY` and has not
  been run. Staging and promotion are tested offline against fixture scrapes
  and the existing captures.
- Phase 2 (extraction, quote verification, numbers, backtest, backfill):
  implemented behind the writer adapter (`openai==3.18.0`, model `gpt-6-sol`,
  structured output, one retry, budget reservation). The backtest over the 66
  records and the backfill dry run over the unlocated claims need
  `OPENAI_API_KEY` and have not run; their machinery is tested offline with a
  fake writer over real captures.
- Phase 3 (Jev judgments, coarse gate, evaluation harness): implemented. The
  judgment cache lives under `.intake/cache/`. The adjudicated evaluation is
  blocked twice: the live Jev pass needs `TYPESAFE_API_KEY`, and the labels
  need two human labellers. Gate thresholds are provisional until then;
  `evals --items <path> --score` is the command that runs once both exist.
- Phase 4 (writing, preflight, run orchestration, review sheet, skill,
  operator document): implemented; the whole pipeline is tested end to end
  offline over a real capture with fake services. The acceptance queue for
  the three coverage-backlog leads is committed at
  `queue/acceptance-2026-09-11.yaml`; the run itself needs both live keys
  and has not run.
- Phase 5 (backfill apply, drift, schedule): apply and drift implemented and
  tested offline (eleven tests over the real zup capture with a fake Steel
  adapter). The live backfill proposals need `OPENAI_API_KEY`, and their
  stage 6 grading needs `TYPESAFE_API_KEY` (without it the sheet says
  `not judged`); one live drift
  report needs `STEEL_API_KEY`; none has run. The schedule was rejected per
  the plan's open decision 4: run the drift report by hand for two months
  first. A gate repair shipped with this phase: `ruff format` now checks Python
  code blocks inside Markdown, so `plans/016-jev-investigation.md` was
  reformatted.
