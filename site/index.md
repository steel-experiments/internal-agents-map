Source: https://internal-agents.com/

Agents at work

# Internal Agents Map

AI systems organizations build or adapt to do work for their own teams.

Explore how teams connect models to their knowledge, tools, and workflows—and where people stay involved. The map includes agents, platforms, orchestration systems, and supporting patterns.

**39** approaches

**35** organizations

**88** sources

Latest entry review: 2026-09-09. Individual source dates vary.

## Explore the catalog

Approaches, not rankings

39 approaches

Airbnb Platform

### Airchat (airchat-cli)

Airbnb's internal agentic-coding harness, built by its Dev AI team. Airchat is a wrapper over Claude Code with a unified gateway for cost and metrics, an internal plugin marketplace, AirDev Workspaces for parallel sessions, and more than a dozen internal MCP servers that connect agents to internal systems. The team abandoned an earlier from-scratch orchestrator and shipped a thin shim over Airchat instead.

Coding Code review

coding task → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**coding task → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

Airbnb's internal agentic-coding harness, built by its Dev AI team. Airchat is a wrapper over Claude Code with a unified gateway for cost and metrics, an internal plugin marketplace, AirDev Workspaces for parallel sessions, and more than a dozen internal MCP servers that connect agents to internal systems. The team abandoned an earlier from-scratch orchestrator and shipped a thin shim over Airchat instead.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   The build is described by Airbnb engineers in talks and podcasts, not in a first-party engineering blog.

- Contextualizes [Agentic coding at Airbnb (DPE.org)](https://dpe.org/sessions/szczepan-faber-mike-nakhimovich/agentic-coding-at-airbnb/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-1/content.md) (direct-participant)
- Supports [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md) (direct-participant)

#### Reported metrics

Headline claim

About 64% of pull requests materialized through agentic coding

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The 64% figure comes from a third-party newsletter that quotes the engineers, not from a first-party Airbnb source.

Reported by
:   Airbnb

Scope
:   Airbnb PRs materialized through agentic coding by the October 2025 talk

Denominator
:   Airbnb pull requests; exact count not supplied

Method
:   Unknown

Observation date
:   2025-10

- Supports [How to get your team past the AI (The AI Thinker)](https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-3/content.md) (independent-secondary) Preserved content.md, lines 16, 24, 194

Key observation

About 64% of pull requests materialized through agentic coding

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The figure comes from a third-party newsletter, not a first-party Airbnb source.

Reported by
:   Airbnb

Scope
:   Airbnb PRs materialized through agentic coding by the October 2025 talk

Denominator
:   Airbnb pull requests; exact count not supplied

Method
:   Unknown

Observation date
:   2025-10

- Supports [How to get your team past the AI (The AI Thinker)](https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-3/content.md) (independent-secondary) Preserved content.md, lines 16, 24, 194

#### Architecture and primitives

Harness

Wrapper over Claude Code with a unified gateway, an internal plugin marketplace, and AirDev parallel workspaces

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md) (direct-participant)

Model

Claude Code (a vendor agent), wrapped by Airbnb

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md) (direct-participant)

Tool access

More than a dozen internal MCP servers connect agents to internal systems

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md) (direct-participant)

#### Operating model evidence

Operating model assessment

Level 3 for coding task → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   Airbnb engineers describe agents producing pull requests that engineers review, which locates human attention at work-product review.

Observation date
:   2025

- Supports [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md) (direct-participant)

#### Sources

1. [Agentic coding at Airbnb (DPE.org)](https://dpe.org/sessions/szczepan-faber-mike-nakhimovich/agentic-coding-at-airbnb/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-1/content.md)  <https://dpe.org/sessions/szczepan-faber-mike-nakhimovich/agentic-coding-at-airbnb/> talk · direct-participant · Last source verification: 2026-08-31
2. [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-2/content.md)  <https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/> podcast · direct-participant · Last source verification: 2026-08-31
3. [How to get your team past the AI (The AI Thinker)](https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/airbnb-airchat-source-3/content.md)  <https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai> news · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#airbnb-airchat)

Atlassian Task agent

### Rovo Dev (RovoDev)

Atlassian's internal coding agent, built on the HULA (Human-in-the-loop software development agents) framework. Rovo Dev works inside Jira and runs a four-step cycle (set context, generate a plan, generate code, and raise a pull request). Atlassian dogfooded it across all Jira sites for more than a year across 1,900+ repositories. It reached general availability in October 2025.

Coding Code review

Jira issue → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**Jira issue → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

Atlassian's internal coding agent, built on the HULA (Human-in-the-loop software development agents) framework. Rovo Dev works inside Jira and runs a four-step cycle (set context, generate a plan, generate code, and raise a pull request). Atlassian dogfooded it across all Jira sites for more than a year across 1,900+ repositories. It reached general availability in October 2025.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-1/content.md) (first-party)
- Supports [HULA: Human-in-the-loop software development agents (arXiv 2411.12924)](https://arxiv.org/abs/2411.12924) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-3/content.md) (first-party)

#### Reported metrics

Headline claim

Dogfooded across 1,900+ repositories with a 50,000+ comment internal dataset

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Atlassian reported the dogfooding scale in its own engineering blog without independent verification.

Reported by
:   Atlassian

Scope
:   Internal code-review dogfooding repositories and Rovo Dev-generated classifier training comments

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026

- Supports [Developer productivity improved with Rovo Dev](https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-2/content.md) (first-party) Preserved content.md, lines 66, 87

Key observation

Dogfooded across 1,900+ repositories over more than a year

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Atlassian reported the dogfooding scale in its own engineering blog.

Reported by
:   Atlassian

Scope
:   Internal code-review evaluation across 1,900+ repositories spanning over a year

Denominator
:   Unknown

Method
:   Year-long online evaluation across internal repositories

Observation date
:   Unknown

- Supports [Developer productivity improved with Rovo Dev](https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-2/content.md) (first-party) Preserved content.md, lines 87

Key observation

Trained on a proprietary internal dogfooding dataset of 50,000+ Rovo Dev comments

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Atlassian reported the dataset size in its own engineering blog.

Reported by
:   Atlassian

Scope
:   ModernBERT classifier training dataset of internally sourced Rovo Dev-generated comments

Denominator
:   Unknown

Method
:   Internal dogfooding comments labeled by whether they led to a code resolution

Observation date
:   Unknown

- Supports [Developer productivity improved with Rovo Dev](https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-2/content.md) (first-party) Preserved content.md, lines 66

#### Architecture and primitives

Harness

Built on the HULA framework, which runs set context, generate plan, generate code, and raise PR

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-1/content.md) (first-party)

Interfaces

jira

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for Jira issue → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The HULA framework and engineering blog describe a human-in-the-loop cycle that ends in a reviewed pull request.

Observation date
:   2024-11

- Supports [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-1/content.md) (first-party)

#### Sources

1. [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-1/content.md)  <https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Developer productivity improved with Rovo Dev](https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-2/content.md)  <https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev> engineering-blog · first-party · Last source verification: 2026-08-31
3. [HULA: Human-in-the-loop software development agents (arXiv 2411.12924)](https://arxiv.org/abs/2411.12924) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/atlassian-rovo-dev-source-3/content.md)  <https://arxiv.org/abs/2411.12924> paper · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#atlassian-rovo-dev)

Block Orchestration system

### Builderbot

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

Brex Platform

### Internal Agent Platform

Retool-based internal platform where employees build, test, and deploy agents for KYC, disputes, QA, collections, and operations.

Finance ops Support Customer success

internal operations request → completed operation: Continuous steering

Operating model, claims & sources

#### Scoped operating models

**internal operations request → completed operation** Continuous steering · Level 2

#### Summary and context

Summary

Retool-based internal platform where employees build, test, and deploy agents for KYC, disputes, QA, collections, and operations.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Reported metrics

Headline claim

Dispute processing time fell from three hours to three seconds

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Dispute-submission preparation using the internal agent platform; not end-to-end chargeback resolution

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 179–189

Key observation

50%+ of customer-support cases resolved by chatbot as first touch

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Customer-support cases resolved by the chatbot at first touch

Denominator
:   Customer-support cases; exact sample size not provided

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 76

Key observation

Dispute processing: 3 hours → 3 seconds

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Dispute-submission preparation using the internal agent platform; not end-to-end chargeback resolution

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 179–189

Key observation

QA covers every support interaction; one person using AI instead of five QA specialists

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   Quality assurance of customer-support interactions

Denominator
:   Every support interaction

Method
:   Agent applies the quality rubric to every response; one person oversees instead of five QA specialists

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 80

Key observation

KYC adverse-media accuracy 85% → 88%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Brex

Scope
:   KYC adverse-media classification; human versus agent accuracy

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary) Preserved content.md, lines 163–167

#### Architecture and primitives

Sandbox

Retool-hosted runtime (no bespoke execution env described)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Harness

Retool-based builder with prompt management and multi-model testing/evaluation; built by a ~25-person systems-engineering team

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Model

Multi-model

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Interfaces

slack, internal-ui

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Tool access

An MCP server exposes external product features to the internal platform; new product tools become internally available immediately; invoked via Slack /c1

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Knowledge

Standard operating procedures uploaded as a knowledge base, such as 100-page dispute guides; customer account data

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Credentials

SSO via internal Retool proxies (no per-user accounts); ConductorOne access management; Okta auth; data classified by risk; ≤30-day retention, no training on inputs

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Supporting component

Non-technical ops staff design prompts, test across models, deploy with QA oversight

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Supporting component

Product features exposed to internal agents through one MCP server

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Lessons and interpretation

Lesson

Target 40% automation, not 100%; the last mile drives investments that often yield zero value

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Brex reports that it manages the internal platform with practices used for an external product

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Don't skip the human in the middle; end-to-end automation fails on accuracy

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Map workflows to the discrete steps a human would take, then translate each to LLM instructions

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

Lesson

Architecture beats vendor; legal/data approvals should follow data-handling characteristics, not the tool name

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Level 2 for internal operations request → completed operation; human attention boundary: continuous-steering.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The secondary report describes a human remaining in the middle of the workflow, but does not fully specify each review surface.

Observation date
:   2025-09-25

- Supports [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md) (independent-secondary)

#### Sources

1. [Agent, Human, Ops: How Brex Is Changing Roles and Workflows](https://www.firstround.com/ai/brex) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/brex-agent-platform-source-1/content.md)  <https://www.firstround.com/ai/brex> case-study · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#brex-agent-platform)

Browserbase Task agent

### bb

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

Cloudflare Platform

### Internal AI engineering stack

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

Coinbase Agent system

### Forge / Mux

Forge turns a Slack/GitHub/Linear discussion into a Linear issue, fix, PR, and one-off build; Mux lets employees run many coding agents concurrently.

Coding Code review

Slack, GitHub, or Linear request → reviewed pull request and build: Work product review

Operating model, claims & sources

#### Scoped operating models

**Slack, GitHub, or Linear request → reviewed pull request and build** Work product review · Level 3

#### Summary and context

Summary

Forge turns a Slack/GitHub/Linear discussion into a Linear issue, fix, PR, and one-off build; Mux lets employees run many coding agents concurrently.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)
- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

#### Reported metrics

Headline claim

Mux: 600+ users including engineers, PMs, and designers (335 active, 197 power users)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Coinbase

