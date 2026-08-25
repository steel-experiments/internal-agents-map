# Internal Agents Map

## Definition

**Internal agents are AI systems organizations build or adapt to do work for their own teams.**

They operate through the organization's knowledge, tools, workflows, and controls. Some work
alongside a person. Others start from an event and run in the background. Human supervision
varies by workflow.

Organizations publish these systems under many names. Internal Agents Map groups their
implementations under one definition so their designs and operating boundaries can be compared.

The map also covers platforms, orchestration systems, and implemented supporting patterns.
These support internal agents but are not agents themselves.

Claims link to public sources. Company reports stay separate from catalog interpretation, and
undocumented details stay unknown.

[Browse the catalog](docs/landscape.md) ·
[Architecture patterns](docs/patterns.md) ·
[Adoption observations](docs/adoption-lessons.md) ·
[Use the data](data/agents.json) ·
[Contribute](CONTRIBUTING.md)

<!-- BEGIN OVERVIEW -->

**Current map: 28 approaches across 26 organizations, backed by 66 sources and 475 evidence-linked claims.**

## Overview

| Organization | Approach | Type | Work |
| --- | --- | --- | --- |
| Block | [Builderbot](docs/landscape.md#block-builderbot) | orchestration-system | coding, code-review |
| Brex | [Internal Agent Platform](docs/landscape.md#brex-agent-platform) | platform | finance-ops, support, customer-success |
| Browserbase | [bb](docs/landscape.md#browserbase-bb) | task-agent | coding, code-review, support, customer-success, research |
| Cloudflare | [Internal AI engineering stack](docs/landscape.md#cloudflare-ai-stack) | platform | coding, code-review |
| Coinbase | [Forge / Mux](docs/landscape.md#coinbase-forge-mux) | agent-system | coding, code-review |
| Domu | [Clementino](docs/landscape.md#domu-clementino) | task-agent | support, finance-ops, coding, recruitment, customer-success |
| DoorDash | [AI Code Review Agent](docs/landscape.md#doordash-code-review) | background-agent | code-review |
| DoorDash | [Flux / Agentic AI Platform](docs/landscape.md#doordash-flux) | platform | code-review, coding, ci-triage, on-call, maintenance, data |
| Dropbox | [Nova](docs/landscape.md#dropbox-nova) | platform | coding, ci-triage, on-call, maintenance |
| Flex | [AI Investigation Agent](docs/landscape.md#flex-investigation-agent) | task-agent | finance-ops, on-call, coding |
| Harvey | [Spectre](docs/landscape.md#harvey-spectre) | platform | coding, code-review, on-call, security |
| Linear | [Linear Agent](docs/landscape.md#linear-agent) | task-agent | support, customer-success, coding |
| monday.com | [Sphera / Atlas / Morphex](docs/landscape.md#monday-sphera-atlas-morphex) | agent-system | coding, code-review |
| PostHog | [StampHog](docs/landscape.md#posthog-stamphog) | background-agent | code-review |
| Ramp | [Inspect](docs/landscape.md#ramp-inspect) | background-agent | coding, code-review, on-call |
| Replit | [Manager agent (agent-of-agents)](docs/landscape.md#replit-manager-agent) | orchestration-system | coding, code-review, support, research, data |
| Salesforce | [Slackbot](docs/landscape.md#salesforce-slackbot) | task-agent | support, customer-success, ops |
| Sentry | [Junior](docs/landscape.md#sentry-junior) | task-agent | coding, code-review, support, on-call |
| Shopify | [Aquifer / River](docs/landscape.md#shopify-internal-agents) | platform | coding, code-review, research, security |
| Sierra | [Pinecone](docs/landscape.md#sierra-pinecone) | task-agent | coding, code-review, support, research, data |
| Slack | [Multi-agent context system](docs/landscape.md#slack-context-system) | supporting-pattern | research |
| Spotify | [Honk / Xirp](docs/landscape.md#spotify-honk-xirp) | agent-system | coding, migrations, code-review |
| Stripe | [Minions](docs/landscape.md#stripe-minions) | background-agent | coding, code-review |
| Uber | [Internal coding agent (unnamed)](docs/landscape.md#uber-coding-agent) | task-agent | coding |
| Uber | [uReview](docs/landscape.md#uber-ureview) | background-agent | code-review |
| WorkOS | [Project Horizon](docs/landscape.md#workos-project-horizon) | platform | coding, code-review, security |
| Y Combinator | [Internal agent infrastructure](docs/landscape.md#ycombinator-agent-infra) | platform | coding, ops |
| Zup | [CodeGen](docs/landscape.md#zup-codegen) | task-agent | coding |

<!-- END OVERVIEW -->

## What the current map shows

Human review is still the norm. 19 of the 28 approaches produce a draft or implementation for
review. 7 keep a person involved throughout the work. 2 report autonomous action within a
scoped workflow.

Different systems keep solving similar infrastructure problems: company context, scoped tools,
execution environments, verification, and integration with systems of record.

Some internal agents are durable: their identity or state persists across runs and restarts.
Others start fresh. Durability is a design choice, not an inclusion requirement.
State duration is undocumented for 23 approaches. Review cost, failure rates, and retired
systems are rarely reported.

## What belongs in the map

An entry needs a named organization, an agent or enabling approach built or materially adapted
for that organization's own work, and public evidence describing its implementation or use.

The map includes agents, agent systems, platforms, orchestration systems, and implemented
supporting patterns. These are separate approach types. Prototypes and systems that later became
open source or commercial products can qualify.

Generic vendor products without a documented internal adaptation are not entries. General
opinion pieces and unattributed claims may appear as context, not as catalog approaches.

## Evidence standard

Every authored claim points to one or more structured sources. Each source records its
relationship to the organization. Reported statements stay separate from catalog judgments, and
company metrics remain self-reported unless independently verified.

`unknown` means undocumented, not absent. Conflicting evidence remains visible. See the
[data schema](data/schema.md) for the complete methodology.

## Contributing

Found a missing approach or better evidence for one already here? Start with the
[record template](templates/agent.yaml) and follow the [contribution guide](CONTRIBUTING.md).

## License

Code and tooling are licensed under [MIT](LICENSE). Content and data are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
