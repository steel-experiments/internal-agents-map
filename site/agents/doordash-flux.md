Source: https://internal-agents.com/#doordash-flux

DoorDash Platform

# Flux / Agentic AI Platform

DoorDash's internal agentic AI platform; a unified cognitive layer over company data and operations, with an AI Marketplace of specialized agents and the Flux cloud-agent runtime for engineering tasks.

Code review Coding CI triage On-call Maintenance Data

engineering task → reviewed agent output: Work product review

Operating model, claims & sources

#### Scoped operating models

**engineering task → reviewed agent output** Work product review · Level 3

#### Summary and context

Summary

DoorDash's internal agentic AI platform; a unified cognitive layer over company data and operations, with an AI Marketplace of specialized agents and the Flux cloud-agent runtime for engineering tasks.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant)
- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

#### Reported metrics

Headline claim

130,000 engineering tasks automated in one month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report of a one-month count; this is the observation date, not the measurement window.

Reported by
:   DoorDash

Scope
:   Engineering tasks automated in one reported month; calendar measurement month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

130,000 engineering tasks automated in one month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report of a one-month count; this is the observation date, not the measurement window.

Reported by
:   DoorDash

Scope
:   Engineering tasks automated in one reported month; calendar measurement month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

25,000+ automated code reviews per week

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report; weekly measurement boundaries are not supplied.

Reported by
:   DoorDash

Scope
:   Weekly automated code reviews powered by Flux

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

300+ playbooks; 10,000+ invocations per week

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   DoorDash

Scope
:   Unique playbooks and weekly invocations on Flux

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party) Preserved content.md, lines 10

#### Architecture and primitives

Sandbox

Firecracker microVMs; <5s p95 end-to-end setup (boot, clone repos, install tools, configure harness)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Harness

Maturity model: deterministic workflows -> ReAct agents -> hierarchical deep agents -> experimental swarms

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Model

Model-agnostic platform primitives support third-party or in-house agent components

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Interfaces

slack, github, scheduled, cli, skill, cursor

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Tool access

In-house MCP gateway ('Agent Gateway'); LangGraph orchestration; prospective A2A; tools declared per playbook with scoped, logged permissions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Knowledge

AI Marketplace of specialized agents; DataExplorer for grounded analytics; DoorDash-specific context in playbooks

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Credentials

Scoped per playbook; brokered through the gateway, never on the laptop; provenance on every action

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Context management

Hybrid retrieval: BM25 + dense semantic + reciprocal-rank fusion -> RAG; schema-aware SQL with EXPLAIN validation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Supporting component

Isolated Firecracker microVM with repos, tools, secrets, runtime deps

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

Governed, audited access to CI, observability, issue trackers, deploy, code search

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

YAML unit of agentic work: task, inputs, skills, tools, permissions, validation, outputs

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

Identifies schemas, generates grounded SQL, validates via EXPLAIN before execution

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Supporting component

Workflows -> agents -> deep-agent hierarchies -> swarms; governance hardens as control decentralizes

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

#### Lessons and interpretation

Lesson

Start narrow to earn trust; began with automated code review before CI triage, on-call, maintenance, ticket-driven dev

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Make the work visible; public Slack threads drove adoption; private per-run channels did not build team habits

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Playbooks need enablement; workshops and hackathons turn repeated operational work into reusable playbooks

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Earn complexity by exhausting simpler primitives first; keep swarms at the research frontier until governance catches up

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Lesson

Deterministic verification before probabilistic judgment; SQL linting and EXPLAIN before deeper validation; LLM-as-judge + DeepEval

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Lesson

Log provenance so any answer traces back to source queries, documents, and inter-agent activity

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for engineering task → reviewed agent output; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The platform spans several workflows; the cited engineering examples retain human review of agent output.

Observation date
:   2025-11-11

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

#### Sources

1. [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md)  <https://x.com/AIatDoorDash/status/2087285008906240193> social-post · direct-participant · Last source verification: 2026-08-31
2. [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md)  <https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md)  <https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#doordash-flux)
