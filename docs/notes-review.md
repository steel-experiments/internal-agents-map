# Notes coverage review

Reviewed on 2026-09-11 against all 39 approaches in `data/agents.json` and the three
current note templates. This is an editorial review, not a new site page.

## Selected for the site

The user selected N2, N3, N4, and N6. These are now authored as notes 04–07.
N1 (access checks) and N5 (interface choice) remain proposals. The review below
records the original assessment; the site now has seven notes.

## Decision

Six additional topics have a distinct builder question and a useful evidence base.
Publish them in small batches. The existing notes cover five approaches across five
organizations, with a strong code-review focus. There is no need for a note per case.

The first batch should cover access checks, surviving process loss, and selective
context loading. The next batch can cover fixed workflow steps, interface choice,
and evaluation with actual work.

## Proposed notes

### N1 — Who checks what the agent may do?

- **Question:** Where does an action receive permission?
- **Basis:** Browserbase checks session scope in its proxy. Sentry injects credentials
  outside its sandbox. Sierra distinguishes interactive user access from service accounts.
- **Observation:** Access checks can exist outside model instructions.
- **Diagram:** Agent request → access check → allowed tool, with a denied branch.
- **Limit:** Hidden long-lived credentials do not remove authority. Browserbase still
  passes session tokens; Sierra documents scoped read-only tokens for some CLI access.
  Do not claim that every credential stays outside every worker.
- **Source anchors:** [Browserbase, proxy flow](../archive/sources/browserbase-bb-source-1/content.md),
  [Sentry, credential handling](../archive/sources/sentry-junior-source-1/content.md),
  [Sierra, identity choices](../archive/sources/sierra-pinecone-source-2/content.md).

### N2 — The worker can stop. The work can continue.

- **Question:** What must survive a process restart?
- **Basis:** Shopify separates sessions from disposable execution. Sentry queues a
  continuation before its timeout. Sierra restores runner state from checkpoints and events.
- **Observation:** Conversation state, task state, and execution state have different lifetimes.
- **Diagram:** A persistent work record above worker A → stop → worker B.
- **Limit:** Saving a conversation does not guarantee that files or side effects recover.
  Browserbase explicitly says that some environment state may be lost. This note concerns
  recovery, not cross-session learning or a universal memory architecture.
- **Source anchors:** [Shopify, session survival](../archive/sources/shopify-internal-agents-source-1/content.md),
  [Sentry, continuation](../archive/sources/sentry-junior-source-1/content.md),
  [Sierra, checkpoints](../archive/sources/sierra-pinecone-source-3/content.md).
- **Distinct from the current stop note:** That note explains when to end attempts;
  this one explains how work survives the loss of its worker.

### N3 — Load tools when the task needs them

- **Question:** Must every request include every tool and instruction?
- **Basis:** Cloudflare replaces many exposed tool schemas with search and execution.
  Sentry connects providers after tool lookup. Browserbase loads task-specific skills.
- **Observation:** The always-present context can stay small as capabilities grow.
- **Diagram:** Small starting context → tool search → selected tool and instructions.
- **Limit:** Discovery adds a step and may fail to find a relevant tool. Loading fewer
  schemas does not by itself establish higher task accuracy. Tools and skills are distinct.
- **Source anchors:** [Cloudflare, Code Mode](../archive/sources/cloudflare-ai-stack-source-1/content.md),
  [Sentry, progressive discovery](../archive/sources/sentry-junior-source-1/content.md),
  [Browserbase, skills](../archive/sources/browserbase-bb-source-1/content.md).

### N4 — Some steps do not need a model

- **Question:** Which workflow decisions should ordinary code control?
- **Basis:** Stripe interleaves model work and fixed blueprint steps. Dropbox controls
  CI and publication outside its agent. PostHog makes eligibility gates authoritative.
- **Observation:** A model can choose a fix while code controls checks and permissions.
- **Diagram:** Fixed setup → model task → fixed check → permitted next step.
- **Limit:** A deterministic check covers a specific property. It does not prove overall
  correctness. Keep PostHog's approval workflow separate from code generation.
