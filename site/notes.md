Source: https://internal-agents.com/notes.html

From the cases

# Notes

Short observations for people who build agents.

Each note examines a design choice from the [catalog](https://internal-agents.com/index.html#catalog) . Sources describe what teams report. Our observations explain what those reports may mean for other builders.

01 / Run limits

## [When should an agent stop?](https://internal-agents.com/notes/stop-a-run.html)

A failed run can still produce useful work. Stripe, Dropbox, and DoorDash use different limits.

Stripe · Dropbox · DoorDash 2 min read

02 / Human attention

## [More comments can mean more work](https://internal-agents.com/notes/review-noise.html)

Uber and HubSpot check review comments before engineers see them.

Uber · HubSpot 2 min read

03 / Agent roles

## [Separate the search from the check](https://internal-agents.com/notes/split-the-work.html)

DoorDash changed how its agents divide a code review. Each design exposed a different problem.

DoorDash 2 min read

04 / Work state

## [The worker can stop. The work can continue.](https://internal-agents.com/notes/work-can-continue.html)

A new worker can continue from a saved record.

Shopify · Sentry · Sierra 2 min read

05 / Tools and context

## [Load tools when the task needs them](https://internal-agents.com/notes/load-tools.html)

An agent can find a tool before it loads the details.

Cloudflare · Sentry · Browserbase 2 min read

06 / Workflow control

## [Some steps do not need a model](https://internal-agents.com/notes/steps-without-a-model.html)

Code can control a step that must follow a fixed rule.

Stripe · Dropbox · PostHog 2 min read

07 / Evaluation

## [Test the agent on your own work](https://internal-agents.com/notes/test-on-your-work.html)

Past tasks and failures can become repeatable checks.

Databricks · Uber 2 min read

These notes describe selected cases. They do not establish that one design works best for every team.
