Source: https://internal-agents.com/#domu-clementino

Domu Task agent

# Clementino

A general-purpose 'AI colleague' spanning sales, finance, client ops, engineering, and recruitment, later split into a reusable toolkit plus Slack and desktop surfaces.

Support Finance ops Coding Recruitment Customer success

employee request → approved customer-impacting action: Work product review

Operating model, claims & sources

#### Scoped operating models

**employee request → approved customer-impacting action** Work product review · Level 3

#### Summary and context

Summary

A general-purpose 'AI colleague' spanning sales, finance, client ops, engineering, and recruitment, later split into a reusable toolkit plus Slack and desktop surfaces.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

~35 integrations organized into skills

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Domu

Scope
:   Clementino toolkit integration modules organized into skills

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party) Preserved content.md, lines 58–60

Key observation

~35 integrations organized into skills

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Domu

Scope
:   Clementino toolkit integration modules organized into skills

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party) Preserved content.md, lines 58–60

#### Architecture and primitives

Harness

Claude/Anthropic SDK wrapper; a reusable tool/skill/memory layer separated from the Slack and desktop interfaces

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Model

Claude (Anthropic SDK)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Interfaces

slack, desktop

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Tool access

~35 integrations organized into skills; specialist delegates per domain

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Knowledge

Four memory layers: conversation context, persistent facts, knowledge RAG, and live system state

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Credentials

Customer-impacting actions gated behind team-visible Slack approvals

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Context management

Four-layer memory separation; prompt size dropped substantially after splitting capabilities from the Slack layer

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Supporting component

Transient conversation, persistent facts, knowledge RAG, and live system state; kept separate

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Supporting component

Capabilities separated from the interface layer so they power multiple surfaces

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Separate reusable capabilities (tools/skills/memory) from the interface layer; prompt size drops while capability is preserved

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Lesson

Model memory explicitly: conversation context, persistent facts, RAG, and live state have different lifecycles

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Lesson

Gate customer-impacting actions behind human approvals rather than trusting the model

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for employee request → approved customer-impacting action; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source documents explicit human approval for customer-impacting actions.

Observation date
:   2026

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Sources

1. [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md)  <https://domu.ai/blog/why-we-split-our-internal-agent-in-two> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#domu-clementino)