Scope
:   Registered Mux users including engineers, PMs, and designers; 335 active and 197 power users

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party) Preserved content.md, lines 24–34

Key observation

Mux: 600+ users including engineers, PMs, and designers (335 active, 197 power users)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Coinbase

Scope
:   Registered Mux users including engineers, PMs, and designers; 335 active and 197 power users

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party) Preserved content.md, lines 24–34

#### Architecture and primitives

Sandbox

Mux gives each concurrent agent its own git worktree, branch, and terminal

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

Harness

Portfolio approach; Claude Code, OpenCode, Cursor, and Copilot rather than one harness; Forge is a custom harness invokable from Slack, GitHub, and Linear

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)
- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

Model

Portfolio across multiple providers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

Interfaces

slack, github, linear

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

Tool access

Linear treated as the structured product context / source of truth

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

Knowledge

Linear as the durable structured-context layer for product work

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

Supporting component

Custom harness: Slack bug discussion → Linear issue → fix → PR → one-off build

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

Supporting component

Concurrency layer; one human coordinates many isolated coding agents, each in its own worktree/branch/terminal

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Support a portfolio of harnesses (Claude Code, OpenCode, Cursor, Copilot) rather than standardizing on one

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

Lesson

Keep the system of record (Linear) as the agent's structured context; conversation can be the input, Linear stays durable

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md) (first-party)

Lesson

Simple per-agent worktree/branch/terminal isolation is a pragmatic alternative to full sandboxing for concurrent coding

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for Slack, GitHub, or Linear request → reviewed pull request and build; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes delegated implementation that returns a pull request and build for human review.

Observation date
:   2026

- Supports [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md) (first-party)

#### Sources

1. [Coding had a concurrency problem: how Mux helped solve it](https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-1/content.md)  <https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Coinbase × Linear (Forge workflow)](https://linear.app/customers/coinbase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/coinbase-forge-mux-source-2/content.md)  <https://linear.app/customers/coinbase> case-study · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#coinbase-forge-mux)

Databricks Agent system

### coSTAR and internal engineering agents

Databricks' internal engineering agents and the coSTAR framework that ships and tests them. Databricks uses internal agents as daily coding drivers on its own codebase, including code-review and on-call support work. coSTAR tests agents on a private benchmark built from Databricks' multi-million line codebase before they ship. Omnigent is a separate shipping open-source product and is excluded from this record.

Coding Code review On-call

internal engineering workflows → agent-produced changes: Unknown

Operating model, claims & sources

#### Scoped operating models

**internal engineering workflows → agent-produced changes** Unknown · Level unknown

#### Summary and context

Summary

Databricks' internal engineering agents and the coSTAR framework that ships and tests them. Databricks uses internal agents as daily coding drivers on its own codebase, including code-review and on-call support work. coSTAR tests agents on a private benchmark built from Databricks' multi-million line codebase before they ship. Omnigent is a separate shipping open-source product and is excluded from this record.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-1/content.md) (first-party)
- Supports [Benchmarking coding agents on a multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-2/content.md) (first-party)

#### Architecture and primitives

Harness

coSTAR framework for shipping and testing internal agents

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-1/content.md) (first-party)

Knowledge

Private benchmark built from the Databricks multi-million line codebase

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Benchmarking coding agents on a multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-2/content.md) (first-party)

#### Other reported details and interpretation

Key observation

Internal agents serve as daily coding drivers on the Databricks codebase

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Databricks described internal use in its own engineering blog.

- Supports [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-1/content.md) (first-party)

Key observation

Private benchmark built from a multi-million line codebase

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Databricks described the benchmark in its own engineering blog.

- Supports [Benchmarking coding agents on a multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for internal engineering workflows → agent-produced changes; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The record covers several internal engineering agents with different workflows, so no single human-attention boundary applies.

Observation date
:   2025

- Supports [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-1/content.md) (first-party)

#### Sources

1. [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-1/content.md)  <https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Benchmarking coding agents on a multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/databricks-costar-source-2/content.md)  <https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#databricks-costar)

Domu Task agent

### Clementino

A general-purpose 'AI colleague' spanning sales, finance, client ops, engineering, and recruitment, later split into a reusable toolkit plus Slack and desktop surfaces.

Support Finance ops Coding Recruitment Customer success

employee request → approved customer-impacting action: Work product review

Operating model, claims & sources

#### Scoped operating models

**employee request → approved customer-impacting action** Work product review · Level 3

#### Summary and context

Summary

A general-purpose 'AI colleague' spanning sales, finance, client ops, engineering, and recruitment, later split into a reusable toolkit plus Slack and desktop surfaces.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

~35 integrations organized into skills

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Domu

Scope
:   Clementino toolkit integration modules organized into skills

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party) Preserved content.md, lines 58–60

Key observation

~35 integrations organized into skills

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Domu

Scope
:   Clementino toolkit integration modules organized into skills

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party) Preserved content.md, lines 58–60

#### Architecture and primitives

Harness

Claude/Anthropic SDK wrapper; a reusable tool/skill/memory layer separated from the Slack and desktop interfaces

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Model

Claude (Anthropic SDK)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Interfaces

slack, desktop

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Tool access

~35 integrations organized into skills; specialist delegates per domain

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Knowledge

Four memory layers: conversation context, persistent facts, knowledge RAG, and live system state

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Credentials

Customer-impacting actions gated behind team-visible Slack approvals

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Context management

Four-layer memory separation; prompt size dropped substantially after splitting capabilities from the Slack layer

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Supporting component

Transient conversation, persistent facts, knowledge RAG, and live system state; kept separate

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Supporting component

Capabilities separated from the interface layer so they power multiple surfaces

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Separate reusable capabilities (tools/skills/memory) from the interface layer; prompt size drops while capability is preserved

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Lesson

Model memory explicitly: conversation context, persistent facts, RAG, and live state have different lifecycles

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

Lesson

Gate customer-impacting actions behind human approvals rather than trusting the model

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for employee request → approved customer-impacting action; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source documents explicit human approval for customer-impacting actions.

Observation date
:   2026

- Supports [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md) (first-party)

#### Sources

1. [Why we split our internal agent in two](https://domu.ai/blog/why-we-split-our-internal-agent-in-two) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/domu-clementino-source-1/content.md)  <https://domu.ai/blog/why-we-split-our-internal-agent-in-two> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#domu-clementino)

DoorDash Background agent

### AI Code Review Agent

A specialized agent that automatically reviews 10,000+ PRs a week across 56 repositories, emphasizing grounded high-confidence findings over noisy comments.

Code review

pull request → AI review comments: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → AI review comments** Work product review · Level 3

#### Summary and context

Summary

A specialized agent that automatically reviews 10,000+ PRs a week across 56 repositories, emphasizing grounded high-confidence findings over noisy comments.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

10,000+ pull requests reviewed per week across 56 repositories

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   DoorDash

Scope
:   Typical weekly PR reviews across 56 onboarded repositories

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party) Preserved content.md, lines 23

Key observation

10,000+ PRs reviewed in a typical week across 56 repositories

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   DoorDash

Scope
:   Typical weekly PR reviews across 56 onboarded repositories

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party) Preserved content.md, lines 23

Key observation

60.2% action rate on settled high/critical findings (measured sample)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   DoorDash

Scope
:   Settled high and critical findings that led to code changes before merge

Denominator
:   2,256 settled high and critical findings

Method
:   Whether the human changed the code before merge in response to the finding

Observation date
:   Unknown

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party) Preserved content.md, lines 27

#### Architecture and primitives

Harness

Three architecture versions; emphasis on attention and grounded, high-confidence findings rather than commenting everywhere

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Interfaces

github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Tool access

Reviews Go, iOS, Android, web, infrastructure, and data code

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Knowledge

Grounded findings tied to evidence

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Supporting component

High-confidence, evidence-backed comments rather than blanket commentary

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Optimize for attention; minimize noisy comments; comment only with grounded, high-confidence findings

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

Lesson

Measure whether engineers actually act on findings (action rate), not comment volume

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for pull request → AI review comments; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes automated findings that engineers evaluate within the pull-request workflow.

Observation date
:   2026

- Supports [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md) (first-party)

#### Sources

1. [How DoorDash built an AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-code-review-source-1/content.md)  <https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#doordash-code-review)

DoorDash Platform

### Flux / Agentic AI Platform

DoorDash's internal agentic AI platform; a unified cognitive layer over company data and operations, with an AI Marketplace of specialized agents and the Flux cloud-agent runtime for engineering tasks.

Code review Coding CI triage On-call Maintenance Data

engineering task → reviewed agent output: Work product review

Operating model, claims & sources

#### Scoped operating models

**engineering task → reviewed agent output** Work product review · Level 3

#### Summary and context

Summary

DoorDash's internal agentic AI platform; a unified cognitive layer over company data and operations, with an AI Marketplace of specialized agents and the Flux cloud-agent runtime for engineering tasks.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant)
- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

#### Reported metrics

Headline claim

130,000 engineering tasks automated in one month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report of a one-month count; this is the observation date, not the measurement window.

Reported by
:   DoorDash

Scope
:   Engineering tasks automated in one reported month; calendar measurement month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

130,000 engineering tasks automated in one month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report of a one-month count; this is the observation date, not the measurement window.

Reported by
:   DoorDash

Scope
:   Engineering tasks automated in one reported month; calendar measurement month unspecified

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

25,000+ automated code reviews per week

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Dated August 11, 2026 report; weekly measurement boundaries are not supplied.

Reported by
:   DoorDash

Scope
:   Weekly automated code reviews powered by Flux

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-08-11

- Supports [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md) (direct-participant) Preserved content.md, lines 10–12

Key observation

300+ playbooks; 10,000+ invocations per week

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   DoorDash

Scope
:   Unique playbooks and weekly invocations on Flux

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party) Preserved content.md, lines 10

#### Architecture and primitives

Sandbox

Firecracker microVMs; <5s p95 end-to-end setup (boot, clone repos, install tools, configure harness)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Harness

Maturity model: deterministic workflows -> ReAct agents -> hierarchical deep agents -> experimental swarms

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Model

Model-agnostic platform primitives support third-party or in-house agent components

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Interfaces

slack, github, scheduled, cli, skill, cursor

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Tool access

In-house MCP gateway ('Agent Gateway'); LangGraph orchestration; prospective A2A; tools declared per playbook with scoped, logged permissions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Knowledge

AI Marketplace of specialized agents; DataExplorer for grounded analytics; DoorDash-specific context in playbooks

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)
- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Credentials

Scoped per playbook; brokered through the gateway, never on the laptop; provenance on every action

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Context management

Hybrid retrieval: BM25 + dense semantic + reciprocal-rank fusion -> RAG; schema-aware SQL with EXPLAIN validation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Supporting component

Isolated Firecracker microVM with repos, tools, secrets, runtime deps

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

Governed, audited access to CI, observability, issue trackers, deploy, code search

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

YAML unit of agentic work: task, inputs, skills, tools, permissions, validation, outputs

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Supporting component

Identifies schemas, generates grounded SQL, validates via EXPLAIN before execution

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Supporting component

Workflows -> agents -> deep-agent hierarchies -> swarms; governance hardens as control decentralizes

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

#### Lessons and interpretation

Lesson

