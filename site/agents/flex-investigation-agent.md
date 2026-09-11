Source: https://internal-agents.com/#flex-investigation-agent

Flex Task agent

# AI Investigation Agent

A Slack agent for HSA/FSA payment operations that traces a payment end-to-end and, when it finds a software bug, prepares a PR with a proposed fix.

Finance ops On-call Coding

payment investigation → proposed code fix: Work product review

Operating model, claims & sources

#### Scoped operating models

**payment investigation → proposed code fix** Work product review · Level 3

#### Summary and context

Summary

A Slack agent for HSA/FSA payment operations that traces a payment end-to-end and, when it finds a software bug, prepares a PR with a proposed fix.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Harness

Investigation-to-fix loop; underlying runtime not documented

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Interfaces

slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Tool access

Traces a payment end-to-end across payment systems; can open a PR with a proposed fix when a bug is found

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Supporting component

Payment trace → root-cause hypothesis → proposed code fix as a PR

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Start where correctness is observable; payment investigation produces artifacts (a trace, a hypothesis, a diff) that can be checked

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

Lesson

An ops agent that can prepare a fix (not just a report) closes the loop from investigation to code

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for payment investigation → proposed code fix; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes a trace, diagnosis, and proposed pull request returned for review.

Observation date
:   2026

- Supports [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md) (first-party)

#### Sources

1. [The Flex AI Investigation Agent for HSA/FSA payments](https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/flex-investigation-agent-source-1/content.md)  <https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#flex-investigation-agent)
