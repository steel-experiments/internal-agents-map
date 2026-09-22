# The source intake pipeline

The intake pipeline turns a list of links into a reviewed catalog record draft.
It is specified in [Plan 017](../plans/017-source-intake-pipeline.md); this page
is the operator document. The pipeline drafts; a person decides. No stage writes
to `main`, opens a pull request, or marks a source reviewed.

## Commands

Run every command from the repository root:

```sh
uv run python -m intake run queue.yaml --budget-usd 2.00   # all twelve stages
uv run python -m intake review <run-id>                     # print a run's review sheet
uv run python -m intake stage render --run <run-id>         # rerun one offline stage
uv run python -m intake capture <url>                       # stage 1 alone
uv run python -m intake promote <dir> --source-id ID        # promote into archive/sources/
uv run python -m intake segment --input <content.md> --output <paragraphs.json>  # stage 2
uv run python -m intake resolve --company X --system Y [--text-file f]           # stage 3
uv run python -m intake render --extraction <file> --output <draft.yaml> --reviewed-at YYYY-MM-DD
uv run python -m intake backfill data/agents/<id>.yaml --budget-usd 10           # locator proposals, dry run
uv run python -m intake backtest --record <yaml> --extraction <file> [--compatibility <json>]
uv run python -m intake schema                               # export the extraction-record JSON schema
npm run verify                                               # the phase gate
```

A queue file is a YAML list; each entry holds `urls` (HTTPS) and optional
`company`, `system_name`, `record_id`, and `homepage` hints:

```yaml
- urls: [https://example.com/posts/agents]
  company: Example
  system_name: Example agent
```

## Reading a run

Each run lives under `.intake/runs/<run-id>/` and is never overwritten:
`review.md` (the sheet), `run.json` (the manifest), `identity.json`,
`paragraphs-s*.json`, `extraction.yaml`, and `extraction-gated.yaml`. Drafts
land under `drafts/`. Staging captures live under `.intake/captures/` and the
Jev cache under `.intake/cache/`; all three are gitignored and regenerable.

The review sheet lists every claim with its quote, its line locator, its
numeric check, its Jev verdicts with probabilities, its disposition, and the
open questions. It names the decision the pipeline proposes and the decision a
person must make. The run manifest records the model strings the APIs
returned, the prompt and question versions, per-stage token usage and cost,
cache hits, and the claim-ID-to-path compatibility map.

## Secrets and `.env`

The adapters read keys from the environment only. Put them in a git-ignored
`.env` at the repository root, beside the DataForSEO keys of the SEO pulse:

- `STEEL_API_KEY` — the Steel API key for capture staging (stage 1).
- `OPENAI_API_KEY` — the writer model (stages 4 and 8).
- `TYPESAFE_API_KEY` — Jev (stages 3, 6, and 9).

No key value is ever written to a manifest, a review sheet, a log, or a commit.
The private-data check in `npm run verify` stays the last guard.

## How to rerun one stage

Offline stages (`segment`, `resolve`, `verify`, `render`, `review`) rerun from
a run directory's artifacts; the new output lands beside the original as
`<artifact>.rerun`. Model-driven stages come from their caches, so a
warm-cache rerun of the whole run makes no new model calls. A cold rerun can
differ, because the writer model is not deterministic; the manifest records
what happened.

## What the pipeline never does

- It never commits, opens a pull request, or publishes.
- It never writes `unreported`; silence renders as `not-reviewed` with a note.
- It never accepts a claim whose quote code has not found in the capture.
- It never reconstructs a source from snippets, a search result, or memory.

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
  need two human labellers. Gate thresholds are provisional until then.
- Phase 4 (writing, preflight, run orchestration, review sheet, skill,
  operator document): implemented; the whole pipeline is tested end to end
  offline over a real capture with fake services. The acceptance run over
  three coverage-backlog leads needs both live keys and has not run.
- Phase 5 (backfill apply, drift, schedule): see the plan's execution log.