Start narrow to earn trust; began with automated code review before CI triage, on-call, maintenance, ticket-driven dev

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Make the work visible; public Slack threads drove adoption; private per-run channels did not build team habits

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Playbooks need enablement; workshops and hackathons turn repeated operational work into reusable playbooks

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

Lesson

Earn complexity by exhausting simpler primitives first; keep swarms at the research frontier until governance catches up

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Lesson

Deterministic verification before probabilistic judgment; SQL linting and EXPLAIN before deeper validation; LLM-as-judge + DeepEval

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

Lesson

Log provenance so any answer traces back to source queries, documents, and inter-agent activity

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for engineering task → reviewed agent output; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The platform spans several workflows; the cited engineering examples retain human review of agent output.

Observation date
:   2025-11-11

- Supports [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md) (first-party)

#### Sources

1. [Delegating Engineering Work To Cloud-Based Agents (Flux)](https://x.com/AIatDoorDash/status/2087285008906240193) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-1/content.md)  <https://x.com/AIatDoorDash/status/2087285008906240193> social-post · direct-participant · Last source verification: 2026-08-31
2. [Beyond single agents: DoorDash's collaborative AI ecosystem](https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-2/content.md)  <https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Delegating Engineering Work To Cloud-Based Agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/doordash-flux-source-3/content.md)  <https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#doordash-flux)

Dropbox Platform

### Nova

An internal platform for coding agents: engineers launch parallel sessions and internal systems invoke agents inside automated SDLC workflows.

Coding CI triage On-call Maintenance

agent-assisted SDLC workflow → accepted change: Unknown

Operating model, claims & sources

#### Scoped operating models

**agent-assisted SDLC workflow → accepted change** Unknown · Level unknown

#### Summary and context

Summary

An internal platform for coding agents: engineers launch parallel sessions and internal systems invoke agents inside automated SDLC workflows.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Dozens of agents can run in parallel from one runbook

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Migration-owner orchestration of dozens of agents from a shared runbook; qualitative capacity description

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

Key observation

Flaky-test remediation (Deflaker): 100+ validation runs

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   CI validation runs per proposed Deflaker flaky-test fix

Denominator
:   Unknown

Method
:   Run the test 100 or more times depending on its failure rate; retry capped at five fix attempts

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 58–62

Key observation

Predecessor Goose-based migrator used across thousands of migration entries before workflows moved onto Nova

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Predecessor Goose-based migrator, before workflows moved onto Nova

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

Key observation

Dozens of agents launchable from one runbook

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Dropbox

Scope
:   Migration-owner orchestration of dozens of agents from a shared runbook; qualitative capacity description

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party) Preserved content.md, lines 65–69

#### Architecture and primitives

Sandbox

Isolated env with a codebase snapshot at a specific commit; full Dropbox monorepo via Bazel; hermetic remote execution + caching

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Harness

Validation loop (propose → validate → feed back) with continue\_on\_validation\_failure and max\_iterations (~5); branch management kept outside the agent

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Model

Platform-agnostic; multiple coding agents behind one interface; swap models without rebuilding infra; prompt-eval tooling

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Interfaces

web, cli, api, slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Tool access

Skills/plugins to gather evidence, read logs, inspect failures; MCP integrations; Bazel-aware selectivity tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Knowledge

Localized AGENTS.md per service; Dash (Dropbox context engineering); passing + failing test logs

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Credentials

Operates within Dropbox's existing infra and validation paths; same auth/authz as engineers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Context management

Session history (notes/logs) carried across retry attempts

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Supporting component

Bounded iteration with feedback on failure; deterministic systems control test execution

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Supporting component

Dropbox context-engineering system feeding agents across the SDLC

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Platform value exceeds code generation; validation, guardrails, and context matter as much

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Context, validation, and guardrails reinforce each other to make background work trustworthy

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Not every step belongs in the agent loop; deterministic systems should control test execution and timing

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

Lesson

Integrate with existing engineering infrastructure rather than building separate AI-specific workflows

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for agent-assisted SDLC workflow → accepted change; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The source documents human participation but does not locate one consistent attention boundary across Nova workflows.

Observation date
:   2026-05-22

- Supports [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md) (first-party)

#### Sources

1. [Introducing Nova, our internal platform for coding agents](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-1/content.md)  <https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Hacker News submission for Nova](https://news.ycombinator.com/item?id=48235065) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/dropbox-nova-source-2/content.md)  <https://news.ycombinator.com/item?id=48235065> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#dropbox-nova)

Flex Task agent

### AI Investigation Agent

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

GitHub Task agent

### Qubot

GitHub's internal data-analytics agent, powered by GitHub Copilot. Any GitHub employee can ask a question about the company data warehouse in plain language and get an answer within seconds.

Data

data question → warehouse answer: Unknown

Operating model, claims & sources

#### Scoped operating models

**data question → warehouse answer** Unknown · Level unknown

#### Summary and context

Summary

GitHub's internal data-analytics agent, powered by GitHub Copilot. Any GitHub employee can ask a question about the company data warehouse in plain language and get an answer within seconds.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Hundreds of users run thousands of queries; data questions in internal Slack channels dropped

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   GitHub reported the adoption figures in its own engineering blog without independent verification.

Reported by
:   GitHub

Scope
:   Internal GitHub Qubot users and queries; no exact count or measurement window

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-06

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party) Preserved content.md, lines 70

Key observation

Hundreds of users run thousands of queries

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   GitHub reported the adoption figures in its own engineering blog.

Reported by
:   GitHub

Scope
:   Internal GitHub Qubot users and queries; no exact count or measurement window

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party) Preserved content.md, lines 70

#### Architecture and primitives

Model

Powered by GitHub Copilot

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party)

Tool access

Queries GitHub's data warehouse

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party)

#### Other reported details and interpretation

Key observation

Volume of data questions in internal data and analytics Slack channels dropped

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Company reports a qualitative decrease without before-and-after counts.

Scope
:   Questions in GitHub internal data and analytics Slack channels

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party) Preserved content.md, lines 70

#### Operating model evidence

Operating model assessment

Unclassified for data question → warehouse answer; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The public evidence does not document where human attention returns in the question-and-answer flow.

Observation date
:   2026-06

- Supports [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md) (first-party)

#### Sources

1. [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/github-qubot-source-1/content.md)  <https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#github-qubot)

Harvey Platform

### Spectre

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

HubSpot Task agent

### Sidekick

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

Linear Task agent

### Linear Agent

A native agent that synthesizes workspace context, triages, creates follow-up work, runs coding sessions, and executes scheduled/event-driven 'Loops'; used by Linear's own CX, Product, and Engineering teams.

Support Customer success Coding

assigned coding work → agent-created change: Work product review

Operating model, claims & sources

#### Scoped operating models

**assigned coding work → agent-created change** Work product review · Level 3

#### Summary and context

Summary

A native agent that synthesizes workspace context, triages, creates follow-up work, runs coding sessions, and executes scheduled/event-driven 'Loops'; used by Linear's own CX, Product, and Engineering teams.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)
- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)
- Supports [Introducing Linear Agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-6/content.md) (first-party)

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

Harness

Separate planning agent (triage/issue creation) and coding agent (code generation); Code Intelligence for codebase knowledge; scheduled/event-driven 'Loops'

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)
- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Model

Codex was used for internal pull-request review; other model choices are not detailed in the preserved sources

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Interfaces

slack, intercom, linear, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Tool access

Triage Intelligence (auto-route, dedup, label); GitHub; testing Code Intelligence + custom MCP servers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Knowledge

Semantic/vector search evolved into agentic context acquisition across the workspace; Datadog/Sentry customer context

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Credentials

The Agent SDK gives agents explicit identities, scoped OAuth tokens, assignable/mentionable handles, and visible human delegation; issues stay assigned to a human; 'an agent cannot be held accountable'

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md) (first-party)

Supporting component

Auto-routes issues, flags duplicates, suggests labels

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Supporting component

Agents get identities, scoped team access, and visible delegation alongside humans

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md) (first-party)

Supporting component

Scheduled or event-driven agent runs that execute recurring work

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Keep the agent close to the source of work (Intercom, Slack, Linear); the best workflows live where work already happens

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Gradual autonomy; start by asking for suggestions, observe, add guidance, only automate once proven reliable

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Break work into small steps to keep coding agents focused and successful

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

One Linear engineer reports that agent mistakes reveal possible failure modes during review

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Close the loop; auto-notify the customer when their request ships

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for assigned coding work → agent-created change; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents delegated coding output while a human remains accountable for the assigned issue.

Observation date
:   2026-08-11

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

#### Sources

1. [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md)  <https://linear.app/now/how-we-built-linear-agent> engineering-blog · first-party · Last source verification: 2026-08-31
2. [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md)  <https://linear.app/now/how-we-use-linear-agent-at-linear> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md)  <https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk> engineering-blog · first-party · Last source verification: 2026-08-31
4. [Hacker News submission for how Linear built its agent](https://news.ycombinator.com/item?id=49252304) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-4/content.md)  <https://news.ycombinator.com/item?id=49252304> hn-thread · community · Last source verification: 2026-08-31
5. [Hacker News submission for the Linear Agent public beta](https://news.ycombinator.com/item?id=48503334) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-5/content.md)  <https://news.ycombinator.com/item?id=48503334> hn-thread · community · Last source verification: 2026-08-31
6. [Introducing Linear Agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-6/content.md)  <https://linear.app/changelog/2026-03-24-introducing-linear-agent> release · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#linear-agent)

Microsoft Background agent

### PRAssistant

Microsoft's internal AI code-review agent, built by the Developer Division Data and AI team. When an engineer creates a pull request, PRAssistant joins as a reviewer and leaves comments like a human reviewer. It is a distinct internal build that predates and later informed GitHub Copilot Pull Request Reviews.

Code review

pull request → AI review comments: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → AI review comments** Work product review · Level 3

#### Summary and context

Summary

Microsoft's internal AI code-review agent, built by the Developer Division Data and AI team. When an engineer creates a pull request, PRAssistant joins as a reviewer and leaves comments like a human reviewer. It is a distinct internal build that predates and later informed GitHub Copilot Pull Request Reviews.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Supports more than 90% of Microsoft PRs, impacting over 600,000 pull requests per month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Microsoft reported the figures in its own engineering blog without independent verification.

Reported by
:   Microsoft

Scope
:   PRs supported by the internal AI review assistant across Microsoft

Denominator
:   Company pull requests for coverage share

Method
:   Unknown

Observation date
:   2025-07

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party) Preserved content.md, lines 10

Key observation

More than 90% of pull requests across the company

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Microsoft reported the figures in its own engineering blog.

Reported by
:   Microsoft

Scope
:   PRs supported by the internal AI review assistant across Microsoft

Denominator
:   Company pull requests for coverage share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party) Preserved content.md, lines 10

Key observation

More than 600,000 pull requests impacted per month

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Microsoft reported the figures in its own engineering blog.

Reported by
:   Microsoft

Scope
:   PRs supported by the internal AI review assistant across Microsoft

Denominator
:   Company pull requests for coverage share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party) Preserved content.md, lines 10

Key observation

About 5,000 repositories in early onboarding

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Microsoft reported the figures in its own engineering blog.

Reported by
:   Microsoft

Scope
:   Repositories onboarded in early AI code-review experiments

Denominator
:   Unknown

