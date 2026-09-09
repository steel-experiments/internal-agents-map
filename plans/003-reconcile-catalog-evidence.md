# Plan 003: Reconcile catalog evidence and record research limitations

> Executor: implement in an isolated worktree; reviewer maintains the index.
> Drift check: `git diff --stat e3a53f7..HEAD -- data docs README.md`
> Review any drift before editing. Other agents own tooling; do not revert their edits.

## Status

- Priority: P2
- Effort: M
- Risk: LOW (editorial accuracy requires source review)
- Depends on: Plan 002 for final generation and verification; research can run in parallel
- Category: docs, direction
- Planned at: commit `e3a53f7`, 2026-09-09

## Why this matters

Preservation now covers 88 sources but data extraction has not fully caught up.
Stripe's record calls its sandbox undocumented even though its preserved sources
explain EC2 devboxes. Only 51 of 645 evidence links have locators and 31 of 115
metric claims have structured dates. No claim currently uses contradicting evidence.
The aim is better traceability and honest limitations, not filling fields or
manufacturing disagreement to improve counts.

## Current state and conventions

Author `data/agents/*.yaml`; build generates `data/agents.json`, `docs/landscape.md`,
and marked blocks in README, patterns, and adoption observations. Read `data/schema.md`
and `CONTRIBUTING.md`. Preserve existing YAML style (PyYAML block style, order retained,
wide wrapping if serialized). Claims reference source IDs with relation supports,
contextualizes, or contradicts; `locator` can identify a stable source section or
immutable local snapshot line. Claim metadata supports valid_at, metric_scope,
denominator, measurement_method, confidence, and confidence_reason. Do not add fields.

- `data/agents/stripe-minions.yaml:31`: `sandbox: Not specified publicly`.
- `archive/sources/stripe-minions-source-2/content.md:24` states devboxes are AWS EC2
  instances. Lines 38 and 84 describe the goose fork and constrained QA environment.
  Read both first-party Stripe captures before updating architecture or metrics.
- Eight records have explicit undocumented/inapplicable sandbox prose: Block, Flex,
  Linear, Replit, Slack context system, Stripe, Uber coding agent, Y Combinator.
- Existing metrics may have different time/scope; preserve older reports explicitly.
  Source publication/capture dates are not automatically metric measurement dates.
- `docs/adoption-lessons.md` asks for failures and dissent; skepticism is context unless
  it actually contradicts a specific claim with evidence.

## Scope

In scope: `data/agents/*.yaml`, `data/schema.md` and `CONTRIBUTING.md` for concise
clarification of unknown/locator conventions if needed, `docs/evidence-review.md` (new),
`docs/adoption-lessons.md` and `docs/patterns.md` for source-grounded editorial additions,
and build-generated `README.md`, `docs/landscape.md`, `data/agents.json`.
Out of scope: scripts/tests owned by Plan 002, existing archive bytes or manifests,
new catalog approaches, invented facts, bulk new source captures, dependency changes.
No commit, push, or external message. Reviewer does any additional web research and
shares results; do not create unpreserved source records to meet a quota.

## Commands

Use the original checkout's absolute `.venv/bin/python` and `.venv/bin/ruff` from the
worktree. `python scripts/build.py` regenerates output; `python scripts/build.py --check`
then exits 0. `python scripts/archive_sources.py --check` verifies all 88 snapshots.
`python -m unittest discover -s tests`, `ruff check .`, `ruff format --check .`,
`python scripts/check_links.py --local`, and `git diff --check` must all pass after
Plan 002 is applied. The old local-link failure persists before Plan 002 integration.

## Steps

1. Read each of the eight affected records and their preserved sources. Correct
   concrete environments when the source supplies them; otherwise use canonical
   `unknown`, or omit an inapplicable optional sandbox and remove its claim/evidence
   metadata together. Do not invent a sandbox for a supporting context pattern.
   Reconcile Stripe's architecture, scope, and time-specific metrics with its captures.
   Add locators for changed claims and do not mark a publication freshly verified online
   merely because its existing snapshot was read. Verify build succeeds.
2. Perform a bounded traceability pass across all 115 current metric claims: read the
   linked snapshot passages, add precise locators when the passage can be identified,
   and add date/scope/denominator/method only where the source actually states them.
   Correct unsupported attribution or scope discovered during that pass. Distinguish
   an observation/publication date from a measurement period. Do not infer missing
   dates from capture timestamps or fill every claim with a generic section name.
   Record unresolved or unsupported cases per approach in docs/evidence-review.md.
   Verify build and archive --check succeed after each batch.
3. Review existing community commentary and first-party retrospectives for concrete
   failures, costs, negative results, and counterevidence. Add source-linked observations
   where warranted. Use contradicts only for a direct conflict with the same scoped
   claim; use contextualizes for skepticism and different time/method. Record actual
   findings and unresolved leads in docs/evidence-review.md, linking local snapshots.
   Incorporate reviewer-supplied research as leads when no preserved source exists.
   Verify each new prose link targets an existing file/heading.
4. In docs/evidence-review.md record review date, scope, before/after locator and metric
   metadata counts computed from JSON, a concise per-approach completion/gap table,
   and failure/counterevidence findings. This is an editorial pass, not independent
   verification of company metrics or an exhaustive ongoing research program.
5. Generate output in the worktree to validate all YAML. Report exact modified files,
   changes and remaining gaps. After review apply only owned changes to the current
   project. Regenerate again with Plan 002's final build code, then run every gate.

## Test plan and done criteria

- [x] Eight affected sandbox records reviewed; Stripe describes source-backed devboxes.
- [x] All original 115 metric claims reviewed, with outcomes/gaps documented per approach.
- [x] Locator coverage increases; added locators identify real supporting passages.
- [x] Dates/metric metadata have source support; missing information stays unknown.
- [x] Negative-result/counterevidence review has source-linked findings or explicit gaps.
- [x] All generated outputs current; all verification commands pass after Plan 002.
- [x] No existing archive artifact or manifest changed; reviewer marks index DONE.

## STOP conditions

Report if evidence cannot support a necessary correction, sources conflict without
resolvable scope/time, or a change requires new schema fields. Preserve uncertainty
and document the gap; lack of evidence is a completed research outcome, not permission
to guess. Do not rewrite stored captures or assign contradicts just to increase a count.

## Maintenance notes

Future intake should attach locators as claims are written. Keep metric dates separate
from capture/review dates. Normalize undocumented optional architecture consistently.
Re-run the traceability counts when this report is refreshed, with its review date.

## Completion — 2026-09-09

Applied reviewed changes to the current checkout and regenerated the catalog with
both plans integrated. All final gates passed: 97 unittest tests, 88 declared capture
validations, generated-file freshness, local links, Ruff lint/format, and whitespace.
Concurrent commits through `e67e79b` added an email-address check and four tests;
those changes were preserved, and the additional privacy gate also passed.

The reviewer independently verified the new report's local links and privacy check,
its exact ledger of all 115 baseline metric IDs, supporting locators for all 108
remaining metrics, and unchanged archive artifacts. Final export: 555 claims,
639 evidence links, 177 links with locators, and 16 documented environments.
Both plans are complete; unresolved source questions remain explicitly documented
in `docs/evidence-review.md`, rather than represented as verified facts.
