Source: https://internal-agents.com/#airbnb-airchat

Airbnb Platform

# Airchat (airchat-cli)

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
