> Archived source snapshot  
> Source ID: `browserbase-bb-source-1`  
> Original URL: <https://browserbase.com/blog/internal-agents>  
> Final URL: <https://www.browserbase.com/blog/internal-agents>  
> Title: How We Build Internal Agents at Browserbase (bb) | Browserbase  
> Captured at: `2026-08-31T17:40:42Z`

---

**TLDR; Generalized agents will become the interface for knowledge work and the browser is the universal “API” for everything that doesn’t expose one.**

Bret Taylor theorizes that the [future of work will be interfaced by agents](https://x.com/tbpn/status/2041286830214259069), give them a task and have them complete it on your behalf. We agree.

"Now we think, in the future, most people are just going to be talking to AI agents, and they're just going to be performing those actions on your behalf.”

Every closed support ticket, every meeting transcript, every data pull, and many PRs at Browserbase goes through one generalized agent. Its name is **bb**.

`@bb` lives in Slack and can write PRs, investigate production sessions, query Snowflake, log feature requests to HubSpot, and run browser agents across engineering, ops, sales, support, and exec.

Instead of building a bot per task, we run one agent loop and “lazy load” two things per task: **skills** (playbooks) and **permissions** (scope). Today, **Agents are most valuable when you point them at easy problems you already know how to solve, giving you more time to work on the hard problems**. We encode those playbooks as skills and let bb run them.

We’ve already connected it to a majority of our systems, but a lot of knowledge work doesn’t happen behind clean APIs. It happens in web apps built for humans (dashboards, portals, inboxes, PDFs). The Browserbase Platform ensures that BB can do all of the same work that we do.

### The results

Our feature request pipeline runs at 100% coverage with zero human effort. Every closed support ticket and every meeting transcript gets scanned automatically, helping reduce 99% of our first response time to <24hrs. Session investigation dropped from 30–60 minutes of manual log-diving to a single Slack message. Many engineers went from writing a majority of PRs by hand to reviewing them.

This post is the full architecture. Sandbox, credential brokering, skill system, Slack integration, and the patterns that make it all work.

![](https://cdn.sanity.io/images/yd6zslid/production/5692d5546181ceb0a054eaf23ba5502a166e1b4e-2920x1412.png?fm=webp&h=774&w=1600&auto=format&fit=min&q=75)

## The Sandbox:

At the core of any deployed agent is it’s execution environment. You need a place where the agent can read files, write code, run shell commands, call APIs, and do it all without touching production infrastructure or leaking credentials.

We run each agent session in an **isolated cloud sandbox,** an ephemeral Linux VM with its own filesystem, network stack, and process tree. Think of it like a fresh laptop that boots in seconds, already has everything installed, and gets thrown away when the work is done. The sandbox idles out after 30 minutes of inactivity, and no state persists between sessions unless we explicitly snapshot it.

### What's inside

The interesting part isn't the sandbox product, it's what we bake into it. Every sandbox starts from a **pre-warmed snapshot** that gets rebuilt every 30 minutes via a cron job:

- **Key Browserbase repositories** cloned into a `/knowledge/` directory. This is the agent's codebase brain. It can grep, read, and reason about any repo without a network fetch.
- The **agents monorepo** itself, fully built with dependencies installed.
- [**OpenCode**](https://opencode.ai/) (the agent runtime) pre-installed and pre-started on a local port, ready to accept prompts immediately.
- **System tools**: bun, git, GitHub CLI, ripgrep, prettier, pdftotext, a TypeScript LSP, and Tailscale for secure network access.

The agent gets **6 tools**:

- `read`: Read files from the filesystem
- `write`: Create new files
- `edit`: Patch existing files
- `exec`: Execute JavaScript with access to all service integrations via proxy
- `safebash`: Run allowlisted shell commands (grep, git, find, jq, etc.)
- `skill`: Load domain-specific instruction sets into context

The `exec` tool is the gateway to everything external (Snowflake, HubSpot, Pylon, Grafana) all routed through a serverless proxy that we'll cover in the next section.

The 30-minute snapshot refresh means the sandbox is at most half an hour behind the latest code on main. When a new sandbox boots, it pulls just the delta (typically a handful of commits) making startup nearly instant.

Anthropic’s Managed Agents and OpenAI’s new agent SDK both separate the harness from the compute (filesystem/sandbox), something we’ve also found to be more performant over all. We’re currently migrating to that architecture, building composable units as isolated and modular as possible. The landscape of agents changes extremely fast, what started as thick custom-tool harnesses has simplified to while loops and separated “brain and hands”. Building our internal agents in “building blocks” helps us reconfigure to SOTA architectures rapidly.

### Deployed → Background → UI Interface

The same agent runs in 4 modes, and the transition between them is surprisingly smooth:

**Deployed (Slack interactive)**: Someone types `@bb` in a Slack channel. The Slack events handler dispatches to an internal endpoint, which creates or reuses a sandbox keyed by the Slack thread ID in a KV store. The agent streams SSE events back, which get translated into real-time Slack message updates. The sandbox persists for multi-turn continuity and follow-up messages in the same thread hit the same sandbox with full conversation history.

```typescript
// Sample Implementation
function dispatch(threadId: string, message: string, user: { displayName: string }) {
  let sandboxId = KV.get("thread:" + threadId + ":sandbox");

  if (!sandboxId) {
    sandboxId = createSandbox({ fromSnapshot: latestSnapshot });
    KV.set("thread:" + threadId + ":sandbox", sandboxId, 86400);
  }

  const stream = sendToAgent(sandboxId, {
    message: message,
    : user.displayName,
    sessionId: threadId,
  });

  for (const event of stream) {
    updateSlackThread(threadId, event);
  }
}
```

**Background (webhooks)**: External events like a Pylon support ticket closing or a Circleback meeting transcript landing trigger webhook handlers that dispatch to the same sandbox infrastructure in "webhook" mode. The agent does its work (detect feature requests, log to HubSpot, post a summary to a dedicated Slack channel) and the sandbox shuts down.

**UI Interface:**

BB also has a rich UI interface, which displays reasoning traces, tool calls, and the sandbox state and filesystem, all in a beautifully designed chat. (Which you might [recognize](http://director.ai/))

For agents to be used to their full capacity, you have to be able to meet people where they are (and where they work). This interface allows anyone to use BB at anytime, whenever, however, and wherever they are.

![](https://cdn.sanity.io/images/yd6zslid/production/3b5efb0efc0d8f0b33de50ce0af4e047cb3cdcde-2032x1167.png?fm=webp&h=919&w=1600&auto=format&fit=min&q=75)

## Credential Brokering: The Sandbox never touches a secret

Here's the uncomfortable truth about agent sandboxes: they run arbitrary code. The LLM decides what to execute, and the sandbox executes it. If you pass API keys as environment variables, nothing stops the agent from running `echo $SOME_API_KEY` or writing credentials to a file that gets committed.

We solve this by splitting “access” into two layers: **credential brokering** and a **secure integration proxy**.

![](https://cdn.sanity.io/images/yd6zslid/production/99d12743c60e874ffcad6dd3990c483debb62581-2920x1412.png?fm=webp&h=774&w=1600&auto=format&fit=min&q=75)

Instead of baking secrets into the sandbox, the sandbox boots with only *references* and short-lived tokens:

1. `BB_PROXY_URL` — the URL of a serverless integration proxy
2. `BB_SESSION_TOKEN` — a rotating session token (TTL’d in a KV store)
3. `AUTOMATION_BYPASS_TOKEN` — a second token required for certain third-party automation flows

Most third-party access is served through the integration proxy, which holds the real credentials and enforces policy (what services/methods are allowed, and under what scope) before any request is executed.

For a small set of integrations, we also do true credential brokering at the network layer (the sandbox never sees the real key). This is powerful, but it’s not a silver bullet.

In practice, only a few secrets are brokered. Everything else stays behind the integration proxy.

If a sandbox crashes, we don’t lose the conversation. Messages live in the KV store and the thread can be resumed. Some environment state may be lost, but the work can continue.

### How the proxy works

The flow is simple:

1. The agent's `exec` tool constructs a request: `POST /api/proxy` with `{ token, service, method, args }`
2. The proxy validates the token against the KV store and retrieves the session's permission scope
3. The proxy checks if the requested `service.method` is allowed
4. If allowed, it calls the real service package (which has actual credentials available only inside the serverless function's environment) and returns the result
5. If denied, it returns a 403

```typescript
// Simplified proxy handler
const serviceRegistry: Record<string, any> = {
  dataWarehouse: DataWarehouseService,
  crm: CrmService,
  support: SupportService,
  observability: ObservabilityService,
  chat: ChatService,
};

export async function POST(req: Request) {
  const { token, service, method, args } = await req.json();

  // Validate session token
  const session = await kv.get<ProxySession>(\`session:${token}\`);
  if (!session) return new Response("Unauthorized", { status: 401 });

  // Check permission scope
  const allowed = matchesGlob(session.permissions.services, \`${service}.${method}\`);
  if (!allowed) return new Response("Forbidden", { status: 403 });

  // Call the real service with real credentials
  const svc = serviceRegistry[service];
  const result = await svc[method](...args);

  return Response.json(result);
}
```

For a small set of integrations (model providers and code hosting), credential brokering happens at the **network level**. The sandbox firewall intercepts outbound HTTP requests to specific hosts and injects real API keys on egress. The sandbox environment variable is set to a placeholder string like `"credential-brokered"` so the SDK initializes without erroring, but the actual key gets injected transparently before the request ever leaves the sandbox.

Credential brokering isn’t the final frontier for secure agent access. Even with brokered credentials, an agent can still generate arbitrary HTTP requests, so we add request interception and domain allowlisting for sensitive internal APIs (e.g., enforcing what domains the browser tool is allowed to reach) regardless of what code the agent writes.

### RBAC & ABAC: Layering Agent Restrictions

BB has traditional RBAC, but also ABAC (Agent based access control). Each proxy session carries a default PermissionConfig with two dimensions:

```typescript
type PermissionConfig = {
  // Which service.method calls are allowed (glob patterns)
  services?: string[]; // e.g., ["crm.*", "support.getIssue"]

  // Which OpenCode tools the agent can use
  tools?: {
    read?: boolean;
    write?: boolean;
    edit?: boolean;
    exec?: boolean;
    safebash?: boolean;
    skill?: boolean;
  };
};
```

**Interactive Slack sessions** get full access, the agent self-selects which skills and services it needs.

**Background webhook sessions** get hard-scoped permissions at invocation time. For example, our Pylon ticket-closed webhook handler:

```typescript
await dispatchWebhook({
  prompt: \`Analyze this closed support ticket for feature requests: ${issue.title}\`,
  permissions: {
    tools: { exec: true, skill: true },
    services: ["crm.*", "support.*"],
  },
});
```

This is **defense in depth**. We don't rely on the model to behave. The system makes misbehavior structurally impossible for a given session scope.

We combine traditional service-level RBAC (e.g., the Snowflake role is read-only) with **agent-specific restrictions** layered on top. Even if the agent has access to Snowflake, it can only run SELECT queries. Even if it has access to HubSpot, a scoped session might only allow `hubspot.search*` and not `hubspot.delete*`. We’ve also noticed permissions tend to correlate with invocation source. For example webhooks carry intent, so a CRM-triggered run might need sales tools but not code access.

Credential brokering means we don’t have to just “trust the model”, we can just remove it’s ability to do wrong.

## One Agent, Many Skills: How bb Generalizes

Most internal agents start as coding agents. Ours did too. The question that changed everything was: if the agent can already read code, write files, and call APIs, why can't it do everything else?

All we had to do was separate the agent's **capabilities** from its **core loop**.

The core loop is [OpenCode](https://opencode.ai/). It handles the LLM conversation, tool orchestration, context management, streaming, and context compaction. We don't touch any of that. Everything domain-specific lives in two layers on top:

### Skills are just loadable context

**Skills** are markdown files in `.opencode/skills/` that inject domain-specific workflows, schemas, and decision trees into the agent's context on demand. These md files give BB structured and detailed instructions on how to do a specific job.

This is progressive disclosure: the general agent stays simple, and only pulls in the minimum context it needs for the task. In practice, “building a general agent” can be as easy as adding heuristics in the system prompt for when to load which skill.

Some of our favorite skills:

- `data-warehouse`: Warehouse query patterns — table definitions, column types, common joins
- `customer-intelligence`: Cross-system query patterns (data warehouse + CRM + support system + billing)
- `crm`: Deal fields, pipeline stages, contact properties, dedup logic
- `investigate-session`: Multi-source log correlation (Tinybird + Loki + NATS message flow)
- `create-pr`: Linear ticket → git branch → code changes → PR workflow
- `write-browserbase-web-automations`: Stagehand scripting patterns for browser tasks
- `log-feature-request`: Feature request detection, CRM dedup, categorization
- `notion`: Read-only access to Notion pages and databases
- `whimsy`: For fun (of course)

A typical skill file looks something like this:

```
# Investigate Session

When asked to investigate a Browserbase session, follow this process:

## 1. Gather session metadata
- Query Tinybird for the session record: \`exec.queryTinybird("SELECT * FROM sessions WHERE id = '{session_id}'")\`
- Check session status, timestamps, and error codes

## 2. Pull service logs
- Query Loki for browser service logs in the session's time window
- Query Loki for connect service logs
- Query Loki for API gateway logs
- Look for: connection timeouts, NATS message drops, proxy chain failures

## 3. Correlate and diagnose
- Map the session lifecycle: create → connect → browser_ready → page_load → action → close
- Identify where the lifecycle broke
- Check for known patterns: race conditions in browser-connect handshake, ...
```

The skill encodes the exact debugging playbook a senior engineer would follow. The agent doesn't need to figure out which logs to check or what the session lifecycle looks like, the skill just tells it.

### Service packages: Typed API wrappers

The second layer is **service packages**: typed TypeScript wrappers around external APIs that get called through the proxy. Each package exposes methods that the `exec` tool can invoke.

This is a big reason bb is performant: it keeps the tool surface small, defines the TypeScript interfaces once in the `exec` tool, and lets the agent do dynamic pre-transforming in deterministic code before results ever hit context.

In practice that means parallel calls (`Promise.all`), parsing/normalizing outputs in TypeScript, and for large payloads writing results straight to disk via `exec.writeToFile` instead of bloating the prompt.

```typescript
// Inside the exec tool's runtime, the agent can call:
const usage = await exec.queryWarehouse(\`SELECT ...\`);

const deals = await exec.searchCrm("deals", {
  filters: [{ property: "company", operator: "EQ", value: companyName }],
});
```

Adding a new integration is straightforward: write a service package, add it to the proxy dispatch map, expose an exec method, and write a skill with domain-specific instructions. Most integrations take less than an afternoon.

### Routing: How the agent picks skills

The system prompt in `bb.md` contains a routing table that maps request patterns to skills:

```
## Skill routing

Based on the user's request, load the appropriate skills:

- Session investigation, debugging, or error analysis → load \`investigate-session\`
- Pull request, code change, or Linear ticket → load \`create-pr\`
- Customer data, usage trends, or account questions → load \`snowflake\` + \`customer-intelligence\`
- Feature request logging or triage → load \`log-feature-request\`
- HubSpot deal or contact questions → load \`hubspot-crm\`
- Browser automation or web data retrieval → load \`write-browserbase-web-automations\`
- Notion page or database queries → load \`notion\`

Load only what you need. Do not load all skills for every request.
```

For interactive Slack sessions, the agent reads this routing table and self-selects. For background webhook sessions, the permissions system hard-restricts which tools and services are available so even if the routing table suggests loading a skill, the agent can only act within its scoped permissions.

## Slack: Where conversations become PRs

Slack is the primary interface because that's where work conversations already happen. The entire interaction model is built around a simple premise: you describe intent, the agent executes, you course-correct.

![](https://cdn.sanity.io/images/yd6zslid/production/9fdccbb5174ef73a5a1d8c6a7fa00fea21ff7f6f-1064x1342.png?fm=webp&h=2018&w=1600&auto=format&fit=min&q=75)

### Day-to-day

Someone types `@bb investigate session sess_abc123` or `@bb what's the usage trend for Acme Corp` in any Slack channel. bb reacts with a 🧑🍳 emoji, spins up a sandbox (or reuses an existing one for the same thread), and starts streaming its response back in real-time. You see text appear, tool calls flash by (file reads, SQL queries, API calls) and the final answer lands as a Slack message. Charts get uploaded as image attachments. CSV exports get sent as file uploads.

Follow-ups are natural: just `@bb` again in the same thread. The sandbox persists, so the agent has all the context from the previous turn including files it read, queries it ran, results it got. You don't re-explain anything.

If bb is mid-response and you send a new message, the current run auto-aborts and restarts with your new context. No stale work, no waiting for a response you've already moved past.

### Humans as channel managers

The interaction model is closer to managing a competent teammate than running a tool. You describe what you need at a high level, "check if Acme's sessions are failing more than usual this week" and the agent figures out the implementation: which tables to query, which logs to check, how to format the answer.

Slack threads give you **free multi-turn state**. Each thread is a persistent workspace with its own sandbox, conversation history, and file state. This is used across the entire company, engineering, ops, sales, support, and exec. The people using bb most heavily aren't always engineers.

People are becoming "channel managers." Instead of doing the work themselves, they manage agents running in Slack channels. It's a subtle but significant shift in how a team operates.

## So?

If generalized agents are going to be the interface for knowledge work, then the winning systems won’t be a pile of one-off bots, they’ll be **one core loop** with the right abstractions for **execution** (the sandbox), **access** (credential brokering + scoped permissions), and **repeatability** (skills). The architecture is simple enough to replicate. You need four things:

1. **A sandbox** — any isolated execution environment with snapshot support and fast cold starts
2. **A proxy** — a serverless function that holds real credentials and brokers access with scoped permissions
3. **An agent harness** — we use [OpenCode](https://opencode.ai/), but any agent loop with a server API works
4. **An agent interface** — Slack is the highest-leverage starting point because it's where your team already communicates

One agent with good abstractions beats a fleet of narrow bots. Build your own bb.