Method
:   Early experiments and data science studies across onboarded repositories

Observation date
:   Unknown

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party) Preserved content.md, lines 35

#### Architecture and primitives

Interfaces

github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for pull request → AI review comments; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The engineering blog describes engineers acting on PRAssistant review comments, which locates human attention at work-product review.

Observation date
:   2025-07

- Supports [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md) (first-party)

#### Sources

1. [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/microsoft-prassistant-source-1/content.md)  <https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#microsoft-prassistant)

monday.com Agent system

### Sphera / Atlas / Morphex

An internal agent system on Amazon Bedrock where agents have identities, managers, scopes, and performance scores; Atlas ships features, Morphex ships PRs autonomously.

Coding Code review

Atlas or Morphex feature task → tested and merged pull request: Outcome review

Operating model, claims & sources

#### Scoped operating models

**Atlas or Morphex feature task → tested and merged pull request** Outcome review · Level 4

#### Summary and context

Summary

An internal agent system on Amazon Bedrock where agents have identities, managers, scopes, and performance scores; Atlas ships features, Morphex ships PRs autonomously.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Reported metrics

Headline claim

Morphex: 19 of 20 PRs merge without human review

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Morphex PRs that merge automatically after CI and Guardrails pass

Denominator
:   Morphex pull requests; sample size and period not supplied

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 148–152

Key observation

Morphex: 19 of 20 PRs merge automatically without human review

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Morphex PRs that merge automatically after CI and Guardrails pass

Denominator
:   Morphex pull requests; sample size and period not supplied

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 148–152

Key observation

90% of Builders use AI coding tools monthly; adoption nearly doubled year over year

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Monthly AI coding-tool adoption among monday Builders, including engineers, PMs, analysts, and designers

Denominator
:   Builders; not exclusively engineers

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 10, 16, 22

Key observation

Per-engineer PR throughput increased by more than 50%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Per-engineer pull-request throughput

Denominator
:   Engineers; baseline period and cohort size not specified

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 10, 23

Key observation

Guardrails catches ~25% of agent PRs before human review; low single-digit revert rate

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Recent cut of top PR-generating agents; Guardrails rejection before review and reverts among merged PRs

Denominator
:   Agent PRs for Guardrails rejection; merged PRs for revert rate

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 154–158

#### Architecture and primitives

Sandbox

Amazon EKS, one pod per active session; a remote sandbox tests each PR before review; EFS workspace mount

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Harness

Claude Agent SDK behind a thin monday-agent-sdk wrapper (provider neutrality, cold-start optimization, custom harness opinions)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Model

Amazon Bedrock; Application Inference Profiles for routing; cross-region failover; PrivateLink (traffic stays in VPC)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Interfaces

slack, monday, github

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Tool access

Triggers via Slack @mention, monday item assignment, or GitHub PR review → SNS → per-team SQS → consumers; monday MCP servers underpin the Guardrails

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Knowledge

File-based memory: MEMORY.md (cross-session) + diary/YYYY-MM-DD.md; sessions/repos/secrets on EFS; durable records on S3

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Credentials

Per-session secrets in AWS Secrets Manager; same RBAC as humans; real Slack/GitHub/monday accounts

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Context management

Live state in ElastiCache (sub-ms); monday boards (Builders CoWORK) as shared state for tasks, status, handoffs

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

Stable identity + assigned human manager + scope + performance score

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

Automated review against monday standards (metrics, feature flags, security)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

MEMORY.md + daily diary instead of vector retrieval

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

monday boards as the shared-state layer for human/agent collaboration

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Lessons and interpretation

Lesson

Evals from day one; should have been day one, not month nine

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

Skip the vector store; file-based memory (MEMORY.md) was the right answer

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

Remote-sandbox every PR before human review, with production-traffic replay

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

The existing auth/identity/deploy pipeline applies to agents; reuse it

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

AI engineering is building the feedback loops that let imperfect agents be trusted safely

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Level 4 for Atlas or Morphex feature task → tested and merged pull request; human attention boundary: outcome-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The secondary source reports predominantly automatic merges and automated guardrails, while humans manage tasks and outcomes.

Observation date
:   2026

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Sources

1. [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md)  <https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/> case-study · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#monday-sphera-atlas-morphex)

Notion Platform

### Custom Agents

Notion's Custom Agents platform, dogfooded internally across non-engineering teams such as IT ticketing, supply chain, procurement, and recruiting. By the end of alpha testing, Notion had more than 3,000 internal Custom Agents. Notion's own security team is one of the most active internal users. Notion rebuilt the agent harness three to five times as frontier models improved.

Support Finance ops Recruitment Security

cross-team internal tasks → Custom Agents output: Unknown

Operating model, claims & sources

#### Scoped operating models

**cross-team internal tasks → Custom Agents output** Unknown · Level unknown

#### Summary and context

Summary

Notion's Custom Agents platform, dogfooded internally across non-engineering teams such as IT ticketing, supply chain, procurement, and recruiting. By the end of alpha testing, Notion had more than 3,000 internal Custom Agents. Notion's own security team is one of the most active internal users. Notion rebuilt the agent harness three to five times as frontier models improved.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Notion's Token Town: 5 Rebuilds, 100+ Tools (Latent Space)](https://latent.space/p/notion) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-1/content.md) (direct-participant)
- Supports [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-2/content.md) (first-party)

#### Reported metrics

Headline claim

More than 3,000 internal Custom Agents by end of alpha testing

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Notion reported the agent count in its own engineering blog without independent verification.

Reported by
:   Notion

Scope
:   Internal Notion Custom Agents at the end of alpha; excludes the separate customer alpha count

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-04

- Supports [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-2/content.md) (first-party) Preserved content.md, lines 51

Key observation

More than 3,000 internal Custom Agents by end of alpha testing

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Notion reported the agent count in its own engineering blog.

Reported by
:   Notion

Scope
:   Internal Notion Custom Agents at the end of alpha; excludes the separate customer alpha count

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-2/content.md) (first-party) Preserved content.md, lines 51

Key observation

Agent harness rebuilt three to five times as models improved

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Participants give differing approximate rebuild counts for harness, framework, and feature; not a precise engineering inventory.

Reported by
:   Notion

Scope
:   Notion agent/framework rebuilds recalled by participants; estimates range from three to five

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Notion's Token Town: 5 Rebuilds, 100+ Tools (Latent Space)](https://latent.space/p/notion) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-1/content.md) (direct-participant) Preserved content.md, lines 115, 275–277, 819

#### Other reported details and interpretation

Key observation

Notion's security team is one of the most active internal users

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Qualitative first-party description; no comparative activity count is supplied.

Scope
:   Notion security team internal Custom Agent use

- Supports [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-2/content.md) (first-party) Preserved content.md, lines 57

#### Operating model evidence

Operating model assessment

Unclassified for cross-team internal tasks → Custom Agents output; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   Custom Agents spans many teams and workflows, so no single human-attention boundary applies.

Observation date
:   2026-04

- Supports [Notion's Token Town: 5 Rebuilds, 100+ Tools (Latent Space)](https://latent.space/p/notion) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-1/content.md) (direct-participant)

#### Sources

1. [Notion's Token Town: 5 Rebuilds, 100+ Tools (Latent Space)](https://latent.space/p/notion) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-1/content.md)  <https://latent.space/p/notion> podcast · direct-participant · Last source verification: 2026-08-31
2. [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/notion-custom-agents-source-2/content.md)  <https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#notion-custom-agents)

Plaid Task agent

### AI Annotator

Plaid's internal labeling agent for its own model training. AI Annotator automates large-scale labeling of anonymized transaction data, with human oversight on the labeled output. Plaid reports greater than 95% human alignment at a lower cost and time than manual labeling.

Data

raw transactions → labeled training data: Work product review

Operating model, claims & sources

#### Scoped operating models

**raw transactions → labeled training data** Work product review · Level 3

#### Summary and context

Summary

Plaid's internal labeling agent for its own model training. AI Annotator automates large-scale labeling of anonymized transaction data, with human oversight on the labeled output. Plaid reports greater than 95% human alignment at a lower cost and time than manual labeling.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

Greater than 95% human alignment at lower cost and time than manual labeling

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figure in its own blog without independent verification.

Reported by
:   Plaid

Scope
:   Transaction labels generated by AI Annotator in early use

Denominator
:   Labels compared with human judgments; sample size unspecified

Method
:   Unknown

Observation date
:   2025-06

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party) Preserved content.md, lines 16–20

Key observation

Greater than 95% human alignment with labeled data

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figure in its own blog.

Reported by
:   Plaid

Scope
:   Transaction labels generated by AI Annotator in early use

Denominator
:   Labels compared with human judgments; sample size unspecified

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party) Preserved content.md, lines 16–20

Key observation

Lower cost and time than manual labeling

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Qualitative company comparison; neither actual costs nor elapsed-time measurements are supplied.

Reported by
:   Plaid

Scope
:   AI transaction annotation cost and time relative to manual labeling

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party) Preserved content.md, lines 20

#### Architecture and primitives

Knowledge

Anonymized Plaid transaction data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for raw transactions → labeled training data; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The reported greater than 95% human alignment implies that people review the labeled output.

Observation date
:   2025-06

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md) (first-party)

#### Sources

1. [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-ai-annotator-source-1/content.md)  <https://plaid.com/blog/ai-agents-june-2025/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#plaid-ai-annotator)

Plaid Task agent

### Fix My Connection

Plaid's internal agent for bank-integration reliability. Fix My Connection proactively detects bank-integration failures and generates repair scripts automatically. Plaid reports more than 2 million successful user-permissioned logins and a 90% reduction in the average time to fix a degradation.

Ops Maintenance

integration degradation → repaired connection: Outcome review

Operating model, claims & sources

#### Scoped operating models

**integration degradation → repaired connection** Outcome review · Level 4

#### Summary and context

Summary

Plaid's internal agent for bank-integration reliability. Fix My Connection proactively detects bank-integration failures and generates repair scripts automatically. Plaid reports more than 2 million successful user-permissioned logins and a 90% reduction in the average time to fix a degradation.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

More than 2 million successful logins and 90% faster average repair

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figures in its own blog without independent verification.

Reported by
:   Plaid

Scope
:   Automated repair of bank connections and the successful user-permissioned logins enabled by those repairs

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2025-06

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party) Preserved content.md, lines 26–32

Key observation

More than 2 million successful user-permissioned logins

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figure in its own blog.

Reported by
:   Plaid

Scope
:   Automated repair of bank connections and the successful user-permissioned logins enabled by those repairs

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party) Preserved content.md, lines 26–32

Key observation

Average time to fix a degradation reduced by 90%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figure in its own blog.

Reported by
:   Plaid

Scope
:   Automated repair of bank connections and the successful user-permissioned logins enabled by those repairs

Denominator
:   Average degradation-repair time before automated repairs; no baseline duration provided

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party) Preserved content.md, lines 26–32

#### Architecture and primitives

Tool access

Plaid bank-integration infrastructure

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 4 for integration degradation → repaired connection; human attention boundary: outcome-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid measures success by outcomes such as successful logins rather than per-repair inspection.

Observation date
:   2025-06

- Supports [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md) (first-party)

#### Sources

1. [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-fix-my-connection-source-1/content.md)  <https://plaid.com/blog/ai-agents-june-2025/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#plaid-fix-my-connection)

