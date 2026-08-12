# Internal Agents Map

`A map and learning exchange for companies building proprietary AI agents for their own teams.`

A curated, open catalog of **internal agents**: the agent platforms companies build inside
their own walls for their own engineers and operators, plus the cross-cutting patterns and
adoption lessons that repeat across them. Anyone can add an agent or a lesson via pull request.

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-green.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What is an "internal agent"?

Not a chatbot, and not a vendor product. An internal agent is a system a company builds so
that AI does real work: writing and reviewing code, triaging CI, handling support and
finance ops, running migrations. It does that work as a member of the company's own
workforce.

What turns a model call into an **agent** is **durable identity**. It persists across
temporary runs, restarts, and even swapping out the model underneath, while keeping its
own state and authority. It remembers and acts; a stateless prompt does neither.

Behind that identity is a stack:

> **agent harness + company context + tools + identity/permissions + evals + execution
> environment**, with the model plugged in underneath and increasingly interchangeable.

The proprietary value is in the harness and the integrations, not the model, which is why
the model is the part teams swap most often. Spotify Xirp swaps it mid-task; monday.com
keeps its provider portable behind a thin wrapper; Sierra routes between Claude Code and
Codex by intent; Shopify calls the runtime a commodity. The full synthesis is in
[Patterns](docs/patterns.md).

### Scope

**Internal / proprietary builds only.** A company must have built this to run inside its own
organization for its own people, whether or not parts later ship externally (for example,
Spotify Xirp's beta, or Sentry's open-sourced Junior). Commercial agents (Devin, Cursor,
Claude Code) and frameworks (Claude Agent SDK, LangGraph) appear only as the harnesses and
dependencies used inside these stacks, listed in [Further reading](docs/further-reading.md),
not as catalog entries.

---

## The landscape

Sorted by company. Each row links to its [data file](data/agents/). The
[full catalog](docs/landscape.md) has the architecture, primitives, metrics, lessons, and
sources for each agent.

<!-- BEGIN LANDSCAPE -->

| Company | Agent | Domains | Autonomy | Sandbox | Interfaces | Status | Year |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Block | [Builderbot](data/agents/block-builderbot.yaml) | coding, code-review | drafts-reviewed | Not detailed publicly | slack, linear, jira, github | internal | 2026 |
| Brex | [Internal Agent Platform](data/agents/brex-agent-platform.yaml) | finance-ops, support, customer-success | human-in-loop | Retool-hosted runtime (no bespoke execution env described) | slack, internal-retool-ui | internal | 2026 |
| Browserbase | [bb](data/agents/browserbase-bb.yaml) | coding, code-review, support, customer-success, research | drafts-reviewed | Ephemeral Linux VM; pre-warmed snapshot rebuilt every 30 min; idles out after 30 min | slack, web-ui, webhook | internal | 2026 |
| Cloudflare | [Internal AI engineering stack](data/agents/cloudflare-ai-stack.yaml) | coding, code-review | drafts-reviewed | Dynamic Workers for sandboxed code execution; Sandbox SDK to clone/build/test | cli, ci, web | internal | 2026 |
| Coinbase | [Forge / Mux](data/agents/coinbase-forge-mux.yaml) | coding, code-review | drafts-reviewed | Mux gives each concurrent agent its own git worktree, branch, and terminal | slack, github, linear | internal | 2026 |
| Domu | [Clementino](data/agents/domu-clementino.yaml) | support, finance-ops, coding, recruitment, customer-success | human-in-loop | — | slack, desktop | internal | 2026 |
| DoorDash | [AI Code Review Agent](data/agents/doordash-code-review.yaml) | code-review | drafts-reviewed | — | github | internal | 2026 |
| DoorDash | [Flux / Agentic AI Platform](data/agents/doordash-flux.yaml) | code-review, coding, ci-triage, on-call, maintenance, data | drafts-reviewed | Firecracker microVMs; <5s p95 end-to-end setup (boot, clone repos, install tools, configure harness) | slack, github, cron, cli, conversational-skill, cursor | internal | 2026 |
| Dropbox | [Nova](data/agents/dropbox-nova.yaml) | coding, ci-triage, on-call, maintenance | human-in-loop | Isolated env with a codebase snapshot at a specific commit; full Dropbox monorepo via Bazel; hermetic remote execution + caching | web-ui, cli, api, slack | internal | 2026 |
| Flex | [AI Investigation Agent](data/agents/flex-investigation-agent.yaml) | finance-ops, on-call, coding | drafts-reviewed | Not specified publicly | slack | internal | 2026 |
| Harvey | [Spectre](data/agents/harvey-spectre.yaml) | coding, code-review, on-call, security | drafts-reviewed | Isolated ephemeral execution environments; durable runs | slack, web, automations | internal | 2026 |
| Linear | [Linear Agent](data/agents/linear-agent.yaml) | support, customer-success, coding | drafts-reviewed | Not detailed publicly | slack, intercom, linear-app, github | internal | 2026 |
| monday.com | [Sphera / Atlas / Morphex](data/agents/monday-sphera-atlas-morphex.yaml) | coding, code-review | autonomous | Amazon EKS, one pod per active session; a remote sandbox tests each PR before review; EFS workspace mount | slack, monday, github | internal | 2026 |
| Ramp | [Inspect](data/agents/ramp-inspect.yaml) | coding, code-review, on-call | drafts-reviewed | Modal sandboxes; per-repo images rebuilt every 30 min from snapshots; warm-on-keystroke; a pool of warm sandboxes | slack, web, chrome-extension, pull-request | internal | 2026 |
| Replit | [Manager agent (agent-of-agents)](data/agents/replit-manager-agent.yaml) | coding, code-review, support, research, data | drafts-reviewed | Not specified publicly | slack | internal | 2026 |
| Salesforce | [Slackbot](data/agents/salesforce-slackbot.yaml) | support, customer-success, ops | drafts-reviewed | — | slack | commercialized | 2026 |
| Sentry | [Junior](data/agents/sentry-junior.yaml) | coding, code-review, support, on-call | human-in-loop | Vercel serverless functions; Vercel agent-browser sandbox with a MITM proxy for traffic interception; ephemeral containers | slack, web-dashboard, github | open-sourced | 2025 |
| Shopify | [Aquifer / River](data/agents/shopify-internal-agents.yaml) | coding, code-review, research, security | drafts-reviewed | An execution environment (filesystem, shell, repo, build/test), separated from the harness — 'decouple brain from hands' | slack, github | internal | 2026 |
| Sierra | [Pinecone](data/agents/sierra-pinecone.yaml) | coding, code-review, support, research, data | drafts-reviewed | Agency layer reconciles recoverable Kubernetes runners; conversation/events/checkpoints stay durable separately | slack, web, linear, mobile | internal | 2026 |
| Slack | [Multi-agent context system](data/agents/slack-context-system.yaml) | research | human-in-loop | n/a — this is a context-management pattern, not a full execution platform | — | internal | 2026 |
| Spotify | [Honk / Xirp](data/agents/spotify-honk-xirp.yaml) | coding, migrations, code-review | drafts-reviewed | Honk runs in a constrained Kubernetes container (it does not inherit arbitrary engineer credentials); jobs execute inside Fleet Management / Fleetshift | slack, github, cli | commercialized | 2025 |
| Stripe | [Minions](data/agents/stripe-minions.yaml) | coding, code-review | drafts-reviewed | Not specified publicly | slack, github | internal | 2026 |
| Uber | [Internal coding agent (unnamed)](data/agents/uber-coding-agent.yaml) | coding | drafts-reviewed | Not specified publicly | — | internal | 2026 |
| WorkOS | [Project Horizon](data/agents/workos-project-horizon.yaml) | coding, code-review, security | drafts-reviewed | Cloudflare Containers + Sandbox SDK; disposable, tightly scoped sandboxes with explicit lifecycle APIs and egress controls; full monorepo stack in Docker dev containers | linear, github, slack, web | internal | 2026 |
| Y Combinator | [Internal agent infrastructure](data/agents/ycombinator-agent-infra.yaml) | coding, ops | human-in-loop | Not detailed publicly (primary source is a podcast) | — | internal | 2026 |
| Zup | [CodeGen](data/agents/zup-codegen.yaml) | coding | human-in-loop | — | — | internal | 2026 |

