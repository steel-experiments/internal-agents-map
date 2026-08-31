> Archived source snapshot  
> Source ID: `block-builderbot-source-2`  
> Original URL: <https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence>  
> Final URL: <https://engineering.block.xyz/blog/protecting-our-systems-with-intelligence>  
> Title: Protecting Our Systems with Intelligence | Block Engineering Blog  
> Captured at: `2026-08-31T17:39:58Z`

---

~/posts/protecting-our-systems-with-intelligence...

How we're using agentic reviewers as guardians to maintain system resilience

$ git blame

$ cat content.md

## Protectors, not assistants

We believe that a core requirement of protecting our [world model](https://block.xyz/inside/from-hierarchy-to-intelligence) is to use intelligence as more than simply an assistant that elevates options and waits for a human to take action. Instead, our agents function as vigilant guardians throughout research, planning, and implementation to ensure that our systems are resilient against the degenerative patterns that every engineering organization faces: individual teams shipping features that are locally rational and globally corrosive. As our first protector, Builderbot sits between our builders and the systems that we are building, constantly observing, learning, recommending, and steering changes to align with our world model.

## Key principles

### Shift left

Protection against the forces that erode systems must happen as early as possible in the software development lifecycle. This is a well established pattern in software development, but becomes even more critical as we focus on scaling our ability to ship features faster with intelligence. In most engineering organizations, CI has become the de facto validation layer — test suites are large, builds are complex, and it's often easier to let the build system figure it out than to verify everything locally. Agents change this equation. They can run the same checks locally before pushing, at a speed and consistency that wasn't practical before, if you give them a consistent entrypoint.

To accomplish this, we are implementing a single common CLI contract for local development in all of our repositories using [Just](https://github.com/casey/just). This enables our local agents to have a standardized entrypoint to all of the same tools that our CI runs. Now, instead of agents fumbling around when they encounter a new repository, they have a standard expectation to `just fmt` or `just test` via pre-commit and pre-push hooks before pushing code to a PR. This small change has massive impacts for our local agents' ability to make the right changes quickly and avoid shifting that burden to CI.

### A protector in every module

Each module needs the ability to define custom hooks, checks, and context that are considered when making changes to code within it. It's not sufficient to define one protector and expect it to work for every system, nor to expect a monorepo's rules to cover every module that lives within it. Hyperlocal context in concert with a global world model is a requirement for protectors to have sufficient context when steering changes to the system. Through trial and error, we have evolved our opinions about how to do this the right way over time. Many agentic reviewers are limited to a single prompt that's expected to cover an entire system, but we have seen much more success when leveraging progressive disclosure to guide agentic system reviews with the right context in the modules that they cover.

[AGENTS.md](http://agents.md/) provides one way to progressively disclose context in the modules where it's relevant. Most agents will automatically load an AGENTS.md file when they start working in a directory, and check for more local AGENTS.md context files as they navigate a system. We frequently include hints in our AGENTS.md files to let agents know external docs that they might want to review, or neighboring systems whose implementations need to stay in sync. By carefully crafting nested AGENTS.md files within a project, it's easy to steer an agent with the local context it needs in order to succeed.

### Context management is key

While AGENTS.md provides one tool for managing hyperlocal context, it's not sufficient on its own to capture our world model in a format accessible to our protectors. Some agentic reviewers offer methods to provide local context in modules by referencing it in AGENTS.md, but each token added to this context file creates a burden for every agent encountering the module. In order to get this context out of our critical paths, we really like Amp's [Code Review Checks](https://ampcode.com/manual#code-review) pattern, which enables us to move our prompts into `.agents/checks/*.md` files to only load the context when it's relevant. Just like AGENTS.md, checks are able to be nested inside individual modules using `**/.agents/checks/*.md`, and each prompt gets executed with its own dedicated review subagent to ensure the signal stays high.

[Agent Skills](https://agentskills.io/) provides another standard for pulling context out of the critical paths for our agents. Agent Skills is a highly extensible format for exposing context to agents and allowing them to dynamically equip themselves with it when it becomes relevant to a given task. Through an internal Skills Marketplace, we leverage hundreds of internally-written Agent Skills to seed each of our environments with context that makes it easy for stateless agents to quickly glean the information they need about our world model to proactively steer decisions during research, planning, and implementation.

## How to build a protector

A protector is fundamentally different from an assistant or an advisor. An assistant waits to be asked. An advisor presents options and steps back. A protector acts — continuously, mostly below the threshold of awareness. The closest analogy is your immune system: it doesn't wait for you to notice you're sick, it doesn't present a dashboard of threats and ask you to choose a response. It acts with enormous sophistication, and you only notice it when it fails.

Builderbot's code review system is a protector for our system architecture. No single engineer can hold the full system in their head anymore, but a protector can. It evaluates every proposed change against a model of the whole — not just the module being touched, but the architectural patterns, security requirements, and operational constraints that span the entire organization. Its default is action, not recommendation. It doesn't file a report and wait; it reviews, flags, and steers, with humans providing the final stamp of approval rather than the initial analysis.

### A single entrypoint

In order to catch issues as early as possible, local agents should have access to all of the same context, tools, and policies as our agents that run in the cloud. To enable this, we distribute a `sq agents review` CLI tool to every workstation and cloud agent runner that has the full context of local and global knowledge. Having a single entrypoint that we use to protect our systems everywhere makes it easy to evolve policies over time. When running against a PR, `sq agents review` can ensure that alignment with our world model has been verified before requesting humans to take a pass and grant final approval.

### Specialized reviews with access to global knowledge

With Code Review Checks, we equip module owners with the ability to define hyperlocal review context that gets dispatched in subagents during an execution of `sq agents review`. Each check runs as an isolated subagent with its own context window — a global check for API standards loads different context than a module-level check for PCI compliance in `payments/` or security review in `auth/`. These subagents run in parallel, and their findings are aggregated into a single review report.

![Parallel code review checks](https://images.ctfassets.net/1wryd5vd9xez/7JN93zMTHYNoxzkUihfHRr/bc5b935e38be5bbefff56f46140fea03/parallel-checks.png)

In addition to local checks, we have a constantly evolving set of global checks that get pulled in at review time to verify that new code is adhering to our global world model, allowing us to catch issues from afar and steer agentic changes by codifying global concerns. Finally, because our agentic reviews run on our own hardware, we're able to reference internal documents and sources during review time that may not otherwise be exposed to a third-party reviewer.

### Continuously evolving policies

Proactive protection shouldn't require humans to be constantly keeping checks in sync with our evolving product direction. We give our protectors a heartbeat to proactively review incidents, announcements, and messages to consider which deterministic and non-deterministic checks to propose for human review. These may be proposed locally within a particular module or repository that has a recurring set of consistent issues, or they can be added globally to steer entire systems toward a new evolution of our world model.

## Velocity with confidence

By building agents that proactively protect our systems, we are equipping our builders with the tools they need to build with confidence that they are moving in step with the broader organization. Shifting checks to run pre-push makes it faster to catch issues and reduces the burden on human reviewers who give the final stamp of approval. By giving tools for managing review context within individual modules, we make it easy for service stewards to have a high degree of ownership over the code they are shepherding. Through global checks, we can distribute our world model broadly to our agents, making it easier than ever to protect our systems while moving quickly.

$cat tags

$
