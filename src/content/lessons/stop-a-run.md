---
title: When should an agent stop?
description: Stripe, Dropbox, and DoorDash use different limits for failed agent runs. An observation on retries, time limits, and useful results.
eyebrow: 01 / Run limits
lede: A failed run can still produce useful work.
summary: A failed run can still produce useful work. Stripe, Dropbox, and DoorDash use different limits.
readingTime: 2 min read
order: 1
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - stripe-minions
  - dropbox-nova
  - doordash-code-review
sources:
  - id: stripe
    title: 'Stripe: Minions, part 2'
    url: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
    note: CI checks and the return to a human operator.
  - id: dropbox
    title: 'Dropbox: Introducing Nova'
    url: https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents
    note: Deflaker and its capped fix attempts.
  - id: doordash
    title: 'DoorDash: How we built an AI code reviewer'
    url: https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/
    note: Repeated requests and per-agent deadlines.
---

<section aria-labelledby="two-kinds-of-limit">

## Two kinds of limit

Stripe lets Minions run continuous integration (CI) checks twice. After the second run, the branch returns to its human operator for scrutiny. Dropbox's Deflaker instead allows up to five attempts, carrying test logs and notes from the previous attempt into the next. These limits count repair attempts. [[1]](#source-stripe) [[2]](#source-dropbox)

DoorDash encountered a different failure: a repeated model request consumed time without advancing the turn counter.

<blockquote cite="https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/"><p>“A turn counter is not a progress detector.”</p></blockquote>

<p class="quote-credit">DoorDash's account of the stalled review. <a href="#source-doordash">[3]</a></p>

DoorDash added per-agent deadlines. The soft deadline asks the reviewer to return findings it has already verified and discard speculation. The hard deadline stops it. An elapsed-time limit can catch a stalled attempt that never reaches a retry counter. [[3]](#source-doordash)

</section>

<section aria-labelledby="returning-useful-work">

## Returning useful work

Stopping and handing off are separate decisions. Stripe returns a branch; DoorDash's soft deadline requests verified findings. Dropbox preserves logs and notes for another attempt. The sources describe different outputs and recipients.

The diagram is our proposed repair loop. It makes the retry branch and the remaining work explicit; it does not describe one implementation shared by these companies.

<figure class="lesson-diagram">
  <div class="lesson-node"><strong>Inspect the result of an attempt</strong><small>Check the output and the remaining attempt or time budget.</small></div>
  <ul class="lesson-branches">
    <li><strong>Checks pass</strong><span>Return the result to the workflow's next review or publication step.</span></li>
    <li><strong>Checks fail; budget remains</strong><span>Carry the failure evidence into a repair, then check again.</span></li>
    <li><strong>Budget exhausted</strong><span>Stop and return the current work, failed checks, and reason for stopping.</span></li>
  </ul>
  <figcaption>Our proposed control flow. A passing check still leaves any required human approval in place.</figcaption>
</figure>

</section>
