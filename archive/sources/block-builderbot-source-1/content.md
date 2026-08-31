> Archived source snapshot  
> Source ID: `block-builderbot-source-1`  
> Original URL: <https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship>  
> Final URL: <https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship>  
> Title: Block - Block rolls out Builderbot, a new suite of AI-native tools that changes the way we ship  
> Captured at: `2026-08-31T17:39:51Z`

---

AI is native to how Block builds and ships. Over the past two years, we've invested in making AI foundational to how our engineers work: open sourcing [goose](https://goose-docs.ai/), our AI agent framework, co-developing the Model Context Protocol (MCP) with Anthropic, and building internal tools that bring AI into every engineer's daily workflow. Today, 100% of Block's engineers regularly use AI in their work.

Still, we kept hitting the same ceiling. Most coding tools work great in a single repo, but none of them could operate across hundreds of millions of lines of code, hundreds of services, and the full complexity of how a company like Block actually builds. So we built a new tool, Builderbot, to help us solve for implementation at scale.

**How it works**

Builderbot is an orchestration layer that coordinates multiple AI agents across our entire codebase. It works inside Slack: anyone can tag @builderbot with a short description of what they need, and it gets to work right there in the thread, whether it’s a bug fix, a migration across services, or a new feature. Multiple team members can collaborate with it in real time, watching it research, plan, and implement while they steer the direction. There's no context switching, the conversation is the development environment.

What makes this different from a coding assistant is scope. Builderbot understands the full context of Block's codebase, every service, every API, every convention, and can contribute to any piece of code at the entire company. An engineer working on Cash App can use it to make a change in a Square service they've never touched, because the system already knows how that service works. It picks up tickets directly from Linear and Jira, creates the branch, writes the code, opens the pull request, watches CI, and iterates based on feedback. Humans step in where humans add the most value.

It also operates on source code and system configuration only; it does not access or process customer data, payment information, or personally identifiable information.

**What it means for how we build**

Builderbot executes over 200,000 operations per day and merges approximately 1,500 pull requests per week, about 15% of all production code changes across Block. What used to take months now takes days.

"The best way to think about Builderbot is as the missing layer between AI coding tools and how engineering actually works at scale," said Brad Axen, Head of AI Capabilities at Block. "It handles the orchestration, the context, the environment, so our engineers can focus on the problems worth solving. On the Square side, we took a list of features sellers had been waiting on for months and our engineers shipped them in days. Builderbot handled the scaffolding and the repetitive work, and our engineers made the decisions that shaped the product. It means an idea can go from backlog to live in front of millions of customers in days instead of months."

**Open foundations**

Builderbot is built on goose, an open source agent framework we developed and contributed to the [Agentic AI Foundation](https://aaif.io/) (AAIF) under the Linux Foundation. The integration challenges we hit building goose inspired our collaboration with Anthropic on MCP, now an industry standard for connecting AI agents to tools and data sources.

We created Builderbot because we needed it. The problems we're solving aren't unique to Block: orchestrating AI agents across a massive codebase, maintaining quality at speed, keeping humans focused on judgment and taste rather than scaffolding. We're sharing how we built it because we think the shift from AI-assisted coding to AI-native engineering is one of the most important conversations happening in technology right now, and we want to contribute openly.
