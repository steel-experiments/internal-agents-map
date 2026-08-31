> Archived source snapshot  
> Source ID: `coinbase-forge-mux-source-1`  
> Original URL: <https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it>  
> Final URL: <https://www.coinbase.com/de/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it>  
> Title: Coding Had a Concurrency Problem: How Mux Helped Solve It  
> Captured at: `2026-08-31T17:41:07Z`

---

For decades, software engineering followed the same loop: pick up a ticket, enter flow state, write code, open a PR, wait for review, merge. The work was sequential because the bottleneck was always a human writing code.

AI coding agents broke that assumption. By early 2026, every Coinbase engineer had access to Cursor, Copilot, OpenCode, and Claude Code (we wrote about that adoption journey in ["Tools for Developer Productivity at Coinbase"](https://www.coinbase.com/de/blog/Tools-for-Developer-Productivity-at-Coinbase?country=US&currency=USD&mobile=false&japan_bespoke_content=false&logged_in=false&null=) last August). Agents were fast. But engineers were still working the old way: one branch, one terminal, one task. While the agent worked, the engineer waited. Switching tasks meant stashing changes, swapping branches, losing context.

The bottleneck had moved. It was no longer how fast we could write code. It was how many things one engineer could orchestrate at once.

## The Shift

When code becomes cheap, the engineer's job changes. The work that matters shifts upward: scoping problems, designing solutions, reviewing output, catching edge cases. The implementation becomes the easy part.

This is the shift we're seeing across Coinbase: engineers becoming orchestrators of agent fleets. A typical workflow now looks more like a conductor leading musicians than a soloist performing a piece. One engineer might have three or four agents working in parallel: one implementing an API, one writing integration tests, one fixing a bug, one refactoring a legacy module. The engineer reviews each as it finishes, provides feedback, and merges.

## The Evidence: Mux

Mux is one tool in a broader portfolio Coinbase engineers rely on day-to-day — Claude Code, OpenCode, Cursor, and a growing set of internal coding agents all see heavy use alongside it. We're highlighting Mux here because it's the tool that most directly enabled the multi-agent orchestration shift this post is about.

Mux is an internal multi-agent coding tool that started when one engineer built it to solve their own problem. The idea was minimal: each agent gets its own git worktree, its own branch, its own terminal. No conflicts. No stashing.

It wasn't designed to be a product. It was shared with a few teammates, posted in a Slack channel, and left alone. There was no adoption campaign. Engineers found it, tried it, and kept it if it solved their problem. Many started contributing back: integrations with internal infrastructure, plugins for team-specific workflows, bug fixes.

- **600+ users** including engineers, PMs, and designers, with 335 active and 197 power users.
- **5,068 merged PRs** across 461 repositories and 10 orgs.
- **3.5x more merged PRs per engineer** for Mux users compared to baseline: 39.6 vs 11.4.

These numbers come with caveats. Mux users likely skew toward engineers who were already high-output and AI-forward, so we don't claim Mux is the sole cause. But the consistency across orgs and repos suggests this isn't a marginal effect. Beyond the metrics, engineers consistently report a qualitative shift: they attempt work they wouldn't have before. Refactors that touch multiple services, batches of bug fixes, features plus their test suites. Multi-day efforts become single-session workflows.

The grassroots adoption matters here. It happened because leadership had already invested in the conditions for it: secure access to frontier models through our internal LLM Gateway, a growing ecosystem of MCP servers, and an engineering culture that gives teams space to experiment. Mux didn't emerge despite the system. It emerged because the system was designed to let things like this happen.

## What About Open Source?

A reasonable question: did we have to build this ourselves? Several open-source multi-agent tools exist (and a growing ecosystem of agent runners).

We chose to build in-house for a specific reason: the value isn't in the multi-agent UI, which exists everywhere. It's in the institutional knowledge that gets baked in. The plugins, skills, and integrations engineers built on top of Mux encode how Coinbase actually ships software: dispatching to our internal cloud agent fleet, deploying through Codeflow, automating team-specific review flows, encoding repo conventions into reusable commands. Open-source tools can be extended with custom plugins, but bridging them to our internal cloud agent infrastructure, our LLM Gateway, and our repo sensitivity controls would have required significant security work and slowed our ability to iterate.

There's a broader point here: AI changed the build-vs-buy calculus for internal tooling. Before AI, building something like Mux internally would have meant vendor evaluations, procurement, and months of negotiation. Now, one engineer with access to the right models and infrastructure can prototype in days what used to require a vendor relationship. Internal tools that encode institutional knowledge are suddenly cheap to build and expensive to ignore.

## What This Means

The shift from implementers to orchestrators isn't unique to Coinbase. Across the industry, leading engineering organizations are converging on the same pattern: humans steer, agents execute.

Two takeaways for engineering teams thinking about where to invest:

**For engineers**: the skills that compound are no longer "writes code fast." They're sharp scoping, careful review, system thinking, and knowing when to trust agent output and when to push back. Engineers who lean into orchestration get more done and spend more time on the parts of the job that matter most.

**For engineering leaders**: invest in the substrate that makes this paradigm possible. Secure access to frontier models, internal infrastructure agents can plug into, and a culture that lets engineers prototype tools that solve their own problems. The most valuable internal tools right now are the ones that encode how your company specifically ships software, and AI has made them cheap enough to build that the ROI calculation has fundamentally changed.

We're early, and the shape of engineering work in two or three years is still taking form. But the direction is clear: AI doesn't just accelerate the code we ship to customers. It changes what engineers do and how teams build the tools they use to ship it.
