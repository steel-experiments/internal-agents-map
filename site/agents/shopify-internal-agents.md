Source: https://internal-agents.com/#shopify-internal-agents

Shopify Platform

# Aquifer / River

The Aquifer agent platform (session/harness/sandbox split) powers River, a Slack-native coding agent, plus research, migration, and app-security agents.

Coding Code review Research Security

River coding request → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**River coding request → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

The Aquifer agent platform (session/harness/sandbox split) powers River, a Slack-native coding agent, plus research, migration, and app-security agents.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

1 in 8 merged PRs company-wide coauthored by River

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   Merged River-coauthored PRs across Shopify

Denominator
:   All Shopify merged pull requests

Method
:   Unknown

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 12

Key observation

River: 59,918 sessions / 30 days across 5,170 Slack channels

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   River sessions and distinct Slack channels in a recent 30-day period

Denominator
:   Unknown

Method
:   river\_sessions domain table, written by River every session

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 83

Key observation

3,536 River-coauthored PRs merged; 1 in 8 merged PRs company-wide

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   River-coauthored merged PRs in the recent 30-day period; company-wide PR share

Denominator
:   All Shopify merged pull requests for the one-in-eight share

Method
:   river\_sessions domain table for reported session-linked counts

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 12, 83

Key observation

Median session 19 min; median 50 tool calls/session

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   Median River session duration and tool calls per session

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 65

#### Architecture and primitives

Sandbox

An execution environment (filesystem, shell, repo, build/test) separated from the harness; Shopify credits the brain-and-hands framing to Anthropic

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Harness

Session (durable; Postgres append-only event log) + Harness (cheap agent loop) + Cell (ephemeral Go runtime); cells die, sessions persist

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Model

The design lets Shopify change the model without changing the sandbox

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Interfaces

slack, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Tool access

Repo + tests + data warehouse + production traces + PR creation; a gateway credentials proxy

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Knowledge

Monorepo 'World' (code + skills + conventions + intent docs + runbooks + AGENTS.md); Nix reproducible envs; Slack-transcript corpus mining

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Credentials

Gateway credentials proxy; per-profile sandbox policies; Shopify SSO

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Context management

Skills loaded on-demand as files, updatable per session; session survival across cell/sandbox/machine death

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Durable identity, disposable loop, isolated execution; swap any layer independently

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Slack-native coding agent in public channels only; visibility drives adoption

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Written-down knowledge mined from successful patterns and public transcripts

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Agent-friendly is human-friendly; monorepo, reproducible envs, written skills, and fast CI help both

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Local agents have a ceiling; private windows mean only the person at the keyboard learns anything

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Session survival is critical; cells die, sandboxes die, machines die; the conversation doesn't

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Treat agents as profiles, not platforms; a new agent is a new bundle on the same substrate

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for River coding request → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents pull-request creation but does not establish outcome-only supervision.

Observation date
:   2026

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Sources

1. [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md)  <https://shopify.engineering/under-the-river> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#shopify-internal-agents)
