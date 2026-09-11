Source: https://internal-agents.com/notes/test-on-your-work.html

[← Notes](https://internal-agents.com/notes.html)

07 / Evaluation

# Test the agent on your own work

Past tasks and failures can become repeatable checks.

11 September 2026 · 2 min read

## What the teams report

Databricks builds benchmark tasks from actual code changes. It removes solution details from task descriptions and keeps relevant tests separate. People check each sample. [[1]](https://internal-agents.com/notes/test-on-your-work.html#source-1)

The team also revises tests when they reject a valid alternative solution. A useful test must check the result without requiring the original implementation. [[1]](https://internal-agents.com/notes/test-on-your-work.html#source-1)

Uber evaluates uReview with a curated benchmark and feedback from engineers. These checks help the team adjust prompts, thresholds, and models. [[2]](https://internal-agents.com/notes/test-on-your-work.html#source-2)

> “every bug we find in production becomes a new scenario”

Databricks, on its coSTAR evaluation method. [[3]](https://internal-agents.com/notes/test-on-your-work.html#source-3)

01 **Past task** Remove the solution hints

02 **Agent run** Capture the result

03 **Evaluation** Check the required properties

A new failure can become another test case.

Our illustration of a possible evaluation cycle. It combines ideas from the reports, not one shared implementation.

Our observation

## The test set needs review too

A test case needs a clear task, an initial state, and a way to assess the result. Past work can supply these parts.

Databricks also checks model judges against human judgments in coSTAR. Its method covers several kinds of agents, including internal engineering workflows. [[3]](https://internal-agents.com/notes/test-on-your-work.html#source-3)

Past cases cannot cover every future failure. A strong result on one team’s tasks may not transfer to another team.

**A question for your build** Which past failure must the next version avoid?

## Sources

1. [Databricks: Benchmarking coding agents](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) Task construction, solution hints, and manual test review.
2. [Uber: uReview](https://www.uber.com/us/en/blog/ureview/) Evaluation and feedback from engineers.
3. [Databricks: coSTAR](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) Failure scenarios and checks on model judges.

[Databricks in the catalog](https://internal-agents.com/index.html#databricks-costar) [Uber in the catalog](https://internal-agents.com/index.html#uber-ureview)

[All notes](https://internal-agents.com/notes.html) [Read: When should an agent stop? →](https://internal-agents.com/notes/stop-a-run.html)
