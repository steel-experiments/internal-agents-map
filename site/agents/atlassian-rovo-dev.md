Source: https://internal-agents.com/#atlassian-rovo-dev

Atlassian Task agent

# Rovo Dev (RovoDev)

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
