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

- **Sierra (Pinecone)** routes between Claude Code and Codex by *intent* (planning, coding,
  prose) and explicitly owns the routing/context layer instead of one model.
- **Linear** spans families: GPT-5 / Gemini 2.5 Pro for triage, Claude Code or Codex for
  coding sessions.
- **Spotify (Xirp/Honk)** runs 50+ parallel sessions with the model swappable mid-task.
- **monday.com** wraps the Claude Agent SDK in a thin layer to keep the provider portable.
- **Block** builds Builderbot on **goose** (a framework), not on one model.
- **Coinbase** deliberately runs a *portfolio* — Claude Code, OpenCode, Cursor, Copilot.
- **Shopify** states it directly: "the runtime is commoditizing; the value is in the harness
  + integrations."

The consequence: **don't build your moat in the model.** Build it in the layers below.

---

## Reference architecture

Lay the entries side by side and a single shape emerges. Work arrives from where employees
already are, flows down through context → harness → sandbox → scoped tools → verification,
lands in an existing system of record, and hands consequential decisions to a human — with
feedback feeding back into the platform.

```text
Slack / Linear / Jira / GitHub / alert / cron
        ↓
control + orchestration plane  (identity, policy, task state)
        ↓
company context layer           (code, catalog, docs, telemetry, data, tickets)
        ↓
harness / model router          (swappable models + runtimes)
        ↓
ephemeral execution sandbox     (zero standing credentials)
        ↓
scoped tools                    (MCP gateway, narrowly authorized APIs)
        ↓
deterministic verification      (tests, CI, lint, EXPLAIN, schema checks)
        ↓
LLM review / judge              (where useful)
        ↓
human approval                  (consequential writes)
        ↓
system of record                (GitHub / Linear / Salesforce)
        ↓
evaluation + failure data ──► back into skills & platform
```

The single most important property of this shape: **each layer is independently swappable.**
You should be able to change Claude to Codex, OpenCode to another harness, or one sandbox
provider to another without rebuilding identity, integrations, context, or workflow state.
(Horizon, Pinecone, and `bb` all demonstrate why — see [WorkOS](../data/agents/workos-project-horizon.yaml),
[Sierra](../data/agents/sierra-pinecone.yaml), [Browserbase](../data/agents/browserbase-bb.yaml).)

---

## 1. Execution / sandbox

A place where agent-written code runs, isolated from production and from the developer's
laptop. Every serious build has one.

| Company | Sandbox |
| --- | --- |
| DoorDash (Flux) | Firecracker microVMs; <5s p95 cold start |
| Ramp (Inspect) | Modal sandboxes; per-repo images rebuilt every 30 min; warm-on-keystroke |
| Browserbase (bb) | Ephemeral Linux VM; pre-warmed snapshot; idles out after 30 min |
| Cloudflare | Dynamic Workers + Sandbox SDK |
| WorkOS (Horizon) | Cloudflare Containers + Sandbox SDK; disposable, scoped, with egress controls |
| Sierra (Pinecone) | Agency layer — recoverable Kubernetes runners; durable state kept separately |
| Spotify (Honk) | Constrained Kubernetes container; does not inherit engineer credentials |
| monday.com | Amazon EKS, one pod per session; remote sandbox tests each PR before review |
| Shopify | Execution env (fs/shell/repo/build) separated from the harness |
| Sentry (Junior) | Vercel serverless + agent-browser sandbox + MITM proxy |
| Coinbase (Mux) | Pragmatic isolation — each concurrent agent gets its own worktree, branch, terminal |
| Dropbox (Nova) | Isolated env with a codebase snapshot at a specific commit |

Two lessons repeat: **pre-warm and snapshot** (Ramp, Browserbase, DoorDash push setup into an
image-build step so the user never waits), and **keep the sandbox disposable**. Shopify's
framing is the cleanest: *"decouple brain from hands."* The deeper implication
(Sierra, WorkOS): **durable session state and ephemeral compute are separate primitives** —
you can kill a compromised or failed worker without losing the work object.

---

## 2. Harness / runtime

The agent loop — what calls the model, parses tool calls, manages the conversation. Three
stances appear:

- **Wrap a vendor SDK and stay portable.** monday.com (Claude Agent SDK + thin wrapper),
  Ramp (OpenCode, server-first), Browserbase (OpenCode core loop), WorkOS (OpenCode, later
  Claude Remote Routines — same platform, swappable harness).
- **Orchestrate multiple agents.** Block (Builderbot, on goose + MCP), Replit (a manager
  agent that spawns sub-agents), Slack (coordinator/dispatcher with expert + critic agents),
  Sierra (app server + Agency + runners).
- **Build the runtime yourself.** Sentry (Junior) built a custom harness with a task broker
  to control interrupt/resume semantics that serverless demands.

The harness is also where **model routing** lives (Sierra's intent router, Cloudflare's AI
Gateway, monday's inference profiles) and where **verification hooks** attach (Ramp's
write-blocking plugin; Dropbox's validation loop with `max_iterations`; Spotify's verifiers).

---

## 3. Session / harness / sandbox — keep them separate