- **Source anchors:** [Stripe, blueprints](../archive/sources/stripe-minions-source-2/content.md),
  [Dropbox, workflow control](../archive/sources/dropbox-nova-source-1/content.md),
  [PostHog, pinned gate implementation](../archive/sources/posthog-stamphog-source-3/content.md).

### N5 — The task may need a different interface

- **Question:** Does the interface fit the work people want to do?
- **Basis:** Domu found Slack useful for shared messages and approvals but awkward for
  files and extended individual work. It separated a reusable toolkit from its interfaces.
- **Observation:** The same capabilities can serve different work through different interfaces.
- **Diagram:** Shared toolkit → Slack for shared work / desktop for work with files.
- **Limit:** This is a selected case, not evidence that every agent needs two interfaces.
  It does not establish that the model had no limitations.
- **Source anchor:** [Domu, the toolkit split](../archive/sources/domu-clementino-source-1/content.md).
- **Distinct from the current agent-role note:** This concerns user interaction, not
  the division of reasoning between agents. It adds a useful non-code-review example.

### N6 — Test the agent on your own work

- **Question:** What test cases tell us whether this agent fits this team?
- **Basis:** Databricks builds tasks from real code changes and manually checks samples.
  Uber uses a curated benchmark and feedback from engineers. coSTAR describes regression
  scenarios and alignment between model judges and human experts.
- **Observation:** Real tasks and known failures can become reusable evaluation cases.
- **Diagram:** Past task or failure → test case → agent run → checked result.
- **Limit:** Test suites can leak solutions, overfit, or miss valid alternative implementations.
  Databricks explicitly removes solution hints and revises tests. Keep model benchmarking
  separate from judging a workflow, and do not attribute broad coSTAR metrics to one internal agent.
- **Source anchors:** [Databricks, benchmark construction](../archive/sources/databricks-costar-source-2/content.md),
  [Databricks, coSTAR](../archive/sources/databricks-costar-source-1/content.md),
  [Uber, evaluation and feedback](../archive/sources/uber-ureview-source-1/content.md).

## Later topics and exclusions

- **Shared capabilities, separate interfaces or agents:** Shopify profiles, Sierra's
  gateway, and Domu's toolkit support this. N5 covers the first useful slice; avoid
  a broad platform essay until there is a focused question about repeated work.
- **Prepare the environment before the task:** Ramp, Stripe, and Browserbase supply
  concrete examples. Useful later, with cold-start cost and infrastructure prerequisites.
- **Measure accepted work:** Sierra, Replit, Harvey, and Spotify support a broader
  outcome note. The existing review-noise note already introduces downstream work;
  avoid merely restating it with more companies.
- **Start from work people can check:** Flex and Plaid offer non-coding examples, but
  verification details are uneven. Extend coverage before making a general selection rule.
- **Memory and long investigations:** Domu, monday.com, and Slack describe different
  mechanisms. Do not infer that file memory beats retrieval or that one memory design fits all tasks.
- **Build versus buy:** Airbnb, HubSpot, Notion, and WorkOS have relevant transitions.
  Current evidence does not support a universal winner or a quantitative break-even point.
- **Slack causes adoption:** Do not use this claim. Interface prevalence is not a causal
  result, and Domu provides an explicit limit to Slack's usefulness.

## Pass over all cases

Each approach appears once below. “Support” means a useful additional example, not an
independent replication or proof of effectiveness. “Hold” means the present evidence
adds too little to justify its own note.

