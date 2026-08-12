# Patterns: the architecture of an internal agent

This is the synthesis layer of the map. Each catalog entry ([`data/agents/`](../data/agents/) →
[full catalog](landscape.md)) is one company's instantiation; this document pulls the
recurring architecture apart into primitives so the next team can pick deliberately instead
of re-deriving them.

It is hand-curated — edit it directly (no build step) and cite the companies you draw from.

---

## The thesis

> An internal agent is **not a model with a prompt**. It's a stack — **agent harness +
> company context + tools + identity/permissions + evals + execution environment** — with
> the model plugged in underneath and, increasingly, interchangeable. The proprietary value
> lives in the harness and integrations, not the model.

Every advanced build in this catalog treats the model as a swappable layer:

- **Spotify (Xirp)** coordinates 50+ parallel sessions, each in its own worktree, with the
  model swappable mid-task across Claude Code, Gemini CLI, Codex, and self-hosted open
  weights.
- **monday.com** wraps the Claude Agent SDK in a thin `monday-agent-sdk` layer specifically
  to keep the provider swappable, and routes across Bedrock inference profiles with
  cross-region failover.
- **Shopify** states it directly: "the runtime is commoditizing; the value is in the
  harness + integrations."
- **Dropbox (Nova)** runs multiple coding agents behind one interface so models can be
  swapped without rebuilding the platform.
- **Cloudflare** routes a growing share of workloads to cheaper self-hosted open-weight
  models (Workers AI) alongside frontier models.

The consequence: **don't build your moat in the model.** Build it in the layers below.

---

## 1. Execution / sandbox

A place where agent-written code runs, isolated from production and from the developer's
laptop. This is table stakes — every serious build has one — and the choices are
surprisingly consistent.

| Company | Sandbox |
| --- | --- |
| DoorDash (Flux) | Firecracker microVMs; <5s p95 cold start |
| Ramp (Inspect) | Modal sandboxes; per-repo images rebuilt every 30 min; warm-on-keystroke |
| Browserbase (bb) | Ephemeral Linux VM; pre-warmed snapshot; idles out after 30 min |
| Cloudflare | Dynamic Workers + Sandbox SDK |
| WorkOS (Horizon) | Cloudflare Containers + Sandbox SDK; disposable, scoped, with egress controls |
| monday.com | Amazon EKS, one pod per session; remote sandbox tests each PR before review |
| Shopify | Execution env (fs/shell/repo/build) separated from the harness |
| Sentry (Junior) | Vercel serverless + agent-browser sandbox + MITM proxy |
| Dropbox (Nova) | Isolated env with a codebase snapshot at a specific commit |

Two lessons repeat: **pre-warm and snapshot** (Ramp, Browserbase, DoorDash all push setup
into an image-build step so the user never waits), and **keep the sandbox disposable** so a
bad run costs nothing. Shopify's framing is the cleanest: *"decouple brain from hands."*

---

## 2. Harness / runtime

The agent loop itself — what calls the model, parses tool calls, manages the conversation.
Three stances appear:

- **Wrap a vendor SDK and stay portable.** monday.com (Claude Agent SDK + thin wrapper),
  Ramp (OpenCode, server-first), Browserbase (OpenCode core loop), WorkOS (OpenCode
  preconfigured). Portable, but you inherit the SDK's opinions.
- **Orchestrate multiple agents.** Block (Builderbot) is explicitly "an orchestration layer
  that coordinates multiple AI agents"; Slack runs a coordinator/dispatcher with separate
  expert and critic agents.
- **Build the runtime yourself.** Sentry (Junior) built a custom harness on Pi's SDK with a
  task broker, explicitly to control the interrupt/resume semantics that serverless demands.

