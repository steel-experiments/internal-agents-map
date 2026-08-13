# Adoption observations

This page summarizes reported operating practices in the catalog. Most sources are company reports. They do not establish cause and effect.

The observations use the 28 approaches reviewed on August 13, 2026. The evidence is uneven. Read each source before you apply a practice to another organization.

## Start with work that people can check

DoorDash reports early use in code review and structured data work. Spotify reports migration work. Flex reports payment investigation. These tasks produce an artifact or result that a person can inspect.

This suggests a practical starting question: can the team decide whether the work is correct? A narrow task with a clear check can make early evaluation easier. The catalog does not prove that every team must start narrow.

## Put the system near existing work

Twenty entries list Slack as an interface. Other entries use GitHub, Linear, web interfaces, command-line tools, scheduled jobs, or event handlers.

An existing interface can reduce the effort needed to try a system. It can also inherit the access, privacy, and retention problems of that interface. Public channels can spread examples, but teams must not expose private work to gain visibility.

## Fund enablement work

Several organizations report work beyond the agent runtime. DoorDash describes workshops and playbooks. Brex describes tools that operations staff use to test prompts and models. monday.com describes managers, scopes, and performance measures for agents.

These reports show that deployment includes training, support, evaluation, and ownership. The public sources do not isolate how much each activity affected adoption.

## Use existing systems of record

Several approaches read from or write to GitHub, Linear, Jira, Salesforce, and internal service catalogs. This can preserve familiar review and audit paths.

The catalog also contains limits. Existing permissions can be too broad for an automated process. Teams still need task scope, approval rules, and an audit record for tool calls.

## Centralize shared controls when the system grows

Cloudflare reports a central gateway and MCP portal. Browserbase, Sentry, WorkOS, and Sierra report proxies or gateways for authorization, logging, or credential injection.

Shared controls can reduce repeated integration work. They can also become a shared failure point. Compare this choice with the deployment stage and number of connected systems.

## Measure accepted outcomes

The catalog contains activity metrics, adoption metrics, and outcome metrics. They answer different questions.

- Sessions and tool calls show use.
- Created pull requests show output.
- Accepted changes and action rates show that a person used the output.
- Cycle time and incident results can show an operational effect.
- Review time and escaped defects can show hidden cost.

Sierra distinguishes use from value in its report. DoorDash reports action rates for review findings. Replit reports output with review, revert, and incident measures. These examples support a broader metric set. They do not make the reported measurements independent.

## Expect work to move

Spotify reports that increased coding output added review pressure. Harvey reports more emphasis on review, prioritization, and coordination as implementation becomes faster.

When one step speeds up, inspect the next step. Track waiting time, review effort, rework, and operational failures. A higher output count alone does not show a better process.

## Expand autonomy with evidence

The sample contains 19 `drafts-reviewed` approaches, seven `human-in-loop` approaches, and two `autonomous` approaches. This distribution reflects public reports in the catalog. It is not a recommendation.

Before a team removes a review step, it should define the failure limit, verification method, rollback path, and responsible owner. The relevant threshold depends on the task. A code migration and a customer payment action do not have the same impact.

## Keep dissent and failed results

Company launch articles tend to report successful outcomes. Community discussion, source code issues, later retrospectives, and independent reporting can supply missing context.

Add those sources to the catalog. Link them as supporting, contradicting, or contextual evidence. Do not remove an older claim when a later source disagrees. Record the date and let readers see the change.
