Source: https://internal-agents.com/#cloudflare-ai-stack

Cloudflare Platform

# Internal AI engineering stack

An internal platform of MCP servers, an access layer, and AI tooling (incl. an AI code reviewer) that makes agents useful inside Cloudflare.

Coding Code review

pull request → AI review findings: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → AI review findings** Work product review · Level 3

#### Summary and context

Summary

An internal platform of MCP servers, an access layer, and AI tooling (incl. an AI code reviewer) that makes agents useful inside Cloudflare.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)
- Contextualizes [Hacker News discussion of Cloudflare's internal AI engineering stack](https://news.ycombinator.com/item?id=47837240) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-2/content.md) (community)

#### Reported metrics

Headline claim

47.95 million AI requests in 30 days across the internal AI engineering system

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Cloudflare

Scope
:   Internal AI engineering requests in the 30 days preceding the report

Denominator
:   Unknown

Method
:   Company-reported AI Gateway count for the preceding 30 days

Observation date
:   2026

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party) Preserved content.md, lines 14–20

Key observation

3,683 internal users (60% of company, 93% of R&D)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Cloudflare

Scope
:   Active internal AI coding-tool users in the preceding 30 days

Denominator
:   Approximately 6,100 employees for company share; R&D organization for R&D share

Method
:   Unknown

Observation date
:   2026

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party) Preserved content.md, lines 14–16

Key observation

47.95M AI requests and 241.37B tokens via AI Gateway in the preceding 30 days

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Cloudflare

Scope
:   Internal AI requests and AI Gateway tokens in the preceding 30 days

Denominator
:   Unknown

Method
:   Reported request counts and AI Gateway token counts

Observation date
:   2026

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party) Preserved content.md, lines 14–20

Key observation

10,952 merge requests in the week of March 23, 2026, nearly double the Q4 baseline; four-week average above 8,700

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Cloudflare

Scope
:   Company merge requests in the week of March 23, 2026, versus Q4 baseline; not agent-authored PRs

Denominator
:   Unknown

Method
:   Weekly merge-request count; distinct from the four-week rolling average

Observation date
:   2026-03

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party) Preserved content.md, lines 25–29

Key observation

295 teams using agentic AI tools

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Cloudflare

Scope
:   Teams using agentic AI tools and coding assistants in the reported 30-day snapshot

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party) Preserved content.md, lines 14–18

#### Architecture and primitives

Sandbox

Dynamic Workers for sandboxed code execution; Sandbox SDK to clone/build/test

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Harness

OpenCode + Windsurf clients; Agents SDK (McpAgent + Durable Objects) for stateful sessions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Model

Workers AI (open-weight, on-platform) + frontier models (Opus, GPT), routed by task

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Interfaces

cli, ci, web

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Tool access

MCP Server Portal; one OAuth point aggregating 182+ tools from 13 servers; AI Gateway for routing, cost, BYOK, ZDR

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Knowledge

Backstage catalog (2,055 services) + AGENTS.md generated across ~3,900 repos

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Credentials

Zero API keys on client machines; a Worker injects keys server-side; Cloudflare Access (Zero Trust) auth

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Context management

Code Mode collapses upstream tool schemas into search + execute, holding token overhead constant at scale

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Supporting component

One OAuth aggregation point for all MCP tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Supporting component

Collapse N tool schemas into 2 calls to hold token overhead constant at scale

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Supporting component

Structured, generated repo context (runtime, nav, conventions, boundaries, deps)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Supporting component

Multi-agent CI review: risk tiering, specialist agents, Codex-rule citations

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Centralize through a proxy early; direct-to-gateway looks simpler but blocks per-user attribution, model cataloging, and policy later

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Lesson

Without structured data, agents are working blind; they read code but can't see the system around it (Backstage / AGENTS.md)

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Lesson

Tool schemas eat context (34 GitLab tools ≈ 7.5% of a 200K window); collapse them at the portal

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

Lesson

Frontier + open-source hybrid: route a growing share of workloads to cheaper self-hosted models

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for pull request → AI review findings; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents automated review findings, but the record combines several platform workflows.

Observation date
:   2026-04-20

- Supports [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md) (first-party)

#### Sources

1. [The AI engineering stack we built internally](https://blog.cloudflare.com/internal-ai-engineering-stack/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-1/content.md)  <https://blog.cloudflare.com/internal-ai-engineering-stack/> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Hacker News discussion of Cloudflare's internal AI engineering stack](https://news.ycombinator.com/item?id=47837240) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/cloudflare-ai-stack-source-2/content.md)  <https://news.ycombinator.com/item?id=47837240> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#cloudflare-ai-stack)
