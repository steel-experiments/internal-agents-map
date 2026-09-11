Source: https://internal-agents.com/#coinbase-forge-mux

Coinbase Agent system

# Forge / Mux

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