<!-- END LANDSCAPE -->

---

## Patterns at a glance

Distilled from the catalog. Each links to the full treatment in [Patterns](docs/patterns.md).

- **The model is a swappable layer:** build value in the harness, context, tools, permissions, evals, and sandbox.
- **Sandbox first:** isolated, pre-warmed, disposable (Firecracker, Modal, Containers, EKS pods).
- **Broker credentials:** the agent never holds a secret (Browserbase, Sentry, WorkOS, Cloudflare).
- **Skills/playbooks encode company knowledge:** DoorDash YAML, Shopify/Sentry markdown, monday.com guardrails.
- **Context is "the system around the code":** Backstage/Portal catalogs, AGENTS.md, file-based memory.
- **Default to Slack; default to public:** visibility drives adoption (Shopify River, Ramp, DoorDash).
- **Don't trust the model:** make misbehavior structurally impossible with scoped, per-session permissions.
- **Climb the autonomy spectrum gradually:** from assistive to autonomous (monday.com Morphex ships without review); evals from day one.

See also [Adoption lessons](docs/adoption-lessons.md) for how these systems get used in practice.

---

## Who is this for?

- **Platform/infra engineers** building or scaling an internal agent: start from a shared
  baseline instead of zero.
- **Engineering leaders** evaluating what an internal agent program looks like in practice.
- **Anyone curious** about how DoorDash, Spotify, Shopify, Cloudflare, Block, and others
  run AI inside their walls.

---

## Contributing

Adding an agent takes ~15 minutes: copy [`templates/agent.yaml`](templates/agent.yaml) →
fill it in → run `python scripts/build.py` → open a PR. See
[CONTRIBUTING.md](CONTRIBUTING.md) and the [schema reference](data/schema.md).

**The one rule: don't invent.** Every claim should trace to a source link. Thin but sourced
beats rich but guessed.

---

## License

- **Code** (`scripts/`, build tooling): [MIT](LICENSE).
- **Documentation and data** (README, `docs/`, `data/`, `templates/`):
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

By contributing you agree your contributions are licensed accordingly. See
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
