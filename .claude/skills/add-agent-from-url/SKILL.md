---
name: add-agent-from-url
description: Assess a source URL for the Internal Agents Map catalog, or add or update a case when requested. Use for links describing an organization's internal agent or supporting system.
---

# Assess or add a case from a URL

Use [CONTRIBUTING.md](../../../CONTRIBUTING.md#inclusion-rules) as the inclusion policy.
Read [data/schema.md](../../../data/schema.md) when writing records. Paths below are relative
to the repository root.

## Match the request

For questions such as “does this qualify?”, return an assessment without editing files.
For a request to add or update a case, make the corresponding local edits. Existing authorization
continues to apply. Do not infer permission to commit or publish from an assessment or add request.
Check the working tree before editing and preserve unrelated changes.

## Read the evidence

Fetch the source and follow references to original material when available. If it is unavailable,
look for a verified preserved copy or replacement source. Do not reconstruct it from snippets or
memory. Without readable evidence, report Needs evidence and identify the missing source.

Extract the organization, internal workflow, and what the team built or adapted. Record the
implementation or use that the source describes, its date, and the publisher's relationship to
the work. Keep metric scopes, dates, denominators, and methods where reported.

Search `data/agents/` with `rg` for the organization, system, and aliases before choosing Add.
A matching system calls for Update, not a duplicate or exclusion.

## Make the decision

Apply the contribution guide's questions and return Add, Update, Needs evidence, or Out of scope.
Give the evidence and a short reason. For Needs evidence, name the unresolved fact. Do not score
cases numerically or require a product name. Commercial status does not decide eligibility.
Supporting systems can qualify when their connection to agent work is documented.

For an assessment, stop after the report. For an authorized catalog change:

- Add: create `data/agents/<id>.yaml` from `templates/agent.yaml`.
- Update: attach new sources and supported claims to the existing record. If the source adds
  nothing new, report that no change is needed.
- Needs evidence or Out of scope: record the reason and source in `docs/coverage-backlog.md`.
  Update an existing lead rather than duplicating it. Preserve dated decision history.

## Write and check the change

Link each claim to source evidence. Distinguish reported claims from catalog judgments and
assess confidence from the support for each claim. Source type alone does not determine confidence.
Company metrics remain self-reported unless independently verified. Unknown means undocumented.

Preserve accepted sources using the contribution guide's source-preservation procedure. Review
the captured text before linking it. The original URL remains the citation. A capture preserves
what was available; it does not make a claim more reliable. Do not save an error or access-control
page as evidence. If preservation fails, report the collection blocker separately from eligibility
and leave the change incomplete. Retain any local draft and list its path and blocker in the
report, so the user can distinguish unfinished work from a completed addition. Do not bypass
access restrictions or weaken validation.

For operating models, record the task scope and documented human review boundary. Each assessment
needs dated claim metadata with `catalog-judgment` provenance. Levels are derived by the build.
Do not derive them from autonomy labels or average different workflows.

Regenerate outputs with `uv run python scripts/build.py`. Run the verification commands in
[the pull request template](../../../.github/pull_request_template.md), including archive, site,
privacy, build, and local-link checks. Read the source against the claims as well: passing checks
cannot establish that an interpretation is correct.

If a check fails, fix the change within scope or report the blocker. Preserve unrelated work;
do not use a broad `git restore` to clean up. Do not commit or publish a failing change.

## Report

State the decision, supporting evidence, and any unresolved question. For edits, include the
record or backlog path and check results. Report commits or publication only when authorized
and completed. Do not claim independent verification from repeated agent agreement.
