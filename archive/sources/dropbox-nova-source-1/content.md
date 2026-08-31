> Archived source snapshot  
> Source ID: `dropbox-nova-source-1`  
> Original URL: <https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents>  
> Final URL: <https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents>  
> Title: Introducing Nova, our internal platform for coding agents - Dropbox  
> Captured at: `2026-08-31T17:42:18Z`

---

Coding agents are becoming an important part of software development. Their most obvious use is helping developers write code faster. But code is only one part of building and operating software. At Dropbox scale, agents also need to work within a [large monorepo](https://dropbox.tech/infrastructure/reducing-our-monorepo-size-to-improve-developer-velocity), validate code changes in Dropbox’s full engineering environment, and [incorporate context](https://dropbox.tech/machine-learning/how-dash-uses-context-engineering-for-smarter-ai) from across the engineering lifecycle. Developers don’t just write code, after all—our engineers manage migrations, unblock CI, investigate failures, and handle repetitive operational work. This work matters, but it is often repetitive and disruptive, pulling engineers’ focus away from deeper product and infrastructure work.

To prepare for a future where agents can assist engineers with a larger share of their work, we built Nova, an internal service for running coding agents in our cloud. Nova lets engineers run multiple coding sessions in parallel and lets internal systems use AI agents as part of automated workflows. This platform approach lets us apply agents across internal workflows instead of building one-off implementations for each use case, making it easier to rapidly experiment with how AI can support engineering work.

In this post, we’ll share why we built Nova, why we chose a platform approach instead of multiple single-purpose solutions, and what we’ve learned from using it across the software development lifecycle.

## Tackling the fragmented workflow problem

The software development lifecycle has many places where engineering judgment matters, but the work itself can be repetitive and time-consuming. Debugging failures, updating dependencies, improving test coverage, and fixing flaky tests are critical to software development. At the same time, these tasks can distract from more meaningful work. Many of these workflows are also well suited for AI assistance through coding agents, though they do not all require the same kind of interaction. Some tasks work best through standard interactive chat, while others can run autonomously in async workflows and only surface results when an agent makes a useful discovery. Supporting both modes consistently requires more than a single-purpose tool.

At Dropbox scale, the development environment creates requirements that off-the-shelf tools are not designed to support. Our [large monorepo](https://dropbox.tech/infrastructure/reducing-our-monorepo-size-to-improve-developer-velocity) depends on [Bazel](https://dropbox.tech/infrastructure/continuous-integration-and-deployment-with-bazel) —a build and test tool that uses caching and remote execution—along with on-premise infrastructure to keep builds and tests fast. Third-party coding agent tools work well for local iteration, but they do not naturally fit a setup that depends on our repository shape, infrastructure, and validation paths. Because our development workflow depends on Dropbox-specific infrastructure and validation paths, we wanted coding agents to operate within those systems rather than introducing a separate AI-specific workflow.

Those requirements pushed us toward building a platform instead of separate solutions for each workflow. The goal was a shared system that could support interactive development, background jobs, and internal services while keeping execution, validation, and context handling consistent. To support those workflows, we built Nova.

## Improving development with Nova

Nova began with a focused problem: helping engineers respond to continuous integration failures with suggested fixes. That starting point was essential to shaping the platform. Each Nova session runs in an isolated environment with a snapshot of the Dropbox codebase from a specific commit. The caller provides the task and can optionally include validation commands to run after the agent finishes. If validation fails, for example because a test does not pass or a build breaks, Nova can continue the session, feed the results back to the agent, and ask it to address the failure. This keeps the agent grounded in the real build and test environment instead of stopping after generating a plausible-looking patch. The workflow follows a simple pattern: propose a change, validate it, and continue only if the results hold up.

Over time, we expanded the platform to support multiple coding agents behind the same interface. Nova integrates into the tools and workflows engineers already use, including a web interface for interactive sessions similar to other cloud-based coding agents. Engineers can also use a command-line interface and API to launch jobs in parallel from locally running agents, scripts, and internal services. To support longer-running workflows, we maintain helpers that make it easier to add AI-powered steps without rebuilding the surrounding infrastructure. Nova also includes tools for prompt evaluation, observability, and feedback collection so engineers can better understand how well agents perform.

As we expanded Nova into more engineering workflows, we found that many tasks required more than editing files. Agents often need to gather evidence, read logs, inspect failures, and carry context across multiple steps. To support that work, Nova includes skills, plugins, and MCP integrations, including access to observability systems.

Expanding beyond interactive coding sessions also shaped how we handled code publication. We chose to keep publication outside the agent and limit each session to a single branch, giving us a predictable view of which branches are active and which changes are being published. Allowing agents to create and manage multiple branches within a session would add significant complexity, including deciding which branch future work should build from. Keeping the workflow deterministic also makes it easier to automate tasks around each branch, such as running tests or rebasing onto the main branch.

```json
{
  "repo_commit": "<commit-sha>",
  "task": "Investigate this CI failure and propose a fix",
  "validation_commands": [
    "bazel test //path/to:test_target",
    "bazel test //path/to/related:all"
  ],
  "continue_on_validation_failure": true,
  "max_iterations": 5,
  "push_branch": "ai/nova/ci-fix"
}
```

Illustrative Nova request. Pseudo-code JSON.

## How we’re using the platform

Since launching Nova, we’ve applied it across a range of engineering workflows, from quick developer-driven coding sessions to long-running remediation and migration efforts. The following use cases show how AI coding agents can fit into both interactive day-to-day development and more durable operational workflows.

**Developer-driven sessions  
**Nova supports the kinds of developer-driven workflows engineers expect from modern coding agents. Engineers use Nova’s web UI to make quick fixes or build prototypes without interrupting their local development loop. For code changes, we use Bazel selectivity tools with Nova’s validation commands so changes are validated against the right compile and test targets. Engineers can also start from a Slack thread and carry that thread context into a Nova session, which reduces setup and preserves discussion that would otherwise need to be rewritten by hand.

**Flaky test remediation  
**One of Nova’s most successful operational workflows has been flaky test remediation. We built an internal tool called Deflaker, a durable workflow that integrates with [Athena, our flaky test detection system](https://dropbox.tech/infrastructure/athena-our-automated-build-health-management-system). Deflaker starts by finding examples of a test both passing and failing. It then sends those logs to Nova as context and asks the agent to identify a likely root cause and propose a fix. We validate the proposed change by running the test 100 or more times in CI, depending on the test failure rate. If the test flakes again, we take the new logs, carry forward notes from the previous attempt, and start another fix attempt. The fix-and-validate loop continues until the workflow lands a working fix or reaches a capped number of attempts (currently five).

![](https://dropbox.tech/cms/content/dam/dropbox/tech-blog/en-us/2026/may/nova/social-and-diagrams/Diagram%201%20(3).png/_jcr_content/renditions/Diagram%201%20(3).webp)

Athena detects a flaky test. Passing and failing logs are sent to Nova. Nova proposes a fix. CI runs more than 100 validation attempts. Success lands the fix, while failure starts another attempt with new logs and notes from the prior session.

**Migrations and dependency upgrades  
**Migrations and dependency upgrades became another natural fit for the platform. Before Nova, we used a bespoke Goose-based AI migrator integrated with our internal migration tracking tool. The system generated parallel AI coding jobs using prompt templates and verification commands, then published the results to GitHub branches. It was used across thousands of migration entries, including conversions from Enzyme tests to React Testing Library and updates to mypy type configuration.

Although the migrator was effective, it had important limitations. There was no interactivity for reviewing or continuing agent output, so failures often left teams with no practical way to recover the work. We also learned that highly repeatable migration work was often better handled directly by migration owners, who could launch and manage dozens of agents with the same runbook rather than coordinating delegated work across teams.

Moving migration workflows onto Nova gave us interactive coding sessions, shared guardrails, reusable workflow tooling, and a consistent operating model. Over time, we want migration owners to be able to write a prompt once, run it in parallel across many parts of the codebase, and review the resulting changes as part of a coordinated rollout. We now also integrate Nova with [RenovateBot](https://github.com/renovatebot/renovate) so agents can take a first pass at repairing breakages introduced by dependency upgrades.

**Emerging workflows and experiments  
**We use Nova to respond to production crash alerts by recreating crash states with tests, generating candidate fixes, and routing the results to service teams. Some of the most promising experiments build on these operational workflows and extend beyond code authoring itself. We’re exploring whether agents can help determine when a code change needs review from secondary teams by evaluating pull requests against team review policies and producing guidance on whether additional review is needed.

Beyond pull request workflows, we’re testing whether scheduled workflows can reduce recurring on-call toil, such as alert flapping or follow-ups buried in Slack channels. Another experiment uses multiple agents to review the same code change from different perspectives, then aggregates the results to deduplicate and filter low-value comments.

## What we learned

One lesson we learned is that the value of coding agents comes as much from the surrounding platform as from code generation itself. Running agents as a service gives us a reusable way to support a wide range of engineering workflows. We also found that context, validation, and guardrails reinforce one another. Localized AGENTS.md files give agents service-specific context, while validation commands, isolated execution, hermetic tests, Bazel caching, and retry loops let them operate against the same systems engineers rely on every day. Each layer improves reliability on its own, but together they make background workflows more trustworthy.

Another important lesson is that not every step belongs inside the agent loop. As we expanded Nova across the software development lifecycle, we had to decide where agentic behavior was useful and where deterministic systems should remain in control. For example, letting an agent manage its own test execution and iteration could leave sessions waiting on CI for hours or result in changes being validated against the wrong tests. We found it worked better for surrounding workflows to trigger CI deterministically and bring the agent back if there was a failure to inspect or fix.

As coding agents continue to improve, we expect them to take on a larger share of repetitive work across the software development lifecycle. The path forward is not just better models, but better integration with the systems that shape engineering work. Nova gives us a shared execution layer for AI-assisted workflows through isolated environments, repository-aware context, validation loops, workflow integration, and reviewable outputs. As we continue expanding context sources, including through Dash and MCP-based integrations, we expect agents to become more useful, more reliable, and better aligned with how engineering gets done at Dropbox.

*Acknowledgments: Samm Desmond, Daniel Avramson, Adam Ziel, and Chris Hodges*

~ ~ ~

*If building innovative products, experiences, and infrastructure excites you, come build the future with us! Visit* [*jobs.dropbox.com*](https://jobs.dropbox.com/) *to see our open roles.*

---

// Copy link  

Link copied