Plaid Supporting pattern

### Internal MCP server

Plaid's central internal Model Context Protocol server. Plaid built it because third-party MCP servers could not reach its internal data. The server integrates more than 20 tools and several internal services such as Jira, application logs, and data schemas, behind Plaid's identity-aware proxy and centralized authorization. Plaid reports thousands of tool calls and dozens of agents built on the server. Separately, Claude Code and Cursor are used by more than 80% of Plaid engineers; server adoption is not quantified.

Coding

engineer request → internal tool access: Unknown

Operating model, claims & sources

#### Scoped operating models

**engineer request → internal tool access** Unknown · Level unknown

#### Summary and context

Summary

Plaid's central internal Model Context Protocol server. Plaid built it because third-party MCP servers could not reach its internal data. The server integrates more than 20 tools and several internal services such as Jira, application logs, and data schemas, behind Plaid's identity-aware proxy and centralized authorization. Plaid reports thousands of tool calls and dozens of agents built on the server. Separately, Claude Code and Cursor are used by more than 80% of Plaid engineers; server adoption is not quantified.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party) Preserved content.md, lines 38–45, 65–89

#### Reported metrics

Headline claim

Dozens of agents rely on the internal MCP server; Claude Code and Cursor are used by over 80% of engineers

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figures in its own engineering blog without independent verification.

Reported by
:   Plaid

Scope
:   Claude Code and Cursor adoption among Plaid engineers; separate from internal MCP server adoption

Denominator
:   Plaid engineers for the AI-client usage share

Method
:   Unknown

Observation date
:   2025

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party) Preserved content.md, lines 38, 89

Key observation

Claude Code and Cursor are used by over 80% of Plaid engineers; the source does not report internal MCP server adoption share

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figures in its own engineering blog.

Reported by
:   Plaid

Scope
:   Claude Code and Cursor adoption among Plaid engineers; separate from internal MCP server adoption

Denominator
:   Plaid engineers for the AI-client usage share

Method
:   Unknown

Observation date
:   Unknown

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party) Preserved content.md, lines 38, 89

Key observation

Thousands of tool calls and dozens of agents built on it

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Plaid reported the figures in its own engineering blog.

Reported by
:   Plaid

Scope
:   Tool calls and agents relying on the internal MCP server across engineering, product, and support

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party) Preserved content.md, lines 89

#### Architecture and primitives

Harness

Central internal MCP server that fronts vendor AI clients

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party)

Tool access

More than 20 tools and several internal services (Jira, logs, schemas)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party)

Credentials

Behind Plaid's identity-aware proxy and centralized authorization

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for engineer request → internal tool access; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The MCP server is a tool-access layer, not a workflow with a single human-attention boundary.

Observation date
:   2025

- Supports [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md) (first-party)

#### Sources

1. [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/plaid-internal-mcp-server-source-1/content.md)  <https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#plaid-internal-mcp-server)

PostHog Background agent

### StampHog

A GitHub-label-triggered PR approval agent that applies fail-closed deterministic safety gates, asks an LLM to check for showstoppers, autonomously approves eligible changes, and refuses or escalates the rest.

Code review

eligible pull request → approval decision: Exception only

Operating model, claims & sources

#### Scoped operating models

**eligible pull request → approval decision** Exception only · Level 5

#### Summary and context

Summary

A GitHub-label-triggered PR approval agent that applies fail-closed deterministic safety gates, asks an LLM to check for showstoppers, autonomously approves eligible changes, and refuses or escalates the rest.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Add a PR auto-stamper
- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

#### Reported metrics

Headline claim

Handled 1,600 PRs in the previous month, as reported on July 9, 2026; roughly one in three merged main-repository PRs received its final approval during the reported quarter

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   PostHog reports two different windows in its July 9, 2026 article; exact monthly and quarterly boundaries are not supplied.

Reported by
:   PostHog

Scope
:   Monthly PRs handled autonomously and quarterly final approvals in the main repository

Denominator
:   Merged main-repository PRs for the quarterly share; absolute handled PRs for the monthly count

Method
:   Company-reported production usage

Observation date
:   2026-07

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 105, 118

Key observation

1,600 PRs handled autonomously in the previous month, as reported on July 9, 2026

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   July 9 is the report date; the source says last month without exact measurement boundaries.

Reported by
:   PostHog

Scope
:   PRs handled autonomously in the previous month, as reported on July 9, 2026; exact boundaries unspecified

Denominator
:   Unknown

Method
:   Company-reported production usage

Observation date
:   2026-07-09

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 118

Key observation

Roughly one in three PRs merged into PostHog's main repository received StampHog's final approval during the reported quarter

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   PostHog

Scope
:   Main-repository merged PRs receiving StampHog final approval during the reported quarter

Denominator
:   Merged PRs in the main repository

Method
:   Company-reported production usage

Observation date
:   2026-07

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Preserved content.md, lines 105

Key observation

20% of PRs approved by StampHog in the July 28, 2026 report, at approximately $300 per month in tokens

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   PostHog

Scope
:   PostHog PRs approved by StampHog and monthly token cost in the July 28, 2026 report

Denominator
:   PostHog PRs in the report's scope

Method
:   Company-reported production usage and token spend

Observation date
:   2026-07

- Supports [10,000 PRs a month is easy: How devex is evolving at PostHog](https://posthog.com/blog/10k-prs-a-month) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-2/content.md) (first-party) Preserved content.md, lines 131

#### Architecture and primitives

Harness

A GitHub Action invokes a Python pipeline that fetches and classifies a PR, applies hard gates, waits for in-flight reviewer bots, runs an LLM review, and posts a verdict

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works and Architecture

Model

Claude through the Claude Agent SDK, with Read, Grep, and Glob tools

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Interfaces

github, ci

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage

Tool access

Reads the diff and repository files plus trusted review-state, discussion, ownership, and reviewer signals

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Knowledge

Repository-specific deny categories, size and risk tiers calibrated from prior human approvals, review guidance, and ownership data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Tiers and Empirical basis

Credentials

A dedicated Anthropic organization secret and a StampHog GitHub App token whose approvals satisfy branch protection

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage and final verdict

Context management

Each run emits a versioned JSON evidence bundle retained as a CI artifact for 30 days; a sticky GitHub comment carries non-approval verdict history and labels preserve retry state

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage and Evidence bundle

Supporting component

Draft state, conflicts, requested changes, sensitive paths, size ceilings, and risk tiers can block AI approval; the LLM may tighten but never loosen a gate

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

Supporting component

Eligible changes can be approved while risky, ambiguous, or insufficiently assured changes are refused or escalated to a suitable human reviewer

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party) Add a PR auto-stamper
- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, LLM Review

Supporting component

Each run records PR metadata, classification, gate results, reviewer output, and the final verdict

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Evidence bundle

#### Lessons and interpretation

Lesson

Use deterministic controls for known risks and allow the LLM to make approval stricter, never more permissive

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code explicitly implements and documents this safety invariant.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, How it works

Lesson

Calibrate thresholds and deny categories from repository history rather than treating small diffs as inherently safe

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code documents calibration against historical approval outcomes.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Tiers and Empirical basis

Lesson

Fail closed and preserve retry state when dependencies, credentials, or concurrent reviewer bots are unavailable

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source code explicitly documents fail-closed and retry behavior.

- Supports [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md) (first-party) commit 988c9031bb93c74bafcdfb670c01497c79a4f644, tools/pr-approval-agent/README.md, Usage

#### Operating model evidence

Operating model assessment

Level 5 for eligible pull request → approval decision; human attention boundary: exception-only.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   Eligible pull requests are approved automatically; risky or ambiguous cases are refused or routed to a human.

Observation date
:   2026-07-09

- Supports [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md) (first-party)

#### Sources

1. [Stop being the code review bottleneck](https://posthog.com/newsletter/code-review-tips) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-1/content.md)  <https://posthog.com/newsletter/code-review-tips> corporate-article · first-party · Last source verification: 2026-08-31
2. [10,000 PRs a month is easy: How devex is evolving at PostHog](https://posthog.com/blog/10k-prs-a-month) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-2/content.md)  <https://posthog.com/blog/10k-prs-a-month> engineering-blog · first-party · Last source verification: 2026-08-31
3. [StampHog PR approval agent source code and documentation](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/posthog-stamphog-source-3/content.md)  <https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent> source-code · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#posthog-stamphog)

Ramp Background agent

### Inspect

A background coding agent that closes the loop on verifying its own work; runs tests, reviews telemetry, queries feature flags, visually verifies the frontend; now also monitoring production and proposing fixes; also a platform that hosts many internal agents.

Coding Code review On-call

Inspect coding task → reviewed production merge: Work product review

Operating model, claims & sources

#### Scoped operating models

**Inspect coding task → reviewed production merge** Work product review · Level 3

#### Summary and context

Summary

A background coding agent that closes the loop on verifying its own work; runs tests, reviews telemetry, queries feature flags, visually verifies the frontend; now also monitoring production and proposing fixes; also a platform that hosts many internal agents.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)
- Supports [Why We Built Our Own Background Agent (Inspect) (Ramp Builders URL)](https://builders.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-4/content.md) (first-party)
- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) What is Inspect? section

#### Reported metrics

Headline claim

75% of Ramp's merged PRs raised by Inspect sessions (May 2026)

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Ramp merged PRs raised by Inspect sessions by May 2026

Denominator
:   Merged Ramp pull requests

Method
:   Unknown

Observation date
:   2026-05

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 58–68

Key observation

Around 60% of Ramp PRs authored by Inspect by January 2026

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Ramp PRs authored by Inspect by January 2026

Denominator
:   Ramp pull requests in the source adoption history

Method
:   Unknown

Observation date
:   2026-01

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 58–68

Key observation

75% of merged PRs raised by Inspect sessions (May 2026)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Ramp

Scope
:   Ramp merged PRs raised by Inspect sessions by May 2026

Denominator
:   Merged Ramp pull requests

Method
:   Unknown

Observation date
:   2026-05

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 58–68
- Supports [Ramp x Linear (75% of merged PRs via Inspect)](https://linear.app/customers/ramp) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-2/content.md) (first-party) Preserved content.md, lines 10

Key observation

Around 30% of merged frontend and backend PRs in the earlier first-party report, after a couple of months of adoption

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Ramp

Scope
:   Merged PRs in Ramp frontend and backend repositories after the first couple of months of adoption

Denominator
:   Merged PRs in frontend and backend repositories

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party) Preserved content.md, lines 24

Key observation

Around 90% of PRs merged into the Inspect repository come from Inspect sessions in the later interview report

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   PRs merged into the Inspect repository

Denominator
:   Merged PRs in the Inspect repository

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 96–102

Key observation

One million total Inspect sessions crossed in July 2026

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Cumulative Inspect sessions crossing the million mark in July 2026

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   2026-07

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 66–72

Key observation

Under 5 seconds to spin up a fully provisioned remote dev environment

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Provisioning a fully configured remote development environment

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 100

Key observation

150+ engineers contributed to the Inspect codebase in the later interview report

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Engineers who contributed to the Inspect codebase in the later interview report

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 102

Key observation

5.5-person Inspect team (four engineers, a director, and a part-time PM)

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Inspect team staffing: four engineers, one director, and a part-time PM

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 101

Key observation

More than 80% of Inspect is written in Inspect sessions

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   Ramp

Scope
:   Inspect code written in Inspect sessions; distinct from merged PR share

Denominator
:   Inspect code; the source does not define a code-volume counting method

Method
:   Unknown

Observation date
:   Unknown

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 111

#### Architecture and primitives

Sandbox

Modal sandboxes; per-repo images rebuilt every 30 min from snapshots; warm-on-keystroke; a pool of warm sandboxes

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Harness

OpenCode (server-first) as the agent runtime; a plugin blocks writes until sync completes; expanded into production monitoring and self-maintenance; Inspect itself is built with React/Vite, Cloudflare Durable Objects, SQLite, and the Cloudflare Agents SDK

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Model

All frontier models, MCPs, custom tools, skills

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Interfaces

slack, web, chrome-extension, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Tool access

Wired into Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack, Buildkite; monitors production, triages issues, proposes fixes; debugging queries a sanitized read-only production DB replica and Snowflake

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Knowledge

Skills that encode how Ramp ships; repo images with the full dev env (Vite, Postgres, Redis, RabbitMQ, Temporal, Chromium, VS Code Server)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Credentials

GitHub auth per user; the sandbox pushes the branch, an API opens the PR with the user's token (no self-approval); production merges retain human review

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Supporting component

Pre-warmed full dev envs; fast cold start; effectively free to run

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Supporting component

Server-first agent with a typed SDK + plugin system; code is its own source of truth

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Supporting component

Any number of people in one session; each change attributed to its author

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

#### Other reported details and interpretation

Key observation

Inspect underpins internal agents including ReviewBuddy, Oncall Assistant, Testo, Ramp Research, Voice of the Customer, and error automations

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Scope
:   Examples of internal agents built on Inspect

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Preserved content.md, lines 134–141

Key observation

Design goal: session speed should be limited only by model-provider time-to-first-token

Opinion · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   The source says session speed should only be limited by model time-to-first-token; this is a design goal, not a measured result.

Scope
:   Target session startup speed, excluding precompleted cloning and installation

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party) Preserved content.md, lines 22

