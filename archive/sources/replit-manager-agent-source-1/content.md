> Archived source snapshot  
> Source ID: `replit-manager-agent-source-1`  
> Original URL: <https://ld.replit.com/blog/self-driving-company>  
> Final URL: <https://ld.replit.com/blog/self-driving-company>  
> Title: The Self-Driving Company | Replit  
> Captured at: `2026-08-31T17:55:49Z`

---

In the past six months, engineers at Replit have nearly tripled code output. Review times held steady. Reversions and product incidents have stayed flat. Quality metrics improved, and releases have accelerated. All the typical trade-offs you might expect have not occurred.

While the code is the visible part, what's happening under the surface is much more interesting.

Agents now investigate production incidents, review pull requests, answer questions, analyze business data, triage support tickets, research sales accounts, and improve the systems that power Replit Agent itself.

It feels like a single master intelligence threaded through every employee, even though it is not. It is an expanding system of agents operating across the company: taking goals from people, gathering context, performing work, checking the results, and escalating when human judgment is needed.

We think this represents the beginning of a new kind of organization: the self-driving company.

A self-driving company is not one without people. People still choose the destination. They decide which problems matter, make difficult tradeoffs, exercise taste, and take responsibility for the outcome.

But increasingly, they do not perform every step required to get there.

The shift began late last year. Like many people working in AI, we returned from the Christmas break feeling that something fundamental had changed. Models could sustain work over much longer horizons.

Tasks that had repeatedly failed, like alert triage and root-cause investigation, began working. AI started solving some of our most stubborn bugs. So we stopped treating agents as tools that lived inside an editor or chat window. We wove them, carefully, into the fabric of the company itself.

Once engineering proved the value, adoption took on a life of its own. Team after team started offloading their most tedious work, reclaiming time for the strategic and creative thinking that actually moves the business. People don't feel like they've been automated. They feel like they've been promoted.

This is the story of how AI has completely changed the way we work at Replit.

### Engineering saw the impact first

In late January we turned up infrastructure to experiment with internal agent use cases quickly. We leveraged our agent harness, microVMs, and remote filesystem infrastructure so any engineer could orchestrate swarms of agents in parallel. Then we locked the whole thing behind access policies, token proxies, audit logging, and our ZeroTrust network. At that point we felt safe giving the agent access to all the things we use to get our jobs done: GitHub, GCP, Azure, Linear, Notion, Slack, ZenDesk, and more.

With context across systems, we saw a leap forward in productivity. Experiments that previously failed became easy. The most immediate impact was in coding stats.

We were in the sprint week leading up to Agent 4 release in March, where we typically see a big spike. Meetings disappear, scope is known, and engineering shifts into pure execution mode (often for up to 16 hours per day). But this time was different. Our productivity curve bent upward in a way none of us had seen before, which can be traced to the adoption of our new internal agentic system. From early January to late June, there was a 5.8X increase in the lines of code contributed.

