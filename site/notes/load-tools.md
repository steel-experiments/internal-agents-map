Source: https://internal-agents.com/notes/load-tools.html

[← Notes](https://internal-agents.com/notes.html)

05 / Tools and context

# Load tools when the task needs them

An agent can find a tool before it loads the details.

11 September 2026 · 2 min read

## What the teams report

Cloudflare found that tool definitions used context space before any task started. Its portal now exposes search and execution tools instead of every definition. [[1]](https://internal-agents.com/notes/load-tools.html#source-1)

Sentry’s Junior starts without a connection to an MCP provider. Model Context Protocol (MCP) connects agents to tools. Junior connects after the agent requests a tool lookup. [[2]](https://internal-agents.com/notes/load-tools.html#source-2)

Browserbase loads skills for each task. These skills contain instructions for specific work. They are separate from the tools that perform actions. [[3]](https://internal-agents.com/notes/load-tools.html#source-3)

> “keep the always-on surface small”

Sentry, on progressive tool discovery. [[2]](https://internal-agents.com/notes/load-tools.html#source-2)

01 **Start small** Core tools and instructions

02 **Find a tool** Search for the capability

03 **Use the tool** Load the required details

Our simplified illustration of tool discovery. Skills supply instructions and may load separately.

Our observation

## More tools need not mean more initial context

Tool discovery can separate available capabilities from the context supplied at the start of a task.

This adds a dependency: the agent must find the correct tool. A missing or unclear tool description can prevent that step.

A small tool set may not need discovery. The reports do not establish that fewer tool definitions always improve accuracy.

**A question for your build** Can the agent find the right tool without first reading every tool definition?

## Sources

1. [Cloudflare: Our internal AI engineering stack](https://blog.cloudflare.com/internal-ai-engineering-stack/) Tool schema overhead and portal-level search.
2. [Sentry: Building an intern](https://cra.mr/building-an-intern/) Progressive discovery and provider connections.
3. [Browserbase: Internal agents](https://browserbase.com/blog/internal-agents) Task-specific skills and a small core tool set.

[Cloudflare in the catalog](https://internal-agents.com/index.html#cloudflare-ai-stack) [Sentry in the catalog](https://internal-agents.com/index.html#sentry-junior) [Browserbase in the catalog](https://internal-agents.com/index.html#browserbase-bb)

[All notes](https://internal-agents.com/notes.html) [Next: Some steps do not need a model →](https://internal-agents.com/notes/steps-without-a-model.html)
