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
   optional `company`, `system_name`, `record_id`, `source_role`, `homepage`
   hints. `source_role` names a provenance class from the catalog's own set
   and sets every source of the entry; an unknown value stops the queue.
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
3. Confirm `published_at` where the sheet flags it; fix `kind` on sources and
   confirm each `provenance_class` — the queue's `source_role` hint set the
   class when one was given, and without a hint the pipeline staged
   conservatively as `other` / `independent-secondary`.
4. The run already promoted its capture bundles under `archive/sources/`,
   archived its run manifest under `archive/intake/<record-id>/`, and wrote
   `company-entry.yaml` when the organization is new (the run directory and
   the archive copy both hold it). Review them, append the company entry to
   `data/companies.yaml`, regenerate the outputs, and open the pull request.
   `intake promote` remains for one-off staging bundles a run did not draft.

## Backfill and drift

- `uv run python -m intake backfill data/agents/<id>.yaml --budget-usd 10
  --proposals p.json` proposes locators for a record's unlocated claims (dry
  run, one writer call for the whole claim list); `p.json` holds one
  unapproved entry per verified quote, and each verified proposal is also
  graded — the relation verdict rides on the sheet, or `not judged` when
  `TYPESAFE_API_KEY` is absent. A person reads
  each quote on the sheet against its capture, sets `approved: true` on the
  entries that hold, and runs
  `uv run python -m intake backfill-apply p.json`, which edits only the
  `locator` fields. Regenerate the outputs and open the pull request yourself.
- `uv run python -m intake drift` rescrapes every captured source and reports
  changed lines with the claims that cite them (`.intake/drift/report.json`),
  re-judging the affected claims as advisory columns. There is no schedule;
  run it by hand (plan open decision 4). The report names the new source ID
  to capture each changed page under; a person captures and reviews.

## What the pipeline never does

- It never writes `unreported`; silence is `not-reviewed` with a note.
- It never accepts a claim whose quote code has not verified in the capture.
- It never commits, opens a pull request, or publishes. It writes draft and
  archive artifacts in the working tree for a person's pull request; nothing
  reaches `main` without that person.

## Configuration

`config.json` holds the model strings, prompt and question versions, the
coarse-gate thresholds with the model version they belong to, the default
budgets, and the fuzzy-quote similarity bound. A threshold without its model
version is invalid. The `evals/` folder holds the golden extraction records;
a change to a prompt or question version reruns the golden tests before it
ships: `uv run python -m unittest discover -s tests -p "test_intake_*.py"`.
