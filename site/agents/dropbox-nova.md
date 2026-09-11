Source: https://internal-agents.com/#dropbox-nova

Dropbox Platform

# Nova

An internal platform for coding agents: engineers launch parallel sessions and internal systems invoke agents inside automated SDLC workflows.

Coding CI triage On-call Maintenance

agent-assisted SDLC workflow → accepted change: Unknown

Operating model, claims & sources

#### Scoped operating models

**agent-assisted SDLC workflow → accepted change** Unknown · Level unknown

#### Summary and context

Summary

An internal platform for coding agents: engineers launch parallel sessions and internal systems invoke agents inside automated SDLC workflows.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Dozens of agents can run in parallel from one runbook

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Migration-owner orchestration of dozens of agents from a shared runbook; qualitative capacity description

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

Key observation

Flaky-test remediation (Deflaker): 100+ validation runs

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   CI validation runs per proposed Deflaker flaky-test fix

Denominator
:   Unknown

Method
:   Run the test 100 or more times depending on its failure rate; retry capped at five fix attempts

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 58–62

Key observation

Predecessor Goose-based migrator used across thousands of migration entries before workflows moved onto Nova

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Predecessor Goose-based migrator, before workflows moved onto Nova

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

Key observation

Dozens of agents launchable from one runbook

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Migration-owner orchestration of dozens of agents from a shared runbook; qualitative capacity description

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

#### Architecture and primitives

Sandbox

Isolated env with a codebase snapshot at a specific commit; full Dropbox monorepo via Bazel; hermetic remote execution + caching

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Harness

Validation loop (propose → validate → feed back) with continue\_on\_validation\_failure and max\_iterations (~5); branch management kept outside the agent

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Model

Platform-agnostic; multiple coding agents behind one interface; swap models without rebuilding infra; prompt-eval tooling

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Interfaces

web, cli, api, slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Tool access

Skills/plugins to gather evidence, read logs, inspect failures; MCP integrations; Bazel-aware selectivity tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Knowledge

Localized AGENTS.md per service; Dash (Dropbox context engineering); passing + failing test logs

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Credentials

Operates within Dropbox's existing infra and validation paths; same auth/authz as engineers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Context management

Session history (notes/logs) carried across retry attempts

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Supporting component

Bounded iteration with feedback on failure; deterministic systems control test execution

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Supporting component

Dropbox context-engineering system feeding agents across the SDLC

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Platform value exceeds code generation; validation, guardrails, and context matter as much

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Context, validation, and guardrails reinforce each other to make background work trustworthy

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Not every step belongs in the agent loop; deterministic systems should control test execution and timing

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Integrate with existing engineering infrastructure rather than building separate AI-specific workflows

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for agent-assisted SDLC workflow → accepted change; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The source documents human participation but does not locate one consistent attention boundary across Nova workflows.

Observation date
:   2026-05-22

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Sources

1. [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md)  <https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Hacker News submission for Nova](https://news.ycombinator.com/item?id=48235065) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-2/content.md)  <https://news.ycombinator.com/item?id=48235065> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#dropbox-nova)
