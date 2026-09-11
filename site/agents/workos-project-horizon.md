Source: https://internal-agents.com/#workos-project-horizon

WorkOS Platform

# Project Horizon

An internal autonomous 'code factory' where a continuously running swarm of agents handles the implementation loop while engineers focus on requirements and acceptance testing. Deliberately modular so the harness can evolve.

Coding Code review Security

requirements and acceptance criteria → tested implementation: Outcome review

Operating model, claims & sources

#### Scoped operating models

**requirements and acceptance criteria → tested implementation** Outcome review · Level 4

#### Summary and context

Summary

An internal autonomous 'code factory' where a continuously running swarm of agents handles the implementation loop while engineers focus on requirements and acceptance testing. Deliberately modular so the harness can evolve.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)
- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)
- Contextualizes [An autonomous UI-quality program](https://workos.com/blog/autonomous-ui-quality-program) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-3/content.md) (first-party)

#### Architecture and primitives

Sandbox

Cloudflare Containers + Sandbox SDK; disposable, tightly scoped sandboxes with explicit lifecycle APIs and egress controls; full monorepo stack in Docker dev containers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Harness

Modular by design; the core article runs OpenCode in the sandbox; the Applied AI Showcase runs Claude Remote Routines. The harness is swappable as agent tech changes; separate PM, implementation, and prospective verification/security roles

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)
- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

Model

Swappable; the harness is the constant, not the model

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)
- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

Interfaces

linear, github, slack, web

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Tool access

A custom MCP server stitches internal data sources (Datadog, Sentry, Slack, WorkOS Pipes); all outbound traffic proxied through Workers with allowlists, limits, logging, and token injection

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)
- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

Knowledge

AGENTS.md and CLAUDE.md capture scripts, docs, conventions; MCP codifies the patterns engineers already follow; Notion + Figma for specs/mockups

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Credentials

WorkOS Pipes (no OAuth/token-refresh to maintain); scoped short-lived GitHub tokens per user; engineers use their own identity in the MCP; least-privilege + egress controls

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Context management

The orchestrator pauses/resumes sandboxes and tracks state + artifacts across a run

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Supporting component

Separate what runs code from what manages the lifecycle

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Supporting component

A runtime controlled end-to-end, with lifecycle APIs and egress controls for the threat model

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Supporting component

Each run ships work and produces the next set of fixes, surfacing where the platform is brittle

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Supporting component

Tuning tools is ongoing, not a one-time integration

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

#### Lessons and interpretation

Lesson

You need purpose-built agent infrastructure; a runtime you control end-to-end with lifecycle APIs and egress controls

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Lesson

Separate concerns: sandboxes are an execution primitive; the orchestrator is the control plane

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Lesson

Build modularly so the harness can evolve; OpenCode today, Claude Remote Routines tomorrow, without rebuilding the platform

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)
- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

Lesson

Make autonomy a platform; the system gets faster and more reliable through use as fixes feed back in

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

Lesson

MCP tuning is an iterative product, not a one-time integration; codify the patterns engineers already follow

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 4 for requirements and acceptance criteria → tested implementation; human attention boundary: outcome-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes engineers focusing on requirements and acceptance testing while agents run the implementation loop.

Observation date
:   2026-05-06

- Supports [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md) (first-party)

#### Sources

1. [Project Horizon - an autonomous code factory at WorkOS](https://workos.com/blog/project-horizon) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-1/content.md)  <https://workos.com/blog/project-horizon> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Applied AI Showcase (Horizon with Claude Remote Routines)](https://workos.com/blog/applied-ai-showcase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-2/content.md)  <https://workos.com/blog/applied-ai-showcase> engineering-blog · first-party · Last source verification: 2026-08-31
3. [An autonomous UI-quality program](https://workos.com/blog/autonomous-ui-quality-program) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-3/content.md)  <https://workos.com/blog/autonomous-ui-quality-program> engineering-blog · first-party · Last source verification: 2026-08-31
4. [Hacker News submission for Project Horizon](https://news.ycombinator.com/item?id=48039227) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/workos-project-horizon-source-4/content.md)  <https://news.ycombinator.com/item?id=48039227> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#workos-project-horizon)
