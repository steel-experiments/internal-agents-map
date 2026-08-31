> Archived source snapshot  
> Source ID: `doordash-flux-source-3`  
> Original URL: <https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/>  
> Final URL: <https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/>  
> Title: Delegating Engineering Work To Cloud-Based Agents - DoorDash  
> Captured at: `2026-08-31T18:09:17Z`

---

Flux is DoorDash’s cloud-based agents platform for engineers. In a single month in 2026, we used Flux to automate 130,000 engineering tasks. Rapidly expanding after Q1 2026 debut, Flux already powers high-volume background workflows across DoorDash, including more than 25,000 automated code reviews each week, and more than 300 unique playbooks and 10,000-plus invocations used every week. These workflows can run unattended, in parallel, around the clock.

In this blog post, we'll walk through the limitations that pushed us beyond local, laptop-based agent workloads, why we chose to build Flux in-house rather than rely solely on hosted coding agents, and the platform primitives such as agent sandboxes, MCP gateway, playbooks, and invocation surfaces to make agent delegation repeatable and secure.

**Flux background workflow use-cases**

![](https://careersatdoordash.com/wp-content/uploads/2026/08/image-7.png)

Table 1: A snapshot of Flux usage across DoorDash in a single month, spanning automated code reviews, playbook runs, and background task completions

## Where we started

Over the past year, users running agentic workloads on their laptops have quickly hit limitations:

- *Resources and availability*. A laptop has a fixed number of CPU cores, limited memory, and a battery, all shared with every application on board. Agentic workflows often need to run compute-intensive tasks such as builds, tests, and large searches in parallel, causing laptops to run out of capacity fast. The workflows also depend on the device being powered on, connected, and available; work pauses when an engineer closes the laptop, loses connectivity, or steps away.
- *Safety controls*. Laptops typically have broad access to sensitive credentials and systems, including SSH keys, VPN sessions, and authenticated tools. Giving an autonomous agent that same level of access creates unnecessary risk and a potentially large blast radius. Local environments also make it harder to tightly scope what an agent can access and for how long.
- *Visibility and auditability*. When workloads run across individual laptops, execution is fragmented and difficult to monitor. It becomes harder to understand what is running, where it is running, on whose behalf, and which systems or files it has touched.

Our thesis to address these issues is simple:

Delegate tasks to secure**,** autonomous coding agents so engineers can dedicate more energy to innovation, critical thinking, and solving complex problems.

## Why we built Flux in-house

Hosted coding agents are useful, but they force a hard tradeoff: Either send sensitive code and execution context to a third party, or open a path from that third party back into internal systems. For DoorDash, the harder problem was not just getting an agent to write code; that’s mostly solved. It was giving that agent the right environment, tools, permissions, integrations, and constraints.

Our strategy is to control the primitives around the agent, including orchestration, sandboxes, workflows, permissions, integrations, and the DoorDash-specific context agents needed to work effectively. We also designed those primitives to be modular, giving us the flexibility to use the best third-party tool for each job or to build in-house when deeper security, integration, performance, or UX ownership matters.

These primitives democratize workflow creation and make systems more adaptable to future use cases. Because they can be composed in different ways, teams can build new agent workflows without reworking the underlying infrastructure or prescribing how each engineer should structure their workflow. For example, we run both the [evals](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) for our [code review](https://careersatdoordash.com/blog/how-we-learned-to-trust-our-ai-code-reviewer-at-doordash/) on Flux infrastructure.

## Primitives, not workflows

As shown in Figure 1, Flux is built around four platform primitives: sandboxes, the model context protocol (MCP) gateway, playbooks, and invocation surfaces. Together, they make agent delegation repeatable. A playbook defines the work. A cloud sandbox gives the agent a real place to do it. An agent gateway controls what systems the agent can access. And invocation surfaces allow engineers to start and receive work from the places they already use.

![](https://careersatdoordash.com/wp-content/uploads/2026/08/image-8.png)

Figure 1: The four platform primitives that make up Flux — sandboxes, the MCP gateway, playbooks, and invocation surfaces — and how they connect to turn a task into work an agent can safely carry out

## Sandboxes provide the execution environment

Local agents work well for interactive development, but they are a poor fit for unattended workflows. They depend on individual engineers’ laptops, compete for local resources, are difficult to audit, and do not scale efficiently across parallel tasks.

Flux moves execution into isolated cloud sandboxes backed by Firecracker micro virtual machines (microVMs) for hardware-level isolation. Each sandbox is provisioned with the repositories, developer tools, secrets, and runtime dependencies the task requires, giving agents a complete engineering workspace while providing DoorDash with a consistent execution, security, and observability model.

Controlling this layer lets us support real engineering workflows, including changes across multiple repositories and multiple pull requests from a single session. Flux has a 95th percentile service level objective of under five seconds for the full end-to-end setup — from starting the microVM to cloning the required repositories, installing build tools, and configuring the supported coding agent harnesses.

## MCP gateway provides governed access

Agents need access to the systems that engineers use every day, including continuous integration (CI), observability platforms, issue trackers, deployment tools, code search, documentation, and service metadata. But granting broad, unrestricted access should not be the default.

Flux connects agents to internal systems through an in-house MCP gateway called Agent Gateway. Each playbook declares the tools it requires, and Flux grants only the scoped permissions needed for that task. Every action is logged, creating a clear audit trail.

This gateway architecture gives us a centralized control point for authentication, authorization, observability, usage tracking, and policy enforcement, all of which make agent access both safer and easier to operate at scale.

## Playbooks define the work

A playbook is a reusable unit of agentic work — the equivalent of a Docker container for skills and agent-driven tasks on the Flux platform. Defined in a single markup YAML file, it packages the task, inputs, context, skills, tools, permissions, validation, expected outputs, and safety boundaries needed to execute work consistently.

Playbooks can combine agentic steps, which provide flexibility and judgment, with deterministic steps, which offer predictability, lower cost, and easier validation. This lets teams move logic between agent-driven execution and conventional code as requirements evolve, without redesigning the workflow.

## Invocation surfaces meet developers where they are

The same playbook can be triggered from Slack, GitHub, cron, the CLI, or a conversational skill. That means teams can define a workflow once and invoke it from whichever surface best matches the moment:

- Slack for collaborative delegation
- GitHub for PR and CI automation
- Cron for recurring maintenance
- CLI for direct developer control, or invoked through a skill

This is what makes Flux easy to adopt.

## Lessons learned

Building Flux taught us as much about product adoption as it did infrastructure, including:

- *Start narrow to earn trust.* We began with automated code review instead of trying to automate the entire software development life cycle. Code review was frequent, measurable, and easy for engineers to evaluate. It gave us a production workflow where we could tune quality, latency, cost, and behavior before expanding into CI triage, on-call tasks, maintenance playbooks, and ticket-driven development.
- *Make the work visible.* Our first Slack integration created private channels for each agent run. That made Flux useful for individuals, but it did not create team habits. Moving work into public threads changed the adoption pattern. Engineers could see what others delegated, watch Flux make progress, review the output, and build trust together.
- *Playbooks need enablement.* Reusable workflows do not appear just because the platform exists. Workshops and hackathons helped teams translate repeated operational work into playbooks. The primitives made automation possible; enablement helped teams recognize which workflows were worth encoding.

## What’s next

In future posts, we will go deeper into the platform primitives that make Flux work, and the developer experience for building new workflows. We’ll also discuss the applications we've built on top, including Flux Responder, our internal Slack agent.

## Acknowledgements

Thanks to Adam Rogal, Adam Yarger, Andy Fang, Ashwin Kachhara, Fan Xia, Ivan Rudovol, Jason Prasad, Jialu Deng, Justin Block, Justin Deocampo, Justin Fan, Keith Lyall, Praneet Singh, Sean Chen, Tyler Berrett, and Volanda Zhu for their contributions to the platform and this post.
