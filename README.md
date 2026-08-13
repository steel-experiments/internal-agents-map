# Internal Agents Map

Internal Agents Map is a source-backed catalog of how organizations build and use artificial
intelligence (AI) agents for internal work. It covers task agents, background agents, shared
platforms, orchestration systems, and implemented supporting patterns.

The catalog collects company articles, source code, documentation, talks, social posts, news,
and community commentary. A common rubric makes different approaches easier to compare. The
goal is to learn from their designs, tradeoffs, results, and failures.

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-green.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What the catalog includes

Organizations use the word "agent" in different ways. The catalog preserves those differences.
It does not require one architecture or level of autonomy.

An approach qualifies when a named organization built or materially adapted it for its own
teams, and a public source describes the implementation or its use. The approach can be an
agent, workflow, platform, runtime, orchestration system, or supporting pattern. Prototypes,
pilots, deployed systems, and later product releases all qualify.

Durable identity is one design choice. It is not an inclusion requirement. The comparison
rubric records identity, state, invocation, autonomy, deployment stage, controls, and available
evidence. Scoped operating-model assessments also show where human attention returns and derive
a Shapiro level for that workflow. An unknown value means the collected sources do not document it.

### Scope

The catalog includes approaches first built or materially adapted for internal work. An entry
can remain internal, become open source, or become a commercial product.

Generic vendor products do not qualify without a documented internal adaptation. General
opinion articles and unattributed rumors do not qualify as approaches. They can still appear as
commentary when they discuss a cataloged approach.

The catalog treats company metrics as self-reported unless an independent source verifies them.
It keeps source claims separate from catalog interpretation. See the [data schema](data/schema.md)
for source and confidence rules.

---

## The landscape

The table is sorted by company. Each row links to the relevant section of the
[full catalog](docs/landscape.md). The YAML records are in [data/agents](data/agents/).

<!-- BEGIN LANDSCAPE -->