![new agent output eclipse the existing agent](https://cdnimg.replit.com/images/bj34pdbp/migration/a0a0f0cf99a2e019a404de4aaef772b11c8e8647-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

new agent output eclipse the existing agent

Part of this increase can be attributed to hiring well. Our new agent accelerates time to productivity, which is great, but we can remove the hiring effect for cleaner data. Keeping a consistent cohort of authors, we see 2.9x as much code as before. Traditionally, it’s considered excellent if you keep output per engineer flat as you scale a team. We just tripled per engineer rate while doubling the team.

![engineers shipping more](https://cdnimg.replit.com/images/bj34pdbp/migration/adba7fb2a4112480fac34f19836f6c3b15cf9cfe-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

engineers shipping more

You might wonder who is reviewing all this new code and whether we’ve created a new bottleneck in the review process. Our code review latency is flat, largely because we put our agent to work in reviewing code. It’s now able to assess risk levels and only call in a second human reviewer when necessary. That means 30% (and growing) of human PR review time has been saved.

![more PRs agentically approved](https://cdnimg.replit.com/images/bj34pdbp/migration/94e7ffd4aa29e2248ae0bfd30dd76534b72a6e11-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

more PRs agentically approved

With our agent writing and reviewing more code, we should be worried about quality. If we look at PR reversion rates (left) and incidents opened, trends are flat. This means we’re actually improving on a relative basis.

![revert rate doing better](https://cdnimg.replit.com/images/bj34pdbp/migration/043985444d77a6534e9e194054daf8491380b415-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

revert rate doing better

One reason is that these processes are also agent assisted. Human code reviews have the benefit of an agentic co-reviewer, so more bugs get caught. Incident investigations (meaningful bugs or actual incidents) are assisted by an agent that attempts to find the root cause, so mean time to mitigation (MTTM) is going down.

![incidents steady, faster migrations](https://cdnimg.replit.com/images/bj34pdbp/migration/bd5deb41cf7d2e412f02ee0117cce5abbb6b0f0b-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

incidents steady, faster migrations

The final test is whether additional code inputs represent real value output. At the end of the day, engineering is delivering features for users. We track projects in Linear so that sales and marketing teams know when to communicate with users about new features. You can see the rate of project completion is sharply up along with our coding volume.

![engineering output tripled](https://cdnimg.replit.com/images/bj34pdbp/migration/63762457d0ffe07ee40e50a9d546c906b5f708ac-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

engineering output tripled

A self-driving engineering team can ship more, while raising quality at the same time.

### Our agent of agents is enabling loop engineering at scale

Zooming in gives us an idea of what this looks like. When engineers find ways to generate loops, sending a fleet of agents off to complete a verifiable task, we see the most dramatic change. Every employee gets access to a manager agent that can spawn multiple agents, enabling orchestration of agents working in loops on your behalf. Loops resulted in some very unique looking PR graphs, like these:

![more output per engineer](https://cdnimg.replit.com/images/bj34pdbp/migration/9fd38e7d9a67e09667edb500730e950b1fdcad2f-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

more output per engineer

One Engineer completed a long stalled migration of our CSS system and shared his learnings. Another engineer automated a migration that enabled us to localize the product. Yet another automated flaky test maintenance. Our CTO finally cracked one of our hardest networking bugs related to PSC and fd shutdown with a swarm of agents. All of our assumptions about what is possible have changed.

![no more emotion css](https://cdnimg.replit.com/images/bj34pdbp/migration/6c73c1461eff175766309ee743674bdd324c5cf4-1027x578.png?w=3840&q=80&fit=max&auto=format)

no more emotion css

![map codebase](https://cdnimg.replit.com/images/bj34pdbp/migration/1d6951cc633fe5e155e87dc7e91ec404a2873964-1029x581.png?w=3840&q=80&fit=max&auto=format)

map codebase

The most exciting self-driving example comes from our AI team. They built a [continual learning system](https://x.com/pirroh/status/2074118901143679414) that analyzes user feedback, proposes improvements, and uses a combination of benchmarks and A/B tests to validate the wins. Replit Agent is self improving!

![self-improving Agent](https://cdnimg.replit.com/images/bj34pdbp/migration/791e06c0a90c91ef33dac7cb5c914dc08a8e119c-1200x630.jpg?w=3840&q=80&fit=max&auto=format)

self-improving Agent

### The build vs. buy conversation has changed

Our new internal agent also changed conversations about whether we build or buy software. We regularly try out new AI tooling. Buying solutions can help us go faster, and we also assess the market constantly. But the more we build, the less of this we will need to do. Our internal agent now outperforms products we test that are seen as market leading. We just churned a seven-figure SaaS solution because our internal app, built entirely in Replit, was superior and employees had migrated over.

All of a sudden, tools feel like they are built for us. The deep integration with our knowledge bases, and customization we’ve done, makes other solutions feel inferior.

What surprised us more was that our internal agent also beat out vertical specific products we evaluated. A tool to help engineers triage alerts and root cause incidents came back with similar quality but at 10x the cost of running it on our agent. A tool that runs automated penetration testing found fewer vulnerabilities than our internal version at 10x higher cost. Both our versions were put into production with ease, reducing MTTM in incidents and hardening critical systems against attacks.

![sev2 example](https://cdnimg.replit.com/images/bj34pdbp/migration/77d744e127a4d23cd5c79e1767c1321fa97e75af-1750x1202.png?w=3840&q=80&fit=max&auto=format)

sev2 example

![pr open 4](https://cdnimg.replit.com/images/bj34pdbp/migration/cf43df8476566abbb5cd1c2a0cc330f8bd3aa4b9-1474x1646.png?w=3840&q=80&fit=max&auto=format)

With how much we’re still learning, and how models are improving, it’s clear this is only the beginning.

### Beyond engineering and into the whole business

A self-driving company doesn’t stop at Engineering. Every function at Replit is changing.

Usage spread quickly out of Engineering, mostly because of a Slack interface. The rest of the company noticed engineers tagging our agent with tasks and tried it for themselves. Initially, the most popular use case was asking questions. By combining our knowledge base with the state of the code base, anybody could clarify product expectations without waiting for engineering input. Those employees could then fix copy or documentation as a follow up. It was an immediate boost in being able to respond to users faster.

![andrew example](https://cdnimg.replit.com/images/bj34pdbp/migration/fbcb96ea1d1b5ad85033fe72534e6c07deccf169-1390x440.png?w=3840&q=80&fit=max&auto=format)

andrew example

![ethan example](https://cdnimg.replit.com/images/bj34pdbp/migration/f8f70241a48c10c18a4173f36a7b4e552d0baf79-1392x456.png?w=3840&q=80&fit=max&auto=format)

ethan example

But that was just the beginning. From there, contributions of new skills and integrations started to come in from all parts of the company.

The first big unlock came from our data team. They gave the agent a semantic layer over our data warehouse, so it knows which tables are sources of truth and how they relate to one another.

Now anyone at Replit can ask business intelligence questions and get a reliable answer. They can build charts and presentations from live data (including every chart in this post). The data team spends its time going deeper on the hardest problems, instead of fielding requests. Recently, a PM was able to self-serve complex launch analysis because our agent understands events in the codebase, how they show up in our customer data platform, and how to join those with complex subscription states.

![multi-chart](https://cdnimg.replit.com/images/bj34pdbp/migration/97969f2f088c8634154ab41fe4348ac2f9506d22-1999x1155.png?w=3840&q=80&fit=max&auto=format)

multi-chart

![autonomous-agent](https://cdnimg.replit.com/images/bj34pdbp/migration/293f72cb9bd9c40bc960ed3e541717e4eb8acd9f-1999x1155.png?w=3840&q=80&fit=max&auto=format)

autonomous-agent

Sales found the same leverage. The sales development team uses the agent to find and enrich product qualified leads, drawing on internal knowledge that more generic tools can’t see, so outreach lands with more context. Account executives use it to prepare for customer conversations to understand who is getting the most value, what projects are most active, and how credit usage tracks against their contract. This is all then packaged up into branded slides customized to the account. A self-driving sales team has more, higher quality touchpoints with their customers.

![slide example 1](https://cdnimg.replit.com/images/bj34pdbp/migration/ae15c552bcd6cdda008430d028e5de81c030cdb5-1999x1126.png?w=3840&q=80&fit=max&auto=format)

slide example 1

![16days](https://cdnimg.replit.com/images/bj34pdbp/migration/70b8695ec6542dadb9bf6fa3907ec744ab3c8bbf-1999x1126.png?w=3840&q=80&fit=max&auto=format)

![216 apps 42](https://cdnimg.replit.com/images/bj34pdbp/migration/5ea4d03ae53dff16d962aeeec9a46796b08c4e3c-1999x1126.png?w=3840&q=80&fit=max&auto=format)

216 apps 42

![activity and spend example slide](https://cdnimg.replit.com/images/bj34pdbp/migration/2f3b0ac6d301814b484b215bc85c75937e47494e-1999x1126.png?w=3840&q=80&fit=max&auto=format)

activity and spend example slide

Our marketing team can use the agent to draft product specs from scratch with a single prompt, based on conversations and documents products across engineering and product. This gives them the ability to start moving on launches sooner and stay up to date, without needing to be in every single meeting. They have more time to plan and be creative, which will ensure our releases have greater impact when they are out in the world.

![Nick Mclachlan](https://cdnimg.replit.com/images/bj34pdbp/migration/7f9c0bc390037a2efe654140f8f03ecac3b91e60-1924x198.png?w=3840&q=80&fit=max&auto=format)

Nick Mclachlan

![SEO Agent](https://cdnimg.replit.com/images/bj34pdbp/migration/31af13e75ab1491f5413c56c992eedcad79ed743-1066x1138.png?w=3840&q=80&fit=max&auto=format)

Our support team gave the agent skills to investigate issues and follow standard playbooks. It can choose to offer a response in our standard customer service voice, or escalate to engineering along with a summary of the ticket and investigation. A self-driving support team closes the hardest tickets (those escalated to humans) 60% faster. Users get back to building sooner.

![ticket time halved](https://cdnimg.replit.com/images/bj34pdbp/migration/1f0d854163cab213d54918fab7c4b8a141f9fcac-1280x720.jpg?w=3840&q=80&fit=max&auto=format)

ticket time halved

In every example, the human didn't get automated out. They got promoted. Self-driving turns doers into directors, and the people thriving are the ones who think in outcomes and set direction. That is the most valuable work there is now.

### Where to next?

Making ourselves more productive is exciting, but what really motivates the people at Replit is democratizing technology.

We want to bring this new way of working to all of our users. We’re hard at work making sure we can do this with the policy, permissions, security, and cost controls needed to deploy this at scale. Replit’s most active users are entrepreneurs and enterprise users building real businesses. Self-driving needs safety measures that can scale to meet those users.

We’re hard at work building that now.

Given all the graphs above, you won’t have to wait long.
