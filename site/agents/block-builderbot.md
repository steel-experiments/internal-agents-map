Source: https://internal-agents.com/#block-builderbot

Block Orchestration system

# Builderbot

A multi-agent orchestration layer built on goose + MCP that coordinates agents across Block's entire codebase, invoked in Slack to take a ticket end-to-end to a reviewed PR.

Coding Code review

ticket → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**ticket → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

A multi-agent orchestration layer built on goose + MCP that coordinates agents across Block's entire codebase, invoked in Slack to take a ticket end-to-end to a reviewed PR.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)
- Supports [Protecting our systems with intelligence (Builderbot architecture)](https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-2/content.md) (first-party)
- Contextualizes [block/builderbot source repository](https://github.com/block/builderbot) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-3/content.md) (first-party)
- Contextualizes [Hacker News discussion of the Builderbot announcement](https://news.ycombinator.com/item?id=48618973) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-4/content.md) (community)

#### Reported metrics

Headline claim

~1,500 PRs merged per week (~15% of all production code changes at Block)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Block

Scope
:   Builderbot merged pull requests per week at Block

Denominator
:   All production code changes across Block for the approximately 15% share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party) Preserved content.md, lines 24

Key observation

200,000+ operations per day

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Block

Scope
:   Builderbot operations per day; the article does not define an operation

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party) Preserved content.md, lines 24

Key observation

~1,500 pull requests merged per week (~15% of all production code changes at Block)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Block

Scope
:   Builderbot merged pull requests per week at Block

Denominator
:   All production code changes across Block for the approximately 15% share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party) Preserved content.md, lines 24

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Harness

Multi-agent orchestration built on goose (open-source agent framework) + MCP; multi-player, real-time, operating inside Slack threads

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Model

goose framework; model not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Interfaces

slack, linear, jira, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Tool access

MCP connects agents to internal tools and data; picks up Linear/Jira tickets, creates the branch, writes code, opens the PR, watches CI

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Knowledge

Company-wide code context across hundreds of millions of lines and hundreds of services; Block also frames Builderbot as an 'agentic protector' around its software world model

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)
- Supports [Protecting our systems with intelligence (Builderbot architecture)](https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-2/content.md) (first-party)

Supporting component

Coordinates multiple agents over one codebase instead of running a single loop

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Supporting component

Linear/Jira ticket -> branch -> code -> PR -> CI watch, end to end

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

#### Other reported details and interpretation

Key observation

"What used to take months now takes days"

Opinion · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   Qualitative company statement, not a measured before-and-after study.

Scope
:   Reported turnaround for Square seller features and repetitive engineering work

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party) Preserved content.md, lines 24–26

#### Lessons and interpretation

Lesson

Concentrate investment on orchestration, context, and the environment; let engineers focus on the problems worth solving

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Lesson

Meet people in Slack: tag @builderbot with a short description and it works in the thread

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

Lesson

Multi-player real-time collaboration lets humans steer research, planning, and implementation rather than only reviewing after the fact

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for ticket → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source explicitly describes end-to-end implementation ending in a reviewed pull request.

Observation date
:   2026-06-21

- Supports [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md) (first-party)

#### Sources

1. [Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-1/content.md)  <https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Protecting our systems with intelligence (Builderbot architecture)](https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-2/content.md)  <https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence> engineering-blog · first-party · Last source verification: 2026-08-31
3. [block/builderbot source repository](https://github.com/block/builderbot) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-3/content.md)  <https://github.com/block/builderbot> repository · first-party · Last source verification: 2026-08-31
4. [Hacker News discussion of the Builderbot announcement](https://news.ycombinator.com/item?id=48618973) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-4/content.md)  <https://news.ycombinator.com/item?id=48618973> hn-thread · community · Last source verification: 2026-08-31
5. [Hacker News comment that points to the Builderbot repository](https://news.ycombinator.com/item?id=48619052) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/block-builderbot-source-5/content.md)  <https://news.ycombinator.com/item?id=48619052> hn-comment · community · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#block-builderbot)
