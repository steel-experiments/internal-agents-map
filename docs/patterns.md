# Architecture patterns

This page compares the 26 approaches in the catalog. It describes reported designs. It does not prescribe one definition of an agent.

Most evidence comes from organizations that describe their own systems. Architecture details are incomplete for many entries. Counts below use the catalog snapshot reviewed on August 12, 2026.

## Sample

The catalog contains these approach types:

| Type | Count |
| --- | ---: |
| Task agent | 9 |
| Platform | 8 |
| Background agent | 3 |
| Agent system | 3 |
| Orchestration system | 2 |
| Supporting pattern | 1 |

Compare approaches of the same type and deployment stage before you draw a conclusion. A platform and a task agent have different responsibilities.

## A common set of components

Among entries with detailed technical reports, several components recur:

```text
invocation
    |
identity and policy
    |
company context
    |
harness and model
    |
execution environment
    |
scoped tools
    |
verification and review
    |
system of record
```

No catalog rule requires this exact design. Some entries implement only part of it. The [Slack context system](landscape.md#slack-context-system), for example, documents context management rather than a complete execution platform.

## Execution environments

Fourteen entries document a concrete execution environment. Reported examples include Firecracker micro virtual machines at DoorDash, Modal sandboxes at Ramp, Kubernetes containers at Spotify, and isolated worktrees at Coinbase.

The remaining entries either omit the detail or describe no separate execution environment. This absence is an evidence gap. It is not proof that no isolation exists.

Several reported designs separate durable work state from temporary compute. Sierra keeps conversation state and checkpoints outside its runners. WorkOS separates its orchestrator from its containers. Spotify runs work in constrained Kubernetes containers. These examples support a useful comparison question: what survives when a worker stops?

## Harnesses and model choice

The catalog shows three broad harness choices:

- A team wraps a vendor software development kit or an existing agent runtime.
- A team coordinates several agents through its own orchestration layer.
- A team builds a custom runtime to control task state, interruption, or verification.

Some organizations report support for several models. Sierra routes work by task. Cloudflare routes models through its gateway. monday.com wraps its model software development kit. These examples do not show that every system can change models during an active task.

Model portability is therefore a rubric question, not a general conclusion. Future records should distinguish model selection at task start from a model change during a task.

## Tools and access controls

Many entries report a gateway or proxy between the model and internal systems. The Model Context Protocol (MCP) appears in the DoorDash, Cloudflare, Sierra, WorkOS, Block, Sentry, and Brex records.

Reported controls include:

- A limited tool set for each task
- User or service authorization at the tool boundary
- Approval gates for consequential actions
- Short-lived or scoped tokens
- Network proxies that inject credentials
- Deterministic tests before a change can proceed

These controls reduce access and limit impact. They do not make incorrect or harmful action impossible. A system can still supply a scoped session token to a worker even when it keeps a long-lived credential outside that worker.

## Company context

Several organizations expose code ownership, service catalogs, tickets, documentation, or telemetry to their systems. Spotify and Cloudflare use service catalog data. Linear uses workspace records. DoorDash reports hybrid retrieval for company information.

The implementations differ. Some use repository instruction files. Some query live systems. Others load domain playbooks when needed. The evidence supports company context as a recurring investment. It does not establish one best storage or retrieval method.

## Invocation

Twenty of 26 entries list Slack as an interface. GitHub, web interfaces, command-line tools, scheduled jobs, and event handlers also appear.

This count shows where reported systems appear in the sample. It does not show that Slack causes adoption. Public channels can help people observe agent work, but they can also expose private or sensitive information. Teams must apply access and retention rules before they copy this practice.

## State and identity

The current public evidence does not document state duration for 22 entries. Four entries describe durable session state. This gap is why durable identity belongs in the rubric instead of the inclusion policy.

The rubric asks separate questions:

- Does state end with one run?
- Does a session survive a worker restart?
- Does memory persist across sessions?
- Does the system act as the user, a service, or a dedicated agent identity?

These choices affect audit records, authorization, recovery, and accountability. Unknown values remain unknown until a source documents them.

## Verification and autonomy

The catalog classifies 18 approaches as `drafts-reviewed`, seven as `human-in-loop`, and one as `autonomous`. These labels describe the reported review boundary. They do not measure output quality.

Reported verification methods include tests, continuous integration checks, schema checks, query planning, policy checks, model judges, and human review. Deterministic checks and model review serve different purposes. A model judge does not replace a test that can decide a property directly.

## Metrics

The reported metrics are not directly comparable. Some measure agent output. Others measure broad AI tool use, automated workflows, sessions, or user adoption.

For example, Spotify reports Honk pull requests and wider Fleet Management automation in the same record. Cloudflare reports traffic for a larger AI engineering system. Keep these scopes separate when you use the data.

Each future metric should record its date, system scope, denominator, method, and source. Treat a company metric as self-reported unless an independent source verifies it.

## Questions for future research

The current evidence leaves several useful questions open:

- Which state and identity models work for each approach type?
- Which controls stop a documented failure rather than a hypothetical one?
- How much review time does generated work require?
- Which metrics remain useful after adoption grows?
- When does a shared platform outperform a narrow task agent?
- Which systems were reduced or removed after deployment?

Add conflicting evidence and reported failures when you find them. A complete map needs negative results as much as successful launches.