#### Lessons and interpretation

Lesson

Own the tooling; it only has to work on your code, which lets you build something more powerful than off-the-shelf

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Lesson

Work in public spaces to create virality loops; let the product do the talking, don't mandate

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Lesson

Ramp argues that a fast background agent can add remote resources and concurrency to the same model

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Lesson

Move as much as possible into the image-build step so users never wait on setup

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

Lesson

The v1 Chrome extension saw little adoption; the pivot to a centrally configured remote dev environment with a coding agent on top drove adoption

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source reports that v1 saw little adoption and that the November 2025 pivot to a remote dev environment preceded rapid adoption.

- Supports [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md) (independent-secondary) Why build your own background coding agent? section

#### Operating model evidence

Operating model assessment

Level 3 for Inspect coding task → reviewed production merge; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source explicitly states that Inspect cannot self-approve and production merges retain human review.

Observation date
:   2026-05

- Supports [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md) (first-party)

#### Sources

1. [Why We Built Our Own Background Agent (Inspect)](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-1/content.md)  <https://engineering.ramp.com/post/why-we-built-our-background-agent> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Ramp x Linear (75% of merged PRs via Inspect)](https://linear.app/customers/ramp) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-2/content.md)  <https://linear.app/customers/ramp> case-study · first-party · Last source verification: 2026-08-31
3. [Hacker News project discussion inspired by Ramp Inspect](https://news.ycombinator.com/item?id=48042123) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-3/content.md)  <https://news.ycombinator.com/item?id=48042123> hn-thread · community · Last source verification: 2026-08-31
4. [Why We Built Our Own Background Agent (Inspect) (Ramp Builders URL)](https://builders.ramp.com/post/why-we-built-our-background-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-4/content.md)  <https://builders.ramp.com/post/why-we-built-our-background-agent> engineering-blog · first-party · Last source verification: 2026-08-31
5. [Why Ramp built its own in-house coding agent, Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ramp-inspect-source-5/content.md)  <https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect> news · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#ramp-inspect)

Replit Orchestration system

### Manager agent (agent-of-agents)

An internal agent-of-agents stack where every employee gets a manager agent that spawns multiple agents for verifiable work and escalates judgment to humans.

Coding Code review Support Research Data

objective → verifiable multi-agent work product: Work product review

Operating model, claims & sources

#### Scoped operating models

**objective → verifiable multi-agent work product** Work product review · Level 3

#### Summary and context

Summary

An internal agent-of-agents stack where every employee gets a manager agent that spawns multiple agents for verifiable work and escalates judgment to humans.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

2.9x code output for a consistent author cohort; review latency, PR reversions, and incident trends reported flat

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Replit

Scope
:   Code output for a consistent author cohort across early January to late June; separate from company-wide hiring effects

Denominator
:   Same cohort of authors before and after

Method
:   Comparison of contributed code for a consistent author cohort; raw company-wide lines of code increased 5.8x

Observation date
:   Unknown

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party) Preserved content.md, lines 10, 38–56

Key observation

2.9x code output for a consistent author cohort from early January to late June

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Replit

Scope
:   Code output for a consistent author cohort across early January to late June; separate from company-wide hiring effects

Denominator
:   Same cohort of authors before and after

Method
:   Comparison of contributed code for a consistent author cohort; raw company-wide lines of code increased 5.8x

Observation date
:   Unknown

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party) Preserved content.md, lines 10, 38–56

Key observation

No corresponding deterioration in review/reversion/incident metrics

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Replit

Scope
:   Company code review latency, PR reversion rates, and incidents opened during increased code output

Denominator
:   Unknown

Method
:   Company comparison of review latency, PR reversion rates, and incident trends

Observation date
:   Unknown

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party) Preserved content.md, lines 50–56

#### Architecture and primitives

Sandbox

microVMs and remote filesystems behind access policies, token proxies, audit logging, and a ZeroTrust network

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party) Preserved content.md, lines 34

Harness

Fleet/loop orchestration: a manager agent launches parallel agents for verifiable work and escalates judgment

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Interfaces

slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Tool access

Investigates incidents, reviews PRs, answers questions, analyzes company data, triages support, researches sales accounts, improves Replit Agent itself

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Context management

Manager agent coordinates parallel sub-agents and routes results

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Supporting component

One human gives an objective; the manager spawns parallel agents for verifiable work and escalates judgment

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Give every employee a manager agent that spawns sub-agents; verifiable work parallelizes, judgment escalates to humans

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

Lesson

Track outcome metrics (reverts, incidents), not activity; output can scale without quality regressions

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for objective → verifiable multi-agent work product; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes autonomous parallel execution followed by human judgment on the resulting work.

Observation date
:   2026

- Supports [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md) (first-party)

#### Sources

1. [The Self-Driving Company](https://ld.replit.com/blog/self-driving-company) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/replit-manager-agent-source-1/content.md)  <https://ld.replit.com/blog/self-driving-company> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#replit-manager-agent)

Retool Task agent

### RetoolGPT

Retool's internal assistant, built as a version of ChatGPT with access to Retool's internal Confluence documents, Retool documentation, and Linear tickets. The team deployed it organization-wide in a read-only environment so the whole team could use it.

Support Coding

internal question → sourced answer: Unknown

Operating model, claims & sources

#### Scoped operating models

**internal question → sourced answer** Unknown · Level unknown

#### Summary and context

Summary

Retool's internal assistant, built as a version of ChatGPT with access to Retool's internal Confluence documents, Retool documentation, and Linear tickets. The team deployed it organization-wide in a read-only environment so the whole team could use it.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-1/content.md) (first-party)
- Supports [AI Build Week, Day 3: How we made RetoolGPT](https://www.youtube.com/watch?v=8VTdYUBAZsY) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-2/content.md) (first-party)

#### Architecture and primitives

Model

Built on ChatGPT

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-1/content.md) (first-party)

Knowledge

Retool Confluence documents, Retool documentation, and Linear tickets

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for internal question → sourced answer; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The public evidence does not document where human attention returns in the question-and-answer flow.

Observation date
:   2025-08

- Supports [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-1/content.md) (first-party)

#### Sources

1. [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-1/content.md)  <https://retool.com/blog/how-we-built-retoolgpt> engineering-blog · first-party · Last source verification: 2026-08-31
2. [AI Build Week, Day 3: How we made RetoolGPT](https://www.youtube.com/watch?v=8VTdYUBAZsY) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/retool-retoolgpt-source-2/content.md)  <https://www.youtube.com/watch?v=8VTdYUBAZsY> talk · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#retool-retoolgpt)

Salesforce Task agent

### Slackbot

Salesforce was 'customer zero' for the rebuilt Slackbot; an employee agent that finds company context, drafts work, and connects Slack context with Salesforce data; now also an external product.

Support Customer success Ops

employee request → drafted work: Work product review

Operating model, claims & sources

#### Scoped operating models

**employee request → drafted work** Work product review · Level 3

#### Summary and context

Summary

Salesforce was 'customer zero' for the rebuilt Slackbot; an employee agent that finds company context, drafts work, and connects Slack context with Salesforce data; now also an external product.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)
- Supports [Interview with Slackbot about connected work context](https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-2/content.md) (first-party)

#### Architecture and primitives

Harness

An employee agent intended as a front door to other agents

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Interfaces

slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Tool access

Finds company context, drafts work, manages meetings, connects Slack context with Salesforce data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Knowledge

Slack context joined with Salesforce CRM data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Credentials

Permission-aware by construction; sees what the employee can see, respects roles and access controls

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Supporting component

Agent visibility is bounded by the invoking employee's permissions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Dogfood internally first ('customer zero') before shipping externally

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Lesson

Make permission-awareness a construction property, not a prompt instruction; the agent sees only what the employee can see

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for employee request → drafted work; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source describes an employee agent that prepares drafts and contextual work for human use.

Observation date
:   2026-01-14

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Sources

1. [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md)  <https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/> release · first-party · Last source verification: 2026-08-31
2. [Interview with Slackbot about connected work context](https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-2/content.md)  <https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/> corporate-article · first-party · Last source verification: 2026-08-31
3. [Salesforce rolls out new Slackbot AI agent](https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-3/content.md)  <https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and> news · independent-secondary · Last source verification: 2026-08-31
4. [Hacker News submission for the Salesforce Slackbot rollout](https://news.ycombinator.com/item?id=46600760) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-4/content.md)  <https://news.ycombinator.com/item?id=46600760> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#salesforce-slackbot)

Sentry Task agent

### Junior

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

Shopify Platform

### Aquifer / River

The Aquifer agent platform (session/harness/sandbox split) powers River, a Slack-native coding agent, plus research, migration, and app-security agents.

Coding Code review Research Security

River coding request → reviewed pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**River coding request → reviewed pull request** Work product review · Level 3

#### Summary and context

Summary

The Aquifer agent platform (session/harness/sandbox split) powers River, a Slack-native coding agent, plus research, migration, and app-security agents.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Reported metrics

Headline claim

1 in 8 merged PRs company-wide coauthored by River

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   Merged River-coauthored PRs across Shopify

Denominator
:   All Shopify merged pull requests

Method
:   Unknown

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 12

Key observation

River: 59,918 sessions / 30 days across 5,170 Slack channels

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   River sessions and distinct Slack channels in a recent 30-day period

Denominator
:   Unknown

Method
:   river\_sessions domain table, written by River every session

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 83

Key observation

3,536 River-coauthored PRs merged; 1 in 8 merged PRs company-wide

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   River-coauthored merged PRs in the recent 30-day period; company-wide PR share

Denominator
:   All Shopify merged pull requests for the one-in-eight share

Method
:   river\_sessions domain table for reported session-linked counts

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 12, 83

Key observation

Median session 19 min; median 50 tool calls/session

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Shopify

Scope
:   Median River session duration and tool calls per session

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party) Preserved content.md, lines 65

