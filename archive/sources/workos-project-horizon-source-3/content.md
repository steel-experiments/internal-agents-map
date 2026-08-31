> Archived source snapshot  
> Source ID: `workos-project-horizon-source-3`  
> Original URL: <https://workos.com/blog/autonomous-ui-quality-program>  
> Final URL: <https://workos.com/blog/autonomous-ui-quality-program>  
> Title: Building an autonomous UI quality program — WorkOS  
> Captured at: `2026-08-31T17:51:49Z`

---

In this article

Explore with AI[Open in ChatGPT](https://chatgpt.com/?q=Read%20this%20article%3A%20https%3A%2F%2Fworkos.com%2Fblog%2Fautonomous-ui-quality-program.%20In%20a%20short%20paragraph%2C%20tell%20me%20what%20it%27s%20about%2C%20what%27s%20new%20or%20interesting%20about%20it%2C%20and%20whether%20it%27s%20worth%20reading%20in%20full.)

[

Open in Claude

](https://claude.ai/new?q=Read%20this%20article%3A%20https%3A%2F%2Fworkos.com%2Fblog%2Fautonomous-ui-quality-program.%20In%20a%20short%20paragraph%2C%20tell%20me%20what%20it%27s%20about%2C%20what%27s%20new%20or%20interesting%20about%20it%2C%20and%20whether%20it%27s%20worth%20reading%20in%20full.)[

Open in Perplexity

](https://www.perplexity.ai/?q=Read%20this%20article%3A%20https%3A%2F%2Fworkos.com%2Fblog%2Fautonomous-ui-quality-program.%20In%20a%20short%20paragraph%2C%20tell%20me%20what%20it%27s%20about%2C%20what%27s%20new%20or%20interesting%20about%20it%2C%20and%20whether%20it%27s%20worth%20reading%20in%20full.)

At WorkOS, we love obsessing over details not just for the sake of polish, but also because we know that it leads to a better product experience and earns trust.

Shipping as fast as we do usually works against quality. We built a ritual around protecting it, a program we call **UI Nits**, and it's how we track every one of those details across our products.

It took us five months to close our first hundred nits. Now we close almost a hundred a month. This is a deep dive into how we've shifted from a Slack channel full of complaints to an automated pipeline where a nit reported in the morning can be in production by the afternoon.

## Building a ritual

UI Nits started as a Slack channel. A place to complain about annoying, awkward, or simply weird UI details. No process, no template, just a simple message to describe the issue, accompanied by a screenshot.

At the time, it wasn't a true program yet. We weren't tracking anything and we couldn't tell you how often things actually got fixed. We changed that by first linking the channel to Linear, where every message became a ticket that we would manually triage.

![](https://cdn.prod.website-files.com/621f84dc15b5ed16dc85a18a/6a67a93320419e8ef4dce315_slack.png)

Once we could measure our impact week over week, we understood the value of the program. We could see what was broken, what got fixed, who fixed it, and then celebrate that work every week as a team.

This ritual extended beyond the design team. Engineering was deeply involved and people across the entire company were filing nits and fixing them. Everyone owned the bar and continuously pushed it forward.

## Bringing in agents

Triage was the most manual part of the program. With each ticket, we'd have to figure out where in the product it lived, gauge its impact, and define a resolution clear enough for someone to pick up.

To improve this, we built a skill for it. Triage is a skill that runs in the cloud against every incoming ticket. It reads the ticket, then enriches it with information so that a human or an agent can pick it up. That usually includes where to find it in the product, how to fix it, and a level of confidence that the solution is correct. If we need to jump in and intervene, it's really easy for us to find the low-confidence tickets and enrich them manually.

![](https://cdn.prod.website-files.com/621f84dc15b5ed16dc85a18a/6a67b7dfe8fa8862ad4650ca_slack-2.png)

As our confidence in the Triage skill improved, we kept adding to it. Now it includes our page traffic, so every nit carries customer impact, helping us spot and prioritize high-volume nits. When suggesting a fix, the skill also checks against product data and makes sure all edge cases are accounted for, so that tickets have more accurate and confident solutions.

Suddenly triage wasn't a bottleneck or a manual process anymore. Agents were helping us and doing it more consistently than we had. More importantly, it set up the next stage: if every ticket arrives with full context and a rated solution, agents don't just have to triage the work; they can do it.

## Becoming fully autonomous

This is the same bet we're making across engineering with [Horizon, our self-driving codebase](https://workos.com/blog/project-horizon): agents running in a review-first loop. With our Triage skill running, Horizon can pick up the high-confidence tickets and fix them automatically, which leaves us with a PR to approve, instead of a ticket to triage, solve, and put back in the queue.

Fixing tickets is only the first part of where this goes. Finding nits, not just fixing them, is equally important, and it's easy for agents to comb through our products and run QA. We use agents to lint against our design system, WorkDS, and ensure that PRs don't drift from our patterns. We also run QA agents to check mobile viewports and file what they find in the same pipeline.

With these automations, every fix feeds back into the system. We're no longer tracking one-off issues, but watching trends for which patterns drift and which components confuse people. The pipeline will continue to learn from itself over time, and the codebase will start repairing itself and learning where not to break.

## Maintaining the ritual

The easy framing of our UI Nits program is that it's about polish. It's really about velocity and trust, about us building shared standards and patterns across our products, and holding everyone across the company to the same quality bar.

Because this pipeline exists, we can ship fast and know that rough edges will get caught and fixed, often the same day. The quality bar isn't slipping and the velocity isn't slowing; we get both at once, because the repair loop is cheap enough that everyone participates.

Agents didn't remove humans from this. They moved us to the two places where judgment actually matters: deciding what's worth fixing and caring whether the fix is right.

If you want to work where craft and agents meet, [we're hiring](https://workos.com/careers#open-positions).
