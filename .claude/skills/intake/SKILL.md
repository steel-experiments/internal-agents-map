---
name: intake
description: Draft a catalog record from one link or a list of links with the Plan 017 pipeline. Use when the owner supplies source URLs to assess or add, or asks to run, resume, or inspect an intake run.
---

# Run the source intake pipeline

Read [docs/intake-pipeline.md](../../../docs/intake-pipeline.md) for the commands and
[Plan 017](../../../plans/017-source-intake-pipeline.md) for the stage contracts. The
pipeline drafts; a person decides. Keep the [add-agent-from-url](../add-agent-from-url/SKILL.md)
policy: it owns eligibility; this skill owns execution.

## Before a run

1. Check that `.env` holds the keys the run needs: `STEEL_API_KEY` (capture),
   `OPENAI_API_KEY` (writer), `TYPESAFE_API_KEY` (Jev). Without a key, the run
   stops at the stage that needs it; report that as the blocker.
2. Write a queue file: one entry per candidate, each with `urls` (HTTPS) and
   optional `company`, `system_name`, `record_id`, `homepage`.
3. Agree the budget with the owner. Default `$2` per run; the run refuses to
   start above its worst-case reservation.

## The run

```sh
uv run python -m intake run queue.yaml --budget-usd 2.00
```

The command prints the run ID, the proposed decision, the draft path under
`drafts/`, and the review sheet path under `.intake/runs/<run-id>/review.md`.
Print a sheet again with `uv run python -m intake review <run-id>`; rerun an
offline stage with `uv run python -m intake stage render --run <run-id>`.

## After a run

1. Read the review sheet top to bottom. Confirm the identity decision and the
   eligibility proposal.
2. Edit every claim row with disposition `review`. The draft under `drafts/`
   is a starting point, not a result.
3. Confirm `published_at` where the sheet flags it; fix `kind` and
   `provenance_class` on sources (the pipeline stages conservatively as
   `other` / `independent-secondary`).
4. Promote the captures (`uv run python -m intake promote <staging-dir> --source-id <id>`),
   add the company entry when the run printed one, and open the pull request.
   The pipeline does none of this itself.

## Backfill and drift

- `uv run python -m intake backfill data/agents/<id>.yaml --budget-usd 10`
  proposes locators for a record's unlocated claims (dry run). A person adds
  `approved: true` to the entries that hold; then
  `uv run python -m intake backfill-apply <proposals.json>` edits only the
  `locator` fields. Regenerate the outputs and open the pull request yourself.
- `uv run python -m intake drift` rescrapes every captured source and reports
  changed lines with the claims that cite them (`.intake/drift/report.json`).
  There is no schedule; run it by hand (plan open decision 4). A changed
  source needs a new capture under a new source ID and a human review.

## What the pipeline never does

- It never writes `unreported`; silence is `not-reviewed` with a note.
- It never accepts a claim whose quote code has not found in the capture.
- It never commits, opens a pull request, or publishes.

## Configuration

`config.json` holds the model strings, prompt and question versions, the
coarse-gate thresholds with the model version they belong to, the default
budgets, and the fuzzy-quote similarity bound. A threshold without its model
version is invalid. The `evals/` folder holds the golden extraction records;
a change to a prompt or question version reruns the golden tests before it
ships: `uv run python -m unittest discover -s tests -p "test_intake_*.py"`.
