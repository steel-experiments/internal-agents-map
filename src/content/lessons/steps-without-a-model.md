---
title: Some steps do not need a model
description: Code can control a step that must follow a fixed rule.
eyebrow: 06 / Workflow control
lede: Code can control a step that must follow a fixed rule.
summary: Code can control a step that must follow a fixed rule.
readingTime: 2 min read
order: 6
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - stripe-minions
  - dropbox-nova
  - posthog-stamphog
sources:
  - id: '1'
    title: 'Stripe: Minions, part 2'
    url: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
    note: Blueprint nodes that run without a model.
  - id: '2'
    title: 'Dropbox: Introducing Nova'
    url: https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents
    note: Publication and test control outside the agent.
  - id: '3'
    title: 'PostHog: PR approval agent'
    url: https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent
    note: Pinned implementation with authoritative safety gates.
---

<section aria-labelledby="who-controls-the-next-step">

## Who controls the next step?

Stripe's blueprints interleave agent work with ordinary code. The agent can decide how to implement a task or repair a failure. Configured linters and the push step run as deterministic nodes. Their execution does not depend on the model remembering to request them. [[1]](#source-1)

Dropbox draws another boundary around Nova: the agent changes one branch, while surrounding workflows retain publication control. Those workflows trigger continuous integration (CI) and call the agent back when failures need repair. Dropbox reports that letting agents manage this themselves caused long waits or validation against the wrong tests. [[2]](#source-2)

</section>

<section aria-labelledby="an-approval-rule-the-model-cannot-relax">

## An approval rule the model cannot relax

PostHog's StampHog checks pull-request eligibility with fixed gates. If a gate rejects the request, the model cannot override it. If the request is eligible, the model can still impose a stricter decision. A backend error or pending reviewer-bot work withholds approval and preserves the trigger for a later retry. [[3]](#source-3)

The cases assign different responsibilities to code: running a required step, owning publication, or limiting an approval decision. An eligible StampHog request can still be refused by the model; a Nova validation result returns control to its surrounding workflow.

Our interpretation is that a passed check needs a named scope. A formatter can establish formatting; a test can exercise the behavior it covers; an eligibility rule can permit further review. None of those results alone grants permission to publish. That permission belongs to the workflow's separate approval and publication controls.

</section>
