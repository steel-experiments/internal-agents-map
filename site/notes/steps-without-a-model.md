Source: https://internal-agents.com/notes/steps-without-a-model.html

[← Notes](https://internal-agents.com/notes.html)

06 / Workflow control

# Some steps do not need a model

Code can control a step that must follow a fixed rule.

11 September 2026 · 2 min read

## What the teams report

Stripe’s blueprints combine model-directed work with ordinary code. A model can implement a task, while code runs configured checks and pushes changes. [[1]](https://internal-agents.com/notes/steps-without-a-model.html#source-1)

Dropbox keeps code publication outside the agent. Its workflows start continuous integration (CI) checks and return failures to the agent for repair. [[2]](https://internal-agents.com/notes/steps-without-a-model.html#source-2)

PostHog checks whether a pull request is eligible for agent approval. Its fixed gates remain authoritative. The model can make approval stricter but cannot relax a gate. [[3]](https://internal-agents.com/notes/steps-without-a-model.html#source-3)

> “not every step belongs inside the agent loop.”

Dropbox, on control of the workflow. [[2]](https://internal-agents.com/notes/steps-without-a-model.html#source-2)

01 **Model task** Propose a result

02 **Fixed check** Apply a known rule

03 **Next step** Proceed or return a failure

Our illustration of a model task followed by code-controlled steps. The cases use different checks and actions.

Our observation

## The rule and the judgment can stay separate

A known rule can have a predictable check. The model can handle the parts that require interpretation.

This separation can also make failures easier to inspect. The record can show which rule blocked the next step.

A passing check proves only what that check covers. It does not establish that the complete result is correct.

**A question for your build** Which step must happen the same way on every run?

## Sources

1. [Stripe: Minions, part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) Blueprint nodes that run without a model.
2. [Dropbox: Introducing Nova](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) Publication and test control outside the agent.
3. [PostHog: PR approval agent](https://github.com/PostHog/posthog/tree/988c9031bb93c74bafcdfb670c01497c79a4f644/tools/pr-approval-agent) Pinned implementation with authoritative safety gates.

[Stripe in the catalog](https://internal-agents.com/index.html#stripe-minions) [Dropbox in the catalog](https://internal-agents.com/index.html#dropbox-nova) [PostHog in the catalog](https://internal-agents.com/index.html#posthog-stamphog)

[All notes](https://internal-agents.com/notes.html) [Next: Test the agent on your own work →](https://internal-agents.com/notes/test-on-your-work.html)
