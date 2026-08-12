# Agent data schema

Every agent is **one YAML file** in `data/agents/`, named `<id>.yaml` (e.g.
`doordash-flux.yaml`). The build script (`scripts/build.py`) reads these files and
regenerates `README.md` (landscape table), `docs/landscape.md` (full catalog), and
`data/agents.json`.

Copy [`templates/agent.yaml`](../templates/agent.yaml) to get started, then fill it in.
Fields marked **★ required** must be present and non-empty; everything else is optional
(omit it rather than leaving it blank — the build hides empty fields automatically).

## Top-level fields

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | ★ | string | kebab-case, **must match the filename** (`doordash-flux`). |
| `company` | ★ | string | Company that built it (`DoorDash`). |
| `agent_name` | ★ | string | Product/system name (`Flux`). |
| `year` | ★ | integer | Year of the first public writeup/evidence. |
| `status` | ★ | enum | `internal` \| `open-sourced` \| `commercialized` (offered externally, e.g. Xirp beta). |
| `domains` | ★ | list | What it does. Free-form tags but prefer existing ones: `coding`, `code-review`, `ci-triage`, `on-call`, `maintenance`, `migrations`, `research`, `support`, `ops`, `security`, `data`, `general`. |
| `autonomy` | ★ | enum | `assistive` \| `human-in-loop` \| `drafts-reviewed` \| `autonomous` (see below). |
| `summary` | ★ | string | One sentence. What it is. |
| `headline_metric` |  | string | The single most impressive number, with unit. |

### `autonomy` values

- **`assistive`** — a human drives; the agent helps (pair-programming, suggestions).
- **`human-in-loop`** — the agent acts but a human is involved in each cycle or approves each action.
- **`drafts-reviewed`** — the agent autonomously drafts work product (PRs, fixes, decisions) that a human reviews before it ships. *The most common level for coding agents.*
- **`autonomous`** — ships / takes effect without human review (e.g. monday.com Morphex).

## `architecture` (optional, map)

Concrete building blocks. Each value is a short phrase.

| Key | What to put |
| --- | --- |
| `sandbox` | Execution environment + isolation (e.g. "Firecracker microVMs; <5s p95 cold start"). |
| `harness` | The agent loop / runtime (e.g. "OpenCode, server-first"). |
| `model` | Which model(s); note if interchangeable. |
| `tool_access` | How it reaches internal systems (MCP gateway, integration proxy, MCP servers). |
| `interfaces` | list — where humans invoke it (`slack`, `github`, `cli`, `web`, `cron`, `chrome`, `api`). |
| `knowledge` | Context/org layer (Backstage, Portal, AGENTS.md, monorepo "world"). |
| `credentials` | How secrets & permissions are handled (brokering, per-session scoping, RBAC/ABAC). |
| `context_mgmt` | How it handles long-running context (summaries, journals, compaction). Omit if n/a. |

## `primitives` (optional, list of `{name, desc}`)

The reusable building blocks the platform exposes — name each one and one-line it.
(e.g. DoorDash: Sandbox, MCP Gateway, Playbook, Invocation Surface.)

## `key_metrics` (optional, list of strings)

Real numbers with units and a timeframe, pulled from a source. If you only have one,
that's fine — also put it in `headline_metric`.

## `lessons_learned` (optional, list of strings)

The transferable insight, not the marketing. "Start narrow to earn trust." Each should
be something another team could act on.

## `sources` (required in spirit, ★ recommended, list of `{title, url, type}`)

Every claim should trace to a source. `type` is one of: `blog`, `talk`, `post` (X/social),
`case-study`, `podcast`, `docs`. Prefer the company's own engineering blog.

---

## Conventions

- **Don't invent.** If a field isn't documented in a source, omit it (or add a `_note`
  under the field). The build hides empty fields, so a thin entry is fine.
- **Quote metrics verbatim** where possible, with the source linked.
- **One agent per file.** If a company has several distinct systems (e.g. monday.com's
  Atlas vs Morphex), you may either combine them in one file or split — combine when
  they share one substrate, split when they're genuinely separate products.
- After editing, run `python scripts/build.py` and commit the regenerated
  `README.md`, `docs/landscape.md`, and `data/agents.json` together with your YAML.
