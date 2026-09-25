---
title: Should one agent search and a different one check?
description: DoorDash changed how its agents divide a code review. An observation on shared context, investigation, and verification.
eyebrow: 03 / Agent roles
lede: DoorDash gives a scout the search and two reviewers the verification.
summary: DoorDash changed how its agents divide a code review. Each design exposed a different problem.
readingTime: 2 min read
order: 3
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - doordash-code-review
sources:
  - id: doordash
    title: 'DoorDash: How we built an AI code reviewer'
    url: https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/
    note: The “How we got here” section describes all three designs.
---

<section aria-labelledby="two-designs-that-missed-findings">

## Two designs that missed findings

DoorDash first assigned code review to specialists for security, tests, performance, and other areas. They found local mistakes but missed changes that crossed system boundaries. No specialist held the wider context.

The second version gave two general reviewers the whole change. They could see those relationships, but each had too much to investigate in one session. Some real findings were lost among the work of reading, tracing, and checking. [[1]](#source-doordash)

</section>

<section aria-labelledby="a-shared-list-of-leads">

## A shared list of leads

The third version puts a scout before the two reviewers. It identifies suspicious changes and produces investigation leads. The reviewers trace those leads, verify the evidence, and drop candidates that do not hold up. [[1]](#source-doordash)

<figure class="lesson-diagram">
  <div class="lesson-node"><strong>Scout: candidate issues</strong><small>Read the diff and describe what needs investigation.</small></div>
  <p class="lesson-diagram-tail">The leads go to two reviewers working in parallel.</p>
  <div class="lesson-reviewers">
    <div class="lesson-node"><strong>Reviewer A</strong><small>Investigate leads and verify findings.</small></div>
    <div class="lesson-node"><strong>Reviewer B</strong><small>Investigate leads and verify findings.</small></div>
  </div>
  <figcaption>Our illustration of the reported handoff. The scout's output is a set of leads, not verified bugs.</figcaption>
</figure>

This gives the handoff a specific work product. A reviewer can examine a candidate and its context without treating the scout's suspicion as a conclusion. The distinction matters because another agent's confidence is not evidence that a bug exists.

DoorDash credits the change with improving its reviewer. The version history, however, does not isolate the effect of the scout from other changes. It supplies a concrete response to overloaded reviewers, without measuring whether this arrangement is better or cheaper for a different review workload.

</section>
