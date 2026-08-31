> Archived source snapshot  
> Source ID: `flex-investigation-agent-source-1`  
> Original URL: <https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments>  
> Final URL: <https://www.withflex.com/blog/the-flex-ai-investigation-agent-for-hsa-fsa-payments>  
> Title: The Flex AI Investigation Agent for HSA/FSA Payments  
> Captured at: `2026-08-31T17:42:35Z`

---

We built a Slack agent that can trace a transaction end to end—and, when it finds a bug, open a pull request with a proposed fix.

 Varsha Parthasarathy

Engineering Lead - Merchant

## AI at Flex, Part 1: The Internal Investigation Agent

We built a Slack agent that can trace a transaction end to end—and, when it finds a bug, open a pull request with a proposed fix.

*This is Part 1 of a three-part series on how Flex is using AI to improve HSA & FSA payment operations. In this post, we cover the internal investigation agent our team uses every day. Part 2 will cover how we’re bringing the same capabilities to merchant partners through a self-serve dashboard. Part 3 will cover what happens when the agent moves beyond investigation and starts taking action.*

Here at Flex, we process thousands of HSA and FSA payments every day across hundreds of merchant partners. When something goes wrong—a payment fails, a refund looks wrong, [a webhook never fires](https://www.withflex.com/blog/secure-flex-checkout-using-webhooks) —our support, operations, and engineering teams have to reconstruct the full lifecycle of the transaction across several systems: our database, payment processor, logs, error tracking, source code, and usually a few Slack threads.

That workflow used to be slow and manual. Even a routine investigation could take 20 minutes of engineering time.

So we built an internal AI investigation agent that lives in Slack to compress that work into seconds. Give it a customer email, order number, transaction ID, error message, or engineering ticket, and it traces the issue end to end, then returns a plain-English explanation with the supporting details.

We realized the same system could do more than just explain what happened. In the right cases, it could identify the root cause of a bug, trace it to the relevant code path, and open a pull request with a proposed fix for human review.

I’m [Varsha Parthasarathy](https://www.linkedin.com/in/varshaparthasarathy-5b488526), Founding Software Engineer and Lead, Merchant Engineering at Flex, and I’m here to explain exactly how we did this, and why it’s so beneficial to the world of HSA/FSA payments, and the merchants who accept them.

## What the AI investigation agent does

The agent handles the kinds of questions that show up constantly in payment operations and support:

- *What happened with this order?*
- *Why was this HSA/FSA card declined?*
- *Did the customer’s consultation get approved?*
- *Was the partner notified?*
- *Is this a real bug or a data issue?*
- *What caused this error, and where in the codebase does it originate?*

The input can be almost anything: a customer email, order number, transaction ID, refund ID, error string, or ticket number. From there, the agent resolves the relevant records and follows the trail across systems.

It does not stop at a single lookup. It reconstructs the full lifecycle of the transaction: what was purchased, how it was paid, whether a consultation happened, whether refunds or disputes were issued, whether partner webhooks were delivered, and whether payouts were created. When something looks wrong, it keeps digging—pulling provider responses, checking real-time payment state, searching logs, or inspecting error traces.

The interface is conversational. Investigations rarely end after the first answer, so team members can ask follow-up questions in the same Slack thread and the agent continues with full context.

## How the investigation loop works

At the core is a tool-calling agent. We gave the model access to a set of narrowly scoped tools, each tied to a system or workflow: resolving identifiers, querying transaction data, fetching charge details from our payment infrastructure, searching logs, reading Sentry issues, creating Linear tickets, and inspecting source code in GitHub.

The model decides which tools to call, in what order, based on what it finds.

That is the key architectural choice: we did not build a giant hand-written decision tree for every failure mode. Instead, we focused on designing good tools with clear interfaces, useful defaults, and clean outputs, then let the model reason about the next step in the investigation.

That approach made the system much more flexible in practice. The same agent can handle refunds, disputes, split-cart payments, failed consultations, webhook issues, and edge cases we never explicitly programmed for.

![How the investigation loop works](https://www.withflex.com/vc-ap-e1bdab/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fnspg2eed%2Fproduction%2F7987c0cfa75f1b3e1fe9fcfd979eb8a993cb7284-700x341.png%3Fw%3D1920%26q%3D100%26auto%3Dformat&w=3840&q=75)

How the investigation loop works

## Four investigation paths

Most requests fall into one of four paths:

### 1\. Transaction investigation

This path starts with a universal resolver that accepts almost any identifier—email, order number, transaction ID—and maps it to the relevant records. From there, the agent walks the full lifecycle of the transaction across payments, refunds, consultations, webhooks, payouts, and related entities.

### 2\. Error debugging

This is where the system becomes especially useful. The agent searches error tracking for matching issues, pulls stack traces and event metadata, cross-references them with production logs, and reads the source code around the failing path to identify the likely root cause.

### 3\. Ticket investigation

For engineering tickets, the agent first determines what kind of problem it is. Some tickets describe real bugs, while others are data anomalies, partner configuration issues, or support questions framed like bugs. The agent routes the investigation accordingly.

### 4\. General product and system questions

Not every request is tied to a single transaction. The same tools also let the agent answer questions about feature flags, partner configurations, product behavior, and higher-level operational metrics.

## From error report to pull request

The most interesting extension of the system was not better lookup—it was closing the loop on debugging.

When the agent investigates a bug, it can do more than summarize the failure. In high-confidence cases, it can prepare a proposed fix.

The flow looks like this:

- Search error tracking for the issue and collect the stack trace, events, and tags
- Search production logs around the relevant time window for more context
- Read the source code in the affected path to verify the failure mode
- Assess confidence before taking any action
![The Flex AI Investigation Agent for HSA/FSA Payments](https://www.withflex.com/vc-ap-e1bdab/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fnspg2eed%2Fproduction%2Fcda906d52846bdeb04bb536f93ec61ceef927365-700x280.png%3Fw%3D1920%26q%3D100%26auto%3Dformat&w=3840&q=75)

The Flex AI Investigation Agent for HSA/FSA Payments

### That confidence assessment is the gate.

#### High confidence

The agent has identified a specific bug, verified the relevant code path, and found a clear fix. In that case, it creates an engineering ticket and spawns a coding sub-agent that clones the repository, applies the fix, runs the validation pipeline, and opens a pull request. The results are posted back into the Slack thread for review.

#### Medium confidence

The agent has a plausible root cause, but not enough certainty to change code. It creates a ticket with its findings and leaves the fix to a human engineer.

#### Low confidence

The agent found symptoms, but not a defensible root cause. It reports the investigation results and stops there.

That distinction is what makes the workflow safe. The agent never merges its own code, never deploys to production, and never acts without a human review point. But by the time an engineer opens the pull request, the investigation, root-cause analysis, ticket creation, and first-pass fix may already be done.

What used to require an hour of context switching often becomes a few minutes of review.

![The Flex AI Investigation Agent for HSA/FSA Payments](https://www.withflex.com/vc-ap-e1bdab/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fnspg2eed%2Fproduction%2F7c8675b7854650ced26e2a6a8ec28fcbc4299729-700x317.png%3Fw%3D1920%26q%3D100%26auto%3Dformat&w=3840&q=75)

The Flex AI Investigation Agent for HSA/FSA Payments

## Built for multi-tenant isolation from day one

Because Flex is a multi-tenant platform, data isolation was a design requirement, not a cleanup task.

When the agent runs in a partner-specific Slack channel, every query is scoped to that partner’s data. More importantly, that isolation is enforced structurally. We do not rely on the model to “remember” to filter results correctly.

Every record returned through the investigation layer passes through ownership verification before it reaches the model. If a record does not belong to the scoped partner, it is never returned.

We also disable entire classes of tools in partner-facing contexts. Internal-only capabilities—error tracking, log search, source code access, analytics, and real-time payment lookups—are unavailable outside internal channels. Internal channels remain unrestricted for the operations and engineering teams that need them.

**That separation turned out to be one of the most important architectural decisions in the system.**

## Connected to the full stack

A transaction investigation usually spans multiple systems, so the agent had to do the same. Today it integrates with:

- **PostgreSQL** (read-only replica) — transactions, orders, customers, products, subscriptions, consultations, webhooks, and payouts
- **Payment infrastructure** — real-time payment state, charge outcomes, risk signals, decline codes, and webhook events
- **CloudWatch Logs** — time-windowed production log search with automatic credential redaction
- **Sentry** — issue search, stack traces, and event context
- **Linear** — reading and creating engineering tickets
- **GitHub** — source code search, code inspection, and pull request creation
- **PostHog** — analytics and behavioral data
- **Slack** — user interface and thread-based follow-up

## Serverless, stateless, and auditable

The system runs as a serverless application on [Modal](https://modal.com/).

Slack sends a request, we acknowledge it immediately, and then spawn a background function to run the investigation. Most runs finish in around 10 to 15 seconds. That model lets us avoid persistent servers and long-lived connections while still supporting an interactive workflow in Slack.

We log every investigation in two streams:

1. A main audit log with the original query, tools used, timing, and final response
2. A detailed trace log with each reasoning step and tool execution

The audit log gives us an operational record. The trace log gives us the raw material to improve the system: which tools were called, where the agent got stuck, which paths produced useful answers, and where we need better tool design.

## Security and guardrails

Giving an AI system access to production-adjacent data—and the ability to open pull requests—requires hard boundaries.

We built the agent around a few rules:

- **Read-only database access** —Transaction queries go through a replica that cannot modify production data.
- **Request verification** — Every Slack request is verified with HMAC-SHA256 before we process it.
- **Partner isolation** — In partner contexts, all data access is scoped and ownership-verified.
- **Human review for actions** — The agent can create tickets and pull requests, but it does not merge code or modify production systems.
- **Validation before PR creation** — The coding sub-agent runs compile checks, linting, formatting, and tests before opening a PR.
- **Sensitive data redaction** — Tokens, API keys, and credentials are automatically stripped from log results.

**Strict timeouts and conversation limits** — Investigations do not run indefinitely, and thread depth is capped.

## What we learned building V0

A few lessons stood out while building the first version.

### 1\. Tool design mattered more than prompt design

We spent more time defining tool interfaces, defaults, and response shapes than tuning prompts. Clear tools produced much better investigations than clever prompt wording ever did.

### 2\. Isolation has to be structural, not behavioral

Telling a model to only show a partner’s data is not a control plane. The model should never see data it is not allowed to access in the first place.

### 3\. Start read-only

Read-only access made the initial rollout safe enough to use broadly. That gave us time to build trust in the investigation layer before allowing the system to take bounded actions like ticket creation or pull request generation.

### 4\. Confidence scoring is what makes automation practical

Not every investigation should end in an action. The system became much more useful once it could distinguish between high-confidence diagnoses, partial leads, and inconclusive results—and behave differently in each case.

### 5\. Validation pipelines matter

Automatically running formatting, linting, compile checks, and tests before opening a PR dramatically improved trust in the fixes the agent proposed. Engineers are much more willing to review machine-generated changes when the basics already pass.

**Coming next:** The internal agent solved a real problem for our operations and engineering teams. But our merchant partners want the same visibility into their transactions without filing a support ticket or waiting for us to investigate manually. In Part 2, we’ll cover how we’re adapting this system into a self-serve investigation experience for partners—using the same core ideas, but with partner-safe tooling and tighter tenant boundaries.

## Our internal AI investigation agent was built with:

- **Anthropic:** tool-calling investigation loop and coding sub-agent
- **Modal:** serverless execution, background jobs, and persistent storage
- **PostgreSQL:** read-only transaction data
- **Payment infrastructure:** real-time payment lookups
- **Sentry:** error tracking and stack trace analysis
- **CloudWatch Logs:** production log search
- **Linear:** ticket workflows
- **GitHub:** source code access and pull request automation
- **Slack:** the interface
