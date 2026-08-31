> Archived source snapshot  
> Source ID: `shopify-internal-agents-source-1`  
> Original URL: <https://shopify.engineering/under-the-river>  
> Final URL: <https://shopify.engineering/under-the-river>  
> Title: Under the River (2026) - Shopify  
> Captured at: `2026-08-31T17:48:37Z`

---

It’s a strange time to be working in developer tools. Things we were doing six months ago don't make sense anymore. Tools that didn't exist a year ago are now central to how we work. The texture of the job has never changed so fast, and the tools we’re building reflect that.

River is an AI agent that lives in our company Slack. We launched it a couple of months ago. Now, one in eight merged pull requests across Shopify is coauthored by it.

[Tobi shared](https://x.com/tobi/status/2053121182044451016) how River has become a teaching workshop for our company, but the agent surface layer is only one part of the story. This is what we built underneath River, and the bet we placed in early 2024 that made it all possible.

## Part I · The signal

## Spring 2024

Here’s where Shopify was: many repos, bespoke development environments, slow feedback. Friction we’d learned to live with, especially when the alternative was "rewrite everything."

Around that time, we made two seemingly unrelated decisions:

1. **Become a monorepo company.** One repository for all things Shopify ships. We call it World.
2. **Build everything with [Nix](https://shopify.engineering/what-is-nix "Shopify Engineering Blog: What is Nix?")**. Dev environments, CI, production images: one reproducible substrate.

These were not crowd-pleasers. They were infrastructure-hygiene moves some thought were a waste of effort. But a bet drove them:

What happened next, in brief: It was painful. And it worked.

## What broke and what we got

Moving Shopify into one repo caused real breaks. CI had to scale by an order of magnitude, almost overnight. Merge queues became load-bearing. The build cache became a product. Test infrastructure had to be rebuilt around the assumption that any change might recompile a large share of the graph. Dozens of scattered team-level assumptions had to be undone, one by one. This is the unsexy part of the story.

But the payoff:

- An AI coding agent at the root of the repo, navigable cross-zone
- Skills: written-down knowledge as files, loaded into agent sessions on demand
- "Ask the repo a question" as a viable interface, by using the nascent agents
- Cross-Shopify navigation: from a log line in production back to the commit that caused it, without leaving a single workspace
- Reproducible everything: same Nix-built environments in dev, CI, and production

Two key insights emerged along the way, and they are the reason we’re writing this today.

## Thing one: agent-friendly ≈ human-friendly

Every change we made for agents was also the right thing for humans. The monorepo. Reproducible environments. Written-down skills. Clean, fast CI signal. These were all already on our wishlist, it’s just that none of them were urgent enough to devote resources to.

- Dev environment not reproducible? Agents can't reproduce anything either.
- Repo fragmented? Agents can't see across it.
- Nobody has written down how things work? Nobody can learn those things. Not humans onboarding, or agents in their first session.

The work to make a codebase legible to an agent is simply the debt you owe to your human engineers. Agents make that debt visible. The result is happier engineers.

## Thing two: local agents have a ceiling

Every engineer has their own agent. That agent runs on their laptop, in their terminal, in their editor. The clever way you investigated a flaky test yesterday is a private artifact and it dies with your session. None of these agents learn from each other.

This is the ceiling. We studied this problem, then we built River.

## Part II · The surface

## River only works in the open

River is an agent that lives in our Slack. You talk to it by typing @river in a public channel. It reads code, runs tests, opens pull requests, queries the data warehouse, looks at production traces, and occasionally pushes back on a plan it thinks is bad. Median session length: 19 minutes. Median tool calls per session: 50.

Here’s what that looks like:

One constraint: River only works in the open. No direct messages. Every conversation with River becomes a public Slack transcript, open by default to other Shopify employees.

We mine that corpus. One person's hard-won fix becomes the next person's starting point because we feed the patterns we see back into River's skills, prompts, and defaults. The agent gets smarter without requiring model retraining. The codebase teaches the agent. The agent teaches the codebase. All of this teaches us. This compounding effect is the most important part.

When a River thread goes well:

- One person @-mentions River with a question.
- River starts working: reads files, runs queries, posts partial findings.
- A second human, drawn by the link in their channel or by a direct ping, drops in with a constraint or a redirect.
- River incorporates the new context without losing the conversation, and continues.
- The thread is searchable. The work is reproducible. The next person to hit a similar problem starts from this thread, not from a blank prompt.

## At scale

In a recent 30 day period: **59,918** River sessions happened in **5,170** Slack channels, touching the work of **7,000+** people inside the company (~1,200 more than when Tobi posted about River in early May). **3,536** River-coauthored pull requests merged in that window. These numbers come from the `river_sessions` domain table that River writes to itself, every session.

River is not the only interesting object here. Our monorepo, World, is the focus, and it’s becoming something new.

World contains code. It also contains skills, conventions, intent documents, runbooks, `AGENTS.md` files, and written-down zone knowledge. It’s an intelligence layer, accumulating and compounding. When someone solves a problem with River, they leave a memory behind: a pebble, a skill update, an `AGENTS.md` diff, sometimes a whole new shared skill. The next session uses it. The next person watching the thread learns from both.

River isn't just using World. River is what makes World a living system. It’s the animating spark. This is why the platform underneath River matters. We need a substrate to host that spark for many agents, workflows, and years.

## "Can I do this for X?"

As River shipped, other teams watched. Predictably, they wanted their own:

- PR review agents
- Research agents
- Migration agents
- Compliance scans
- Performance investigations
- … and a long tail of other requests

All variants of the same idea: agentic workflow against the monorepo, in Slack, durable, multiplayer. We had built River. We had not built a thing that could be a hundred Rivers.

## We needed a platform

River was running fine. We had the architecture and intuitions about what must survive process death, but we weren’t there yet. We needed the right abstractions. We were circling the shape without naming it. Others were converging on this, too.

Reading this essay validated what we’d already been circling. Separating an agent's "brain" (the model deciding what to do) from its "hands" (the sandbox where code actually runs) keeps the conversation safely stored. And this work is not isolated: the shape of long-running agents is being figured out by several groups in parallel.

## Part III · What's underneath

## The session must survive

*Rivers shape the World. The Aquifer holds the water.*

**Aquifer** is Shopify's internal platform for running AI agents. It’s the substrate: session, harness, sandbox, gateway, the durable event log, the credentials proxy, the observability pipeline. River is a profile on top of it. Aquifer's design constraint is simple: everything else stems from it. Cells die, sandboxes die, machines die. The conversation doesn't.

This is obvious for humans. Slack threads outlive the servers that handled them. We are applying the same standard to agent threads. Here’s the decomposition:

- **Session:** Durable identity. Append-only event log. Postgres-backed. The canonical truth about what's happened so far.
- **Harness:** The agent loop. Reads history, calls the model, emits tool intents. Cheap to recreate, disposable.
- **Sandbox:** Where the code runs. Filesystem, shell, the repo. Bash, edit, build, test. Disposable. Sometimes warm, often fresh.

The harness lives outside the sandbox. The agent doesn’t live where the code lives. Three properties fall out of that, and you can’t get any of them otherwise:

- **Safety:** the agent loop is not in the same blast radius as `rm -rf`
- **Replaceability:** you can swap models, runtimes, even languages on the harness side without disturbing the sandbox
- **Observability:** the entire decision stream is on the harness side, visible to one place

## Session cells

When a session goes live, we materialize a *session cell*: an ephemeral process on a host, running the Go runtime and the agent harness in the same process group.

If idle, it exits. Next interaction: a fresh cell, possibly on a different host. But the session identity is unchanged, and the conversation is all there. The work picks up where it left off because the work lives in Postgres, not in memory. Cattle, not pets, at the session level. We don’t nurse individual processes. We provision, run, suspend, destroy, and re-provision them, and we do it on a substrate that makes this cheap.

We get asked which orchestrator we use, but the answer matters less than the principle: pick the end-to-end substrate, and refuse to compromise on cattle-not-pets at the session level.

## River is one profile. Aquifer is the platform.

River is one *profile* on top of Aquifer. PR review is another profile. Vanilla, the headless "pi" agent, is another. Future agents are peers, not children.

A profile is data: a system prompt, a set of skills, a set of extensions, a sandbox policy, model defaults. All built with Nix and shipped as bundles. Adding a new agent product means adding a bundle, not building a new platform. This is how we ship agents internally now.

The same objects support three distinct consumers:

- **Mode · Interactive:** River. Durable session, live human, long-lived.
- **Mode · Automation:** PR review. Durable session, woken by an external system, often no human in the loop.
- **Mode · Job:** CI, batch. Ephemeral. Provision, run, stream, destroy. Reuses the sandbox plane; the session log is optional.

This stack uses the same session model, sandbox plane, and gateway for each of the three consumers. This shape is important: every time we tried a different architecture, we found ourselves re-inventing one of these three modes.

Our substrate enables durable, threaded multiplayer conversation (with an agent participating as a first-class citizen) against the real codebase, data warehouse, and production signals. River is the visible part, Aquifer is the platform we built to ship more like it.

## We are at the start

River shipped about two months ago. Aquifer is rolling out underneath it, profile by profile. The usage numbers we shared are already wrong, in the upward direction.

The question we keep hearing echoes Robert Macfarlane's 2025 book title: *Is a River Alive*? We don't know how all of this will evolve. We know what it does, and we are still finding language for what it is.

River is what happens when the substrate underneath learns to flow. The Aquifer remembers. The Slack thread is where the work surfaces. The shop floor talks back, in public, every day, and gets a little smarter overnight. River, in this telling, is the verb.

What comes next at Shopify *only* happens because the substrate is there. New agent products are not new platforms; they are new bundles. Everything ships with a durable session, the gateway, a sandbox, and the multiplayer corpus. The cost of the next River-shaped thing is no longer a new platform, it’s just a profile.

That’s the unlock. That’s the thing that, two years from now, will be the boring assumption underneath every interesting product.

## What to take with you

You aren't at Shopify, and you can't tag River in our Slack. But the point is not the agent on the surface. It’s the substrate underneath, and the core bet that produced it: *the session is the thing that must survive*.

If you're building agent infrastructure, here are three priorities:

1. **Decouple the brain from the hands.** The harness does not live in the sandbox. When you commit to that boundary, safety, replaceability, and observability stop being trade-offs. You will not be able to retrofit it.
2. **Make the agent multiplayer by construction.** A private agent has a ceiling: the person at the keyboard. A public agent teaches every session that comes after it. The corpus is the compounding asset; the privacy of an agent thread is a disadvantage.
3. **Treat the next agent as a profile, not a platform.** The cost of a new agent product should be a new bundle on the same substrate. If your second agent forces a second platform, you haven't built the substrate yet.

## Building the next layer

Inside Shopify, all of this is in motion. None of it is finished. The architecture is stable enough that teams can build on top of it, and unfinished enough to still be some of the most interesting work of our careers.

Two years from now, the agent will not be the interesting part. What's underneath it will be. That’s the bet we made in 2024, and the data we have today says it paid off.
