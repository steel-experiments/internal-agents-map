> Archived source snapshot  
> Source ID: `stripe-minions-source-1`  
> Original URL: <https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents>  
> Final URL: <https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents>  
> Title: Minions: Stripe’s one-shot, end-to-end coding agents | Stripe Dot Dev Blog  
> Captured at: `2026-08-31T17:49:52Z`

---

/Article

Across the industry, agentic coding has gone from new and exciting to table stakes, and as underlying models continue to improve, unattended coding agents have gone from possibility to reality.

Minions are Stripe’s homegrown coding agents. They’re fully unattended and built to one-shot tasks. Over a thousand pull requests merged each week at Stripe are completely minion-produced, and while they’re human-reviewed, they contain no human-written code.

Our developers can still plan and collaborate with agents such as Claude and Cursor, but in a world where one of our most constrained resources is developer attention, unattended agents allow for parallelization of tasks.

A typical minion run starts in a Slack message and ends in a pull request which passes CI and is ready for human review, with no interaction in between. We frequently see engineers spinning up multiple minions in parallel, to enable them to parallelize the completion of many different tasks. This can be particularly helpful during an on-call rotation to effectively resolve many small issues that might arise.

In the first part of this blog post miniseries, we’ll show you how our engineers use minions and what they can do. In Part 2, we’ll dive into the implementation under the hood and how we built them.

### Why did we build it ourselves?

Vibe coding a prototype from scratch is fundamentally different from contributing code to Stripe’s codebase.

Stripe’s codebase encompasses hundreds of millions of lines of code across a few large repositories. Most of our backend is written in Ruby (not Rails) with Sorbet typing, a relatively uncommon stack. Throughout, our code uses a vast number of homegrown libraries that are unique to Stripe and therefore natively unfamiliar to LLMs.

The stakes are high: this code moves well over $1 trillion per year of payment volume live in production. Simultaneously, Stripe has many intricate real-world dependencies on financial institutions and regulatory and compliance obligations that our code must honor.

LLM agents are incredibly good at building software from scratch when there are relatively few constraints on a system. However, iterating on any codebase of the scale, complexity, and maturity of Stripe’s is inherently much harder. Humans must build sophisticated mental models to make effective changes in our repos, and enabling agents to develop the correct intuitions and use the correct tools within the confines of their context windows is challenging.

Over the years, Stripe has invested in developer productivity foundations that support our unique constraints at all stages in the development lifecycle—source control, environments, code generation, CI, and much more—and so our custom minion harness tightly integrates with that tooling. Minions use the same developer tooling that equally enables Stripe’s human engineers to effectively operate on our scale: if it’s good for humans, it’s good for LLMs, too.

### What is it like to use a minion?

There are several different entry points for minions, designed to integrate as ergonomically as possible with where Stripes are. While we provide CLI and web interfaces for initiating minions, engineers will most frequently start one from Slack. By tagging our Slack app, engineers can kick off a minion directly from the thread discussing a change, and it’ll be able to access the entire thread and any links included as context.

If you’re an engineer working on internal tools, you might kick off a minion with a message like this:

> A Slack message invoking a minion run

Minions can also be invoked from inside other internal applications at Stripe. Our internal docs platform, feature flag platform, and internal ticketing UI all integrate with minions. For example, when our CI systems detect flaky tests, we create automated tickets that prompt users to fix the problem with a minion.

> A flaky test ticket with a button to start a minion that’d fix it

While the minion works, or after the fact, engineers can see the decisions and actions the minion took in a web UI.

> An example of the web interface for managing minion runs

Once it has completed its task, a minion creates a branch, pushes it to CI, and prepares a pull request following Stripe’s PR template. If the code looks good, the engineer opens the PR and requests a review from another Stripe engineer. If not, they can give the minion further instructions, and it will push updated code to the branch when it’s done.

Engineers can also iterate on a completed minion run manually once it’s completed. While our North Star is a pull request produced without any human code, a minion run that’s not entirely correct is often still an excellent starting point for an engineer’s focused work.

### How do minions work?

There are many stages to a minion, and in the second part of this miniseries, we’ll have more details about how minions work. Many of the details are Stripe-specific, but we do think that there are some generalizable lessons. To whet your appetite, here’s a brief chronological tour.

A minion run starts in an isolated developer environment—or “devbox”—which are the same type of machine that Stripe engineers write code on. Devboxes are pre-warmed so one can be spun up in 10 seconds, with Stripe code and services pre-loaded. They’re isolated from production resources and the internet, so we can run minions on devboxes without human permission checks. This also gives parallelization without the overhead of something like git worktrees, which wouldn’t scale at Stripe.

The core agent loop runs on a fork of Block’s coding agent [goose](https://github.com/block/goose), one of the first widely used coding agents, which we forked early on. We’ve customized the orchestration flow in an opinionated way to interleave agent loops and deterministic code—for git operations, linters, testing, and so on—so that minion runs mix the creativity of an agent with the assurance that they’ll always complete Stripe-required steps like linters.

In general, minions read the same coding agent rule files that human-operated tools such as Cursor and Claude Code do, consuming several different agent rule file formats. However, it would be impractical for Stripe to have many unconditional rules, so almost all agent rules at Stripe are conditionally applied based on subdirectories.

Minions are connected to MCP, which provides a common language for networkable LLM function calling. This is how they gather context like internal documentation, ticket details, build statuses, code intelligence via Sourcegraph search, and more. Indeed, we deterministically run relevant MCP tools over likely-looking links before a minion run even starts, to better hydrate the context.

Since MCP is a common language for all agents at Stripe, not just minions, we built a central internal MCP server called Toolshed, which hosts more than 400 MCP tools spanning internal systems and SaaS platforms we use at Stripe. Minions and other agents have connectivity to configurable but curated subsets of the full breadth of tools.

Minions are built with the goal of one-shotting their tasks, but if they don’t, then it’s key to give agents feedback. We do this via several automated layers of tests that minions can iterate against. The first line of defense is an automated local executable, which uses heuristics to select and automatically run selected lints on each git push. This takes less than five seconds.

We seek to “shift feedback left” when thinking about developer productivity. That means that it’s best for humans and agents if any lint step that would fail in CI is enforced in the IDE or on a git push, and presented to the engineer immediately.

If the local testing doesn’t catch anything, CI selectively runs tests from Stripe’s battery of tests—there are over three million of them—upon a push. Many of our tests have autofixes for failures, which we automatically apply. If a test failure has no autofix, we send it back to the minion to try and fix.

Since CI runs cost tokens, compute, and time, we only have at most two rounds of CI. If tests fail after an initial push, we prompt the minion to fix failing tests and push a second time, but are then done. There’s a balancing act between speed and completeness here, and there are diminishing marginal returns for an LLM to run many rounds of a full CI loop. We feel this guidance of “often one, at most two, CI runs—and only after we’ve fixed everything we can locally” strikes a good balance.

In short, minions are set up with the same tools we give human engineers and the necessary context to follow Stripe best practices in the code they write. And engineers can and do invoke them ergonomically as part of their normal job duties.

### What’s next?

Minions have already reimagined what it’s like to code at Stripe. The industry is still exploring what the future of agentic coding will look like, but we’re sure that the unattended code agent use case will remain among the most exciting applications of agents.

In [Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), we’ll dive more deeply into how we implemented minions.

Interested in working with, or on, minions? [We’re hiring](https://stripe.com/jobs).
