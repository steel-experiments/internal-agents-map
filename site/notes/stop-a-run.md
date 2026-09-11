Source: https://internal-agents.com/notes/stop-a-run.html

[← Notes](https://internal-agents.com/notes.html)

01 / Run limits

# When should an agent stop?

A failed run can still produce useful work.

11 September 2026 · 2 min read

## What the teams report

Stripe limits Minions to two rounds of continuous integration (CI) checks. It then returns the branch to a person. More attempts cost time and compute. [[1]](https://internal-agents.com/notes/stop-a-run.html#source-stripe)

Dropbox uses a different limit for Deflaker, its tool to repair unstable tests. It carries notes and test logs between attempts. It stops after a successful fix or five attempts. [[2]](https://internal-agents.com/notes/stop-a-run.html#source-dropbox)

> “A turn counter is not a progress detector.”

DoorDash, on a repeated request that did not advance the turn counter. [[3]](https://internal-agents.com/notes/stop-a-run.html#source-doordash)

DoorDash added deadlines for each agent. A soft deadline requests verified findings. A hard deadline stops the agent. [[3]](https://internal-agents.com/notes/stop-a-run.html#source-doordash)

01 **Attempt** Make a change

02 **Check** Inspect the result

03 **Stop or retry** Apply the run limit

At the limit → Save the work and explain the failure.

Our illustration of a possible control flow. Each source uses different checks and limits.

Our observation

## The limit needs a useful exit

An attempt limit and a time limit address different failures. Neither limit explains what the next person needs.

A useful exit can include the current work, failed checks, and a reason to stop. This is a design proposal, not a shared implementation.

The cases do not establish one correct retry count.

**A question for your build** What will a person receive if the next attempt fails?

## Sources

1. [Stripe: Minions, part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) CI checks and the return to a human operator.
2. [Dropbox: Introducing Nova](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents) Deflaker and its capped fix attempts.
3. [DoorDash: How we built an AI code reviewer](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) Repeated requests and per-agent deadlines.

[Stripe in the catalog](https://internal-agents.com/index.html#stripe-minions) [Dropbox in the catalog](https://internal-agents.com/index.html#dropbox-nova) [DoorDash in the catalog](https://internal-agents.com/index.html#doordash-code-review)

[All notes](https://internal-agents.com/notes.html) [Next: More comments can mean more work →](https://internal-agents.com/notes/review-noise.html)
