> Archived source snapshot  
> Source ID: `airbnb-airchat-source-3`  
> Original URL: <https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai>  
> Final URL: <https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai>  
> Title: How to get your team past the AI coding plateau  
> Captured at: `2026-08-31T17:38:58Z`

---

### Get a working definition of agentic coding. Walk through the principles and the learnings. Plot your team on the grid. Fill the readiness checklist. Bring the next move to your CTO.

Your engineering team installed Cursor or Claude Code six months ago. Maybe Copilot before that. They use it daily. **PRs go out a bit faster, code reviews catch a bit less, everyone agrees it’s good.** And then last week, someone said the quiet part out loud at your team meeting. ”Wait, is this it?”

The team learned a new tool. They got a small productivity bump. The next jump never came. **And now, sitting in the all-hands, you can feel the air going out of the room.** You sold this to your CTO as a step-change in time to market. It’s looking more like an autocomplete upgrade.

I want you to spend 35 minutes on a video before your team decides this is as good as it gets. It’s a talk from Szczepan Faber and Mike Nakhimovich, two engineers on Airbnb’s developer platform team. They explain how their org went from zero to 64% of PRs materialized through agentic coding in nine months. **No marketing slides, no vendor pitch, two practitioners with diagrams and the receipts.**

![](https://www.youtube.com/watch?v=o6oYc9-X9Iw)

I know. Another AI talk. **But this one is different.** Most agentic engineering announcements recently read like product trailers. Stripe wrote up their [Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents), one-shot end-to-end coding agents that ship code from issue to PR. Spotify wrote up their [background coding agent](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) you can fire off from Slack. Both are real engineering teams shipping real systems. But the writing is announcement-shaped, and you walk away knowing what they built, not how to bring your own team along.

This one is two practitioners walking through their methodology, their mistakes, the proficiency model they built for engineers, and the org structure that scaled it. With actual numbers. With actual diagrams. **Practitioner depth, not announcement depth.**

A disclaimer before you watch. **The talk is from October 2025, which is roughly prehistory in AI time.** A few things they mention have already evolved. Their internal stack is theirs, not yours. You shouldn’t copy what they did. Since then, Airbnb’s CEO has publicly stated AI writes nearly 60% of new code at Airbnb ([TechCrunch coverage of the May 2026 earnings call](https://techcrunch.com/2026/05/08/airbnb-says-ai-now-writes-60-of-its-new-code/)). The platform team’s October talk is still the operating manual. The May number is the receipt. The definitions, principles, and learnings travel.

This post is the distillation. A working definition of agentic coding so you can say it cleanly to your team. The principles their team operated by. The mistakes they fixed. And a small grid you can use to plot your tech function and pick the next project to push for. Watch the video first if you have the time. If you don’t, **this post stands on its own.**

![hand-drawn black-and-white infographic showing five horizontal stops the article walks through — Plateau, Definition, Principles, Learnings, Grid — each represented by a small icon and labeled with what to expect.](https://substackcdn.com/image/fetch/$s_!w_c_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b886815-e430-4cf8-abee-d6487819d278_2816x1536.png)

hand-drawn black-and-white infographic showing five horizontal stops the article walks through — Plateau, Definition, Principles, Learnings, Grid — each represented by a small icon and labeled with what to expect.

- **The plateau.** I’ll show you why AI coding tools alone gave your team a small bump and stalled.
- **The definition.** I’ll give you a clean working definition of agentic coding to quote to your team.
- **The principles.** I’ll walk you through the org moves Airbnb’s team built around the tools.
- **The learnings.** I’ll point out the post-mortems you’d repeat without them.
- **The grid.** I’ll hand you a four-cell grid to plot your team and pick the next move.

By the end, you’ll have the working definition, the principles, the learnings, and a four-cell grid plotted with your tech team’s location and a next-move sentence. You’ll also walk away with a 7-category readiness checklist you can paste into a Google Doc and fill in row by row. **You walk away with the conversation to have with your CTO on Monday, and a way to reframe AI tool ROI as agentic coding maturity.**

Let’s pin it down.

---

## Name the plateau

Every team is hitting the same wall right now. The AI coding tool went in, the productivity bump was real, and then nothing. The team starts wondering out loud whether they bought the future or just a faster autocomplete. **Naming the wall is the first move, because the wall has a shape and the shape tells you what comes next.**

Airbnb’s platform team measured it. They ran the velocity numbers across three engineer cohorts. Non-AI users moved at the team’s baseline pace. AI-aided non-agentic users (the autocomplete-and-chat crowd) shipped PRs at +27% velocity. Full agentic users shipped at +38%. **The eleven-point gap between tools-only and agentic is the ceiling teams hit when they stop at the tool.** That gap is not a tool failure. It’s the natural plateau most teams sit on right now.

![hand-drawn bar chart with three vertical bars representing PR velocity uplift: non-AI users at 0%, AI-aided tools-only at 27%, and full agentic coding at 38%. A curly brace between the second and third bars highlights the eleven-point gap, labeled “where infrastructure, practice, and leadership live.”](https://substackcdn.com/image/fetch/$s_!KrBZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d72b116-6430-4e03-bcb4-86a512765300_2816x1536.png)

hand-drawn bar chart with three vertical bars representing PR velocity uplift: non-AI users at 0%, AI-aided tools-only at 27%, and full agentic coding at 38%. A curly brace between the second and third bars highlights the eleven-point gap, labeled “where infrastructure, practice, and leadership live.”

One honest caveat before we keep going. The wider data is messier than Airbnb’s three bars suggest. Google Cloud’s [2025 DORA report](https://dora.dev/dora-report-2025/) found individual output rises while team delivery stays flat. [METR’s July 2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found experienced open-source devs were 19% slower with AI tools, while they believed they were 20% faster. **Airbnb’s three bars are one of the cleanest team-level signals we have, not the universal shape.** Treat them as the strongest existing public benchmark, not the law of nature.

Three things sit inside that eleven-point gap.

- The first is **practice maturity**: how engineers actually use the tool day to day, whether they auto-approve, whether they review every diff, whether they push back when the agent is confidently wrong.
- The second is **org infrastructure**: the paved paths, the internal champions, the sandboxed environments, the MCP servers that wire internal context into the loop.
- The third is **leadership conviction**: whether the org frames agentic coding as a step-change worth funding or a productivity tweak worth tolerating.

**Each one is a stop on a journey your team has been walking since the IDE era.** None of them gets fixed by buying a better tool.

![hand-drawn three-stage timeline showing the evolution of software engineering, from a solo engineer typing alone (Stage 1: Legacy development), to the same engineer with a small agent icon offering autocomplete (Stage 2: AI-assisted), to one engineer steering multiple agents in parallel (Stage 3: Agentic coding).](https://substackcdn.com/image/fetch/$s_!_I2o!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83b3e4e9-82bb-4af3-8c9c-7242c7f0705c_2816x1536.png)

hand-drawn three-stage timeline showing the evolution of software engineering, from a solo engineer typing alone (Stage 1: Legacy development), to the same engineer with a small agent icon offering autocomplete (Stage 2: AI-assisted), to one engineer steering multiple agents in parallel (Stage 3: Agentic coding).

Your team is at Stage 2. The plateau is not a sign you picked the wrong tool. It’s a sign the next investment is in the things around the tool. That reframe is the one you carry into the leadership conversation. **You bought the engine. Now you’re missing the chassis.**

Naming the gap is the first move. Naming what agentic coding actually is comes next. That’s the language you’ll use upstream.

---

## Define what agentic coding is

Part of why your team is stuck in the plateau is that they’re using one word for two different things. Autocomplete is not agentic coding. Copy-paste from ChatGPT is not agentic coding. A single-shot retrieval over your codebase is not agentic coding. **None of those is the thing Airbnb measured at +38%.** Clean the definition first, then have the budget conversation honestly.

![hand-drawn diagram of the agentic coding loop. An engineer at a laptop writes a spec. The spec feeds into a circular loop containing four labeled nodes: multiple LLM calls, multiple tool and MCP calls, configuration files, and guardrails. The loop outputs a code change. A human reviews the change before it merges into a PR.](https://substackcdn.com/image/fetch/$s_!0UtW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F868fb635-3be2-44ce-aa50-f80858ab0b30_2816x1536.png)

hand-drawn diagram of the agentic coding loop. An engineer at a laptop writes a spec. The spec feeds into a circular loop containing four labeled nodes: multiple LLM calls, multiple tool and MCP calls, configuration files, and guardrails. The loop outputs a code change. A human reviews the change before it merges into a PR.

An engineer writes a short spec or prompt. That spec kicks off an autonomous loop. Inside the loop, an LLM is called several times. Tools and MCPs are called several times. The loop loads config files (AGENTS.md, CLAUDE.md, cursor rules) and runs against guardrails. Out the other side comes a materialized code change. A human reviews every line before it merges. **The thing that makes it agentic is the autonomy in the middle, not the input or the output.**

The engineer doesn’t know exactly what’s happening in there. Szczepan put it bluntly:

> An engineer who is leveraging an agentic tool, you don’t know how many \[calls happen\]. You start your agentic session, but you don’t know exactly what prompts the agentic tool will use when it calls LLMs. You don’t know exactly how many times it’s going to call LLMs. You don’t know exactly what tools it’s going to use.

**That uncertainty is the point.** The loop owns the path. You own the spec and the review.

Three things people call agentic coding that aren’t. Autocomplete in your IDE is not agentic coding (one-shot, no tool calls). Pasting code into a chat window and copying the answer back is not agentic coding (no loop, no autonomy). A single-shot RAG search returning a snippet is not agentic coding (no decision-making, no tool composition). Szczepan made the same point.

> That’s not where the magic happens. This is not this paradigm shifting change where a human engineer can steer multiple agentic sessions and materialize code changes.

**The +27% in the velocity chart is what you get from those. The +38% is what you get from the loop.**

**The cleanest way to explain the shape to leadership is borrowed from pair programming.** You probably have engineers who’ve done it. In classic pair programming, the driver holds the keyboard and is tactical. The navigator looks at the whole forest and is strategic. They alternate roles through the day. Agentic coding flips that into something stable.

![hand-drawn side-by-side comparison. Left panel: two engineers at one laptop in classic pair programming, one as the tactical driver at the keyboard, the other as the strategic navigator looking at the screen, alternating roles. Right panel: one engineer as the permanent navigator gesturing at the screen, a robot as the permanent driver at the keyboard materializing code.](https://substackcdn.com/image/fetch/$s_!RBpe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77667215-3d5b-4270-bfcc-15d3cd341caf_2816x1536.png)

hand-drawn side-by-side comparison. Left panel: two engineers at one laptop in classic pair programming, one as the tactical driver at the keyboard, the other as the strategic navigator looking at the screen, alternating roles. Right panel: one engineer as the permanent navigator gesturing at the screen, a robot as the permanent driver at the keyboard materializing code.

The engineer becomes the permanent navigator. The agent becomes the permanent driver. The engineer steers the session with chat, click, voice, or image. The agent materializes the code. Szczepan said it directly:

> Agentic coding is where a developer becomes this permanent navigator and it’s steering that agentic session, and an agent or your tool is materializing code changes.

**The leadership analogy travels because every CTO over the age of 35 has done pair programming.**

The technical version of the analogy is sharper. What the navigator is actually doing has a name. Andrej Karpathy [coined “context engineering”](https://x.com/karpathy/status/1937902205765607626) in June 2025 as the successor to prompt engineering. He called it ”the delicate art and science of filling the context window with just the right information for the next step.” That’s the navigator’s job. **Pair programming is the analogy that lands. Context engineering is the technical second skin.**

Now that you can name it, here’s what Airbnb’s team learned about making it actually pay off.

---

## Borrow these principles

The tool was the easy part. The principles are the actual work. None of these cost engineering headcount. **All of them are decisions you can push for from where you sit.** Here are five that travel from Airbnb’s context to almost any other org.

### Start with a bold vision, work backwards

Airbnb’s platform team opened their January 2025 leadership pitch with a single sentence:

> AI-powered, agentic coding will eventually replace traditional programming methods. How do we work backwards from that end state?

Then they actually worked backwards. They didn’t ask “what experiment do we run next quarter?” They asked “what does Step 10 look like?” and walked backwards to Step 1. Szczepan was direct about why.

> If you only think about incremental improvements, it’s kind of hard to make a big change.

**The move is the same for you.** Put the destination on a slide before you put the roadmap on a slide.

### Use an analogy with leadership

The pair-programming analogy didn’t land at Airbnb because it was clever. It landed because leadership had done pair programming.

> The way we’ve explained that to our leadership at start of 2025, we’ve used pair programming analogy for this.

Szczepan said. Pick an analogy your leadership already trusts. Map agentic coding into it. **Leadership conversations don’t move on facts. They move on framings your audience already believes.** If they came from a team that used trunk-based development, talk in those terms. If they came from agile, talk in those terms.

### Measure holistically, never personally

The default trap is to pick one number. Velocity goes up. Ship it. Sentiment goes down. Drop it. **Airbnb uses three lenses together, never individually:** developer sentiment from quarterly surveys, tool adoption across surfaces and PRs, and engineering output like PR velocity aggregated across the team.

![hand-drawn three-panel diagram. Panel 1 shows a thought bubble labeled “Sentiment, do engineers feel the tool is helping?” Panel 2 shows a bar chart labeled “Adoption, who is using it on which surfaces.” Panel 3 shows a line graph labeled “Engineering output, aggregated team velocity.” A banner underneath reads “Used together. Aggregated. For insight, not oversight.”](https://substackcdn.com/image/fetch/$s_!KEnH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1b1a8a8-056d-4a51-95d7-fdcd3c81498a_2816x1536.png)

hand-drawn three-panel diagram. Panel 1 shows a thought bubble labeled “Sentiment, do engineers feel the tool is helping?” Panel 2 shows a bar chart labeled “Adoption, who is using it on which surfaces.” Panel 3 shows a line graph labeled “Engineering output, aggregated team velocity.” A banner underneath reads “Used together. Aggregated. For insight, not oversight.”

The philosophy slide from their talk is forwardable on its own.

> Our aim is to learn how AI impacts developer experience and software quality so we can improve both. Not to micromanage or rank individual performance. Focus on insight, not oversight.

This is the principle to use when leadership asks for ROI metrics that don’t exist yet. **The answer is not one metric.** The answer is three, read together, looked at the team level. If you want a public framework they’ve heard of, Airbnb’s three lenses overlap with what [DX calls the Core 4](https://getdx.com/news/introducing-the-dx-core-4/) (Noda and Tacho, January 2025): Speed, Effectiveness, Quality, Impact. Same principle: never one number, never per-individual.

### Meet developers where they are

Sixty percent of Airbnb’s engineers prefer remote workspaces. Forty percent prefer local. IDE lovers stayed in IntelliJ. CLI lovers stayed in Vim. Mike tried the migration play once.

> We considered, maybe for a few days, grabbing all of our IntelliJ users and moving them over to VS Code. That lasted for a few days before I had to fear for my life that someone would come after me.

He said. **The principle: build parity across surfaces, not migrations.** Or as Mike put it elsewhere:

> We don’t have one typical engineer at Airbnb.

You probably don’t either.

### Invest in the org around the tool

**This is the biggest gap most teams skip.** The tool ships. The infra doesn’t. Nobody builds a champions network, no one paves the install path, no one wires internal context into the agent. Airbnb invested in all three. A champions network of thirty cross-functional engineers (not the core team of four). Paved paths with single-command install, automagic auth, and project templates. Over a dozen internal MCP servers connecting agents to internal systems. Szczepan said the line out loud:

> Your agentic tool is not enough. You will have to have a lot of tech around it.

If you want a second public example to back this up, Shopify built the same pattern at roughly 10x the scale. CEO Tobi Lütke’s leaked AI memo became an internal movement. The eng org built an internal LLM proxy, standardized MCP servers wired to their wiki and PM tool and data warehouse, and bi-annual performance reviews that explicitly evaluate “AI-reflexivity.” Two-anchor evidence is sturdier than one-anchor evidence. ([First Round wrote it up](https://www.firstround.com/ai/shopify); [Bessemer wrote up the engineering playbook](https://www.bvp.com/atlas/inside-shopifys-ai-first-engineering-playbook).) **This is the line item to fight for in your next budget cycle.**

### Add three engineering principles

Three more principles, briefly. First, wrap open source instead of building your own orchestrator. The rule is “don’t build a full orchestrator from scratch,” not “wrap whatever’s hosted externally.” Even Airbnb wraps their own `airchat-cli`, not raw OpenAI or Anthropic. In regulated orgs (finance, healthcare, EU-AI-Act-bound), routing internal code through a third-party CLI is a procurement and legal fight, not a one-line decision. **Build the thin wrapper layer locally if compliance demands it.**

**Second, bring context to agents through tool calling, not by training models.** ”Tool calling is all you need,” Mike said. He’s riffing on the 2017 Transformer paper title. His point: the LLM doesn’t need bespoke training on your codebase. It just needs the right tools available. Whether tool calling alone is enough versus the richer MCP pattern is contested in 2026. [Anthropic’s November 2025 “Code execution with MCP”](https://www.anthropic.com/engineering/code-execution-with-mcp) pushes more sophisticated patterns. Mike’s line still holds as the directional claim.

Third, never drop human review on the way to the PR. Szczepan’s line is the one to forward to anyone tempted to “ship faster”:

> I don’t trust the AI. I trust my skill in prompting and using the tools.

**The agentic loop ends at the diff.** Every line is reviewed by a human before merge, especially the test code.

Worth knowing what to avoid too. Here’s what Airbnb’s team got wrong before getting it right.

---

## Avoid these mistakes

Even Airbnb’s platform team got things wrong before they got them right. They have four engineers, a dedicated mandate from leadership, and the resources of a 7,000-engineer parent org. They still hit these. **Worth borrowing the post-mortems before you make them yourself.**

### Don’t bet on a slow curve

Airbnb’s platform team predicted at the start of 2025 that materializing code through agentic sessions would hit 20% to 40% of PRs by the end of the year. By the time they gave their talk in October 2025, they were at 64%.

> We were sandbagging them a bit too much, I think, because we were not ambitious enough. It’s going faster.

Szczepan said. **If the people building the platform underestimated their own curve by a factor of two, the “wait and see” position upstream is probably already late.**

There’s a name for that position. Geoffrey Moore called it “ [early majority pragmatism](https://en.wikipedia.org/wiki/Crossing_the_Chasm) ” in Crossing the Chasm (1991). Pragmatists wait for proof. Visionaries (early adopters) ship before the proof exists. Recent commentary suggests consumer GenAI has crossed the chasm; agentic enterprise systems are mid-crossing. **The frame gives you a named, well-known concept to drop in the 1:1:** ”You’re in classic early majority position. The data suggests the chasm has already been crossed.”

### Don’t build your own orchestrator, wrap one

Mike’s team spent months building an internal agentic orchestrator. Registered agents. Planning chained to coding chained to validation. It was elegant. It never shipped.

> AI moves way too fast. We were still planning, figuring out what we were going to do that existed in the market, and the market now is five steps ahead of us. It wasn’t going to work.

He said. They walked away from the orchestrator and pivoted to a thin shim over `airchat-cli`.

> Can’t beat them, join them. We pivoted and instead delegated to our Airchat CLI.

The rule for any size team: **if open source is iterating faster than you can ship, wrap it.**

### Slow down before you auto-approve

There’s a temptation, once an engineer gets comfortable with agentic coding, to skip straight to auto-approve. Don’t. Three things happen when engineers skip the manual-approval stage too fast. PRs get huge. The engineer doesn’t actually read every line of the diff. **Test code drops in quality first, because test code gets reviewed less carefully than production code.** Airbnb’s Level 3 (auto-approve plus diff review) is a learned skill, not a default. Szczepan said it cleanly:

> An engineer may create very large PRs that they don’t review fully. They don’t actually understand and review every single line of code. They may not review test code as eagerly as the production code.

**The fix, when you’re in the loop, is to push back on the tool when it’s confidently wrong.** Szczepan walked through it.

> You don’t trust it. If something feels suspicious, you ask it: “Why did you do this in line 120?” And after a couple of rounds, you get to this satisfying moment where the agentic tool gives up and says, “Oh yeah, you’re right. I’m sorry. I was wrong. Let’s fix it.”

That’s not friction. That’s the practice.

### Close the skill gap fast

This one comes from Mike’s lived experience, not a number on a slide. Mike is a college dropout who admits he doesn’t know Git from the command line. With agents, he ships across multiple languages.

> I’m one of those non-believers. This is all going to be slop. This is all going to be vibe coding. This is going to be worse than what I can write by hand. And when I was using GPT 3.5, that was true. I personally got lapped by agentic coding.

He said. **In Mike’s team’s setup, the gap between agentic-fluent and non-agentic engineers widened faster than anyone predicted.**

Definition, principles, learnings. Now plot where you actually are.

---

## Plot your team on the grid

Reading the principles and learnings is one thing. Doing something with them this quarter is another. **The grid below is the diagnostic.** It’s not a model of who you are. It’s a map of where to invest next.

The grid has two axes. The vertical axis is median engineer fluency. The horizontal axis is org infrastructure. For the vertical axis, plot the median engineer on your team, not your top performer. Airbnb published a four-level fluency ladder that travels well.

![hand-drawn four-rung ladder showing the agentic coding fluency journey. Rung 1: First Steps, autocomplete and copy-paste. Rung 2: Agentic Learner, agentic tool with manual approval. Rung 3: Advanced Practitioner, auto-approve and parallel sessions. Rung 4: Pioneer, building MCPs and leading team transformation. A small figure climbs the ladder.](https://substackcdn.com/image/fetch/$s_!8o8U!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F585362aa-0174-42ab-b2da-233c624ebc04_2816x1536.png)

hand-drawn four-rung ladder showing the agentic coding fluency journey. Rung 1: First Steps, autocomplete and copy-paste. Rung 2: Agentic Learner, agentic tool with manual approval. Rung 3: Advanced Practitioner, auto-approve and parallel sessions. Rung 4: Pioneer, building MCPs and leading team transformation. A small figure climbs the ladder.

- **Level 1 is first steps.** Autocomplete, occasional chat, copy-paste from ChatGPT.
- **Level 2 is agentic learner.** Uses an agentic tool with manual approval; improving prompts and configs.
- **Level 3 is advanced practitioner.** Auto-approves, reviews diffs, runs parallel sessions across multiple workspaces.
- **Level 4 is pioneer.** Builds custom MCPs, leads team transformation.

**One caveat that matters: Level 4 (pioneer) is an organizational role, not just a personal skill.** It requires platform-team mandate and org permission, not only individual fluency. Pioneers are usually the output of being in Multiplier mode (the top-right cell of the grid), not a prerequisite.

For the horizontal axis, ask plainly: is there a champions network, paved paths, internal MCP servers, sandboxed environments? Or is everyone on their own? You’ll know within five minutes.

![hand-drawn 2x2 grid. The vertical axis is median engineer fluency from mostly beginners to mostly power users. The horizontal axis is org infrastructure from none/scattered to paved (champions, MCP servers, sandboxes). The four cells are named: Tourist phase (bottom-left), Hero phase (top-left), Onboarded but underused (bottom-right), Multiplier mode (top-right with a small star). Small arrows point each cell toward Multiplier mode. ](https://substackcdn.com/image/fetch/$s_!c2YS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd446ee8d-7666-41fa-b29e-2102d5e67ac7_2816x1536.png)

hand-drawn 2x2 grid. The vertical axis is median engineer fluency from mostly beginners to mostly power users. The horizontal axis is org infrastructure from none/scattered to paved (champions, MCP servers, sandboxes). The four cells are named: Tourist phase (bottom-left), Hero phase (top-left), Onboarded but underused (bottom-right), Multiplier mode (top-right with a small star). Small arrows point each cell toward Multiplier mode.

Each cell has a name, a description, and a next-move sentence for you.

- **Tourist phase (low fluency, low infrastructure).** Everyone copy-pastes from ChatGPT. No champions, no shared standards, no one paving anything.
	- **Next move:** push for one champion in your tech team and one paved tool. Don’t try to do five things at once. Sequencing matters more here than ambition.
- **Hero phase (high fluency, low infrastructure).** One or two senior engineers shipping miracles with agentic coding. The rest of the team hasn’t moved. The seniors burn out, leave, or get poached.
	- **Next move:** make the cost-of-burnout case to leadership. The hero’s productivity doesn’t scale without the infra.
- **Onboarded but underused (low fluency, high infrastructure).** The tools exist, the infra is paved, but engagement is flat. Usually a culture gap, not a skills gap.
	- **Next move:** push for three Shopify-style moves. Visible leader use (a senior engineering leader ships a PR with an agent during the next all-hands). A paved-path simplification audit (every extra click between an engineer and an agent kills adoption). And AI-fluency woven into performance reviews, not as a productivity metric but as an expectation. Not more tools.
- **Multiplier mode (high fluency, high infrastructure).** This is where Airbnb’s 64% PR adoption lives. Power users running five parallel sessions, MCP ecosystem growing organically, the working group of champions teaching everyone else.
	- **Next move:** defend the budget, bring product into agentic workflows (PMs prototyping with the same loop), start measuring time-to-market shifts.

The 2x2 is the headline. The roadmap lives in a row-by-row diagnostic with seven categories: direction and adoption posture, measurement, tooling stack, internal context, engineer skill journey, org structure, and quality bar. Each category has two or three rows. Each row asks one question. ”What does your team actually have here?” Fill in the empties. Count them. **Pick one row to push for this quarter. Not five.**

![hand-drawn report-card sheet titled “Your team’s roadmap” with seven horizontal rows labeled with the seven categories of the readiness checklist. Each row has two or three empty checkboxes and hand-drawn underlines suggesting “fill in your answer here.” A pencil rests at the bottom-left corner.](https://substackcdn.com/image/fetch/$s_!IdMw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02ed7678-bae3-479e-98b4-97d4c1c7dc35_2816x1536.png)

hand-drawn report-card sheet titled “Your team’s roadmap” with seven horizontal rows labeled with the seven categories of the readiness checklist. Each row has two or three empty checkboxes and hand-drawn underlines suggesting “fill in your answer here.” A pencil rests at the bottom-left corner.

Paste it into a Google Doc, fill in the “Where you are” column row by row, and bring it to your next 1:1. The empties are your roadmap.

One honest caveat. This grid is a snapshot of one company’s landing point and what travels from it. Your context is different. Your org is smaller. The talk is six months old in AI time. **Use the grid as a starting point, not a verdict. Use the checklist as a conversation starter, not a scorecard.** Revisit it in 90 days.

Once you know where you are, the upstream conversation changes.

---

## Bring it to your CTO on Monday

Drop this sentence in the 1:1. Replace the bracketed bits with what you plotted.

> Our AI tool was step 1. On the grid, we’re in \[cell name\]. On the checklist, we have empties in \[row X\], \[row Y\], and \[row Z\]. The next investment we should make is \[the row that unblocks the others\]. Here’s why it matters for time to market.

That’s the line that reframes the conversation. The unanswerable version is “what’s the ROI on our AI coding tool?” The answerable version is “where are we on agentic coding maturity, and what’s the next investment?” **The grid gives the headline. The checklist gives the specifics.** Your CTO can disagree with the cell. She can argue about the next investment. She can’t pretend you haven’t done the work.

Four moves for the week, in order.

1. **Watch the [35-minute talk](https://youtu.be/o6oYc9-X9Iw).** You can do this over a coffee.
2. **Plot your tech function on the grid.** Fifteen minutes.
3. **[Read the checklist](https://docs.google.com/document/d/11BG_m9-e0kcuwVp-ycy9fO6kcHhIeH6elt8BMoRvbqM/edit?usp=sharing)**, copy it, fill the “Where you are” column row by row. Honest beats complete. Thirty minutes.
4. Schedule a 30-minute 1:1 with your CTO. Send the filled checklist before the meeting. Pick the one row you want her to fund this quarter.

The principles travel. The specifics don’t. Your context isn’t theirs. **Trust your read over the diagnostic.** Reply and tell me where you plotted your team!

---

∙
