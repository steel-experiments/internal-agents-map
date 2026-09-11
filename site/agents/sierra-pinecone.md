Source: https://internal-agents.com/#sierra-pinecone

Sierra Task agent

# Pinecone

One company-wide agent that collapsed separate support, analytics, engineering, and sales agents into a single runtime with an MCP Gateway to 45 systems.

Coding Code review Support Research Data

employee request → reviewed agent output: Work product review

Operating model, claims & sources

#### Scoped operating models

**employee request → reviewed agent output** Work product review · Level 3

#### Summary and context

Summary

One company-wide agent that collapsed separate support, analytics, engineering, and sales agents into a single runtime with an MCP Gateway to 45 systems.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)
- Supports [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md) (first-party)

#### Reported metrics

Headline claim

More than 75,000 sessions created by 600 people in the month preceding the report

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sierra

Scope
:   Pinecone users and sessions in the month preceding the report; calendar month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party) Preserved content.md, lines 134–139

Key observation

More than 75,000 sessions created by 600 people in the month preceding the report

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sierra

Scope
:   Pinecone users and sessions in the month preceding the report; calendar month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party) Preserved content.md, lines 134–139

Key observation

70% of company PRs opened through Pinecone in the month preceding the report

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sierra

Scope
:   Company PRs opened through Pinecone in the month preceding the report

Denominator
:   Sierra PRs opened in that month; not merged PRs

Method
:   Unknown

Observation date
:   Unknown

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party) Preserved content.md, lines 138

#### Architecture and primitives

Sandbox

Agency layer reconciles recoverable Kubernetes runners; conversation/events/checkpoints stay durable separately

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Harness

App server + Agency + runners; intent-based model/environment routing (Claude Code + Codex)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)
- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Model

Claude Code + Codex; routes by intent (planning, coding, prose)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

Interfaces

slack, web, linear, mobile

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

Tool access

MCP Gateway connected to 45 systems; a network proxy decides whether privileged requests proceed and injects credentials after approval

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md) (first-party)

Knowledge

Durable sessions over disposable environments; Redis Streams

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)
- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Credentials

Gateway enforces the invoking employee's access at tool-call time and isolates customer data; the harness never holds the real secret

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md) (first-party)
- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Context management

Durable session state separated from ephemeral compute

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Supporting component

One gateway spanning 45 systems, enforcing employee permissions at call time

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md) (first-party)

Supporting component

Recoverable K8s runners with a network proxy for credential injection

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Supporting component

Routes model and environment by request intent, independent of the tool layer

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Collapse departmental bots into one agent; cross-functional jobs don't respect org-chart boundaries

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

Lesson

Own the routing/context/workflow layer; let models be interchangeable (different models win at planning, coding, prose)

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)
- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Lesson

Enforce permissions at the tool-call layer via a gateway, not via prompt instructions

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md) (first-party)
- Supports [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md) (first-party)

Lesson

Session counts and tool calls are usage, not value; track business outcomes instead

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for employee request → reviewed agent output; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents delegated work through a company-wide agent without establishing outcome-only supervision.

Observation date
:   2026

- Supports [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md) (first-party)

#### Sources

1. [Pinecone: harnessing the wisdom of the workforce](https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-1/content.md)  <https://sierra.ai/jp/blog/pinecone-harnessing-the-wisdom-of-the-workforce> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Building Sierra's MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-2/content.md)  <https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Agency: secure, scalable sandboxes for agents](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sierra-pinecone-source-3/content.md)  <https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#sierra-pinecone)