The harness is also where the **model catalog and routing** live (Cloudflare's AI Gateway,
monday's inference profiles) and where **verification hooks** attach (Ramp's plugin that
blocks writes until sync completes; Dropbox's validation loop with `max_iterations`).

---

## 3. Session / harness / sandbox — keep them separate

Shopify's three-way split is worth calling out on its own, because several others converge
on the same shape without naming it:

- **Session** — durable identity and the append-only event log (Postgres). Survives everything.
- **Harness** — the cheap, disposable agent loop. Dies freely.
- **Sandbox / Cell** — the ephemeral execution runtime. Dies freely.

The payoff: you can swap any one layer without touching the others, and a dead cell or
sandbox never kills the conversation. monday.com separates durable state (S3), live state
(ElastiCache), and the per-session pod (EKS) along the same lines; WorkOS separates the
sandbox (execution primitive) from the orchestrator (control plane).

> **Lesson:** *session survival is non-negotiable.* Cells die, sandboxes die, machines die.
> The conversation can't.

---

## 4. The tool & access layer

How the agent reaches your internal systems — and how you stop it from reaching the wrong
ones. This is where most of the real engineering lives.

**MCP as the connective tissue.** DoorDash's "Agent Gateway," Cloudflare's MCP Server
Portal (one OAuth point aggregating 182+ tools from 13 servers), WorkOS's custom MCP
server, Block's MCP, and Sentry's progressive-discovery MCP all converge on MCP as the way
to expose internal capabilities. Brex even uses MCP to expose *product* features to internal
agents, so new product tools become internally available immediately.

**Credential brokering, not credential sharing.** The strongest pattern in the whole
catalog: *the agent never holds a secret.*

- Browserbase: the sandbox boots with references + rotating session tokens only; the proxy
  holds the real credentials.
- Sentry: a MITM proxy injects tokens host-side — "the model never has access to the token,
  because it's never in the sandbox."
- WorkOS: all outbound traffic is proxied through Workers; tokens are injected without
  exposure; engineers use their own identity, scoped and short-lived.
- Cloudflare: zero API keys on client machines — a Worker injects them server-side.

**Collapse the tool surface.** Tool schemas eat context. Cloudflare measured 34 GitLab tools
≈ 7.5% of a 200K-token window, and built **Code Mode** to collapse N tool schemas into a
search + execute pair, holding token overhead constant. Sentry reaches the same conclusion
differently with **progressive discovery** — Junior connects to no MCP provider by default
until the agent explicitly requests a tool lookup.

---

## 5. Skills / playbooks

Encoded, reusable knowledge — the difference between an agent that flails and one that ships
like your best engineer. Two styles:

- **Declarative playbooks.** DoorDash packages work as YAML units (task, inputs, skills,
  tools, permissions, validation, outputs). Shopify and Sentry write skills as markdown files
  loaded on demand. monday.com encodes engineering standards as automated **PR Guardrails.**
- **Progressive disclosure.** Browserbase and Sentry both keep the general-purpose agent
  small and load domain knowledge lazily, rather than front-loading every capability.

> **Lesson:** *skills are where company-specific value compounds.* The model is a commodity;
  the playbook that knows your release process is not.

---

## 6. The context / knowledge layer — "the system around the code"

Agents that can read code but can't see the system around it are working blind (Cloudflare's
words). The org-context layer is what turns a coding agent into *your* coding agent.

- **Service catalogs.** Spotify's Portal/Backstage gives every session ownership, dependency
  graphs, and architecture on init. Cloudflare generates AGENTS.md across ~3,900 repos and
  indexes 2,055 services in Backstage.
