Source: https://internal-agents.com/#browserbase-bb

Browserbase Task agent

# bb

One generalized agent in Slack that writes PRs, investigates sessions, queries the warehouse, logs feature requests, and runs browser agents across engineering, ops, sales, and support.

Coding Code review Support Customer success Research

coding request → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**coding request → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

One generalized agent in Slack that writes PRs, investigates sessions, queries the warehouse, logs feature requests, and runs browser agents across engineering, ops, sales, and support.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Feature-request pipeline at 100% coverage with zero human effort

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Browserbase

Scope
:   Automatic feature-request scanning of every closed support ticket and meeting transcript

Denominator
:   Closed support tickets and meeting transcripts

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party) Preserved content.md, lines 26

Key observation

Feature-request pipeline at 100% coverage, zero human effort

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Browserbase

Scope
:   Automatic feature-request scanning of every closed support ticket and meeting transcript

Denominator
:   Closed support tickets and meeting transcripts

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party) Preserved content.md, lines 26

Key observation

99% of first-response times < 24 hrs

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   The source reports 99% below 24 hours with awkward wording; no sample, timestamps, or method is provided.

Reported by
:   Browserbase

Scope
:   Reported support first-response time below 24 hours

Denominator
:   Support first responses; exact sample and measurement window not provided

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party) Preserved content.md, lines 26

Key observation

Session investigation: 30–60 min of log-diving → one Slack message

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A Slack message replaces the manual initiation workflow; the article does not report end-to-end automated investigation latency.

Reported by
:   Browserbase

Scope
:   Session investigation initiation: manual log-diving versus a Slack request

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party) Preserved content.md, lines 26

#### Architecture and primitives

Sandbox

Ephemeral Linux VM; pre-warmed snapshot rebuilt every 30 min; idles out after 30 min

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Harness

OpenCode core loop with 6 tools (read/write/edit/exec/safebash/skill)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Model

Frontier models

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Interfaces

slack, web, webhook

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Tool access

exec routes through a serverless integration proxy (Snowflake, HubSpot, Pylon, Grafana); the sandbox never sees real secrets

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Knowledge

Key repos cloned into /knowledge/; skills (markdown) loaded on demand

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Credentials

Credential brokering; the sandbox boots with references + rotating session tokens only; the proxy holds real creds; egress injection for a few hosts

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Supporting component

Markdown playbooks lazy-loaded per task so the general agent stays small

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Supporting component

Scoped permissions per session limit the actions available to the agent

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Supporting component

The sandbox runs arbitrary code yet never touches a secret

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

One agent with good abstractions beats a fleet of narrow bots

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Lesson

Separate capabilities from the core loop; domain logic lives in skills + service packages

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Lesson

Don't trust the model, remove its ability to do wrong: scope tools and services per invocation source

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

Lesson

Meet people where they are; Slack is the highest-leverage surface because that's where work already happens

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for coding request → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source documents agent-authored pull requests while the enclosing workflow retains human review.

Observation date
:   2026

- Supports [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md) (first-party)

#### Sources

1. [How we build internal agents at Browserbase](https://browserbase.com/blog/internal-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/browserbase-bb-source-1/content.md)  <https://browserbase.com/blog/internal-agents> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#browserbase-bb)
