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

**Current map: 39 approaches across 35 organizations, backed by 88 sources and 558 evidence-linked claims.**

## Overview

| Organization | Approach | Type | Work |
| --- | --- | --- | --- |
| Airbnb | [Airchat (airchat-cli)](docs/landscape.md#airbnb-airchat) | platform | coding, code-review |
| Atlassian | [Rovo Dev (RovoDev)](docs/landscape.md#atlassian-rovo-dev) | task-agent | coding, code-review |
| Block | [Builderbot](docs/landscape.md#block-builderbot) | orchestration-system | coding, code-review |
| Brex | [Internal Agent Platform](docs/landscape.md#brex-agent-platform) | platform | finance-ops, support, customer-success |
| Browserbase | [bb](docs/landscape.md#browserbase-bb) | task-agent | coding, code-review, support, customer-success, research |
| Cloudflare | [Internal AI engineering stack](docs/landscape.md#cloudflare-ai-stack) | platform | coding, code-review |
| Coinbase | [Forge / Mux](docs/landscape.md#coinbase-forge-mux) | agent-system | coding, code-review |
| Databricks | [coSTAR and internal engineering agents](docs/landscape.md#databricks-costar) | agent-system | coding, code-review, on-call |
| Domu | [Clementino](docs/landscape.md#domu-clementino) | task-agent | support, finance-ops, coding, recruitment, customer-success |
| DoorDash | [AI Code Review Agent](docs/landscape.md#doordash-code-review) | background-agent | code-review |
| DoorDash | [Flux / Agentic AI Platform](docs/landscape.md#doordash-flux) | platform | code-review, coding, ci-triage, on-call, maintenance, data |
| Dropbox | [Nova](docs/landscape.md#dropbox-nova) | platform | coding, ci-triage, on-call, maintenance |
| Flex | [AI Investigation Agent](docs/landscape.md#flex-investigation-agent) | task-agent | finance-ops, on-call, coding |
| GitHub | [Qubot](docs/landscape.md#github-qubot) | task-agent | data |
| Harvey | [Spectre](docs/landscape.md#harvey-spectre) | platform | coding, code-review, on-call, security |
| HubSpot | [Sidekick](docs/landscape.md#hubspot-sidekick) | task-agent | code-review |
| Linear | [Linear Agent](docs/landscape.md#linear-agent) | task-agent | support, customer-success, coding |
| Microsoft | [PRAssistant](docs/landscape.md#microsoft-prassistant) | background-agent | code-review |
| monday.com | [Sphera / Atlas / Morphex](docs/landscape.md#monday-sphera-atlas-morphex) | agent-system | coding, code-review |
| Notion | [Custom Agents](docs/landscape.md#notion-custom-agents) | platform | support, finance-ops, recruitment, security |
| Plaid | [AI Annotator](docs/landscape.md#plaid-ai-annotator) | task-agent | data |
| Plaid | [Fix My Connection](docs/landscape.md#plaid-fix-my-connection) | task-agent | ops, maintenance |
| Plaid | [Internal MCP server](docs/landscape.md#plaid-internal-mcp-server) | supporting-pattern | coding |
| PostHog | [StampHog](docs/landscape.md#posthog-stamphog) | background-agent | code-review |
| Ramp | [Inspect](docs/landscape.md#ramp-inspect) | background-agent | coding, code-review, on-call |
| Replit | [Manager agent (agent-of-agents)](docs/landscape.md#replit-manager-agent) | orchestration-system | coding, code-review, support, research, data |
| Retool | [RetoolGPT](docs/landscape.md#retool-retoolgpt) | task-agent | support, coding |
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

**Reading the levels:** Adapted from [Dan Shapiro's
framework](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/),
**L2** means continuous steering, **L3** work-product review, **L4** outcome review, and **L5**
exception-only supervision. Levels describe a specific workflow, not company maturity. [Methodology
→](data/schema.md#operating-models-and-derived-levels)

## What the current map shows

Human review is still the norm. 23 of the 39 approaches produce a draft or implementation for
review. 8 keep a person involved throughout the work. 3 report autonomous action within a
scoped workflow; 2 are assistive and 3 remain unknown.

Different systems keep solving similar infrastructure problems: company context, scoped tools,
execution environments, verification, and integration with systems of record.

Some internal agents are durable: their identity or state persists across runs and restarts.
Others start fresh. Durability is a design choice, not an inclusion requirement.
State duration is undocumented for 34 approaches. Review cost, failure rates, and retired
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

Accepted sources are [preserved while they are live](docs/source-preservation.md). The publisher
URL remains the citation; verified snapshots provide an audit trail if it is later removed.

`unknown` means undocumented, not absent. Conflicting evidence remains visible. See the
[data schema](data/schema.md) for the complete methodology.

## Contributing

Found a missing approach or better evidence for one already here? Start with the
[record template](templates/agent.yaml) and follow the [contribution guide](CONTRIBUTING.md).

## License

Code and tooling are licensed under [MIT](LICENSE). Content and data are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Preserved third-party source
material under [`archive/`](archive/README.md) retains its original ownership and is not
relicensed under those terms.
