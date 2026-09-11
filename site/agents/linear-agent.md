Source: https://internal-agents.com/#linear-agent

Linear Task agent

# Linear Agent

A native agent that synthesizes workspace context, triages, creates follow-up work, runs coding sessions, and executes scheduled/event-driven 'Loops'; used by Linear's own CX, Product, and Engineering teams.

Support Customer success Coding

assigned coding work → agent-created change: Work product review

Operating model, claims & sources

#### Scoped operating models

**assigned coding work → agent-created change** Work product review · Level 3

#### Summary and context

Summary

A native agent that synthesizes workspace context, triages, creates follow-up work, runs coding sessions, and executes scheduled/event-driven 'Loops'; used by Linear's own CX, Product, and Engineering teams.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)
- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)
- Supports [Introducing Linear Agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-6/content.md) (first-party)

#### Architecture and primitives

Sandbox

unknown

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The preserved sources do not document an execution sandbox; unknown does not mean absent.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

Harness

Separate planning agent (triage/issue creation) and coding agent (code generation); Code Intelligence for codebase knowledge; scheduled/event-driven 'Loops'

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)
- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Model

Codex was used for internal pull-request review; other model choices are not detailed in the preserved sources

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Interfaces

slack, intercom, linear, github

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Tool access

Triage Intelligence (auto-route, dedup, label); GitHub; testing Code Intelligence + custom MCP servers

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Knowledge

Semantic/vector search evolved into agentic context acquisition across the workspace; Datadog/Sentry customer context

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Credentials

The Agent SDK gives agents explicit identities, scoped OAuth tokens, assignable/mentionable handles, and visible human delegation; issues stay assigned to a human; 'an agent cannot be held accountable'

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md) (first-party)

Supporting component

Auto-routes issues, flags duplicates, suggests labels

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Supporting component

Agents get identities, scoped team access, and visible delegation alongside humans

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md) (first-party)

Supporting component

Scheduled or event-driven agent runs that execute recurring work

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Keep the agent close to the source of work (Intercom, Slack, Linear); the best workflows live where work already happens

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Gradual autonomy; start by asking for suggestions, observe, add guidance, only automate once proven reliable

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Break work into small steps to keep coding agents focused and successful

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

One Linear engineer reports that agent mistakes reveal possible failure modes during review

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

Lesson

Close the loop; auto-notify the customer when their request ships

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for assigned coding work → agent-created change; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source documents delegated coding output while a human remains accountable for the assigned issue.

Observation date
:   2026-08-11

- Supports [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md) (first-party)

#### Sources

1. [How we built Linear Agent](https://linear.app/now/how-we-built-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-1/content.md)  <https://linear.app/now/how-we-built-linear-agent> engineering-blog · first-party · Last source verification: 2026-08-31
2. [How we use Linear Agent at Linear](https://linear.app/now/how-we-use-linear-agent-at-linear) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-2/content.md)  <https://linear.app/now/how-we-use-linear-agent-at-linear> engineering-blog · first-party · Last source verification: 2026-08-31
3. [Our approach to building the Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-3/content.md)  <https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk> engineering-blog · first-party · Last source verification: 2026-08-31
4. [Hacker News submission for how Linear built its agent](https://news.ycombinator.com/item?id=49252304) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-4/content.md)  <https://news.ycombinator.com/item?id=49252304> hn-thread · community · Last source verification: 2026-08-31
5. [Hacker News submission for the Linear Agent public beta](https://news.ycombinator.com/item?id=48503334) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-5/content.md)  <https://news.ycombinator.com/item?id=48503334> hn-thread · community · Last source verification: 2026-08-31
6. [Introducing Linear Agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/linear-agent-source-6/content.md)  <https://linear.app/changelog/2026-03-24-introducing-linear-agent> release · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#linear-agent)
