# The source intake pipeline

The intake pipeline turns a list of links into a reviewed catalog record draft.
It is specified in [Plan 017](../plans/017-source-intake-pipeline.md); this page
is the operator document. The pipeline drafts; a person decides. No stage writes
to `main`, opens a pull request, or marks a source reviewed.

## Commands

Run every command from the repository root:

```sh
uv run python -m intake capture <url>                 # stage 1: capture to .intake/captures/
uv run python -m intake promote <dir> --source-id ID  # promote a staging bundle into archive/sources/
uv run python -m intake segment --input <content.md> --output <paragraphs.json>  # stage 2
uv run python -m intake resolve --company X --system Y [--text-file f]           # stage 3
uv run python -m intake render --extraction <file> --output <draft.yaml> --reviewed-at YYYY-MM-DD
uv run python -m intake backtest --record <yaml> --extraction <file>
uv run python -m intake schema                        # export the extraction-record JSON schema
npm run verify                                        # the phase gate
```

## Secrets and `.env`

The adapters read keys from the environment only. Put them in a git-ignored
`.env` at the repository root, beside the DataForSEO keys of the SEO pulse:

- `STEEL_API_KEY` — the Steel API key for capture staging (stage 1).
- `OPENAI_API_KEY` — the writer model (stages 4 and 8; Phase 2).
- `TYPESAFE_API_KEY` — Jev (stages 3, 6, and 9; Phase 3).

No key value is ever written to a manifest, a review sheet, a log, or a commit.
The private-data check in `npm run verify` stays the last guard.

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
- Phases 2 to 5: not implemented; their stages need the writer-model and Jev
  adapters.