#### Architecture and primitives

Sandbox

An execution environment (filesystem, shell, repo, build/test) separated from the harness; Shopify credits the brain-and-hands framing to Anthropic

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Harness

Session (durable; Postgres append-only event log) + Harness (cheap agent loop) + Cell (ephemeral Go runtime); cells die, sessions persist

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Model

The design lets Shopify change the model without changing the sandbox

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Interfaces

slack, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Tool access

Repo + tests + data warehouse + production traces + PR creation; a gateway credentials proxy

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Knowledge

Monorepo 'World' (code + skills + conventions + intent docs + runbooks + AGENTS.md); Nix reproducible envs; Slack-transcript corpus mining

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Credentials

Gateway credentials proxy; per-profile sandbox policies; Shopify SSO

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Context management

Skills loaded on-demand as files, updatable per session; session survival across cell/sandbox/machine death

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Durable identity, disposable loop, isolated execution; swap any layer independently

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Slack-native coding agent in public channels only; visibility drives adoption

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Supporting component

Written-down knowledge mined from successful patterns and public transcripts

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Agent-friendly is human-friendly; monorepo, reproducible envs, written skills, and fast CI help both

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Local agents have a ceiling; private windows mean only the person at the keyboard learns anything

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Session survival is critical; cells die, sandboxes die, machines die; the conversation doesn't

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

Lesson

Treat agents as profiles, not platforms; a new agent is a new bundle on the same substrate

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for River coding request → reviewed pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents pull-request creation but does not establish outcome-only supervision.

Observation date
:   2026

- Supports [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md) (first-party)

#### Sources

1. [Under the River](https://shopify.engineering/under-the-river) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/shopify-internal-agents-source-1/content.md)  <https://shopify.engineering/under-the-river> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#shopify-internal-agents)

Sierra Task agent

### Pinecone

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

Slack Supporting pattern

### Multi-agent context system

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

Spotify Agent system

### Honk / Xirp

Honk is Spotify's background coding agent (high confidence); Xirp is the workspace/context/session layer around it (medium confidence). Honk runs on a Claude-Agent-SDK harness in Kubernetes, uses trusted CI tools, and combines formatting and linting with LLM-based diff evaluation.

Coding Migrations Code review

Honk coding task → verified pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**Honk coding task → verified pull request** Work product review · Level 3

#### Summary and context

Summary

Honk is Spotify's background coding agent (high confidence); Xirp is the workspace/context/session layer around it (medium confidence). Honk runs on a Claude-Agent-SDK harness in Kubernetes, uses trusted CI tools, and combines formatting and linting with LLM-based diff evaluation.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)
- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

#### Reported metrics

Headline claim

1,500+ merged pull requests generated by Honk

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Spotify

Scope
:   Cumulative merged Honk-generated PRs reported in Part 1; no measurement cutoff in preserved text

Denominator
:   Unknown

Method
:   Company-reported merged pull request count

Observation date
:   Unknown

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party) Preserved content.md, lines 70

Key observation

1,500+ merged AI-generated PRs (Honk)

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Spotify

Scope
:   Cumulative merged Honk-generated PRs reported in Part 1; no measurement cutoff in preserved text

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party) Preserved content.md, lines 70

Key observation

60-90% time savings on migrations vs manual

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Spotify

Scope
:   Selected code migrations using Honk compared with writing the changes manually

Denominator
:   Manual completion time for the same migration work

Method
:   Unknown

Observation date
:   Unknown

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party) Preserved content.md, lines 70–77

Key observation

Around half of Spotify PRs automated by Fleet Management since mid-2024, including deterministic transformations

Metric · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Spotify

Scope
:   Fleet Management automated pull requests since mid-2024, including deterministic transforms

Denominator
:   All Spotify pull requests

Method
:   Unknown

Observation date
:   2024

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party) Preserved content.md, lines 22–38

#### Architecture and primitives

Sandbox

Honk runs in a constrained Kubernetes container (it does not inherit arbitrary engineer credentials); jobs execute inside Fleet Management / Fleetshift

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)

Harness

Honk: Claude Agent SDK + Spotify's own harness + Kubernetes pods; Honk v2 adds shared sessions, projects, and Chirp orchestration

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)

Model

Claude via the Agent SDK (Claude-centric); the surrounding platform is multi-model

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)
- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

Interfaces

slack, github, cli

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)

Tool access

Limited, deliberate tool surface; trusted CI tools verify changes, while an internal CLI runs formatting and linting through MCP and evaluates diffs with an LLM judge

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)

Knowledge

Backstage/catalog ownership and developer-standardization primitives built over years, exposed via MCP/CLI

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

Credentials

Runs in a constrained container rather than inheriting engineer credentials

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)

Context management

Fleet Management coordinates repo targeting, builds/tests, and PR workflow at scale; Xirp pairs sessions with Portal org context

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

Supporting component

The harness combines build/test tools, formatting and linting, and LLM-based diff evaluation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)

Supporting component

Target thousands of repos, run builds/tests, open and merge PRs at fleet scale

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md) (first-party)

Supporting component

The session/context surface around the agent rather than an autonomous worker itself

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

#### Lessons and interpretation

Lesson

Combine deterministic build, formatting, and lint checks with LLM-based diff evaluation

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)

Lesson

Constrain the agent's environment and tools rather than handing it engineer credentials

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)

Lesson

Invest in org context (Backstage/catalog) before agentic dev accelerates

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)
- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

Lesson

Autonomy without structure fragments into per-engineer configs; shared org context is the multiplier

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for Honk coding task → verified pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source documents automated verification followed by a pull-request workflow that retains human review.

Observation date
:   2025

- Supports [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md) (first-party)

#### Sources

1. [Spotify's Journey with Our Background Coding Agent (Honk)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-1/content.md)  <https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Code with Claude: coding is no longer the constraint (Honk v2)](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-2/content.md)  <https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Xirp - Powered by Spotify Portal](https://xirp.spotify.com/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/spotify-honk-xirp-source-3/content.md)  <https://xirp.spotify.com/> documentation · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#spotify-honk-xirp)

Stripe Background agent

### Minions

Homegrown one-shot coding agents that read work context, locate the right repo/workspace, implement a change end-to-end, and produce a PR for human review.

Coding Code review

work context → merge-ready pull request: Work product review

Operating model, claims & sources

#### Scoped operating models

**work context → merge-ready pull request** Work product review · Level 3

#### Summary and context

Summary

Homegrown one-shot coding agents that read work context, locate the right repo/workspace, implement a change end-to-end, and produce a PR for human review.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)
- Contextualizes [Hacker News discussion of Minions part two](https://news.ycombinator.com/item?id=47086557) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-3/content.md) (community) Preserved content.md, lines 146–158, 190–194
- Contextualizes [Hacker News comment asking for examples and review evidence](https://news.ycombinator.com/item?id=47086907) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-4/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the level of technical detail](https://news.ycombinator.com/item?id=47086953) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-5/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment asking about shipped and maintained output](https://news.ycombinator.com/item?id=47087114) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-6/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the value of pull request counts](https://news.ycombinator.com/item?id=47111453) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-7/content.md) (community) Preserved content.md, lines 10–14

#### Reported metrics

Headline claim

Over 1,300 completely minion-produced PRs merged per week in Part 2, with human review and no human-written code

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Stripe reports merged PR volume without an independent count or measurement window; Part 2 is explicitly later than Part 1.

Reported by
:   Stripe

Scope
:   Weekly merged PRs completely produced by Minions; Part 2 report, up from Part 1

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 12
- Contextualizes [Hacker News discussion of Minions part two](https://news.ycombinator.com/item?id=47086557) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-3/content.md) (community) Preserved content.md, lines 146–158, 190–194
- Contextualizes [Hacker News comment asking for examples and review evidence](https://news.ycombinator.com/item?id=47086907) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-4/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the level of technical detail](https://news.ycombinator.com/item?id=47086953) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-5/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment asking about shipped and maintained output](https://news.ycombinator.com/item?id=47087114) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-6/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the value of pull request counts](https://news.ycombinator.com/item?id=47111453) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-7/content.md) (community) Preserved content.md, lines 10–14

Key observation

Over 1,000 completely minion-produced PRs merged per week in Part 1, with human review and no human-written code

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Stripe reports merged PR volume without an independent count or measurement window; no calendar metric date appears in the capture.

Reported by
:   Stripe

Scope
:   Weekly merged PRs completely produced by Minions; earlier Part 1 report

Denominator
:   Unknown

Method
:   Unknown

Observation date
:   Unknown

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party) Preserved content.md, lines 14
- Contextualizes [Hacker News discussion of Minions part two](https://news.ycombinator.com/item?id=47086557) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-3/content.md) (community) Preserved content.md, lines 146–158, 190–194
- Contextualizes [Hacker News comment asking for examples and review evidence](https://news.ycombinator.com/item?id=47086907) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-4/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the level of technical detail](https://news.ycombinator.com/item?id=47086953) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-5/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment asking about shipped and maintained output](https://news.ycombinator.com/item?id=47087114) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-6/content.md) (community) Preserved content.md, lines 10–14
- Contextualizes [Hacker News comment questioning the value of pull request counts](https://news.ycombinator.com/item?id=47111453) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-7/content.md) (community) Preserved content.md, lines 10–14

#### Architecture and primitives

Sandbox

Pre-warmed AWS EC2 devboxes in the QA environment, isolated from real user data, production services, and arbitrary network egress

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 24–30, 84

Harness

Fork of Block's goose, orchestrated by code-defined blueprints that interleave agent loops with deterministic lint, git, and CI steps

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 38–56

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)

Interfaces

slack, github, cli, web, internal-ui

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party) Preserved content.md, lines 34–48

Tool access

Curated subsets of Toolshed MCP tools for internal documentation, tickets, build status, and code intelligence; security controls constrain destructive actions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 72–84

Knowledge

Repository-scoped rule files shared with human-operated coding agents, plus internal context fetched through MCP

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 64–76

Credentials

Full permissions inside quarantined devboxes; MCP security controls limit destructive actions, and production pull requests require human review

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party) Preserved content.md, lines 40–42, 84

Supporting component

From work context to merge-ready PR in one shot, with human approval

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)
- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party)

#### Lessons and interpretation

Lesson

One-shot end-to-end coding agents work at scale when humans retain review/approval

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)

Lesson

