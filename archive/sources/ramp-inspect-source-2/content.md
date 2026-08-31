> Archived source snapshot  
> Source ID: `ramp-inspect-source-2`  
> Original URL: <https://linear.app/customers/ramp>  
> Final URL: <https://linear.app/customers/ramp>  
> Title: The coding agent behind 75% of Ramp’s merged PRs  
> Captured at: `2026-08-31T17:46:31Z`

---

Businesses shuttle many billions of dollars along the lines of code in Ramp’s codebase each year. Despite the stakes, in November 2025 Ramp made the call to hand most of its code to an agent it built in-house. That agent, called Inspect, now writes three of every four PRs Ramp merges. Its context includes six years of specs, customer requests, and roadmaps kept in Linear.

Ramp [ramp.com ↗](https://ramp.com/)

FoundedNew York, 2019

SwitchedOctober 2019

Company size1,600

### What Inspect is⁠

Inspect is a background coding agent that writes code and verifies its own output using the tools a Ramp engineer would reach for. Each session runs in a sandbox configured with Ramp’s own infrastructure, and anyone can start one from the web interface, a Chrome extension, or Slack, where a reply of “@Inspect, fix this” is often all it takes to open a PR.

Sessions are also shareable. A designer can take a dashboard rework most of the way there from a Figma file, then hand the session to an engineer to bring it live. Engineers end up reviewing work that is already close to done.

### Why Ramp built its own coding agent⁠

Inspect began as a casual idea between Zach Bruggeman and two colleagues, Jason Quense and Rahul Sengottuvelu, who built the first version in two weeks. Rather than adopt one of the many agents on the market, they wanted one shaped around Ramp’s internal workflows. “It’s a really tight integration with our development lifecycle and our tooling,” Zach says.

Building internally let them be exact about how the agent connects to everything else. They know the one API key it needs and precisely what the schema of their logs looks like, which made the agent faster to build and better at its job. A central team defines what agents can access and do, so functional teams can build their own automations safely on the same rails.

### How it works with Linear⁠

Ramp has run its entire product development process through Linear since 2019, which means Linear holds a structured record of everything behind the product. The specs teams write, the feedback customers send, the roadmaps they plan against, and how it all connects.

By integrating through Linear’s API for agents, the team gave Inspect native access to that whole layer. Combined with its reach into Ramp’s codebase and internal docs, the agent operates with something close to the full picture a well-informed engineer would have. Asked to fix a bug, it can trace the thread from a customer request through a product spec to the relevant code, rather than working from a narrow prompt.

Zach calls the connection a natural fit, and says building it was quick. He prompted a coding agent with [Linear’s docs](https://linear.app/developers/agent-interaction), added a couple of rough pointers, and it got the integration “90 percent of the way there in about 30 minutes.”

The speed has moved Ramp’s bottleneck from writing code to reviewing it, a constraint any company running agents at this scale will meet. Zach says he’s paying close attention to how companies like Linear are shaping what code review becomes next.

*Since our interview with the Ramp team, we launched [Diffs](https://linear.app/docs/diffs), which lets you review code changes directly in Linear.*