| Case | Editorial decision | Theme | Reason or limitation |
| --- | --- | --- | --- |
| [Airbnb — Airchat (airchat-cli)](landscape.md#airbnb-airchat) | Later | Runtime changes | Abandoned a custom orchestrator; useful contrast, but not evidence that wrappers always win. |
| [Atlassian — Rovo Dev (RovoDev)](landscape.md#atlassian-rovo-dev) | Support N6 | Evaluation | Internal feedback data and a defined Jira-to-PR workflow; keep training data separate from evaluation data. |
| [Block — Builderbot](landscape.md#block-builderbot) | Later | Shared work | Live human steering and ticket-to-PR integration; does not establish that multiple agents outperform one. |
| [Brex — Internal Agent Platform](landscape.md#brex-agent-platform) | Later | Workflow ownership | Operations staff build and test workflows; useful non-engineering example, with secondary-only evidence. |
| [Browserbase — bb](landscape.md#browserbase-bb) | N1, N2, N3 | Access, recovery, context | Proxy checks session scope; source also describes conversation recovery and task-specific skills. |
| [Cloudflare — Internal AI engineering stack](landscape.md#cloudflare-ai-stack) | N3; support N1 | Tool discovery | Concrete schema overhead and search/execute design; the token reduction is not an accuracy result. |
| [Coinbase — Forge / Mux](landscape.md#coinbase-forge-mux) | Later | Shared work and isolation | Linear preserves work context; worktrees separate concurrent edits but are not security sandboxes. |
| [Databricks — coSTAR and internal engineering agents](landscape.md#databricks-costar) | N6 | Evaluation | Real codebase tasks, separate tests, manual sample review, and checks aligned with expert judgment. |
| [Domu — Clementino](landscape.md#domu-clementino) | N5; support N1 | Interface and approval | Actual interface limit and toolkit split; customer-impacting actions need approval. |
| [DoorDash — AI Code Review Agent](landscape.md#doordash-code-review) | Existing; support N6 | Stopping, decomposition, evaluation | Already supplies two notes; use other teams as the primary sources for most new notes. |
| [DoorDash — Flux / Agentic AI Platform](landscape.md#doordash-flux) | Support N3, N4; later | Tools and fixed checks | Scoped playbooks and SQL checks; adoption practices are a later topic. Do not count its reviewer twice. |
| [Dropbox — Nova](landscape.md#dropbox-nova) | Existing; N4 | Run limits and fixed steps | Keeping CI and publication outside the agent supports a distinct note beyond retry counts. |
| [Flex — AI Investigation Agent](landscape.md#flex-investigation-agent) | Later | Investigation to repair | Trace, hypothesis, and proposed PR form a clear workflow; runtime and validation detail are thin. |
| [GitHub — Qubot](landscape.md#github-qubot) | Hold | Data access | Useful use-case example; too little implementation evidence for a separate design note. |
| [Harvey — Spectre](landscape.md#harvey-spectre) | Support N2; later | Durable work and review effort | Durable runs and disposable compute support N2; review and coordination pressure support a later outcome note. |
| [HubSpot — Sidekick](landscape.md#hubspot-sidekick) | Existing; later | Review noise and runtime changes | Current note covers filtering. Runtime transition could support a later comparison with Airbnb. |
| [Linear — Linear Agent](landscape.md#linear-agent) | Support N1; later | Identity and systems of record | Scoped identities and human accountability; separate product features from documented internal use. |
| [Microsoft — PRAssistant](landscape.md#microsoft-prassistant) | Hold | Review coverage | Large reported deployment, but limited architecture detail. Scale alone does not add a new lesson. |
| [monday.com — Sphera / Atlas / Morphex](landscape.md#monday-sphera-atlas-morphex) | Support N4, N6; later | Checks and memory | Verification and ownership are useful; file memory does not prove that vector retrieval is unnecessary. |
| [Notion — Custom Agents](landscape.md#notion-custom-agents) | Later | Changing the runtime | Repeated harness rebuilds are relevant, but causes and before/after designs need more detail. |
| [Plaid — AI Annotator](landscape.md#plaid-ai-annotator) | Support N6 | Evaluation outside coding | Human alignment is a useful outcome example; sampling and measurement detail limit comparison. |
| [Plaid — Fix My Connection](landscape.md#plaid-fix-my-connection) | Later | Investigation to repair | Reported repair outcome supports the workflow theme; verification and action boundaries need more detail. |
| [Plaid — Internal MCP server](landscape.md#plaid-internal-mcp-server) | Support N1; later | Shared access | Identity-aware authorization and internal data access; distinguish server use from broad AI-client adoption. |
| [PostHog — StampHog](landscape.md#posthog-stamphog) | N4; support N1 | Fixed eligibility gates | Pinned implementation documents hard gates that a model cannot relax. |
| [Ramp — Inspect](landscape.md#ramp-inspect) | Later | Prepared environments and adoption | Warm environments and a product pivot are concrete; do not isolate one cause for adoption gains. |
| [Replit — Manager agent (agent-of-agents)](landscape.md#replit-manager-agent) | Later | Outcome measures and delegation | Review, reversion, and incident measures can extend the outcome theme; self-reported and not a controlled comparison. |
| [Retool — RetoolGPT](landscape.md#retool-retoolgpt) | Support N1 | Read-only scope | A useful simple access boundary; insufficient detail for a separate runtime note. |
| [Salesforce — Slackbot](landscape.md#salesforce-slackbot) | Support N1 | Permission-aware access | Employee permissions constrain visibility; implementation detail is limited. |
| [Sentry — Junior](landscape.md#sentry-junior) | N1, N2, N3 | Access, recovery, tool discovery | Proxy credentials, continuation after timeouts, and progressive tool lookup are documented mechanisms. |
| [Shopify — Aquifer / River](landscape.md#shopify-internal-agents) | N2; support N3; later | Durable work and shared platform | Session/harness/sandbox split is explicit; profiles and shared knowledge could support a later note. |
| [Sierra — Pinecone](landscape.md#sierra-pinecone) | N1, N2; later | Permissions, state, shared controls | Sources distinguish user and service identity, checkpoints, and common integrations. |
| [Slack — Multi-agent context system](landscape.md#slack-context-system) | Later | Working context | Structured findings and critiques concern long investigations; distinct from selective tool loading, but more specialized. |
| [Spotify — Honk / Xirp](landscape.md#spotify-honk-xirp) | Support N4; later | Fixed checks and company context | Trusted CI plus model review; older developer infrastructure is a prerequisite, not a model capability. |
| [Stripe — Minions](landscape.md#stripe-minions) | Existing; N4; later | Fixed workflow and environments | Blueprints separate code-controlled steps from model decisions; devboxes support a later setup note. |
| [Uber — Internal coding agent (unnamed)](landscape.md#uber-coding-agent) | Hold | Output volume | Headline changes-per-week and little architecture evidence; no distinct note justified. |
| [Uber — uReview](landscape.md#uber-ureview) | Existing; N6 | Review filtering and evaluation | Curated benchmark and developer feedback provide more than the existing noise note covers. |
| [WorkOS — Project Horizon](landscape.md#workos-project-horizon) | Support N1, N2; later | Control boundaries and runtime changes | Execution/lifecycle separation and scoped access; no general proof that every team needs custom infrastructure. |
| [Y Combinator — Internal agent infrastructure](landscape.md#ycombinator-agent-infra) | Hold | Custom infrastructure | Broad strategic claims with little implementation detail; not enough for prescriptive advice. |
| [Zup — CodeGen](landscape.md#zup-codegen) | Support N1, N4 | Constrained tools | Research case supports tool-level restrictions; keep the research stage visible. |

## Evidence handling

All 95 `lessons_learned` claims are catalog judgments. This review uses those as leads,
then checks reported implementation claims and selected preserved source passages.
All 39 records were reviewed; this was not a fresh re-verification of all 88 source URLs.

The source review found detail worth retaining during later catalog maintenance:
Browserbase explicitly describes conversation recovery after sandbox loss, and Sierra
explicitly separates user identity from service-account identity. Broad rubric values
must not erase these workflow-level distinctions. No catalog classifications were changed.

The six proposed articles should follow [the notes writing guide](notes-writing.md):
short STE-guided prose, exact brief quotations, original source links, clear attribution,
and a simple original diagram. No new public articles were created by this review.
