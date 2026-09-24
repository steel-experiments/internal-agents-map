---
title: The worker can stop. The work can continue.
description: A new worker can continue from a saved record.
eyebrow: 04 / Work state
lede: A new worker can continue from a saved record.
summary: A new worker can continue from a saved record.
readingTime: 2 min read
order: 4
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - shopify-internal-agents
  - sentry-junior
  - sierra-pinecone
sources:
  - id: '1'
    title: 'Shopify: Under the River'
    url: https://shopify.engineering/under-the-river
    note: The session record and disposable workers.
  - id: '2'
    title: 'Sentry: Building an intern'
    url: https://cra.mr/building-an-intern/
    note: Pauses and continuation tasks before timeouts.
  - id: '3'
    title: 'Sierra: Agency'
    url: https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents
    note: Checkpoints and event replay after inactivity.
---

<section aria-labelledby="what-the-next-worker-reads">

## What the next worker reads

Shopify's Aquifer keeps session identity and an append-only event log in Postgres. An idle worker can exit; a fresh worker reads the same conversation when the next interaction arrives. [[1]](#source-1)

<figure class="lesson-diagram">
  <div class="lesson-reviewers">
    <div class="lesson-node"><strong>Worker A</strong><small>Records events, then exits.</small></div>
    <div class="lesson-node"><strong>Worker B</strong><small>Reads the session when work resumes.</small></div>
  </div>
  <div class="lesson-shared-state"><strong>Shared Postgres session</strong><span>The identity and event log remain outside either worker.</span></div>
  <figcaption>Our illustration of Aquifer's reported separation of workers and session state.</figcaption>
</figure>

Sentry's Junior pauses near a serverless deadline and queues a continuation task. Its intended pause point is the end of a tool result. This describes task continuation; it does not document recovery of every local file. [[2]](#source-2)

Sierra's Agency restores a hibernated runner by replaying ordered events from its last checkpoint. The application-specific runner decides what goes into the checkpoint and subsequent events. That choice determines what replay can restore. [[3]](#source-3)

</section>

<section aria-labelledby="conversation-files-and-effects">

## Conversation, files, and effects

These mechanisms preserve different records. A restored conversation does not imply that a workspace file survived. A restored file does not establish whether an earlier request completed in another system.

Our inference is that recovery needs to identify which of these records the next worker can trust. For an external action, a receipt or an idempotency mechanism may be needed to distinguish a completed request from one that needs retrying. The reports above do not establish that their session recovery provides this property for every connected tool.

</section>