Shopify's three-way split is worth calling out on its own, because several others converge
on the same shape:

- **Session** — durable identity and the append-only event log (Postgres). Survives everything.
- **Harness** — the cheap, disposable agent loop. Dies freely.
- **Sandbox / Cell** — the ephemeral execution runtime. Dies freely.

monday.com separates durable state (S3), live state (ElastiCache), and the per-session pod
(EKS) along the same lines; WorkOS separates the sandbox (execution primitive) from the
orchestrator (control plane); Sierra keeps conversation/checkpoints durable while runners are
ephemeral. **Session survival is non-negotiable** — cells die, sandboxes die, machines die;
the conversation can't.

---

## 4. The tool & access layer

How the agent reaches your internal systems — and how you stop it from reaching the wrong
ones. Most of the real engineering lives here.

**MCP as the connective tissue.** DoorDash's Agent Gateway, Cloudflare's MCP Server Portal
(182+ tools, 13 servers, one OAuth point), **Sierra's MCP Gateway spanning 37 systems**,
WorkOS's custom MCP, Block's MCP, Sentry's progressive-discovery MCP, and Brex's MCP all
converge on MCP as the way to expose internal capabilities.

**Credential brokering, not credential sharing.** The strongest pattern in the catalog: *the
agent never holds a secret.*

- Browserbase: sandbox boots with references + rotating tokens only; the proxy holds the real
  credentials; access scoped *by operation* (e.g. select-only warehouse).
- Sentry: a MITM proxy injects tokens host-side — "the model never has access to the token,
  because it's never in the sandbox."
- WorkOS: all outbound traffic proxied through Workers; tokens injected without exposure.
- Sierra: a network proxy decides whether privileged requests may proceed and injects
  credentials *after* approval — the harness never possesses the real secret.
- Cloudflare: zero API keys on client machines — a Worker injects them server-side.

**Collapse the tool surface.** Tool schemas eat context. Cloudflare measured 34 GitLab tools
≈ 7.5% of a 200K-token window and built **Code Mode** to collapse N schemas into search +
execute. Sentry reaches the same conclusion via **progressive discovery** — Junior connects
to no MCP provider by default until the agent requests a tool lookup.

---

## 5. Skills / playbooks

Encoded, reusable knowledge — the difference between an agent that flails and one that ships
like your best engineer. Two styles:

- **Declarative playbooks.** DoorDash (YAML units), Shopify and Sentry (markdown skills
  loaded on demand), monday.com (automated PR Guardrails), Sentry ("skills-as-runbooks").
- **Progressive disclosure.** Browserbase and Sentry keep the general-purpose agent small and
  load domain knowledge lazily.

> **Lesson:** *skills are where company-specific value compounds.* The model is a commodity;
  the playbook that knows your release process is not.

---

## 6. One agent, many skills — not one bot per department

A pattern the newer entries make unmistakable: **collapse departmental bots into one
general-purpose runtime with composable skills.** Cross-functional jobs don't respect
org-chart boundaries.

- **Sierra** began with separate PINE (support), Pinewood (analytics), Pinecone (engineering),
  and Reggie Jr (sales) agents — then intentionally collapsed them into one Pinecone.
- **Browserbase** chose one `bb` loop with dynamically loaded skills over one bot per use case.
- **Sentry** CEO David Cramer argues one general-purpose agent connected to many systems beat
  several vendor-specific bots.
- **Domu** split Clementino into a reusable tool/skill/memory layer powering multiple surfaces.

The exception proves the rule: keep specialized agents only where the *safety policy or
environment* genuinely differs (WorkOS's independent verification/security agents). Creating
a "Sales Agent," "Finance Agent," and "Engineer Agent" just because the org chart has those
departments is increasingly hard to justify.

---

## 7. The context / knowledge layer — "the system around the code"

Agents that can read code but can't see the system around it are working blind (Cloudflare's
words).

- **Service catalogs.** Spotify's Backstage/Portal; Cloudflare's Backstage (2,055 services)
  + AGENTS.md across ~3,900 repos.