| Company | Approach | Type | Domains | Operating model | Autonomy | Stage | Status | Year |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Airbnb | [Airchat (airchat-cli)](docs/landscape.md#airbnb-airchat) | platform | coding, code-review | L3 · coding task → reviewed pull request | drafts-reviewed | scaled | internal | 2025 |
| Atlassian | [DOT (Design Org Teammate)](docs/landscape.md#atlassian-dot) | task-agent | support | Unknown · tooling question → help-channel answer | assistive | deployed | internal | 2026 |
| Atlassian | [Rovo Dev (RovoDev)](docs/landscape.md#atlassian-rovo-dev) | task-agent | coding, code-review | L3 · Jira issue → reviewed pull request | human-in-loop | scaled | commercialized | 2024 |
| Block | [Builderbot](docs/landscape.md#block-builderbot) | orchestration-system | coding, code-review | L3 · ticket → reviewed pull request | drafts-reviewed | scaled | internal | 2026 |
| Brex | [Internal Agent Platform](docs/landscape.md#brex-agent-platform) | platform | finance-ops, support, customer-success | L2 · internal operations request → completed operation | human-in-loop | scaled | internal | 2025 |
| Browserbase | [bb](docs/landscape.md#browserbase-bb) | task-agent | coding, code-review, support, customer-success, research | L3 · coding request → reviewed pull request | drafts-reviewed | deployed | internal | 2026 |
| Cloudflare | [Internal AI engineering stack](docs/landscape.md#cloudflare-ai-stack) | platform | coding, code-review | L3 · pull request → AI review findings | drafts-reviewed | scaled | internal | 2026 |
| Coinbase | [Forge / Mux](docs/landscape.md#coinbase-forge-mux) | agent-system | coding, code-review | L3 · Slack, GitHub, or Linear request → reviewed pull request and build | drafts-reviewed | scaled | internal | 2026 |
| Domu | [Clementino](docs/landscape.md#domu-clementino) | task-agent | support, finance-ops, coding, recruitment, customer-success | L3 · employee request → approved customer-impacting action | human-in-loop | deployed | internal | 2026 |
| DoorDash | [AI Code Review Agent](docs/landscape.md#doordash-code-review) | background-agent | code-review | L3 · pull request → AI review comments | drafts-reviewed | scaled | internal | 2026 |
| DoorDash | [Flux / Agentic AI Platform](docs/landscape.md#doordash-flux) | platform | code-review, coding, ci-triage, on-call, maintenance, data | L3 · engineering task → reviewed agent output | drafts-reviewed | scaled | internal | 2025 |
| Dropbox | [Nova](docs/landscape.md#dropbox-nova) | platform | coding, ci-triage, on-call, maintenance | Unknown · agent-assisted SDLC workflow → accepted change | human-in-loop | scaled | internal | 2026 |
| Flex | [AI Investigation Agent](docs/landscape.md#flex-investigation-agent) | task-agent | finance-ops, on-call, coding | L3 · payment investigation → proposed code fix | drafts-reviewed | deployed | internal | 2026 |
| GitHub | [Qubot](docs/landscape.md#github-qubot) | task-agent | data | Unknown · data question → warehouse answer | assistive | scaled | internal | 2026 |
| Harvey | [Spectre](docs/landscape.md#harvey-spectre) | platform | coding, code-review, on-call, security | L3 · incident or request → reviewable diff or pull request | drafts-reviewed | deployed | internal | 2026 |
| Linear | [Linear Agent](docs/landscape.md#linear-agent) | task-agent | support, customer-success, coding | L3 · assigned coding work → agent-created change | drafts-reviewed | scaled | commercialized | 2026 |
| Microsoft | [PRAssistant](docs/landscape.md#microsoft-prassistant) | background-agent | code-review | L3 · pull request → AI review comments | drafts-reviewed | scaled | internal | 2025 |
| monday.com | [Sphera / Atlas / Morphex](docs/landscape.md#monday-sphera-atlas-morphex) | agent-system | coding, code-review | L4 · Atlas or Morphex feature task → tested and merged pull request | autonomous | scaled | internal | 2026 |
| Notion | [Custom Agents](docs/landscape.md#notion-custom-agents) | platform | support, finance-ops, recruitment, security | Unknown · cross-team internal tasks → Custom Agents output | unknown | scaled | internal | 2026 |
| PostHog | [StampHog](docs/landscape.md#posthog-stamphog) | background-agent | code-review | L5 · eligible pull request → approval decision | autonomous | scaled | open-sourced | 2026 |
| Ramp | [Inspect](docs/landscape.md#ramp-inspect) | background-agent | coding, code-review, on-call | L3 · Inspect coding task → reviewed production merge | drafts-reviewed | scaled | internal | 2026 |
| Replit | [Manager agent (agent-of-agents)](docs/landscape.md#replit-manager-agent) | orchestration-system | coding, code-review, support, research, data | L3 · objective → verifiable multi-agent work product | drafts-reviewed | scaled | internal | 2026 |
| Retool | [RetoolGPT](docs/landscape.md#retool-retoolgpt) | task-agent | support, coding | Unknown · internal question → sourced answer | assistive | deployed | internal | 2025 |
| Salesforce | [Slackbot](docs/landscape.md#salesforce-slackbot) | task-agent | support, customer-success, ops | L3 · employee request → drafted work | drafts-reviewed | scaled | commercialized | 2025 |
| Sentry | [Junior](docs/landscape.md#sentry-junior) | task-agent | coding, code-review, support, on-call | L2 · assigned task → human-steered and reviewed output | human-in-loop | deployed | open-sourced | 2026 |
| Shopify | [Aquifer / River](docs/landscape.md#shopify-internal-agents) | platform | coding, code-review, research, security | L3 · River coding request → reviewed pull request | drafts-reviewed | scaled | internal | 2026 |
| Sierra | [Pinecone](docs/landscape.md#sierra-pinecone) | task-agent | coding, code-review, support, research, data | L3 · employee request → reviewed agent output | drafts-reviewed | scaled | internal | 2026 |
| Slack | [Multi-agent context system](docs/landscape.md#slack-context-system) | supporting-pattern | research | Unknown · long-running investigation → synthesized report | human-in-loop | research | internal | 2026 |
| Spotify | [Honk / Xirp](docs/landscape.md#spotify-honk-xirp) | agent-system | coding, migrations, code-review | L3 · Honk coding task → verified pull request | drafts-reviewed | scaled | mixed | 2025 |
| Stripe | [Minions](docs/landscape.md#stripe-minions) | background-agent | coding, code-review | L3 · work context → merge-ready pull request | drafts-reviewed | scaled | internal | 2026 |
| Uber | [Internal coding agent (unnamed)](docs/landscape.md#uber-coding-agent) | task-agent | coding | Unknown · coding request → complete code change | drafts-reviewed | deployed | internal | 2026 |
| Uber | [uReview](docs/landscape.md#uber-ureview) | background-agent | code-review | L3 · pull request → filtered AI review findings | drafts-reviewed | scaled | internal | 2025 |
| WorkOS | [Project Horizon](docs/landscape.md#workos-project-horizon) | platform | coding, code-review, security | L4 · requirements and acceptance criteria → tested implementation | drafts-reviewed | deployed | internal | 2026 |
| Y Combinator | [Internal agent infrastructure](docs/landscape.md#ycombinator-agent-infra) | platform | coding, ops | Unknown · internal request → agent-assisted organizational work | human-in-loop | deployed | internal | 2026 |
| Zup | [CodeGen](docs/landscape.md#zup-codegen) | task-agent | coding | L2 · constrained coding task → human-supervised edit | human-in-loop | research | internal | 2026 |

<!-- END LANDSCAPE -->

---

## Analysis

[Architecture patterns](docs/patterns.md) compares the published technical designs.
[Adoption lessons](docs/adoption-lessons.md) collects reported operating practices. Both pages
state evidence limits and distinguish company reports from catalog interpretation.

---

## Who is this for?

- Engineers who build internal agent systems
- Leaders who compare implementation choices
- Researchers who track reported agent designs and results
- Contributors who find missing sources or conflicting evidence

---

## Contributing

Copy [templates/agent.yaml](templates/agent.yaml), add the evidence, and run
`python3 scripts/build.py`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full procedure.

Do not invent missing details. Link each claim to a source. Label commentary, inference, and
conflicting evidence instead of discarding them.

---

## License

- **Code and tooling** (`scripts/`, `tests/`, and workflow files): [MIT](LICENSE).
- **Documentation, policy, templates, and data**:
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

By contributing you agree your contributions are licensed accordingly. See
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
