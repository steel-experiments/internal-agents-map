---
title: More comments can mean more work
description: How Uber and HubSpot filter agent review comments. An observation on useful findings and the work required from human reviewers.
eyebrow: 02 / Human attention
lede: A review agent also creates work for its reader.
summary: Uber and HubSpot check review comments before engineers see them.
readingTime: 2 min read
order: 2
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - uber-ureview
  - hubspot-sidekick
sources:
  - id: uber
    title: 'Uber: uReview'
    url: https://www.uber.com/us/en/blog/ureview/
    note: Quality filters, duplicate removal, and feedback from engineers.
  - id: hubspot
    title: 'HubSpot: Sidekick code review'
    url: https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution
    note: The change to Aviator and the judge agent.
---

<section aria-labelledby="what-gets-published">

## What gets published

Uber found that a single prompt produced false alarms and correct comments with little practical value. uReview now grades confidence, removes duplicates, and suppresses categories that engineers rarely use. Those decisions reduce the set of findings an engineer sees. [[1]](#source-uber)

HubSpot also found that a faster reviewer could still produce poor comments. It added a judge agent before publication. That supplies another assessment, with its own potential errors, rather than independent confirmation that a finding is correct. [[2]](#source-hubspot)

Both teams filter comments, but their reports describe different checks. Neither comment volume nor an added judge establishes how much review work the system saves.

</section>

<section aria-labelledby="the-cost-of-a-stricter-filter">

## The cost of a stricter filter

A published comment asks an engineer to inspect evidence, decide whether to act, and resolve or dismiss the finding. A useful comment can save later debugging; a weak one can consume more time than it saves.

Suppressing a comment also has a cost when it hides a real defect. Uber evaluates precision and recall against annotated commits, then tracks feedback and whether comments were addressed. Those measures answer different questions: benchmark recall concerns known issues, while addressed comments describe use of the published output. [[1]](#source-uber)

Our reading is that a filter needs evidence from both sides of the publication decision. Reviewing a sample of discarded candidates could reveal missed defects; timing human follow-up could expose expensive comments. These are evaluation proposals. The reports do not supply a complete measurement of downstream reviewer time or the defects that escaped both automated and human review.

</section>
