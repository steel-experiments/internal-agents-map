---
title: Test the agent on your own work
description: Past tasks and failures can become repeatable checks.
eyebrow: 07 / Evaluation
lede: Past tasks and failures can become repeatable checks.
summary: Past tasks and failures can become repeatable checks.
readingTime: 2 min read
order: 7
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - databricks-costar
  - uber-ureview
sources:
  - id: '1'
    title: 'Databricks: Benchmarking coding agents'
    url: https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase
    note: Task construction, solution hints, and manual test review.
  - id: '2'
    title: 'Uber: uReview'
    url: https://www.uber.com/us/en/blog/ureview/
    note: Evaluation and feedback from engineers.
  - id: '3'
    title: 'Databricks: coSTAR'
    url: https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things
    note: Failure scenarios and checks on model judges.
---

<section aria-labelledby="reconstruct-the-task-without-the-answer">

## Reconstruct the task without the answer

Databricks builds coding tasks from actual pull requests. It rewrites the task description around the desired outcome, removes explanations of the historical solution, and keeps the relevant tests separate. People check each candidate sample. Without that separation, a successful run could reflect access to the answer rather than the ability to solve the task. [[1]](#source-1)

The original tests also need inspection. Databricks found tests that rejected valid alternative implementations and rewrote them by hand. A benchmark can therefore fail in either direction: solution hints make it too easy, while tests tied to one implementation reject correct work. [[1]](#source-1)

</section>

<section aria-labelledby="review-the-judge-as-well-as-the-agent">

## Review the judge as well as the agent

In coSTAR, Databricks records agent traces and scores them with model judges. A separate loop compares those judges with human assessments and refines them against a curated set of examples. The team explicitly reports continuing costs for human labeling and recalibration, plus failures that existing judges do not cover. [[3]](#source-3)

Uber's uReview evaluates a different output: review findings against annotated commits, supplemented by engineer feedback. Its precision and recall concern detected issues; Databricks' coding benchmark concerns completed code changes. Their scores cannot be substituted for each other. [[2]](#source-2)

Our reading is that a reusable past task needs a preserved starting state, a clear request, and an assessment that accepts valid alternatives. Human agreement on one set of examples can expose judge errors, but it cannot establish coverage of unseen failures. coSTAR adds production failures as new scenarios precisely because the original suite remains incomplete. [[3]](#source-3)

</section>
