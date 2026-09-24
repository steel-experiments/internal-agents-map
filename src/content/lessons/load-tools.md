---
title: Two ways to discover tools
description: Cloudflare searches tool schemas; Sentry connects to providers on demand. Each design adds a dependency during the task.
eyebrow: 05 / Tools and context
lede: Cloudflare searches tool schemas; Sentry connects to providers on demand.
summary: Cloudflare and Sentry defer different parts of tool setup until a task needs them.
readingTime: 2 min read
order: 5
publishedAt: '2026-09-11'
updatedAt: '2026-09-16'
relatedAgentIds:
  - cloudflare-ai-stack
  - sentry-junior
sources:
  - id: '1'
    title: 'Cloudflare: Our internal AI engineering stack'
    url: https://blog.cloudflare.com/internal-ai-engineering-stack/
    note: Tool schema overhead and portal-level search.
  - id: '2'
    title: 'Sentry: Building an intern'
    url: https://cra.mr/building-an-intern/
    note: Progressive discovery and provider connections.
---

<section aria-labelledby="two-discovery-paths">

## Two discovery paths

Cloudflare measured roughly 15,000 tokens for 34 GitLab tool schemas before the model started a task. Its portal now exposes search and execution functions in place of every upstream definition. The agent searches for a capability, then uses the selected tool. [[1]](#source-1)

Sentry's Junior initially connects to no Model Context Protocol (MCP) provider. MCP gives the agent access to tools. Junior requests a lookup for a named provider, connects to it, and discovers its tools when needed. [[2]](#source-2)

| Design | What is available initially | What discovery adds |
| --- | --- | --- |
| Cloudflare portal | Search and execution functions | The tool schema needed for a particular operation |
| Sentry Junior | A way to request a provider's tools | A provider connection and its available tools |

The two designs defer different work. Cloudflare searches across a catalog of schemas; Junior first needs to reach the relevant provider. This puts connection failures and search failures at different points in the task.

</section>

<section aria-labelledby="discovery-can-fail-before-execution">

## Discovery can fail before execution

Our interpretation is that these designs exchange upfront context for a dependency during the task. A search can return the wrong capability. A provider can be unavailable or fail authorization. A useful tool can also have a description that prevents the agent from finding it.

Those failures need to be distinguished from a tool that was found but returned an error. Cloudflare's context measurement supports the overhead concern; it does not establish an accuracy improvement. For a small, stable set of tools, discovery would add another operation whose benefit still needs measurement.

</section>