Let the agent locate the right repo/workspace itself rather than pre-scoping it

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)
- Supports [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for work context → merge-ready pull request; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source explicitly states that humans review and approve production pull requests.

Observation date
:   2026-02-20

- Supports [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md) (first-party)

#### Sources

1. [Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-1/content.md)  <https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents> engineering-blog · first-party · Last source verification: 2026-08-31
2. [Minions - Part Two](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-2/content.md)  <https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Hacker News discussion of Minions part two](https://news.ycombinator.com/item?id=47086557) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-3/content.md)  <https://news.ycombinator.com/item?id=47086557> hn-thread · community · Last source verification: 2026-08-31
4. [Hacker News comment asking for examples and review evidence](https://news.ycombinator.com/item?id=47086907) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-4/content.md)  <https://news.ycombinator.com/item?id=47086907> hn-comment · community · Last source verification: 2026-08-31
5. [Hacker News comment questioning the level of technical detail](https://news.ycombinator.com/item?id=47086953) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-5/content.md)  <https://news.ycombinator.com/item?id=47086953> hn-comment · community · Last source verification: 2026-08-31
6. [Hacker News comment asking about shipped and maintained output](https://news.ycombinator.com/item?id=47087114) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-6/content.md)  <https://news.ycombinator.com/item?id=47087114> hn-comment · community · Last source verification: 2026-08-31
7. [Hacker News comment questioning the value of pull request counts](https://news.ycombinator.com/item?id=47111453) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/stripe-minions-source-7/content.md)  <https://news.ycombinator.com/item?id=47111453> hn-comment · community · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#stripe-minions)

Uber Task agent

### Internal coding agent (unnamed)

Uber's internal coding agent, reported by its CTO as producing roughly 1,800 complete code changes per week.

Coding

coding request → complete code change: Unknown

Operating model, claims & sources

#### Scoped operating models

**coding request → complete code change** Unknown · Level unknown

#### Summary and context

Summary

Uber's internal coding agent, reported by its CTO as producing roughly 1,800 complete code changes per week.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary)

#### Reported metrics

Headline claim

~1,800 complete code changes per week (~8% of changes)

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

Reported by
:   Uber

Scope
:   Code changes written entirely by the internal coding agent and human reviewed

Denominator
:   All Uber code changes for the reported 8% share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary) Preserved content.md, lines 24–26

Key observation

~1,800 complete code changes per week (~8% of changes at the time)

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

Reported by
:   Uber

Scope
:   Code changes written entirely by the internal coding agent and human reviewed

Denominator
:   All Uber code changes for the reported 8% share

Method
:   Unknown

Observation date
:   Unknown

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary) Preserved content.md, lines 24–26

Key observation

95% of engineers use AI tools monthly

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

Reported by
:   Uber

Scope
:   Monthly use of AI tools among Uber engineers; not internal-agent-specific adoption

Denominator
:   Uber engineers

Method
:   Unknown

Observation date
:   Unknown

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary) Preserved content.md, lines 18

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary)

Harness

Not specified publicly

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Unclassified for coding request → complete code change; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The available source reports output volume but does not document where human attention returns.

Observation date
:   2026

- Supports [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md) (independent-secondary)

#### Sources

1. [Uber's CTO on AI coding agents (Business Insider)](https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-coding-agent-source-1/content.md)  <https://www.businessinsider.com/uber-cto-ai-coding-agentic-software-engineers-2026-3> news · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#uber-coding-agent)

Uber Background agent

### uReview

An event-driven AI code reviewer for Uber's internal review platform that generates, grades, filters, deduplicates, and posts findings while leaving engineers in control of the reviewed change.

Code review

pull request → filtered AI review findings: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → filtered AI review findings** Work product review · Level 3

#### Summary and context

Summary

An event-driven AI code reviewer for Uber's internal review platform that generates, grades, filters, deduplicates, and posts findings while leaving engineers in control of the reviewed change.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Introduction; How It Works

#### Reported metrics

Headline claim

Uber's introduction reports reviews of over 90% of approximately 65,000 weekly diffs, with over 75% usefulness and over 65% addressed comments; a later paragraph says 65,000 diffs per month

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The opening paragraph reports approximately 65,000 weekly diffs, but the cost discussion says 65,000 per month. These conflicting periods remain unresolved; neither is independently verified.

Reported by
:   Uber

Scope
:   Introduction's reported weekly diff coverage, plus comment usefulness/addressed rates; later paragraph's monthly period conflicts and remains unresolved

Denominator
:   Introduction reports approximately 65,000 weekly diffs; cost paragraph says monthly. Usefulness covers rated comments; addressed rate covers posted comments

Method
:   Production coverage, developer ratings, and automatic addressed-comment detection

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 34, 98
- Contradicts [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 120 (65,000 per month, versus weekly in line 34)

Key observation

Introduction reports reviews of over 90% of approximately 65,000 weekly diffs; cost discussion instead says 65,000 diffs per month

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The opening paragraph reports approximately 65,000 weekly diffs, but the cost discussion says 65,000 per month. These conflicting periods remain unresolved; neither is independently verified.

Reported by
:   Uber

Scope
:   Introduction's reported weekly diffs analyzed; monthly period in the cost paragraph conflicts and remains unresolved

Denominator
:   Approximately 65,000 weekly diffs according to the introduction; same volume described as monthly in the cost paragraph

Method
:   Unknown

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 34
- Contradicts [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 120 (65,000 per month, versus weekly in line 34)

Key observation

Over 75% of comments rated useful by engineers who interact with the tool

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Comments rated useful by engineers who provide feedback

Denominator
:   Comments with engineer interaction

Method
:   Useful / Not Useful rating links

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 76, 98

Key observation

Over 65% of posted comments addressed in the same changeset

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Posted comments considered addressed in the same changeset

Denominator
:   Posted comments

Method
:   Five reruns on the final commit and semantic-similarity matching

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 82, 98

Key observation

Median review latency of 4 minutes across all six Uber monorepos

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Reviews across all six Uber monorepos

Denominator
:   Unknown

Method
:   Production latency telemetry

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 94

Key observation

Approximately 1,500 developer hours reportedly saved per week, based on an assumed 10-minute second review per processed commit

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The source estimates about 1,500 hours using over 10,000 commits and a 10-minute assumption; the rounded figures do not arithmetically reconcile exactly and are not observed time savings.

Reported by
:   Uber

Scope
:   Processed commits excluding configuration files; modeled second-review time savings

Denominator
:   Over 10,000 commits per week

Method
:   Processed commits multiplied by an assumed 10 minutes for a second human review

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 104

#### Architecture and primitives

Harness

A prompt-chained pipeline separates comment generation, confidence grading, validation, semantic deduplication, and category filtering; three specialized assistants were in operation when published

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) How It Works; Comment Generation; Post-Processing

Model

Periodic benchmark evaluation; Claude 4 Sonnet as generator with o4-mini-high as grader was the highest-F1 reported pairing

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Empirical Model Evaluation

Interfaces

internal-ui, ci

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Delivery and Feedback Collection; Impact and Evaluation

Tool access

Reviews eligible code in Uber's six monorepos across Go, Java, Android, iOS, TypeScript, and Python; richer internal artifacts were not yet connected when published

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Impact and Evaluation; Better at Catching Bugs than Assessing System Design

Knowledge

Surrounding source context plus a shared registry of Uber-specific coding and style rules

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Ingestion and Preprocessing; Comment Generation by Specialized Assistants

Context management

Comments and metadata are streamed through Kafka to Hive for feedback analysis, experiments, and operational dashboards

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Delivery and Feedback Collection

Supporting component

Standard, best-practices, and AppSec reviewers generate findings for different issue classes

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Generation by Specialized Assistants

Supporting component

Confidence grading, semantic deduplication, and historically low-value category suppression reduce noise

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Post-Processing and Quality Filtering

Supporting component

Developer ratings, addressed-comment detection, and a curated benchmark tune prompts, thresholds, and models

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Evaluation and Continuous Improvement

#### Lessons and interpretation

Lesson

Prefer fewer high-confidence findings over high comment volume

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and documents the associated mechanisms.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Precision Is More Valuable than Volume

Lesson

Combine prompts with deterministic filtering, deduplication, evaluation, and feedback instrumentation

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and documents the pipeline.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Guardrails Are Just as Important as Prompts

Lesson

Roll out gradually by team and assistant while tracking precision, recall, usefulness, and false positives

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and describes the rollout telemetry.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Trust Grows with Gradual Rollout

#### Operating model evidence

Operating model assessment

Level 3 for pull request → filtered AI review findings; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes AI-generated review findings while engineers remain in control of the change.

Observation date
:   2025-08-12

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party)

#### Sources

1. [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md)  <https://www.uber.com/us/en/blog/ureview/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#uber-ureview)

WorkOS Platform

### Project Horizon

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

Y Combinator Platform

### Internal agent infrastructure

Internal agent infrastructure and own harnesses built from the ground up, framed as making AI the operating system the whole organization runs on.

Coding Ops

internal request → agent-assisted organizational work: Unknown

Operating model, claims & sources

#### Scoped operating models

**internal request → agent-assisted organizational work** Unknown · Level unknown

#### Summary and context

Summary

Internal agent infrastructure and own harnesses built from the ground up, framed as making AI the operating system the whole organization runs on.

Fact · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

Harness

Own harnesses built from the ground up for internal AI use

Fact · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Don't add AI as a feature; make it the operating system the whole organization runs on

Inference · Catalog judgment · Low confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

Lesson

Build the harness and surrounding infra in-house rather than bolting onto a hosted agent

Inference · Catalog judgment · Low confidence

Evidence and qualifications

Confidence reason
:   Only limited public evidence supports this claim.

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Unclassified for internal request → agent-assisted organizational work; human attention boundary: unknown.

Inference · Catalog judgment · Unverified confidence

Evidence and qualifications

Confidence reason
:   The source describes internal agent infrastructure but not a sufficiently specific human attention boundary.

Observation date
:   2026

- Supports [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md) (first-party)

#### Sources

1. [Inside YC's AI Playbook (Lightcone podcast, with Pete Koomen)](https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/ycombinator-agent-infra-source-1/content.md)  <https://www.ycombinator.com/library/Qh-inside-yc-s-ai-playbook> podcast · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#ycombinator-agent-infra)

Zup Task agent

### CodeGen

A research-documented internal coding agent where constrained editing tools and layered safety controls mattered more than prompt tweaks.

Coding

constrained coding task → human-supervised edit: Continuous steering

Operating model, claims & sources

#### Scoped operating models

**constrained coding task → human-supervised edit** Continuous steering · Level 2

#### Summary and context

Summary

A research-documented internal coding agent where constrained editing tools and layered safety controls mattered more than prompt tweaks.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

#### Architecture and primitives

Harness

Constrained editing tools; state-management concerns; progressive levels of human oversight

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Model

Not specified (see paper)

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Tool access

Constrained editing tools rather than free-form code generation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Credentials

Layered safety controls

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Supporting component

Tools that limit what the agent can change, vs. unconstrained generation

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Supporting component

Levels of human review that increase trust over time

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Targeted tool design and layered safety controls matter more than prompt tweaks

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

Lesson

Progressive levels of human oversight help build trust before granting autonomy

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 2 for constrained coding task → human-supervised edit; human attention boundary: continuous-steering.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The research source describes progressive human oversight but does not establish background delegation.

Observation date
:   2026

- Supports [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md) (first-party)

#### Sources

1. [Building an Internal Coding Agent at Zup](https://arxiv.org/abs/2604.09805) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/zup-codegen-source-1/content.md)  <https://arxiv.org/abs/2604.09805> paper · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#zup-codegen)
