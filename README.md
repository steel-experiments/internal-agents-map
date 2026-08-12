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
evidence. An unknown value means the collected sources do not document it.

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

| Company | Approach | Type | Domains | Autonomy | Stage | Status | Year |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Block | [Builderbot](docs/landscape.md#block-builderbot) | orchestration-system | coding, code-review | drafts-reviewed | scaled | internal | 2026 |
| Brex | [Internal Agent Platform](docs/landscape.md#brex-agent-platform) | platform | finance-ops, support, customer-success | human-in-loop | scaled | internal | 2025 |
| Browserbase | [bb](docs/landscape.md#browserbase-bb) | task-agent | coding, code-review, support, customer-success, research | drafts-reviewed | deployed | internal | 2026 |
| Cloudflare | [Internal AI engineering stack](docs/landscape.md#cloudflare-ai-stack) | platform | coding, code-review | drafts-reviewed | scaled | internal | 2026 |
| Coinbase | [Forge / Mux](docs/landscape.md#coinbase-forge-mux) | agent-system | coding, code-review | drafts-reviewed | scaled | internal | 2026 |
| Domu | [Clementino](docs/landscape.md#domu-clementino) | task-agent | support, finance-ops, coding, recruitment, customer-success | human-in-loop | deployed | internal | 2026 |
| DoorDash | [AI Code Review Agent](docs/landscape.md#doordash-code-review) | background-agent | code-review | drafts-reviewed | scaled | internal | 2026 |
| DoorDash | [Flux / Agentic AI Platform](docs/landscape.md#doordash-flux) | platform | code-review, coding, ci-triage, on-call, maintenance, data | drafts-reviewed | scaled | internal | 2025 |
| Dropbox | [Nova](docs/landscape.md#dropbox-nova) | platform | coding, ci-triage, on-call, maintenance | human-in-loop | scaled | internal | 2026 |
| Flex | [AI Investigation Agent](docs/landscape.md#flex-investigation-agent) | task-agent | finance-ops, on-call, coding | drafts-reviewed | deployed | internal | 2026 |
| Harvey | [Spectre](docs/landscape.md#harvey-spectre) | platform | coding, code-review, on-call, security | drafts-reviewed | deployed | internal | 2026 |
| Linear | [Linear Agent](docs/landscape.md#linear-agent) | task-agent | support, customer-success, coding | drafts-reviewed | scaled | commercialized | 2026 |
| monday.com | [Sphera / Atlas / Morphex](docs/landscape.md#monday-sphera-atlas-morphex) | agent-system | coding, code-review | autonomous | scaled | internal | 2026 |
| Ramp | [Inspect](docs/landscape.md#ramp-inspect) | background-agent | coding, code-review, on-call | drafts-reviewed | scaled | internal | 2026 |
| Replit | [Manager agent (agent-of-agents)](docs/landscape.md#replit-manager-agent) | orchestration-system | coding, code-review, support, research, data | drafts-reviewed | scaled | internal | 2026 |
| Salesforce | [Slackbot](docs/landscape.md#salesforce-slackbot) | task-agent | support, customer-success, ops | drafts-reviewed | scaled | commercialized | 2025 |
| Sentry | [Junior](docs/landscape.md#sentry-junior) | task-agent | coding, code-review, support, on-call | human-in-loop | deployed | open-sourced | 2026 |
| Shopify | [Aquifer / River](docs/landscape.md#shopify-internal-agents) | platform | coding, code-review, research, security | drafts-reviewed | scaled | internal | 2026 |
| Sierra | [Pinecone](docs/landscape.md#sierra-pinecone) | task-agent | coding, code-review, support, research, data | drafts-reviewed | scaled | internal | 2026 |
| Slack | [Multi-agent context system](docs/landscape.md#slack-context-system) | supporting-pattern | research | human-in-loop | research | internal | 2026 |
| Spotify | [Honk / Xirp](docs/landscape.md#spotify-honk-xirp) | agent-system | coding, migrations, code-review | drafts-reviewed | scaled | mixed | 2025 |
| Stripe | [Minions](docs/landscape.md#stripe-minions) | background-agent | coding, code-review | drafts-reviewed | scaled | internal | 2026 |
| Uber | [Internal coding agent (unnamed)](docs/landscape.md#uber-coding-agent) | task-agent | coding | drafts-reviewed | deployed | internal | 2026 |
| WorkOS | [Project Horizon](docs/landscape.md#workos-project-horizon) | platform | coding, code-review, security | drafts-reviewed | deployed | internal | 2026 |
| Y Combinator | [Internal agent infrastructure](docs/landscape.md#ycombinator-agent-infra) | platform | coding, ops | human-in-loop | deployed | internal | 2026 |
| Zup | [CodeGen](docs/landscape.md#zup-codegen) | task-agent | coding | human-in-loop | research | internal | 2026 |

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
