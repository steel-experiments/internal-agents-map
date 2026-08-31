> Archived source snapshot  
> Source ID: `hubspot-sidekick-source-2`  
> Original URL: <https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot>  
> Final URL: <https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot>  
> Title: Cloud Coding Agents at HubSpot  
> Captured at: `2026-08-31T17:43:18Z`

---

*This post is the second in a series about empowering product, UX, and engineering teams with AI, especially in the context of writing code. Read the first post about scaling AI adoption* [*here*](https://product.hubspot.com/blog/context-is-key-how-hubspot-scaled-ai-adoption)*!*

In our last post, we shared a small part of our journey towards universal AI adoption in our engineering organization and claimed that [AI has fundamentally transformed how we build software at HubSpot](https://product.hubspot.com/blog/context-is-key-how-hubspot-scaled-ai-adoption#:~:text=AI%20has%20fundamentally%20transformed%20how%20we%20build%20software%20at%20HubSpot). That’s a pretty bold statement!

We have had a lot of success rolling out local AI coding agents to our engineering teams, but the transformative nature of AI-enabled software development became most apparent to us when we began to deeply integrate it at all points in the software development process.

One example of this integration is our recent rollout of cloud coding agents for engineers, which have been live for planning, implementation, and code review at HubSpot for the past six months. To date, we have merged over 7,000 fully AI-generated pull requests and code reviewed over 50,000 pull requests authored by humans. We run all of the agents on our own infrastructure and tightly integrate them with GitHub, allowing HubSpot engineers to ship changes quickly and with more confidence than ever before.

In this blog post, we will explore the technical architecture of this system, discuss how we went from zero to MVP quickly with a small team, and share what we learned about getting good results from fully autonomous coding agents.

![Graph showing total cloud agent executions to date from 2025-07-01 to present](https://product.hubspot.com/hs-fs/hubfs/total-executions-to-date%20(1).png?width=1950&height=1554&name=total-executions-to-date%20(1).png)

*Total cloud agent executions to date \[sanitized data\]*

## Self-hosting a cloud execution platform for Claude Code

From our past experience deploying local coding agents, we knew that giving them a tight feedback loop would be key to their success. At HubSpot, this meant giving them access to our existing developer tooling and infrastructure in order to read build logs, run integration tests, and call internal services. We have an extremely consistent and opinionated internal stack, which gave us a clear vision for the capabilities our platform would need to provide to the coding agent. On the other hand, our heavy usage of internal tools and libraries would have also made replicating our developer environment with an external provider quite challenging. For this reason, we decided that building an internal platform for executing cloud coding agents would be the quickest way to begin showing results.

Luckily, HubSpot already has a strong culture of building internal infrastructure platforms from scratch – we already have an [internal build and deploy system](https://product.hubspot.com/blog/continuous-delivery) built on top of Kubernetes which runs over one million builds per day and hosts tens of thousands of microservices across approximately 3,000 EC2 instances. It was an easy choice for us to build our agent execution platform on top of Kubernetes as well.

Our platform, dubbed Crucible, consists of several components:

- **Frontend** - A simple internal site for displaying historical executions and viewing transcripts/logs.
- **API server** - Handles incoming requests to start new agent executions and retrieve the status and results of existing executions (generally a git diff of files changed by the agent).
- **Kubernetes Jobs** - Agent executions correspond 1:1 with a [Job resource](http://kubernetes.io/docs/concepts/workloads/controllers/job/) in Kubernetes. The API server manages creating Jobs on-demand and monitors them for completion.
- **Docker images** - We created custom Docker images with Claude Code and all of our other local developer tooling preinstalled. The image entrypoint handles cloning the Git repository targeted by the current execution and running Claude with the execution prompt.

This approach has several advantages: it guarantees that every agent is sandboxed, it’s extremely easy to scale, and it’s flexible enough to handle many different kinds of requests (for example, agents don’t have to make code changes – they could also be instructed to examine a branch and leave a pull request review using gh).

It was not without its challenges though. Here are just a few of the problems we had to solve:

- Replicating the HubSpot local development environment inside of a container was difficult. Our tools were generally built to run on laptops, not Kubernetes, so many tools required patches from us to work properly in a containerized environment.
- Builds (especially Java builds) were extremely slow! To solve this, we used learnings from our internal build infrastructure and began running agents on a dedicated Kubernetes node pool with a build cache mounted from the host. This reduced first build times for most repositories from 10-15 minutes to around 2-3 minutes.
- Not all code repositories are created equally. Hardware resources (especially memory) need to be tuned to appropriate values depending on the repository being worked on. This problem was made much simpler by our use of Kubernetes, which makes vertical scaling extremely easy.

![Graph of memory and CPU usage for Crucible pods](https://product.hubspot.com/hs-fs/hubfs/pod-metrics.png?width=1950&height=1446&name=pod-metrics.png)

*Variance in repository size leads to unpredictable resource usage between pods*

## Triggering cloud agents from GitHub and Slack

With a solid foundation, we could begin working on integrations for GitHub and Slack. We wanted to reduce friction for using our tools as much as possible, which meant meeting users where they are instead of directing them to a new internal platform.

Sidekick is an AI assistant we had previously created to help engineers in navigating our internal documentation. We decided to extend its functionality using several new Crucible-based tools via @-mention on GitHub or Slack:

- **Issue planning** - Just like when working with local coding agents, cloud agents benefit immensely from a detailed implementation plan with specific references to files which need to be modified. Users can easily trigger a planning step on a GitHub issue by directly mentioning our internal bot ("@SidekickAI create a plan"). The plan will then be posted as a comment on the issue, where it can be edited by the user before moving on to the implementation step.
- **Autonomous implementation** - Assigning Sidekick to an issue will trigger a cloud agent to autonomously implement the issue and create a pull request. The complete prompt is generated from a template and includes the issue details, guidance about committing and pushing changes, and instructions for communicating with the user (by either posting follow-up comments or editing the pull request body).
- **Pull request review** - AI pull request reviews are triggered automatically when pull requests are created, marked ready for review, or when Sidekick is manually requested as a reviewer. There is a lot to say about pull request reviews, so stay tuned for a future blog post on this topic!

![Screenshot of a GitHub issue where Sidekick is assigned and responds that it has started working on the issue](https://product.hubspot.com/hs-fs/hubfs/sidekick-github-framed.png?width=1950&height=1557&name=sidekick-github-framed.png)

*Assigning Sidekick to work on an issue*

## Autonomous coding agents

Of the above workflows, one which was especially challenging to get right was autonomous issue implementation. Agents would often decide they were finished despite a failing build, not communicate adequately with users, or even entirely forget that they were supposed to create a pull request!

Here’s what we learned along the way to making these agents produce reliable and consistent results:

1. **Non-deterministic code transformations go hand-in-hand with deterministic logic.** When thinking about the process of implementing a feature request, we asked ourselves: what are the steps that we can map to deterministic business logic? Where do we need LLM’s creativity? Over time, we shifted more and more logic to deterministic code paths. For example, when starting work on an issue, the first step will always be to create a new branch and a draft pull request. Rather than ask the agent to do this, we do it deterministically and then template the resulting branch and pull request number into the agent prompt.
2. **Agents can be tamed.** Claude Code (and other tools such as [OpenCode](https://opencode.ai/)) have support for hooks, which can be used to inject behavior at various points in the tool call lifecycle or before the agent stops. Use these features gratuitously to build a harness which enforces the behaviors you want. As an example, here are just a few of the hooks we use in our system:
	1. *Enforce clear and concise communication* - automatically block commit messages if they are too long
		2. *Ensure the agent follows our coding style* - automatically block edits if they appear to be doing something unconventional (for example, using fully qualified class names in Java). In case it is actually required for what the agent is doing, allow the same edit to succeed on the second try.
		3. *Ensure the agent completes its task* - block stopping until the build passes and all changes are committed and pushed to GitHub.
3. **UX is hard.** In our initial version of this workflow, we automatically marked the pull request as “ready for review” when it was completed, which as it turns out many teams did not like! We also had to solve a few other UX challenges, including how to select the correct Git repository to make changes in (solution: run a tiny agent to find the correct repository) and how to keep track of pull requests created by Sidekick on your behalf (solution: embed the engineer’s username in the pull request body and branch name).

![Screenshot of the Crucible frontend showing tabs for transcript, logs, prompt, diff, and container details](https://product.hubspot.com/hs-fs/hubfs/crucible-ui-framed.png?width=1950&height=1464&name=crucible-ui-framed.png)

*The Crucible frontend*

## How to ship good AI coding tools quickly

Our Engineering team at HubSpot loves working with Crucible and Sidekick. Most HubSpot engineers use them every day to accelerate their work. We believe our success comes down to a few factors:

- **Standing on the shoulders of giants** - When we began this project, we did not have the internal expertise to build a competitive coding agent from scratch. Instead, we used an existing platform, Claude Code, which we already knew worked well for our engineers. Throughout the project’s lifecycle, Claude’s coding performance continued to improve, a benefit we reaped for free while allowing us to keep focusing our attention on the surrounding infrastructure.
- **Building our own system** - HubSpot has a mature engineering organization where creating new microservices is extremely easy, including microservices which interact directly with low-level infrastructure like Kubernetes. This made building our own agent execution platform simpler than expected, and it allowed us to much more easily recreate our local development environment and sidestep authentication/network access concerns which would come with adopting an external product.
- **Flexibility** - Since launch, our internal customers have repurposed Crucible for all sorts of things, from mass code migrations to automatic AI fixes for failing builds. We are constantly experimenting with new use-cases and agents (we support more than just Claude Code!), which is all enabled by the general purpose nature of the system we designed.

## Looking ahead

We have lots planned for the future! Crucible has also served as the foundation for an internal evaluation framework for coding agents, and we are continuing to iterate on the UX for our existing workflows. [GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/assigning-and-completing-issues-with-coding-agent-in-github-copilot/) offers similar features and gets a lot right with its UX, especially with the way it is able to include small indications of progress in the timeline.

![Screenshot of GitHub Copilot, showing inline timeline indications of progress](https://product.hubspot.com/hs-fs/hubfs/github-copilot-example.png?width=2400&height=753&name=github-copilot-example.png)

*Timeline indicators for bot actions have a cleaner UX than comments*

One of the things we’re most excited for though is to experiment more with other coding agents besides Claude Code. Most recently, [OpenCode](https://opencode.ai/) has been very interesting due to its [robust plugin architecture](https://opencode.ai/docs/plugins/), but we also want to test a new kind of coding agent built entirely in-house using our internal agent framework. We’re hoping that this will offer us easier control over complex workflows like pull request review and autonomous implementation.

We look forward to sharing more about all of these things in future posts, but that just about wraps it up for today!

![Screenshot of blog author asking the Sidekick bot on Slack to post the blog. Unfortunately, Sidekick does not know how to do this yet.](https://product.hubspot.com/hs-fs/hubfs/sidekick-post-the-blog-fixed.png?width=2100&height=459&name=sidekick-post-the-blog-fixed.png)

Thanks for reading, and a special thank you to [Ze’ev Klapow](https://www.linkedin.com/in/ze-ev-klapow-19a81a3b/), [Francesco Signoretti](https://www.linkedin.com/in/signorettif/), [Brian LaMattina](https://www.linkedin.com/in/brian-l-577bb6114/), [David Camprubí](https://www.linkedin.com/in/davidcamprubi/), [Emily Adams](https://www.linkedin.com/in/emily-n-adamss/), and everyone else at HubSpot who helped with this project.

---

*Next: How we raised our quality bar for AI code reviews*