- **Repo-context files.** AGENTS.md / CLAUDE.md (Cloudflare, WorkOS, Shopify's "World"
  monorepo, Dropbox's per-service AGENTS.md) — structured, often *generated*, repo context.
- **Memory as files, not vectors.** monday.com explicitly skipped the vector store: memory
  is MEMORY.md (cross-session) plus a daily diary. Sentry persists transcripts in Redis and
  traces code paths by searching the repo.

---

## 7. Invocation surfaces — meet work where it already is

Define an agent once; invoke it from Slack, GitHub, cron, CLI, web, or Chrome. DoorDash and
Browserbase are explicit about this ("trigger the same playbook from Slack, GitHub, cron,
CLI, or a skill"). But the dominant surface, overwhelmingly, is **Slack** — because that's
where the work already is:

- Block (`@builderbot`), Browserbase (`bb`), Ramp, Sentry (Junior), Shopify (River),
  monday.com (@mention), Brex (`/c1`), WorkOS all live primarily in Slack.
- **Shopify's River is public-by-default** — it operates only in public Slack channels, never
  DMs, so every session is visible and learning spreads. Ramp and DoorDash reach the same
  conclusion: *public threads drive adoption; private ones don't.*

---

## 8. Context management for long runs

Once an agent run spans hundreds of steps and megabytes of output, naive "pass everything
every turn" overflows the window. The advanced builds treat context management as its own
subsystem:

- **Slack** keeps three structured channels: a Director's Journal (working memory), a
  Critic's Review (credibility-weighted findings), and a Critic's Timeline (deduped
  chronological synthesis).
- **monday.com** uses file-based memory plus monday boards (Builders CoWORK) as shared state.
- **Sentry** persists transcripts incrementally and subscribes to GitHub events for
  asynchronous follow-ups.

---

## 9. Governance & permissions — make misbehavior structurally impossible

The shared posture across the catalog: **don't trust the model; remove its ability to do
wrong.**

- Scope tools and services per invocation source (Browserbase — RBAC + ABAC per session).
- Same identity/RBAC as humans, with real accounts (monday.com).
- Per-user authorization for writes (Sentry: "for writes require per-user authorization";
  Linear: "an agent cannot be held accountable" — humans own the final approval).
- Data-handling rules that follow the data, not the tool (Brex: classification, ≤30-day
  retention, no training on inputs; Cloudflare Zero Trust).

monday.com frames the whole discipline succinctly: *AI engineering is building the feedback
loops that let imperfect agents be trusted safely.*

---

## 10. The autonomy spectrum

Where you sit on this axis is the single most consequential design choice, and the catalog
spans all four levels:

| Level | Example |
| --- | --- |
| **Assistive** — human drives, agent helps | (common in IDE copilots; less represented here) |
| **Human-in-loop** — acts, human involved each cycle / approves writes | Brex, Dropbox (Nova), Sentry (Junior), Slack, Y Combinator |
| **Drafts-reviewed** — autonomously drafts work product a human reviews before ship | DoorDash, Spotify, Ramp, Browserbase, Cloudflare, Linear, Shopify, WorkOS, Block |
| **Autonomous** — ships without human review | monday.com **Morphex** (19 of 20 PRs merge with no human review) |

Two patterns worth stealing: **gradual autonomy** (Linear: start with suggestions, observe,
add guidance, automate only once proven) and **tiered systems within one platform**
(monday.com's Atlas = drafts-reviewed, Morphex = autonomous; Brex's L1/L2/L3). And the
canonical caution from Brex: *target 40% automation, not 100%* — the last mile is where
investments go to die.

---

## 11. Background vs interactive; evals & model routing

- **Background agents are winning where speed is solved.** Ramp's argument: a background
  agent that's fast is *strictly better* than local — same intelligence, more power, unlimited
  concurrency. DoorDash, Spotify, Shopify, Block, WorkOS all run agents that work while you
  do something else.
- **Evals from day one.** monday.com's most-cited regret: evals should have been day one, not
  month nine. Cloudflare's AI Gateway, Spotify's LLM-as-judge + MLflow traces, and Brex's
  prompt/eval studio all put measurement ahead of capability.
- **Route by task.** Cloudflare and monday.com both route between frontier and cheaper
  self-hosted models per workload — the model layer is a portfolio, not a single choice.

---

### Patterns at a glance

- The model is a swappable layer; build value in harness, context, tools, perms, evals, sandbox.
- Pre-warm and snapshot the sandbox; keep it disposable; decouple brain from hands.
- Keep session, harness, and sandbox as separate layers.
- Broker credentials — the agent never holds a secret.
- Collapse the tool surface (Code Mode / progressive discovery).
- Encode company knowledge in skills/playbooks and AGENTS.md; use a service catalog.
- Default to Slack; default to public.
- Treat context management as its own subsystem for long runs.
- Don't trust the model — make misbehavior structurally impossible.
- Move up the autonomy spectrum gradually; evals from day one.
