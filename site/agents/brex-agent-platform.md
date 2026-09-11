Source: https://internal-agents.com/#brex-agent-platform

Brex Platform

# Internal Agent Platform

Retool-based internal platform where employees build, test, and deploy agents for KYC, disputes, QA, collections, and operations.

Finance ops Support Customer success

internal operations request → completed operation: Continuous steering

Operating model, claims & sources

#### Scoped operating models

**internal operations request → completed operation** Continuous steering · Level 2

#### Summary and context

Summary

Retool-based internal platform where employees build, test, and deploy agents for KYC, disputes, QA, collections, and operations.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Reported metrics

Headline claim

Dispute processing time fell from three hours to three seconds

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Dispute-submission preparation using the internal agent platform; not end-to-end chargeback resolution

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 179–189

Key observation

50%+ of customer-support cases resolved by chatbot as first touch

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Customer-support cases resolved by the chatbot at first touch

Denominator
:   Customer-support cases; exact sample size not provided

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 76

Key observation

Dispute processing: 3 hours → 3 seconds

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Dispute-submission preparation using the internal agent platform; not end-to-end chargeback resolution

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 179–189

Key observation

QA covers every support interaction; one person using AI instead of five QA specialists

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Quality assurance of customer-support interactions

Denominator
:   Every support interaction

Method
:   Agent applies the quality rubric to every response; one person oversees instead of five QA specialists

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 80

Key observation

KYC adverse-media accuracy 85% → 88%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   KYC adverse-media classification; human versus agent accuracy

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 163–167

#### Architecture and primitives

Sandbox

Retool-hosted runtime (no bespoke execution env described)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Harness

Retool-based builder with prompt management and multi-model testing/evaluation; built by a ~25-person systems-engineering team

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Model

Multi-model

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Interfaces

slack, internal-ui

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Tool access

An MCP server exposes external product features to the internal platform; new product tools become internally available immediately; invoked via Slack /c1

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Knowledge

Standard operating procedures uploaded as a knowledge base, such as 100-page dispute guides; customer account data

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Credentials

SSO via internal Retool proxies (no per-user accounts); ConductorOne access management; Okta auth; data classified by risk; ≤30-day retention, no training on inputs

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Supporting component

Non-technical ops staff design prompts, test across models, deploy with QA oversight

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Supporting component

Product features exposed to internal agents through one MCP server

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Lessons and interpretation

Lesson

Target 40% automation, not 100%; the last mile drives investments that often yield zero value

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Brex reports that it manages the internal platform with practices used for an external product

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Don't skip the human in the middle; end-to-end automation fails on accuracy

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Map workflows to the discrete steps a human would take, then translate each to LLM instructions

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Architecture beats vendor; legal/data approvals should follow data-handling characteristics, not the tool name

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Level 2 for internal operations request → completed operation; human attention boundary: continuous-steering.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The secondary report describes a human remaining in the middle of the workflow, but does not fully specify each review surface.

Observation date
:   2025-09-25

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Sources

1. [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md)  <https://www.firstround.com/ai/brex> case-study · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#brex-agent-platform)
