Source: https://internal-agents.com/#posthog-stamphog

PostHog Background agent

# StampHog

A GitHub-label-triggered PR approval agent that applies fail-closed deterministic safety gates, asks an LLM to check for showstoppers, autonomously approves eligible changes, and refuses or escalates the rest.

Code review

eligible pull request → approval decision: Exception only

Operating model, claims & sources

#### Scoped operating models

**eligible pull request → approval decision** Exception only · Level 5

#### Summary and context

Summary

A GitHub-label-triggered PR approval agent that applies fail-closed deterministic safety gates, asks an LLM to check for showstoppers, autonomously approves eligible changes, and refuses or escalates the rest.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Add a PR auto-stamper
- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

#### Reported metrics

Headline claim

Handled 1,600 PRs in the previous month, as reported on July 9, 2026; roughly one in three merged main-repository PRs received its final approval during the reported quarter

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   PostHog reports two different windows in its July 9, 2026 article; exact monthly and quarterly boundaries are not supplied.

Reported by
:   PostHog

Scope
:   Monthly PRs handled autonomously and quarterly final approvals in the main repository

Denominator
:   Merged main-repository PRs for the quarterly share; absolute handled PRs for the monthly count

Method
:   Company-reported production usage

Observation date
:   2026-07

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 105, 118

Key observation

1,600 PRs handled autonomously in the previous month, as reported on July 9, 2026

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   July 9 is the report date; the source says last month without exact measurement boundaries.

Reported by
:   PostHog

Scope
:   PRs handled autonomously in the previous month, as reported on July 9, 2026; exact boundaries unspecified

Denominator
:   Unknown

Method
:   Company-reported production usage

Observation date
:   2026-07-09

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 118

Key observation

Roughly one in three PRs merged into PostHog's main repository received StampHog's final approval during the reported quarter

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   PostHog

Scope
:   Main-repository merged PRs receiving StampHog final approval during the reported quarter

Denominator
:   Merged PRs in the main repository

Method
:   Company-reported production usage

Observation date
:   2026-07

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 105

Key observation

20% of PRs approved by StampHog in the July 28, 2026 report, at approximately $300 per month in tokens

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   PostHog

Scope
:   PostHog PRs approved by StampHog and monthly token cost in the July 28, 2026 report

Denominator
:   PostHog PRs in the report's scope

Method
:   Company-reported production usage and token spend

Observation date
:   2026-07

- Supports [10,000 PRs a month is easy: How devex is evolving at PostHog](https://posthog.com/blog/10k-prs-a-month) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-2/content.md) (first-party) Preserved content.md, lines 131

#### Architecture and primitives

Harness

A GitHub Action invokes a Python pipeline that fetches and classifies a PR, applies hard gates, waits for in-flight reviewer bots, runs an LLM review, and posts a verdict

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works and Architecture

Model

Claude through the Claude Agent SDK, with Read, Grep, and Glob tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Interfaces

github, ci

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage

Tool access

Reads the diff and repository files plus trusted review-state, discussion, ownership, and reviewer signals

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Knowledge

Repository-specific deny categories, size and risk tiers calibrated from prior human approvals, review guidance, and ownership data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Tiers and Empirical basis

Credentials

A dedicated Anthropic organization secret and a StampHog GitHub App token whose approvals satisfy branch protection

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage and final verdict

Context management

Each run emits a versioned JSON evidence bundle retained as a CI artifact for 30 days; a sticky GitHub comment carries non-approval verdict history and labels preserve retry state

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage and Evidence bundle

Supporting component

Draft state, conflicts, requested changes, sensitive paths, size ceilings, and risk tiers can block AI approval; the LLM may tighten but never loosen a gate

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

Supporting component

Eligible changes can be approved while risky, ambiguous, or insufficiently assured changes are refused or escalated to a suitable human reviewer

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Add a PR auto-stamper
- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Supporting component

Each run records PR metadata, classification, gate results, reviewer output, and the final verdict

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Evidence bundle

#### Lessons and interpretation

Lesson

Use deterministic controls for known risks and allow the LLM to make approval stricter, never more permissive

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code explicitly implements and documents this safety invariant.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

Lesson

Calibrate thresholds and deny categories from repository history rather than treating small diffs as inherently safe

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code documents calibration against historical approval outcomes.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Tiers and Empirical basis

Lesson

Fail closed and preserve retry state when dependencies, credentials, or concurrent reviewer bots are unavailable

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code explicitly documents fail-closed and retry behavior.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage

#### Operating model evidence

Operating model assessment

Level 5 for eligible pull request → approval decision; human attention boundary: exception-only.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   Eligible pull requests are approved automatically; risky or ambiguous cases are refused or routed to a human.

Observation date
:   2026-07-09

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party)

#### Sources

1. [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md)  <https://posthog.com/newsletter/code-review-tips> corporate-article · first-party · Last source verification: 2026-08-31
2. [10,000 PRs a month is easy: How devex is evolving at PostHog](https://posthog.com/blog/10k-prs-a-month) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-2/content.md)  <https://posthog.com/blog/10k-prs-a-month> engineering-blog · first-party · Last source verification: 2026-08-31
3. [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md)  <https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent> source-code · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#posthog-stamphog)
