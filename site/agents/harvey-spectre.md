Source: https://internal-agents.com/#harvey-spectre

Harvey Platform

# Spectre

Harvey's internal collaborative cloud agent platform; reacts to incidents, bug reports, and Slack messages and produces reviewable diffs, branches, and PRs.

Coding Code review On-call Security

incident or request → reviewable diff or pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**incident or request → reviewable diff or pull request** Work product review · Level 3

#### Summary and context

Summary

Harvey's internal collaborative cloud agent platform; reacts to incidents, bug reports, and Slack messages and produces reviewable diffs, branches, and PRs.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

#### Architecture and primitives

Sandbox

Isolated ephemeral execution environments; durable runs

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Harness

Collaborative cloud agent platform with explicit boundaries around GitHub, Datadog, Linear, and other connected systems

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Interfaces

slack, web, automation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Tool access

Explicit tool boundaries; reacts to incidents, bug reports, customer feedback, and Slack messages

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Credentials

Explicit tool boundaries; outputs are reviewable

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Context management

Durable runs over disposable execution environments

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Supporting component

Long-lived run state over throwaway compute

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Supporting component

Outputs are summaries, diffs, branches, PRs; not silent actions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Make outputs reviewable (diffs, branches, PRs) rather than letting the agent act silently

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Lesson

Implementation speed shifts the bottleneck toward review, prioritization, and coordination

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

Lesson

Harvey keeps its product-agent and security-agent platforms on separate substrates because they have different trust boundaries

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an agentic security operations center](https://www.harvey.ai/blog/building-an-agentic-security-operations-center) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for incident or request → reviewable diff or pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source explicitly frames diffs, branches, and pull requests as reviewable outputs.

Observation date
:   2026

- Supports [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md) (first-party)

#### Sources

1. [Building Spectre; internal collaborative cloud agent platform](https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-1/content.md)  <https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Building an agentic security operations center](https://www.harvey.ai/blog/building-an-agentic-security-operations-center) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/harvey-spectre-source-2/content.md)  <https://www.harvey.ai/blog/building-an-agentic-security-operations-center> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#harvey-spectre)
