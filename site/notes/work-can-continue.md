Source: https://internal-agents.com/notes/work-can-continue.html

[← Notes](https://internal-agents.com/notes.html)

04 / Work state

# The worker can stop. The work can continue.

A new worker can continue from a saved record.

11 September 2026 · 2 min read

## What the teams report

Shopify keeps the session record in Postgres. A worker can stop, and a new worker can read the same history. The session keeps its identity. [[1]](https://internal-agents.com/notes/work-can-continue.html#source-1)

Sentry’s Junior pauses before a serverless timeout. It places a continuation task in a queue so another run can continue the work. [[2]](https://internal-agents.com/notes/work-can-continue.html#source-2)

Sierra uses checkpoints and ordered events to restore a runner after it stops for a period of inactivity. [[3]](https://internal-agents.com/notes/work-can-continue.html#source-3)

> “Cells die, sandboxes die, machines die. The conversation doesn't.”

Shopify, on session survival. [[1]](https://internal-agents.com/notes/work-can-continue.html#source-1)

01 **Worker A** Reads and updates the record

02 **Worker stops** Saved state remains

03 **Worker B** Reads the saved state

The saved record exists outside the worker.

Our illustration of work that survives a worker stop. Each team saves and restores different state.

Our observation

## A saved record needs a clear scope

A conversation, a file, and an action in another system are different kinds of state. Each needs a defined recovery method.

Conversation history alone does not establish which actions completed. A recovery design also needs to account for work already done.

These cases show ways to continue a task. They do not establish that every file or action survives every failure.

**A question for your build** What must the next worker know before it can continue?

## Sources

1. [Shopify: Under the River](https://shopify.engineering/under-the-river) The session record and disposable workers.
2. [Sentry: Building an intern](https://cra.mr/building-an-intern/) Pauses and continuation tasks before timeouts.
3. [Sierra: Agency](https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents) Checkpoints and event replay after inactivity.

[Shopify in the catalog](https://internal-agents.com/index.html#shopify-internal-agents) [Sentry in the catalog](https://internal-agents.com/index.html#sentry-junior) [Sierra in the catalog](https://internal-agents.com/index.html#sierra-pinecone)

[All notes](https://internal-agents.com/notes.html) [Next: Load tools when the task needs them →](https://internal-agents.com/notes/load-tools.html)
