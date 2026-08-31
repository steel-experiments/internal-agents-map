> Archived source snapshot  
> Source ID: `sierra-pinecone-source-3`  
> Original URL: <https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents>  
> Final URL: <https://sierra.ai/es/blog/agency-secure-scalable-sandboxes-for-agents>  
> Title: Agency: Secure, scalable sandboxes for agents | Sierra  
> Captured at: `2026-08-31T17:49:02Z`

---

*This is part of our series on how we're [AI-pilling Sierra](https://sierra.ai/blog/ai-pilling-our-company-lessons-learned).*

In our last few posts, we talked about what happens when every employee has a single AI agent called [Pinecone](https://sierra.ai/blog/pinecone-harnessing-the-wisdom-of-the-workforce): work gets done faster, institutional knowledge compounds, and the agent can safely interact with the company's systems to get the necessary context through the [MCP Gateway](https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg).

Before Pinecone, it wasn't unusual to see engineers walking around the office with half-open laptops — not because they were working, but because their AI agents were. Close the lid, and the agent stopped. Walk away for lunch, and you might come back to find it waiting for approval after making no progress for an hour.

This limitation, among other things, reinforced something we'd started to realize: the hardest part of building great agents wasn't the model anymore — it was everything around it. That’s where Agency comes in, the infrastructure that gives every Pinecone session and every task for [Ghostwriter](https://sierra.ai/product/ghostwriter) (our agent-building agent for customers) a secure place to live and run.

## Prototypical start: Environment matters most

Both Pinecone and Ghostwriter started life as prototypes: isolated sandboxes packed onto a single VM. They were built by engineers from different teams, each trying to solve similar problems for different audiences. The early success observed by both prototypes proved the hypothesis. The models are smart enough for sophisticated coding tasks: it’s the environment, the tooling and ability to verify its own work that surrounds the model that dictates the rate of progress.

Going back to the half-open laptops example: Running the agent with *\--allow-dangerously-skip-permissions or sandbox\_mode = “danger-full-access”* was not really an option. That would mean that the agent would run with the developer’s access token, which had write access to systems that were too dangerous to give to an agent, especially an unattended one.

To give both Pinecone and Ghostwriter safe autonomy, both prototypes had a concept of sandboxes: isolated environments in which we could control what the agents had access to. Then, we could run them in “full-access” mode. However, the prototypes were limited to running a few sandboxes concurrently before being resource constrained.

To truly unlock these products, we needed a new primitive, with sandboxes that were:

- **Secure** enough to handle customer data
- **Fast** enough to spin one up without losing your flow state
- **Cheap** enough that you never think twice about creating another
- **Reliable** enough to trust with long-running, sophisticated tasks without losing work
- **Powerful** enough to match the dev workflow on our laptops: 8+ cores, 24GiB ram, fast disk
- **Scalable** enough that we could dynamically provision capacity

## Why we built our own: The space was too undefined

There are solid off-the-shelf sandbox providers (though, there were fewer when we started). When the problem is well-understood and the pre-built solution trade-offs are known, that's a huge accelerant — why build your own blob store when S3 and GCS exist? Plus, mature infrastructure lets you focus on what differentiates your product.

But agent sandboxes weren't a mature problem yet. When the problem is not yet clearly defined, or it's not clear which trade-offs are right, you inherit someone else's assumptions and spend your time working around them instead of understanding your own problem. So we decided to build our own.

At the time, sandbox providers often had hard limits on the amount of resources you could assign per sandbox or strict limits on how much time a sandbox could live or how many we could have running at the same time. Those constraints would have become Pinecone's or Ghostwriter’s constraints. From a user's perspective, they'd feel arbitrary: *Why can't my agent run overnight? Why is my build slower than it is on my laptop?*

In the end, our goals for building were two-fold:

- **Ease of use:** We wanted users spending their time on high-leverage decisions — not on figuring out how to be productive in a different system with different limitations.
- **Pragmatism**: We didn’t need to add a third party vendor that handled customer data, which meant that we could get Ghostwriter in the hands of our most discerning customers, with stringent vendor approval standards, faster.

## The shape of the Agency … and how most agents spend their lives waiting

Agency is our agent sandbox orchestration layer. Named both for granting agents autonomy – the *agency* to do their task autonomously – and as the place where agents do their work, Agency is built as a native Kubernetes application that has two primary layers:

1. **A stateless control plane**, responsible for provisioning and managing runners
2. **A fleet of stateful runners**, where agents actually execute their work

![A flow chart outlining the agency architecture](https://sierra.ai/-/cdn/image?src=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fca4jck6w%2Fproduction%2F541fe9afc122f1b9c2e1171a19bca04cc638b903-5040x4992.png%3Frect%3D0%2C502%2C5040%2C4490&width=3840&quality=75)

A flow chart outlining the agency architecture

The stateless layer exposes APIs like *CreateRunnerInstance* and *DeleteRunnerInstance*, allowing applications built on top of Agency to provision runners on demand. It authenticates requests using IAM, manages runner templates and permissions, tracks runner state in DynamoDB, and translates each runner definition into a Kubernetes pod. The runners themselves are the execution environment: each receives dedicated compute, persistent storage for repositories and build artifacts, and everything needed to behave like a developer's workstation.

The stateful runner layer is where the agentic environment lives and is composed of all the on-demand pods created by the control plane. Each pod usually contains a Persistent Volume (backed by a cloud based block storage service) for the agent to check out repos, build code, etc.

### Safety as a requirement

We knew runners would eventually need to work with sensitive customer data while also producing and running untrusted code. That meant security couldn't be something we bolted on later, and it had to be part of the architecture itself. We also settled on the requirement that agents should not have any API keys or other secrets accessible to them by default, as it would be trivial for a jailbroken agent to exfiltrate them.

Solving for security requirements early on led to several architectural decisions, such as:

1. All inference in runners happens via an LLM proxy, running outside of the sandbox. This allows us to inject real api keys just in time and also do token accounting without cooperation or potential meddling by a compromised agent.
2. Each runner type got dedicated IAM roles so that we could strictly control permissions independently for different application types.
3. Within the runner pod, the agent runs inside a hardened container: it runs as a non-root user, drops all capabilities and permissions, has a read-only root file system, etc.
4. All internet traffic is routed through a filtering egress proxy so that we can tightly control which hosts the agent can reach.
5. The runner pods are scheduled on isolated Kubernetes Nodepools to limit exposure of unrelated workloads we run on our cluster.
6. All coordination with the control plane service carries the runner pod identity to prevent one runner instance from impersonating another instance, which could compromise data isolation guarantees.

### Most agents spend their time waiting

Although we figured we may end up creating a large number of runner instances, our intuition was that only a small fraction would actually be doing work at any given moment. This was mostly informed by the observation that unattended agents spent most of their time waiting for user input rather than streaming tokens and doing work. This turned out to be true. There is usually 2 to 4 orders of magnitude difference between the number of active runner instances within the last 8 hours compared to the last 8 days.

If we could dynamically (and transparently!) spin down idle agents and bring them back when needed, then we could support giving each runner more resources than otherwise possible on a relatively small pool of nodes. That observation led to one of Agency's core primitives: runner hibernation. In order to make runner hibernation transparent to applications like Pinecone and Ghostwriter, we needed to decouple communication between the runner and the application so that the runner is not directly reachable from the application. Instead, applications and runners communicate with each other by passing messages.

A runner instance can be modeled as a Finite State Machine. Applications enqueue messages addressed to a specific instance into its input queue and upon handling that message, the runner might change its state. At any time, if the runner wishes to communicate with the outside world, it does so by enqueuing a message to its output queue, which is then consumed by the application. In this way, neither the runner instance nor the application need to be in synchronous communication with each other in order to evolve the FSM state. By using an in-memory queue implementation, like Elasticache Redis Streams, and limiting the size of the events (a few hundred KiB) we can make the round trips fast enough (p50: 8ms, p99: 40ms) when both parties are online.

This leaves the problem of restoring the FSM’s state after hibernation. Because a runner instance is a singleton and only it enqueues anything to the output queue, the output queue can be strictly ordered and can be thought of as an append-only log. If the runner instance periodically emits checkpoint events, this ordered, append-only property can then be used to restore the runner instance state: replay the events from the output queue from the last checkpoint event onwards. It is the application specific runner’s responsibility to decide what goes in the checkpoint and delta events — they are opaque proto messages to the Agency control plane. After the event replay is complete, the runner can go back to consuming the input queue for regular operations.

To Pinecone and Ghostwriter, nothing changes. A runner simply wakes up and continues working. Underneath, Agency has reclaimed compute resources, restored the runner's state, and resumed execution without the application ever noticing.

## Lessons learned

There were several other challenges we tackled, and overall we came away with a few key lessons learned:

**Build composable primitives, not one-off solutions**. The same philosophy that led us to build MCP Gateway was applied again with Agency. Rather than building a platform specifically for Pinecone or Ghostwriter, we built a generic primitive for secure agent execution. That decision makes it easy to reuse Agency across multiple products, and new ones we haven't imagined yet. The degree of composability increases when each of the pieces themselves solve a single problem making minimal assumptions on how it is being used in the overall picture.

**Having control over your internal agentic stack pays off.** When you’re not beholden to a third-party vendor to remove a blocker, you can unlock productivity. For example, we were able to build “Ephemeral Sessions” in Pinecone in under a week. These sessions are the only ones in which customer data is allowed to be loaded and, therefore, has limits on data provenance, persistence, and visibility. Because we have control over the orchestration, agent sandboxing, MCP Gateway and the final UX, this was just another Pinecone feature that we built with Pinecone and rolled out rapidly.

**Strive for building boring software.** Software ought to be boring. It should empower its users to accomplish their goals while being simple to use and reliable to operate. Agency is one of the most boring services we run (in a good way!): it is the invisible layer that keeps our attention where it matters — at the Pinecone and Ghostwriter application layer where we have the highest impact potential with our users.

Building simple, boring software is notoriously hard — and downright fun!