- **Repo-context files.** AGENTS.md / CLAUDE.md (Cloudflare, WorkOS, Shopify's "World"
  monorepo, Dropbox's per-service files).
- **Memory as files, not vectors.** monday.com (MEMORY.md + daily diary); Sentry (Redis
  transcripts + repo search). **Domu** models memory as four explicit layers: conversation,
  persistent facts, knowledge RAG, and live system state.
- **Hybrid retrieval.** DoorDash runs the most explicit traditional stack: BM25 + dense
  semantic + reciprocal-rank fusion → RAG; schema-aware SQL with `EXPLAIN` validation.
- **Structured workspace as context.** Linear evolved from vector search into agentic context
  acquisition; Coinbase treats Linear as the agent's structured product context.

---

## 8. Invocation surfaces — meet work where it already is

Define an agent once; invoke it from Slack, GitHub, cron, CLI, web, or Chrome. But the
dominant surface, overwhelmingly, is **Slack** — because that's where work already lives:
Block, Browserbase, Ramp, Sentry, Shopify (River), monday.com, Brex, WorkOS, Coinbase,
Sierra, Stripe, Flex, Replit all center on Slack.

**Public beats private.** Shopify's River operates only in public channels, never DMs, so
every session is visible and learning spreads; Ramp and DoorDash reach the same conclusion.

**Systems of record stay systems of record.** Linear, Jira, and GitHub are *not* chat
destinations — they hold durable state. WorkOS listens to Linear/GitHub webhooks and writes
back; Coinbase keeps Linear as structured context; Sierra argues GitHub should own the PR,
Salesforce the account, Linear the issue, while Pinecone spans them.

---

## 9. Context management for long runs

Once a run spans hundreds of steps and megabytes, "pass everything every turn" overflows the
window. The advanced builds treat context management as its own subsystem:

- **Slack** — three structured channels: Director's Journal (working memory), Critic's Review
  (credibility-weighted findings), Critic's Timeline (deduped chronological synthesis).
- **monday.com** — file-based memory + monday boards (Builders CoWORK) as shared state.
- **Sentry** — incremental transcript updates in Redis + GitHub-event subscriptions.
- **Domu** — four-layer memory with distinct lifecycles.

---

## 10. Governance & permissions — make misbehavior structurally impossible

The shared posture: **don't trust the model; remove its ability to do wrong.**

- Scope tools/services per invocation source (Browserbase — RBAC + ABAC per session; Sierra —
  employee permissions enforced at the tool-call layer via the Gateway).
- Same identity/RBAC as humans, with real accounts (monday.com; Salesforce — "sees only what
  the employee can see").
- Per-user authorization for writes (Sentry; Linear — "an agent cannot be held accountable").
- Data-handling rules that follow the data (Brex; Cloudflare Zero Trust).
- Bounded autonomy: step/time budgets and circuit breakers (DoorDash); approval gates on
  customer-impacting actions (Domu); hard service/function limits on webhook jobs (Browserbase).

The rule that captures all of it, from DoorDash and Sierra's practice:

> **The probabilistic agent should decide *what to attempt*; deterministic infrastructure
> should decide *what it is permitted to do*.**

monday.com frames the discipline: *AI engineering is building the feedback loops that let
imperfect agents be trusted safely.*

---

## 11. The autonomy spectrum

Where you sit on this axis is the most consequential design choice, and the catalog spans all
four levels:

| Level | Example |
| --- | --- |
| **Assistive** — human drives | (IDE copilots; less represented here) |
| **Human-in-loop** — human in each cycle / approves writes | Brex, Dropbox, Sentry, Slack, Domu, Zup, Y Combinator |
| **Drafts-reviewed** — drafts work product a human reviews | DoorDash, Spotify, Ramp, Browserbase, Cloudflare, Linear, Shopify, WorkOS, Block, Coinbase, Sierra, Stripe, Harvey, Replit, Flex, Salesforce, Uber |
| **Autonomous** — ships without human review | monday.com **Morphex** (19 of 20 PRs merge with no human review) |

Three patterns worth stealing: **gradual autonomy** (Linear: suggestions → observe →
automate once proven); **tiered systems within one platform** (monday Atlas = drafts-reviewed,
Morphex = autonomous; Brex L1/L2/L3); and **earn complexity by exhausting simpler primitives
first**. DoorDash's maturity model keeps deterministic workflows for repeatable jobs, single
agents for exploration, deep-agent hierarchies for long-horizon work, and swarms only at the
research frontier — and warns that governance hardens as control decentralizes. Coinbase's Mux
is the simpler-than-swarm alternative: one human coordinating many isolated coding agents.

And the canonical caution from Brex: *target 40% automation, not 100%* — the last mile is
where investments go to die.

---

## 12. Background vs interactive; evals & model routing

- **Background agents win where speed is solved.** Ramp: a fast background agent is *strictly
  better* than local — same intelligence, more power, unlimited concurrency. DoorDash,
  Spotify, Shopify, Block, WorkOS, Stripe all run agents that work while you do something else.
- **Evals from day one.** monday.com's most-cited regret: day one, not month nine.
  Cloudflare's AI Gateway, Spotify's LLM-as-judge + MLflow, Brex's prompt/eval studio,
  DoorDash's DeepEval + LLM-as-judge all put measurement ahead of capability.
- **Route by task.** Sierra and Cloudflare route between frontier and cheaper models per
  workload; the model layer is a portfolio.

---

### Patterns at a glance

- The model is a swappable layer; build value in harness, context, tools, perms, evals, sandbox.
- Keep control plane, context, harness, and execution as separately swappable layers.
- Pre-warm and snapshot the sandbox; keep it disposable; decouple brain from hands.
- Broker credentials — the agent never holds a secret.
- Collapse the tool surface (Code Mode / progressive discovery).
- One agent, many skills — don't build a bot per department.
- Encode company knowledge in skills/playbooks and AGENTS.md; use a service catalog.
- Default to Slack; default to public; keep systems of record as systems of record.
- The probabilistic agent decides what to attempt; deterministic infrastructure decides what's permitted.
- Climb the autonomy spectrum gradually; earn complexity; evals from day one.
