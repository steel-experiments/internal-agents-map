# Further reading

This catalog is deliberately scoped to **companies building proprietary agents for their own
employees and internal workflows**. Commercial agents and general frameworks are *out of
scope as catalog entries* — but they show up constantly as the harnesses, runtimes, and
reference ideas used *inside* these stacks. This page collects them so contributors know
where the boundary is and where to read more.

## Why these aren't catalog entries

- **Commercial coding agents** (Devin, Cursor, Claude Code, etc.) are products sold to many
  companies, not an internal build for one. They appear here only when an entry uses them as a
  harness (e.g. Spotify Xirp runs Claude Code / Gemini CLI / Codex as interchangeable
  harnesses; Linear uses Codex for PR review).
- **Agent frameworks/SDKs** (Claude Agent SDK, LangGraph, OpenAI Agents SDK) are tooling, not
  organizations running agents internally. monday.com wraps the Claude Agent SDK; Sentry and
  others build on similar SDKs.
- **Agent products/infrastructure** (OpenAI Symphony, Anthropic/Claude, Vercel AI SDK, Kimi,
  etc.) are vendor offerings, not a single company's internal agent.

If you're unsure whether something belongs in the catalog, the test is: *did one organization
build this to run inside its own walls for its own people?* If yes → catalog entry. If it's a
product or framework many orgs adopt → it belongs here, or as a `harness`/`tool_access` note
inside an entry.

## Foundational agent concepts

- **Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents):**
  the canonical primer on the workflow-vs-agent distinction, tool use, and orchestration
  patterns. Much of this catalog is concrete instantiations of the ideas here.
- **Anthropic — multi-agent research systems** (the lead of [this work](https://www.anthropic.com/engineering)):
  relevant to Slack's coordinator/dispatcher pattern and Block's orchestration layer.

## Frameworks & runtimes used inside these stacks

- **[Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview):** the runtime
  behind monday.com's system (wrapped for provider neutrality).
- **[OpenCode](https://github.com/sst/opencode):** the server-first harness used by Ramp,
  Browserbase, and WorkOS.
- **[LangGraph](https://github.com/langchain-ai/langgraph):** graph-based agent orchestration
  — a common alternative for the coordinator/dispatcher shape.
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/):** the connective tissue
  for nearly every tool-access layer in this catalog (DoorDash Agent Gateway, Cloudflare MCP
  Server Portal, WorkOS/Block/Sentry/Brex MCP servers).

## Commercial coding agents (referenced as harnesses)

- **[Claude Code](https://claude.com/claude-code)**, **Cursor**, **Cognition Devin**,
  **GitHub Copilot Workspace** — the interchangeable harness layer that several entries plug
  in and swap between.

## Adjacent community efforts

- **The cross-company "internal agents" discussion** (e.g. the r/AI_Agents JSON thread
  surveying who is building what) — a useful discovery source for new entries.
- **`agentic-internet` / agent-landscape repos** — broader catalogs of agent companies and
  projects; complementary but broader in scope than this map.

## Within this repo

- [Patterns](patterns.md) — the architecture synthesis.
- [Adoption lessons](adoption-lessons.md) — how these systems get adopted.
- [Full catalog](landscape.md) — generated per-agent detail.
- [Schema](../data/schema.md) — how to add an entry.
