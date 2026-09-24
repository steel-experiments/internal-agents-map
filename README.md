# Internal Agents Map

**[Explore the map](https://internal-agents.com/)**

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
[Website and delivery](docs/site.md) ·
[Architecture patterns](docs/patterns.md) ·
[Adoption observations](docs/adoption-lessons.md) ·
[Use the data](data/agents.json) ·
[Contribute](CONTRIBUTING.md)

<!-- BEGIN OVERVIEW -->

**Current map: 51 agents across 41 organizations, plus 15 infrastructure records. The complete catalog is backed by 120 distinct sources and 1172 evidence-linked claims.**

## Agents

| Organization | Approach | Type | Work |
| --- | --- | --- | --- |
| Airbnb | [Datako](docs/landscape.md#airbnb-datako) | agent | data |
| Airbnb | [Pascal](docs/landscape.md#airbnb-pascal) | agent | research |
| Amplitude | [Design Agent](docs/landscape.md#amplitude-design-agent) | agent | design |
| Atlassian | [Rovo Dev (RovoDev)](docs/landscape.md#atlassian-rovo-dev) | agent | coding, code-review |
| Bitrise | [Kolega](docs/landscape.md#bitrise-kolega) | agent | coding, code-review, ci-triage, maintenance |
| Block | [Builderbot](docs/landscape.md#block-builderbot) | agent | coding, code-review |
| Brex | [Collections response agent](docs/landscape.md#brex-collections) | agent | finance-ops |
| Brex | [Dispute preparation agent](docs/landscape.md#brex-disputes) | agent | finance-ops |
| Brex | [Onboarding decision system](docs/landscape.md#brex-onboarding) | agent | finance-ops |
| Brex | [Support quality agent](docs/landscape.md#brex-support-qa) | agent | support |
| Cloudflare | [AI Code Reviewer](docs/landscape.md#cloudflare-code-reviewer) | agent | code-review |
| Coinbase | [Forge](docs/landscape.md#coinbase-forge-mux) | agent | coding, code-review |
| Cursor | [Support investigation workflow in Cursor](docs/landscape.md#cursor-support-workflow) | agent | support |
| Deel | [Four-stage payroll sync triage pipeline](docs/landscape.md#deel-payroll-incident-agents) | agent | finance-ops, ops |
| Domu | [Clementino](docs/landscape.md#domu-clementino) | agent | support, finance-ops, coding, recruitment, customer-success |
| DoorDash | [AI Code Review Agent](docs/landscape.md#doordash-code-review) | agent | code-review |
| DoorDash | [DataExplorer](docs/landscape.md#doordash-dataexplorer) | agent | data |
| Dropbox | [Deflaker](docs/landscape.md#dropbox-deflaker) | agent | coding |
| Figma | [Security alert triage and investigation agents](docs/landscape.md#figma-security-agent) | agent-system | security, on-call, coding |
| Flex | [AI Investigation Agent](docs/landscape.md#flex-investigation-agent) | agent | finance-ops, on-call, coding |
| GitHub | [Qubot](docs/landscape.md#github-qubot) | agent | data |
| Harvey | [Security operations agents](docs/landscape.md#harvey-security-operations) | agent-system | security |
| HubSpot | [Sidekick](docs/landscape.md#hubspot-sidekick) | agent | code-review |
| Linear | [Linear Agent](docs/landscape.md#linear-agent) | agent | support, customer-success, coding |
| Meta | [Ranking Engineer Agent (REA)](docs/landscape.md#meta-rea) | agent | data, research |
| Microsoft | [AI-powered code review assistant](docs/landscape.md#microsoft-prassistant) | agent | code-review |
| monday.com | [Sphera / Atlas / Morphex](docs/landscape.md#monday-sphera-atlas-morphex) | agent-system | coding, code-review |
| Notion | [Internal bug-triage agent](docs/landscape.md#notion-bug-triage) | agent | maintenance |
| Notion | [Scruff](docs/landscape.md#notion-scruff) | agent | security |
| OpenAI | [Agentic software factory](docs/landscape.md#openai-software-factory) | agent-system | coding, code-review, ci-triage, ops |
| OpenAI | [Sevbot](docs/landscape.md#openai-sevbot) | agent | on-call |
| Plaid | [AI Annotator](docs/landscape.md#plaid-ai-annotator) | agent | data |
| Plaid | [Fix My Connection](docs/landscape.md#plaid-fix-my-connection) | agent | ops, maintenance |
| PostHog | [StampHog](docs/landscape.md#posthog-stamphog) | agent | code-review |
| Ramp | [Inspect](docs/landscape.md#ramp-inspect) | agent | coding, code-review, on-call |
| Replit | [Manager agent (agent-of-agents)](docs/landscape.md#replit-manager-agent) | agent | coding, code-review, support, research, data |
| Salesforce | [Slackbot](docs/landscape.md#salesforce-slackbot) | agent | support, customer-success, ops |
| Sentry | [Junior](docs/landscape.md#sentry-junior) | agent | coding, code-review, support, on-call |
| Shopify | [River](docs/landscape.md#shopify-river) | agent | coding |
| Sierra | [Pinecone](docs/landscape.md#sierra-pinecone) | agent | coding, code-review, support, research, data |
| Slack | [Security investigation service](docs/landscape.md#slack-context-system) | agent | security |
| Snap | [Casper](docs/landscape.md#snap-casper) | agent-system | coding, maintenance, on-call, data |
| Snap | [CodePal](docs/landscape.md#snap-codepal) | agent | code-review |
| Spotify | [Honk](docs/landscape.md#spotify-honk-xirp) | agent | coding, migrations, code-review |
| Stripe | [Minions](docs/landscape.md#stripe-minions) | agent | coding, code-review |
| StrongDM | [Software Factory](docs/landscape.md#strongdm-software-factory) | agent | coding |
| Uber | [Internal coding agent (unnamed)](docs/landscape.md#uber-coding-agent) | agent | coding |
| Uber | [uReview](docs/landscape.md#uber-ureview) | agent | code-review |
| WorkOS | [Project Horizon](docs/landscape.md#workos-project-horizon) | agent | coding, code-review, security |
| Y Combinator | [Internal operations agent](docs/landscape.md#ycombinator-operations) | agent | ops, finance-ops |
| Zup | [CodeGen](docs/landscape.md#zup-codegen) | agent | coding |

## Infrastructure

| Organization | Approach | Type | Work |
| --- | --- | --- | --- |
| Airbnb | [Airchat (airchat-cli)](docs/landscape.md#airbnb-airchat) | platform | coding, code-review |
| Brex | [Internal Agent Platform](docs/landscape.md#brex-agent-platform) | platform | finance-ops, support, customer-success |
| Cloudflare | [Internal AI engineering stack](docs/landscape.md#cloudflare-ai-stack) | platform | coding, code-review |
| Coinbase | [Mux](docs/landscape.md#coinbase-mux) | platform | coding |
| Databricks | [coSTAR](docs/landscape.md#databricks-costar) | supporting-pattern | coding, code-review, on-call |
| DoorDash | [Analytics AI Marketplace](docs/landscape.md#doordash-ai-marketplace) | platform | data |
| DoorDash | [Flux](docs/landscape.md#doordash-flux) | platform | code-review, coding, ci-triage, on-call, maintenance |
| Dropbox | [Nova](docs/landscape.md#dropbox-nova) | platform | coding, ci-triage, on-call, maintenance |
| Duolingo | [Agentic workflows](docs/landscape.md#duolingo-agentic-workflows) | platform | coding |
| Harvey | [Spectre](docs/landscape.md#harvey-spectre) | platform | coding, code-review, on-call, security |
| Notion | [Custom Agents](docs/landscape.md#notion-custom-agents) | platform | support, finance-ops, recruitment, security |
| Plaid | [Internal MCP server](docs/landscape.md#plaid-internal-mcp-server) | supporting-pattern | coding |
| Shopify | [Aquifer](docs/landscape.md#shopify-internal-agents) | platform | coding, code-review |
| Shopify | [Roast](docs/landscape.md#shopify-roast) | platform | coding, code-review, on-call, research |
| Y Combinator | [Internal agent infrastructure](docs/landscape.md#ycombinator-agent-infra) | platform | coding, ops |

<!-- END OVERVIEW -->

**Reading the levels:** Adapted from [Dan Shapiro's
framework](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/),
**L2** means continuous steering, **L3** work-product review, **L4** outcome review, and **L5**
exception-only supervision. Levels describe a specific workflow, not company maturity. [Methodology
→](data/schema.md#operating-models-and-derived-levels)

<!-- BEGIN README FINDINGS -->

## What the current map shows

These counts classify 66 catalog entries. A platform and one of its components can both appear, so the entries are not independent deployments, shares of industry practice, or counts of successful runs.

Agent autonomy (51 records; infrastructure excluded) is classified as 28 drafts-reviewed, 5 human-in-loop, 6 autonomous, 1 assistive, and 11 unknown. Human-in-loop includes approval checkpoints; it does not mean a person continuously steers the whole run.

The catalog contains 64 scoped supervision assessments across those entries, including 3 continuous-steering, 32 work-product-review, 1 outcome-review, 7 exception-only, and 21 unknown assessments. 9 entries have more than one assessed workflow; the counts therefore do not assign one level to each company.

15 entries are platforms or supporting patterns. State duration is undocumented for 39 entries. Review cost, failure rates, and retired systems remain rarely reported.

<!-- END README FINDINGS -->

## What belongs in the map

An entry needs a named organization, an agent or enabling approach built or materially adapted
for that organization's own work, and public evidence describing its implementation or use.

Agents, platforms, and implemented supporting systems have separate approach types. Research
implementations, prototypes, and commercial or open-source systems can qualify. A product name
is optional. Generic adoption claims are insufficient.

See the [inclusion rules](CONTRIBUTING.md#inclusion-rules) for the shared policy.

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

## Agents and infrastructure

The map maintains two collections. Agents perform identifiable work for internal
teams; Infrastructure supplies reusable execution, orchestration, or tool access.
Both retain structured, source-backed records. Lessons compare practices across cases.
Choose the subject before assigning workflow claims or metrics: a task-performing
system remains an agent even when it orchestrates subagents. A family requires
independently useful constituent agents. Sandbox detail alone does not establish a
platform. Attribute downstream agent results to their actual subject and author
`built-on` only when a source establishes the dependency.

The homepage counts agents; the Infrastructure index keeps supporting implementations
discoverable. Full JSON exports include both collections, identified by derived
`catalog_section`. Existing detail URLs and anchors remain stable. See the
[schema migration](data/schema.md#collection-migration-catalog-7-compact-index-3).
