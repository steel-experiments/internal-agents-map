Source: https://internal-agents.com/#hubspot-sidekick

HubSpot Task agent

# Sidekick

HubSpot's internal AI code-review agent. Sidekick reviews every pull request and uses a multi-model Judge Agent to filter comments before posting. Its review implementation moved from Claude Code on Crucible Kubernetes workloads to Aviator, HubSpot's internal Java agent framework; the later report does not specify Aviator's execution isolation.

Code review

pull request → AI review comments: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → AI review comments** Work product review · Level 3

#### Summary and context

Summary

HubSpot's internal AI code-review agent. Sidekick reviews every pull request and uses a multi-model Judge Agent to filter comments before posting. Its review implementation moved from Claude Code on Crucible Kubernetes workloads to Aviator, HubSpot's internal Java agent framework; the later report does not specify Aviator's execution isolation.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 14, 24–45, 75–87
- Contextualizes [Cloud coding agents at HubSpot](https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-2/content.md) (first-party) Preserved content.md, lines 30–57 (earlier Crucible implementation)

#### Reported metrics

Headline claim

Reviews every pull request and cut engineer feedback time by 90%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   HubSpot reported the figures in its own engineering blog without independent verification.

Reported by
:   HubSpot

Scope
:   Time for engineers to receive code feedback from Sidekick; not overall PR completion time

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-03

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 14–18

Key observation

Reviews every pull request

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   HubSpot reported the figures in its own engineering blog.

Reported by
:   HubSpot

Scope
:   Pull-request coverage after the six-month rollout

Denominator
:   HubSpot pull requests

Method
:   Unknown

Observation date
:   Unknown

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 14

Key observation

Engineer feedback time cut by 90%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   HubSpot reported the figures in its own engineering blog.

Reported by
:   HubSpot

Scope
:   Time for engineers to receive code feedback from Sidekick; not overall PR completion time

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 14–18

Key observation

Over 80% thumbs-up reaction rate on review feedback during the preceding couple of months

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   HubSpot reported the figures in its own engineering blog.

Reported by
:   HubSpot

Scope
:   Developer emoji reactions on review comments during the preceding couple of months

Denominator
:   Thumbs-up and thumbs-down reactions; not all developers or all reviews

Method
:   Emoji reactions and replies on review comments

Observation date
:   Unknown

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 99–116

#### Architecture and primitives

Harness

Aviator, an internal Java agent framework; replaced the earlier Claude Code review implementation on Crucible

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 24–45

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   Current review runs on Aviator; its execution isolation is not specified. Crucible Kubernetes workloads describe the predecessor implementation.

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party) Preserved content.md, lines 39–45

Tool access

Aviator framework for precise tool control

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party)

Interfaces

github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for pull request → AI review comments; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The engineering blog describes engineers acting on Sidekick review comments, which locates human attention at work-product review.

Observation date
:   2026-03

- Supports [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md) (first-party)

#### Sources

1. [Automated code review, the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-1/content.md)  <https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Cloud coding agents at HubSpot](https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/hubspot-sidekick-source-2/content.md)  <https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#hubspot-sidekick)
