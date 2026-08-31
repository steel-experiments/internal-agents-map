> Archived source snapshot  
> Source ID: `sentry-junior-source-1`  
> Original URL: <https://cra.mr/building-an-intern/>  
> Final URL: <https://cra.mr/building-an-intern/>  
> Title: Building an Intern  
> Captured at: `2026-08-31T17:48:07Z`

---

I’ve been building [Junior](https://junior.sentry.dev/) for the last four months. The short version: it’s an intern in Slack.

Originally it started as a joke, *it’s my junior*, but only in the sense that I’m grounded in what models are and aren’t capable of. I describe it as an intern because I think that’s a pretty literal concept here. You give them information, you review their work, and you steer them in the right direction.

My goal was pretty straightforward:

- perform basic tasks within Slack
- keep the runtime as secure as is practical
- avoid running infrastructure

It seemed easy at first. I wrote about the early version in [Building a Slack Agent with Pi on Vercel](https://cra.mr/building-a-slack-agent-with-pi-on-vercel/). It worked, but you were quick to spot things that could be improved in the UX and limitations of using stateless compute.

I spent the next four months iterating on my ideas and bringing some sense of stability to the harness. Frankly it was a lot more effort than I had expected. It’s now around 100,000 lines of TypeScript before you count tests, evals, docs, and the all-important lockfiles. I mention this because I want people to understand software isn’t free, and if you want to turn an idea into a good product, it’s still a large (and often ongoing) time commitment. This project probably amplified that.

The code is open source at [github.com/getsentry/junior](https://github.com/getsentry/junior), and the docs live at [junior.sentry.dev](https://junior.sentry.dev/).

## I don’t want another agent

Every vendor is building an agent now. Sentry has one. So does Datadog, GitHub, Linear, and everyone else under the sun. They’re fine, but they’re constrained. They know their product better than an MCP and a set of skills, and they often add value here and there due to their specialization. They just don’t hit for me. I don’t work with one product, nor do I work with the concepts and playbooks that any given vendor decides matter for me.

I have conversations - mostly in Slack - where in any given moment I want to answer a question from any given source of material, turn that into an action-now or action-later task, and I don’t want to worry about which of N bots I need to cross-collaborate with to do that. More importantly, I also don’t want to jump into something like Chat or Claude to answer these concerns.

This is what I am addressing with Junior. In the same way any other generalized agent would do it, but one built for us.

Instead of asking a PM how some part of Sentry works, you can ask Junior. Not because Junior already knows, because it usually doesn’t. Because it can (and will!) go look: search the repo, trace the code path, and answer from code instead of ignoring your question or only doing a half-ass job.

![](https://cra.mr/assets/junior/junior-product-question.png)

Junior answering a Slack question about how access to private code actually works.

The first early win truly was GitHub issues for me. We already had Linear in Slack and folks regularly used it to quickly create issues (albeit, not great versions), but we were missing this kind of productivity boost for GitHub. So many times I’d find myself working on a project, having a conversation, just wishing I had an agent right there that I could tag, have it summarize it, and open the ticket. Now I do. Even more so, I can have Junior go deeper than any of these other tools would: do the gap analysis, create an RCA, and really give a solid starting point for just summarizing a few sentences of text. Unlike the rest of us, it doesn’t get lazy halfway through.

Visual QA was another one. Junior does this with Vercel’s [`agent-browser`](https://github.com/vercel-labs/agent-browser). Someone can ask it to open a feature, click around, take screenshots or videos, and write up the rough edges in the same thread where the team is already talking about the work. We’re still early here, but my hope is we can get the agent automatically QA’ing most Sentry frontend changes since the experience here is really great.

![](https://cra.mr/assets/junior/junior-visual-qa.png)

Junior doing visual QA. Not perfect, obviously: I still had to ask where the files went.

The collaborative part was almost accidental. I mostly wanted access to these tools from Slack, but as soon as that worked, everyone else saw the value. There was a bit of a push on our end (“waste the robots’ time instead of humans, please”), but broadly speaking I think it’s hard to not recognize the value once you experience it. Junior quickly went from getting tagged here and there to being used quite frequently throughout the day.

## Junior is not trying to win the agent race

Junior is a harness more than it is a finished agent, and it isn’t going to be the best at everything.

I know the comparison people will make: OpenClaw, Hermes, or whatever other slop is popular this week. I don’t pay them much attention other than looking for inspiration here and there. I’m trying to solve Sentry’s problem: a secure agent in Slack that has access to as much of our workflow toolchain as it can. One that increases in value over time, and one where we won’t create liability that is otherwise avoidable.

My best example is coding tasks. Junior can do them, but it’s absolutely garbage at it. It has all the same tools you’d expect from any competitive coding agent, but it will perform worse. Part of it is because of the default configuration - we use Sonnet by default because for most concerns we’d prefer faster answers to waiting on a more expensive model like Opus. There’s also the other gap where we’ve loaded it up with quite a few general-purpose skills and tools. While it’s possible to have those minimize the impact, you still can’t work past the model concern.

That’s fine for us, and one of the reasons Junior is engineered to work as a framework, to be customizable, is to allow us to experiment with purpose-built installs. The coding example is one we’re going to actually explore to see if another instance of Junior can actually be tuned enough to work competitively well (e.g. as good as Cursor or Claude via Slack). We think it’s doable, and when you combine the other capabilities and UX on top I think we’ll find ourselves reaching for it more.

In fact, the only reason Junior is open source is because I - and Sentry - do open source. If you get value out of that, great! If not, totally cool, it’s just how we roll.

## This is where it gets complicated

When you think about a Slackbot, it’s “receive webhook, call model, post reply.” You throw in a few tools. Done, right? If only. Serverless functions have timeouts. They disappear. Then you need authentication. What about steering? Obviously it’s more complicated than I originally suggested, but you don’t really consider how complex things get until you’re deep into the weeds.

Junior’s architecture around this has gotten increasingly complex - despite my attempts to simplify it:

```text
Slack webhook
  -> saved to the conversation's inbox
  -> enqueue conversation task
  -> worker claims the conversation
  -> agent continues from the session log
  -> [repeat by interrupts to avoid timeouts]
  -> final reply posted to Slack
```

This is a pretty standard approach to this kind of task broker, and it’s built on top of Vercel Queues:

```ts
async function workConversation(message) {
  const conversation = await loadConversation(message.conversationId);

  // nothing to do, or another worker is already on it
  if (!conversation.hasPendingWork()) return;
  if (conversation.hasActiveLease()) return checkAgainLater(message);

  // claim the conversation so no other worker touches it
  const lease = await acquireLease(conversation);

  // pull in whatever arrived since last time, then keep going
  await ingestPendingMessages(conversation);

  // finish the run or interrupt safely after a tool result so
  // we can avoid serverless timeouts
  const result = await withInterruptTimer(continueAgent(conversation));

  if (result.finished) {
    await deliverReplyToSlack(result);
    await markComplete(conversation, lease);
  } else {
    // out of time: progress is already saved, so ask for
    // another wake-up and let go
    await requeueForContinuation(message);
    await releaseLease(conversation, lease);
  }
}
```

The real code has more edge cases, but you can get a good idea for the complexity from the above. Suffice to say it’s a lot of moving parts, and while they’re arguably valuable to create reliability, a lot of it comes from working around platform constraints.

## Stateless compute is hostile to agents

Junior runs on Vercel. Both Vercel and Cloudflare provide a bunch of great primitives here: compute, sandboxes, brokers, and storage (albeit Vercel’s storage is third-party). This is great, but I alluded to how stateless compute (serverless) creates a lot of complexity and inefficiency. It’s clearly an understood problem as providers have been working to increase function runtimes.

It goes beyond just the timeouts and ephemeral nature of this stuff though. Even bundling something like Junior on these platforms is excessively complex. I wanted a simple architecture that you could install Junior, customize it (e.g. `SOUL.md`, skills, etc), and deploy it. Oh right, it’s the JS ecosystem which means I need to deal with bundlers. I settled on Nitro to solve for this, and while it’s not been without its challenges, it’s been mostly ok at hiding this complexity:

```ts
import { juniorNitro } from "@sentry/junior/nitro";

export default defineNitroConfig({
  modules: [
    juniorNitro({
      maxDuration: 300,
      plugins: "./plugins",
      dashboard: {
        allowedGoogleDomains: ["sentry.io"],
      },
    }),
  ],
});
```

The challenge ends up being that you have to register a handful of niche Vercel primitives. Vercel Queue triggers, for example, have to be defined in a specific way and have to be public routes. It’s all plumbing that doesn’t need to exist, but it does because of the forced adaptation around serverless. Once you work around this it ends up being somewhat ok - though I’ll admit I still have a handful of TODOs, and I’m sure someone who cares (or knows more) could find some better approaches.

Ultimately the real challenge was the timeouts. The default for Vercel was (is?) 300 seconds, and very few meaningful agentic runs finish in ~5 minutes. So we implement a soft deadline at 240 seconds, attempting to create a resumable point (end of a tool result). When it hits, Junior pauses and enqueues a continuation task to resume where it left off. It ends up being a nice architecture even if timeouts were longer, but it’s a lot more moving parts.

A big part of this means incrementally persisting the conversation transcript (Pi’s session log). We currently just stuff this into Redis and update it as progress is made in the run. This has a lot of benefits so is worth doing either way. It lets us see in ~realtime what’s happening with a thread, but also allows graceful recovery. It’s not all that different than what Codex and Claude do locally when they append to the session log on disk.

I do wish this all could be done with less plumbing, as everyone has to build the ~same thing here, but in my experience the bigger adapters (like AI SDK) end up being more work than they’re worth due to the complexity exposed in their interface, which is why we opted to use Pi’s SDK here (which I believe is built on top of AI SDK). We’ll let that headache be [Mario’s](https://x.com/badlogicgames) problem.

## Credential management is hard

The first challenge we hit was credential management. Vercel provides a MITM proxy that allows you to intercept all traffic coming out of the Sandbox. This is the perfect solution for safe credential injection, but it’s a bit more nuanced than that.

A simple use case would just say: all requests to github.com should use this access token. Where do you get the access token though? And is it really all requests?

I started by just implementing a baseline interceptor, so it would know which domains needed which credentials, and abstracted the OAuth flows via the plugin metadata:

```yaml
name: sentry
display-name: Sentry
description: Sentry issue tracking

config-keys:
  - org
  - project

credentials:
  type: oauth-bearer
  domains:
    - sentry.io
    - us.sentry.io
    - de.sentry.io
  auth-token-env: SENTRY_AUTH_TOKEN
  auth-token-placeholder: host_managed_credential

oauth:
  client-id-env: SENTRY_CLIENT_ID
  client-secret-env: SENTRY_CLIENT_SECRET
  authorize-endpoint: https://sentry.io/oauth/authorize/
  token-endpoint: https://sentry.io/oauth/token/
  scope: "event:read org:read project:read team:read"

runtime-dependencies:
  - type: npm
    package: sentry
```

Whenever a request to any of the domains above is made, Junior will determine if it has a valid credential, inject it if needed, and if not, interrupt the agent to pause for authentication (which it does via ephemeral Slack links). It’s mostly a good experience (caveat: bugs), and solves the problem really, really well.

Roughly this looks something like this:

```text
sandbox command
  -> https://us.sentry.io/api/...
  -> Vercel Sandbox network policy forwards to Junior
  -> Junior verifies sandbox OIDC token
  -> Junior verifies signed credential context
  -> Junior resolves provider from forwarded host
  -> Junior issues short-lived lease
  -> Junior adds Authorization header from host side
  -> upstream provider receives the request
```

**The model never has access to the token, because it’s never in the sandbox.**

GitHub is my favorite example because it’s where everything goes from a simple idea to a ton of complexity. The [GitHub plugin](https://github.com/getsentry/junior/tree/main/packages/junior-github) declares `api.github.com` and `github.com`, exposes a placeholder sandbox `GITHUB_TOKEN` for CLI compatibility, and then decides which real grant to issue from the HTTP evidence:

```ts
function grantForGitHubRequest(request) {
  if (isRawIssueOrPullRequestCreate(request)) {
    throw new EgressPolicyDenied(
      "Use the typed GitHub tool so Junior owns idempotency.",
    );
  }

  if (isGitSmartHttpWrite(request)) return "user-write";
  if (isRestWrite(request)) return "user-write";
  if (isGraphqlMutation(request)) return "user-write";
  if (isGetUser(request)) return "user-read";
  return "installation-read";
}
```

That’s not exactly how it works, but what we’re trying to do here is allow global read access, but for writes require per-user authorization. That needs a normal OAuth flow on top of a global installation token. Easy enough, but you’ll notice my favorite subject in there: GraphQL.

Raw sandbox calls to `POST /repos/:owner/:repo/issues`, `POST /repos/:owner/:repo/pulls`, or the equivalent GraphQL mutations have to be rejected without the appropriate credentials. That meant we had to parse GraphQL because it intentionally ignores HTTP semantics. We actually go beyond this, because we also restrict certain operations now without additional permission. For example, we force any issue or pull request creation to go through our tools so we can add a deterministic footer.

It’s not pretty, but it’s become quite an effective solution. We’ve taken this same approach with interceptors to force some deterministic behavior beyond auth. For example, when the agent wants to create a GitHub issue, we want it to have an explicit footer attached. We do that by blocking the appropriate requests *unless* they contain a JWT token that signals they’re authorized. We then register a set of custom tools for the agent to use. It would generally use these by default, but best effort wasn’t my goal here. I want it to *only* be able to do things the right way.

## Don’t dump every tool into the prompt

I’ve written enough about [MCP, skills, and agents](https://cra.mr/mcp-skills-and-agents/) to be annoying about it, so I’ll spare you the full rant here. For Junior, MCP is important, but it’s not enough on its own.

We handled MCP authentication the same way we handle generalized OAuth from a user experience angle, but we go beyond that and do progressive discovery. This is the same basic shape I wrote about in [A Bigger Toolbox for MCP](https://cra.mr/a-bigger-toolbox-for-mcp/): keep the always-on surface small, let the agent search when it needs more, then execute the specific thing it found.

Junior does even more to improve this behavior. By default, Junior doesn’t connect to *any* MCP provider. We only connect to an MCP when the agent specifically requests a tool lookup for it (via `searchMcpTools`).

To the model, the flow looks more like this:

```ts
await searchMcpTools({ provider: "example-provider" });

await callMcpTool({
  toolName: "mcp__example-provider__find_account",
  arguments: {
    email: "person@example.com",
  },
});
```

We haven’t gone farther than this yet for progressive tool discovery, but we added support for plugins to register tools so that’s pretty high on my list to improve now. It’s likely we’ll end up with the same pattern: some p0 top-level tools that we want the agent to always have access to, and then a search/execute pattern for anything else registered.

This doesn’t stop at tools though, as they’re only part of the equation for getting work done. Like other agents, we’ve also implemented a pattern of using skills for capabilities.

The Sentry skill, for example, tells Junior to:

- use live Sentry CLI queries for issues, logs, traces, orgs, projects, and API fallback
- resolve `sentry.org` and `sentry.project` from conversation config
- check `TELEMETRY.md` in a repo before forming product telemetry queries
- prefer `--json` for parseable output
- rerun real Sentry commands once when auth looks stale so the runtime can trigger reconnect
- avoid guessing missing scopes from a generic `403`
- never print token values

While Sentry is more of a broad capabilities skill, we find them particularly valuable as playbooks. For example, we have a `release-package` skill which teaches Junior how to execute the right GitHub workflows to do NPM releases for a handful of our packages.

## Not everything is Slack

Junior also has to react to things that aren’t Slack messages. The two primary concerns we look at, at the time of writing, are scheduled tasks and inbound events. I’m going to focus on the latter, as scheduled tasks aren’t anything special.

GitHub PR creation is the first concrete version of allowing the agent to respond to external events. We have implemented a resource subscription concept, which allows Junior to determine which events it cares about. The PR creation tool is a great example of this. When it creates a PR it also returns a note about the resource and then Junior can decide to opt in:

```ts
await subscribeToResourceEvents({
  provider: "github",
  resourceType: "pull_request",
  label: "GitHub PR getsentry/junior#691",
  resourceRef: "github:pull_request:getsentry/junior#691",
  events: ["checks.failed", "review.changes_requested", "state.merged"],
  intent:
    "Watch the PR Junior opened and update this thread when it needs attention.",
});
```

When GitHub webhooks arrive, Junior normalizes them into resource events: a failed check becomes `checks.failed`, a review approval becomes `review.approved`, a merged PR becomes `state.merged`. From there Junior matches active subscriptions and then creates a synthetic user message for the agent to act upon. We did make one change here in that unlike normal user messages, we queue this input rather than inject steering immediately after a tool result.

It’s up to Junior at that point to decide what to do. It might have knowledge in its memory that you don’t care about updates, it might have a skill that understands when checks fail it should perform a set of behaviors. Ultimately I think the model here is compelling, but I’ll admit we haven’t fully battle-tested this approach yet.

We have also yet to solve credentials around these kinds of tasks. We explicitly forbid credentials in the scheduler today - generally because we don’t want the agent accidentally doing something harmful, or more importantly someone injecting an intentionally harmful scheduled task that we might not notice. It still retains read access in some scenarios (like GitHub), but this is obviously something that’s important for us to solve.

## Junior has to debug itself

Debugging agents sucks. There are *so many failure modes* for distributed systems already, and LLMs compound this to such a degree that the way we’ve historically approached it isn’t enough. To work around this I mostly focus on having agents help debug agents, and in this case that means both Junior diagnosing its own failures and my coding harness having access to similar information.

As a simple example, if someone says “Junior fucked up,” I need to see:

- which conversation this was
- which run produced the answer
- what messages were in the model history
- which skill was loaded
- which MCP providers were active
- which tools were called
- what auth pause or resume happened
- whether Slack delivery failed
- which trace or error explains the behavior

Junior uses Sentry for this (obviously). The biggest change is getting comfortable with spans. We lean heavily on OpenTelemetry semantics here to work with Sentry’s agent tracing products, and on top of that we also teach Junior (and our coding agents) what to expect here. Unlike logs they’re typically not readily available, nor are they common practice to instrument, so a lot of effort needs to go into making these traces accessible to the agents locally as well as in production.

That said, a chat conversation isn’t always the easiest way to debug a complex problem. Sentry has a Conversations feature that makes these easier to consume. Initially I hit some rough edges on this so I quickly rolled a Junior-specific view (albeit, it’s much more limited), and that really helps me visually understand the flow of events.

![](https://cra.mr/assets/junior/junior-dashboard-conversation.png)

The same visual QA thread in Junior's dashboard: transcript, tool calls, timings, token counts, and a Sentry link in one place.

An important note here is we took a pretty clean stance on privacy. If the conversation happens in a private channel or a DM, we redact everything that’s not pure metadata. That means no inputs, no outputs, no tool arguments. If it’s in a public channel, we capture everything. We do this both in our internal APIs (visible in the dashboard), as well as the information we send to Sentry. I’m hoping we can find ways to improve Sentry’s SDKs here to make this kind of behavior easier, as it certainly isn’t today.

## Testing agents is awful

I’m so sick and tired of Codex writing unit tests. Unlimited unit tests literally testing nothing. Codex isn’t here to blame, everyone else is. Unit tests have always been garbage for most software, but the fact that agents require another service makes this even worse. There’s very little you can reliably unit test, and you really have to forcefully steer the system into focusing on something more akin to end-to-end tests (or really high-level integration) to capture behavior above all else. To be clear, I’m not talking about “is this prompt better or worse”, I’m just talking about “does it remotely work the way it’s supposed to work”. That means evals.

Junior uses [vitest-evals](https://vitest-evals.sentry.dev/) for this, which keeps evals close to the rest of the test suite instead of turning them into eval theater off to the side. The rubrics still have explicit pass and fail criteria:

```ts
await run({
  events: [
    threadMessage("Remember this: the budget deadline is Friday."),
    threadMessage(
      "<@U_APP> connect the demo account, then tell me the deadline.",
    ),
  ],
  criteria: rubric({
    pass: [
      "The same Slack thread gets a resumed answer after authorization completes.",
      "The resumed answer explicitly says the earlier budget deadline was Friday.",
    ],
    fail: [
      "Do not post the authorization URL in the public thread.",
      "Do not ask the user to repeat the deadline.",
      "Do not behave as if prior thread context was lost.",
    ],
  }),
});
```

While the above is focused on a judge rubric, this is just an assertion in vitest. That means we can also assert on side effects the same way we would normally in integration tests. The important thing is we’ve got a clean abstraction to run the agent, to inject the right kinds of event scenarios, and then we need to rely on traditional techniques. This is a change in how we develop software, and it makes integration tests more important than ever.

While TDD is a great pipe dream, think about how you practically build and iterate on software, and you’ll quickly recognize that you often manually QA changes before cementing most behavior. It’s useful to allow the agent to do that too, even if it’s only doing it after it’s generated 100 slop unit tests. Junior has a local client, `junior chat`, which, while not perfect, allows you to interact with a large chunk of the runtime without going through Slack.

We combine this with a `junior-qa` skill inside the repo, instructing the agent on how it should approach this kind of QA. You’d think this wouldn’t be that important, but despite my best efforts I’ve still been unable to fully encapsulate a large enough chunk of behavior in tests that this often flushes out bugs.

One last important note here: both `junior chat` and `vitest-evals` expose traces. This means the agent has access to the conversation to better enable self-debugging.

## Honestly, it all is awful

This is the most fun I’ve had building something in recent history, but it’s also routinely the most frustrating. It’s a large, complex system even if it seems like a simple agent. On top of that the behavior of LLMs means you’re constantly making a judgment call on if you should even try to solve something (since often things are steering concerns).

I’ll admit some of the pain is self-inflicted. Plugins started as YAML, because YAML feels like enough when a plugin is just a name and a list of domains. Then plugins kept absorbing responsibility (credentials, OAuth, runtime dependencies, MCP endpoints, hooks, routes, skills) and the YAML version fell apart. Then plugins became real packages, which made them more functional, but also increased complexity.

Much of this I just drastically underestimated. I didn’t consider the serverless limitations - although I’d probably make the same decisions even if I did. I adopted some libraries which were half-baked and I ended up having to patch around or ultimately rip out. I think a lot of this will improve over the next couple of years as we move on from vibe-coded solutions onto more mature and stable scaffolding for building agents.

Add it all up and you get roughly 100,000 lines of TypeScript and four months of work, and I have a feeling the pace of change is not going to slow down in the next four.

If you’re interested in exploring Junior, start with the [docs](https://junior.sentry.dev/) if you want to run it. Read the [source](https://github.com/getsentry/junior) if you want to argue with the implementation. Apologies in advance, as it certainly is still full of bugs.
