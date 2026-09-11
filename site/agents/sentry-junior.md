Source: https://internal-agents.com/#sentry-junior

Sentry Task agent

# Junior

An open-source Slack agent built at Sentry that acts like an intern; takes tasks, retrieves context across many company systems, and is steered and reviewed by humans. Its CEO argues one general-purpose agent beat several vendor-specific bots.

Coding Code review Support On-call

assigned task → human-steered and reviewed output: Continuous steering

Operating model, claims & sources

#### Scoped operating models

**assigned task → human-steered and reviewed output** Continuous steering · Level 2

#### Summary and context

Summary

An open-source Slack agent built at Sentry that acts like an intern; takes tasks, retrieves context across many company systems, and is steered and reviewed by humans. Its CEO argues one general-purpose agent beat several vendor-specific bots.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)
- Supports [getsentry/junior source repository](https://github.com/getsentry/junior) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-2/content.md) (first-party)
- Contextualizes [Sentry Labs](https://labs.sentry.dev/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-3/content.md) (first-party)

#### Reported metrics

Headline claim

Open-source (Apache-2.0) Slack agent (~100k lines of TS) used internally at Sentry

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sentry

Scope
:   Junior codebase size and license in the author report

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party) Preserved content.md, lines 10–24, 34–60
- Supports [getsentry/junior Apache 2.0 license](https://github.com/getsentry/junior/blob/main/LICENSE?plain=1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-4/content.md) (first-party) Preserved content.md, lines 412–414

Key observation

Around 100,000 lines of TypeScript excluding tests, evals, docs, and lockfiles

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sentry

Scope
:   TypeScript lines in Junior excluding tests, evals, documentation, and lockfiles

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party) Preserved content.md, lines 22

Key observation

4 months from start to writeup

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Sentry

Scope
:   Author-reported development and iteration time before the writeup

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party) Preserved content.md, lines 10–22

#### Architecture and primitives

Sandbox

Vercel serverless functions; Vercel agent-browser sandbox with an on-path proxy for traffic interception; ephemeral containers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Harness

Custom harness on Pi's SDK; a task broker over Vercel Queues with an inbox -> worker-claim -> interrupt/resume pattern to survive serverless timeouts; 'skills-as-runbooks'

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Model

Claude Sonnet (faster); swappable (Opus as a more expensive option)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Interfaces

slack, web, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Tool access

Progressive discovery via MCP; by default Junior connects to no provider until the agent requests a tool lookup; plugins connect Sentry, GitHub, Linear, Notion

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Knowledge

Conversation transcripts persisted in Redis; repo search to trace code paths; skill docs (TELEMETRY.md, SOUL.md)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Credentials

On-path proxy injection; the model never sees the token because it is not in the sandbox; plugins declare OAuth flows and credential domains; GitHub distinguishes read vs. write

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Context management

Incremental transcript updates in Redis; resource subscriptions to GitHub PR events for follow-ups

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Supporting component

searchMcpTools loads tools on demand instead of dumping every schema into the prompt

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Supporting component

Credentials injected host-side; the sandbox/model never touches a secret

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Supporting component

Survives serverless timeouts via a queue + claim model

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

One general-purpose agent connected to many company systems beats several vendor-specific bots

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Lesson

Skills-as-runbooks encode operational knowledge the agent can follow

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Lesson

Stateless compute fights you; serverless functions time out and disappear; model the agent around interrupt/resume

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Lesson

Unit tests are the wrong yardstick for agents; invest in evals and integration tests instead

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

Lesson

Writes need per-user authorization, not blanket trust

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 2 for assigned task → human-steered and reviewed output; human attention boundary: continuous-steering.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source explicitly describes humans steering and reviewing the agent throughout its work.

Observation date
:   2026

- Supports [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md) (first-party)

#### Sources

1. [Building an Intern (Junior at Sentry)](https://cra.mr/building-an-intern/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-1/content.md)  <https://cra.mr/building-an-intern/> engineering-blog · first-party · Last source verification: 2026-08-31
2. [getsentry/junior source repository](https://github.com/getsentry/junior) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-2/content.md)  <https://github.com/getsentry/junior> repository · first-party · Last source verification: 2026-08-31
3. [Sentry Labs](https://labs.sentry.dev/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-3/content.md)  <https://labs.sentry.dev/> documentation · first-party · Last source verification: 2026-08-31
4. [getsentry/junior Apache 2.0 license](https://github.com/getsentry/junior/blob/main/LICENSE?plain=1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/sentry-junior-source-4/content.md)  <https://github.com/getsentry/junior/blob/main/LICENSE?plain=1> source-code · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#sentry-junior)
