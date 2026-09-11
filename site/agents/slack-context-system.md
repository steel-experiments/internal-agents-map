Source: https://internal-agents.com/#slack-context-system

Slack Supporting pattern

# Multi-agent context system

A coordinator/dispatcher multi-agent design with structured context channels for long-running investigations spanning hundreds of steps.

Research

long-running investigation → synthesized report: Unknown

Operating model, claims & sources

#### Scoped operating models

**long-running investigation → synthesized report** Unknown · Level unknown

#### Summary and context

Summary

A coordinator/dispatcher multi-agent design with structured context channels for long-running investigations spanning hundreds of steps.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

#### Reported metrics

Headline claim

Context management for security investigations spanning hundreds of inference requests and megabytes of output

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Slack

Scope
:   Complex security investigations requiring tailored multi-agent context; qualitative workload scale

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party) Preserved content.md, lines 34–38
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary) Preserved content.md, lines 22

Key observation

Handles multi-agent runs spanning hundreds of requests and megabytes of output

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Slack

Scope
:   Complex security investigations requiring tailored multi-agent context; qualitative workload scale

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party) Preserved content.md, lines 34–38
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary) Preserved content.md, lines 22

#### Architecture and primitives

Harness

Coordinator/dispatcher: a central coordinator dispatches to expert agents and to critic agents

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Tool access

Expert agents produce reports; critic agents evaluate them using evidence-inspection tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Context management

Three channels; Director's Journal (working memory), Critic's Review (credibility-weighted findings), Critic's Timeline (deduped chronological synthesis)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Supporting component

Structured working memory: findings, decisions, questions, hypotheses

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Supporting component

A truth filter with credibility scores over submitted findings

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Supporting component

A chronological, deduped, conflict-resolved synthesis retained across steps

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

#### Lessons and interpretation

Lesson

Don't pass all information at every step; build structured summaries agents can reliably build on

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Lesson

Separate expert agents (produce) from critic agents (evaluate); corroborated findings are prioritized

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

Lesson

Context management becomes its own subsystem once runs get long

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)
- Supports [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Unclassified for long-running investigation → synthesized report; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The research pattern documents agent coordination and criticism but not the normal human attention boundary.

Observation date
:   2026

- Supports [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md) (first-party)

#### Sources

1. [Managing context in long-running agentic applications](https://slack.engineering/managing-context-in-long-run-agentic-applications/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-1/content.md)  <https://slack.engineering/managing-context-in-long-run-agentic-applications/> engineering-blog · first-party · Last source verification: 2026-08-31
2. [How Slack manages context in long-running multi-agent systems](https://www.infoq.com/news/2026/04/slack-agent-context-management/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/slack-context-system-source-2/content.md)  <https://www.infoq.com/news/2026/04/slack-agent-context-management/> news · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#slack-context-system)
